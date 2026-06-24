from __future__ import annotations

import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from workbench.catalog import Catalog
from workbench.ingest import ingest_path
from workbench.paths import ROOT, STAGE_DIRS
from workbench.policy import load_policies
from workbench.qc import run_qc


def _ffmpeg() -> str:
    import shutil

    path = shutil.which("ffmpeg")
    if not path:
        raise RuntimeError("ffmpeg not found on PATH")
    return path


def run_live_demo(profile: str = "asr_corpus_v1") -> dict[str, Any]:
    """Generate sample media, ingest, tag compliance, run QC — returns a visible activity log."""
    catalog = Catalog()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    uid = uuid.uuid4().hex[:8]
    audio_dir = STAGE_DIRS["audio_raw"]
    audio_dir.mkdir(parents=True, exist_ok=True)
    audio_path = audio_dir / f"demo_speech_{stamp}_{uid}.wav"

    log: list[dict[str, str]] = []

    def step(name: str, detail: str, status: str = "ok") -> None:
        log.append({"step": name, "detail": detail, "status": status})

    step("generate", f"Creating sample speech clip {audio_path.name}")
    raw_path = audio_path.with_suffix(".raw.wav")
    subprocess.run(
        [
            _ffmpeg(),
            "-y",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=440:duration=3",
            "-ar",
            "16000",
            "-ac",
            "1",
            str(raw_path),
        ],
        capture_output=True,
        check=True,
    )
    step("normalize", "Normalizing loudness for ASR QC gates")
    filters = [
        ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"],
        ["-af", "volume=-18dB"],
    ]
    normalized = False
    for af in filters:
        result = subprocess.run(
            [_ffmpeg(), "-y", "-i", str(raw_path), *af, "-ar", "16000", "-ac", "1", str(audio_path)],
            capture_output=True,
        )
        if result.returncode == 0:
            normalized = True
            break
    if not normalized:
        raise RuntimeError("Audio normalization failed — check ffmpeg install")
    raw_path.unlink(missing_ok=True)

    step("ingest", "Registering asset in catalog with SHA-256 + content signature")
    result = ingest_path(catalog, audio_path, profile=profile, run_quality_checks=True)
    asset = catalog.get_asset(result.asset_id)
    if not asset:
        raise RuntimeError("Demo ingest failed")

    step("compliance", "Attaching license + consent metadata")
    asset.compliance["license"] = "CC-BY-4.0"
    asset.compliance["consent"] = "synthetic-demo"
    asset.compliance["speaker_id"] = f"demo_{uid}"
    catalog.upsert_asset(asset)
    catalog.record_provenance(
        asset_id=asset.asset_id,
        event_type="compliance_update",
        tool="vaultline-demo",
        details={"license": "CC-BY-4.0", "consent": "synthetic-demo"},
    )

    from workbench.policy import profile_policy_name

    policy_name = profile_policy_name(profile)
    policy = load_policies()[policy_name]
    qc = run_qc(audio_path, policy, asset.compliance)
    catalog.record_qc(
        asset_id=asset.asset_id,
        policy_name=policy_name,
        verdict=qc.verdict,
        score=qc.score,
        checks=qc.checks,
    )
    asset.qc_score = qc.score
    asset.qc_verdict = qc.verdict
    asset.status = "qc_pass" if qc.verdict == "pass" else "qc_fail"
    catalog.upsert_asset(asset)

    step(
        "qc",
        f"Policy {policy_name}: {qc.verdict.upper()} (score {qc.score:.0%})",
        status="ok" if qc.verdict == "pass" else "warn",
    )

    if qc.failures:
        for failure in qc.failures:
            step("qc_check", failure, status="warn")

    step("lineage", f"Provenance events recorded for {asset.asset_id}")
    step("ready", "Asset is in catalog — visible in console and API")

    return {
        "asset_id": asset.asset_id,
        "path": asset.rel_path,
        "qc_verdict": asset.qc_verdict,
        "qc_score": asset.qc_score,
        "profile": profile,
        "log": log,
        "catalog": catalog.summary(),
    }


def save_demo_request(payload: dict[str, Any]) -> Path:
    leads_dir = ROOT / "leads" / "inbound"
    leads_dir.mkdir(parents=True, exist_ok=True)
    out = leads_dir / "demo-requests.jsonl"
    row = {"received_at": datetime.now(timezone.utc).isoformat(), **payload}
    with out.open("a", encoding="utf-8") as handle:
        import json

        handle.write(json.dumps(row) + "\n")
    return out