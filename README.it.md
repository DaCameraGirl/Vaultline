<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Vaultline — governance dei media per l'addestramento IA" width="100%"/>
</p>

# Vaultline

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸_English-131a26?style=for-the-badge&labelColor=0f131a" alt="English"/></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/🇪🇸_Español-131a26?style=for-the-badge&labelColor=0f131a" alt="Español"/></a>
  <a href="README.fr.md"><img src="https://img.shields.io/badge/🇫🇷_Français-131a26?style=for-the-badge&labelColor=0f131a" alt="Français"/></a>
  <a href="README.de.md"><img src="https://img.shields.io/badge/🇩🇪_Deutsch-131a26?style=for-the-badge&labelColor=0f131a" alt="Deutsch"/></a>
  <a href="README.pt-BR.md"><img src="https://img.shields.io/badge/🇧🇷_Português-131a26?style=for-the-badge&labelColor=0f131a" alt="Português"/></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/🇨🇳_中文-131a26?style=for-the-badge&labelColor=0f131a" alt="中文"/></a>
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵_日本語-131a26?style=for-the-badge&labelColor=0f131a" alt="日本語"/></a>
  <a href="README.ko.md"><img src="https://img.shields.io/badge/🇰🇷_한국어-131a26?style=for-the-badge&labelColor=0f131a" alt="한국어"/></a>
  <a href="README.it.md"><img src="https://img.shields.io/badge/🇮🇹_Italiano-5eead4?style=for-the-badge&labelColor=0f131a" alt="Italiano"/></a>
  <a href="README.ar.md"><img src="https://img.shields.io/badge/🇸🇦_العربية-131a26?style=for-the-badge&labelColor=0f131a" alt="العربية"/></a>
</p>

<p align="center">
  <a href="https://dacameragirl.github.io/Vaultline/"><img src="https://img.shields.io/badge/🌐_Sito_live-5eead4?style=for-the-badge&labelColor=0f131a" alt="Sito live"/></a>
  <a href="https://dacameragirl.github.io/links/"><img src="https://img.shields.io/badge/🔗_Hub_progetti-131a26?style=for-the-badge&labelColor=0f131a" alt="Hub progetti"/></a>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=0f131a" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0f131a" alt="Python"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0f131a" alt="Docker"/>
  <img src="https://img.shields.io/badge/Render-5eead4?style=for-the-badge&labelColor=0f131a" alt="Render"/>
</p>

**Governance dei media per l'addestramento IA** — provenienza, QC, conformità e release immutabili per dati di addestramento voce e video.

Dimostra cosa è entrato nel modello: ogni clip tracciata, validata da QC e pronta per il rilascio.

> **Stato:** il sito marketing è live su GitHub Pages. La **piattaforma completa** (API + console + ingest) gira in locale tramite collegamento Desktop o si distribuisce con [DEPLOY.md](./DEPLOY.md).

## Repository vs. sito live

| Cosa | URL |
|---|---|
| **Repository GitHub** | [github.com/DaCameraGirl/Vaultline](https://github.com/DaCameraGirl/Vaultline) |
| **Marketing / landing** (GitHub Pages) | [dacameragirl.github.io/Vaultline](https://dacameragirl.github.io/Vaultline/) |
| **Piattaforma completa** (API + console + ingest) | Collegamento Desktop o [DEPLOY.md](./DEPLOY.md) |
| **Hub progetti** | [dacameragirl.github.io/links](https://dacameragirl.github.io/links/) |

GitHub mostra questo README. Aggiungi ai preferiti il **sito live** per l'URL marketing — è separato dalla pagina del repository.

## Punti salienti

| Livello | Funzione |
|---|---|
| **API enterprise** | FastAPI — ingest, upload, QC, conformità, release, export audit |
| **Sito marketing** | UI prodotto live su `/site/index.html` quando l'API è in esecuzione |
| **Console ops** | Dashboard su `/console/index.html` — asset, lineage, azioni |
| **CLI** | `bench.py` per operazioni pipeline |
| **Catalogo** | Registro SQLite provenienza + QC + release |
| **Go-to-market** | `leads/target-accounts.csv`, `marketing/one-pager.md`, template outreach |
| **Docker** | `docker compose up` per deploy stile produzione |
| **Render** | Blueprint `render.yaml` per API ospitata |

## Eseguire in locale (piattaforma completa)

**Più semplice — doppio clic su `Vaultline` sul Desktop.**

Configurazione iniziale:

```powershell
powershell -File setup/create-desktop-shortcut.ps1
```

Oppure:

```powershell
setup\Launch Vaultline.bat
```

**URL con il server in esecuzione:**

| Superficie | URL |
|---|---|
| Marketing + API live | http://localhost:8470/site/index.html |
| Console | http://localhost:8470/console/index.html |
| Documentazione API | http://localhost:8470/docs |

Verifica tutto:

```powershell
powershell -File setup/verify.ps1
```

Arresta:

```powershell
powershell -File setup/stop-vaultline.ps1
```

## Chi acquista

| Segmento | Problema |
|---|---|
| IA vocale (ASR/TTS) | Audit consenso + QC prima della consegna del modello |
| Lab video / multimodali | Dataset benchmark con lineage tracciabile |
| Vendor IA enterprise | Questionari procurement sulla governance dei dati |

**Acquirente:** VP Engineering · Head of ML Data · Director AI Compliance

## Commercializzare

1. Apri `leads/target-accounts.csv`
2. Usa i template in `marketing/outreach-templates.md`
3. Condividi il link live: marketing Pages + console ospitata o demo locale
4. Allega `marketing/one-pager.md` nelle call enterprise

Vedi `marketing/CAMPAIGN.md` per il piano di 30 giorni.

## Riferimento rapido API

```http
GET  /health
GET  /v1/dashboard
GET  /v1/assets
POST /v1/uploads
POST /v1/ingest
POST /v1/releases
GET  /v1/audit/export
```

## Distribuire in produzione

Vedi **[DEPLOY.md](./DEPLOY.md)** — GitHub Pages (marketing), Render (API) o Docker.

## Struttura del progetto

```text
Vaultline/
├── api/server.py           API enterprise
├── marketing/              Landing + copy GTM (sorgente deploy Pages)
├── console/                Dashboard ops
├── leads/                  Account target
├── workbench/              Catalogo, QC, ingest, export
├── catalog/                Registro SQLite (locale, gitignored)
├── releases/               Bundle dataset immutabili
├── docs/assets/            SVG hero README
└── config/enterprise.yaml  Configurazione prodotto
```

## Collaboratori

- **Angela Hudson** ([DaCameraGirl](https://github.com/DaCameraGirl)) — direzione prodotto, GTM, testing
- **Claude** — scaffold piattaforma, API, console, marketing, kit deploy

## Licenza

© 2026 Angela Hudson (DaCameraGirl). Vedi [LICENSE](./LICENSE).