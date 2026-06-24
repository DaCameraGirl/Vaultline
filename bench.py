#!/usr/bin/env python3
"""SignalForge Workbench — industry-grade research media infrastructure."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from workbench.catalog import Asset, Catalog
from workbench.export import eligible_for_release, export_huggingface, export_jsonl, write_release_manifest
from workbench.ingest import ingest_inbox, ingest_path, scan_tree
from workbench.paths import ASSETS_DIR, ROOT, STAGE_DIRS
from workbench.policy import load_policies, load_profiles, profile_policy_name
from workbench.qc import run_qc
from workbench.watch import watch_inbox

try:
    from rich.console import Console
    from rich.table import Table

    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


def emit(message: str) -> None:
    if HAS_RICH:
        console.print(message)
    else:
        print(message)


def cmd_dashboard(_: argparse.Namespace) -> int:
    catalog = Catalog()
    summary = catalog.summary()
    if HAS_RICH:
        table = Table(title="SignalForge Workbench")
        table.add_column("Metric")
        table.add_column("Value", justify="right")
        table.add_row("Total assets", str(summary["total_assets"]))
        table.add_row("Releases", str(summary["releases"]))
        for verdict, count in sorted(summary["by_qc_verdict"].items()):
            table.add_row(f"QC · {verdict}", str(count))
        console.print(table)
        stage_table = Table(title="Pipeline stages")
        stage_table.add_column("Stage")
        stage_table.add_column("Catalogued", justify="right")
        stage_table.add_column("On disk", justify="right")
        for stage, folder in STAGE_DIRS.items():
            on_disk = len([p for p in folder.rglob("*") if p.is_file() and not p.name.startswith(".")]) if folder.exists() else 0
            stage_table.add_row(stage, str(summary["by_stage"].get(stage, 0)), str(on_disk))
        console.print(stage_table)
    else:
        emit(json.dumps(summary, indent=2))
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    catalog = Catalog()
    if args.inbox:
        results = ingest_inbox(catalog, profile=args.profile, operator=args.operator)
    else:
        target = (ROOT / args.path).resolve()
        if target.is_file():
            results = [
                ingest_path(
                    catalog,
                    target,
                    profile=args.profile,
                    run_quality_checks=bool(args.profile),
                    operator=args.operator,
                )
            ]
        else:
            results = scan_tree(
                catalog,
                target,
                profile=args.profile,
                run_quality_checks=bool(args.profile),
            )
    for result in results:
        emit(
            f"{result.asset_id} · {result.rel_path} · stage={result.stage} "
            f"dup={result.duplicate} qc={result.qc_verdict}"
        )
    emit(f"Ingested {len(results)} asset(s)")
    return 0


def cmd_qc(args: argparse.Namespace) -> int:
    catalog = Catalog()
    policies = load_policies()
    policy = policies[args.policy]
    target = (ROOT / args.path).resolve()
    paths = [target] if target.is_file() else [
        p for p in target.rglob("*") if p.is_file() and p.suffix.lower() in {".mp4", ".mov", ".mkv", ".wav", ".flac", ".mp3", ".m4a"}
    ]
    passed = failed = 0
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        asset = catalog.get_asset_by_path(rel)
        compliance = asset.compliance if asset else {}
        result = run_qc(path, policy, compliance)
        if asset:
            catalog.record_qc(
                asset_id=asset.asset_id,
                policy_name=args.policy,
                verdict=result.verdict,
                score=result.score,
                checks=result.checks,
            )
            asset.qc_score = result.score
            asset.qc_verdict = result.verdict
            asset.status = "qc_pass" if result.verdict == "pass" else "qc_fail"
            catalog.upsert_asset(asset)
        flag = "PASS" if result.verdict == "pass" else "FAIL"
        emit(f"[{flag}] {rel} score={result.score:.2f}")
        for failure in result.failures:
            emit(f"       - {failure}")
        passed += result.verdict == "pass"
        failed += result.verdict == "fail"
    emit(f"QC complete: {passed} passed, {failed} failed")
    return 1 if failed else 0


def cmd_lineage(args: argparse.Namespace) -> int:
    catalog = Catalog()
    chain = catalog.lineage(args.asset_id)
    if not chain:
        emit(f"No lineage recorded for {args.asset_id}")
        return 1
    emit(json.dumps(chain, indent=2))
    return 0


def cmd_catalog_search(args: argparse.Namespace) -> int:
    catalog = Catalog()
    assets = catalog.list_assets(
        stage=args.stage,
        kind=args.kind,
        qc_verdict=args.qc_verdict,
        profile=args.profile,
        limit=args.limit,
    )
    if HAS_RICH:
        table = Table(title="Catalog search")
        table.add_column("asset_id")
        table.add_column("path")
        table.add_column("kind")
        table.add_column("qc")
        table.add_column("tool")
        for asset in assets:
            table.add_row(
                asset.asset_id,
                asset.rel_path,
                asset.kind,
                asset.qc_verdict or "-",
                asset.source_tool,
            )
        console.print(table)
    else:
        emit(json.dumps([asset.__dict__ for asset in assets], indent=2, default=str))
    return 0


def cmd_compliance(args: argparse.Namespace) -> int:
    catalog = Catalog()
    asset = catalog.get_asset(args.asset_id)
    if not asset:
        raise SystemExit(f"Unknown asset: {args.asset_id}")
    asset.compliance[args.field] = args.value
    catalog.upsert_asset(asset)
    catalog.record_provenance(
        asset_id=asset.asset_id,
        event_type="compliance_update",
        tool="workbench",
        details={"field": args.field, "value": args.value},
    )
    emit(f"Set {args.asset_id} compliance.{args.field} = {args.value}")
    return 0


def cmd_release_create(args: argparse.Namespace) -> int:
    catalog = Catalog()
    profiles = load_profiles()["profiles"]
    profile = profiles[args.profile]
    assets = eligible_for_release(catalog, args.profile)
    if len(assets) < profile["release"]["min_assets"]:
        raise SystemExit(
            f"Profile {args.profile} requires {profile['release']['min_assets']} passing assets; found {len(assets)}"
        )
    release_id = args.name or f"{args.profile}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    manifest_path = write_release_manifest(
        catalog,
        release_id=release_id,
        profile_name=args.profile,
        version=args.version,
        assets=assets,
        notes=args.notes,
    )
    emit(f"Release {release_id} created with {len(assets)} asset(s)")
    emit(f"Manifest: {manifest_path.relative_to(ROOT)}")
    return 0


def cmd_release_list(_: argparse.Namespace) -> int:
    catalog = Catalog()
    releases = catalog.list_releases()
    if HAS_RICH:
        table = Table(title="Releases")
        table.add_column("release_id")
        table.add_column("profile")
        table.add_column("version")
        table.add_column("assets", justify="right")
        table.add_column("created")
        for release in releases:
            table.add_row(
                release["release_id"],
                release["profile_name"],
                release["version"],
                str(release["asset_count"]),
                release["created_at"],
            )
        console.print(table)
    else:
        emit(json.dumps(releases, indent=2))
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    catalog = Catalog()
    assets = catalog.list_assets(
        profile=args.profile,
        qc_verdict="pass" if args.passing_only else None,
        limit=10_000,
    )
    if not assets:
        raise SystemExit("No assets matched export criteria.")
    output = ROOT / args.output
    if args.format == "jsonl":
        path = export_jsonl(catalog, assets, output)
    elif args.format == "huggingface":
        path = export_huggingface(catalog, assets, output)
    else:
        raise SystemExit(f"Unknown format: {args.format}")
    emit(f"Exported {len(assets)} asset(s) to {path.relative_to(ROOT)}")
    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    catalog = Catalog()
    emit(f"Watching {STAGE_DIRS['inbox']} (profile={args.profile or 'none'})")
    watch_inbox(catalog, profile=args.profile, once=args.once)
    return 0


def cmd_profiles(_: argparse.Namespace) -> int:
    profiles = load_profiles()["profiles"]
    policies = load_policies()
    if HAS_RICH:
        table = Table(title="Dataset profiles")
        table.add_column("profile")
        table.add_column("qc_policy")
        table.add_column("min_assets", justify="right")
        table.add_column("description")
        for name, spec in profiles.items():
            table.add_row(
                name,
                spec["qc_policy"],
                str(spec["release"]["min_assets"]),
                spec["description"],
            )
        console.print(table)
        policy_table = Table(title="QC policies")
        policy_table.add_column("policy")
        policy_table.add_column("applies_to")
        policy_table.add_column("min_pass", justify="right")
        for name, policy in policies.items():
            policy_table.add_row(name, ", ".join(policy.applies_to), f"{policy.min_pass_score:.2f}")
        console.print(policy_table)
    else:
        emit(json.dumps(profiles, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bench",
        description="SignalForge Workbench — research media asset infrastructure",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("dashboard", help="Operational overview").set_defaults(func=cmd_dashboard)
    sub.add_parser("profiles", help="List dataset profiles and QC policies").set_defaults(func=cmd_profiles)

    ingest = sub.add_parser("ingest", help="Register assets in the catalog with optional QC")
    ingest.add_argument("--path", default="assets", help="File or directory to ingest")
    ingest.add_argument("--inbox", action="store_true", help="Route and ingest inbox files")
    ingest.add_argument("--profile", help="Dataset profile for immediate QC gating")
    ingest.add_argument("--operator", default="system")
    ingest.set_defaults(func=cmd_ingest)

    qc = sub.add_parser("qc", help="Run QC policy against assets")
    qc.add_argument("--path", default="assets/06_exports")
    qc.add_argument("--policy", required=True)
    qc.set_defaults(func=cmd_qc)

    lineage = sub.add_parser("lineage", help="Show provenance chain for an asset")
    lineage.add_argument("asset_id")
    lineage.set_defaults(func=cmd_lineage)

    search = sub.add_parser("catalog", help="Search the asset catalog")
    search.add_argument("--stage")
    search.add_argument("--kind")
    search.add_argument("--qc-verdict")
    search.add_argument("--profile")
    search.add_argument("--limit", type=int, default=100)
    search.set_defaults(func=cmd_catalog_search)

    compliance = sub.add_parser("compliance", help="Set compliance metadata on an asset")
    compliance.add_argument("--asset", dest="asset_id", required=True)
    compliance.add_argument("--field", required=True)
    compliance.add_argument("--value", required=True)
    compliance.set_defaults(func=cmd_compliance)

    release = sub.add_parser("release", help="Release management")
    release_sub = release.add_subparsers(dest="release_command", required=True)
    create = release_sub.add_parser("create", help="Create an immutable dataset release")
    create.add_argument("--profile", required=True)
    create.add_argument("--version", default="1.0.0")
    create.add_argument("--name")
    create.add_argument("--notes", default="")
    create.set_defaults(func=cmd_release_create)
    release_sub.add_parser("list", help="List releases").set_defaults(func=cmd_release_list)

    export = sub.add_parser("export", help="Export catalog to training formats")
    export.add_argument("--format", choices=["jsonl", "huggingface"], default="jsonl")
    export.add_argument("--profile")
    export.add_argument("--output", default="manifests/export.jsonl")
    export.add_argument("--passing-only", action="store_true")
    export.set_defaults(func=cmd_export)

    watch = sub.add_parser("watch", help="Watch inbox and auto-ingest")
    watch.add_argument("--profile")
    watch.add_argument("--once", action="store_true")
    watch.set_defaults(func=cmd_watch)

    return parser


def main() -> int:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())