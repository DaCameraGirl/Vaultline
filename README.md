<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Vaultline — AI training media governance" width="100%"/>
</p>

# Vaultline

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸_English-5eead4?style=for-the-badge&labelColor=0f131a" alt="English"/></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/🇪🇸_Español-131a26?style=for-the-badge&labelColor=0f131a" alt="Español"/></a>
  <a href="README.fr.md"><img src="https://img.shields.io/badge/🇫🇷_Français-131a26?style=for-the-badge&labelColor=0f131a" alt="Français"/></a>
  <a href="README.de.md"><img src="https://img.shields.io/badge/🇩🇪_Deutsch-131a26?style=for-the-badge&labelColor=0f131a" alt="Deutsch"/></a>
  <a href="README.pt-BR.md"><img src="https://img.shields.io/badge/🇧🇷_Português-131a26?style=for-the-badge&labelColor=0f131a" alt="Português"/></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/🇨🇳_中文-131a26?style=for-the-badge&labelColor=0f131a" alt="中文"/></a>
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵_日本語-131a26?style=for-the-badge&labelColor=0f131a" alt="日本語"/></a>
  <a href="README.ko.md"><img src="https://img.shields.io/badge/🇰🇷_한국어-131a26?style=for-the-badge&labelColor=0f131a" alt="한국어"/></a>
  <a href="README.it.md"><img src="https://img.shields.io/badge/🇮🇹_Italiano-131a26?style=for-the-badge&labelColor=0f131a" alt="Italiano"/></a>
  <a href="README.ar.md"><img src="https://img.shields.io/badge/🇸🇦_العربية-131a26?style=for-the-badge&labelColor=0f131a" alt="العربية"/></a>
</p>

<p align="center">
  <a href="https://dacameragirl.github.io/Vaultline/"><img src="https://img.shields.io/badge/🌐_Live_Site-5eead4?style=for-the-badge" alt="Live site"/></a>
  <a href="https://dacameragirl.github.io/links/"><img src="https://img.shields.io/badge/🔗_Project_Hub-131a26?style=for-the-badge" alt="Project hub"/></a>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Render-5eead4?style=for-the-badge" alt="Render"/>
</p>

**AI training media governance** — provenance, QC, compliance, and immutable releases for voice and video training data.

Prove what went into the model: every clip traced, QC-gated, and release-ready.

> **Status:** marketing site is live on GitHub Pages. The **full platform** (API + console + ingest) runs locally via Desktop shortcut or deploys with [DEPLOY.md](./DEPLOY.md).

## Repo vs live

| What | URL |
|---|---|
| **GitHub repo** | [github.com/DaCameraGirl/Vaultline](https://github.com/DaCameraGirl/Vaultline) |
| **Marketing / landing** (GitHub Pages) | [dacameragirl.github.io/Vaultline](https://dacameragirl.github.io/Vaultline/) |
| **Full platform** (API + console + ingest) | Desktop shortcut or [DEPLOY.md](./DEPLOY.md) |
| **Project hub** | [dacameragirl.github.io/links](https://dacameragirl.github.io/links/) |

GitHub shows this README. Bookmark the **live site** for the marketing URL — it's separate from the repo page.

## Highlights

| Layer | What it does |
|---|---|
| **Enterprise API** | FastAPI — ingest, upload, QC, compliance, releases, audit export |
| **Marketing site** | Live product UI at `/site/index.html` when the API is running |
| **Ops console** | Dashboard at `/console/index.html` — assets, lineage, actions |
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

| Surface | URL |
|---|---|
| Marketing + live API | http://localhost:8470/site/index.html |
| Console | http://localhost:8470/console/index.html |
| API docs | http://localhost:8470/docs |

Verify everything:

```powershell
powershell -File setup/verify.ps1
```

Stop:

```powershell
powershell -File setup/stop-vaultline.ps1
```

## Who buys this

| Segment | Pain |
|---|---|
| Voice AI (ASR/TTS) | Consent + QC audits before model ship |
| Video / multimodal labs | Benchmark datasets with traceable lineage |
| Enterprise AI vendors | Procurement questionnaires on data governance |

**Buyer:** VP Engineering · Head of ML Data · Director AI Compliance

## Market it

1. Open `leads/target-accounts.csv`
2. Use templates in `marketing/outreach-templates.md`
3. Share live link: Pages marketing + hosted or local console demo
4. Attach `marketing/one-pager.md` on enterprise calls

See `marketing/CAMPAIGN.md` for the 30-day plan.

## API quick reference

```http
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

```text
Vaultline/
├── api/server.py           Enterprise API
├── marketing/              Landing + GTM copy (Pages deploy source)
├── console/                Ops dashboard
├── leads/                  Target accounts
├── workbench/              Catalog, QC, ingest, export
├── catalog/                SQLite registry (local, gitignored)
├── releases/               Immutable dataset bundles
├── docs/assets/            README hero SVG
└── config/enterprise.yaml  Product config
```

## Contributors

- **Angela Hudson** ([DaCameraGirl](https://github.com/DaCameraGirl)) — product direction, GTM, testing
- **Claude** — platform scaffold, API, console, marketing, deploy kit

## License

© 2026 Angela Hudson (DaCameraGirl). See [LICENSE](./LICENSE).