<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Vaultline — KI-Trainingsmedien-Governance" width="100%"/>
</p>

# Vaultline

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸_English-131a26?style=for-the-badge&labelColor=0f131a" alt="English"/></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/🇪🇸_Español-131a26?style=for-the-badge&labelColor=0f131a" alt="Español"/></a>
  <a href="README.fr.md"><img src="https://img.shields.io/badge/🇫🇷_Français-131a26?style=for-the-badge&labelColor=0f131a" alt="Français"/></a>
  <a href="README.de.md"><img src="https://img.shields.io/badge/🇩🇪_Deutsch-5eead4?style=for-the-badge&labelColor=0f131a" alt="Deutsch"/></a>
  <a href="README.pt-BR.md"><img src="https://img.shields.io/badge/🇧🇷_Português-131a26?style=for-the-badge&labelColor=0f131a" alt="Português"/></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/🇨🇳_中文-131a26?style=for-the-badge&labelColor=0f131a" alt="中文"/></a>
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵_日本語-131a26?style=for-the-badge&labelColor=0f131a" alt="日本語"/></a>
  <a href="README.ko.md"><img src="https://img.shields.io/badge/🇰🇷_한국어-131a26?style=for-the-badge&labelColor=0f131a" alt="한국어"/></a>
  <a href="README.it.md"><img src="https://img.shields.io/badge/🇮🇹_Italiano-131a26?style=for-the-badge&labelColor=0f131a" alt="Italiano"/></a>
  <a href="README.ar.md"><img src="https://img.shields.io/badge/🇸🇦_العربية-131a26?style=for-the-badge&labelColor=0f131a" alt="العربية"/></a>
</p>

<p align="center">
  <a href="https://dacameragirl.github.io/Vaultline/"><img src="https://img.shields.io/badge/🌐_Live_Site-5eead4?style=for-the-badge&labelColor=0f131a" alt="Live-Site"/></a>
  <a href="https://dacameragirl.github.io/links/"><img src="https://img.shields.io/badge/🔗_Projekt_Hub-131a26?style=for-the-badge&labelColor=0f131a" alt="Projekt-Hub"/></a>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=0f131a" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0f131a" alt="Python"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0f131a" alt="Docker"/>
  <img src="https://img.shields.io/badge/Render-5eead4?style=for-the-badge&labelColor=0f131a" alt="Render"/>
</p>

**KI-Trainingsmedien-Governance** — Herkunft, QC, Compliance und unveränderliche Releases für Sprach- und Video-Trainingsdaten.

Nachweis, was ins Modell geflossen ist: jeder Clip nachverfolgt, QC-geprüft und release-bereit.

> **Status:** Die Marketing-Website ist live auf GitHub Pages. Die **vollständige Plattform** (API + Konsole + Ingest) läuft lokal über die Desktop-Verknüpfung oder wird mit [DEPLOY.md](./DEPLOY.md) bereitgestellt.

## Repo vs. Live-Site

| Was | URL |
|---|---|
| **GitHub-Repo** | [github.com/DaCameraGirl/Vaultline](https://github.com/DaCameraGirl/Vaultline) |
| **Marketing / Landing** (GitHub Pages) | [dacameragirl.github.io/Vaultline](https://dacameragirl.github.io/Vaultline/) |
| **Vollständige Plattform** (API + Konsole + Ingest) | Desktop-Verknüpfung oder [DEPLOY.md](./DEPLOY.md) |
| **Projekt-Hub** | [dacameragirl.github.io/links](https://dacameragirl.github.io/links/) |

GitHub zeigt dieses README. Setzen Sie ein Lesezeichen auf die **Live-Site** für die Marketing-URL — sie ist getrennt von der Repo-Seite.

## Highlights

| Ebene | Funktion |
|---|---|
| **Enterprise-API** | FastAPI — Ingest, Upload, QC, Compliance, Releases, Audit-Export |
| **Marketing-Site** | Live-Produkt-UI unter `/site/index.html`, wenn die API läuft |
| **Ops-Konsole** | Dashboard unter `/console/index.html` — Assets, Lineage, Aktionen |
| **CLI** | `bench.py` für Pipeline-Operationen |
| **Katalog** | SQLite-Register für Herkunft + QC + Releases |
| **Go-to-Market** | `leads/target-accounts.csv`, `marketing/one-pager.md`, Outreach-Vorlagen |
| **Docker** | `docker compose up` für produktionsähnliches Deployment |
| **Render** | `render.yaml`-Blueprint für gehostete API |

## Lokal ausführen (vollständige Plattform)

**Am einfachsten — Doppelklick auf `Vaultline` auf dem Desktop.**

Ersteinrichtung:

```powershell
powershell -File setup/create-desktop-shortcut.ps1
```

Oder:

```powershell
setup\Launch Vaultline.bat
```

**URLs bei laufendem Server:**

| Oberfläche | URL |
|---|---|
| Marketing + Live-API | http://localhost:8470/site/index.html |
| Konsole | http://localhost:8470/console/index.html |
| API-Docs | http://localhost:8470/docs |

Alles prüfen:

```powershell
powershell -File setup/verify.ps1
```

Stoppen:

```powershell
powershell -File setup/stop-vaultline.ps1
```

## Wer kauft das

| Segment | Schmerzpunkt |
|---|---|
| Sprach-KI (ASR/TTS) | Consent- und QC-Audits vor Modell-Auslieferung |
| Video- / Multimodal-Labs | Benchmark-Datensätze mit nachverfolgbarer Lineage |
| Enterprise-KI-Anbieter | Beschaffungsfragebögen zur Daten-Governance |

**Käufer:** VP Engineering · Head of ML Data · Director AI Compliance

## Vermarkten

1. `leads/target-accounts.csv` öffnen
2. Vorlagen in `marketing/outreach-templates.md` nutzen
3. Live-Link teilen: Pages-Marketing + gehostete oder lokale Konsolen-Demo
4. `marketing/one-pager.md` bei Enterprise-Calls anhängen

Siehe `marketing/CAMPAIGN.md` für den 30-Tage-Plan.

## API-Kurzreferenz

```http
GET  /health
GET  /v1/dashboard
GET  /v1/assets
POST /v1/uploads
POST /v1/ingest
POST /v1/releases
GET  /v1/audit/export
```

## In Produktion deployen

Siehe **[DEPLOY.md](./DEPLOY.md)** — GitHub Pages (Marketing), Render (API) oder Docker.

## Projektstruktur

```text
Vaultline/
├── api/server.py           Enterprise-API
├── marketing/              Landing + GTM-Copy (Pages-Deploy-Quelle)
├── console/                Ops-Dashboard
├── leads/                  Zielkonten
├── workbench/              Katalog, QC, Ingest, Export
├── catalog/                SQLite-Register (lokal, gitignored)
├── releases/               Unveränderliche Datensatz-Bundles
├── docs/assets/            README-Hero-SVG
└── config/enterprise.yaml  Produktkonfiguration
```

## Mitwirkende

- **Angela Hudson** ([DaCameraGirl](https://github.com/DaCameraGirl)) — Produktrichtung, GTM, Testing
- **Claude** — Plattform-Scaffold, API, Konsole, Marketing, Deploy-Kit

## Lizenz

© 2026 Angela Hudson (DaCameraGirl). Siehe [LICENSE](./LICENSE).