# Phase C.3c-build — March Orders

**Target:** Build a rough `GlazingModule` against the C.1 `TradeModule` Protocol, consuming the C.3b `glazing_vocabulary`. Schedule-first with elevation/plan reconciliation. Concrete field set per Daniel's 2026-04-28 spec. Vault-rule applied at sealing.

**Authored:** 2026-04-28
**Authority:** Daniel (POC owner), 2026-04-28 spec verbatim in §1 of this document
**Predecessor:** C.3b (commit `eb49a08` on branch `phase2-v0.3-C3b-glazing-vocabulary`, including D-8 follow-up). Sacred floor: backend 214/19/0, frontend 107 + spotchecks + 8/8 mutations. All Phase B + C.1 + C.2 + C.3b + D-8 work pushed to remote 2026-04-28.
**Source authority:** **Daniel's spec** (§1 of this document). NOT a TracePoint port — TracePoint has no glazing module. NOT a from-scratch invention either — built against existing parked seeds + C.3b vocabulary, following Daniel's domain-knowledge spec for what GlazingModule should attempt at the rough level.
**Discipline:** First Huckleberry-original trade module. "Rough ship + vault-rule" pattern per CLAUDE.md §3 Decision 15 (extended 2026-04-28 to cover trade modules). No tuning in this session. No correctness optimization. The point is to ship a module that runs and produces output of useful shape; tuning happens after C.3c-run sweep produces data.
**Expected wall-clock:** ~75–105 minutes.

---

## 0. The Discipline Frame for This Phase

This is the first Huckleberry-original trade module. Every prior trade-module-shaped artifact (RoofingModule, roofing_vocabulary, the trade Protocol itself) was a verbatim port from TracePoint with byte-identical verification. C.3c-build has no upstream source. The verification standard shifts from "byte-identical to TracePoint" to "satisfies the contract + implements Daniel's spec + produces output."

**Rough-ship discipline (CLAUDE.md §3 Decision 15):**

- The module ships ROUGH. Output may be incomplete, may over-pull (+20%, +50%, more), may under-pull, may misclassify. That is acceptable at this phase.
- The module gets vault-ruled at sealing. Future tuning is a dedicated session with `core/` frozen.
- This session does NOT tune. If a gap is obvious during build, it gets named in the module's docstring as a known limitation; it does NOT get fixed in this session.
- "While we're in there" additions are forbidden, same as every prior phase.

**The C.3c-run sweep (separate, future session) will provide the data that informs whether tuning is needed.** Until that sweep runs and produces output, all tuning impulses are speculation. C.3c-build's job is to make the sweep possible, not to optimize for sweep results.

---

## 1. Daniel's Spec (Verbatim, 2026-04-28)

The following is the design source for C.3c-build. Quoted verbatim from the conversation that authorized this phase. It is the authoritative scope for what GlazingModule attempts.

> "Simplest contract for glazing module is find door/window/storefront/glazing schedule then find exterior elevations and floor plan per level look for glazing verbiage and symbols match schedule naming scheme count those put in table in table define what each item thats glazing verbiage with sqft, system, glass type, manufacture, color/finish, width in feet and inches to the nearest '.0000', height in feet and inches to the nearest '.0000'. same with doors on glazing schedules there are tables with locations especially for doors. doors are door type, frame type, manufacture, kind of door, material, glass door, finish of door, location of door, height and width in feet and inches to the nearest '.oooo'. storefront same as windows, but system type, manufacturer, sqft per segment, door in that segment, double door in segment, location, finish, height and width in feet and inches to the nearest '.oooo'. if no schedule can be found search from title page or search on various pages most architects do not do things uniformly this is why vague instructions are the starting point."

Translated into a structured field set the module produces:

**Per glazing-window item:**
- mark (e.g., W-1, W-A)
- count (from elevation/plan reconciliation)
- system (storefront / aluminum-fixed / aluminum-operable / vinyl / etc., from vocabulary)
- glass_type (tempered / laminated / IGU / Low-E / spandrel / etc.)
- manufacturer (aliased through vocabulary's MANUFACTURERS table)
- color_finish
- width_ft (decimal feet to .0000 precision, e.g., 4.0833 for 4'-1")
- height_ft (decimal feet to .0000 precision)
- sqft (width × height, .0000 precision)
- location (text, e.g., "rear elevation, bay 3")
- source_page (where the schedule entry was found)
- confidence (vocabulary-match confidence, simple float)

**Per door item:**
- mark
- count
- door_type (HM / aluminum-storefront / wood / etc.)
- frame_type (HM / aluminum / wood / etc.)
- manufacturer
- door_kind (single / pair / overhead / etc.)
- material
- glass_door (bool — has glazing or solid)
- finish
- location
- width_ft (.0000)
- height_ft (.0000)
- source_page
- confidence

**Per storefront-segment item:**
- mark (e.g., SF-1)
- count
- system_type (captured / SSG / etc.)
- manufacturer
- sqft_per_segment (.0000)
- door_in_segment (bool)
- double_door_in_segment (bool)
- location
- finish
- width_ft (.0000)
- height_ft (.0000)
- source_page
- confidence

**Search strategy (per spec):**
1. **Schedule-first.** Look for door/window/storefront/glazing schedule sheets. Schedule keywords + sheet titles are the primary signal. Pull mark + size + system + glass + finish + manufacturer from schedule rows.
2. **Elevation/plan reconciliation.** Find exterior elevations and floor plans. Look for glazing verbiage and mark callouts (W-1, SF-1, etc.). Count occurrences. Reconcile counts against schedule.
3. **Title-page fallback.** If no schedule sheet identified by keyword, search title page for sheet index entries that name glazing schedules ("A-601 DOOR SCHEDULE" etc.).
4. **Various-pages fallback.** If neither schedule nor title-page reveals the schedule location, scan all pages for table-shaped content matching schedule patterns (mark column + size column + manufacturer column).

The fallback chain matters because **most architects do not do things uniformly** — Daniel's wording. Vagueness in the search heuristics is intentional; tightening the heuristics is tuning, not building.

---

## 2. Goal Statement

**C.3c-build ships when:**

1. `backend/core/glazing_module.py` exists, implementing the `TradeModule` Protocol from C.1 (`backend/core/trade_module.py`)
2. `GlazingModule.run(input: TradeModuleInput) -> TradeModuleOutput` is callable; reads `input.tables` and/or `input.interior_text_blocks`; produces output of the field shape in §1
3. The output object satisfies whatever shape `TradeModuleOutput` defines in C.1; if the C.1 `TradeModuleOutput` cannot carry the §1 field set without extension, the contract is extended ADDITIVELY (own commit, same shape as C.3b's `tables` field addition) before the module is built
4. Module imports cleanly: `python -c "from core.glazing_module import GlazingModule; print('ok')"`
5. Module instantiates and runs cleanly on at least one input — minimum: a stub `TradeModuleInput` constructed in code (NOT a real bidset run; the sweep is a future phase). Smoke test only.
6. `glazing_module.py` is added to the vault-ruled list in CLAUDE.md §3 Decision 15
7. Sacred floor preserved at every verification point (214/19/0)
8. No new dependencies
9. RoofingModule (C.2) still passes its import-resolution smoke test — the contract extension (if needed) is additive and roofing ignores any new field
10. Single commit at end (or two: contract extension + module build, depending on whether contract extension is needed)

**C.3c-build explicitly does NOT ship:**

- Behavior validation against any real bidset (that's the sweep — separate phase)
- Tuning of glazing_vocabulary based on what the module surfaces during build (vault rule)
- Tuning of roofing_module based on observations during build (vault rule)
- Activation in `dispatch_gate.py` (Phase D/E)
- Tests for module behavior beyond the smoke test (sweep produces the behavior data; tests are written from sweep observations, not in advance)
- Modification to the parked glazing seeds
- Any field beyond the §1 spec
- Any heuristic beyond the §1 search strategy
- v0.2.1 work
- Debug module port (that's C.5, next phase)
- Frontend integration

---

## 3. Sacred Floor

| Suite | Count |
|---|---:|
| Frontend `run_tests.js` | 107/107 |
| Frontend spotchecks (4) | all pass |
| Frontend `mutation_test_step11.js` | 8/8 mutations caught |
| Backend `test_pdf_engine.py` | 40/40 |
| Backend `test_dispatch.py` | 34 passed, 19 skipped |
| Backend `test_filter_pipeline.py` | 27/27 |
| Backend `test_geometry_matrix.py` | 36/36 |
| Backend `test_polygon_scorers.py` | 16/16 |
| Backend `test_architect_profile.py` | 23/23 |
| Backend v0.1 baseline | 38/38 |
| Backend full suite | **214 passed, 19 skipped, 0 failed** |

End of session: 214/19/0 unchanged. C.3c-build adds no test files. The verification floor is sacred-floor regression + import-resolution + module-instantiation smoke test.

---

## 4. Constraints

### 4.1 — Authorized to modify

- `backend/core/trade_module.py` — ONLY if §5 step C.3c-build.2 confirms that `TradeModuleOutput` cannot carry the §1 field set without extension. If extension is needed: SINGLE additive change (one or more new optional fields with default values), own commit, documented as deliberate adaptation. No other changes.
- `CLAUDE.md` — extend §3 Decision 15's vault-ruled list to include `backend/core/glazing_module.py` at sealing.

### 4.2 — Authorized to create

- `backend/core/glazing_module.py` — NEW file. Implements the spec in §1.

### 4.3 — Sacred (do not modify)

- All TracePoint sources at `tracepoint_port/TracePoint/`
- Phase 1 frontend HTML and all frontend tests
- All v0.2 / B.1 / B.2 / B.3 / B.4 ported files
- C.1 ported file (`trade_module.py` — see §4.1 for the conditional exception)
- C.2 ported files (`roofing_vocabulary.py`, `roofing_module.py`, `trade_input_builder.py`)
- C.3b built file (`glazing_vocabulary.py`) — vault-ruled
- `backend/core/__init__.py` (empty)
- `backend/seeds/glazing_assemblies.py` and `glazing_materials.py` — parked
- All other seed files
- `shared/bidset_record.py`
- `dispatch_gate.py` activation gates
- All `MARCH_ORDERS_*.md`, `STEP_*.md`, `DISCOVERED_ISSUES.md`, `V0_2_VALIDATION.md`, `VALIDATION_LEDGER.md`, `HANDOFF_*.md`, observation/diagnostic docs
- `PROJECT_CLAUDE.md` (will be updated AFTER this phase ships, in a separate brief; not in C.3c-build's scope)

### 4.4 — Do not expand scope

- DO NOT add fields beyond §1 spec
- DO NOT add search heuristics beyond §1 strategy
- DO NOT tune vocabulary based on what surfaces during build
- DO NOT tune roofing_module
- DO NOT add validation against real bidsets in this session
- DO NOT activate the module anywhere
- DO NOT add new dependencies
- DO NOT add features "while we're in there"
- DO NOT touch frontend code
- DO NOT precompute "improvements" the sweep hasn't asked for

### 4.5 — Do not optimize for correctness

This is the most counterintuitive constraint of the session, so it gets its own subsection. The point of C.3c-build is to ship a module that runs. NOT a module that produces correct output.

If during build you (Claude Code) think "this regex would catch more cases" — STOP. That's tuning. Note the limitation in the module docstring; do not refine the regex.

If during build you think "this fallback is too vague" — STOP. The vagueness is intentional per Daniel's spec. Vague heuristics are the starting point because real bidsets are not uniform. Tightening them in advance bakes in assumptions about uniformity that don't hold.

If during build you think "the schedule parser should handle edge case X" — STOP. Edge case X may or may not exist in real bidsets; we don't know yet. The sweep tells us. Until the sweep runs, every edge-case handler is speculation.

The module ships rough. +20% over-pull is fine. +50% over-pull is fine. Under-pull is fine. Misclassification is fine. The sweep tells us where the module needs work. That work happens later, in a separate session, with `core/` frozen, vault-rule observed.

### 4.6 — Karpathy procedure (held on substance)

- Read first: C.1 contract (`trade_module.py`), C.2 module for shape reference (`roofing_module.py`), C.3b vocabulary (`glazing_vocabulary.py`), Daniel's spec (§1 of this document, end-to-end)
- Failing test floor: smoke test — write a minimal "module imports and runs on stub input" assertion before writing the module body. The assertion fails with ImportError until the module exists, then with implementation errors until the body is written, then passes when body is complete.
- Minimum implementation: §1 spec only, nothing more
- 100% green floor: 214/19/0 holds at every verification point

### 4.7 — Autonomous execution

Same pattern as B.4 / C.2 / C.3b. Steps run sequentially in one session. ONE final gate report. §7 stops only.

---

## 5. Step List

### Step C.3c-build.0 — Pre-flight

**Read end-to-end:**
- This march orders document, including §1 spec verbatim
- `CLAUDE.md` §3 Decision 15 (vault rule, current text including the 2026-04-28 trade-module extension)
- `CLAUDE.md` §6 (hard guardrails refresh)

**Verify (no writes):**
- Branch state: branch fresh as `phase2-v0.3-C3c-glazing-module` from `eb49a08` (C.3b head). C.3c-build is conceptually distinct from C.3b (vocabulary build vs module build).
- Sacred floor: 214/19/0 backend, frontend baseline
- Working tree clean (or stash)
- Source files exist and readable: `backend/core/trade_module.py`, `backend/core/roofing_module.py`, `backend/core/glazing_vocabulary.py`

**Internal gate:** Pre-conditions green. Branch + stash in place.

**§7 stop only if:** baseline mismatch, source files missing, working tree won't clean.

### Step C.3c-build.1 — Read source files end-to-end

**Read in full:**
- `backend/core/trade_module.py` — confirm `TradeModuleInput` shape (including the `tables` field added in C.3b), confirm `TradeModuleOutput` shape, confirm Protocol method signature
- `backend/core/roofing_module.py` — for module shape reference. The glazing module's overall structure (class name, init, `run()` method, helpers, docstring conventions) should mirror RoofingModule for consistency.
- `backend/core/glazing_vocabulary.py` — confirm public surface (COMPONENTS, SYSTEMS, HARDWARE_SETS, MANUFACTURERS, etc., plus GLAZING_VOCABULARY aggregate)
- §1 of this document, again, with attention to the field set

**Decisions to record at this step:**

1. **Output schema fit.** Does the C.1 `TradeModuleOutput` carry the §1 field set as-is, or does it need extension? If extension needed, what fields, what types?
2. **Helper function decomposition.** §1 implies several distinct sub-tasks (find schedules, parse schedule rows, find elevations, count callouts, reconcile, dimension parsing). What helpers does the module need? Decide structure before writing.
3. **Dimension parsing helper.** Converting "4'-1"" or "4 ft 1 in" or "4'-1 1/2"" to decimal feet at .0000 precision is its own helper (likely shared utility). Does anything in `core/` already do this? If yes, use it. If not, the helper goes in glazing_module.py for now (vault-ruled with the module).

**Internal gate:** Output schema fit known. Helper decomposition decided. Dimension-parsing utility location decided.

**§7 stop only if:** the existing C.1 contract structurally cannot carry the §1 fields even with extension (would require redesigning the contract — out of scope, planning conversation needed).

### Step C.3c-build.2 — Extend TradeModuleOutput if needed (conditional)

**ONLY IF Step C.3c-build.1 determined that `TradeModuleOutput` needs extension to carry the §1 field set.**

If extension needed:
- Modify `backend/core/trade_module.py` to add ONLY the new optional fields with default values
- Field naming follows the §1 spec (e.g., `glazing_items: list[dict] | None = None`, `door_items: list[dict] | None = None`, `storefront_items: list[dict] | None = None`)
- Documented in commit message as deliberate adaptation per CLAUDE.md §3 Decision 15's "Contract evolution" clause
- Roofing module continues to work because new fields have defaults
- Own commit, named "C.3c-build (1/2): Extend TradeModuleOutput for glazing-shaped output"

If extension NOT needed: skip this step; proceed to C.3c-build.3 with single-commit shipping.

**Verify:** sacred floor unchanged after extension; RoofingModule imports cleanly.

**Internal gate:** Contract carries the §1 fields (whether already or after extension).

**§7 stop only if:** more than 3 new fields are needed (would suggest the §1 spec doesn't fit the existing contract shape, which is a deeper architecture question).

### Step C.3c-build.3 — Build glazing_module.py

**Write:** Create `backend/core/glazing_module.py`. Structure follows `roofing_module.py`'s shape.

The file's logical structure (illustrative; exact code is Claude Code's call subject to constraints):

```python
"""
GlazingModule — rough first-pass trade module for glazing scope.

Phase: C.3c-build (2026-04-28)
Source spec: MARCH_ORDERS_C_3c_build.md §1 (Daniel's spec, verbatim)
Vault rule: applied at sealing per CLAUDE.md §3 Decision 15.

The module ships ROUGH. Output may be incomplete, over-pull, under-pull,
misclassify. That is acceptable at this phase. Tuning happens in dedicated
sessions with core/ frozen, after the C.3c-run sweep produces real-bidset
output.

Search strategy (per spec):
1. Schedule-first: door/window/storefront/glazing schedule sheets
2. Elevation/plan reconciliation
3. Title-page fallback
4. Various-pages fallback (most architects do not do things uniformly)

Field set (per spec):
- Glazing-window items: mark, count, system, glass_type, manufacturer,
  color_finish, width_ft (.0000), height_ft (.0000), sqft (.0000),
  location, source_page, confidence
- Door items: mark, count, door_type, frame_type, manufacturer, door_kind,
  material, glass_door, finish, location, width_ft (.0000), height_ft
  (.0000), source_page, confidence
- Storefront-segment items: mark, count, system_type, manufacturer,
  sqft_per_segment (.0000), door_in_segment, double_door_in_segment,
  location, finish, width_ft (.0000), height_ft (.0000), source_page,
  confidence

Known limitations (rough-ship):
- Schedule parsing assumes pdfplumber-style table extraction; rasterized
  schedules will not be parsed
- Mark naming is regex-matched from vocabulary; non-vocabulary marks may
  be missed or miscategorized
- Reconciliation between schedule and elevation counts may double-count
  on bidsets where the same mark appears in multiple schedule sections
- Dimension parsing handles "X'-Y\"" and "X ft Y in" but may not handle
  fractional inches with non-standard punctuation
- Confidence scores are simple vocabulary-match confidence, not
  domain-validated
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional

from core.trade_module import TradeModule, TradeModuleInput, TradeModuleOutput
from core.glazing_vocabulary import GLAZING_VOCABULARY


@dataclass
class GlazingModule:
    """Rough glazing trade module. See module docstring."""

    def run(self, input: TradeModuleInput) -> TradeModuleOutput:
        """
        Per spec: schedule-first → elevation/plan reconciliation → title-page
        fallback → various-pages fallback. Produces glazing/door/storefront
        items per the field set in module docstring.
        """
        # 1. Schedule-first: scan input.tables for schedule sheets
        schedules = self._find_schedules(input)
        
        # 2. Elevation/plan reconciliation: scan interior_text_blocks for
        #    glazing-verbiage marks and count
        elevation_counts = self._reconcile_elevations(input, schedules)
        
        # 3. If no schedules found, title-page fallback
        if not schedules:
            schedules = self._title_page_fallback(input)
        
        # 4. If still nothing, various-pages fallback
        if not schedules:
            schedules = self._various_pages_fallback(input)
        
        # 5. Synthesize items from schedules + elevation_counts
        glazing_items = self._build_glazing_items(schedules, elevation_counts)
        door_items = self._build_door_items(schedules, elevation_counts)
        storefront_items = self._build_storefront_items(schedules, elevation_counts)
        
        # 6. Return TradeModuleOutput per the (possibly extended) C.1 contract
        return TradeModuleOutput(
            trade_id="glazing",
            # ... fields per the contract ...
            glazing_items=glazing_items,
            door_items=door_items,
            storefront_items=storefront_items,
        )

    # Helper functions — kept private to the module, vault-ruled with it.
    
    def _find_schedules(self, input): ...
    def _reconcile_elevations(self, input, schedules): ...
    def _title_page_fallback(self, input): ...
    def _various_pages_fallback(self, input): ...
    def _build_glazing_items(self, schedules, counts): ...
    def _build_door_items(self, schedules, counts): ...
    def _build_storefront_items(self, schedules, counts): ...
    def _parse_dimension(self, text: str) -> float: ...  # converts "4'-1" → 4.0833
```

The illustrative shape above is a guide, not a contract. Claude Code implements the actual code, with these constraints:

- **Use `glazing_vocabulary.GLAZING_VOCABULARY` for all vocabulary lookups.** Do NOT hardcode keyword lists in glazing_module.py.
- **Search strategy follows §1 in order.** Schedule-first, then reconciliation, then fallbacks. Each step is a separate helper.
- **Helpers are private to the module** (`_find_schedules`, etc.). They are vault-ruled with the module.
- **Dimension parser handles the common cases** — "X'-Y\"", "X ft Y in", decimal — and falls back to None or raises a clear error for cases it doesn't handle. NOT a perfect parser. Roughness acceptable.
- **No external libraries** beyond what's already in `pyproject.toml`. No new dependencies.
- **Confidence scores are simple.** Vocabulary-match confidence (e.g., 0.9 for direct keyword match, 0.5 for fuzzy match, 0.2 for fallback inference). NOT calibrated; vault-ruled at this state.
- **Module docstring lists known limitations explicitly.** Same shape as the illustrative one above. This is part of "ship rough; document what's rough." Future tuning sessions read the docstring to know where to start.

**Smoke test:** create `backend/tests/test_glazing_module_smoke.py` with ONE test that imports the module, instantiates it, and runs it on a minimal stub `TradeModuleInput` constructed in code. The test verifies the call doesn't raise and returns a `TradeModuleOutput`. NOT a behavior test — purely "the module is reachable and the contract is satisfied."

This adds ONE test file with ONE test. Backend full-suite count goes from 214 to 215. The smoke test's role: gate that the module is wired correctly, NOT that it produces correct output.

**Verify:**
- `python -c "from core.glazing_module import GlazingModule; m = GlazingModule(); print(type(m))"`
- `pytest backend/tests/test_glazing_module_smoke.py -v` — passes
- `pytest backend/tests/ -q` — 215 passed, 19 skipped, 0 failed

**Internal gate:** Module imports, instantiates, runs on stub. All sacred floors held. RoofingModule still imports cleanly.

**§7 stop only if:**
- Module cannot be made to satisfy the contract without contract changes beyond what Step C.3c-build.2 authorized
- Sacred floor regresses
- Smoke test fails for a reason other than expected work-in-progress (e.g., vocabulary import fails — would mean glazing_vocabulary.py has a problem from C.3b that C.3b's verification missed)

### Step C.3c-build.4 — Apply vault rule to glazing_module.py

**Write:** Edit CLAUDE.md §3 Decision 15. Add `backend/core/glazing_module.py` to the "Vault-ruled retroactively (2026-04-28)" list — actually, since C.3c-build seals the module on 2026-04-28 same date, add it to a new "Vault-ruled at sealing (2026-04-28)" entry, OR extend the existing 2026-04-28 list with a sealing-date sub-note. Wording is Claude Code's call so long as the substantive effect is: glazing_module.py is now vault-ruled, future tuning is gated.

**Verify:** CLAUDE.md edit is single-section, no other text changed.

### Step C.3c-build.5 — Final regression sweep + commits + gate report

**Run:**
```
cd backend && pytest -v
node run_tests.js
node spotcheck_10b.js
node spotcheck_cricket.js
node spotcheck_durolast.js
node spotcheck_manufacturer.js
node mutation_test_step11.js
```

Expected: 215/19/0 backend (added smoke test), frontend at baseline.

**Commit (one or two depending on Step C.3c-build.2 outcome):**

If contract extension was needed (Step C.3c-build.2 fired):
```
# Commit 1/2: contract extension
git add backend/core/trade_module.py
git commit -m "Phase C.3c-build (1/2): Extend TradeModuleOutput for glazing-shaped output

Additive-only changes per CLAUDE.md §3 Decision 15 'Contract evolution' clause.
Adds: <list new fields>

RoofingModule unaffected (new fields have None defaults). Documented as
deliberate adaptation."

# Commit 2/2: module + smoke test + vault rule
git add backend/core/glazing_module.py backend/tests/test_glazing_module_smoke.py CLAUDE.md
git commit -m "Phase C.3c-build (2/2): Build rough GlazingModule per Daniel's 2026-04-28 spec, vault-rule applied

Module ships ROUGH per CLAUDE.md §3 Decision 15. Output may over-pull,
under-pull, or misclassify; correctness validation deferred to C.3c-run
sweep. Tuning happens in dedicated sessions with core/ frozen.

Implements:
- Schedule-first search strategy
- Elevation/plan reconciliation
- Title-page and various-pages fallbacks
- Glazing/door/storefront field set per spec
- Dimension parsing to .0000 precision

Vault rule applied: glazing_module.py added to CLAUDE.md §3 Decision 15
vault-ruled list. Future tuning sessions only.

Source spec: MARCH_ORDERS_C_3c_build.md §1, verbatim from Daniel's
2026-04-28 conversation.

Smoke test: test_glazing_module_smoke.py — module imports, instantiates,
runs on stub input without raising. NOT a behavior test."
```

If contract extension NOT needed:
```
git add backend/core/glazing_module.py backend/tests/test_glazing_module_smoke.py CLAUDE.md
git commit -m "Phase C.3c-build: Build rough GlazingModule per Daniel's 2026-04-28 spec, vault-rule applied
[ ... same body as 2/2 above ... ]"
```

**Then:** `git stash pop` if pre-flight stashed.

**Final gate report** in standard format. Single report.

```
=== Phase C.3c-build Session Report — <date> ===

STEPS COMPLETED: C.3c-build — first Huckleberry-original trade module
(GlazingModule), built per Daniel's 2026-04-28 spec (verbatim in march
orders §1). Vault rule applied at sealing.

FILES CHANGED:
  backend/core/glazing_module.py                NEW (<N> lines, sha1 <hash>)
                                                Implements TradeModule Protocol
                                                Schedule-first + elevation/plan + 2 fallbacks
                                                Field set per march orders §1
                                                Module docstring lists known limitations
  backend/tests/test_glazing_module_smoke.py    NEW (1 test)
                                                Smoke test only — not a behavior test
  CLAUDE.md                                     MODIFIED (§3 Decision 15: glazing_module.py added to vault-ruled list)
  backend/core/trade_module.py                  MODIFIED (conditional, only if §5 step C.3c-build.2 fired)
                                                Additive: <list fields if applicable>

DEPENDENCIES: pyproject.toml unchanged. No new deps.

FILES NOT CHANGED (sacred):
  All TracePoint sources
  Phase 1 frontend
  v0.2 / B.1 / B.2 / B.3 / B.4 / C.1 (modulo §4.1 conditional) / C.2 / C.3b ported and built files
  Parked seeds (glazing_assemblies.py, glazing_materials.py)
  All other seed files
  shared/bidset_record.py
  All other docs (MARCH_ORDERS_*, STEP_*, DISCOVERED_ISSUES, V0_2_VALIDATION,
    VALIDATION_LEDGER, HANDOFF_*, observation/diagnostic docs, PROJECT_CLAUDE.md)
  dispatch_gate.py — GlazingModule NOT activated; remains unwired

TESTS:
| Suite                                | Before  | After   | Status |
|--------------------------------------|---------|---------|--------|
| Frontend run_tests.js                | 107/107 | 107/107 | sacred |
| Frontend spotchecks (4)              | all     | all     | sacred |
| Frontend mutation_test_step11.js     | 8/8     | 8/8     | sacred |
| Backend test_pdf_engine.py           | 40/40   | 40/40   | sacred |
| Backend test_dispatch.py             | 34+19sk | 34+19sk | sacred |
| Backend test_filter_pipeline.py      | 27/27   | 27/27   | sacred |
| Backend test_geometry_matrix.py      | 36/36   | 36/36   | sacred |
| Backend test_polygon_scorers.py      | 16/16   | 16/16   | sacred |
| Backend test_architect_profile.py    | 23/23   | 23/23   | sacred |
| Backend v0.1 baseline                | 38/38   | 38/38   | sacred |
| Backend test_glazing_module_smoke.py | -       | 1/1     | C.3c-build NEW |
| Backend full suite                   | 214     | 215     | +1 smoke test |

REGRESSIONS: none

KARPATHY DISCIPLINE:
  Read first: <files read with line counts>
  Smoke test floor: test_glazing_module_smoke.py written before module body;
    failed with ImportError until module landed.
  Minimum implementation: §1 spec only, no expansion. Module docstring
    explicitly lists known limitations (rough-ship discipline).
  100% green floor: all sacred suites unchanged. Smoke test passes.
  Vault rule applied: glazing_module.py added to CLAUDE.md §3 Decision 15
    at sealing.
  No tuning: <list any tuning impulses that surfaced and were declined>

DISCOVERED ISSUES: <none, OR D-N+ if any surfaced>

EXECUTION DETAIL:
  Branch: phase2-v0.3-C3c-glazing-module (NEW; from eb49a08)
  Commits: <one or two SHAs>
  Stash: handled per pre-flight

git log: ...

PHASE C.3c-build COMPLETE: First Huckleberry-original trade module shipped
rough and vault-ruled. Module is ready for C.3c-run sweep (separate phase
after C.5 debug module port). C.5 march orders draft is the next planning
task.

AWAITING APPROVAL: yes — Daniel approves C.3c-build commit(s) and confirms
PROJECT_CLAUDE.md update + C.5 planning may begin.
```

---

## 6. §7 Stop Conditions

1. **Sacred floor regresses** at any verification point
2. **Module cannot satisfy the contract** even with the conditional Step C.3c-build.2 extension
3. **More than 3 new fields needed** on TradeModuleOutput (suggests deeper architecture question)
4. **Tuning impulses surface that don't fit "list as known limitation in docstring"** (e.g., a refactor of glazing_vocabulary that would cross the vault rule)
5. **Production file outside the 4 authorized targets gets modified**
6. **Vocabulary-side problem surfaces** during build (e.g., a key in glazing_vocabulary references something that doesn't exist) — would indicate a C.3b verification gap
7. **The dimension parser proves harder than expected** (e.g., bidsets use a notation neither the spec nor common patterns predict) — STOP, don't invent edge-case handlers, surface for next session

§7 stops are documentation actions. Surface; ask Daniel.

---

## 7. Done Definition

- [ ] `backend/core/glazing_module.py` exists, implements `TradeModule` Protocol, runs on stub
- [ ] Module docstring lists known limitations explicitly
- [ ] `backend/tests/test_glazing_module_smoke.py` exists with 1 passing smoke test
- [ ] CLAUDE.md §3 Decision 15 updated with glazing_module.py vault-ruled
- [ ] Sacred floors held
- [ ] No new dependencies
- [ ] No tuning of glazing_vocabulary or roofing_module
- [ ] No activation in dispatch_gate
- [ ] One or two commits on `phase2-v0.3-C3c-glazing-module` branch
- [ ] Final gate report produced

When done: **C.3c-build is sealed.** Module is vault-ruled. Next: PROJECT_CLAUDE.md update (separate brief), then C.5 debug module port (separate brief), then C.3c-run sweep (separate brief).

---

**End of MARCH_ORDERS_C_3c_build.md. Awaiting Daniel's review and Claude Code execution.**
