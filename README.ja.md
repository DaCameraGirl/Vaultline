<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Vaultline — AI トレーニングメディアガバナンス" width="100%"/>
</p>

# Vaultline

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/🇺🇸_English-131a26?style=for-the-badge&labelColor=0f131a" alt="English"/></a>
  <a href="README.es.md"><img src="https://img.shields.io/badge/🇪🇸_Español-131a26?style=for-the-badge&labelColor=0f131a" alt="Español"/></a>
  <a href="README.fr.md"><img src="https://img.shields.io/badge/🇫🇷_Français-131a26?style=for-the-badge&labelColor=0f131a" alt="Français"/></a>
  <a href="README.de.md"><img src="https://img.shields.io/badge/🇩🇪_Deutsch-131a26?style=for-the-badge&labelColor=0f131a" alt="Deutsch"/></a>
  <a href="README.pt-BR.md"><img src="https://img.shields.io/badge/🇧🇷_Português-131a26?style=for-the-badge&labelColor=0f131a" alt="Português"/></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/🇨🇳_中文-131a26?style=for-the-badge&labelColor=0f131a" alt="中文"/></a>
  <a href="README.ja.md"><img src="https://img.shields.io/badge/🇯🇵_日本語-5eead4?style=for-the-badge&labelColor=0f131a" alt="日本語"/></a>
  <a href="README.ko.md"><img src="https://img.shields.io/badge/🇰🇷_한국어-131a26?style=for-the-badge&labelColor=0f131a" alt="한국어"/></a>
  <a href="README.it.md"><img src="https://img.shields.io/badge/🇮🇹_Italiano-131a26?style=for-the-badge&labelColor=0f131a" alt="Italiano"/></a>
  <a href="README.ar.md"><img src="https://img.shields.io/badge/🇸🇦_العربية-131a26?style=for-the-badge&labelColor=0f131a" alt="العربية"/></a>
</p>

<p align="center">
  <a href="https://dacameragirl.github.io/Vaultline/"><img src="https://img.shields.io/badge/🌐_ライブサイト-5eead4?style=for-the-badge&labelColor=0f131a" alt="ライブサイト"/></a>
  <a href="https://dacameragirl.github.io/links/"><img src="https://img.shields.io/badge/🔗_プロジェクトハブ-131a26?style=for-the-badge&labelColor=0f131a" alt="プロジェクトハブ"/></a>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=0f131a" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0f131a" alt="Python"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0f131a" alt="Docker"/>
  <img src="https://img.shields.io/badge/Render-5eead4?style=for-the-badge&labelColor=0f131a" alt="Render"/>
</p>

**AI トレーニングメディアガバナンス** — 音声・動画トレーニングデータのプロベナンス、QC、コンプライアンス、不変リリース。

モデルに何が入ったかを証明：すべてのクリップを追跡し、QC でゲートし、リリース準備完了。

> **ステータス：** マーケティングサイトは GitHub Pages で公開中。**フルプラットフォーム**（API + コンソール + インジェスト）はデスクトップショートカットでローカル実行、または [DEPLOY.md](./DEPLOY.md) でデプロイ可能。

## リポジトリ vs. ライブサイト

| 内容 | URL |
|---|---|
| **GitHub リポジトリ** | [github.com/DaCameraGirl/Vaultline](https://github.com/DaCameraGirl/Vaultline) |
| **マーケティング / ランディング**（GitHub Pages） | [dacameragirl.github.io/Vaultline](https://dacameragirl.github.io/Vaultline/) |
| **フルプラットフォーム**（API + コンソール + インジェスト） | デスクトップショートカットまたは [DEPLOY.md](./DEPLOY.md) |
| **プロジェクトハブ** | [dacameragirl.github.io/links](https://dacameragirl.github.io/links/) |

GitHub にはこの README が表示されます。マーケティング URL には**ライブサイト**をブックマークしてください — リポジトリページとは別です。

## ハイライト

| レイヤー | 機能 |
|---|---|
| **エンタープライズ API** | FastAPI — インジェスト、アップロード、QC、コンプライアンス、リリース、監査エクスポート |
| **マーケティングサイト** | API 実行時に `/site/index.html` でライブ製品 UI |
| **Ops コンソール** | `/console/index.html` のダッシュボード — アセット、系譜、アクション |
| **CLI** | パイプライン操作用 `bench.py` |
| **カタログ** | SQLite プロベナンス + QC + リリースレジストリ |
| **Go-to-market** | `leads/target-accounts.csv`、`marketing/one-pager.md`、アウトリーチテンプレート |
| **Docker** | 本番スタイルのデプロイに `docker compose up` |
| **Render** | ホスト API 用 `render.yaml` ブループリント |

## ローカル実行（フルプラットフォーム）

**最も簡単 — デスクトップの `Vaultline` をダブルクリック。**

初回セットアップ：

```powershell
powershell -File setup/create-desktop-shortcut.ps1
```

または：

```powershell
setup\Launch Vaultline.bat
```

**サーバー実行時の URL：**

| 画面 | URL |
|---|---|
| マーケティング + ライブ API | http://localhost:8470/site/index.html |
| コンソール | http://localhost:8470/console/index.html |
| API ドキュメント | http://localhost:8470/docs |

すべて検証：

```powershell
powershell -File setup/verify.ps1
```

停止：

```powershell
powershell -File setup/stop-vaultline.ps1
```

## 購入者

| セグメント | 課題 |
|---|---|
| 音声 AI（ASR/TTS） | モデル出荷前の同意 + QC 監査 |
| 動画 / マルチモーダルラボ | 追跡可能な系譜を持つベンチマークデータセット |
| エンタープライズ AI ベンダー | データガバナンスに関する調達アンケート |

**バイヤー：** VP Engineering · Head of ML Data · Director AI Compliance

## マーケティング

1. `leads/target-accounts.csv` を開く
2. `marketing/outreach-templates.md` のテンプレートを使用
3. ライブリンクを共有：Pages マーケティング + ホストまたはローカルコンソールデモ
4. エンタープライズコールで `marketing/one-pager.md` を添付

30 日間プランは `marketing/CAMPAIGN.md` を参照。

## API クイックリファレンス

```http
GET  /health
GET  /v1/dashboard
GET  /v1/assets
POST /v1/uploads
POST /v1/ingest
POST /v1/releases
GET  /v1/audit/export
```

## 本番デプロイ

**[DEPLOY.md](./DEPLOY.md)** を参照 — GitHub Pages（マーケティング）、Render（API）、または Docker。

## プロジェクト構成

```text
Vaultline/
├── api/server.py           エンタープライズ API
├── marketing/              ランディング + GTM コピー（Pages デプロイ元）
├── console/                Ops ダッシュボード
├── leads/                  ターゲットアカウント
├── workbench/              カタログ、QC、インジェスト、エクスポート
├── catalog/                SQLite レジストリ（ローカル、gitignored）
├── releases/               不変データセットバンドル
├── docs/assets/            README ヒーロー SVG
└── config/enterprise.yaml  製品設定
```

## コントリビューター

- **Angela Hudson** ([DaCameraGirl](https://github.com/DaCameraGirl)) — プロダクト方向性、GTM、テスト
- **Claude** — プラットフォームスキャフォールド、API、コンソール、マーケティング、デプロイキット

## ライセンス

© 2026 Angela Hudson (DaCameraGirl)。[LICENSE](./LICENSE) を参照。