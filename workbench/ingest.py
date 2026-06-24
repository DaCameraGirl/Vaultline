from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from workbench.catalog import Asset, Catalog, utcnow
from workbench.fingerprints import content_signature, sha256_file
from workbench.media import classify_kind, probe_media
from workbench.paths import AUDIO_EXTS, IMAGE_EXTS, ROOT, STAGE_DIRS, VIDEO_EXTS
from workbench.policy import load_policies, profile_policy_name
from workbench.qc import run_qc


@dataclass
class IngestResult:
    asset_id: str
    rel_path: str
    stage: str
    duplicate: bool
    qc_verdict: str | None


def infer_source_tool(path: Path) -> str:
    lowered = str(path).lower()
    for tool in ("shotcut", "openshot", "lightworks", "ardour", "lmms"):
        if tool in lowered:
            return tool
    return "unknown"


def infer_stage(path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    if not parts or parts[0] != "assets":
        return "external"
    mapping = {
        "00_inbox": "inbox",
        "01_video_raw": "video_raw",
        "02_audio_raw": "audio_raw",
        "03_editing": "editing",
        "04_audio_stems": "audio_stems",
        "05_processed": "processed",
        "06_exports": "exports",
    }
    return mapping.get(parts[1], "external")


def asset_id_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    stem = re.sub(r"[^a-zA-Z0-9]+", "_", rel).strip("_").lower()
    return stem or path.stem.lower()


def route_target(path: Path) -> Path:
    ext = path.suffix.lower()
    if ext in VIDEO_EXTS | IMAGE_EXTS:
        return STAGE_DIRS["video_raw"] / path.name
    if ext in AUDIO_EXTS:
        return STAGE_DIRS["audio_raw"] / path.name
    raise ValueError(f"Unsupported file type: {path.suffix}")


def ingest_path(
    catalog: Catalog,
    path: Path,
    *,
    profile: str | None = None,
    run_quality_checks: bool = True,
    operator: str = "system",
) -> IngestResult:
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(path)

    digest = sha256_file(path)
    duplicates = catalog.find_by_sha256(digest)
    probe = probe_media(path) if path.suffix.lower() in VIDEO_EXTS | AUDIO_EXTS else {}
    kind = classify_kind(path, probe if probe else None)
    content_sig = content_signature(path, kind) if kind in {"video", "audio"} else digest

    near_dupes = catalog.find_by_content_sig(content_sig)
    duplicate = bool(duplicates or near_dupes)

    rel_path = path.relative_to(ROOT).as_posix()
    asset = Asset(
        asset_id=asset_id_for(path),
        rel_path=rel_path,
        kind=kind,
        stage=infer_stage(path),
        sha256=digest,
        content_sig=content_sig,
        status="duplicate" if duplicate else "registered",
        source_tool=infer_source_tool(path),
        profile=profile,
        duration_sec=probe.get("duration_sec"),
        width=probe.get("width"),
        height=probe.get("height"),
        fps=probe.get("fps"),
        sample_rate_hz=probe.get("sample_rate_hz"),
        channels=probe.get("channels"),
        updated_at=utcnow(),
    )
    catalog.upsert_asset(asset)
    catalog.record_provenance(
        asset_id=asset.asset_id,
        event_type="ingest",
        tool="workbench",
        operator=operator,
        output_hash=digest,
        details={"duplicate": duplicate, "profile": profile},
    )

    qc_verdict = None
    if run_quality_checks and profile and kind in {"video", "audio"}:
        policy_name = profile_policy_name(profile)
        policy = load_policies()[policy_name]
        result = run_qc(path, policy, asset.compliance)
        catalog.record_qc(
            asset_id=asset.asset_id,
            policy_name=policy_name,
            verdict=result.verdict,
            score=result.score,
            checks=result.checks,
        )
        qc_verdict = result.verdict
        asset.qc_score = result.score
        asset.qc_verdict = result.verdict
        asset.status = "qc_pass" if result.verdict == "pass" else "qc_fail"
        asset.updated_at = utcnow()
        catalog.upsert_asset(asset)

    return IngestResult(
        asset_id=asset.asset_id,
        rel_path=rel_path,
        stage=asset.stage,
        duplicate=duplicate,
        qc_verdict=qc_verdict,
    )


def ingest_inbox(
    catalog: Catalog,
    *,
    profile: str | None = None,
    operator: str = "system",
) -> list[IngestResult]:
    inbox = STAGE_DIRS["inbox"]
    results: list[IngestResult] = []
    for path in sorted(inbox.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        dest = route_target(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            continue
        shutil.move(str(path), str(dest))
        try:
            results.append(
                ingest_path(
                    catalog,
                    dest,
                    profile=profile,
                    run_quality_checks=bool(profile),
                    operator=operator,
                )
            )
        except Exception as exc:
            print(f"[ingest] failed {dest.name}: {exc}")
    return results


def scan_tree(
    catalog: Catalog,
    root: Path,
    *,
    profile: str | None = None,
    run_quality_checks: bool = False,
) -> list[IngestResult]:
    results: list[IngestResult] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.suffix.lower() not in VIDEO_EXTS | AUDIO_EXTS | IMAGE_EXTS:
            continue
        results.append(
            ingest_path(
                catalog,
                path,
                profile=profile,
                run_quality_checks=run_quality_checks,
            )
        )
    return results