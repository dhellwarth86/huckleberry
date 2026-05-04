# E.2.0 API Client Spec — Frontend apiClient Wrapper

**Date:** 2026-04-30
**Branch:** `phase2-v0.3-E2-0-strip-plan`
**Companion docs:** `E2_0_STRIP_PLAN.md`, `E2_0_NEW_FILE_DESIGN.md`, `E2_0_TEST_FLOOR_PROPOSAL.md`
**Phase:** E.2.0 (read-only diagnostic — this document specifies the API client; E.2.2 implements it)
**Backend contract:** `E0_API_DESIGN.md` §5.2 (E.1 endpoints), shipped code in `api/main.py`, `api/routes/jobs.py`, `api/schemas/jobs.py`

---

## §1 — Wrapper structure

The API client is a plain JavaScript object named `apiClient`, declared in Script block 1 of the new file (§4, section 1 of D2). It uses browser-native `fetch()` — no axios, no external HTTP library, no npm dependency.

```javascript
const apiClient = {
  healthCheck:  async function() { ... },
  createJob:    async function(payload) { ... },
  getJob:       async function(jobId) { ... },
  // E.2.2 stubs (declared but not wired):
  listJobs:     async function(opts) { ... },
  getResults:   async function(jobId) { ... },
  dispatchJob:  async function(jobId) { ... },
};
```

### §1.1 — Design constraints

1. **No build step.** The client is inline JavaScript in the HTML file. No import/export, no module system, no bundler.
2. **No external deps.** `fetch()` is available in all target browsers (modern Chrome/Firefox/Edge). No polyfill needed.
3. **All methods are `async`.** Callers use `await apiClient.method()` or `.then()`.
4. **All methods throw on network errors.** Callers catch and handle (typically by triggering a health re-probe → UNREACHABLE state).
5. **All methods return parsed JSON on success.** The `apiCall` helper (§2) handles `response.json()`.
6. **Base URL from constant.** `API_BASE` (D2 §3.1) is the single source of truth — no URL construction scattered through callers.

---

## §2 — apiCall helper

All `apiClient` methods delegate to a single internal helper that encapsulates fetch + error handling + JSON parsing:

```javascript
async function apiCall(method, path, opts = {}) {
  const url = API_BASE + path;
  const fetchOpts = {
    method,
    headers: {},
  };

  if (opts.body !== undefined) {
    fetchOpts.headers['Content-Type'] = 'application/json';
    fetchOpts.body = JSON.stringify(opts.body);
  }

  if (opts.timeout) {
    const controller = new AbortController();
    fetchOpts.signal = controller.signal;
    setTimeout(() => controller.abort(), opts.timeout);
  }

  const resp = await fetch(url, fetchOpts);

  if (!resp.ok) {
    const errBody = await resp.json().catch(() => ({ detail: resp.statusText }));
    const err = new Error(errBody.detail || `HTTP ${resp.status}`);
    err.status = resp.status;
    err.body = errBody;
    throw err;
  }

  return resp.json();
}
```

### §2.1 — Key behaviors

| Behavior | Detail |
|---|---|
| **URL construction** | `API_BASE + path` — caller passes paths like `/health`, `/jobs`, `/jobs/${id}` |
| **Content-Type** | Set to `application/json` only when `opts.body` is present |
| **Timeout** | Uses `AbortController`. Only `healthCheck` uses a timeout (5s). Other methods have no timeout in E.2 (backend operations are fast for the E.1 surface). |
| **Error shape** | On non-2xx, reads `resp.json()` to extract `{"detail": "..."}` (FastAPI's standard error shape). Creates an `Error` with `.status` and `.body` properties. |
| **Network failure** | `fetch()` itself throws `TypeError` on DNS/connection failure. This propagates to the caller unmodified — the status-bar polling loop catches it. |
| **No retry logic** | E.2 does not retry. The status-bar polling loop handles reconnection; individual API calls report failure to the UI. Retry logic is an E.3+ concern. |
| **No auth headers** | E.1 ships with no auth. When auth arrives, a single line in `apiCall` adds the header. |

---

## §3 — Real implementations (E.1 endpoints)

### §3.1 — `apiClient.healthCheck()`

```javascript
healthCheck: async function() {
  return apiCall('GET', '/health', { timeout: HEALTH_PROBE_TIMEOUT_MS });
}
```

**Backend endpoint:** `GET /health` → `{"status": "ok", "version": "0.3.0-E.1"}`

**Return shape:**

```javascript
{ status: "ok", version: "0.3.0-E.1" }
```

**Usage:** Called by the status-bar polling loop (D2 §5). The `version` field is displayed in the sidebar and status bar.

**Error behavior:** Throws on network failure or timeout. The polling loop catches and transitions to UNREACHABLE state.

---

### §3.2 — `apiClient.createJob(payload)`

```javascript
createJob: async function(payload) {
  return apiCall('POST', '/jobs', { body: payload });
}
```

**Backend endpoint:** `POST /jobs` → 201 + `JobResponse` JSON

**Payload shape (matches `JobCreateRequest` Pydantic schema):**

```javascript
{
  name: "B2607 AEA Silverleaf",              // required, non-empty, max 200 chars
  pdf_path: "C:\\path\\to\\bidset.pdf",       // required, non-empty
  gc: "Accelerated Construction Services",    // optional
  location_city: "St Augustine",              // optional
  location_state: "FL",                       // optional, max 2 chars
  trade_scope: "roofing,glazing",             // optional, default "roofing"
  bid_due_date: "2026-05-15",                 // optional, ISO 8601 date
  notes: null,                                // optional
  status: "draft"                             // optional, default "draft"
}
```

**Return shape (matches `JobResponse` Pydantic schema):**

```javascript
{
  id: "98bd2e75-0458-41f8-865b-a4b8304c163b",
  name: "B2607 AEA Silverleaf",
  gc: "Accelerated Construction Services",
  location_city: "St Augustine",
  location_state: "FL",
  trade_scope: "roofing,glazing",
  bid_due_date: null,
  notes: null,
  status: "draft",
  created_at: "2026-04-30T18:04:14.069582+00:00",
  updated_at: "2026-04-30T18:04:14.069582+00:00",
  pdf_path: "C:\\path\\to\\bidset.pdf",
  pdf_sha1: "76dc89072dae77c1b476b60da85870f3d799cd31",
  dispatch_complete: false
}
```

**Usage in E.2.2:** Called from `loadPdfFile()` after the user uploads a PDF. The flow becomes: user drops PDF → `extractPlanSetFromPdf()` renders pages → `apiClient.createJob()` creates the backend job → store `jobId` in `App.currentJobId` → scope tab can fetch results later.

**Error cases:**

| Error | HTTP status | `err.body.detail` | UI response |
|---|---|---|---|
| Pydantic validation (missing name) | 422 | FastAPI validation envelope | Show error in upload card |
| `pdf_path` not found | 400 | `"pdf_path not found"` | Show error in upload card |
| Network failure | (thrown TypeError) | — | Trigger health re-probe; show error in upload card |

---

### §3.3 — `apiClient.getJob(jobId)`

```javascript
getJob: async function(jobId) {
  return apiCall('GET', '/jobs/' + encodeURIComponent(jobId));
}
```

**Backend endpoint:** `GET /jobs/{job_id}` → 200 + `JobResponse` JSON

**Return shape:** Same `JobResponse` shape as `createJob` (§3.2).

**Usage in E.2.2:** Called when navigating to a job by ID (future job list integration), or to refresh job state after dispatch.

**Error cases:**

| Error | HTTP status | `err.body.detail` | UI response |
|---|---|---|---|
| Job not found | 404 | `"Job not found"` | Show "Job not found" message; do not crash |
| Network failure | (thrown TypeError) | — | Trigger health re-probe |

**Security note:** `encodeURIComponent(jobId)` prevents path-traversal injection in the URL. The backend's `get_job(job_id)` does a parameterized SQL query, so SQL injection is already mitigated server-side, but the client should not construct unsanitized URLs.

---

## §4 — Stub slots (E.2 forward-compat — declared, not implemented)

These methods are declared in the `apiClient` object so that D3 establishes the full client surface. They throw a clear error in E.2.1; E.2.2 wires them to real endpoints as those endpoints ship.

### §4.1 — `apiClient.listJobs(opts)`

```javascript
listJobs: async function(opts) {
  throw new Error('listJobs not implemented — waiting for GET /jobs endpoint (E.2)');
}
```

**Future endpoint:** `GET /jobs` (E.2, per API design §5.3)
**Future opts shape:** `{ sort_by, sort_order, filter_gc, filter_status, filter_state }`
**Future return shape:** `JobResponse[]`

### §4.2 — `apiClient.getResults(jobId)`

```javascript
getResults: async function(jobId) {
  throw new Error('getResults not implemented — waiting for GET /jobs/{id}/results endpoint (E.2)');
}
```

**Future endpoint:** `GET /jobs/{job_id}/results` (E.2, per API design §5.3)
**Future return shape:**

```javascript
{
  job_id: "...",
  dispatch_results: { "0": { page_idx: 0, page_type: "cover", ... }, ... },
  trade_outputs: { "0": { roofing: { fields: {...}, ... }, ... }, ... }
}
```

This is the primary data source for the Scope tab and Pages tab after E.2.2. `dispatch_results` provides page classification (`page_type`); `trade_outputs` provides per-page roofing fields.

### §4.3 — `apiClient.dispatchJob(jobId)`

```javascript
dispatchJob: async function(jobId) {
  throw new Error('dispatchJob not implemented — waiting for POST /jobs/{id}/dispatch endpoint (E.2)');
}
```

**Future endpoint:** `POST /jobs/{job_id}/dispatch` (E.2, per API design §5.3)
**Open design question:** Sync vs. async. Vine Street took 1,195s in D.2 — a sync HTTP request is unworkable. The E.2 march orders must decide on progress reporting (SSE, polling, or background task).

---

## §5 — Error handling matrix

### §5.1 — Error classification

All errors from `apiCall` fall into exactly three categories:

| Category | Detection | Example | Client action |
|---|---|---|---|
| **Network error** | `fetch()` throws `TypeError` | Backend not running, DNS failure, CORS block | Trigger health re-probe → UNREACHABLE. Show inline error message to user. |
| **HTTP error (4xx)** | `resp.ok === false`, `err.status` is 400/404/422 | Bad input, missing job, validation failure | Show `err.body.detail` to user in the relevant UI area (upload card, scope tab, etc.). Do NOT trigger health re-probe (backend is reachable, the request was just invalid). |
| **HTTP error (5xx)** | `resp.ok === false`, `err.status` is 500+ | SQLite write failure, unexpected server crash | Show generic "Server error — try again" to user. Trigger health re-probe (5xx may indicate backend instability). |

### §5.2 — Caller-side patterns

Every call site follows this pattern:

```javascript
try {
  const result = await apiClient.someMethod(args);
  // use result
} catch (err) {
  if (err.status) {
    // HTTP error — show err.body.detail in appropriate UI
    showErrorInUI(err.body?.detail || 'Request failed');
    if (err.status >= 500) probeHealth();
  } else {
    // Network error — trigger health state change
    probeHealth();
    showErrorInUI('Backend unreachable');
  }
}
```

### §5.3 — No global error handler

Errors are handled at the call site, not via a global `window.onerror` or `unhandledrejection` handler. Rationale: each call site knows what UI surface to update (upload card error, scope tab error, status bar). A global handler would need to route errors back to UI surfaces — unnecessary indirection for 3 real methods.

### §5.4 — No retry logic

E.2 does not retry failed API calls. If a call fails:

1. Network errors trigger a health re-probe which sets the status bar to UNREACHABLE.
2. The interval polling (every 30s) will eventually detect when the backend comes back.
3. The user can retry their action manually.

Automatic retry with backoff is an E.3+ enhancement if needed. For local dev (E.2's only target), the backend is either running or it isn't — retry rarely helps.

---

## §6 — Status-bar integration

### §6.1 — Health polling lifecycle

The `apiClient.healthCheck()` method is the bridge between the API client and the status-bar state machine (D2 §5). The integration points are:

1. **Boot:** The boot IIFE calls `startHealthPolling()` which calls `probeHealth()` which calls `apiClient.healthCheck()`.
2. **Interval:** `setInterval(probeHealth, HEALTH_POLL_INTERVAL_MS)` fires every 30s.
3. **API failure cascade:** When any `apiClient` method throws a network error, the caller calls `probeHealth()` which calls `apiClient.healthCheck()`.

### §6.2 — Version display

When `healthCheck()` succeeds, the response's `version` field (e.g., `"0.3.0-E.1"`) is displayed in:

- Status bar: `#sbBackendVersion`
- Sidebar: `#sbApiVersion`

If the version changes between probes (e.g., backend was restarted with a newer version), the display updates automatically. No special handling needed — the polling loop overwrites the text content on every successful probe.

### §6.3 — Job context in sidebar

When `createJob()` or `getJob()` succeeds, the sidebar `#sbCurrentJob` element is updated:

```javascript
document.getElementById('sbCurrentJob').textContent = result.name + ' (' + result.id.slice(0, 8) + '…)';
```

This gives the user a persistent indicator of which job is loaded. Cleared on page reload (no localStorage persistence in E.2).

### §6.4 — No loading spinners in E.2

E.2 does not add loading spinners or progress indicators to API calls. The E.1 surface is fast enough (sub-100ms for both endpoints) that spinners would flash and disappear. If E.2's `dispatchJob()` endpoint involves long-running work, the dispatch progress UX is designed in E.2's march orders — not pre-built here.

---

**End of E.2.0 API Client Spec. E.2.2 implements the client against this specification.**
