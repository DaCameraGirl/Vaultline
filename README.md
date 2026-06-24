<p align="center">
  <a href="https://dacameragirl.github.io/Vaultline/">
    <img src="https://img.shields.io/badge/▶_OPEN_LIVE_SITE-5eead4?style=for-the-badge&labelColor=0f131a" alt="Open live site"/>
  </a>
  <a href="https://github.com/DaCameraGirl/Vaultline">
    <img src="https://img.shields.io/badge/Code-GitHub-3d8bfd?style=for-the-badge&labelColor=0f131a" alt="GitHub"/>
  </a>
</p>

# Vaultline

**AI training media governance** — provenance, QC, compliance, and immutable releases for voice and video training data.

Prove what went into the model: every clip traced, QC-gated, and release-ready.

## Repo vs live app

| What you want | URL |
|---------------|-----|
| **Marketing / landing** (GitHub Pages) | **[dacameragirl.github.io/Vaultline](https://dacameragirl.github.io/Vaultline/)** |
| **Full platform** (API + console + ingest) | Run locally (Desktop shortcut) or deploy with [DEPLOY.md](./DEPLOY.md) |
| **All Angela's projects** | **[dacameragirl.github.io/links](https://dacameragirl.github.io/links/)** |
| Source on GitHub | `github.com/DaCameraGirl/Vaultline` |

GitHub shows this README. The **live marketing site** is a separate Pages URL — bookmark the link above.

## What ships in this repo

| Layer | What it is |
|-------|------------|
| **Enterprise API** | FastAPI — ingest, upload, QC, compliance, releases, audit export |
| **Marketing site** | Live product UI at `/site/index.html` when the API is running |
| **Ops console** | Dashboard at `/console/index.html` |
| **CLI** | `bench.py` for pipeline operations |
| **Catalog** | SQLite provenance + QC + release registry |
| **Go-to-market** | `leads/target-accounts.csv`, `marketing/one-pager.md`, outreach templates |
| **Docker** | `docker compose up` for production-style deploy |
| **Render** | `render.yaml` blueprint for hosted API |

## Run locally (full platform)

**Easiest — double-click `Vaultline` on your Desktop.**

First-time setup:

```powershell
powershell -File setup/create-desktop-shortcut.ps1
```

Or:

```powershell
setup\Launch Vaultline.bat
```

**URLs when the server is running:**

- Marketing + live API: http://localhost:8470/site/index.html
- Console: http://localhost:8470/console/index.html
- API docs: http://localhost:8470/docs

Verify everything:

```powershell
powershell -File setup/verify.ps1
```

Stop:

```powershell
powershell -File setup/stop-vaultline.ps1
```

## Who buys this

- Voice AI companies (ASR/TTS) facing consent + QC audits
- Video/multimodal labs shipping benchmark datasets
- Enterprise AI vendors answering procurement questionnaires

**Buyer:** VP Engineering · Head of ML Data · Director AI Compliance

## Market it

1. Open `leads/target-accounts.csv`
2. Use templates in `marketing/outreach-templates.md`
3. Share live link: Pages marketing + hosted or local console demo
4. Attach `marketing/one-pager.md` on enterprise calls

See `marketing/CAMPAIGN.md` for the 30-day plan.

## API quick reference

```
GET  /health
GET  /v1/dashboard
GET  /v1/assets
POST /v1/uploads
POST /v1/ingest
POST /v1/releases
GET  /v1/audit/export
```

## Deploy to production

See **[DEPLOY.md](./DEPLOY.md)** — GitHub Pages (marketing), Render (API), or Docker.

## Project structure

```
Vaultline/
├── api/server.py           Enterprise API
├── marketing/              Landing + GTM copy
├── console/                Ops dashboard
├── leads/                  Target accounts
├── workbench/              Catalog, QC, ingest, export
├── catalog/                SQLite registry (local, gitignored)
├── releases/               Immutable dataset bundles
└── config/enterprise.yaml  Product config
```

## License

Copyright (c) 2026 Angela Hudson. See [LICENSE](./LICENSE).