from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from workbench.paths import DB_PATH


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Asset:
    asset_id: str
    rel_path: str
    kind: str
    stage: str
    sha256: str
    content_sig: str
    status: str = "registered"
    source_tool: str = "unknown"
    profile: str | None = None
    duration_sec: float | None = None
    width: int | None = None
    height: int | None = None
    fps: float | None = None
    sample_rate_hz: int | None = None
    channels: int | None = None
    qc_score: float | None = None
    qc_verdict: str | None = None
    compliance: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utcnow)
    updated_at: str = field(default_factory=utcnow)


class Catalog:
    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS assets (
                    asset_id TEXT PRIMARY KEY,
                    rel_path TEXT NOT NULL UNIQUE,
                    kind TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    content_sig TEXT NOT NULL,
                    status TEXT NOT NULL,
                    source_tool TEXT NOT NULL,
                    profile TEXT,
                    duration_sec REAL,
                    width INTEGER,
                    height INTEGER,
                    fps REAL,
                    sample_rate_hz INTEGER,
                    channels INTEGER,
                    qc_score REAL,
                    qc_verdict TEXT,
                    compliance_json TEXT NOT NULL DEFAULT '{}',
                    metadata_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_assets_stage ON assets(stage);
                CREATE INDEX IF NOT EXISTS idx_assets_kind ON assets(kind);
                CREATE INDEX IF NOT EXISTS idx_assets_sha256 ON assets(sha256);
                CREATE INDEX IF NOT EXISTS idx_assets_content_sig ON assets(content_sig);
                CREATE INDEX IF NOT EXISTS idx_assets_qc_verdict ON assets(qc_verdict);

                CREATE TABLE IF NOT EXISTS provenance (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset_id TEXT NOT NULL,
                    parent_asset_id TEXT,
                    event_type TEXT NOT NULL,
                    tool TEXT NOT NULL,
                    operator TEXT,
                    input_hash TEXT,
                    output_hash TEXT,
                    details_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
                );

                CREATE INDEX IF NOT EXISTS idx_provenance_asset ON provenance(asset_id);
                CREATE INDEX IF NOT EXISTS idx_provenance_parent ON provenance(parent_asset_id);

                CREATE TABLE IF NOT EXISTS qc_results (
                    qc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset_id TEXT NOT NULL,
                    policy_name TEXT NOT NULL,
                    verdict TEXT NOT NULL,
                    score REAL NOT NULL,
                    checks_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
                );

                CREATE TABLE IF NOT EXISTS releases (
                    release_id TEXT PRIMARY KEY,
                    profile_name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    asset_count INTEGER NOT NULL,
                    manifest_path TEXT NOT NULL,
                    notes TEXT,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS release_assets (
                    release_id TEXT NOT NULL,
                    asset_id TEXT NOT NULL,
                    PRIMARY KEY(release_id, asset_id),
                    FOREIGN KEY(release_id) REFERENCES releases(release_id),
                    FOREIGN KEY(asset_id) REFERENCES assets(asset_id)
                );
                """
            )

    def upsert_asset(self, asset: Asset) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO assets (
                    asset_id, rel_path, kind, stage, sha256, content_sig, status,
                    source_tool, profile, duration_sec, width, height, fps,
                    sample_rate_hz, channels, qc_score, qc_verdict,
                    compliance_json, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(asset_id) DO UPDATE SET
                    rel_path=excluded.rel_path,
                    kind=excluded.kind,
                    stage=excluded.stage,
                    sha256=excluded.sha256,
                    content_sig=excluded.content_sig,
                    status=excluded.status,
                    source_tool=excluded.source_tool,
                    profile=excluded.profile,
                    duration_sec=excluded.duration_sec,
                    width=excluded.width,
                    height=excluded.height,
                    fps=excluded.fps,
                    sample_rate_hz=excluded.sample_rate_hz,
                    channels=excluded.channels,
                    qc_score=excluded.qc_score,
                    qc_verdict=excluded.qc_verdict,
                    compliance_json=excluded.compliance_json,
                    metadata_json=excluded.metadata_json,
                    updated_at=excluded.updated_at
                """,
                (
                    asset.asset_id,
                    asset.rel_path,
                    asset.kind,
                    asset.stage,
                    asset.sha256,
                    asset.content_sig,
                    asset.status,
                    asset.source_tool,
                    asset.profile,
                    asset.duration_sec,
                    asset.width,
                    asset.height,
                    asset.fps,
                    asset.sample_rate_hz,
                    asset.channels,
                    asset.qc_score,
                    asset.qc_verdict,
                    json.dumps(asset.compliance),
                    json.dumps(asset.metadata),
                    asset.created_at,
                    asset.updated_at,
                ),
            )

    def get_asset(self, asset_id: str) -> Asset | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM assets WHERE asset_id = ?", (asset_id,)).fetchone()
        return self._row_to_asset(row) if row else None

    def get_asset_by_path(self, rel_path: str) -> Asset | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM assets WHERE rel_path = ?", (rel_path,)).fetchone()
        return self._row_to_asset(row) if row else None

    def find_by_sha256(self, sha256: str) -> list[Asset]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM assets WHERE sha256 = ?", (sha256,)).fetchall()
        return [self._row_to_asset(row) for row in rows]

    def find_by_content_sig(self, content_sig: str) -> list[Asset]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM assets WHERE content_sig = ?", (content_sig,)).fetchall()
        return [self._row_to_asset(row) for row in rows]

    def list_assets(
        self,
        *,
        stage: str | None = None,
        kind: str | None = None,
        qc_verdict: str | None = None,
        profile: str | None = None,
        limit: int = 500,
    ) -> list[Asset]:
        clauses: list[str] = []
        params: list[Any] = []
        if stage:
            clauses.append("stage = ?")
            params.append(stage)
        if kind:
            clauses.append("kind = ?")
            params.append(kind)
        if qc_verdict:
            clauses.append("qc_verdict = ?")
            params.append(qc_verdict)
        if profile:
            clauses.append("profile = ?")
            params.append(profile)

        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        query = f"SELECT * FROM assets {where} ORDER BY updated_at DESC LIMIT ?"
        params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [self._row_to_asset(row) for row in rows]

    def summary(self) -> dict[str, Any]:
        with self._connect() as conn:
            total = conn.execute("SELECT COUNT(*) FROM assets").fetchone()[0]
            by_stage = dict(conn.execute("SELECT stage, COUNT(*) FROM assets GROUP BY stage").fetchall())
            by_verdict = dict(
                conn.execute(
                    "SELECT COALESCE(qc_verdict, 'unscored'), COUNT(*) FROM assets GROUP BY qc_verdict"
                ).fetchall()
            )
            releases = conn.execute("SELECT COUNT(*) FROM releases").fetchone()[0]
        return {
            "total_assets": total,
            "by_stage": by_stage,
            "by_qc_verdict": by_verdict,
            "releases": releases,
        }

    def record_provenance(
        self,
        *,
        asset_id: str,
        event_type: str,
        tool: str,
        parent_asset_id: str | None = None,
        operator: str | None = None,
        input_hash: str | None = None,
        output_hash: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO provenance (
                    asset_id, parent_asset_id, event_type, tool, operator,
                    input_hash, output_hash, details_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    asset_id,
                    parent_asset_id,
                    event_type,
                    tool,
                    operator,
                    input_hash,
                    output_hash,
                    json.dumps(details or {}),
                    utcnow(),
                ),
            )

    def lineage(self, asset_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                WITH RECURSIVE chain AS (
                    SELECT event_id, asset_id, parent_asset_id, event_type, tool, operator,
                           input_hash, output_hash, details_json, created_at, 0 AS depth
                    FROM provenance WHERE asset_id = ?
                    UNION ALL
                    SELECT p.event_id, p.asset_id, p.parent_asset_id, p.event_type, p.tool,
                           p.operator, p.input_hash, p.output_hash, p.details_json, p.created_at,
                           chain.depth + 1
                    FROM provenance p
                    JOIN chain ON p.asset_id = chain.parent_asset_id
                )
                SELECT * FROM chain ORDER BY depth, created_at
                """,
                (asset_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def record_qc(
        self,
        *,
        asset_id: str,
        policy_name: str,
        verdict: str,
        score: float,
        checks: dict[str, Any],
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO qc_results (asset_id, policy_name, verdict, score, checks_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (asset_id, policy_name, verdict, score, json.dumps(checks), utcnow()),
            )
            conn.execute(
                """
                UPDATE assets SET qc_score = ?, qc_verdict = ?, updated_at = ? WHERE asset_id = ?
                """,
                (score, verdict, utcnow(), asset_id),
            )

    def create_release(
        self,
        *,
        release_id: str,
        profile_name: str,
        version: str,
        asset_ids: list[str],
        manifest_path: str,
        notes: str = "",
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO releases (release_id, profile_name, version, asset_count, manifest_path, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (release_id, profile_name, version, len(asset_ids), manifest_path, notes, utcnow()),
            )
            conn.executemany(
                "INSERT INTO release_assets (release_id, asset_id) VALUES (?, ?)",
                [(release_id, asset_id) for asset_id in asset_ids],
            )

    def list_releases(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM releases ORDER BY created_at DESC"
            ).fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def _row_to_asset(row: sqlite3.Row) -> Asset:
        return Asset(
            asset_id=row["asset_id"],
            rel_path=row["rel_path"],
            kind=row["kind"],
            stage=row["stage"],
            sha256=row["sha256"],
            content_sig=row["content_sig"],
            status=row["status"],
            source_tool=row["source_tool"],
            profile=row["profile"],
            duration_sec=row["duration_sec"],
            width=row["width"],
            height=row["height"],
            fps=row["fps"],
            sample_rate_hz=row["sample_rate_hz"],
            channels=row["channels"],
            qc_score=row["qc_score"],
            qc_verdict=row["qc_verdict"],
            compliance=json.loads(row["compliance_json"]),
            metadata=json.loads(row["metadata_json"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )