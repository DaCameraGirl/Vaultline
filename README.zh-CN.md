<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Vaultline — AI 训练媒体治理" width="100%"/>
</p>

# Vaultline

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸_English-131a26?style=for-the-badge&labelColor=0f131a" alt="English"/></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/🇪🇸_Español-131a26?style=for-the-badge&labelColor=0f131a" alt="Español"/></a>
  <a href="README.fr.md"><img src="https://img.shields.io/badge/🇫🇷_Français-131a26?style=for-the-badge&labelColor=0f131a" alt="Français"/></a>
  <a href="README.de.md"><img src="https://img.shields.io/badge/🇩🇪_Deutsch-131a26?style=for-the-badge&labelColor=0f131a" alt="Deutsch"/></a>
  <a href="README.pt-BR.md"><img src="https://img.shields.io/badge/🇧🇷_Português-131a26?style=for-the-badge&labelColor=0f131a" alt="Português"/></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/🇨🇳_中文-5eead4?style=for-the-badge&labelColor=0f131a" alt="中文"/></a>
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵_日本語-131a26?style=for-the-badge&labelColor=0f131a" alt="日本語"/></a>
  <a href="README.ko.md"><img src="https://img.shields.io/badge/🇰🇷_한국어-131a26?style=for-the-badge&labelColor=0f131a" alt="한국어"/></a>
  <a href="README.it.md"><img src="https://img.shields.io/badge/🇮🇹_Italiano-131a26?style=for-the-badge&labelColor=0f131a" alt="Italiano"/></a>
  <a href="README.ar.md"><img src="https://img.shields.io/badge/🇸🇦_العربية-131a26?style=for-the-badge&labelColor=0f131a" alt="العربية"/></a>
</p>

<p align="center">
  <a href="https://dacameragirl.github.io/Vaultline/"><img src="https://img.shields.io/badge/🌐_在线站点-5eead4?style=for-the-badge&labelColor=0f131a" alt="在线站点"/></a>
  <a href="https://dacameragirl.github.io/links/"><img src="https://img.shields.io/badge/🔗_项目中心-131a26?style=for-the-badge&labelColor=0f131a" alt="项目中心"/></a>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=0f131a" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0f131a" alt="Python"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0f131a" alt="Docker"/>
  <img src="https://img.shields.io/badge/Render-5eead4?style=for-the-badge&labelColor=0f131a" alt="Render"/>
</p>

**AI 训练媒体治理** — 为语音与视频训练数据提供来源追溯、质量控制、合规与不可变发布。

证明模型使用了什么：每个片段可追溯、经 QC 把关、随时可发布。

> **状态：** 营销站点已在 GitHub Pages 上线。**完整平台**（API + 控制台 + 摄取）可通过桌面快捷方式本地运行，或按 [DEPLOY.md](./DEPLOY.md) 部署。

## 仓库 vs. 在线站点

| 内容 | URL |
|---|---|
| **GitHub 仓库** | [github.com/DaCameraGirl/Vaultline](https://github.com/DaCameraGirl/Vaultline) |
| **营销 / 落地页**（GitHub Pages） | [dacameragirl.github.io/Vaultline](https://dacameragirl.github.io/Vaultline/) |
| **完整平台**（API + 控制台 + 摄取） | 桌面快捷方式或 [DEPLOY.md](./DEPLOY.md) |
| **项目中心** | [dacameragirl.github.io/links](https://dacameragirl.github.io/links/) |

GitHub 显示本 README。请将**在线站点**加入书签作为营销 URL — 它与仓库页面是分开的。

## 亮点

| 层级 | 功能 |
|---|---|
| **企业 API** | FastAPI — 摄取、上传、QC、合规、发布、审计导出 |
| **营销站点** | API 运行时，`/site/index.html` 提供实时产品 UI |
| **运维控制台** | `/console/index.html` 仪表盘 — 资产、血缘、操作 |
| **CLI** | `bench.py` 用于流水线操作 |
| **目录** | SQLite 来源 + QC + 发布注册表 |
| **市场进入** | `leads/target-accounts.csv`、`marketing/one-pager.md`、外联模板 |
| **Docker** | `docker compose up` 用于类生产部署 |
| **Render** | `render.yaml` 蓝图用于托管 API |

## 本地运行（完整平台）

**最简单 — 双击桌面上的 `Vaultline`。**

首次设置：

```powershell
powershell -File setup/create-desktop-shortcut.ps1
```

或：

```powershell
setup\Launch Vaultline.bat
```

**服务器运行时的 URL：**

| 界面 | URL |
|---|---|
| 营销 + 实时 API | http://localhost:8470/site/index.html |
| 控制台 | http://localhost:8470/console/index.html |
| API 文档 | http://localhost:8470/docs |

验证一切：

```powershell
powershell -File setup/verify.ps1
```

停止：

```powershell
powershell -File setup/stop-vaultline.ps1
```

## 目标客户

| 细分 | 痛点 |
|---|---|
| 语音 AI（ASR/TTS） | 模型交付前的同意与 QC 审计 |
| 视频 / 多模态实验室 | 具备可追溯血缘的基准数据集 |
| 企业 AI 供应商 | 采购问卷中的数据治理要求 |

**采购方：** 工程副总裁 · ML 数据负责人 · AI 合规总监

## 市场推广

1. 打开 `leads/target-accounts.csv`
2. 使用 `marketing/outreach-templates.md` 中的模板
3. 分享在线链接：Pages 营销 + 托管或本地控制台演示
4. 企业通话时附上 `marketing/one-pager.md`

30 天计划见 `marketing/CAMPAIGN.md`。

## API 快速参考

```http
GET  /health
GET  /v1/dashboard
GET  /v1/assets
POST /v1/uploads
POST /v1/ingest
POST /v1/releases
GET  /v1/audit/export
```

## 部署到生产环境

见 **[DEPLOY.md](./DEPLOY.md)** — GitHub Pages（营销）、Render（API）或 Docker。

## 项目结构

```text
Vaultline/
├── api/server.py           企业 API
├── marketing/              落地页 + GTM 文案（Pages 部署源）
├── console/                运维仪表盘
├── leads/                  目标客户
├── workbench/              目录、QC、摄取、导出
├── catalog/                SQLite 注册表（本地，gitignored）
├── releases/               不可变数据集包
├── docs/assets/            README 主图 SVG
└── config/enterprise.yaml  产品配置
```

## 贡献者

- **Angela Hudson** ([DaCameraGirl](https://github.com/DaCameraGirl)) — 产品方向、GTM、测试
- **Claude** — 平台脚手架、API、控制台、营销、部署套件

## 许可证

© 2026 Angela Hudson (DaCameraGirl)。见 [LICENSE](./LICENSE)。