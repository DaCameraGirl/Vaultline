const $ = (sel) => document.querySelector(sel);
const logEl = () => $("#log");

function log(msg, type = "info") {
  const el = logEl();
  if (!el) return;
  const line = document.createElement("div");
  line.className = `log log-${type}`;
  line.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
  el.prepend(line);
}

async function api(path, options = {}) {
  const res = await fetch(path, options);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    let detail = data.detail || res.statusText;
    if (Array.isArray(detail)) detail = detail.join(", ");
    throw new Error(detail);
  }
  return data;
}

function qcClass(v) {
  if (v === "pass") return "ok";
  if (v === "fail") return "bad";
  return "muted";
}

async function loadDashboard() {
  const dash = await api("/v1/dashboard");
  const assets = await api("/v1/assets?limit=100");
  const health = await api("/health");

  $("#status").textContent = "● Live";
  $("#status").className = "pill ok";
  $("#total").textContent = dash.summary.total_assets;
  $("#releases").textContent = dash.summary.releases;
  $("#passed").textContent = dash.summary.by_qc_verdict?.pass ?? 0;
  $("#failed").textContent = dash.summary.by_qc_verdict?.fail ?? 0;
  $("#version").textContent = health.version || "—";

  const tbody = $("#assets");
  if (!assets.length) {
    tbody.innerHTML = `<tr><td colspan="7" class="muted">No assets — go to <a href="/site/index.html">Home</a> and run demo.</td></tr>`;
    return;
  }

  tbody.innerHTML = assets.map((a) => `<tr data-id="${a.asset_id}" class="row-click">
    <td class="${qcClass(a.qc_verdict)}">${a.qc_verdict || "—"}</td>
    <td>${a.kind}</td>
    <td>${a.stage}</td>
    <td title="${a.rel_path}">${a.rel_path.split("/").pop()}</td>
    <td>${a.qc_score != null ? (a.qc_score * 100).toFixed(0) + "%" : "—"}</td>
    <td>${a.profile || "—"}</td>
    <td><button class="link-btn" data-lineage="${a.asset_id}">Lineage</button></td>
  </tr>`).join("");

  tbody.querySelectorAll("[data-lineage]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      showLineage(btn.dataset.lineage);
    });
  });

  tbody.querySelectorAll(".row-click").forEach((row) => {
    row.addEventListener("click", () => showAsset(assets.find((a) => a.asset_id === row.dataset.id)));
  });
}

async function showLineage(assetId) {
  try {
    const chain = await api(`/v1/assets/${encodeURIComponent(assetId)}/lineage`);
    $("#detail").textContent = JSON.stringify(chain, null, 2);
    log(`Lineage loaded for ${assetId}`, "ok");
  } catch (err) {
    log(`Lineage failed: ${err.message}`, "error");
  }
}

function showAsset(asset) {
  if (!asset) return;
  $("#detail").textContent = JSON.stringify(asset, null, 2);
}

async function repair() {
  log("Running catalog repair…");
  try {
    const r = await api("/v1/catalog/repair", { method: "POST" });
    log(`Repair: ${r.now_passing} pass, ${r.still_failing} fail`, "ok");
    await loadDashboard();
  } catch (err) {
    log(`Repair failed: ${err.message}`, "error");
  }
}

async function runDemo() {
  log("Running live demo…");
  try {
    const r = await api("/v1/demo/run?profile=asr_corpus_v1", { method: "POST" });
    log(`Demo asset ${r.asset_id} — QC ${r.qc_verdict}`, r.qc_verdict === "pass" ? "ok" : "warn");
    await loadDashboard();
  } catch (err) {
    log(`Demo failed: ${err.message}`, "error");
  }
}

function init() {
  $("#btn-repair")?.addEventListener("click", repair);
  $("#btn-demo")?.addEventListener("click", runDemo);
  $("#btn-refresh")?.addEventListener("click", () => loadDashboard().catch((e) => log(e.message, "error")));
  $("#btn-audit")?.addEventListener("click", () => {
    window.open("/v1/audit/download", "_blank");
    log("Audit download started", "ok");
  });

  loadDashboard().catch((err) => {
    $("#status").textContent = "● Offline";
    $("#status").className = "pill bad";
    log(`API offline: ${err.message}`, "error");
  });
  setInterval(() => loadDashboard().catch(() => {}), 12000);
}

document.addEventListener("DOMContentLoaded", init);