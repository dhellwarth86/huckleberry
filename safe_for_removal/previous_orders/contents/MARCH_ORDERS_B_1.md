# Phase B.1 — March Orders

**Target:** Port TracePoint Stages 2–5 (the composable filter gate pipeline) verbatim into the Huckleberry backend. This is the smallest sub-phase of Phase B and the cleanest test of whether the Phase B port shape transfers from v0.2's success.

**Authored:** 2026-04-27
**Authority:** Daniel (POC owner)
**Discipline:** Karpathy procedure (read first → failing tests first → minimum implementation → verify 100% → ship). Same as `MARCH_ORDERS_v0_2.md`. The B-16/17/18 anti-pattern is the named failure mode this discipline prevents.
**Predecessor:** v0.2 (commit `441896a`). v0.2.1 has NOT shipped and is intentionally NOT a prerequisite for B.1 — schema migration / D-4 / D-5 are independent of filter pipeline work.
**Source authority:** `tracepoint_port/TracePoint/core/filter_pipeline.py` (230 lines) and `tracepoint_port/TracePoint/tests/test_filter_pipeline.py` (270 lines). Verified in `backend/TRACEPOINT_DISCOVERY.md` §3.7 and §8.1.

---

## 0. Context — Why This Is a Verbatim Port, Not a Build

TracePoint paper §2.2 describes Stages 2–5 as the **composable filter gate pipeline**: four pure-function gates (zone mask, weight filter, length filter, dash filter) plus a fifth opt-in color filter, plus the two pipeline runners (`run_heavy_pipeline`, `run_allpaths_pipeline`).

Each gate is a pure function: paths in → paths out + a `GateLog` of what was removed. Adding a new gate requires one function definition and one line in the pipeline runner. The composability was validated empirically on TracePoint's 10 test plans and on its 15 bid set sweep. Calibrated decisions live inside the gates: the 1.0pt heavy-line cutoff, the 0.5-inch length floor, the dash-pattern detection. **These thresholds are canon. Do not retune.** The v0.2 paper §8.5 ("calibrate from data, not intuition") is the named lesson; B.1 inherits it.

If a behavior in TracePoint surprises you, the answer is "TracePoint is canon, port it." Calibration thresholds, gate orderings, dataclass fields, regex patterns — port verbatim. Do not optimize, refactor, generalize, or rename for "clarity."

---

## 1. TracePoint Files Read in Full (Pre-Condition Met)

Before any code touches the backend, the following files are read end-to-end:

**Port targets:**
- `tracepoint_port/TracePoint/core/filter_pipeline.py` (230 lines)
- `tracepoint_port/TracePoint/tests/test_filter_pipeline.py` (270 lines)

**Read for context, NOT ported in B.1:**
- `tracepoint_port/TracePoint/core/geometry_matrix.py` — uses the heavy_pipeline output as its first stage; B.2's port target, not B.1's
- `tracepoint_port/TracePoint/core/pdf_engine.py` — already ported in v0.2; provides the `VectorPath` dataclass that filter_pipeline gates consume
- `tracepoint_port/TracePoint/core/zone_filter.py` — already ported in v0.2; provides the zone exclusions that `gate_zone_mask` consumes

The discovery pass (`backend/TRACEPOINT_DISCOVERY.md`) already established that `filter_pipeline.py` has stdlib-only imports (`dataclasses`, `typing`) and **does NOT import from `core.*` or `data.*`**. This means there are no import-path edits required. The expected `diff` against TracePoint source is **zero lines**.

---

## 2. Goal Statement

**B.1 ships when:**

1. `backend/core/filter_pipeline.py` exists and is **byte-identical** to `tracepoint_port/TracePoint/core/filter_pipeline.py` (verified by `diff` returning zero output)
2. `backend/tests/test_filter_pipeline.py` exists and is **byte-identical** to `tracepoint_port/TracePoint/tests/test_filter_pipeline.py`
3. The portable test suite is green at 100% — exact count to be measured during execution; expected ≥30 tests based on the 270-line test file size and v0.2's 60 tests/412 lines ratio
4. Phase 1 v6.3.5 still passes its full test floor (sacred — must not regress)
5. Phase 2 v0.1 backend tests still pass 38/38 (sacred — must not regress)
6. v0.2 ported tests still pass: test_pdf_engine.py 40/40 + test_dispatch.py unit subset 34 (sacred — must not regress)
7. **No new backend dependencies added.** B.1 is stdlib-only by design.

**B.1 explicitly does NOT ship:**
- B.2 geometry engine (`geometry_matrix.py`)
- B.3 polygon scorers (`polygon_scorers.py`)
- B.4 architect-profile + storage + correction_store
- v0.2.1 schema migration / D-4 / D-5
- Any new HTTP endpoint, viewer integration, or trade module work
- Any change to v0.2's ported files (`config.py`, `pdf_engine.py`, `zone_filter.py`, `context.py`, `dispatch_gate.py`)

---

## 3. Pre-Conditions (Verify Before Step 1)

Before any code touches the backend monorepo:

- [ ] Sacred floor verified: 138 frontend (or current verified count, see §3.1 below) + 112 backend (40 test_pdf_engine + 34 test_dispatch unit + 38 v0.1) + 19 skipped = 250 / 19 / 0
- [ ] `tracepoint_port/TracePoint/core/filter_pipeline.py` exists and is read-only (verify file mtime unchanged, no .pyc beside it)
- [ ] `tracepoint_port/TracePoint/tests/test_filter_pipeline.py` exists and is read-only
- [ ] `backend/core/filter_pipeline.py` does NOT exist yet
- [ ] `backend/tests/test_filter_pipeline.py` does NOT exist yet
- [ ] Branch state: working tree clean. Either continue on `phase2-v0.2-dispatch-port` or branch from it as `phase2-v0.3-B1-filter-pipeline`. Daniel's call at the gate.

### 3.1 Sacred floor reconciliation note

The frontend test runner reported 107/107 in Task 1's gate report; CLAUDE.md and prior session memory cite 138 as the canonical Phase 1 v6.3.5 floor. This is documented as an open environmental question (file version drift between v6.3.1 in the workspace and v6.3.5 canon). For B.1's gate, the rule is **"no regression from the start-of-session count"** — whatever frontend count the test runner produces at Step 0 is the floor that Step 5 must hold. If the count changes between Step 0 and Step 5, that's a regression. Don't try to reconcile to "138" from a v6.3.1 environment.

---

## 4. Constraints

### 4.1 — Sacred files (do not modify)

- **Phase 1 v6.3.5 frontend HTML** — sacred per CLAUDE.md §0
- **Phase 2 v0.1 backend** — `shared/bidset_record.py`, the v0.1 test fixtures, `backend/seeds/roofing_materials.py` (the 21-item ROOFING_SEED_ITEMS file)
- **v0.2 ported files** — `backend/core/{config,pdf_engine,zone_filter,context,dispatch_gate}.py`, `backend/seeds/roofing_spec_database.py`, `backend/tests/{test_pdf_engine,test_dispatch}.py`. Byte-identical to TracePoint source (or 3-line same-character diff for dispatch_gate.py). Do not touch.
- **TracePoint source files in `tracepoint_port/TracePoint/`** — read-only reference. Copy from, never modify, never delete (Daniel manages the folder).
- **CLAUDE.md** — read-only during B.1 execution. The Task 1 bookkeeping pass already corrected B.2 and B.4 entries; no further CLAUDE.md edits in B.1.

### 4.2 — Do not expand scope

- DO NOT port `geometry_matrix.py` — that's B.2.
- DO NOT port `polygon_scorers.py` — that's B.3.
- DO NOT port `architect_profile.py`, `storage.py`, or `correction_store.py` — that's B.4.
- DO NOT port `trade_module.py`, `roofing_module.py`, or `vocabulary.py` — those are Phase D.
- DO NOT port any FastAPI route from `tracepoint_port/TracePoint/server/`.
- DO NOT add new pyproject.toml dependencies. B.1 is stdlib-only.
- DO NOT migrate `BidsetRecord` to `PlanSetContext` — that's v0.2.1.
- DO NOT fix D-4 or D-5 — that's v0.2.1.
- DO NOT add features "while we're in there" — refactoring, error handling, generalizing, renaming. The v0.2 discipline holds identically here.

### 4.3 — Do not reinvent

- DO NOT rewrite any TracePoint regex pattern, calibration threshold, gate ordering, or dataclass field "for clarity."
- DO NOT change the gate function signatures. The composable contract (`paths in → paths out + GateLog`) is canon.
- DO NOT change the 1.0pt heavy-line cutoff, the 0.5-inch length floor, or any dash-pattern detection threshold. These are the calibrated values from TracePoint's 15 bid set sweep.
- DO NOT change the order of gates within `run_heavy_pipeline` or `run_allpaths_pipeline`. The order is empirically derived.
- DO NOT add new gates, even if a future need is obvious. New gates are a separate ticket with their own diagnostic.
- DO NOT replace `dataclasses` with Pydantic, NamedTuples, or anything else "for consistency with the rest of the backend." TracePoint uses dataclasses; the port preserves dataclasses.

### 4.4 — Karpathy procedure (mandatory, no exceptions)

For every Step that involves writing or modifying code:
1. **Read existing code first** (state which files were read in the Step report — full line counts, not "lines 1–50 + grep")
2. **Write or copy failing tests first** and confirm they fail before writing production code
3. **Write minimum code to pass the tests** — the verbatim port IS the minimum
4. **Run full backend + frontend test suite** — confirm 100% pass on portable tests, no sacred regressions
5. **Commit** with structured message; do NOT push (Daniel decides push timing)

Skip-step is forbidden. Speculation patches are forbidden. Partial reads are forbidden — `filter_pipeline.py` at 230 lines is small enough that a full read takes one tool call; do it.

§7 stops are correct discipline. If the verbatim port surfaces something the orders did not anticipate (extra import site, undocumented dependency, schema mismatch), STOP, document as a Discovered Issue, and ask Daniel before resolving. Do not extrapolate.

---

## 5. Step List (Gated, Sequential)

Each Step ends with a gate. Do not start the next Step until the current Step's gate is satisfied AND Daniel approves continuation.

### Step B.1.0 — Pre-flight

**Read:**
- This march orders document, end-to-end
- `CLAUDE.md` §6 (hard guardrails) — refresh on what cannot be touched
- `backend/TRACEPOINT_DISCOVERY.md` §3.7 (filter_pipeline inventory) and §8.1 (B.1 spec)

**Verify (no writes):**
- All §3 pre-conditions are satisfied
- The two source files exist at expected paths and are readable
- The two target paths in `backend/core/` and `backend/tests/` are clear (no pre-existing files)
- Sacred floor count at session start (run frontend test runner, run `pytest backend/tests/`, record both counts)

**Gate:** Pre-flight checklist 100% green. Sacred floor recorded as the baseline B.1.5 must preserve.

**Pause-for-confirm.**

---

### Step B.1.1 — Read filter_pipeline.py end-to-end

**Read:** `tracepoint_port/TracePoint/core/filter_pipeline.py` — full 230 lines. Not a partial read. Not a grep-and-skim.

**Verify (no writes):**
- Public exports as documented in discovery: `GateLog`, `FilterResult`, `gate_zone_mask`, `gate_weight_filter`, `gate_length_filter`, `gate_dash_filter`, `gate_color_filter`, `run_heavy_pipeline`, `run_allpaths_pipeline`
- Imports are stdlib only (`dataclasses`, `typing`) — confirm by grep, no `from core.` or `from data.` lines anywhere in the file
- No surprises: anything in the file that would require import-path edits gets surfaced as a Discovered Issue at this Step, NOT silently absorbed

**Gate:** File read in full. Public surface verified. Zero `from core.*` or `from data.*` imports confirmed by grep. If any surprise is found, STOP and report as D-ticket per §4.4.

**Pause-for-confirm.**

---

### Step B.1.2 — Read test_filter_pipeline.py end-to-end

**Read:** `tracepoint_port/TracePoint/tests/test_filter_pipeline.py` — full 270 lines.

**Verify (no writes):**
- Test file imports `from core.filter_pipeline import ...` (this WILL be an ImportError until Step B.1.4 lands the production code — that's the failing-test floor)
- No PDF dependencies (per discovery: uses `MockPath`)
- No fitz, PIL, opencv, shapely imports
- Test class structure mapped — count test classes and approximate test count

**Gate:** Test file read in full. No PDF dependencies confirmed. Test count expectation recorded for Step B.1.5's gate.

**Pause-for-confirm.**

---

### Step B.1.3 — Failing test floor

**Read:** Confirmed in B.1.1 and B.1.2.

**Write:**
- Copy `tracepoint_port/TracePoint/tests/test_filter_pipeline.py` → `backend/tests/test_filter_pipeline.py`
- Pure copy. Verbatim. No edits.

**Run:**
```
pytest backend/tests/test_filter_pipeline.py -v
```

**Expected result:** Every test in the file FAILS with `ImportError: No module named 'core.filter_pipeline'` (or equivalent). This is the failing-test floor — production code does not exist yet.

**Verify:**
- Existing 250/19/0 sacred floor still holds for the rest of the suite (run full pytest excluding the new failing file, or use `--continue-on-collection-errors` to confirm the new file is the only failure)
- No regressions to v0.2 ported tests (test_pdf_engine.py 40/40, test_dispatch.py unit 34/34)

**Gate:** Test file in place. All tests failing with ImportError on the missing production module. Sacred floor otherwise unchanged.

**Pause-for-confirm.**

---

### Step B.1.4 — Port filter_pipeline.py verbatim

**Read:** Confirmed in B.1.1.

**Write:**
- Copy `tracepoint_port/TracePoint/core/filter_pipeline.py` → `backend/core/filter_pipeline.py`
- Pure copy. Verbatim. No edits. No import-path edits expected (filter_pipeline imports stdlib only).

**Verify:**
```
diff tracepoint_port/TracePoint/core/filter_pipeline.py backend/core/filter_pipeline.py
```
**Expected output: zero lines.** Byte-identical.

If `diff` produces any output, STOP. Do not "fix it up." That output is a §7 Discovered Issue requiring Daniel's review before proceeding. Same character as v0.2's D-2 dispatch_gate.py line-1359 issue.

**Run:**
```
pytest backend/tests/test_filter_pipeline.py -v
```

**Expected result:** All tests in `test_filter_pipeline.py` now pass — they failed at Step B.1.3 with ImportError, they pass at Step B.1.4 because the imports resolve. Test count = whatever Step B.1.2 recorded.

**Verify:**
- Full backend pytest: existing 112 tests + new B.1 tests, all green, 19 skipped, 0 failed
- Phase 1 frontend test runner: same count as Step B.1.0's baseline, no regression
- Total sacred floor: 250 + B.1 count / 19 / 0

**Gate:** filter_pipeline.py byte-identical to source. test_filter_pipeline.py 100% green. Phase 1 unchanged. Phase 2 v0.1 unchanged. v0.2 ported tests unchanged.

**Pause-for-confirm.**

---

### Step B.1.5 — Final regression and gate report

**Read:** N/A (verification step).

**Write:** No production code. No tests. Only the gate report itself.

**Run (final regression sweep):**
```
# Backend
cd backend && pytest -v

# Frontend
node run_tests.js
```

**Expected:**
- Backend: 112 + B.1 count tests passing, 19 skipped, 0 failed
- Frontend: same count as B.1.0 baseline, no regression

**Produce gate report** in the standard format:
```
=== Phase B.1 Session Report — <date> ===
STEP COMPLETED: B.1 — port filter_pipeline.py and test_filter_pipeline.py verbatim
FILES CHANGED:
  backend/core/filter_pipeline.py        NEW (230 lines, byte-identical to TracePoint)
  backend/tests/test_filter_pipeline.py  NEW (270 lines, byte-identical to TracePoint)
  Verbatim verification: `diff` against TracePoint source produced zero output
  for both files.
FILES NOT CHANGED (sacred):
  - All TracePoint sources at tracepoint_port/TracePoint/  (read-only)
  - Phase 1 v6.3.5 frontend HTML
  - backend/seeds/*  (Phase 2 seed files)
  - backend/scripts/_pipeline/*  (v0.1)
  - shared/bidset_record.py  (v0.1 schema; v0.2.1 ticket scope)
  - backend/core/{config,pdf_engine,zone_filter,context,dispatch_gate}.py
    (v0.2 ported files — all unchanged)
  - backend/seeds/roofing_spec_database.py
  - backend/tests/{test_pdf_engine,test_dispatch}.py  (v0.2 ported tests)
  - CLAUDE.md, DISCOVERED_ISSUES.md, V0_2_VALIDATION.md, all other docs
  - pyproject.toml — NO new dependencies added
TESTS:
  Phase 1 v6.3.5 frontend:           <count>/<count>  (sacred — re-verified)
  Phase 2 v0.1 backend (alone):       38/38   (sacred — re-verified)
  test_pdf_engine.py:                 40/40   (still green from v0.2)
  test_dispatch.py:                   34 passed, 19 skipped (still green from v0.2)
  test_filter_pipeline.py (new):      <count>/<count>  (B.1 gate target hit)
  Full backend suite:                 <total> passed, 19 skipped, 0 failed
  Cross-suite total:                  <250 + B.1 count> passing / 19 skipped / 0 failing
REGRESSIONS: none
PROCESSES: all foreground; nothing left running
DEPENDENCIES: pyproject.toml unchanged. No new deps added.
KARPATHY DISCIPLINE:
  - Read first: TracePoint filter_pipeline.py (230 lines, full) and
                test_filter_pipeline.py (270 lines, full) read end-to-end
                BEFORE any writes
  - Failing test floor: Step B.1.3 turned 0/<count> into <count>/<count>
                by porting production code only
  - Minimum implementation: pure verbatim copy, zero edits, `diff` confirms
  - 100% green floor: all sacred suites unchanged, B.1 tests fully green
DISCOVERED ISSUES: <none, OR D-6+ if any surfaced>
NEXT STEP: B.2 — port geometry_matrix.py and test_geometry_matrix.py
           Adds backend dependencies: opencv-python, numpy, shapely, Pillow.
           Pre-flight will include dependency install verification on Daniel's
           target environment before any code lands.
AWAITING APPROVAL: yes — Daniel approves B.2 march orders draft before
                   any further code lands.
```

**Gate:** Gate report produced. All sacred floors held. B.1 tests all green. No regressions. No D-tickets opened (or all open D-tickets explicitly named in the report).

**Pause-for-confirm. B.1 is sealed when Daniel approves the report.**

---

## 6. Test Floor Targets

| Suite | v0.2 baseline | After B.1 | Notes |
|---|---:|---:|---|
| Phase 1 frontend | <varies — see §3.1> | unchanged | sacred; no regression |
| Phase 2 v0.1 backend | 38 | 38 | sacred; no regression |
| test_pdf_engine.py | 40 | 40 | v0.2; no regression |
| test_dispatch.py unit | 34 | 34 | v0.2; no regression |
| test_dispatch.py integration | 19 skipped | 19 skipped | v0.2; gated on PDF availability |
| test_filter_pipeline.py | 0 | (count TBD) | B.1 NEW |
| Backend total passing | 112 | 112 + B.1 count | |
| Backend total skipped | 19 | 19 | unchanged |
| Backend total failed | 0 | 0 | floor |

The exact B.1 test count is intentionally not pre-stated in this document. It will be measured at Step B.1.2 (when the test file is read in full) and confirmed at Step B.1.5 (final report). Pre-stating a specific count creates a temptation to fudge the count if the test file produces a different number; let the empirical count be the empirical count.

---

## 7. §7 — Discovered Issues Discipline

If anything surprises you during execution, STOP and document as a Discovered Issue (D-ticket), do NOT silently resolve.

Specifically watch for:

1. **Diff output ≠ zero** at Step B.1.4. Even one extra blank line at end of file is a §7 stop. Do NOT normalize line endings, do NOT trim whitespace. Surface the difference; let Daniel decide.
2. **Import errors beyond the expected `core.filter_pipeline` ImportError** at Step B.1.3. If test_filter_pipeline.py imports something else that isn't available, that's a §7 stop.
3. **Test count differs significantly from expectation.** If Step B.1.2 estimates 30 tests and Step B.1.5 sees 100, surface the discrepancy. Could be a test class that expanded under TracePoint's later development.
4. **Sacred floor regression of any kind.** Any test that passes in the pre-flight baseline and fails after a B.1 step is a §7 stop. Investigate before proceeding.
5. **A `from core.something` import that wasn't in the discovery's documented import list.** Surface it. Discovery may have missed something.

§7 stops are documentation actions, not blocking actions. Document the issue in `backend/DISCOVERED_ISSUES.md` as D-6 (or next available number), pause, ask Daniel. Do not extrapolate.

This is the same discipline that produced D-1 through D-5 across v0.2 and is what kept the verbatim port faithful end-to-end.

---

## 8. Open Questions for Daniel

These are flagged for resolution at the B.1.0 pre-flight gate, not pre-answered in this document:

1. **Branch strategy.** Continue on `phase2-v0.2-dispatch-port` or branch as `phase2-v0.3-B1-filter-pipeline`? Each B.1 → B.4 gets its own branch is cleanest; one continuous branch is fastest. Daniel decides.

2. **`backend/core/__init__.py` export update.** TracePoint's `core/__init__.py` is empty (per discovery). After B.1 lands, do callers `from core.filter_pipeline import gate_zone_mask` directly (current TracePoint convention) or does `__init__.py` get an explicit re-export? Recommend keeping `__init__.py` empty per TracePoint convention; do not add re-exports during B.1.

3. **Commit timing.** Single commit at Step B.1.5? Stage commits per Step? v0.2 used a single commit per phase; same convention recommended for B.1.

These are documented for the B.1.0 gate review and resolved before Step B.1.1 begins.

---

## 9. Done Definition

B.1 is done when:

- [ ] `backend/core/filter_pipeline.py` exists, byte-identical to TracePoint source
- [ ] `backend/tests/test_filter_pipeline.py` exists, byte-identical to TracePoint source
- [ ] All B.1 tests pass at 100%
- [ ] Phase 1 frontend test count: no regression from B.1.0 baseline
- [ ] Phase 2 v0.1 backend tests: still 38/38
- [ ] v0.2 ported tests: still 40 + 34
- [ ] No new dependencies in `pyproject.toml`
- [ ] No changes to any sacred file
- [ ] No D-tickets opened, or all open D-tickets explicitly resolved/deferred with Daniel's approval
- [ ] Single commit on the chosen branch (no push)
- [ ] Gate report produced and approved by Daniel

When done, B.2 march orders may be drafted (port `geometry_matrix.py` — adds opencv-python, numpy, shapely, Pillow; the dependency-surface phase). B.2 is not yet scoped; that's the next planning conversation after B.1 ships.

---

**End of MARCH_ORDERS_B_1.md. Awaiting Daniel's review.**
