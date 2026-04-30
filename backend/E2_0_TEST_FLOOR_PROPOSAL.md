# E.2.0 Test Floor Proposal — Frontend Test Re-Baseline

**Date:** 2026-04-30
**Branch:** `phase2-v0.3-E2-0-strip-plan`
**Companion docs:** `E2_0_STRIP_PLAN.md`, `E2_0_NEW_FILE_DESIGN.md`, `E2_0_API_CLIENT_SPEC.md`
**Phase:** E.2.0 (read-only diagnostic — this document proposes the new test floor; E.2.1 executes it)
**Current sacred test floors:** Backend 222/19/0 · Frontend 138/138

---

## §1 — What retires

These test collections are deleted because they exercise code that the strip plan (D1) removes. Every test listed below tests functions that will not exist in the new file.

### §1.1 — UNIT_TESTS (pipeline unit tests)

**v6.3.5 location:** lines 3066–3334
**Count:** 88 tests
**What they cover:** TP pipeline stages 1–12, domain-type factories (`makePath`, `makeZone`, `makeText`, `makeContext`), helpers (`pathLengthInches`, `segIntersects`, `pointInPolygon`, `polygonArea`, `convexHull`, `shoelaceArea`).
**Why retiring:** The `TP` namespace (S1) is stripped. These 88 tests cover code that no longer exists in the frontend. The Python backend's 222-test suite covers the same pipeline from the canonical implementation.

### §1.2 — INTEGRATION_TESTS (pipeline integration tests)

**v6.3.5 location:** lines 3336–3398
**Count:** 5 tests
**What they cover:** Full `TP.run` pipeline against synthetic plans — the "build a 5,000 sqft building, run all 12 stages, verify detected area within tolerance" tests.
**Why retiring:** `TP.run` is stripped. Synthetic plan generation (`buildSyntheticPlan`) is stripped (S10). End-to-end pipeline testing lives in the backend pytest suite.

### §1.3 — SCOPE_TESTS

**v6.3.5 location:** lines 5559–6927
**Count:** 30 tests (estimated from the array spanning ~1,369 lines)
**What they cover:** `extractScope()` behavior, `ROOF_VOCAB` regex matching, `classifyPage()` accuracy, `makeScopeSystem()` construction, scope UI rendering with mocked data, takeoff model building against scope output.
**Why retiring:** `extractScope()` (S7a), `ROOF_VOCAB` (S5), `classifyPage()` (S7b) are all stripped. The scope inference now runs on the backend; the vault-ruled `roofing_vocabulary.py` is the canonical vocabulary source.

**Partial salvage consideration:** ~4 of the SCOPE_TESTS exercise `buildTakeoffModel()` which stays. These specific tests are candidates for porting to the new test suite (see §3.3). However, they require `extractScope()` output as input fixtures — they cannot survive unmodified. The ported versions would use hardcoded scope fixtures instead of calling `extractScope()`.

### §1.4 — SCOPE_INTEGRATION_TESTS

**v6.3.5 location:** lines 8051–8637
**Count:** 15 tests (estimated from ~587 lines)
**What they cover:** End-to-end scope: `buildSyntheticPlan()` → `extractScope()` → verify scope systems → verify annotations → verify takeoff model.
**Why retiring:** Both `buildSyntheticPlan()` and `extractScope()` are stripped. The end-to-end scope path now runs through the backend API.

### §1.5 — TOOL_TESTS that depend on stripped code

From the 15 TOOL_TESTS at lines 4565–4723, these 4 tests depend on stripped functions:

| Test name | Line | Dependency | Disposition |
|---|---|---|---|
| `tool · end-to-end: manual polygon + manual scale → correct sqft` | 4669 | `buildSyntheticPlan()`, `TP.run()` | **Retire** — pipeline e2e |
| `tool · end-to-end: L-shape polygon → correct sqft` | 4697 | `buildSyntheticPlan()`, `TP.run()` | **Retire** — pipeline e2e |
| `tool · buildOverridesFromViewer: empty state` | 4639 | `buildOverridesFromViewer()` | **Retire** — function stripped with pipeline |
| `tool · buildOverridesFromViewer: mixed annotations` | 4652 | `buildOverridesFromViewer()` | **Retire** — function stripped with pipeline |

### §1.6 — Retirement summary

| Collection | Tests retiring | Reason |
|---|---|---|
| UNIT_TESTS (pipeline) | 88 | TP namespace stripped |
| INTEGRATION_TESTS (pipeline) | 5 | TP.run stripped |
| SCOPE_TESTS | 30 | extractScope / ROOF_VOCAB / classifyPage stripped |
| SCOPE_INTEGRATION_TESTS | 15 | Synthetic plan + extractScope stripped |
| TOOL_TESTS (pipeline-dependent) | 4 | buildSyntheticPlan / TP.run / buildOverridesFromViewer stripped |
| **Total retiring** | **142** | |

Note: the current floor is 138. The count exceeds 138 because `SCOPE_TESTS` and `SCOPE_INTEGRATION_TESTS` are appended to `UNIT_TESTS` and `INTEGRATION_TESTS` via `Array.prototype.push.apply` at lines 7322 and 8637. The 138 count from `npm test` reflects all 5 arrays merged into 2 batches. The ~142 retirement count is an estimate based on line-span analysis; the exact count will be confirmed during E.2.1 execution.

---

## §2 — What survives

### §2.1 — TOOL_TESTS (11 of 15 survive)

These 11 TOOL_TESTS exercise annotation tools, coordinate math, and measurement helpers that are keeper code (F2, F3 per audit):

| Test name | Line | Tests | Depends on stripped code? |
|---|---|---|---|
| `tool · parseFeetInches: "100" → 100 ft` | 4566 | `parseFeetInches()` | No |
| `tool · parseFeetInches: "100'" → 100 ft` | 4569 | `parseFeetInches()` | No |
| `tool · parseFeetInches: "100'-6"" → 100.5 ft` | 4572 | `parseFeetInches()` | No |
| `tool · parseFeetInches: "50ft 3in" → 50.25 ft` | 4575 | `parseFeetInches()` | No |
| `tool · parseFeetInches: invalid → null` | 4578 | `parseFeetInches()` | No |
| `tool · polygonAreaPt: 100'×50' rectangle` | 4581 | `polygonAreaPt()` | No — this function is in the Viewer/tools section, not in `TP` |
| `tool · polygonAreaPt: L-shape → 4,100 sqft` | 4594 | `polygonAreaPt()` | No |
| `tool · polygonPerimeterPt: 100'×50' rect` | 4610 | `polygonPerimeterPt()` | No |
| `tool · bboxOfPoints: simple square` | 4618 | `bboxOfPoints()` | No |
| `tool · calibrate math` | 4623 | Pure arithmetic | No |
| `tool · measure math: 3-4-5 triangle` | 4632 | Pure arithmetic | No |

**Important distinction:** `polygonAreaPt()` (used by TOOL_TESTS) is a different function from `polygonArea()` (in the `TP` namespace). `polygonAreaPt()` is a standalone helper in the Viewer/tools section that computes area from annotation point arrays. It stays. The `TP.polygonArea()` (shoelace formula on path segments) strips with the TP namespace — but `polygonAreaPt()` likely inlines the same shoelace math and does not reference `TP`. If it does reference `TP.polygonArea`, E.2.1 inlines the ~8-line shoelace formula directly.

### §2.2 — Test harness mechanics

These functions survive unchanged:

| Function | Line | Purpose |
|---|---|---|
| `assert(cond, msg)` | 3059 | Boolean assertion with message |
| `approx(actual, expected, tol, msg)` | 3061 | Numeric approximation assertion |
| `withTestIsolation(fn)` | 3416 | Snapshot/restore App + Viewer globals around tests |
| `runTestBatch(tests, listId, isIntegration)` | 3450 | Renders test items in DOM, runs sequentially, updates summary |
| `runUnitTests()` | 3400 | Runs unit test batch |
| `runAllTests()` | 3404 | Runs unit + integration batches |

### §2.3 — Test wiring

The `showTab` hook at line 7314 survives (lazy rendering on tab switch). The `Array.prototype.push.apply(UNIT_TESTS, SCOPE_TESTS)` at line 7322 is deleted (SCOPE_TESTS no longer exist). The `Array.prototype.push.apply(INTEGRATION_TESTS, SCOPE_INTEGRATION_TESTS)` at line 8637 is deleted (SCOPE_INTEGRATION_TESTS no longer exist).

---

## §3 — What's new

### §3.1 — API client smoke tests (NEW — added in E.2.2)

New tests exercising the `apiClient` wrapper against the live backend:

| Test name | What it tests | Category |
|---|---|---|
| `api · healthCheck returns ok + version` | `apiClient.healthCheck()` → `{ status: "ok", version: "0.3.0-E.1" }` | INTEGRATION |
| `api · createJob returns 201 + JobResponse shape` | `apiClient.createJob({...})` → has `id`, `name`, `pdf_sha1`, `status: "draft"` | INTEGRATION |
| `api · getJob returns 200 + matching job` | `apiClient.getJob(id)` → `id` matches, `name` matches | INTEGRATION |
| `api · getJob 404 for unknown id` | `apiClient.getJob('nonexistent')` → throws with `status: 404` | INTEGRATION |
| `api · createJob 422 for missing name` | `apiClient.createJob({pdf_path: '...'})` → throws with `status: 422` | INTEGRATION |

**Count:** 5 new tests

**Important:** These tests require a running backend (`uvicorn` on port 8000). They are **integration tests**, not unit tests. The test harness must handle the case where the backend is not running — these tests should skip gracefully (mark as SKIP, not FAIL) when `apiClient.healthCheck()` fails.

**Implementation pattern:**

```javascript
const API_SMOKE_TESTS = [
  { name: "api · healthCheck returns ok + version", fn: async () => {
    const r = await apiClient.healthCheck();
    assert(r.status === 'ok', 'status should be ok');
    assert(typeof r.version === 'string' && r.version.length > 0, 'version should be non-empty string');
  }},
  // ... etc
];
```

### §3.2 — Status-bar state tests (NEW — added in E.2.1)

New tests verifying the status-bar state machine:

| Test name | What it tests | Category |
|---|---|---|
| `statusbar · initial state is checking` | After boot, `_healthState === 'checking'` | UNIT |
| `statusbar · setHealthState updates DOM` | `setHealthState('connected')` → dot has class `connected`, text shows `CONNECTED` | UNIT |
| `statusbar · setHealthState cycles all three states` | Verify all three states produce correct class + text | UNIT |

**Count:** 3 new tests

### §3.3 — Takeoff model tests (PORTED from SCOPE_TESTS)

A small number of SCOPE_TESTS exercise `buildTakeoffModel()` which is a keeper function. These are ported with hardcoded scope fixtures replacing the `extractScope()` dependency:

| Test name | What it tests | Category |
|---|---|---|
| `takeoff · buildTakeoffModel with empty annotations` | Takeoff rows generated for seed items with zero measurements | UNIT |
| `takeoff · buildTakeoffModel with areas produces correct SF` | Building areas → membrane/insulation SF rows computed correctly | UNIT |
| `takeoff · waste factor defaults to 10%` | `DEFAULT_WASTE_FACTOR` (inlined 0.10) applied to rows | UNIT |
| `takeoff · waste override per seed item` | `system.takeoffOverrides[seedId].wastePct` overrides default | UNIT |

**Count:** 4 new tests (ported + rewritten from SCOPE_TESTS)

### §3.4 — Stub correctness tests (NEW — added in E.2.1)

New tests verifying the stubs behave correctly:

| Test name | What it tests | Category |
|---|---|---|
| `stub · extractScope returns empty shape` | Stub `extractScope()` returns `{ systems: [], rawText: '', lastScanAt: <number> }` | UNIT |
| `stub · classifyPage returns OTHER` | Stub `classifyPage()` returns `{ kind: 'OTHER', scores: {}, confidence: 'low' }` | UNIT |

**Count:** 2 new tests

---

## §4 — Proposed floor count

### §4.1 — Arithmetic

| Category | Count |
|---:|---:|
| **Surviving TOOL_TESTS** | 11 |
| **New API smoke tests** | 5 |
| **New status-bar tests** | 3 |
| **Ported takeoff tests** | 4 |
| **New stub tests** | 2 |
| **Total proposed** | **25** |

### §4.2 — Sacred floor declaration

**Proposed frontend sacred test floor:** `25 / 25` (all pass, zero fail)

This is a dramatic drop from the current 138/138 floor. That is expected and correct: the 138 floor was dominated by pipeline and scope tests (88 + 5 + 30 + 15 = 138 retiring) that tested code that is leaving the frontend entirely.

The 25-test floor covers:

1. **Annotation tools work correctly** (11 surviving TOOL_TESTS) — the highest-risk surface after strip, per D1 Risk 1
2. **API client connects to backend** (5 API smoke tests) — the new architectural seam
3. **Status bar reflects connection state** (3 tests) — the primary user-facing signal
4. **Takeoff model computes correctly with backend-provided data** (4 tests) — ensures takeoff export still works
5. **Stubs behave as specified** (2 tests) — guards against E.2.1 stub bugs breaking the UI

### §4.3 — Backend floor unchanged

**Backend sacred test floor remains:** `222 / 19 / 0` (222 pass, 19 skip, 0 fail)

E.2.0 makes no backend code changes. The backend floor is unaffected.

### §4.4 — Floor progression across E.2 sub-phases

| Phase | Frontend floor | Notes |
|---|---|---|
| **Current (v6.3.5)** | 138 / 138 | Pipeline + scope + tools |
| **E.2.1 (strip)** | 20 / 20 | Tools (11) + status-bar (3) + takeoff (4) + stubs (2). API tests not yet wired. |
| **E.2.2 (connect)** | 25 / 25 | API smoke tests (5) added once client is wired |
| **E.2.debug** | 25 / 25 | All pass; manual verification of viewer + annotations |
| **E.2.hard-gate** | 25 / 25 | Gate pass |

---

## §5 — Harness changes

### §5.1 — Test array restructure

v6.3.5 uses 5 separate arrays that get merged at runtime:

```
UNIT_TESTS (88) ← push(TOOL_TESTS (15)) ← push(SCOPE_TESTS (30))
INTEGRATION_TESTS (5) ← push(SCOPE_INTEGRATION_TESTS (15))
Total: 138 run as 2 batches
```

Post-strip, the arrays simplify to:

```
UNIT_TESTS = [...TOOL_TESTS_SURVIVING (11), ...STATUSBAR_TESTS (3), ...TAKEOFF_TESTS (4), ...STUB_TESTS (2)]
INTEGRATION_TESTS = [...API_SMOKE_TESTS (5)]
Total: 25 run as 2 batches
```

The `TOOL_TESTS` constant remains as a declaration. The surviving 11 tests are defined in-place. `UNIT_TESTS` starts as the combined array of all non-API tests. `INTEGRATION_TESTS` contains only the API smoke tests.

### §5.2 — API test skip logic

API smoke tests must handle the backend-not-running case:

```javascript
const API_SMOKE_TESTS = [
  { name: "api · healthCheck returns ok + version", fn: async () => {
    try {
      const r = await apiClient.healthCheck();
      assert(r.status === 'ok', 'status should be ok');
    } catch (e) {
      if (!e.status) throw new Error('SKIP: backend not reachable');
      throw e;
    }
  }},
  // ...
];
```

The test harness's `runTestBatch` needs a minor edit: if an error message starts with `SKIP:`, render the test as `SKIP` (amber) instead of `FAIL` (red). This is the lightest possible skip mechanism — no new assertion type, no new test state, just a message convention.

### §5.3 — `run_tests.js` update

The jsdom-based test runner (`frontend/run_tests.js`) currently runs against `Huckleberry_AI_6.3.5_Scope.html` via `package.json`:

```json
"test": "node run_tests.js Huckleberry_AI_6.3.5_Scope.html"
```

E.2.1 updates this to:

```json
"test": "node run_tests.js src/Huckleberry_AI_phase2.v1.0.0.html"
```

The runner itself needs no structural changes — it already hoists `UNIT_TESTS` and `INTEGRATION_TESTS` via `window.__TESTS__`. The new file defines the same two global arrays.

**jsdom limitation:** The API smoke tests will always SKIP in the jsdom environment because `fetch()` is not available in jsdom by default (no network I/O). This is correct behavior: `npm test` runs the 20 unit tests and reports 5 skips for the API tests. The API tests are exercised via browser with a live backend.

### §5.4 — `npm test` expected output post-E.2.1

```
UNIT_TESTS: 20 | INTEGRATION_TESTS: 0 (5 SKIP) | total: 20 pass, 0 fail, 5 skip
```

Post-E.2.2 with live backend:

```
UNIT_TESTS: 20 | INTEGRATION_TESTS: 5 | total: 25 pass, 0 fail, 0 skip
```

---

## §6 — What the floor doesn't cover

The proposed 25-test floor is intentionally narrow. It covers the highest-risk post-strip surfaces but does not attempt full coverage of every retained function. The following are explicitly out of scope for the E.2 test floor:

### §6.1 — Manual verification (E.2.debug scope)

| Surface | Why not automated | E.2.debug verification |
|---|---|---|
| PDF rendering (page loads, thumbnails appear) | Requires real PDF file + browser canvas API | Load Silverleaf PDF in browser, visually confirm pages render |
| Viewer pan/zoom | Requires OSD interaction + visual confirmation | Open viewer, pan/zoom, confirm no regression |
| Annotation placement accuracy | Requires click position → PDF point verification | Drop a pin, draw a polygon, verify coordinates are correct |
| Konva overlay alignment | Requires visual overlay-on-OSD check | Draw annotation, confirm it aligns with the page content underneath |
| Excel export | Requires file download + content verification | Build takeoff with manual data, export, open in Excel, verify |
| Tab switching | DOM-class toggle; trivial but numerous | Click all 7 tabs, confirm correct pane shows |
| Scope tab rendering from stub | Stub returns empty; visual check that "no scope" message appears | Load PDF, click Scope tab, confirm empty message |

### §6.2 — Not covered by frontend tests (covered by backend tests)

| Surface | Backend coverage |
|---|---|
| Pipeline stages 1–12 | Backend 222-test suite |
| ROOF_VOCAB accuracy | Backend vault-ruled `roofing_vocabulary.py` + tests |
| Page classification accuracy | Backend `dispatch_gate.py` tests |
| Scope extraction correctness | Backend `roofing_module.py` + `scope_scanner` tests |
| Job persistence (create/read/update) | Backend `test_api_jobs.py` (6 tests) |
| PDF path/text extraction | Backend `PDFEngine` + pdfplumber tests |

### §6.3 — Deferred to E.3+ test expansion

| Surface | When | Why deferred |
|---|---|---|
| Annotation round-trip to backend | E.3 (annotation save endpoint) | Endpoint doesn't exist yet |
| Job list rendering | E.2+ (when `GET /jobs` ships) | Endpoint doesn't exist yet |
| Dispatch progress UI | E.2+ (when `POST /jobs/{id}/dispatch` ships) | Endpoint doesn't exist yet |
| Multi-system scope rendering from API data | E.2.2 (when `getResults` wired) | Needs real backend dispatch data |
| Cross-browser compatibility | Post-E.3 | Testing infra not set up |

### §6.4 — Honest assessment

The 25-test floor is a **transitional floor**. It is deliberately lower than the 138-test floor it replaces because:

1. ~80% of the retiring tests covered pipeline code that is definitively gone from the frontend. Those tests don't need replacement — their coverage now lives in the backend's 222-test suite.
2. The new tests cover the new architecture's seams (API client, status bar, stubs) and the highest-risk surviving code (annotation tools, takeoff model).
3. The floor will grow as E.2.2 wires API endpoints and E.3 adds annotation persistence — each new API integration adds corresponding smoke tests.

The floor is honest about what it covers and what it doesn't. The gaps in §6.1 are addressed by E.2.debug's manual verification protocol. The gaps in §6.2 are addressed by the backend test suite. The gaps in §6.3 are addressed when those features ship.

---

**End of E.2.0 Test Floor Proposal. E.2.1 executes the test re-baseline according to this specification.**
