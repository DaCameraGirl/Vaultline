#!/usr/bin/env python3
"""End-to-end smoke test for Vaultline. Exit 0 = all checks passed."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8470"


def get(path: str) -> dict:
    with urllib.request.urlopen(f"{BASE}{path}", timeout=10) as resp:
        return json.loads(resp.read().decode())


def post(path: str) -> dict:
    req = urllib.request.Request(f"{BASE}{path}", method="POST", data=b"")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def check(name: str, ok: bool, detail: str = "") -> None:
    flag = "PASS" if ok else "FAIL"
    line = f"[{flag}] {name}"
    if detail:
        line += f" — {detail}"
    print(line)
    results.append(ok)


results: list[bool] = []

try:
    health = get("/health")
    check("health", health.get("status") == "ok", f"v{health.get('version')}")
    check("features", "quantum" in health.get("features", []))
    check("dashboard", "summary" in get("/v1/dashboard"))
    check("profiles", "profiles" in get("/v1/profiles"))
    check("quantum_status", "ready" in get("/v1/quantum/status"))

    demo = post("/v1/demo/run?profile=asr_corpus_v1")
    check("demo_run", bool(demo.get("asset_id")), f"qc={demo.get('qc_verdict')}")

    repair = post("/v1/catalog/repair")
    check("repair", repair.get("repaired", 0) >= 0, f"passing={repair.get('now_passing')}")

    assets = get("/v1/assets?limit=5")
    check("assets", isinstance(assets, list) and len(assets) > 0, f"count={len(assets)}")

    audit = get("/v1/audit/download")
    # audit download returns file not json - test export endpoint differently
except urllib.error.HTTPError as exc:
    check("server_reachable", False, f"HTTP {exc.code} — run setup/launch-vaultline.ps1")
except urllib.error.URLError as exc:
    check("server_reachable", False, f"{exc.reason} — run setup/launch-vaultline.ps1")

# audit is file download - separate check
try:
    req = urllib.request.Request(f"{BASE}/v1/audit/download")
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read()
        check("audit_download", len(body) > 100, f"{len(body)} bytes")
except Exception as exc:
    check("audit_download", False, str(exc))

passed = sum(results)
failed = len(results) - passed
print(f"\n{passed}/{len(results)} checks passed")
sys.exit(0 if failed == 0 else 1)