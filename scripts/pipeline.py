#!/usr/bin/env python3
"""CLI for the AI Research Media Workbench asset pipeline."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
ASSETS_DIR = ROOT / "assets"
MANIFESTS_DIR = ROOT / "manifests"

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".avi"}
AUDIO_EXTS = {".wav", ".flac", ".mp3", ".ogg", ".m4a", ".aac"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


@dataclass
class AssetRecord:
    id: str
    path: str
    kind: str
    status: str
    duration_sec: float | None = None
    width: int | None = None
    height: int | None = None
    fps: float | None = None
    sample_rate_hz: int | None = None
    channels: int | None = None
    tags: list[str] = field(default_factory=list)
    source_tool: str = "unknown"
    notes: str = ""
    issues: list[str] = field(default_factory=list)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def require_ffmpeg() -> str:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg is required but was not found on PATH.")
    return ffmpeg


def require_ffprobe() -> str:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise SystemExit("ffprobe is required but was not found on PATH.")
    return ffprobe


def run_json_command(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def probe_media(path: Path) -> dict[str, Any]:
    ffprobe = require_ffprobe()
    payload = run_json_command(
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
        "has_video": video is not None,
        "has_audio": audio is not None,
    }


def classify_kind(path: Path, probe: dict[str, Any]) -> str:
    ext = path.suffix.lower()
    if ext in VIDEO_EXTS or probe.get("has_video"):
        return "video"
    if ext in AUDIO_EXTS or probe.get("has_audio"):
        return "audio"
    if ext in IMAGE_EXTS:
        return "image"
    return "other"


def infer_source_tool(path: Path) -> str:
    lowered = str(path).lower()
    for tool in ("shotcut", "openshot", "lightworks", "ardour", "lmms"):
        if tool in lowered:
            return tool
    return "unknown"


def asset_id_for(path: Path, root: Path) -> str:
    rel = path.relative_to(root).as_posix()
    stem = re.sub(r"[^a-zA-Z0-9]+", "_", rel).strip("_").lower()
    return stem or path.stem.lower()


def collect_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(
        p for p in target.rglob("*") if p.is_file() and not p.name.startswith(".")
    )


def validate_asset(path: Path, preset: dict[str, Any], root: Path) -> AssetRecord:
    rel_path = path.relative_to(root).as_posix()
    record = AssetRecord(
        id=asset_id_for(path, root),
        path=rel_path,
        kind="other",
        status="pending",
        source_tool=infer_source_tool(path),
    )

    try:
        probe = probe_media(path)
    except (subprocess.CalledProcessError, json.JSONDecodeError, ValueError):
        record.status = "invalid"
        record.issues.append("ffprobe could not read this file")
        return record

    record.kind = classify_kind(path, probe)
    record.duration_sec = probe.get("duration_sec")
    record.width = probe.get("width")
    record.height = probe.get("height")
    record.fps = probe.get("fps")
    record.sample_rate_hz = probe.get("sample_rate_hz")
    record.channels = probe.get("channels")

    issues: list[str] = []

    if record.kind == "video":
        expected = preset
        if record.width and record.width != expected.get("width"):
            issues.append(f"width {record.width} != expected {expected.get('width')}")
        if record.height and record.height != expected.get("height"):
            issues.append(f"height {record.height} != expected {expected.get('height')}")
        if record.fps and expected.get("fps") and abs(record.fps - expected["fps"]) > 0.6:
            issues.append(f"fps {record.fps:.2f} != expected {expected.get('fps')}")
    elif record.kind == "audio":
        expected = preset
        if record.sample_rate_hz and record.sample_rate_hz != expected.get("sample_rate_hz"):
            issues.append(
                f"sample rate {record.sample_rate_hz} != expected {expected.get('sample_rate_hz')}"
            )
        if record.channels and record.channels != expected.get("channels"):
            issues.append(f"channels {record.channels} != expected {expected.get('channels')}")

    record.issues = issues
    record.status = "valid" if not issues else "invalid"
    return record


def choose_preset(record: AssetRecord, presets: dict[str, Any]) -> dict[str, Any] | None:
    if record.kind == "video":
        if record.height and record.height >= 1080:
            return presets["video"]["training_1080p"]
        return presets["video"]["training_720p"]
    if record.kind == "audio":
        if record.sample_rate_hz == 16000:
            return presets["audio"]["speech_asr"]
        return presets["audio"]["speech_tts"]
    return None


def cmd_status(_: argparse.Namespace) -> int:
    stages = [
        ("Inbox", ASSETS_DIR / "00_inbox"),
        ("Video raw", ASSETS_DIR / "01_video_raw"),
        ("Audio raw", ASSETS_DIR / "02_audio_raw"),
        ("Editing", ASSETS_DIR / "03_editing"),
        ("Audio stems", ASSETS_DIR / "04_audio_stems"),
        ("Processed", ASSETS_DIR / "05_processed"),
        ("Exports", ASSETS_DIR / "06_exports"),
    ]
    print(f"Project root: {ROOT}")
    print()
    for label, folder in stages:
        files = collect_files(folder) if folder.exists() else []
        media = [f for f in files if f.suffix.lower() in VIDEO_EXTS | AUDIO_EXTS | IMAGE_EXTS]
        print(f"{label:12} {len(media):4} media file(s)  ({folder.relative_to(ROOT)})")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    presets = load_yaml(CONFIG_DIR / "export-presets.yaml")
    target = (ROOT / args.path).resolve()
    if not target.exists():
        raise SystemExit(f"Path not found: {target}")

    preset_key = args.preset
    if preset_key:
        section, _, name = preset_key.partition(".")
        preset = presets.get(section, {}).get(name)
        if not preset:
            raise SystemExit(f"Unknown preset: {preset_key}")
    else:
        preset = presets["video"]["training_720p"]

    records: list[AssetRecord] = []
    for path in collect_files(target):
        if path.suffix.lower() not in VIDEO_EXTS | AUDIO_EXTS:
            continue
        if preset_key:
            record = validate_asset(path, preset, ROOT)
        else:
            probe = probe_media(path)
            record = AssetRecord(
                id=asset_id_for(path, ROOT),
                path=path.relative_to(ROOT).as_posix(),
                kind=classify_kind(path, probe),
                status="pending",
                duration_sec=probe.get("duration_sec"),
                width=probe.get("width"),
                height=probe.get("height"),
                fps=probe.get("fps"),
                sample_rate_hz=probe.get("sample_rate_hz"),
                channels=probe.get("channels"),
                source_tool=infer_source_tool(path),
            )
            chosen = choose_preset(record, presets)
            if chosen:
                record = validate_asset(path, chosen, ROOT)
        records.append(record)

    valid = sum(1 for r in records if r.status == "valid")
    invalid = sum(1 for r in records if r.status == "invalid")
    print(f"Checked {len(records)} file(s): {valid} valid, {invalid} invalid")
    for record in records:
        flag = "OK" if record.status == "valid" else "!!"
        detail = f"{record.kind}"
        if record.width and record.height:
            detail += f" {record.width}x{record.height}"
        if record.fps:
            detail += f" @{record.fps:.2f}fps"
        if record.sample_rate_hz:
            detail += f" {record.sample_rate_hz}Hz"
        print(f"[{flag}] {record.path} ({detail})")
        for issue in record.issues:
            print(f"      - {issue}")

    if args.write_manifest:
        manifest_path = MANIFESTS_DIR / f"validation_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        write_manifest(records, manifest_path, preset_name=args.preset or "auto")
        print(f"\nWrote manifest: {manifest_path.relative_to(ROOT)}")

    return 1 if invalid else 0


def write_manifest(records: list[AssetRecord], output: Path, preset_name: str) -> None:
    payload = {
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project": ROOT.name,
        "preset": preset_name,
        "assets": [asdict(record) for record in records],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def cmd_manifest(args: argparse.Namespace) -> int:
    target = (ROOT / args.path).resolve()
    if not target.exists():
        raise SystemExit(f"Path not found: {target}")

    presets = load_yaml(CONFIG_DIR / "export-presets.yaml")
    records: list[AssetRecord] = []
    for path in collect_files(target):
        if path.suffix.lower() not in VIDEO_EXTS | AUDIO_EXTS | IMAGE_EXTS:
            continue
        probe = probe_media(path)
        record = AssetRecord(
            id=asset_id_for(path, ROOT),
            path=path.relative_to(ROOT).as_posix(),
            kind=classify_kind(path, probe),
            status="pending",
            duration_sec=probe.get("duration_sec"),
            width=probe.get("width"),
            height=probe.get("height"),
            fps=probe.get("fps"),
            sample_rate_hz=probe.get("sample_rate_hz"),
            channels=probe.get("channels"),
            source_tool=infer_source_tool(path),
        )
        chosen = choose_preset(record, presets)
        if chosen:
            validated = validate_asset(path, chosen, ROOT)
            record.status = validated.status
            record.issues = validated.issues
        else:
            record.status = "valid"
        records.append(record)

    output = MANIFESTS_DIR / args.output
    write_manifest(records, output, preset_name="auto")
    print(f"Wrote {len(records)} asset(s) to {output.relative_to(ROOT)}")
    return 0


def cmd_normalize_audio(args: argparse.Namespace) -> int:
    ffmpeg = require_ffmpeg()
    presets = load_yaml(CONFIG_DIR / "export-presets.yaml")
    preset = presets["audio"][args.preset]
    target = (ROOT / args.input).resolve()
    output_dir = (ROOT / args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    files = [
        p
        for p in collect_files(target)
        if p.suffix.lower() in AUDIO_EXTS and p.is_file()
    ]
    if not files:
        raise SystemExit(f"No audio files found under {target}")

    for src in files:
        rel = src.relative_to(target) if target in src.parents else Path(src.name)
        dest = output_dir / rel.with_suffix(f".{preset['format']}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        command = [
            ffmpeg,
            "-y",
            "-i",
            str(src),
            "-vn",
            "-ac",
            str(preset["channels"]),
            "-ar",
            str(preset["sample_rate_hz"]),
            "-sample_fmt",
            "s16" if preset["bit_depth"] == 16 else "s32",
            "-af",
            f"loudnorm=I={preset['loudness_lufs']}:TP=-1.5:LRA=11",
            str(dest),
        ]
        print(f"Normalizing {src.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
        subprocess.run(command, check=True)

    print(f"Normalized {len(files)} file(s) into {output_dir.relative_to(ROOT)}")
    return 0


def cmd_segment(args: argparse.Namespace) -> int:
    ffmpeg = require_ffmpeg()
    presets = load_yaml(CONFIG_DIR / "export-presets.yaml")
    video_preset = presets["video"][args.preset]
    src = (ROOT / args.input).resolve()
    output_dir = (ROOT / args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        raise SystemExit(f"Input not found: {src}")

    probe = probe_media(src)
    duration = probe.get("duration_sec") or 0
    if duration <= 0:
        raise SystemExit("Could not determine input duration.")

    segment_len = args.length
    stem = src.stem
    index = 0
    start = 0.0
    created = 0

    while start < duration:
        out = output_dir / f"{stem}_{index:04d}.mp4"
        command = [
            ffmpeg,
            "-y",
            "-ss",
            str(start),
            "-i",
            str(src),
            "-t",
            str(segment_len),
            "-vf",
            f"scale={video_preset['width']}:{video_preset['height']}:force_original_aspect_ratio=decrease,"
            f"pad={video_preset['width']}:{video_preset['height']}:(ow-iw)/2:(oh-ih)/2",
            "-r",
            str(video_preset["fps"]),
            "-c:v",
            "libx264",
            "-pix_fmt",
            video_preset["pixel_format"],
            "-crf",
            str(video_preset["crf"]),
            "-c:a",
            "aac",
            "-b:a",
            f"{video_preset['audio_bitrate_kbps']}k",
            str(out),
        ]
        print(f"Writing {out.relative_to(ROOT)} (start={start:.2f}s)")
        subprocess.run(command, check=True)
        created += 1
        index += 1
        start += segment_len

    print(f"Created {created} segment(s) in {output_dir.relative_to(ROOT)}")
    return 0


def cmd_route_inbox(args: argparse.Namespace) -> int:
    inbox = ASSETS_DIR / "00_inbox"
    video_out = ASSETS_DIR / "01_video_raw"
    audio_out = ASSETS_DIR / "02_audio_raw"
    video_out.mkdir(parents=True, exist_ok=True)
    audio_out.mkdir(parents=True, exist_ok=True)

    moved = 0
    for path in collect_files(inbox):
        if path.suffix.lower() in VIDEO_EXTS | IMAGE_EXTS:
            dest = video_out / path.name
        elif path.suffix.lower() in AUDIO_EXTS:
            dest = audio_out / path.name
        else:
            print(f"Skipping unsupported file: {path.name}")
            continue
        if dest.exists():
            print(f"Already exists, skipping: {dest.name}")
            continue
        shutil.move(str(path), str(dest))
        print(f"Moved {path.name} -> {dest.parent.name}/")
        moved += 1

    print(f"Routed {moved} file(s) from inbox")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show asset counts by pipeline stage")

    validate = sub.add_parser("validate", help="Validate assets against export presets")
    validate.add_argument("--path", default="assets/06_exports", help="Folder or file to validate")
    validate.add_argument(
        "--preset",
        help="Preset key, e.g. video.training_720p or audio.speech_asr",
    )
    validate.add_argument("--write-manifest", action="store_true", help="Save results to manifests/")
    validate.set_defaults(func=cmd_validate)

    manifest = sub.add_parser("manifest", help="Build a JSON manifest for a folder")
    manifest.add_argument("--path", default="assets/06_exports", help="Folder to scan")
    manifest.add_argument("--output", default="dataset_manifest.json", help="Output filename")
    manifest.set_defaults(func=cmd_manifest)

    normalize = sub.add_parser("normalize-audio", help="Normalize audio via ffmpeg loudnorm")
    normalize.add_argument("--input", default="assets/04_audio_stems", help="Input folder")
    normalize.add_argument("--output", default="assets/05_processed/audio", help="Output folder")
    normalize.add_argument("--preset", choices=["speech_asr", "speech_tts", "music_sfx"], default="speech_asr")
    normalize.set_defaults(func=cmd_normalize_audio)

    segment = sub.add_parser("segment", help="Split a video into fixed-length training clips")
    segment.add_argument("--input", required=True, help="Source video path")
    segment.add_argument("--output", default="assets/05_processed/video", help="Output folder")
    segment.add_argument("--length", type=float, default=5.0, help="Segment length in seconds")
    segment.add_argument(
        "--preset",
        choices=["training_720p", "training_1080p"],
        default="training_720p",
    )
    segment.set_defaults(func=cmd_segment)

    route = sub.add_parser("route-inbox", help="Move inbox files into raw video/audio folders")
    route.set_defaults(func=cmd_route_inbox)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "status":
        return cmd_status(args)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())