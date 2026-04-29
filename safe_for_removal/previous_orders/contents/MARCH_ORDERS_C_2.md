# Phase C.2 — March Orders

**Target:** Port TracePoint's roofing trade module verbatim into the Huckleberry backend. First concrete trade module against the C.1 contract. Three production files (vocabulary + roofing module + build_trade_input helper) plus their tests. Autonomous single-session big-run.

**Authored:** 2026-04-27
**Authority:** Daniel (POC owner)
**Predecessor:** C.1 (commit `23a459c` on branch `phase2-v0.3-C1-trade-module-interface`). Sacred floor at session start: backend 214 passing / 19 skipped / 0 failing, frontend 107 + spotchecks + mutation tests unchanged.
**Source authority:** `tracepoint_port/TracePoint/` — read-only reference.
**Discipline:** Karpathy preserved on substance. Autonomous between substantive gates per the B.2+B.3 / B.4 / C.1 pattern. Daniel reviews ONE final report at the end.
**Expected wall-clock:** ~75–105 minutes. Larger than B.4 (which was 700 lines); smaller than B.2 (which was 1,212 lines + 4 deps).

---

## 0. What C.2 Is and What It Is Not

**C.2 is the first trade module that DOES something.** C.1 ported the contract (the Protocol and three dataclasses defining what a trade module looks like). C.2 ports an actual trade module that implements the contract — TracePoint's roofing module, which reads structured PDF input, runs roofing-specific scope detection, and produces roofing-shaped output (system identification, quantities, materials).

**C.2 is behavior-bearing.** Unlike C.1, C.2 has actual logic: vocabulary matching, scope detection, quantity derivation. This means the full failing-test-floor pattern from B.1–B.4 applies — copy tests first (they fail with ImportError), then port production code (tests now pass), then verify sacred floors held.

**C.2 is verbatim port discipline.** Same standard as every other Phase B port: `diff = 0` against TracePoint source, SHA-1 verification, no edits, no calibration changes, no "improvements for clarity."

**C.2 is NOT:**
- Activation of the trade module in `dispatch_gate.py` (that's later — C.4 or Phase E)
- Building any second trade module (glazing is C.3)
- Solving the cross-trade integration questions from C.1's appendix (those are C.4)
- A standalone HTTP route (the FastAPI server route is part of TracePoint's `server/` folder, not in scope here — only the `build_trade_input()` helper that the route uses comes over)
- v0.2.1 work (D-4 / D-5 / schema migration remain queued)

---

## 1. TracePoint Files Read in Full (Pre-Condition)

Before any code touches the backend, the following files are read end-to-end:

**C.2 port targets (production):**
- `tracepoint_port/TracePoint/modules/roofing/vocabulary.py` (575 lines)
- `tracepoint_port/TracePoint/modules/roofing/roofing_module.py` (434 lines)
- `tracepoint_port/TracePoint/server/routes/trade.py` — extract ONLY the `build_trade_input()` helper function (~90 lines of the 229-line file). The remainder (FastAPI route handlers) is NOT in scope per §0.

**C.2 port targets (tests):**
- All `tracepoint_port/TracePoint/tests/test_*roofing*.py` files. Discovery did not enumerate these by name; pre-flight verifies the exact list and counts.
- Any `tracepoint_port/TracePoint/tests/test_vocabulary.py` if present
- Any `tracepoint_port/TracePoint/tests/test_build_trade_input.py` or equivalent if present

**Read for context, NOT ported:**
- `backend/core/trade_module.py` (C.1) — the Protocol that roofing_module.py implements
- `backend/seeds/roofing_spec_database.py` (v0.2) — vocabulary likely consumes this
- `backend/seeds/roof_assemblies.py` (Phase 2 seed, no current consumer) — vocabulary or roofing_module may consume this; pre-flight discovery confirms
- TracePoint paper §9 — describes the trade module pattern roofing implements

**Discovery's import expectations** (per `backend/TRACEPOINT_DISCOVERY.md`):
- `vocabulary.py` (575 lines): expected stdlib + project imports. Pre-flight verifies which.
- `roofing_module.py` (434 lines): expected to import from `core.trade_module` (C.1) and from the roofing vocabulary file. Pre-flight verifies.
- `build_trade_input()` from `server/routes/trade.py`: expected to import from core dispatch context types. Pre-flight verifies which symbols are needed and whether the helper has any FastAPI-specific dependencies that would block extraction.

If any imports are unexpected, that's a §7 stop at Step C.2.2.

---

## 2. The build_trade_input Extraction Question (Resolved Up Front)

The discovery document says the `build_trade_input()` helper is part of `server/routes/trade.py` (a FastAPI route file). We do NOT want to port the FastAPI route — that belongs to Phase E. We DO want the helper because roofing_module needs it.

**Resolution:** extract the `build_trade_input()` function (and any private helpers it depends on) into a new standalone file `backend/core/trade_input_builder.py`. This is a **deliberate adaptation**, not a verbatim copy of `server/routes/trade.py`. The function body inside `build_trade_input()` is verbatim from TracePoint; only the file location changes (extracted out of the route file into a standalone module).

This extraction is similar in shape to v0.2's three same-character import edits in `dispatch_gate.py` — minimal change, well-scoped, called out explicitly. The extraction MUST preserve the function signature, body, and any private helpers used. The only edit is removing the FastAPI route decorator (if any) and any FastAPI imports that aren't needed by the helper itself.

If `build_trade_input()` is tightly coupled to FastAPI request/response objects in ways that make extraction non-trivial, that's a §7 stop at Step C.2.2 — surface, ask Daniel.

---

## 3. Sacred Floor — Hold Each Line Item

**Start-of-session baseline (C.1's end-state):**

| Suite | Count |
|---|---:|
| Frontend `run_tests.js` | 107/107 |
| Frontend `spotcheck_10b.js` | 7/7 |
| Frontend `spotcheck_cricket.js` | 4/4 |
| Frontend `spotcheck_durolast.js` | 8/8 |
| Frontend `spotcheck_manufacturer.js` | 14/14 |
| Frontend `mutation_test_step11.js` | 8/8 mutations caught |
| Backend `test_pdf_engine.py` | 40/40 |
| Backend `test_dispatch.py` | 34 passed, 19 skipped |
| Backend `test_filter_pipeline.py` (B.1) | 27/27 |
| Backend `test_geometry_matrix.py` (B.2) | 36/36 |
| Backend `test_polygon_scorers.py` (B.3) | 16/16 |
| Backend `test_architect_profile.py` (B.4) | 23/23 |
| Backend v0.1 baseline | 38/38 |
| Backend full suite | **214 passed, 19 skipped, 0 failed** |

**Expected end-of-session:** 214 + C.2 test count, 19 skipped (or higher if roofing tests have skip markers for missing fixtures), 0 failed. Every other line unchanged.

If anything regresses below baseline at any verification point, that's a §7 stop.

---

## 4. Constraints

### 4.1 — Sacred files (do not modify)

- All TracePoint sources at `tracepoint_port/TracePoint/` (read-only reference)
- Phase 1 frontend HTML and all frontend test files
- All v0.2 ported files (`config.py`, `pdf_engine.py`, `zone_filter.py`, `context.py`, `dispatch_gate.py`, `roofing_spec_database.py`, `test_pdf_engine.py`, `test_dispatch.py`)
- All B.1/B.2/B.3/B.4 ported files
- C.1 ported file (`backend/core/trade_module.py`) and its appendix doc (`backend/CROSS_TRADE_INTEGRATION_NOTES.md`)
- `backend/core/__init__.py` (kept empty)
- `backend/seeds/*` — vocabulary.py may IMPORT from these but does not modify them
- `shared/bidset_record.py` (v0.2.1 ticket scope)
- `dispatch_gate.py` — C.2 does NOT wire roofing_module into dispatch_gate's call sites. That's later.
- All `MARCH_ORDERS_*.md`, `STEP_*.md`, `DISCOVERED_ISSUES.md`, `V0_2_VALIDATION.md`, observation/diagnostic docs
- `CLAUDE.md` — NOT edited by C.2 (C.1 already corrected the §5 C.1 paragraph; no C.2-specific edits are needed unless §5 C.2 needs alignment)

### 4.2 — Do not expand scope

- DO NOT port FastAPI route handlers from `server/routes/trade.py` (only `build_trade_input()` helper)
- DO NOT port any other route file
- DO NOT activate roofing_module in dispatch_gate or anywhere else in the call graph
- DO NOT build a glazing module (C.3)
- DO NOT solve the cross-trade integration questions from C.1's appendix (C.4)
- DO NOT add new dependencies. All imports should resolve from existing backend dependencies.
- DO NOT modify any seed file (vocabulary.py CONSUMES seeds; doesn't modify them)
- DO NOT migrate `BidsetRecord` (v0.2.1)
- DO NOT fix D-4, D-5, or D-6 (separate work)
- DO NOT add features "while we're in there"
- DO NOT touch frontend code

### 4.3 — Do not reinvent

- DO NOT change any TracePoint regex, vocabulary mapping, calibration threshold, dataclass field, or function signature "for clarity"
- DO NOT change quantity derivation logic
- DO NOT change scope detection thresholds
- DO NOT replace `dataclasses` with anything else
- DO NOT reorganize the file structure (vocabulary stays one file even though it's 575 lines; roofing_module stays one file)
- DO NOT change the `build_trade_input()` function body — only relocation is permitted, not redesign

### 4.4 — Karpathy procedure (held on substance)

- Read first (full reads). State which files were read in the final gate report.
- Verbatim copy. `diff = 0` for vocabulary.py and roofing_module.py and all test files.
- For `build_trade_input()`: function body byte-identical, only file location and minimal import-list adaptation permitted (and explicitly called out in the gate report).
- Sacred floors held at every verification point.
- §7 stops surface Discovered Issues; do not silently resolve.

### 4.5 — Autonomous execution

Same pattern as B.2+B.3 / B.4 / C.1. Steps C.2.0 through C.2.6 run in one session. Substantive gates only. ONE final gate report at the end.

---

## 5. Step List

### Step C.2.0 — Pre-flight

**Read:** This march orders document end-to-end. `CLAUDE.md` §6 (hard guardrails refresh). `backend/TRACEPOINT_DISCOVERY.md` §3.10–3.12 (modules + server inventories) and §8.5 (C.2 spec if present).

**Verify (no writes):**
- All §1 source files exist and readable. Record SHA-1s.
- All §3 baseline counts match exactly via `pytest backend/tests/ -q` and `node` test runners.
- Working tree clean (or known-stash-pattern). If stash needed: `git stash push -u -m "C.2 pre-flight: stash docs"`.
- Branch state: continue on `phase2-v0.3-C1-trade-module-interface` (carries C.1) and add C.2 commits to it, OR branch fresh as `phase2-v0.3-C2-roofing-module` from `23a459c`. **Recommended: branch fresh** — C.2 is conceptually distinct from C.1 (behavior-bearing trade module vs Protocol contract), and the C.1 branch should stay as the Protocol-only deliverable. Same naming convention as B.1/C.1.
- **CRITICAL:** verify `backend/CROSS_TRADE_INTEGRATION_NOTES.md` is NOT in working-tree mods (it should be committed as part of C.1). If it IS uncommitted, that's a §7 stop — C.1 didn't seal cleanly.

**Internal gate:** Pre-conditions green. Baseline recorded. Branch and stash in place.

**§7 stop only if:** baseline mismatch, source file missing, working tree won't clean, C.1 artifacts uncommitted.

### Step C.2.1 — Discovery: enumerate roofing tests in TracePoint

**Read:** Run `ls tracepoint_port/TracePoint/tests/` and identify all test files matching:
- `test_*roofing*.py`
- `test_vocabulary.py` (if exists)
- `test_build_trade_input.py` or `test_trade_input*.py` (if exists)

**Record:** For each file found:
- Full path
- Line count
- SHA-1
- Imports (grep `^import` and `^from`)
- Approximate test count (grep `^def test_` or `^    def test_`)

**Internal gate:** Test file inventory complete. Recorded for use in Steps C.2.4 and C.2.6.

**§7 stop only if:** zero roofing tests found in TracePoint (would be a discovery surprise — paper describes roofing module testing in §4)

### Step C.2.2 — Read all production source files end-to-end

**Read in full:**
- `tracepoint_port/TracePoint/modules/roofing/vocabulary.py` (575 lines)
- `tracepoint_port/TracePoint/modules/roofing/roofing_module.py` (434 lines)
- `tracepoint_port/TracePoint/server/routes/trade.py` (229 lines — read the WHOLE file to understand `build_trade_input()` in context, even though only the helper itself ports over)

**Verify (no writes):**
- `vocabulary.py` imports: record. Likely candidates per discovery: stdlib + possibly `from data.roof_assemblies import ...` (which maps to `from seeds.roof_assemblies import ...` in Huckleberry — same character edit pattern as v0.2's dispatch_gate). Confirm what's actually there.
- `roofing_module.py` imports: record. Expected: stdlib + `from core.trade_module import TradeModule, TradeModuleInput, TradeModuleOutput` + `from modules.roofing.vocabulary import ...` (which becomes `from core.roofing_vocabulary import ...` or similar — the vocabulary module's home in Huckleberry is a path-edit decision).
- `build_trade_input()`: identify the function definition (line range), its private helpers (any function called only by build_trade_input that's also in trade.py), its imports (the subset trade.py needs vs the subset build_trade_input alone needs), and its return type.

**Path-edit decisions to record at this step (do not execute yet):**
1. `modules/roofing/vocabulary.py` → where in `backend/`? Recommend `backend/core/roofing_vocabulary.py` (keeps it co-located with roofing_module.py in flat core/, matches existing seeds/ flat layout).
2. `modules/roofing/roofing_module.py` → `backend/core/roofing_module.py`.
3. `server/routes/trade.py::build_trade_input` → `backend/core/trade_input_builder.py` (extracted helper, deliberate adaptation per §2).
4. Import path edits required: `from modules.roofing.vocabulary` → `from core.roofing_vocabulary`. Any `from data.*` → `from seeds.*` (same as v0.2 pattern). Any other `from server.*` or `from modules.*` references in build_trade_input → must be resolved by extraction or cleanup.

**Expected diff vs source:**
- `vocabulary.py`: zero or N same-character import edits (N = count of `from data.*` lines), recorded at this step
- `roofing_module.py`: same-character import edits (vocabulary module path + any `from data.*`)
- `trade_input_builder.py`: NEW file (not a one-to-one port), function body byte-identical to TracePoint's `build_trade_input` body

**Internal gate:** All imports recorded. Path-edit plan recorded. Public surface of all three files known.

**§7 stop only if:**
- Any unexpected `from server.*` or `from modules.*.something_else` import that would force pulling in additional files
- `build_trade_input()` is FastAPI-coupled in ways extraction can't cleanly resolve
- vocabulary or roofing_module imports anything from a Phase B.4 module that's gated off (architect_profile activation, storage activation)

### Step C.2.3 — Failing test floor for C.2

**Write:** Copy each test file identified in Step C.2.1 from `tracepoint_port/TracePoint/tests/` to `backend/tests/`. Pure copies, verbatim. No edits.

For each test file, also apply the import path edits identified in Step C.2.2 IF AND ONLY IF the import paths in the test file mirror those of production code (e.g., `from modules.roofing.vocabulary` → `from core.roofing_vocabulary`). These are mechanical, not behavioral, changes — same pattern as v0.2's dispatch_gate import edits. Record exactly which test files needed which edits.

**Run:**
```
pytest backend/tests/test_<roofing-tests>.py -v
pytest backend/tests/ --ignore=backend/tests/test_<roofing-tests>.py -q
```

**Expected:** All new C.2 tests fail with `ModuleNotFoundError: No module named 'core.roofing_vocabulary'` (and/or `core.roofing_module`, `core.trade_input_builder`). Rest of suite holds at 214 passed, 19 skipped, 0 failed.

**Internal gate:** Test files in place. ImportError on missing production modules. Sacred floor + B.1/B.2/B.3/B.4/C.1 unchanged.

**§7 stop only if:** non-ImportError test failure (would indicate test files reference something else not yet ported), OR sacred floor regression elsewhere.

### Step C.2.4 — Verbatim port of three production files

**Write (in this order, because of import dependencies):**

1. `backend/core/roofing_vocabulary.py` — copy from `tracepoint_port/TracePoint/modules/roofing/vocabulary.py`. Apply ONLY the import-path edits identified in Step C.2.2 (likely `from data.*` → `from seeds.*`). NO other changes.

2. `backend/core/roofing_module.py` — copy from `tracepoint_port/TracePoint/modules/roofing/roofing_module.py`. Apply ONLY the import-path edits (`from modules.roofing.vocabulary` → `from core.roofing_vocabulary`, plus any `from data.*` → `from seeds.*`). NO other changes.

3. `backend/core/trade_input_builder.py` — NEW file. Contents:
   - Necessary imports (subset of trade.py's imports needed by build_trade_input + helpers)
   - `build_trade_input()` function — body byte-identical to TracePoint
   - Any private helpers it depends on, byte-identical
   - NO FastAPI imports (decorator, request/response objects)
   - NO route handlers

**Verify:**
```
# roofing_vocabulary.py
diff <(sed 's/from data\./from seeds./g' tracepoint_port/TracePoint/modules/roofing/vocabulary.py) backend/core/roofing_vocabulary.py
# Expected: zero output (the sed expression produces what backend should look like)

# roofing_module.py
diff <(sed -e 's|from modules\.roofing\.vocabulary|from core.roofing_vocabulary|g' -e 's|from data\.|from seeds.|g' tracepoint_port/TracePoint/modules/roofing/roofing_module.py) backend/core/roofing_module.py
# Expected: zero output

# trade_input_builder.py — function body comparison
# Extract build_trade_input function body from both files, diff
diff <(sed -n '/^def build_trade_input/,/^def [a-z]\|^class /p' tracepoint_port/TracePoint/server/routes/trade.py | head -n -1) <(sed -n '/^def build_trade_input/,/^def [a-z]\|^class /p' backend/core/trade_input_builder.py | head -n -1)
# Expected: zero output (function body identical, only surrounding file differs)
```

**Record SHA-1s** of all three new files for the gate report.

**§7 stop only if:** any `diff` produces unexpected output (output indicating non-import-edit changes). Acceptable diff output for vocabulary and roofing_module is exactly the recorded same-character import edits and nothing more.

**Run:**
```
pytest backend/tests/ -v
```

**Expected:** All C.2 tests now pass. Full backend suite: 214 + C.2 count, 19 skipped (or +N if roofing tests have skip markers), 0 failed.

**Internal gate:** All three production files in place with verified-minimal edits. C.2 tests 100% green. Full backend suite green.

**§7 stop only if:** any test failure or sacred regression beyond the new C.2 test additions.

### Step C.2.5 — Final regression sweep

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

**Expected:** Backend at 214 + C.2 count passing, 19+ skipped, 0 failed. Frontend every suite at exact baseline.

**Internal gate:** Every line of §3 baseline preserved or improved. New entries (C.2 test files) at 100%.

**§7 stop only if:** any regression at all from §3 baseline.

### Step C.2.6 — Commit + final gate report

**Write (commit only, no code):**
```
git add backend/core/roofing_vocabulary.py backend/core/roofing_module.py backend/core/trade_input_builder.py backend/tests/test_*.py
git commit -m "Phase C.2: Port TracePoint roofing module verbatim (vocabulary + module + build_trade_input helper)"
```

**Then:** `git stash pop` to restore documentation files.

Verify post-pop: `pytest backend/tests/ -q` still at 214 + C.2 count / 19+ / 0.

**Produce final gate report** in standard format:

```
=== Phase C.2 Session Report — <date> ===

STEPS COMPLETED: C.2 — verbatim port of roofing module (vocabulary.py + roofing_module.py + extracted build_trade_input helper) and all roofing tests.

FILES CHANGED:
  backend/core/roofing_vocabulary.py             NEW (575 lines, sha1 <hash>)
                                                  Edits vs source: <N> import-path same-character edits (from data.* → from seeds.*)
  backend/core/roofing_module.py                 NEW (434 lines, sha1 <hash>)
                                                  Edits vs source: <N> import-path same-character edits (from modules.roofing.vocabulary → from core.roofing_vocabulary, etc.)
  backend/core/trade_input_builder.py            NEW (~90 lines, sha1 <hash>)
                                                  Extracted from server/routes/trade.py per march orders §2 — function body byte-identical to TracePoint's build_trade_input(); FastAPI route decorator/imports excluded.
  backend/tests/test_<roofing tests>.py          NEW (one file per test source identified in C.2.1)
                                                  Edits: import-path same-character only (mirror of production edits)

DEPENDENCIES: pyproject.toml unchanged. No new deps.

PATH-EDIT LOG (verbatim-port deviations, all same-character):
  vocabulary.py      <list each edit, e.g., "line 12: 'from data.roof_assemblies' → 'from seeds.roof_assemblies'">
  roofing_module.py  <list each edit>
  trade_input_builder.py  N/A — new file extraction, see §2 of march orders
  test files         <list each>

FILES NOT CHANGED (sacred):
  All TracePoint sources (read-only)
  Phase 1 frontend
  v0.2/B.1/B.2/B.3/B.4/C.1 ported files (none touched)
  backend/core/__init__.py (still empty)
  backend/seeds/* (consumed by vocabulary.py, never modified)
  shared/bidset_record.py
  dispatch_gate.py — roofing_module NOT activated; remains unwired per §4.2
  All other docs

TESTS:
| Suite                                 | Before  | After     | Status |
|---------------------------------------|---------|-----------|--------|
| Frontend run_tests.js                 | 107/107 | 107/107   | sacred |
| Frontend spotchecks (4)               | all     | all       | sacred |
| Frontend mutation_test_step11.js      | 8/8     | 8/8       | sacred |
| Backend test_pdf_engine.py            | 40/40   | 40/40     | sacred |
| Backend test_dispatch.py              | 34+19sk | 34+19sk   | sacred |
| Backend test_filter_pipeline.py       | 27/27   | 27/27     | sacred |
| Backend test_geometry_matrix.py       | 36/36   | 36/36     | sacred |
| Backend test_polygon_scorers.py       | 16/16   | 16/16     | sacred |
| Backend test_architect_profile.py     | 23/23   | 23/23     | sacred |
| Backend v0.1 baseline                 | 38/38   | 38/38     | sacred |
| Backend test_<roofing tests>.py       | -       | <N>/<N>   | C.2 NEW |
| Backend full suite                    | 214     | 214 + N   | +N passing |

REGRESSIONS: none

KARPATHY DISCIPLINE:
  Read first: <list of files read end-to-end with line counts; sum>.
  Failing test floor: C.2.3 produced expected ModuleNotFoundError before production code landed.
  Minimum implementation: pure verbatim copies for vocabulary.py and roofing_module.py with same-character import edits only. trade_input_builder.py is an extracted-helper adaptation per march orders §2 with function body byte-identical to TracePoint.
  100% green floor: all sacred suites unchanged at every checkpoint.

DISCOVERED ISSUES: <none, OR D-7+ if any surfaced>

EXECUTION DETAIL:
  Branch: phase2-v0.3-C2-roofing-module (NEW; created from 23a459c per march orders §5 C.2.0 recommendation).
  Pre-flight stash: stash@{0}: C.2 pre-flight: stash docs. Popped at end.
  C.2 commit: <SHA> "Phase C.2: Port TracePoint roofing module verbatim..."
  Stash list at end: empty.

git log (current branch):
  <C.2 SHA>   Phase C.2: ...
  23a459c     Phase C.1: Port TracePoint trade_module.py Protocol verbatim, add cross-trade integration notes
  a8ee936     Phase B.4: ...
  70c1835     Phase B.3: ...
  4af872e     Phase B.2: ...
  1c3fde4     Phase B.1: ...
  441896a     Phase 2 v0.2: Port TracePoint dispatch gate

PHASE C.2 COMPLETE: First behavior-bearing trade module ported. Roofing module
implements the C.1 Protocol contract. C.3 (glazing module against the same
contract) is now unblocked and is the validation that the contract generalizes.

NEXT STEP: Phase C.3 — port glazing module against the same Protocol contract.
Per discovery, TracePoint may not have a fully-built glazing module yet — pre-flight
will verify what exists. If glazing source is incomplete in TracePoint, C.3
becomes a different shape of work (build-against-contract instead of port).
That's a planning conversation, not autonomous execution.

AWAITING APPROVAL: yes — Daniel approves C.2 commit and confirms C.3 planning may begin.
```

---

## 6. §7 Stop Conditions

Stop and surface as Discovered Issue, ask Daniel:

1. **Diff produces unexpected output** at C.2.4 (anything beyond the recorded same-character import edits)
2. **SHA-1 mismatch** for files that should be byte-identical (vocabulary content / roofing_module content excluding import lines / build_trade_input function body)
3. **Any sacred floor count regresses** at any verification point
4. **Unexpected import** in any source file that requires pulling in additional unported code
5. **`build_trade_input()` cannot be cleanly extracted** from the FastAPI route file
6. **No roofing tests found** in TracePoint (discovery would have missed something significant)
7. **Test count significantly different from estimate** (the estimate is empirical from C.2.1, so significant means orders-of-magnitude off)
8. **Production file outside the 3 + N test target files gets modified** by accident
9. **vocabulary.py or roofing_module.py imports from a Phase B.4 module** that's gated off (architect_profile activation, storage activation) — would force the activation question to be answered now instead of in Phase D/E
10. **C.1 artifacts uncommitted** at pre-flight (C.1 didn't seal cleanly)

§7 stops are documentation actions. Document in `backend/DISCOVERED_ISSUES.md` as next available D-number, pause, ask Daniel.

---

## 7. Done Definition

This session is done when:

- [ ] `backend/core/roofing_vocabulary.py` ported with same-character import edits documented
- [ ] `backend/core/roofing_module.py` ported with same-character import edits documented
- [ ] `backend/core/trade_input_builder.py` extracted with function body byte-identical to TracePoint
- [ ] All roofing tests (count empirical from C.2.1) ported with mirroring import edits
- [ ] All ported tests 100% green
- [ ] All sacred floors held at every verification point
- [ ] No new dependencies
- [ ] No changes to dispatch_gate's call sites (roofing_module not wired)
- [ ] No D-tickets opened, OR all open ones resolved/deferred
- [ ] Single commit on the new branch
- [ ] Stash popped cleanly
- [ ] Final gate report produced

When done, **C.2 is sealed.** Next: C.3 (glazing module against same contract). C.3 may be a different shape of work depending on what glazing source exists in TracePoint — that's a planning conversation when the time comes.

---

**End of MARCH_ORDERS_C_2.md. Awaiting Daniel's review and Claude Code execution brief.**
