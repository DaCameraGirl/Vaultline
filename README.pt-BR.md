<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Vaultline — governança de mídia para treinamento de IA" width="100%"/>
</p>

# Vaultline

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸_English-131a26?style=for-the-badge&labelColor=0f131a" alt="English"/></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/🇪🇸_Español-131a26?style=for-the-badge&labelColor=0f131a" alt="Español"/></a>
  <a href="README.fr.md"><img src="https://img.shields.io/badge/🇫🇷_Français-131a26?style=for-the-badge&labelColor=0f131a" alt="Français"/></a>
  <a href="README.de.md"><img src="https://img.shields.io/badge/🇩🇪_Deutsch-131a26?style=for-the-badge&labelColor=0f131a" alt="Deutsch"/></a>
  <a href="README.pt-BR.md"><img src="https://img.shields.io/badge/🇧🇷_Português-5eead4?style=for-the-badge&labelColor=0f131a" alt="Português"/></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/🇨🇳_中文-131a26?style=for-the-badge&labelColor=0f131a" alt="中文"/></a>
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵_日本語-131a26?style=for-the-badge&labelColor=0f131a" alt="日本語"/></a>
  <a href="README.ko.md"><img src="https://img.shields.io/badge/🇰🇷_한국어-131a26?style=for-the-badge&labelColor=0f131a" alt="한국어"/></a>
  <a href="README.it.md"><img src="https://img.shields.io/badge/🇮🇹_Italiano-131a26?style=for-the-badge&labelColor=0f131a" alt="Italiano"/></a>
  <a href="README.ar.md"><img src="https://img.shields.io/badge/🇸🇦_العربية-131a26?style=for-the-badge&labelColor=0f131a" alt="العربية"/></a>
</p>

<p align="center">
  <a href="https://dacameragirl.github.io/Vaultline/"><img src="https://img.shields.io/badge/🌐_Site_ao_vivo-5eead4?style=for-the-badge&labelColor=0f131a" alt="Site ao vivo"/></a>
  <a href="https://dacameragirl.github.io/links/"><img src="https://img.shields.io/badge/🔗_Hub_de_projetos-131a26?style=for-the-badge&labelColor=0f131a" alt="Hub de projetos"/></a>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=0f131a" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0f131a" alt="Python"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0f131a" alt="Docker"/>
  <img src="https://img.shields.io/badge/Render-5eead4?style=for-the-badge&labelColor=0f131a" alt="Render"/>
</p>

**Governança de mídia para treinamento de IA** — proveniência, QC, conformidade e releases imutáveis para dados de treinamento de voz e vídeo.

Prove o que entrou no modelo: cada clipe rastreado, validado por QC e pronto para release.

> **Status:** o site de marketing está no ar no GitHub Pages. A **plataforma completa** (API + console + ingestão) roda localmente pelo atalho da Área de Trabalho ou é implantada com [DEPLOY.md](./DEPLOY.md).

## Repositório vs. site ao vivo

| O quê | URL |
|---|---|
| **Repositório GitHub** | [github.com/DaCameraGirl/Vaultline](https://github.com/DaCameraGirl/Vaultline) |
| **Marketing / landing** (GitHub Pages) | [dacameragirl.github.io/Vaultline](https://dacameragirl.github.io/Vaultline/) |
| **Plataforma completa** (API + console + ingestão) | Atalho da Área de Trabalho ou [DEPLOY.md](./DEPLOY.md) |
| **Hub de projetos** | [dacameragirl.github.io/links](https://dacameragirl.github.io/links/) |

O GitHub exibe este README. Favorite o **site ao vivo** para a URL de marketing — ela é separada da página do repositório.

## Destaques

| Camada | Função |
|---|---|
| **API empresarial** | FastAPI — ingestão, upload, QC, conformidade, releases, exportação de auditoria |
| **Site de marketing** | UI do produto ao vivo em `/site/index.html` quando a API está rodando |
| **Console de ops** | Dashboard em `/console/index.html` — ativos, linhagem, ações |
| **CLI** | `bench.py` para operações do pipeline |
| **Catálogo** | Registro SQLite de proveniência + QC + releases |
| **Go-to-market** | `leads/target-accounts.csv`, `marketing/one-pager.md`, modelos de outreach |
| **Docker** | `docker compose up` para deploy estilo produção |
| **Render** | Blueprint `render.yaml` para API hospedada |

## Executar localmente (plataforma completa)

**Mais fácil — clique duplo em `Vaultline` na Área de Trabalho.**

Configuração inicial:

```powershell
powershell -File setup/create-desktop-shortcut.ps1
```

Ou:

```powershell
setup\Launch Vaultline.bat
```

**URLs com o servidor em execução:**

| Superfície | URL |
|---|---|
| Marketing + API ao vivo | http://localhost:8470/site/index.html |
| Console | http://localhost:8470/console/index.html |
| Docs da API | http://localhost:8470/docs |

Verificar tudo:

```powershell
powershell -File setup/verify.ps1
```

Parar:

```powershell
powershell -File setup/stop-vaultline.ps1
```

## Quem compra

| Segmento | Dor |
|---|---|
| IA de voz (ASR/TTS) | Auditorias de consentimento e QC antes do envio do modelo |
| Labs de vídeo / multimodal | Conjuntos de benchmark com linhagem rastreável |
| Fornecedores enterprise de IA | Questionários de compras sobre governança de dados |

**Comprador:** VP de Engenharia · Head of ML Data · Director AI Compliance

## Comercializar

1. Abra `leads/target-accounts.csv`
2. Use os modelos em `marketing/outreach-templates.md`
3. Compartilhe o link ao vivo: marketing no Pages + console hospedado ou demo local
4. Anexe `marketing/one-pager.md` em calls enterprise

Veja `marketing/CAMPAIGN.md` para o plano de 30 dias.

## Referência rápida da API

```http
GET  /health
GET  /v1/dashboard
GET  /v1/assets
POST /v1/uploads
POST /v1/ingest
POST /v1/releases
GET  /v1/audit/export
```

## Implantar em produção

Veja **[DEPLOY.md](./DEPLOY.md)** — GitHub Pages (marketing), Render (API) ou Docker.

## Estrutura do projeto

```text
Vaultline/
├── api/server.py           API empresarial
├── marketing/              Landing + copy GTM (fonte de deploy Pages)
├── console/                Dashboard de ops
├── leads/                  Contas-alvo
├── workbench/              Catálogo, QC, ingestão, exportação
├── catalog/                Registro SQLite (local, gitignored)
├── releases/               Pacotes de dados imutáveis
├── docs/assets/            SVG hero do README
└── config/enterprise.yaml  Configuração do produto
```

## Colaboradores

- **Angela Hudson** ([DaCameraGirl](https://github.com/DaCameraGirl)) — direção de produto, GTM, testes
- **Claude** — scaffold da plataforma, API, console, marketing, kit de deploy

## Licença

© 2026 Angela Hudson (DaCameraGirl). Veja [LICENSE](./LICENSE).