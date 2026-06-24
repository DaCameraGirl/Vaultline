from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from workbench.paths import CONFIG_DIR


@dataclass
class QCPolicy:
    name: str
    description: str
    applies_to: list[str]
    min_duration_sec: float | None = None
    max_duration_sec: float | None = None
    min_width: int | None = None
    min_height: int | None = None
    target_fps: float | None = None
    fps_tolerance: float = 0.6
    target_sample_rate_hz: int | None = None
    target_channels: int | None = None
    min_loudness_lufs: float | None = None
    max_loudness_lufs: float | None = None
    max_silence_ratio: float | None = None
    min_blur_score: float | None = None
    require_compliance_fields: list[str] = field(default_factory=list)
    min_pass_score: float = 0.75


def load_policies() -> dict[str, QCPolicy]:
    path = CONFIG_DIR / "qc-policies.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    policies: dict[str, QCPolicy] = {}
    for name, spec in raw.get("policies", {}).items():
        policies[name] = QCPolicy(name=name, **spec)
    return policies


def load_profiles() -> dict[str, Any]:
    path = CONFIG_DIR / "dataset-profiles.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def profile_policy_name(profile_name: str) -> str:
    profiles = load_profiles()
    profile = profiles.get("profiles", {}).get(profile_name)
    if not profile:
        raise KeyError(f"Unknown dataset profile: {profile_name}")
    return profile["qc_policy"]