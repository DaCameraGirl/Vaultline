from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

from workbench.media import require_ffmpeg, require_ffprobe


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(chunk_size)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def content_signature(path: Path, kind: str) -> str:
    """Stable signature for near-duplicate detection."""
    if kind == "video":
        return _video_signature(path)
    if kind == "audio":
        return _audio_signature(path)
    return sha256_file(path)


def _video_signature(path: Path) -> str:
    try:
        ffprobe = require_ffprobe()
        result = subprocess.run(
            [
                ffprobe,
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=width,height,avg_frame_rate,duration",
                "-show_entries",
                "format=duration,size",
                "-of",
                "csv=p=0",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return sha256_file(path)
        frame = _extract_frame_hash(path)
        return hashlib.sha256(f"{result.stdout.strip()}|{frame}".encode()).hexdigest()
    except Exception:
        return sha256_file(path)


def _audio_signature(path: Path) -> str:
    try:
        ffprobe = require_ffprobe()
        result = subprocess.run(
            [
                ffprobe,
                "-v",
                "error",
                "-select_streams",
                "a:0",
                "-show_entries",
                "stream=sample_rate,channels,duration",
                "-show_entries",
                "format=duration,size",
                "-of",
                "csv=p=0",
                str(path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return sha256_file(path)
        return hashlib.sha256(result.stdout.strip().encode()).hexdigest()
    except Exception:
        return sha256_file(path)


def _extract_frame_hash(path: Path) -> str:
    try:
        ffmpeg = require_ffmpeg()
        result = subprocess.run(
            [
                ffmpeg,
                "-v",
                "error",
                "-i",
                str(path),
                "-vf",
                "select=eq(n\\,0),scale=32:32,format=gray",
                "-f",
                "rawvideo",
                "-",
            ],
            capture_output=True,
            check=False,
        )
        if result.returncode != 0 or not result.stdout:
            return sha256_file(path)
        return hashlib.sha256(result.stdout).hexdigest()
    except Exception:
        return sha256_file(path)