# Vaultline

**AI Training Media Governance** — enterprise audit, QC, and release control for voice and video training data.

Deploy today. Market today. No cloud lock-in.

---

## What ships in this repo

| Layer | What it is |
|-------|------------|
| **Enterprise API** | FastAPI — ingest, upload, QC, compliance, releases, audit export |
| **Marketing site** | Premium landing page at `/site/index.html` |
| **Ops console** | Live dashboard at `/console/index.html` |
| **CLI** | `bench.py` for pipeline operations |
| **Catalog** | SQLite provenance + QC + release registry |
| **Go-to-market** | `leads/target-accounts.csv`, `marketing/one-pager.md`, outreach templates |
| **Docker** | `docker-compose up` for production-style deploy |

## Start the platform

```powershell
powershell -File setup/start.ps1
```

Or:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python bench.py serve
```

**Live URLs:**
- Marketing: http://localhost:8470/site/index.html
- Console: http://localhost:8470/console/index.html
- API docs: http://localhost:8470/docs

## Who desperately needs this

- Voice AI companies (ASR/TTS) facing consent + QC audits
- Video/multimodal labs shipping benchmark datasets
- Enterprise AI vendors answering procurement questionnaires
- Regulated speech (health, legal, biometric)

**Buyer:** VP Engineering · Head of ML Data · Director AI Compliance

## Market it

1. Open `leads/target-accounts.csv` — 24 priority accounts pre-loaded
2. Find verified emails: LinkedIn → Hunter.io (company domain only)
3. Send templates from `marketing/outreach-templates.md`
4. Demo link: your deployed `/site/index.html` + `/console/index.html`
5. Attach `marketing/one-pager.md` for enterprise calls

**Contact on all materials:** hello@vaultline.ai (set up forwarding on your domain)

## Enterprise pricing (on marketing site)

- Team: $2,400/mo
- Enterprise: $8,500/mo
- Air-gapped/regulated: custom

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

## Docker deploy

```powershell
docker compose up --build
```

## Editor integrations

Shotcut · OpenShot · Lightworks · Ardour · LMMS — creative surface unchanged. Vaultline is the governance layer underneath.

## Project structure

```
vaultline/
├── api/server.py           Enterprise API
├── marketing/              Landing page + one-pager + outreach
├── console/                Live ops dashboard
├── leads/                  Target account list
├── workbench/              Catalog, QC, ingest, export engine
├── catalog/catalog.db      Asset registry
├── releases/               Immutable dataset bundles
└── config/enterprise.yaml  Product + commercial config
```