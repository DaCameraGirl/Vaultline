#!/usr/bin/env python3
"""Legacy entry point — use bench.py for all new workflows."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "bench.py"

ALIASES = {
    "status": ["dashboard"],
    "route-inbox": ["ingest", "--inbox"],
    "validate": ["qc", "--policy", "multimodal_video", "--path", "assets/06_exports"],
    "manifest": ["export", "--format", "jsonl", "--output", "manifests/dataset_manifest.json"],
}


def main() -> int:
    if len(sys.argv) < 2:
        print("SignalForge Workbench now uses bench.py")
        print("  python bench.py dashboard")
        print("  python bench.py ingest --inbox --profile multimodal_v1")
        return 1

    command = sys.argv[1]
    if command in {"-h", "--help"}:
        subprocess.run([sys.executable, str(BENCH), "--help"], check=False)
        return 0

    forwarded = ALIASES.get(command, [command, *sys.argv[2:]])
    result = subprocess.run([sys.executable, str(BENCH), *forwarded])
    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())