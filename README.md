# AI Research Media Workbench

A local pipeline for building and refining digital assets for AI research using **Shotcut**, **OpenShot**, **Lightworks**, **Ardour**, and **LMMS**.

Editors handle creative work. This repo handles structure, validation, normalization, and dataset manifests.

## What each tool does here

| Tool | Role in this project |
|------|----------------------|
| **Shotcut** | Trim and segment raw video into training clips |
| **OpenShot** | Fast explainer edits and internal demo cuts |
| **Lightworks** | Polished reels for papers, grants, and conferences |
| **Ardour** | Clean speech, normalize levels, export stems |
| **LMMS** | Synthetic music and controlled soundscapes |

## Pipeline stages

```
assets/00_inbox          Drop anything here first
assets/01_video_raw      Routed video and image sources
assets/02_audio_raw      Routed audio sources
assets/03_editing        Exports from Shotcut / OpenShot
assets/04_audio_stems    Exports from Ardour / LMMS
assets/05_processed      ffmpeg-normalized or segmented output
assets/06_exports        ML-ready final assets and demo deliverables
manifests/               JSON manifests for training pipelines
projects/                Saved editor project files by tool
```

## Quick start

### 1. Install the editors

```powershell
powershell -File setup/install-tools.ps1
```

After installing, detect executables:

```powershell
powershell -File setup/detect-tools.ps1
```

### 2. Set up Python helpers

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Requires **ffmpeg** and **ffprobe** on PATH (you already have ffmpeg if `ffmpeg -version` works).

### 3. Launch a tool against project folders

```powershell
powershell -File setup/launch-tools.ps1 shotcut
powershell -File setup/launch-tools.ps1 ardour
powershell -File setup/launch-tools.ps1 all
```

### 4. Run the asset pipeline

```powershell
# Route new files from inbox into raw folders
python scripts/pipeline.py route-inbox

# Check what is in each stage
python scripts/pipeline.py status

# Split a long capture into 5-second training clips
python scripts/pipeline.py segment --input assets/01_video_raw/demo_run.mp4 --length 5

# Normalize Ardour/LMMS stems for ASR datasets
python scripts/pipeline.py normalize-audio --preset speech_asr

# Validate exports against presets in config/export-presets.yaml
python scripts/pipeline.py validate --path assets/06_exports --write-manifest

# Build a dataset manifest for downstream training code
python scripts/pipeline.py manifest --path assets/06_exports --output dataset_manifest.json
```

## Recommended workflow

1. Drop raw captures into `assets/00_inbox`, then run `route-inbox`.
2. Use **Shotcut** to trim and export rough clips into `assets/03_editing`.
3. Pull dialogue and speech into **Ardour** for cleanup; export stems to `assets/04_audio_stems`.
4. Use **LMMS** when you need repeatable synthetic audio conditions.
5. Run `segment` or `normalize-audio` to produce ML-ready files in `assets/05_processed`.
6. Use **Lightworks** for final demo reels into `assets/06_exports/demos`.
7. Run `validate` and `manifest` before handing assets to training or eval code.

## Export presets

Presets live in `config/export-presets.yaml`:

- `video.training_720p` / `video.training_1080p` for clip datasets
- `audio.speech_asr` (16 kHz mono) and `audio.speech_tts` (44.1 kHz)
- `audio.music_sfx` for LMMS stems
- `video.demo_reel` for polished deliverables

Edit these to match your model requirements, then re-run `validate`.

## File naming

Use `{subject}_{action}_{index}` so manifests stay machine-readable:

```
interview_wave_0001.wav
demo_run_inference_0012.mp4
synth_pad_loop_0040.wav
```

## Project layout

```
ai-research-media-workbench/
├── assets/              Pipeline stages (inbox → exports)
├── config/              Export presets and tool paths
├── manifests/           Generated JSON manifests
├── projects/            Editor project files by tool
├── scripts/pipeline.py    CLI automation
├── setup/               Install, detect, and launch helpers
└── templates/           Manifest JSON schema
```

## Notes

- `scripts/pipeline.py` uses ffmpeg for normalization and segmentation; editors remain your creative surface.
- If a tool is not installed yet, `launch-tools.ps1` prints a clear message instead of failing silently.
- Pair this with training/eval repos by pointing them at `manifests/dataset_manifest.json`.