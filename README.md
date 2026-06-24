# SignalForge Workbench

Research media infrastructure for teams that ship **reproducible multimodal datasets** — not one-off demo folders.

Editors (**Shotcut**, **OpenShot**, **Lightworks**, **Ardour**, **LMMS**) are where creative work happens. SignalForge is the layer the industry actually needs underneath: **catalog, provenance, QC gates, compliance, and immutable releases** wired to modern training exports.

## Why teams keep this running

| Problem in the wild | What SignalForge does |
|---------------------|------------------------|
| "Which clip is the canonical one?" | SHA-256 + content signatures, duplicate detection |
| "What transform produced this file?" | Full provenance chain per asset |
| "Can this go in the training split?" | Policy-driven QC with pass/fail verdicts |
| "Do we have consent/license on every clip?" | Compliance metadata enforced at release time |
| "What exactly did we ship last month?" | Versioned releases with JSONL, HuggingFace, and WebDataset bundles |

## Architecture

```
Editors (human creative surface)
  Shotcut / OpenShot / Lightworks  → video
  Ardour / LMMS                    → audio
           ↓
SignalForge Workbench (machine layer)
  ingest → catalog.db → QC policies → compliance → release bundles
           ↓
Training / eval stacks
  HuggingFace · JSONL · WebDataset · custom loaders
```

## Quick start

```powershell
cd "C:\Users\enter\Documents\Apps_And_Code\01_App_Project_Folders\ai-research-media-workbench"

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Install and wire editor paths
powershell -File setup/install-tools.ps1
powershell -File setup/detect-tools.ps1
```

Requires **ffmpeg** / **ffprobe** on PATH.

## Daily operations

```powershell
# Operational dashboard
python bench.py dashboard

# See dataset profiles and QC policies
python bench.py profiles

# Drop files in assets/00_inbox, then ingest + gate
python bench.py ingest --inbox --profile multimodal_v1

# Or register an existing tree
python bench.py ingest --path assets/06_exports --profile asr_corpus_v1

# Attach compliance before release
python bench.py compliance --asset <asset_id> --field license --value "CC-BY-4.0"
python bench.py compliance --asset <asset_id> --field consent --value "signed-2026-06-01"

# Run QC explicitly
python bench.py qc --policy speech_audio --path assets/04_audio_stems

# Trace lineage
python bench.py lineage <asset_id>

# Ship an immutable release (blocked until profile minimums are met)
python bench.py release create --profile multimodal_v1 --version 1.0.0 --notes "June pilot split"

# Export for training pipelines
python bench.py export --format huggingface --profile multimodal_v1 --passing-only --output manifests/hf_export

# Watch inbox during active capture sessions
python bench.py watch --profile multimodal_v1
```

## Dataset profiles

Profiles define what "release-ready" means. Config: `config/dataset-profiles.yaml`.

| Profile | Use case |
|---------|----------|
| `multimodal_v1` | Video+audio clips for multimodal pretraining/eval |
| `asr_corpus_v1` | 16 kHz speech corpus for ASR |
| `tts_eval_v1` | 44.1 kHz speech for TTS evaluation |
| `demo_reel_v1` | Publication-grade research reels |
| `synthetic_audio_v1` | Controlled LMMS/Ardour benchmark stems |

Each profile maps to a **QC policy** in `config/qc-policies.yaml` with measurable gates: duration, resolution, FPS, loudness (LUFS), silence ratio, blur score, and required compliance fields.

## Editor roles

| Tool | When to reach for it |
|------|----------------------|
| **Shotcut** | Segment long captures into training-length clips |
| **OpenShot** | Fast internal explainers |
| **Lightworks** | Conference and grant reels (`demo_reel_v1`) |
| **Ardour** | Speech cleanup, stem export, loudness prep |
| **LMMS** | Repeatable synthetic audio (`synthetic_audio_v1`) |

Launch any editor against project folders:

```powershell
powershell -File setup/launch-tools.ps1 shotcut
powershell -File setup/launch-tools.ps1 ardour
```

## Release bundles

`python bench.py release create` writes to `releases/<release_id>/`:

- `release_manifest.json` — full asset records + hashes
- `multimodal.jsonl` — one row per asset for custom loaders
- `huggingface/` — `dataset_info.json` + `train.jsonl`
- `webdataset_*.tar` — shard-ready tar bundles with sidecar JSON

Releases are registered in `catalog/catalog.db` and are intended to be **immutable** — the unit you cite in papers, eval harnesses, and audit trails.

## Project layout

```
ai-research-media-workbench/
├── bench.py                 Primary CLI
├── workbench/               Catalog, QC, ingest, export engine
├── catalog/catalog.db       Asset registry (local SQLite)
├── config/
│   ├── dataset-profiles.yaml
│   ├── qc-policies.yaml
│   ├── compliance-template.yaml
│   ├── export-presets.yaml
│   └── tool-paths.yaml
├── assets/                  Pipeline stages (inbox → exports)
├── releases/                Immutable versioned dataset bundles
├── projects/                Editor project files
└── setup/                   Install, detect, launch helpers
```

## Compliance

Before releasing human-subject or licensed media, set compliance fields per asset. Template: `config/compliance-template.yaml`.

Required fields vary by profile (e.g. `multimodal_v1` requires `license` + `consent`; `asr_corpus_v1` also requires `speaker_id`).

## Legacy CLI

`scripts/pipeline.py` forwards to `bench.py` for older commands (`status`, `route-inbox`, etc.). New work should use `bench.py` directly.