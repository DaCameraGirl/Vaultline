# Deploying Vaultline

Vaultline is two surfaces:

1. **Marketing site** — static landing on GitHub Pages (no API).
2. **Platform** — FastAPI + console on your machine, Docker, or Render.

## Live URLs

| Surface | URL |
|---------|-----|
| Marketing (Pages) | https://dacameragirl.github.io/Vaultline/ |
| Full platform (after Render) | `https://<your-vaultline-service>.onrender.com` |
| API docs | `/docs` on whichever host is running the API |

## Part A — GitHub Pages (marketing)

Already wired: push to `main` runs `.github/workflows/pages.yml`.

The Pages build is a **read-only landing page**. Demo forms and live QC need the API (Part B).

## Part B — Run locally (development)

```powershell
powershell -File setup/create-desktop-shortcut.ps1
# Double-click Vaultline on Desktop, or:
setup\Launch Vaultline.bat
```

Verify:

```powershell
powershell -File setup/verify.ps1
```

## Part C — Render (hosted API)

1. [render.com](https://render.com) → **New → Blueprint** → select **Vaultline**.
2. Apply `render.yaml` (service `vaultline-api`).
3. Add secrets in Render → **Environment**:
   - `IBM_QUANTUM_API_KEY` (optional, for quantum seed feature)
4. Note the public URL, e.g. `https://vaultline-api.onrender.com`.
5. Open `https://vaultline-api.onrender.com/site/index.html` for the live marketing + API UI.

Free tier sleeps after idle; first request may take ~30s.

## Part D — Docker

```powershell
docker compose up --build
```

Open http://localhost:8470/site/index.html

## Hub and desktop links

- **Angela's Projects hub:** https://dacameragirl.github.io/links/ (Open = Pages marketing)
- **Desktop shortcut:** launches local full platform (`setup/launch-vaultline.ps1`)

After Render is live, update the hub `Open` link to the Render URL for the full console.