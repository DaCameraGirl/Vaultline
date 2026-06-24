<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Vaultline — gobernanza de medios para entrenamiento de IA" width="100%"/>
</p>

# Vaultline

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸_English-131a26?style=for-the-badge&labelColor=0f131a" alt="English"/></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/🇪🇸_Español-5eead4?style=for-the-badge&labelColor=0f131a" alt="Español"/></a>
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
  <a href="https://dacameragirl.github.io/Vaultline/"><img src="https://img.shields.io/badge/🌐_Sitio_en_vivo-5eead4?style=for-the-badge&labelColor=0f131a" alt="Sitio en vivo"/></a>
  <a href="https://dacameragirl.github.io/links/"><img src="https://img.shields.io/badge/🔗_Hub_de_proyectos-131a26?style=for-the-badge&labelColor=0f131a" alt="Hub de proyectos"/></a>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=0f131a" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0f131a" alt="Python"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0f131a" alt="Docker"/>
  <img src="https://img.shields.io/badge/Render-5eead4?style=for-the-badge&labelColor=0f131a" alt="Render"/>
</p>

**Gobernanza de medios para entrenamiento de IA** — procedencia, control de calidad, cumplimiento y versiones inmutables para datos de entrenamiento de voz y video.

Demuestra qué entró en el modelo: cada clip rastreado, validado por QC y listo para publicación.

> **Estado:** el sitio de marketing está en vivo en GitHub Pages. La **plataforma completa** (API + consola + ingestión) se ejecuta localmente mediante el acceso directo del escritorio o se despliega con [DEPLOY.md](./DEPLOY.md).

## Repositorio vs. sitio en vivo

| Qué | URL |
|---|---|
| **Repositorio de GitHub** | [github.com/DaCameraGirl/Vaultline](https://github.com/DaCameraGirl/Vaultline) |
| **Marketing / landing** (GitHub Pages) | [dacameragirl.github.io/Vaultline](https://dacameragirl.github.io/Vaultline/) |
| **Plataforma completa** (API + consola + ingestión) | Acceso directo del escritorio o [DEPLOY.md](./DEPLOY.md) |
| **Hub de proyectos** | [dacameragirl.github.io/links](https://dacameragirl.github.io/links/) |

GitHub muestra este README. Guarda en favoritos el **sitio en vivo** para la URL de marketing — es independiente de la página del repositorio.

## Aspectos destacados

| Capa | Qué hace |
|---|---|
| **API empresarial** | FastAPI — ingestión, carga, QC, cumplimiento, versiones, exportación de auditoría |
| **Sitio de marketing** | UI del producto en vivo en `/site/index.html` cuando la API está en ejecución |
| **Consola de operaciones** | Panel en `/console/index.html` — activos, linaje, acciones |
| **CLI** | `bench.py` para operaciones del pipeline |
| **Catálogo** | Registro SQLite de procedencia + QC + versiones |
| **Go-to-market** | `leads/target-accounts.csv`, `marketing/one-pager.md`, plantillas de outreach |
| **Docker** | `docker compose up` para despliegue estilo producción |
| **Render** | Blueprint `render.yaml` para API alojada |

## Ejecutar localmente (plataforma completa)

**Lo más fácil — doble clic en `Vaultline` en el escritorio.**

Configuración inicial:

```powershell
powershell -File setup/create-desktop-shortcut.ps1
```

O:

```powershell
setup\Launch Vaultline.bat
```

**URLs cuando el servidor está en ejecución:**

| Superficie | URL |
|---|---|
| Marketing + API en vivo | http://localhost:8470/site/index.html |
| Consola | http://localhost:8470/console/index.html |
| Documentación de la API | http://localhost:8470/docs |

Verificar todo:

```powershell
powershell -File setup/verify.ps1
```

Detener:

```powershell
powershell -File setup/stop-vaultline.ps1
```

## Quién lo compra

| Segmento | Dolor |
|---|---|
| IA de voz (ASR/TTS) | Auditorías de consentimiento y QC antes del envío del modelo |
| Laboratorios de video / multimodal | Conjuntos de datos de referencia con linaje trazable |
| Proveedores empresariales de IA | Cuestionarios de adquisición sobre gobernanza de datos |

**Comprador:** VP de Ingeniería · Director de Datos de ML · Director de Cumplimiento de IA

## Comercialízalo

1. Abre `leads/target-accounts.csv`
2. Usa las plantillas en `marketing/outreach-templates.md`
3. Comparte el enlace en vivo: marketing en Pages + consola alojada o demo local
4. Adjunta `marketing/one-pager.md` en llamadas empresariales

Consulta `marketing/CAMPAIGN.md` para el plan de 30 días.

## Referencia rápida de la API

```http
GET  /health
GET  /v1/dashboard
GET  /v1/assets
POST /v1/uploads
POST /v1/ingest
POST /v1/releases
GET  /v1/audit/export
```

## Desplegar en producción

Consulta **[DEPLOY.md](./DEPLOY.md)** — GitHub Pages (marketing), Render (API) o Docker.

## Estructura del proyecto

```text
Vaultline/
├── api/server.py           API empresarial
├── marketing/              Landing + copy GTM (fuente de despliegue Pages)
├── console/                Panel de operaciones
├── leads/                  Cuentas objetivo
├── workbench/              Catálogo, QC, ingestión, exportación
├── catalog/                Registro SQLite (local, gitignored)
├── releases/               Paquetes de datos inmutables
├── docs/assets/            SVG hero del README
└── config/enterprise.yaml  Configuración del producto
```

## Colaboradores

- **Angela Hudson** ([DaCameraGirl](https://github.com/DaCameraGirl)) — dirección de producto, GTM, pruebas
- **Claude** — andamiaje de la plataforma, API, consola, marketing, kit de despliegue

## Licencia

© 2026 Angela Hudson (DaCameraGirl). Consulta [LICENSE](./LICENSE).