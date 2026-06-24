from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from workbench.catalog import Catalog
from workbench.export import export_jsonl, write_release_manifest
from workbench.ingest import ingest_inbox, ingest_path
from workbench.paths import ASSETS_DIR, ROOT, STAGE_DIRS
from workbench.policy import load_policies, load_profiles

CONFIG = yaml.safe_load((ROOT / "config" / "enterprise.yaml").read_text(encoding="utf-8"))
PRODUCT = CONFIG["product"]
API_KEY_REQUIRED = CONFIG["deployment"]["require_api_key"]
API_KEY_HEADER = CONFIG["deployment"]["api_key_header"]
EXPECTED_KEY = CONFIG["deployment"].get("api_key", "")

app = FastAPI(
    title=PRODUCT["name"],
    description=PRODUCT["tagline"],
    version=PRODUCT["version"],
    docs_url="/docs",
    redoc_url="/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MARKETING_DIR = ROOT / "marketing"
CONSOLE_DIR = ROOT / "console"
if MARKETING_DIR.exists():
    app.mount("/site", StaticFiles(directory=str(MARKETING_DIR), html=True), name="site")
if CONSOLE_DIR.exists():
    app.mount("/console", StaticFiles(directory=str(CONSOLE_DIR), html=True), name="console")


def verify_key(x_vaultline_key: str | None = Header(default=None, alias=API_KEY_HEADER)) -> None:
    if API_KEY_REQUIRED and x_vaultline_key != EXPECTED_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


class ComplianceUpdate(BaseModel):
    field: str
    value: str


class ReleaseRequest(BaseModel):
    profile: str
    version: str = "1.0.0"
    name: str | None = None
    notes: str = ""


class IngestRequest(BaseModel):
    path: str = "assets"
    profile: str | None = None
    inbox: bool = False


class DemoRequest(BaseModel):
    name: str
    email: str
    company: str
    message: str = ""


@app.get("/")
def root():
    return RedirectResponse(url="/site/index.html")


@app.get("/api")
def api_index() -> dict[str, str]:
    return {
        "product": PRODUCT["name"],
        "tagline": PRODUCT["tagline"],
        "app": "/site/index.html",
        "docs": "/docs",
        "console": "/console/index.html",
        "health": "/health",
    }


@app.get("/health")
def health() -> dict[str, Any]:
    catalog = Catalog()
    return {
        "status": "ok",
        "product": PRODUCT["name"],
        "version": PRODUCT["version"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "catalog": catalog.summary(),
    }


@app.get("/v1/dashboard", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
def dashboard() -> dict[str, Any]:
    catalog = Catalog()
    summary = catalog.summary()
    stages = {
        stage: len([p for p in folder.rglob("*") if p.is_file() and not p.name.startswith(".")])
        for stage, folder in STAGE_DIRS.items()
        if folder.exists()
    }
    return {
        "summary": summary,
        "stages_on_disk": stages,
        "profiles": list(load_profiles().get("profiles", {}).keys()),
        "policies": list(load_policies().keys()),
    }


@app.get("/v1/assets", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
def list_assets(
    stage: str | None = None,
    kind: str | None = None,
    qc_verdict: str | None = None,
    profile: str | None = None,
    limit: int = 200,
) -> list[dict[str, Any]]:
    catalog = Catalog()
    return [asset.__dict__ for asset in catalog.list_assets(stage=stage, kind=kind, qc_verdict=qc_verdict, profile=profile, limit=limit)]


@app.get("/v1/assets/{asset_id}", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
def get_asset(asset_id: str) -> dict[str, Any]:
    catalog = Catalog()
    asset = catalog.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset.__dict__


@app.get("/v1/assets/{asset_id}/lineage", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
def asset_lineage(asset_id: str) -> list[dict[str, Any]]:
    catalog = Catalog()
    chain = catalog.lineage(asset_id)
    if not chain:
        raise HTTPException(status_code=404, detail="No lineage for asset")
    return chain


@app.post("/v1/assets/{asset_id}/compliance", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
def set_compliance(asset_id: str, body: ComplianceUpdate) -> dict[str, str]:
    catalog = Catalog()
    asset = catalog.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    asset.compliance[body.field] = body.value
    catalog.upsert_asset(asset)
    catalog.record_provenance(
        asset_id=asset.asset_id,
        event_type="compliance_update",
        tool="vaultline-api",
        details={"field": body.field, "value": body.value},
    )
    return {"status": "updated", "asset_id": asset_id, "field": body.field}


@app.post("/v1/ingest", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
def ingest(body: IngestRequest) -> dict[str, Any]:
    catalog = Catalog()
    if body.inbox:
        results = ingest_inbox(catalog, profile=body.profile)
    else:
        target = (ROOT / body.path).resolve()
        if target.is_file():
            results = [ingest_path(catalog, target, profile=body.profile, run_quality_checks=bool(body.profile))]
        else:
            from workbench.ingest import scan_tree

            results = scan_tree(catalog, target, profile=body.profile, run_quality_checks=bool(body.profile))
    return {
        "ingested": len(results),
        "assets": [result.__dict__ for result in results],
    }


@app.post("/v1/uploads", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
async def upload_to_inbox(file: UploadFile = File(...), profile: str | None = None) -> dict[str, Any]:
    inbox = STAGE_DIRS["inbox"]
    inbox.mkdir(parents=True, exist_ok=True)
    dest = inbox / file.filename
    content = await file.read()
    dest.write_bytes(content)
    catalog = Catalog()
    from workbench.ingest import route_target, ingest_path
    import shutil

    routed = route_target(dest)
    routed.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(dest), str(routed))
    result = ingest_path(catalog, routed, profile=profile, run_quality_checks=bool(profile))
    return {"uploaded": file.filename, "result": result.__dict__}


@app.post("/v1/releases", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
def create_release(body: ReleaseRequest) -> dict[str, Any]:
    from workbench.export import eligible_for_release

    catalog = Catalog()
    profiles = load_profiles()["profiles"]
    if body.profile not in profiles:
        raise HTTPException(status_code=400, detail=f"Unknown profile: {body.profile}")
    profile = profiles[body.profile]
    assets = eligible_for_release(catalog, body.profile)
    if len(assets) < profile["release"]["min_assets"]:
        raise HTTPException(
            status_code=409,
            detail=f"Profile requires {profile['release']['min_assets']} passing assets; found {len(assets)}",
        )
    release_id = body.name or f"{body.profile}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    manifest_path = write_release_manifest(
        catalog,
        release_id=release_id,
        profile_name=body.profile,
        version=body.version,
        assets=assets,
        notes=body.notes,
    )
    return {
        "release_id": release_id,
        "asset_count": len(assets),
        "manifest": str(manifest_path.relative_to(ROOT)),
    }


@app.get("/v1/releases", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
def list_releases() -> list[dict[str, Any]]:
    return Catalog().list_releases()


@app.get("/v1/audit/export", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
def audit_export() -> JSONResponse:
    catalog = Catalog()
    assets = catalog.list_assets(limit=50_000)
    releases = catalog.list_releases()
    payload = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "product": PRODUCT["name"],
        "version": PRODUCT["version"],
        "asset_count": len(assets),
        "release_count": len(releases),
        "assets": [a.__dict__ for a in assets],
        "releases": releases,
    }
    export_dir = ROOT / "catalog" / "audit_exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    out = export_dir / f"audit_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return JSONResponse(content={"path": str(out.relative_to(ROOT)), "records": len(assets)})


@app.get("/v1/profiles", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
def profiles() -> dict[str, Any]:
    from dataclasses import asdict

    return {
        "profiles": load_profiles().get("profiles", {}),
        "policies": {k: asdict(v) for k, v in load_policies().items()},
    }


@app.get("/v1/commercial", dependencies=[Depends(verify_key)] if API_KEY_REQUIRED else [])
def commercial() -> dict[str, Any]:
    return CONFIG["commercial"]


@app.post("/v1/demo/run")
def demo_run(profile: str = "asr_corpus_v1") -> dict[str, Any]:
    from api.demo import run_live_demo

    try:
        return run_live_demo(profile=profile)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/v1/leads/demo-request")
def demo_request(body: DemoRequest) -> dict[str, str]:
    from api.demo import save_demo_request

    path = save_demo_request(body.model_dump())
    return {
        "status": "saved",
        "message": "Demo request received. We'll follow up at the email provided.",
        "path": str(path.relative_to(ROOT)),
    }


@app.get("/v1/leads/demo-request")
def list_demo_requests() -> list[dict[str, Any]]:
    path = ROOT / "leads" / "inbound" / "demo-requests.jsonl"
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows[-50:]


@app.get("/v1/quantum/status")
def quantum_status_endpoint() -> dict[str, Any]:
    from workbench.quantum import quantum_status

    return quantum_status()


@app.post("/v1/quantum/seed")
def quantum_seed(prefer_hardware: bool = False, asset_id: str | None = None) -> dict[str, Any]:
    from dataclasses import asdict

    from workbench.quantum import attach_seed_to_asset, generate_quantum_seed

    catalog = Catalog()
    try:
        seed = generate_quantum_seed(prefer_hardware=prefer_hardware)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    payload = asdict(seed)
    if asset_id:
        try:
            attach_seed_to_asset(catalog, asset_id, seed)
            payload["attached_to"] = asset_id
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
    return payload


@app.get("/v1/audit/download")
def audit_download():
    catalog = Catalog()
    assets = catalog.list_assets(limit=50_000)
    releases = catalog.list_releases()
    payload = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "product": PRODUCT["name"],
        "version": PRODUCT["version"],
        "asset_count": len(assets),
        "release_count": len(releases),
        "assets": [a.__dict__ for a in assets],
        "releases": releases,
    }
    export_dir = ROOT / "catalog" / "audit_exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    out = export_dir / f"audit_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return FileResponse(path=out, filename=out.name, media_type="application/json")


def main() -> None:
    import uvicorn

    host = CONFIG["deployment"]["api_host"]
    port = CONFIG["deployment"]["api_port"]
    uvicorn.run("api.server:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()