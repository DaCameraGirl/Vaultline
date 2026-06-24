from __future__ import annotations

import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from workbench.catalog import Asset, Catalog
from workbench.paths import MANIFESTS_DIR, RELEASES_DIR, ROOT


def asset_record(asset: Asset) -> dict[str, Any]:
    return {
        "asset_id": asset.asset_id,
        "path": asset.rel_path,
        "kind": asset.kind,
        "stage": asset.stage,
        "sha256": asset.sha256,
        "content_sig": asset.content_sig,
        "status": asset.status,
        "source_tool": asset.source_tool,
        "profile": asset.profile,
        "duration_sec": asset.duration_sec,
        "width": asset.width,
        "height": asset.height,
        "fps": asset.fps,
        "sample_rate_hz": asset.sample_rate_hz,
        "channels": asset.channels,
        "qc_score": asset.qc_score,
        "qc_verdict": asset.qc_verdict,
        "compliance": asset.compliance,
        "metadata": asset.metadata,
        "created_at": asset.created_at,
        "updated_at": asset.updated_at,
    }


def export_jsonl(catalog: Catalog, assets: list[Asset], output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for asset in assets:
            abs_path = ROOT / asset.rel_path
            row = {
                "id": asset.asset_id,
                "media_path": asset.rel_path,
                "media_type": asset.kind,
                "duration": asset.duration_sec,
                "sha256": asset.sha256,
                "qc_verdict": asset.qc_verdict,
                "source_tool": asset.source_tool,
                "text": asset.metadata.get("transcript", ""),
                "tags": asset.metadata.get("tags", []),
                "compliance": asset.compliance,
                "exists": abs_path.exists(),
            }
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return output


def export_huggingface(catalog: Catalog, assets: list[Asset], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    dataset = {
        "dataset_name": output_dir.name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "features": {
            "asset_id": "string",
            "path": "string",
            "kind": "string",
            "duration_sec": "float",
            "sha256": "string",
            "qc_verdict": "string",
            "transcript": "string",
            "tags": "list[string]",
        },
        "splits": {
            "train": [asset_record(asset) for asset in assets],
        },
    }
    manifest = output_dir / "dataset_info.json"
    manifest.write_text(json.dumps(dataset, indent=2), encoding="utf-8")

    jsonl = output_dir / "train.jsonl"
    export_jsonl(catalog, assets, jsonl)
    return manifest


def export_webdataset(catalog: Catalog, assets: list[Asset], output: Path, shard_size: int = 128) -> list[Path]:
    output.parent.mkdir(parents=True, exist_ok=True)
    shards: list[Path] = []
    for shard_index, start in enumerate(range(0, len(assets), shard_size)):
        shard_path = output.with_name(f"{output.stem}_{shard_index:05d}.tar")
        with tarfile.open(shard_path, "w") as tar:
            for offset, asset in enumerate(assets[start : start + shard_size]):
                abs_path = ROOT / asset.rel_path
                if not abs_path.exists():
                    continue
                arcname = f"{offset:06d}.{abs_path.suffix.lstrip('.')}"
                tar.add(abs_path, arcname=arcname)
                meta = json.dumps(asset_record(asset), indent=2).encode("utf-8")
                meta_info = tarfile.TarInfo(name=f"{offset:06d}.json")
                meta_info.size = len(meta)
                tar.addfile(meta_info, fileobj=_bytes_to_fileobj(meta))
        shards.append(shard_path)
    return shards


def _bytes_to_fileobj(data: bytes):
    import io

    return io.BytesIO(data)


def eligible_for_release(catalog: Catalog, profile_name: str) -> list[Asset]:
    assets = catalog.list_assets(profile=profile_name, qc_verdict="pass", limit=10_000)
    return [asset for asset in assets if asset.status in {"qc_pass", "registered"}]


def write_release_manifest(
    catalog: Catalog,
    *,
    release_id: str,
    profile_name: str,
    version: str,
    assets: list[Asset],
    notes: str = "",
) -> Path:
    release_dir = RELEASES_DIR / release_id
    release_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "release_id": release_id,
        "profile": profile_name,
        "version": version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "asset_count": len(assets),
        "notes": notes,
        "assets": [asset_record(asset) for asset in assets],
    }
    manifest_path = release_dir / "release_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    export_jsonl(catalog, assets, release_dir / "multimodal.jsonl")
    export_huggingface(catalog, assets, release_dir / "huggingface")
    export_webdataset(catalog, assets, release_dir / "webdataset.tar")

    catalog.create_release(
        release_id=release_id,
        profile_name=profile_name,
        version=version,
        asset_ids=[asset.asset_id for asset in assets],
        manifest_path=str(manifest_path.relative_to(ROOT)),
        notes=notes,
    )
    return manifest_path