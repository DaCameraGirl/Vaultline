from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
ASSETS_DIR = ROOT / "assets"
CATALOG_DIR = ROOT / "catalog"
RELEASES_DIR = ROOT / "releases"
MANIFESTS_DIR = ROOT / "manifests"
DB_PATH = CATALOG_DIR / "catalog.db"

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}
AUDIO_EXTS = {".wav", ".flac", ".mp3", ".ogg", ".m4a", ".aac", ".wma"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}

STAGE_DIRS = {
    "inbox": ASSETS_DIR / "00_inbox",
    "video_raw": ASSETS_DIR / "01_video_raw",
    "audio_raw": ASSETS_DIR / "02_audio_raw",
    "editing": ASSETS_DIR / "03_editing",
    "audio_stems": ASSETS_DIR / "04_audio_stems",
    "processed": ASSETS_DIR / "05_processed",
    "exports": ASSETS_DIR / "06_exports",
}