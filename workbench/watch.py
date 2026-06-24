from __future__ import annotations

import time
from pathlib import Path

from workbench.catalog import Catalog
from workbench.ingest import ingest_inbox
from workbench.paths import STAGE_DIRS


def watch_inbox(
    catalog: Catalog,
    *,
    profile: str | None = None,
    poll_interval_sec: float = 2.0,
    once: bool = False,
) -> None:
    inbox = STAGE_DIRS["inbox"]
    inbox.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()

    while True:
        current = {
            str(path.resolve())
            for path in inbox.iterdir()
            if path.is_file() and not path.name.startswith(".")
        }
        fresh = current - seen
        if fresh:
            results = ingest_inbox(catalog, profile=profile)
            for result in results:
                print(
                    f"[ingest] {result.rel_path} stage={result.stage} "
                    f"duplicate={result.duplicate} qc={result.qc_verdict}"
                )
            seen = current
        if once:
            break
        time.sleep(poll_interval_sec)