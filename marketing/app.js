const $ = (sel) => document.querySelector(sel);
const logEl = () => $("#activity-log");

function appendLog(message, type = "info") {
  const el = logEl();
  if (!el) return;
  const line = document.createElement("div");
  line.className = `log-line log-${type}`;
  line.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
  el.prepend(line);
}

async function api(path, options = {}) {
  const res = await fetch(path, options);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    let detail = data.detail || res.statusText || "Request failed";
    if (Array.isArray(detail)) detail = detail.map((d) => d.msg || d).join(", ");
    if (res.status === 404 && String(detail) === "Not Found") {
      detail = "Endpoint missing — restart server: powershell -File setup/restart.ps1";
    }
    throw new Error(detail);
  }
  return data;
}

async function refreshQuantum() {
  const el = $("#quantum-status");
  if (!el) return;
  try {
    const status = await api("/v1/quantum/status");
    if (status.ready) {
      el.textContent = "● IBM Quantum ready — click ⚛ Quantum seed";
      el.className = "ok";
    } else if (status.configured) {
      el.textContent = "Key set — install Qiskit: pip install -r requirements-quantum.txt";
      el.className = "warn";
    } else {
      el.textContent = "No API key — run setup/quantum-key.ps1";
      el.className = "muted";
    }
  } catch (err) {
    el.textContent = err.message.includes("restart") ? err.message : `Quantum unavailable — ${err.message}`;
    el.className = "warn";
  }
}

async function quantumSeed() {
  const btn = $("#btn-quantum");
  btn.disabled = true;
  appendLog("Requesting quantum-backed synthesis_seed from IBM…", "info");
  try {
    const assets = await api("/v1/assets?limit=1&kind=audio");
    const assetId = assets[0]?.asset_id;
    const url = assetId
      ? `/v1/quantum/seed?asset_id=${encodeURIComponent(assetId)}`
      : "/v1/quantum/seed";
    const result = await api(url, { method: "POST" });
    appendLog(`Quantum seed: ${result.synthesis_seed} (${result.backend})`, "ok");
    if (result.attached_to) appendLog(`Attached to asset ${result.attached_to}`, "ok");
    await refreshLive();
  } catch (err) {
    appendLog(`Quantum seed failed: ${err.message}`, "error");
  } finally {
    btn.disabled = false;
  }
}

async function refreshLive() {
  try {
    const health = await api("/health");
    const dash = await api("/v1/dashboard");
    const assets = await api("/v1/assets?limit=8");

    $("#live-status").textContent = health.status === "ok" ? "● Live" : "Offline";
    $("#live-status").className = health.status === "ok" ? "pill ok" : "pill bad";
    $("#stat-assets").textContent = health.catalog?.total_assets ?? 0;
    $("#stat-releases").textContent = health.catalog?.releases ?? 0;
    $("#stat-pass").textContent = health.catalog?.by_qc_verdict?.pass ?? 0;
    $("#stat-fail").textContent = health.catalog?.by_qc_verdict?.fail ?? 0;

    const tbody = $("#asset-rows");
    tbody.innerHTML = assets.length
      ? assets.map((a) => `<tr>
          <td title="${a.asset_id}">${a.asset_id.slice(0, 20)}…</td>
          <td>${a.kind}</td>
          <td class="${a.qc_verdict === 'pass' ? 'ok' : a.qc_verdict === 'fail' ? 'bad' : ''}">${a.qc_verdict || "—"}</td>
          <td>${a.source_tool}</td>
        </tr>`).join("")
      : `<tr><td colspan="4" class="muted">No assets yet — run the live demo or upload a file.</td></tr>`;
  } catch (err) {
    $("#live-status").textContent = "● API offline";
    $("#live-status").className = "pill bad";
    appendLog(`Cannot reach API: ${err.message}. Run: powershell -File setup/start.ps1`, "error");
  }
}

async function repairCatalog() {
  appendLog("Repairing catalog — compliance fill, audio normalize, re-QC…", "info");
  try {
    const result = await api("/v1/catalog/repair", { method: "POST" });
    appendLog(`Repair done: ${result.now_passing} passing, ${result.still_failing} still failing`, "ok");
    for (const asset of result.assets || []) {
      if (asset.after !== asset.before) {
        appendLog(`${asset.path}: ${asset.before || "?"} → ${asset.after}`, asset.after === "pass" ? "ok" : "warn");
      }
      for (const failure of asset.failures || []) {
        appendLog(`  ↳ ${failure}`, "warn");
      }
    }
    await refreshLive();
  } catch (err) {
    appendLog(`Repair failed: ${err.message}`, "error");
  }
}

async function runDemo() {
  const btn = $("#btn-demo");
  btn.disabled = true;
  appendLog("Starting live demo…", "info");
  try {
    const result = await api("/v1/demo/run?profile=asr_corpus_v1", { method: "POST" });
    for (const step of result.log || []) {
      appendLog(`${step.step}: ${step.detail}`, step.status === "warn" ? "warn" : "ok");
    }
    appendLog(`Done — asset ${result.asset_id} QC=${result.qc_verdict}`, "ok");
    await refreshLive();
  } catch (err) {
    appendLog(`Demo failed: ${err.message}`, "error");
  } finally {
    btn.disabled = false;
  }
}

async function uploadFile(file) {
  appendLog(`Uploading ${file.name}…`, "info");
  const form = new FormData();
  form.append("file", file);
  try {
    const result = await api("/v1/uploads?profile=asr_corpus_v1", { method: "POST", body: form });
    appendLog(`Uploaded ${result.uploaded} → QC ${result.result?.qc_verdict || "pending"}`, "ok");
    await refreshLive();
  } catch (err) {
    appendLog(`Upload failed: ${err.message}`, "error");
  }
}

async function exportAudit() {
  appendLog("Exporting audit bundle…", "info");
  try {
    window.open("/v1/audit/download", "_blank");
    appendLog("Audit JSON download started.", "ok");
  } catch (err) {
    appendLog(`Audit export failed: ${err.message}`, "error");
  }
}

async function submitDemoForm(ev) {
  ev.preventDefault();
  const body = {
    name: $("#demo-name").value.trim(),
    email: $("#demo-email").value.trim(),
    company: $("#demo-company").value.trim(),
    message: $("#demo-message").value.trim(),
  };
  if (!body.name || !body.email || !body.company) {
    appendLog("Fill in name, email, and company.", "warn");
    return;
  }
  try {
    const result = await api("/v1/leads/demo-request", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    $("#demo-form-status").textContent = result.message;
    appendLog(`Demo request saved for ${body.email}`, "ok");
    ev.target.reset();
  } catch (err) {
    appendLog(`Demo request failed: ${err.message}`, "error");
  }
}

function init() {
  $("#btn-demo")?.addEventListener("click", runDemo);
  $("#btn-audit")?.addEventListener("click", exportAudit);
  $("#btn-quantum")?.addEventListener("click", quantumSeed);
  $("#btn-refresh")?.addEventListener("click", refreshLive);
  $("#btn-repair")?.addEventListener("click", repairCatalog);
  $("#demo-form")?.addEventListener("submit", submitDemoForm);

  const drop = $("#dropzone");
  const input = $("#file-input");
  drop?.addEventListener("click", () => input?.click());
  drop?.addEventListener("dragover", (e) => { e.preventDefault(); drop.classList.add("hover"); });
  drop?.addEventListener("dragleave", () => drop.classList.remove("hover"));
  drop?.addEventListener("drop", (e) => {
    e.preventDefault();
    drop.classList.remove("hover");
    const file = e.dataTransfer?.files?.[0];
    if (file) uploadFile(file);
  });
  input?.addEventListener("change", () => {
    const file = input.files?.[0];
    if (file) uploadFile(file);
  });

  refreshLive();
  refreshQuantum();
  setInterval(refreshLive, 8000);
}

document.addEventListener("DOMContentLoaded", init);