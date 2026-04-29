# Phase B.2 + B.3 — March Orders (Combined Big Run)

**Target:** Port TracePoint Stages 6–9 (geometry engine, `geometry_matrix.py`) AND Stages 10–12 (post-clustering scorers, `polygon_scorers.py`) verbatim into the Huckleberry backend in a single autonomous session.

**Authored:** 2026-04-27
**Authority:** Daniel (POC owner)
**Predecessor:** B.1 (commit `1c3fde4` on branch `phase2-v0.3-B1-filter-pipeline`). Sacred floor at session start: 277 / 19 / 0 (frontend 107 + spotchecks 41 + backend 139 = 287 with mutation tests counted; the 277 is the run_tests.js + backend pytest sum without spotchecks/mutation tests counted twice).
**Source authority:** `tracepoint_port/TracePoint/` — read-only reference. Every file ported is verified byte-identical via SHA-1 / `diff = 0` per `backend/TRACEPOINT_DISCOVERY.md` §8.
**Discipline:** Karpathy procedure preserved on substance (read first, verbatim copy, sacred floors, §7 stops). Procedural pause-for-confirm gates BETWEEN steps are removed for autonomous execution. Daniel reviews ONE final report at the end.
**Expected wall-clock:** ~90–120 minutes including dependency install verification.

---

## 0. Scope and Why This Is Two Phases in One Session

B.2 ports the geometry engine — the cv2/numpy/shapely contour-detection-and-clustering layer that produces candidate building polygons. B.3 ports the post-clustering scorers — interior density, rectilinearity, and final selection. They are sequential by dependency (B.3's tests use `GeometryMatrix.DetectedContour` from B.2) but each is a clean verbatim port with byte-identical `diff = 0` verification.

Combined for one session because:
- B.2's substantive risk is the **dependency install** (opencv-python, numpy, shapely, Pillow on Daniel's Windows environment). That gate happens once, before any production code lands. After it clears, the port itself is mechanical.
- B.3 has **zero new dependencies** and is stdlib-only. Once B.2's deps are in, B.3 adds zero new risk.
- Splitting B.2 and B.3 across sessions doubles the read-and-pre-flight overhead for marginal safety gain. The substantive verification (`diff = 0`, all sacred floors held, all new tests green) happens in both cases.

**Total port surface this session:**
- B.2: `geometry_matrix.py` (832 lines) + `test_geometry_matrix.py` (380 lines) = 1,212 lines
- B.3: `polygon_scorers.py` (272 lines) + `test_polygon_scorers.py` (170 lines) = 442 lines
- **Combined: 1,654 lines of verbatim port + dependency surface verification**

---

## 1. TracePoint Files Read in Full (Pre-Condition)

Before any code touches the backend, the following files are read end-to-end:

**B.2 port targets (read in full):**
- `tracepoint_port/TracePoint/core/geometry_matrix.py` (832 lines)
- `tracepoint_port/TracePoint/tests/test_geometry_matrix.py` (380 lines)

**B.3 port targets (read in full):**
- `tracepoint_port/TracePoint/core/polygon_scorers.py` (272 lines)
- `tracepoint_port/TracePoint/tests/test_polygon_scorers.py` (170 lines)

**Read for context, NOT ported:**
- `tracepoint_port/TracePoint/requirements.txt` — version-constraint reference for the four new deps
- `backend/pyproject.toml` — the file edited at Step B.2.1 to add the four deps
- `backend/core/filter_pipeline.py` — B.1 ported; geometry engine consumes its `FilterResult` indirectly
- `backend/core/pdf_engine.py` — provides `VectorPath` consumed by geometry_matrix
- `backend/core/context.py` — provides PageZone/TextBlock dataclasses consumed by polygon_scorers

The discovery pass already established:
- `geometry_matrix.py` imports: `dataclasses`, `typing`, `cv2`, `numpy`, `PIL.Image`, `shapely.geometry.Polygon/MultiPolygon`, `shapely.ops.unary_union`, `shapely.validation.make_valid`, plus `core.config.{ARCH_SCALES,CONTOUR_APPROX_EPSILON,CONTOUR_MIN_AREA_RATIO}`. **Zero `from data.*` imports.** Expected diff vs source: zero lines (cv2/numpy/shapely imports stay; the `from core.config import ...` line stays — `core.config` already exists in backend from v0.2).
- `polygon_scorers.py` imports: `re`, `dataclasses`, `typing`. **Stdlib-only.** Zero `from core.*` or `from data.*` imports. Expected diff vs source: zero lines.

If discovery's import analysis is wrong, that's a §7 stop at Step B.2.2 or B.3.1 — surface as Discovered Issue, do not silently absorb.

---

## 2. Goal Statement

**This session ships when:**

1. `backend/pyproject.toml` adds four dependencies with versions matching `tracepoint_port/TracePoint/requirements.txt`: `opencv-python>=4.9.0`, `numpy>=1.26.0`, `shapely>=2.0.0`, `Pillow>=10.0.0`
2. Dependencies install cleanly on Daniel's environment via `pip install -e .` (or `uv pip install -e ".[dev]"` if uv is in use)
3. `backend/core/geometry_matrix.py` exists, byte-identical to TracePoint source (`diff = 0`, SHA-1 match)
4. `backend/tests/test_geometry_matrix.py` exists, byte-identical
5. `backend/core/polygon_scorers.py` exists, byte-identical
6. `backend/tests/test_polygon_scorers.py` exists, byte-identical
7. All B.2 tests pass at 100% (count empirical, ~30–50 expected from 380-line test file)
8. All B.3 tests pass at 100% (count empirical, ~20–35 expected from 170-line test file)
9. Sacred floors held — see §3 below
10. Single commit per phase: B.2 commits at end of B.2, B.3 commits at end of B.3. Two commits total this session.

**This session explicitly does NOT ship:**
- B.4 architect_profile / storage / correction_store
- v0.2.1 schema migration / D-4 / D-5
- Phase D trade module work
- L-shape/T-shape user-polygon override (frontend UX concern, stays in frontend)
- Any threshold retuning of TracePoint's calibrated values (0.5-inch proximity, 50 sq.in. minimum, 1.0pt heavy-line cutoff, 0.06 callout density, 0.03 secondary, 0.5 long-text ratio)
- Any change to v0.2 ported files or B.1 ported files
- Any new dependency beyond the four listed above

---

## 3. Sacred Floor — Hold Each Line Item

Same rule as B.1: don't reconcile to a single total; hold each line independently. Step B.3.5 must show every line at-or-better than the start-of-session baseline.

**Start-of-session baseline (B.1's end-state):**

| Suite | Count |
|---|---|
| Frontend `run_tests.js` | 107/107 |
| Frontend `spotcheck_10b.js` | 7/7 |
| Frontend `spotcheck_cricket.js` | 4/4 |
| Frontend `spotcheck_durolast.js` | 8/8 |
| Frontend `spotcheck_manufacturer.js` | 14/14 |
| Frontend `mutation_test_step11.js` | 8/8 mutations caught |
| Backend `test_pdf_engine.py` | 40/40 |
| Backend `test_dispatch.py` | 34 passed, 19 skipped |
| Backend `test_filter_pipeline.py` (B.1) | 27/27 |
| Backend v0.1 baseline | 38/38 |
| Backend full suite | 139 passed, 19 skipped, 0 failed |

**Expected end-of-session:**

| Suite | Count |
|---|---|
| All frontend suites | unchanged (sacred) |
| Backend `test_pdf_engine.py` | 40/40 (sacred) |
| Backend `test_dispatch.py` | 34 passed, 19 skipped (sacred) |
| Backend `test_filter_pipeline.py` | 27/27 (sacred) |
| Backend v0.1 baseline | 38/38 (sacred) |
| Backend `test_geometry_matrix.py` (B.2 NEW) | empirical, ~30–50 |
| Backend `test_polygon_scorers.py` (B.3 NEW) | empirical, ~20–35 |
| Backend full suite | 139 + B.2 count + B.3 count, 19 skipped, 0 failed |

If anything regresses below the baseline at any verification point, that's a §7 stop.

---

## 4. Constraints

### 4.1 — Sacred files (do not modify)

- All files at `tracepoint_port/TracePoint/` — read-only reference, never modified
- Phase 1 frontend HTML
- All v0.2 ported files: `backend/core/{config,pdf_engine,zone_filter,context,dispatch_gate}.py`, `backend/seeds/roofing_spec_database.py`, `backend/tests/{test_pdf_engine,test_dispatch}.py`
- B.1 ported files: `backend/core/filter_pipeline.py`, `backend/tests/test_filter_pipeline.py`
- v0.1 schema files: `shared/bidset_record.py`, `backend/seeds/roofing_materials.py` (the 21-item ROOFING_SEED_ITEMS), `backend/scripts/_pipeline/*`
- `backend/core/__init__.py` — keep empty per TracePoint convention (do not add re-exports)
- `CLAUDE.md`, `MARCH_ORDERS_v0_2.md`, `MARCH_ORDERS_B_1.md`, all `STEP_*.md`, `DISCOVERED_ISSUES.md`, `V0_2_VALIDATION.md`, all observation/diagnostic docs — read-only during execution

### 4.2 — Do not expand scope

- DO NOT port `architect_profile.py`, `storage.py`, `correction_store.py` — that's B.4
- DO NOT port `trade_module.py`, `roofing_module.py`, `vocabulary.py` — Phase D
- DO NOT port any FastAPI route from `tracepoint_port/TracePoint/server/`
- DO NOT add new dependencies beyond the four listed in §2
- DO NOT migrate `BidsetRecord` to `PlanSetContext` — v0.2.1
- DO NOT fix D-4 or D-5 — v0.2.1
- DO NOT add features "while we're in there"
- DO NOT touch frontend code in any way

### 4.3 — Do not reinvent

- DO NOT rewrite any TracePoint regex pattern, calibration threshold, gate ordering, dataclass field, or function signature "for clarity"
- DO NOT change the calibrated thresholds: 0.5-inch proximity, 50 sq.in. minimum, 1.0pt heavy-line cutoff, 0.06 callout density bonus, 0.03 secondary, 0.5 long-text ratio penalty, noise-zone overlap
- DO NOT replace `dataclasses` with Pydantic, NamedTuples, or anything else "for backend consistency"
- DO NOT change opencv import style (`import cv2` vs `from cv2 import ...`) — match TracePoint exactly
- DO NOT replace `numpy` with anything else even if a one-line use looks trivial
- DO NOT replace `shapely` operations with custom geometry — calibrated empirically

### 4.4 — Karpathy procedure (held on substance)

- Read first (full reads, not partial). State which files were read in the final gate report.
- Verbatim copy. `diff = 0` is the verification.
- Sacred floors held at every verification point.
- §7 stops surface Discovered Issues, do not silently resolve.

### 4.5 — Autonomous execution permitted between substantive gates

The procedural pause-for-confirm gates between every numbered step are removed. Claude Code runs Steps B.2.0 through B.3.5 in one session, stopping ONLY on §7 conditions. Steps internally verify their own completion before proceeding to the next. ONE final gate report at the end of B.3.5.

---

## 5. Step List (Substantive Gates Only)

### Step B.2.0 — Pre-flight

**Read:** This march orders document end-to-end. `CLAUDE.md` §6 (hard guardrails, refresh). `backend/TRACEPOINT_DISCOVERY.md` §3.8, §3.9, §6.3, §8.2, §8.3 (B.2 + B.3 specs).

**Verify (no writes):**
- All §1 source files exist and are readable
- All §3 baseline counts match exactly via `node run_tests.js`, the spotcheck scripts, and `pytest -q`
- Working tree clean (or known-stash-pattern clean per B.1's pop-after-commit pattern). If stash needed, `git stash push -u -m "B.2/B.3 pre-flight"` BEFORE branching.
- Branch state: confirm starting from `phase2-v0.3-B1-filter-pipeline` HEAD `1c3fde4`. Create `phase2-v0.3-B2-geometry-engine` from this HEAD. (B.3 will branch off B.2's commit at end of Step B.2.5; OR continue on the B.2 branch if Daniel prefers — recommended: continue on B.2 branch with two commits, simpler than a third branch for B.3.)

**Internal gate:** All pre-conditions green. Sacred baseline recorded. New branch checked out. Working tree clean.

**§7 stop only if:** any baseline count differs from B.1's reported end-state, any source file missing, working tree won't clean.

### Step B.2.1 — Add B.2 dependencies to pyproject.toml

**Read:** `backend/pyproject.toml` end-to-end. `tracepoint_port/TracePoint/requirements.txt` for version constraints.

**Write:** Add to `[project] dependencies` section (do NOT remove anything that's already there):
```
"opencv-python>=4.9.0",
"numpy>=1.26.0",
"shapely>=2.0.0",
"Pillow>=10.0.0",
```

**Run:**
```
# Whichever the backend uses — pip or uv
pip install -e ".[dev]"
# OR
uv pip install -e ".[dev]"

# Verify imports
python -c "import cv2, numpy, shapely, PIL; print(cv2.__version__, numpy.__version__, shapely.__version__, PIL.__version__)"

# Sacred floor check — no production code changed yet, so existing 139 backend tests must still all pass
pytest backend/tests/ -q
```

**Internal gate:** Imports resolve. All 139 backend tests still passing. No deps removed. No syntax errors in pyproject.toml.

**§7 stop only if:**
- Any of the four packages fails to install (Windows wheel issues with opencv-python are a known risk — surface immediately, do not try to compile from source)
- Imports fail
- Any sacred test regresses

### Step B.2.2 — Read geometry_matrix.py and test_geometry_matrix.py end-to-end

**Read:** Full files. `core/geometry_matrix.py` (832 lines) and `tests/test_geometry_matrix.py` (380 lines).

**Verify (no writes):**
- Imports match discovery: stdlib + cv2 + numpy + PIL + shapely + `from core.config import ARCH_SCALES, CONTOUR_APPROX_EPSILON, CONTOUR_MIN_AREA_RATIO`
- Zero `from core.pdf_engine`, `from core.zone_filter`, `from core.context`, or any other `from core.*` beyond config
- Zero `from data.*` imports
- Zero references to `correction_store`, `architect_profile`, `storage` (those are B.4)
- Test file imports `from core.geometry_matrix import GeometryMatrix, DetectedContour, GeometryResult` — confirms public surface
- Test count classes/functions roughly mapped — record approximate count for B.2.5 gate

**Internal gate:** Imports as anticipated. Public surface confirmed.

**§7 stop only if:** any unexpected import surfaces (e.g., a `from core.dispatch_gate import ...` that discovery missed), any reference to a future-phase module.

### Step B.2.3 — Failing test floor for B.2

**Write:** Copy `tracepoint_port/TracePoint/tests/test_geometry_matrix.py` → `backend/tests/test_geometry_matrix.py`. Pure copy, verbatim, no edits.

**Run:**
```
pytest backend/tests/test_geometry_matrix.py -v
```

**Expected:** Every test fails with `ImportError: No module named 'core.geometry_matrix'` (or pytest collection-time error reported as 1 error, same as B.1's pattern).

**Run:** Sacred floor still holds for everything else:
```
pytest backend/tests/ --ignore=backend/tests/test_geometry_matrix.py -q
```
Expected: 139 passed, 19 skipped, 0 failed (B.1's end-state, unchanged).

**Internal gate:** Test file in place. ImportError on missing production module. Sacred floor unchanged.

**§7 stop only if:** any non-ImportError failure (would mean some other dep is broken), or sacred floor regresses.

### Step B.2.4 — Port geometry_matrix.py verbatim

**Write:** Copy `tracepoint_port/TracePoint/core/geometry_matrix.py` → `backend/core/geometry_matrix.py`. Pure copy, verbatim, no edits expected.

**Verify:**
```
diff tracepoint_port/TracePoint/core/geometry_matrix.py backend/core/geometry_matrix.py
sha1sum tracepoint_port/TracePoint/core/geometry_matrix.py backend/core/geometry_matrix.py
```
**Expected:** `diff` produces zero output. SHA-1 sums match.

**§7 stop only if:** `diff` produces ANY output. Do not "fix it up." Surface as Discovered Issue requiring Daniel input.

**Run:**
```
pytest backend/tests/test_geometry_matrix.py -v
pytest backend/tests/ -q
```

**Expected:** All B.2 tests now pass. Full backend suite: 139 + B.2 count, 19 skipped, 0 failed.

**Internal gate:** B.2 tests 100% green. Full backend suite passes. No sacred regressions.

**§7 stop only if:** any test failure (other than the expected pre-port ImportError sequence resolving), any sacred regression.

### Step B.2.5 — B.2 commit

**Write (commit only, no code):**
```
git add backend/core/geometry_matrix.py backend/tests/test_geometry_matrix.py backend/pyproject.toml
git commit -m "Phase B.2: Port TracePoint geometry_matrix.py verbatim, add cv2/numpy/shapely/Pillow deps"
```

Record commit SHA for the final report.

**Internal gate:** Commit landed. Working tree clean (except for any unrelated stashed docs from B.2.0).

**No §7 stop here unless commit fails for some structural reason.**

### Step B.3.1 — Read polygon_scorers.py and test_polygon_scorers.py end-to-end

**Read:** Full files. `core/polygon_scorers.py` (272 lines) and `tests/test_polygon_scorers.py` (170 lines).

**Verify (no writes):**
- Imports match discovery: stdlib only (`re`, `dataclasses`, `typing`)
- Zero `from core.*` and zero `from data.*` imports
- Zero cv2/numpy/shapely/PIL imports (B.3 is stdlib-only — uses MockTextBlock/MockZone/MockPath in tests)
- Test file imports `from core.polygon_scorers import InteriorScore, score_interior, score_rectilinearity` — confirms public surface
- Test count roughly mapped

**Internal gate:** Imports as anticipated. Stdlib-only confirmed.

**§7 stop only if:** any unexpected import, especially if polygon_scorers references geometry_matrix at import time (it shouldn't — they're called sequentially by external code, not co-imported).

### Step B.3.2 — Failing test floor for B.3

**Write:** Copy `tracepoint_port/TracePoint/tests/test_polygon_scorers.py` → `backend/tests/test_polygon_scorers.py`. Pure copy, verbatim.

**Run:**
```
pytest backend/tests/test_polygon_scorers.py -v
pytest backend/tests/ --ignore=backend/tests/test_polygon_scorers.py -q
```

**Expected:** B.3 tests fail with ImportError. Rest of suite (B.1 + B.2 + v0.2 ported + v0.1 baseline) all green.

**Internal gate:** Test file in place. ImportError. Sacred floor + B.2 unchanged.

**§7 stop only if:** non-ImportError failure or any regression elsewhere.

### Step B.3.3 — Port polygon_scorers.py verbatim

**Write:** Copy `tracepoint_port/TracePoint/core/polygon_scorers.py` → `backend/core/polygon_scorers.py`. Verbatim.

**Verify:**
```
diff tracepoint_port/TracePoint/core/polygon_scorers.py backend/core/polygon_scorers.py
sha1sum tracepoint_port/TracePoint/core/polygon_scorers.py backend/core/polygon_scorers.py
```
**Expected:** `diff` zero output, SHA-1 match.

**Run:**
```
pytest backend/tests/test_polygon_scorers.py -v
pytest backend/tests/ -q
```

**Expected:** B.3 tests 100% green. Full backend suite: 139 + B.2 count + B.3 count, 19 skipped, 0 failed.

**Internal gate:** B.3 tests green. Full suite passes. No regressions.

**§7 stop only if:** `diff` non-zero, any test failure, any sacred regression.

### Step B.3.4 — Final regression sweep

**Run (in order):**
```
# Backend full suite — final
cd backend && pytest -v

# Frontend — every suite explicitly
node run_tests.js
node spotcheck_10b.js
node spotcheck_cricket.js
node spotcheck_durolast.js
node spotcheck_manufacturer.js
node mutation_test_step11.js
```

**Expected:**
- Backend: 139 + B.2 count + B.3 count passing, 19 skipped, 0 failed
- Frontend: every suite at exact baseline count, 0 failures

**Internal gate:** Every line of §3 baseline preserved or improved. Two new entries (B.2 + B.3 test files) at 100%.

**§7 stop only if:** any regression at all from the §3 baseline.

### Step B.3.5 — B.3 commit + final gate report

**Write (commit only, no code):**
```
git add backend/core/polygon_scorers.py backend/tests/test_polygon_scorers.py
git commit -m "Phase B.3: Port TracePoint polygon_scorers.py verbatim"
```

**Produce final gate report** in standard format. Single report covers both B.2 and B.3.

```
=== Phase B.2 + B.3 Combined Session Report — <date> ===

STEPS COMPLETED: B.2 (geometry engine, 832 lines + tests + 4 deps) and B.3 (post-clustering scorers, 272 lines + tests, stdlib-only)

FILES CHANGED:
  backend/pyproject.toml                          MODIFIED (added 4 deps)
  backend/core/geometry_matrix.py                 NEW (832 lines, byte-identical to TracePoint, sha1 <hash>)
  backend/tests/test_geometry_matrix.py           NEW (380 lines, byte-identical to TracePoint, sha1 <hash>)
  backend/core/polygon_scorers.py                 NEW (272 lines, byte-identical to TracePoint, sha1 <hash>)
  backend/tests/test_polygon_scorers.py           NEW (170 lines, byte-identical to TracePoint, sha1 <hash>)
  Verbatim verification: diff against TracePoint source = zero output for all 4 ported files. SHA-1 sums match.

DEPENDENCIES ADDED (B.2):
  opencv-python>=4.9.0    installed version: <X.Y.Z>
  numpy>=1.26.0           installed version: <X.Y.Z>
  shapely>=2.0.0          installed version: <X.Y.Z>
  Pillow>=10.0.0          installed version: <X.Y.Z>

FILES NOT CHANGED (sacred):
  All TracePoint sources at tracepoint_port/TracePoint/ (read-only)
  Phase 1 frontend HTML and all frontend test files
  v0.2 ported files: backend/core/{config,pdf_engine,zone_filter,context,dispatch_gate}.py
  v0.2 ported tests: backend/tests/{test_pdf_engine,test_dispatch}.py
  B.1 ported files: backend/core/filter_pipeline.py, backend/tests/test_filter_pipeline.py
  backend/core/__init__.py (kept empty)
  backend/seeds/* (Phase 2 seed files)
  shared/bidset_record.py (v0.1)
  CLAUDE.md, MARCH_ORDERS_*.md, all docs

TESTS:
| Suite                              | Before  | After   | Status |
|------------------------------------|---------|---------|--------|
| Frontend run_tests.js              | 107/107 | 107/107 | sacred |
| Frontend spotcheck_10b.js          | 7/7     | 7/7     | sacred |
| Frontend spotcheck_cricket.js      | 4/4     | 4/4     | sacred |
| Frontend spotcheck_durolast.js     | 8/8     | 8/8     | sacred |
| Frontend spotcheck_manufacturer.js | 14/14   | 14/14   | sacred |
| Frontend mutation_test_step11.js   | 8/8     | 8/8     | sacred |
| Backend test_pdf_engine.py         | 40/40   | 40/40   | sacred |
| Backend test_dispatch.py           | 34+19sk | 34+19sk | sacred |
| Backend test_filter_pipeline.py    | 27/27   | 27/27   | sacred |
| Backend v0.1 baseline              | 38/38   | 38/38   | sacred |
| Backend test_geometry_matrix.py    | -       | <N>/<N> | B.2 NEW |
| Backend test_polygon_scorers.py    | -       | <M>/<M> | B.3 NEW |
| Backend full suite total           | 139     | 139+N+M | +N+M passing |

REGRESSIONS: none

KARPATHY DISCIPLINE:
  Read first: 4 source files read end-to-end before any writes (832 + 380 + 272 + 170 = 1654 lines)
  Failing test floor: B.2.3 and B.3.2 produced expected ImportError before production code landed
  Minimum implementation: pure verbatim copies, zero edits. diff = 0 for all 4 files.
  100% green floor: all sacred suites unchanged, B.2 + B.3 tests fully green

DISCOVERED ISSUES: <none, OR D-6+ if any surfaced>

EXECUTION DETAIL:
  Branch: phase2-v0.3-B1-filter-pipeline → phase2-v0.3-B2-geometry-engine (created from 1c3fde4)
  B.2 commit: <SHA> "Phase B.2: Port TracePoint geometry_matrix.py verbatim, add cv2/numpy/shapely/Pillow deps"
  B.3 commit: <SHA> "Phase B.3: Port TracePoint polygon_scorers.py verbatim"
  Stash status at end: <empty, OR popped successfully>

NEXT STEP: B.4 — port architect_profile.py + correction_store.py (verbatim) and storage.py (Postgres adaptation per CLAUDE.md §5). B.4 has the most substantive risk in Phase B because storage.py is non-verbatim. B.4 march orders draft is the next planning task, not execution.

AWAITING APPROVAL: yes — Daniel approves both commits and gives push timing call.

B.2 + B.3 sealed. Backend suite: 139 → 139+N+M passing. Verbatim port held end-to-end on 1,304 lines of source. No D-tickets opened.
```

---

## 6. §7 Stop Conditions (Surface Issues, Don't Resolve)

Stop and surface as Discovered Issue, ask Daniel before proceeding:

1. **`diff` produces non-zero output** at B.2.4 or B.3.3
2. **SHA-1 mismatch** between source and ported file
3. **Dependency install fails** at B.2.1 (especially Windows wheel issues with opencv-python)
4. **Any sacred floor count regresses** at any verification point
5. **Unexpected import** surfaces in geometry_matrix.py or polygon_scorers.py beyond what discovery documented
6. **Test count significantly different** from rough expectation (e.g., test_geometry_matrix.py reports 5 tests instead of ~30–50, or 200 instead — surface as discrepancy, the test file may have changed since discovery)
7. **Production file outside the 4 B.2/B.3 targets gets modified** by accident
8. **`pyproject.toml` removes anything** that was previously present (additions only)

§7 stops are documentation actions, not blocking actions. Document in `backend/DISCOVERED_ISSUES.md` as D-6 (or next available number), pause, ask Daniel.

---

## 7. Done Definition

This session is done when:

- [ ] B.2 dependencies in pyproject.toml, install verified
- [ ] `backend/core/geometry_matrix.py` byte-identical to TracePoint source
- [ ] `backend/tests/test_geometry_matrix.py` byte-identical
- [ ] `backend/core/polygon_scorers.py` byte-identical
- [ ] `backend/tests/test_polygon_scorers.py` byte-identical
- [ ] All B.2 tests 100% green
- [ ] All B.3 tests 100% green
- [ ] All sacred floors held at every verification point
- [ ] No new dependencies beyond the 4 listed
- [ ] No changes to any sacred file
- [ ] No D-tickets opened, OR all open D-tickets explicitly resolved/deferred
- [ ] Two commits on the chosen branch (B.2 then B.3), no push
- [ ] Final gate report produced

When done, B.4 march orders may be drafted next. B.4 is the heaviest in Phase B because of the Postgres adaptation; it gets its own dedicated planning conversation.

---

**End of MARCH_ORDERS_B_2_AND_B_3.md. Awaiting Daniel's review and Claude Code execution brief.**
