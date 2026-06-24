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
  if (!res.ok) throw new Error(data.detail || res.statusText || "Request failed");
  return data;
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
  $("#btn-refresh")?.addEventListener("click", refreshLive);
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
  setInterval(refreshLive, 8000);
}

document.addEventListener("DOMContentLoaded", init);