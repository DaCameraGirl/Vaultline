from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


def require_ffmpeg() -> str:
    path = shutil.which("ffmpeg")
    if not path:
        raise RuntimeError("ffmpeg is required but was not found on PATH.")
    return path


def require_ffprobe() -> str:
    path = shutil.which("ffprobe")
    if not path:
        raise RuntimeError("ffprobe is required but was not found on PATH.")
    return path


def run_json(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    return json.loads(result.stdout)


def probe_media(path: Path) -> dict[str, Any]:
    ffprobe = require_ffprobe()
    try:
        payload = run_json(
            [
                ffprobe,
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                str(path),
            ]
        )
    except (RuntimeError, json.JSONDecodeError):
        return {
            "duration_sec": None,
            "width": None,
            "height": None,
            "fps": None,
            "sample_rate_hz": None,
            "channels": None,
            "video_codec": None,
            "audio_codec": None,
            "bitrate": None,
            "has_video": False,
            "has_audio": False,
        }
    streams = payload.get("streams", [])
    fmt = payload.get("format", {})
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)

    duration = None
    if fmt.get("duration"):
        duration = float(fmt["duration"])
    elif video and video.get("duration"):
        duration = float(video["duration"])
    elif audio and audio.get("duration"):
        duration = float(audio["duration"])

    fps = None
    if video:
        rate = video.get("avg_frame_rate") or video.get("r_frame_rate") or "0/1"
        num, _, den = rate.partition("/")
        if den and float(den) != 0:
            fps = float(num) / float(den)

    return {
        "duration_sec": duration,
        "width": int(video["width"]) if video and video.get("width") else None,
        "height": int(video["height"]) if video and video.get("height") else None,
        "fps": fps,
        "sample_rate_hz": int(audio["sample_rate"]) if audio and audio.get("sample_rate") else None,
        "channels": int(audio["channels"]) if audio and audio.get("channels") else None,
        "video_codec": video.get("codec_name") if video else None,
        "audio_codec": audio.get("codec_name") if audio else None,
        "bitrate": int(fmt["bit_rate"]) if fmt.get("bit_rate") else None,
        "has_video": video is not None,
        "has_audio": audio is not None,
    }


def classify_kind(path: Path, probe: dict[str, Any] | None = None) -> str:
    from workbench.paths import AUDIO_EXTS, IMAGE_EXTS, VIDEO_EXTS

    ext = path.suffix.lower()
    if probe is None:
        if ext in VIDEO_EXTS:
            return "video"
        if ext in AUDIO_EXTS:
            return "audio"
        if ext in IMAGE_EXTS:
            return "image"
        return "other"

    if ext in VIDEO_EXTS or probe.get("has_video"):
        return "video"
    if ext in AUDIO_EXTS or probe.get("has_audio"):
        return "audio"
    if ext in IMAGE_EXTS:
        return "image"
    return "other"