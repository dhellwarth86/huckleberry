# E.2.0 New File Design — Huckleberry_AI_phase2.v1.0.0.html

**Date:** 2026-04-30
**Branch:** `phase2-v0.3-E2-0-strip-plan`
**Companion docs:** `E2_0_STRIP_PLAN.md`, `E2_0_API_CLIENT_SPEC.md`, `E2_0_TEST_FLOOR_PROPOSAL.md`
**Phase:** E.2.0 (read-only diagnostic — this document designs the new file; E.2.1 creates it)
**Source file:** `frontend/Huckleberry_AI_6.3.5_Scope.html` (SHA-1 `cf3765d61fd6f17de46024a3a84c62f25b19b3c5`, 8,694 lines)
**Target file:** `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` (estimated ~4,841–4,941 lines)

---

## §1 — File header (CDN imports, style block)

### §1.1 — DOCTYPE + `<head>` + CDN imports

The new file preserves the v6.3.5 `<head>` structure with minimal edits:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Huckleberry AI — Phase 2</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/openseadragon.min.js"></script>
<script src="https://unpkg.com/konva@9.3.0/konva.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Outfit:wght@300;400;500;600;700&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
```

**What changes from v6.3.5:**

| Element | v6.3.5 | phase2.v1.0.0 | Reason |
|---|---|---|---|
| `<title>` | `Huckleberry AI 6.0 — TracePoint Geometry Engine` | `Huckleberry AI — Phase 2` | No longer a geometry engine; now an API-connected viewer |
| CDN deps | pdf.js, openseadragon, konva, xlsx | **Same four, same versions** | All four are keeper frontend concerns (F2, F3, F4, F6 per audit §4.3) |

**No new CDN deps added.** The API client (D3) uses browser-native `fetch()` — no axios, no external HTTP library. The no-build-step constraint from Phase 1 is preserved.

### §1.2 — `<style>` block

The `<style>` block (v6.3.5 lines 12–1209, ~1,198 lines) carries forward with targeted deletions of pipeline-specific CSS:

**Sections deleted (pipeline CSS per S14 in strip plan):**

| CSS section | v6.3.5 lines | Content | Why removed |
|---|---|---|---|
| `.pipeline-stages` styles | 193–221 (~29 lines) | Sidebar pipeline stage list styling | Pipeline sidebar section stripped |
| `@keyframes pulse` | 223–226 (~4 lines) | Pipeline stage animation | Only used by pipeline stage `.ps-num` |
| `.stages-grid` / `.stage-card` styles | 402–464 (~63 lines) | Pipeline tab card grid styling | Pipeline tab stripped |

**Sections added:**

| CSS section | Content | Purpose |
|---|---|---|
| `.status-bar .sb-health-dot` | 8×8 circle indicator, three color states | Visual health indicator for API connection state |
| `.status-bar .sb-health-dot.connected` | `background: var(--green)` | API reachable |
| `.status-bar .sb-health-dot.checking` | `background: var(--amber)` | Health probe in flight |
| `.status-bar .sb-health-dot.unreachable` | `background: var(--red)` | API not responding |

**CSS `:root` variables:** Unchanged. The visual identity (colors, fonts, spacing) carries forward completely.

**Net CSS change:** ~96 lines deleted, ~15 lines added. The style block shrinks from ~1,198 to ~1,117 lines.

---

## §2 — Body markup (7-tab structure, status bar)

### §2.1 — Header

The header preserves the Huckleberry logo mark and version badge. Changes:

| Element | v6.3.5 | phase2.v1.0.0 |
|---|---|---|
| Version badge | `v6.3.5` | `phase2.v1.0.0` |
| `#hdrStatusPipe` | `PIPELINE READY` | **Removed** — pipeline state no longer exists |
| `#hdrStatusTests` | `TESTS NOT RUN` | **Kept** |
| Logo badge text | `TRACEPOINT GEOMETRY ENGINE` | `TRACEPOINT VIEWER` |

### §2.2 — Status bar (replacing the "AI BACKEND: REMOVED" lie)

The v6.3.5 status bar (lines 1233–1243) is rewritten to reflect the API-connected architecture:

```html
<div class="status-bar">
  <div class="sb-item">
    <span class="sb-label">API:</span>
    <span class="sb-health-dot checking" id="sbHealthDot"></span>
    <span class="sb-value" id="sbApiStatus">CHECKING…</span>
  </div>
  <div class="sb-divider"></div>
  <div class="sb-item">
    <span class="sb-label">BACKEND:</span>
    <span class="sb-value" id="sbBackendVersion">—</span>
  </div>
  <div class="sb-divider"></div>
  <div class="sb-item">
    <span class="sb-label">MODE:</span>
    <span class="sb-value">API-CONNECTED · VIEWER + TOOLS</span>
  </div>
  <div class="sb-divider"></div>
  <div class="sb-item">
    <span class="sb-label">PDF.JS:</span>
    <span class="sb-value">3.11.174</span>
  </div>
  <div class="sb-divider"></div>
  <div class="sb-item">
    <span class="sb-label">TESTS:</span>
    <span class="sb-value" id="sbTestCount">— / —</span>
  </div>
</div>
```

The `sbHealthDot` and `sbApiStatus` elements are driven by the status-bar polling loop (§5).

### §2.3 — Sidebar

The sidebar strips the pipeline-specific sections and replaces them with API connection state:

**Removed:**

- "Pipeline State" section (v6.3.5 lines 1252–1258): `sbLastRun`, `sbPathCount`, `sbPolyCount`, `sbDetSF`, `sbConf`
- "12-Stage Pipeline" section (v6.3.5 lines 1261–1276): stage list `#sbPipeline` with 12 `<li>` entries
- "Karpathy Loop" section (v6.3.5 lines 1279–1286): build/test/test/test copy

**Added:**

```html
<aside class="sidebar">
  <div class="sb-section">
    <div class="sb-section-title">Connection</div>
    <div class="sb-stat"><span class="sb-stat-label">API</span><span class="sb-stat-value" id="sbApiState">checking…</span></div>
    <div class="sb-stat"><span class="sb-stat-label">Backend</span><span class="sb-stat-value" id="sbApiVersion">—</span></div>
    <div class="sb-stat"><span class="sb-stat-label">Job</span><span class="sb-stat-value" id="sbCurrentJob">none</span></div>
  </div>

  <div class="sb-section" style="border-bottom:none;">
    <div class="sb-section-title">Architecture</div>
    <div style="font-family:var(--mono);font-size:10.5px;color:var(--muted);line-height:1.7;">
      PDF rendering: client-side (pdf.js)<br>
      Scope + pipeline: backend API<br>
      Annotations: local until save
    </div>
  </div>
</aside>
```

### §2.4 — Tab bar (7 tabs, Pipeline removed)

v6.3.5 has 8 tabs (0–7). Pipeline (tab 5) is removed. The remaining 7 tabs renumber:

| New index | Tab label | Old index | Pane ID |
|---:|---|---:|---|
| 0 | NEW SESSION | 0 | `#pane0` |
| 1 | SCOPE | 1 | `#pane1` |
| 2 | PAGES | 2 | `#pane2` |
| 3 | VIEWER | 3 | `#pane3` |
| 4 | TAKEOFF | 4 | `#pane4` |
| 5 | TESTS | 6 (was) | `#pane5` (was `#pane6`) |
| 6 | ABOUT | 7 (was) | `#pane6` (was `#pane7`) |

```html
<div class="tabs">
  <div class="tab active" onclick="showTab(0)"><span class="tab-num">01</span>NEW SESSION</div>
  <div class="tab" onclick="showTab(1)"><span class="tab-num">02</span>SCOPE</div>
  <div class="tab" onclick="showTab(2)"><span class="tab-num">03</span>PAGES</div>
  <div class="tab" onclick="showTab(3)"><span class="tab-num">04</span>VIEWER</div>
  <div class="tab" onclick="showTab(4)"><span class="tab-num">05</span>TAKEOFF</div>
  <div class="tab" onclick="showTab(5)"><span class="tab-num">06</span>TESTS</div>
  <div class="tab" onclick="showTab(6)"><span class="tab-num">07</span>ABOUT</div>
</div>
```

### §2.5 — Tab pane changes

**Pane 0 — NEW SESSION:**
- "LOAD SYNTHETIC PLAN" button: **removed** (synthetic plans only fed the pipeline; S10 strips the function)
- Upload zone, trade cards, STEP 3 next-steps: **kept**
- `showTab()` calls in STEP 3 buttons: indices unchanged (1–4 are the same before and after pipeline removal)
- PDF upload card copy: updated from "Scope parses automatically" to "Upload bidset, backend processes scope"

**Pane 1 — SCOPE:** Kept. `renderScopeTab()` / `renderSystemCard()` / scope editing UI unchanged. Data source changes from `extractScope()` to API (but that's a JS change, not a markup change).

**Pane 2 — PAGES:** Kept. Thumbnail grid + filter chips unchanged. Classifier labels will come from API instead of `classifyPage()`.

**Pane 3 — VIEWER:**
- Toolbar: **kept** (all 10 tool buttons unchanged)
- Page picker / OSD container / Konva container / HUD: **kept**
- Viewer sidebar:
  - Current System select: **kept**
  - Pin / Edge / Polygon palette sections: **kept**
  - Active Tool section: **kept**
  - Scale (Manual Override) section: **kept** (calibrate tool still works; no pipeline to override but user can still set scale for measurements)
  - "This Page · Annotations" section: **kept**
  - **"Pipeline Inputs" section (v6.3.5 lines 1503–1510): REMOVED** — this section showed `manual scale` / `manual polygon` / `user zones` pipeline inputs and the "RUN WITH OVERRIDES" button. Pipeline is gone; these controls are meaningless.
  - "VIEW TAKEOFF" button (line 1509): **moved up** to the "This Page" section as a standalone navigation button

**Pane 4 — TAKEOFF:**
- Section header + takeoff grid: **kept**
- "STAGE-BY-STAGE BREAKDOWN" card (v6.3.5 lines 1530–1554): **removed** — this showed pipeline stage timing, which no longer exists
- "No pipeline run yet" message: **reworded** to "Upload a bidset and run scope to populate takeoff"
- `exportTakeoffToExcel()` button: **kept**

**Pane 5 — PIPELINE (v6.3.5 lines 1559–1601): ENTIRE PANE REMOVED.** This was the 12-stage card grid + execution log + geometry visualization canvas. All content strips.

**Pane 5 (new) — TESTS:** Renumbered from old pane 6. Content unchanged except:
- Copy references to "12 STAGES × N CASES" → updated to reflect post-strip test suite
- Karpathy discipline copy softened (pipeline no longer runs in browser)

**Pane 6 (new) — ABOUT:** Renumbered from old pane 7. Content updated:
- "6.1 additions" history section: **kept** (historical record)
- "The Surgery" section: **kept** (historical)
- "The 12 Stages" list: **kept** (reference — stages now run on backend)
- Add a new section at top: "Phase 2 architecture" explaining the API-connected viewer model

### §2.6 — Fullscreen exit button

`<button class="viewer-fullscreen-exit" ...>` at line 1212: **kept unchanged.**

---

## §3 — Top-level constants

The new file introduces three top-level constants immediately at the start of the first `<script>` block:

```javascript
const API_BASE = 'http://127.0.0.1:8000';
const HEALTH_POLL_INTERVAL_MS = 30000;
const HEALTH_PROBE_TIMEOUT_MS = 5000;
```

### §3.1 — `API_BASE`

- **Type:** `string`
- **Default:** `'http://127.0.0.1:8000'`
- **Used by:** Every `apiClient` function (D3). Single source of truth for the backend URL.
- **No env-var mechanism in E.2.1.** The file is a single HTML file with no build step; there is no `.env` or `import.meta.env`. The constant is a hardcoded string. If deployment needs change, E.3+ can add a `<meta>` tag override or a query-param override. For E.2, local dev on port 8000 is the only target.

### §3.2 — `HEALTH_POLL_INTERVAL_MS`

- **Type:** `number` (milliseconds)
- **Default:** `30000` (30 seconds)
- **Used by:** Status-bar polling loop (§5). After the initial health probe at boot, subsequent probes fire at this interval.
- **Why 30s:** Frequent enough to detect backend restart within a reasonable window; infrequent enough to produce negligible load on a local uvicorn.

### §3.3 — `HEALTH_PROBE_TIMEOUT_MS`

- **Type:** `number` (milliseconds)
- **Default:** `5000` (5 seconds)
- **Used by:** The `fetch()` call inside `apiClient.healthCheck()`. If the backend doesn't respond within 5s, the probe is treated as a failure and the status bar shows `UNREACHABLE`.
- **Why 5s:** Generous for a local /health endpoint (observed 1.1s boot + sub-1ms response in E.1 smoke test). The timeout is not for the backend being slow — it's for the backend not existing (e.g., user hasn't started uvicorn).

### §3.4 — Constants NOT carried forward

| v6.3.5 constant | Lines | Disposition |
|---|---|---|
| `STAGE_META` array (13 entries) | 2571–2606 | **Stripped** — pipeline stage metadata |
| `ROOFING_CONSTANTS` | near 5017 | **Stripped** — `wasteFactor` inlined as `const DEFAULT_WASTE_FACTOR = 0.10` in the takeoff section |
| `ROOF_VOCAB` | 5018–5143 | **Stripped** — vocabulary lives in backend's vault-ruled `roofing_vocabulary.py` |
| `ROOFING_SEED_ITEMS` | 4805–4990 | **Kept** — seed items are a rendering/UI concern; the merge logic stays (per audit item B7) |

---

## §4 — Script section ordering

The new file contains **two `<script>` blocks** (down from three in v6.3.5), organized into 9 ordered sections. The ordering is dependency-driven: each section may reference anything defined in a prior section but nothing defined in a later one.

### Script block 1 (was v6.3.5 Script 1 — TP pipeline; now: API client + utilities)

| Order | Section | Content | Approx lines | v6.3.5 origin |
|---:|---|---|---:|---|
| 1 | **API client** | `API_BASE`, `HEALTH_POLL_INTERVAL_MS`, `HEALTH_PROBE_TIMEOUT_MS` constants + `apiClient` object (D3 spec) | ~80 | **NEW** |
| 2 | **Tab + UI utilities** | `showTab()`, `escapeHTML()` / `esc()` | ~10 | v6.3.5 lines 2544–2547, 3508–3510 |

### Script block 2 (merged from v6.3.5 Scripts 2 + 3, minus stripped code)

| Order | Section | Content | Approx lines | v6.3.5 origin |
|---:|---|---|---:|---|
| 3 | **PDF loader** | `extractPlanSetFromPdf()` (rendering-only rewrite per S8), `getOrRenderPageCanvas()` | ~100 | v6.3.5 lines 2757–2956 (stripped walker, kept renderer) |
| 4 | **Test harness** | `assert()`, `approx()`, `withTestIsolation()`, `runTestBatch()`, `runUnitTests()`, `runAllTests()` | ~110 | v6.3.5 lines 3059–3064, 3400–3506 |
| 5 | **App state + file handling** | `App` object, `handleFileSelect()`, `handleDrop()`, `loadPdfFile()`, `refreshAfterPdfLoad()` | ~80 | v6.3.5 lines 3630–3720 (minus pipeline-specific calls) |
| 6 | **Viewer** | `Viewer` object, coordinate math, OSD + Konva init, page navigation, tool handlers (pan/calibrate/measure/line/polygon/rectangle/pin/excludeZone) | ~800 | v6.3.5 lines 3725–4560 (unchanged keeper region) |
| 7 | **Scope UI + seed data** | `ROOFING_SEED_ITEMS`, seed/merge helpers, stubs for `extractScope()` / `classifyPage()`, scope rendering (`renderScopeTab`, `renderSystemCard`, `rescanScope`, `renderPagesTab`), system editing functions | ~500 | v6.3.5 lines 4789–5555 (minus stripped B2/B3/B4/B5/B6) |
| 8 | **Takeoff + Excel export** | `DEFAULT_WASTE_FACTOR`, `buildTakeoffModel()`, `exportTakeoffToExcel()`, `renderTakeoffTab()`, `setTakeoffWaste()`, vertex snap helper | ~350 | v6.3.5 lines 6929–7311 |
| 9 | **Viewer extensions + hooks + tests + boot** | `showTab` hook (lazy rendering), viewer–scope wiring, TOOL_TESTS, API smoke tests (new), fullscreen handler, boot IIFE | ~500 | v6.3.5 lines 7313–8694 (minus SCOPE_TESTS/SCOPE_INTEGRATION_TESTS) |

### §4.1 — Dependency graph (section → depends on)

```
1. API client         → (none)
2. Tab + UI utils     → (none)
3. PDF loader         → 2 (escapeHTML)
4. Test harness       → 2 (escapeHTML)
5. App state          → 1 (apiClient), 2 (showTab), 3 (extractPlanSetFromPdf)
6. Viewer             → 3 (getOrRenderPageCanvas), 5 (App)
7. Scope UI           → 1 (apiClient), 2 (escapeHTML), 5 (App), 6 (Viewer)
8. Takeoff            → 5 (App), 6 (Viewer), 7 (scope data)
9. Extensions + boot  → 1 (apiClient), 2 (showTab), 4 (test harness), 5–8 (all)
```

### §4.2 — What moved between script blocks

v6.3.5 splits code across three `<script>` tags for historical reasons (Script 1 = pipeline, Script 2 = UI + tests, Script 3 = scope module). The new file consolidates into two:

- **Script 1** contains only the API client and UI utilities — the smallest, most independent pieces that everything else depends on.
- **Script 2** contains everything else in dependency order. The three-way split no longer has a reason to exist because the pipeline (Script 1's sole content in v6.3.5) is gone.

### §4.3 — Sections explicitly NOT present

| What | Why not |
|---|---|
| `TP` namespace | Stripped (S1) — pipeline runs on backend |
| `STAGE_META` + pipeline UI functions | Stripped (S2) — pipeline tab gone |
| `UNIT_TESTS` (pipeline tests) | Stripped (S3) — tests covered stripped code |
| `INTEGRATION_TESTS` (pipeline tests) | Stripped (S4) — same |
| `ROOF_VOCAB` | Stripped (S5) — vocabulary lives in backend |
| Text helpers | Stripped (S6) — only used by stripped extractScope |
| `extractScope` (real impl) | Stripped (S7a) — replaced by stub |
| `classifyPage` (real impl) | Stripped (S7b) — replaced by stub |
| `buildSyntheticPlan` / `loadSyntheticPlan` | Stripped (S10) — synthetic plans fed pipeline |
| `visualize()` | Stripped (S11) — geometry canvas visualizer |
| `SCOPE_TESTS` | Stripped (S12) — tests covered stripped code |
| `SCOPE_INTEGRATION_TESTS` | Stripped (S13) — same |
| `runPipeline()` / `runPipelineWithOverrides()` | Stripped (S9) — pipeline execution UI |
| `resetPipelineUI()` | Stripped (S9) — pipeline state reset |
| `_TP_run_original` shimming | Stripped (S9) — pipeline override layer |
| `renderStagesGrid()` / `setStageCardState()` / `formatStatVal()` / `setSidebarStage()` / `consoleLog()` | Stripped (S2) — pipeline UI functions |
| `renderSyntheticCanvasForViewer()` | Stripped — synthetic demo was pipeline-only |

---

## §5 — Status-bar dynamic polling spec

### §5.1 — Three states

The status bar's API indicator cycles through exactly three states:

| State | `sbHealthDot` class | `sbApiStatus` text | `sbApiState` text (sidebar) | `sbApiVersion` text (sidebar) |
|---|---|---|---|---|
| **CHECKING** | `checking` (amber) | `CHECKING…` | `checking…` | `—` |
| **CONNECTED** | `connected` (green) | `CONNECTED` | `connected` | version string from `/health` response (e.g., `0.3.0-E.1`) |
| **UNREACHABLE** | `unreachable` (red) | `UNREACHABLE` | `unreachable` | `—` |

### §5.2 — Three triggers

| Trigger | When | Action |
|---|---|---|
| **Boot** | DOMContentLoaded (or immediate if `document.readyState !== 'loading'`) | Probe `/health` immediately. Set state to CHECKING, then resolve to CONNECTED or UNREACHABLE. Start the interval timer. |
| **Interval** | Every `HEALTH_POLL_INTERVAL_MS` (30s) after boot | Probe `/health`. Transition state based on result. |
| **Manual** | User clicks a "retry" link in the UNREACHABLE state, or any API call returns a network error | Probe `/health` immediately (debounced — skip if a probe is already in flight). |

### §5.3 — State transition rules

```
CHECKING  → fetch resolves 200 + {"status":"ok"}  → CONNECTED
CHECKING  → fetch rejects / times out / non-200   → UNREACHABLE

CONNECTED → interval probe 200                    → CONNECTED  (no-op; update version if changed)
CONNECTED → interval probe fail                   → UNREACHABLE
CONNECTED → any apiClient call gets network error  → UNREACHABLE (+ immediate re-probe)

UNREACHABLE → interval probe 200                  → CONNECTED
UNREACHABLE → interval probe fail                 → UNREACHABLE (no-op)
UNREACHABLE → manual retry probe 200              → CONNECTED
UNREACHABLE → manual retry probe fail             → UNREACHABLE (no-op)
```

### §5.4 — CSS for the health dot

```css
.sb-health-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin: 0 6px;
  vertical-align: middle;
}
.sb-health-dot.connected { background: var(--green); box-shadow: 0 0 6px rgba(46,204,113,0.6); }
.sb-health-dot.checking { background: var(--amber); box-shadow: 0 0 6px rgba(243,156,18,0.4); }
.sb-health-dot.unreachable { background: var(--red); box-shadow: 0 0 6px rgba(231,76,60,0.4); }
```

### §5.5 — Implementation sketch

```javascript
let _healthState = 'checking';
let _healthProbeInFlight = false;
let _healthIntervalId = null;

async function probeHealth() {
  if (_healthProbeInFlight) return;
  _healthProbeInFlight = true;
  setHealthState('checking');
  try {
    const resp = await apiClient.healthCheck();
    setHealthState('connected');
    document.getElementById('sbApiVersion').textContent = resp.version || '—';
    document.getElementById('sbBackendVersion').textContent = resp.version || '—';
  } catch {
    setHealthState('unreachable');
  } finally {
    _healthProbeInFlight = false;
  }
}

function setHealthState(state) {
  _healthState = state;
  const dot = document.getElementById('sbHealthDot');
  const txt = document.getElementById('sbApiStatus');
  const side = document.getElementById('sbApiState');
  if (dot) { dot.className = 'sb-health-dot ' + state; }
  if (txt) { txt.textContent = state.toUpperCase(); }
  if (side) { side.textContent = state; }
}

function startHealthPolling() {
  probeHealth();
  _healthIntervalId = setInterval(probeHealth, HEALTH_POLL_INTERVAL_MS);
}
```

Called from the boot IIFE (§4, section 9).

### §5.6 — Degraded-mode behavior

When `_healthState === 'unreachable'`:

- The file still functions as a PDF **renderer** — users can load PDFs, view pages, draw annotations, and export takeoff Excel from manually entered data.
- Scope tab shows "Backend unreachable — scope data unavailable" instead of parsed scope.
- Pages tab shows page thumbnails but no classifier labels (page types default to `OTHER`).
- No error modals, no blocking dialogs. The status bar indicator is the primary communication surface.
- API calls from `apiClient` methods fail gracefully (return null or throw, caught by callers) — per D3 error handling spec.

---

## §6 — What v6.3.5 elements do NOT carry forward

This section is the definitive list of v6.3.5 content that is intentionally excluded from the new file. Items are grouped by type.

### §6.1 — Markup removed

| Element | v6.3.5 location | Reason |
|---|---|---|
| Pipeline tab bar entry | line 1298 (`showTab(5)` → PIPELINE) | Pipeline tab stripped |
| Pipeline tab pane `#pane5` | lines 1559–1601 | Pipeline tab stripped |
| Pipeline sidebar — "Pipeline State" | lines 1252–1258 | Pipeline state no longer tracked client-side |
| Pipeline sidebar — "12-Stage Pipeline" | lines 1261–1276 | Pipeline stages no longer rendered client-side |
| Pipeline sidebar — "Karpathy Loop" | lines 1279–1286 | Pipeline loop copy removed |
| Header stat `#hdrStatusPipe` — "PIPELINE READY" | line 1224 | No pipeline to be "ready" |
| Status bar — "ENGINE: TRACEPOINT 12-STAGE" | line 1234 | Engine is now the backend; status bar rewritten |
| Status bar — "AI BACKEND: REMOVED" | line 1236 | Lie — backend is now present |
| Status bar — "MODE: 100% OFFLINE · CLIENT-SIDE" | line 1238 | Lie — mode is now API-connected |
| "LOAD SYNTHETIC PLAN" button | line 1311 | Synthetic plans only fed the pipeline |
| Viewer sidebar — "Pipeline Inputs" section | lines 1503–1510 | Pipeline inputs meaningless without pipeline |
| "RUN WITH OVERRIDES" button | line 1508 | Pipeline execution removed |
| Takeoff "STAGE-BY-STAGE BREAKDOWN" table | lines 1530–1554 | Pipeline stage timing removed |
| Geometry visualization canvas + legend | lines 1586–1600 | Pipeline visualization removed |

### §6.2 — JavaScript removed (see strip plan for line-by-line detail)

| Function / block | Approx lines removed | Reason |
|---|---|---|
| `TP` namespace (entire Script 1) | ~832 | Pipeline runs on backend |
| `STAGE_META` + pipeline UI functions | ~73 | Pipeline tab gone |
| `UNIT_TESTS` (pipeline unit tests) | ~269 | Tests covered stripped code |
| `INTEGRATION_TESTS` (pipeline integration tests) | ~63 | Tests covered stripped code |
| `ROOF_VOCAB` | ~126 | Vocabulary canonical in backend |
| Text helpers (`collectPlanText`, `findMatches`, `splitBySystemLabels`) | ~43 | Only used by stripped extractScope |
| `extractScope()` (real implementation) | ~115 | Replaced by stub → API |
| `classifyPage()` (real implementation) | ~17 | Replaced by stub → API |
| PDF.js operator-list walker (extraction within `extractPlanSetFromPdf`) | ~107 | Extraction is backend's job; rendering stays |
| `buildSyntheticPlan()` + `loadSyntheticPlan()` | ~130 | Synthetic plans fed pipeline only |
| `visualize()` | ~93 | Geometry canvas visualizer for pipeline |
| `runPipeline()` + `resetPipelineUI()` | ~82 | Pipeline execution UI |
| `runPipelineWithOverrides()` + `_TP_run_original` shimming | ~77 | Pipeline override layer |
| `SCOPE_TESTS` | ~1,369 | Tests covered stripped code |
| `SCOPE_INTEGRATION_TESTS` | ~587 | Tests covered stripped code |
| `renderStagesGrid()`, `setStageCardState()`, `formatStatVal()`, `setSidebarStage()`, `consoleLog()` | ~73 | Pipeline UI functions |

### §6.3 — CSS removed

| Selector(s) | Lines removed | Reason |
|---|---|---|
| `.pipeline-stages`, `.pipeline-stages li`, `.ps-num` variants | ~29 | Pipeline sidebar |
| `@keyframes pulse` | ~4 | Pipeline animation |
| `.stages-grid`, `.stage-card` and children | ~63 | Pipeline tab cards |
| `.console` (pipeline log styling) | TBD by grep | Pipeline execution log |

### §6.4 — Copy / text changes (not removals, but edits)

| Element | v6.3.5 text | New text | Reason |
|---|---|---|---|
| `<title>` | `Huckleberry AI 6.0 — TracePoint Geometry Engine` | `Huckleberry AI — Phase 2` | Architecture change |
| Logo badge | `TRACEPOINT GEOMETRY ENGINE` | `TRACEPOINT VIEWER` | No longer an engine |
| Upload zone sub-copy | `vector + text` | `multi-page PDFs supported` | Browser no longer extracts vectors |
| File info box | `${paths} total vector paths · ${texts} text fragments` | `${pages} page(s) loaded` | Paths/texts no longer extracted client-side |
| Tests tab title | `TEST HARNESS · KARPATHY LOOP` | `TEST HARNESS` | Karpathy loop was pipeline-specific |
| Tests tab copy | References to "12 STAGES × N CASES" | Updated to reflect new test suite | Pipeline stages gone |
| About tab | History sections | Add "Phase 2 architecture" section | Document the API transition |
| Takeoff "no results" message | `No pipeline run yet` | `Upload a bidset and create a job to populate takeoff` | Pipeline no longer triggers takeoff |

---

**End of E.2.0 New File Design. E.2.1 creates the file according to this specification.**
