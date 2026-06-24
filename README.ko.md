<p align="center">
  <img src="docs/assets/readme-hero.svg" alt="Vaultline — AI 학습 미디어 거버넌스" width="100%"/>
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
  <a href="README.ko.md"><img src="https://img.shields.io/badge/🇰🇷_한국어-5eead4?style=for-the-badge&labelColor=0f131a" alt="한국어"/></a>
  <a href="README.it.md"><img src="https://img.shields.io/badge/🇮🇹_Italiano-131a26?style=for-the-badge&labelColor=0f131a" alt="Italiano"/></a>
  <a href="README.ar.md"><img src="https://img.shields.io/badge/🇸🇦_العربية-131a26?style=for-the-badge&labelColor=0f131a" alt="العربية"/></a>
</p>

<p align="center">
  <a href="https://dacameragirl.github.io/Vaultline/"><img src="https://img.shields.io/badge/🌐_라이브_사이트-5eead4?style=for-the-badge&labelColor=0f131a" alt="라이브 사이트"/></a>
  <a href="https://dacameragirl.github.io/links/"><img src="https://img.shields.io/badge/🔗_프로젝트_허브-131a26?style=for-the-badge&labelColor=0f131a" alt="프로젝트 허브"/></a>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=0f131a" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0f131a" alt="Python"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0f131a" alt="Docker"/>
  <img src="https://img.shields.io/badge/Render-5eead4?style=for-the-badge&labelColor=0f131a" alt="Render"/>
</p>

**AI 학습 미디어 거버넌스** — 음성 및 영상 학습 데이터의 출처, QC, 컴플라이언스, 불변 릴리스.

모델에 무엇이 들어갔는지 증명: 모든 클립 추적, QC 게이트 통과, 릴리스 준비 완료.

> **상태:** 마케팅 사이트는 GitHub Pages에서 라이브 중입니다. **전체 플랫폼**(API + 콘솔 + 수집)은 데스크톱 바로가기로 로컬 실행하거나 [DEPLOY.md](./DEPLOY.md)로 배포할 수 있습니다.

## 저장소 vs. 라이브 사이트

| 항목 | URL |
|---|---|
| **GitHub 저장소** | [github.com/DaCameraGirl/Vaultline](https://github.com/DaCameraGirl/Vaultline) |
| **마케팅 / 랜딩** (GitHub Pages) | [dacameragirl.github.io/Vaultline](https://dacameragirl.github.io/Vaultline/) |
| **전체 플랫폼** (API + 콘솔 + 수집) | 데스크톱 바로가기 또는 [DEPLOY.md](./DEPLOY.md) |
| **프로젝트 허브** | [dacameragirl.github.io/links](https://dacameragirl.github.io/links/) |

GitHub에는 이 README가 표시됩니다. 마케팅 URL은 **라이브 사이트**를 북마크하세요 — 저장소 페이지와 별개입니다.

## 하이라이트

| 계층 | 기능 |
|---|---|
| **엔터프라이즈 API** | FastAPI — 수집, 업로드, QC, 컴플라이언스, 릴리스, 감사보내기 |
| **마케팅 사이트** | API 실행 시 `/site/index.html`에서 라이브 제품 UI |
| **Ops 콘솔** | `/console/index.html` 대시보드 — 자산, 계보, 작업 |
| **CLI** | 파이프라인 작업용 `bench.py` |
| **카탈로그** | SQLite 출처 + QC + 릴리스 레지스트리 |
| **Go-to-market** | `leads/target-accounts.csv`, `marketing/one-pager.md`, 아웃리치 템플릿 |
| **Docker** | 프로덕션 스타일 배포에 `docker compose up` |
| **Render** | 호스팅 API용 `render.yaml` 블루프린트 |

## 로컬 실행 (전체 플랫폼)

**가장 쉬운 방법 — 데스크톱의 `Vaultline` 더블클릭.**

최초 설정:

```powershell
powershell -File setup/create-desktop-shortcut.ps1
```

또는:

```powershell
setup\Launch Vaultline.bat
```

**서버 실행 시 URL:**

| 화면 | URL |
|---|---|
| 마케팅 + 라이브 API | http://localhost:8470/site/index.html |
| 콘솔 | http://localhost:8470/console/index.html |
| API 문서 | http://localhost:8470/docs |

모두 검증:

```powershell
powershell -File setup/verify.ps1
```

중지:

```powershell
powershell -File setup/stop-vaultline.ps1
```

## 구매 대상

| 세그먼트 | 페인 포인트 |
|---|---|
| 음성 AI (ASR/TTS) | 모델 출하 전 동의 + QC 감사 |
| 영상 / 멀티모달 랩 | 추적 가능한 계보를 가진 벤치마크 데이터셋 |
| 엔터프라이즈 AI 벤더 | 데이터 거버넌스 관련 조달 설문 |

**구매자:** VP Engineering · Head of ML Data · Director AI Compliance

## 마케팅

1. `leads/target-accounts.csv` 열기
2. `marketing/outreach-templates.md`의 템플릿 사용
3. 라이브 링크 공유: Pages 마케팅 + 호스팅 또는 로컬 콘솔 데모
4. 엔터프라이즈 콜에서 `marketing/one-pager.md` 첨부

30일 계획은 `marketing/CAMPAIGN.md` 참조.

## API 빠른 참조

```http
GET  /health
GET  /v1/dashboard
GET  /v1/assets
POST /v1/uploads
POST /v1/ingest
POST /v1/releases
GET  /v1/audit/export
```

## 프로덕션 배포

**[DEPLOY.md](./DEPLOY.md)** 참조 — GitHub Pages(마케팅), Render(API) 또는 Docker.

## 프로젝트 구조

```text
Vaultline/
├── api/server.py           엔터프라이즈 API
├── marketing/              랜딩 + GTM 카피 (Pages 배포 소스)
├── console/                Ops 대시보드
├── leads/                  타겟 계정
├── workbench/              카탈로그, QC, 수집,보내기
├── catalog/                SQLite 레지스트리 (로컬, gitignored)
├── releases/               불변 데이터셋 번들
├── docs/assets/            README 히어로 SVG
└── config/enterprise.yaml  제품 설정
```

## 기여자

- **Angela Hudson** ([DaCameraGirl](https://github.com/DaCameraGirl)) — 제품 방향, GTM, 테스트
- **Claude** — 플랫폼 스캐폴드, API, 콘솔, 마케팅, 배포 키트

## 라이선스

© 2026 Angela Hudson (DaCameraGirl). [LICENSE](./LICENSE) 참조.