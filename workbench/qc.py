from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from workbench.media import classify_kind, probe_media, require_ffmpeg
from workbench.policy import QCPolicy


@dataclass
class QCResult:
    verdict: str
    score: float
    checks: dict[str, Any] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)


def run_qc(path: Path, policy: QCPolicy, compliance: dict[str, Any] | None = None) -> QCResult:
    probe = probe_media(path)
    kind = classify_kind(path, probe)
    checks: dict[str, Any] = {"kind": kind, "probe": probe}
    failures: list[str] = []
    passed = 0
    total = 0

    if kind not in policy.applies_to:
        return QCResult(verdict="skip", score=1.0, checks={"reason": f"{kind} not in policy scope"})

    def gate(name: str, ok: bool, detail: Any) -> None:
        nonlocal passed, total
        total += 1
        checks[name] = {"ok": ok, "detail": detail}
        if ok:
            passed += 1
        else:
            failures.append(f"{name}: {detail}")

    if policy.min_duration_sec is not None:
        duration = probe.get("duration_sec") or 0
        gate("duration_min", duration >= policy.min_duration_sec, duration)

    if policy.max_duration_sec is not None:
        duration = probe.get("duration_sec") or 0
        gate("duration_max", duration <= policy.max_duration_sec, duration)

    if kind == "video":
        if policy.min_width is not None:
            gate("width", (probe.get("width") or 0) >= policy.min_width, probe.get("width"))
        if policy.min_height is not None:
            gate("height", (probe.get("height") or 0) >= policy.min_height, probe.get("height"))
        if policy.target_fps is not None and probe.get("fps"):
            delta = abs(probe["fps"] - policy.target_fps)
            gate("fps", delta <= policy.fps_tolerance, probe.get("fps"))
        if policy.min_blur_score is not None:
            blur = _video_blur_score(path)
            checks["blur_score"] = blur
            gate("blur", blur >= policy.min_blur_score, blur)

    if kind in {"audio", "video"} and probe.get("has_audio"):
        if policy.target_sample_rate_hz is not None and probe.get("sample_rate_hz"):
            gate("sample_rate", probe["sample_rate_hz"] == policy.target_sample_rate_hz, probe["sample_rate_hz"])
        if policy.target_channels is not None and probe.get("channels"):
            gate("channels", probe["channels"] == policy.target_channels, probe["channels"])
        loudness = _integrated_loudness(path)
        checks["loudness_lufs"] = loudness
        loudness_valid = -70 < loudness < 0
        if loudness_valid:
            if policy.min_loudness_lufs is not None:
                gate("loudness_min", loudness >= policy.min_loudness_lufs, loudness)
            if policy.max_loudness_lufs is not None:
                gate("loudness_max", loudness <= policy.max_loudness_lufs, loudness)
        else:
            checks["loudness_skipped"] = "unreadable measurement — gate skipped"
        if policy.max_silence_ratio is not None:
            silence_ratio = _silence_ratio(path)
            checks["silence_ratio"] = silence_ratio
            gate("silence_ratio", silence_ratio <= policy.max_silence_ratio, silence_ratio)

    if policy.require_compliance_fields:
        compliance = compliance or {}
        missing = [field for field in policy.require_compliance_fields if not compliance.get(field)]
        gate("compliance", not missing, missing or "ok")

    score = passed / total if total else 1.0
    verdict = "pass" if score >= policy.min_pass_score and not failures else "fail"
    return QCResult(verdict=verdict, score=round(score, 4), checks=checks, failures=failures)


def _integrated_loudness(path: Path) -> float:
    ffmpeg = require_ffmpeg()
    result = subprocess.run(
        [ffmpeg, "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True,
        text=True,
    )
    match = re.search(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", result.stderr)
    if match:
        return float(match.group(1))
    return -999.0


def _silence_ratio(path: Path) -> float:
    ffmpeg = require_ffmpeg()
    result = subprocess.run(
        [
            ffmpeg,
            "-i",
            str(path),
            "-af",
            "silencedetect=noise=-35dB:d=0.35",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    probe = probe_media(path)
    duration = probe.get("duration_sec") or 1.0
    silent = 0.0
    starts: list[float] = []
    for line in result.stderr.splitlines():
        if "silence_start" in line:
            match = re.search(r"silence_start:\s*([\d.]+)", line)
            if match:
                starts.append(float(match.group(1)))
        if "silence_end" in line:
            match = re.search(r"silence_end:\s*([\d.]+)", line)
            if match and starts:
                start = starts.pop()
                silent += float(match.group(1)) - start
    return min(1.0, silent / duration)


def _video_blur_score(path: Path) -> float:
    ffmpeg = require_ffmpeg()
    result = subprocess.run(
        [
            ffmpeg,
            "-i",
            str(path),
            "-vf",
            "signalstats,metadata=print:file=-",
            "-frames:v",
            "45",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    )
    ydifs: list[float] = []
    for line in result.stderr.splitlines():
        if "lavfi.signalstats.YDIF" in line:
            match = re.search(r"YDIF=([\d.]+)", line)
            if match:
                ydifs.append(float(match.group(1)))
    if not ydifs:
        return 0.0
    return round(sum(ydifs) / len(ydifs), 4)