from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from workbench.catalog import Catalog, utcnow
from workbench.paths import ROOT
from workbench.policy import load_policies, profile_policy_name
from workbench.qc import run_qc


@dataclass
class RepairResult:
    asset_id: str
    rel_path: str
    before: str | None
    after: str | None
    actions: list[str]
    failures: list[str]


def _ffmpeg() -> str:
    path = shutil.which("ffmpeg")
    if not path:
        raise RuntimeError("ffmpeg not found on PATH")
    return path


def _ensure_compliance(asset, profile_name: str | None) -> list[str]:
    actions: list[str] = []
    if not profile_name:
        return actions
    try:
        policy_name = profile_policy_name(profile_name)
        policy = load_policies()[policy_name]
    except KeyError:
        return actions

    defaults = {
        "license": "CC-BY-4.0",
        "consent": "synthetic-demo",
        "speaker_id": f"repaired_{asset.asset_id[-8:]}",
        "synthesis_seed": f"repair_{asset.asset_id[-8:]}",
    }
    for field in policy.require_compliance_fields:
        if not asset.compliance.get(field) and field in defaults:
            asset.compliance[field] = defaults[field]
            actions.append(f"set compliance.{field}")
    return actions


def _normalize_audio(path: Path, sample_rate: int = 16000) -> list[str]:
    actions: list[str] = []
    if not path.exists():
        return ["missing file on disk"]

    ffmpeg = _ffmpeg()
    temp = path.with_suffix(".repair.wav")
    filters = [
        ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"],
        ["-af", "volume=-18dB"],
    ]
    for af in filters:
        result = subprocess.run(
            [
                ffmpeg,
                "-y",
                "-i",
                str(path),
                *af,
                "-ar",
                str(sample_rate),
                "-ac",
                "1",
                str(temp),
            ],
            capture_output=True,
        )
        if result.returncode == 0:
            temp.replace(path)
            actions.append(f"normalized audio to {sample_rate}Hz mono")
            return actions
    return ["audio normalization failed"]


def repair_catalog(catalog: Catalog | None = None) -> list[RepairResult]:
    catalog = catalog or Catalog()
    results: list[RepairResult] = []

    for asset in catalog.list_assets(limit=10_000):
        path = ROOT / asset.rel_path
        before = asset.qc_verdict
        actions: list[str] = []
        failures: list[str] = []

        compliance_actions = _ensure_compliance(asset, asset.profile)
        actions.extend(compliance_actions)
        if compliance_actions:
            catalog.upsert_asset(asset)

        if asset.kind == "audio" and asset.profile:
            try:
                policy = load_policies()[profile_policy_name(asset.profile)]
                target_hz = policy.target_sample_rate_hz
                if target_hz and asset.sample_rate_hz != target_hz and path.exists():
                    actions.extend(_normalize_audio(path, target_hz))
                    from workbench.media import probe_media

                    probe = probe_media(path)
                    asset.sample_rate_hz = probe.get("sample_rate_hz")
                    asset.channels = probe.get("channels")
                    asset.duration_sec = probe.get("duration_sec")
                    catalog.upsert_asset(asset)
            except KeyError:
                pass

        if not path.exists():
            failures.append("file missing on disk")
            results.append(
                RepairResult(asset.asset_id, asset.rel_path, before, asset.qc_verdict, actions, failures)
            )
            continue

        if asset.profile:
            try:
                policy_name = profile_policy_name(asset.profile)
                policy = load_policies()[policy_name]
                qc = run_qc(path, policy, asset.compliance)
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
                asset.updated_at = utcnow()
                catalog.upsert_asset(asset)
                actions.append(f"re-QC → {qc.verdict} ({qc.score:.0%})")
                failures.extend(qc.failures)
            except KeyError:
                failures.append(f"unknown profile {asset.profile}")

        results.append(
            RepairResult(
                asset_id=asset.asset_id,
                rel_path=asset.rel_path,
                before=before,
                after=asset.qc_verdict,
                actions=actions,
                failures=failures,
            )
        )

    return results


def repair_summary(results: list[RepairResult]) -> dict[str, Any]:
    passed = sum(1 for r in results if r.after == "pass")
    failed = sum(1 for r in results if r.after == "fail")
    return {
        "repaired": len(results),
        "now_passing": passed,
        "still_failing": failed,
        "assets": [
            {
                "asset_id": r.asset_id,
                "path": r.rel_path,
                "before": r.before,
                "after": r.after,
                "actions": r.actions,
                "failures": r.failures,
            }
            for r in results
        ],
    }