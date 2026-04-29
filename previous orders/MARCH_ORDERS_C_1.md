# Phase C.1 — March Orders

**Target:** Define the platform/trade boundary by porting TracePoint's `core/trade_module.py` Protocol and dataclass contract verbatim into the Huckleberry backend, and capture the Huckleberry-specific cross-trade integration cases that TracePoint's contract does not cover. C.1 is the foundation step of Phase C; C.2 (first concrete trade module) cannot start until the contract is in place.

**Authored:** 2026-04-27
**Authority:** Daniel (POC owner)
**Predecessor:** B.4 (commit `a8ee936` on branch `phase2-v0.3-B2-geometry-engine`). End-of-B.4 sacred floor: backend 214 passing / 19 skipped / 0 failing, frontend 107 + 4 spotchecks (7+4+8+14) + 8/8 mutations all unchanged.
**Source authority:** `tracepoint_port/TracePoint/` — read-only reference.
**Discipline:** Karpathy preserved on substance. Autonomous between substantive gates per the B.2/B.3/B.4 pattern. Daniel reviews ONE final report at the end.
**Expected wall-clock:** ~30–45 minutes. Smaller than B.4 — single ~90-line port + one new doc, no new tests.

---

## 0. Why This Differs From CLAUDE.md §5 C.1

CLAUDE.md §5 currently describes Phase C.1 as: *"Define the trade module interface. Design work, no production code. What does a trade module receive (TradeModuleInput), what does it produce, how does it register, how does it report uncertainty. Output is a design document reviewed before C.2."*

That description was authored before the realignment fully landed and before TracePoint's `core/trade_module.py` was identified as already containing the Protocol + dataclasses Daniel's design work would have produced. Re-doing that work as fresh design would violate the verbatim-port discipline that has held through B.1–B.4 ("DO NOT reinvent" — §4.3 of every B.x march orders).

**Decision:** C.1 ports `trade_module.py` verbatim — same shape as B.1–B.4 — and adds a Huckleberry-specific cross-trade integration appendix for the cases TracePoint's single-trade contract does not address (RTU on roof, storefront-at-parapet, siding-to-roofline transitions, structural-deck/roofing). That appendix is design work; the contract itself is a port.

**Consequence for CLAUDE.md:** §5 C.1 paragraph requires a one-paragraph correction to match this decision. That correction is Step C.1.1, before any production code lands. Same shape as B.4.1's §5 correction.

---

## 1. TracePoint Files Read in Full (Pre-Condition)

Before any code touches the backend, the following file is read end-to-end:

**C.1 port target (read in full):**
- `tracepoint_port/TracePoint/core/trade_module.py` (90 lines)

**Read for context, NOT ported in C.1:**
- `tracepoint_port/TracePoint/modules/roofing/roofing_module.py` — concrete consumer of the contract; informs the appendix (what info actually crosses the boundary in TracePoint). Reading this is for understanding only; no code lands in C.1.
- `tracepoint_port/TracePoint/server/routes/trade.py` — the `build_trade_input()` assembly point; reading this is for understanding only; no code lands in C.1.
- TracePoint paper §9 — "scope extraction requires position-based filtering of text blocks INSIDE the building polygon" — the architectural premise the contract embodies.

**Discovery already established (verified at C.1.0):**
- `trade_module.py` imports: stdlib only (`__future__.annotations`, `dataclasses` (`dataclass`, `field`), `typing` (`Any`, `Optional`, `Protocol`)). Zero `from core.*`, zero `from data.*`, zero `from modules.*`, zero third-party.
- Source SHA-1: `d272f47d4ab9d32afe6beb7d38aa0b7f50f4ccbe`. Source line count: 90.
- TracePoint has no `tests/test_trade_module.py`. The Protocol is a contract definition, not implementation; it is exercised through concrete trade modules (Phase C.2+).
- Expected diff vs source: zero lines.
- No new backend dependencies.

If discovery's import analysis is wrong at C.1.2 (after the full read), that's a §7 stop — surface as Discovered Issue, do not silently absorb. (The B.4 discovery had three import-analysis discrepancies; the corresponding D-6 in C.1 should be opened the same way if discrepancies surface here.)

---

## 2. Goal Statement

**C.1 ships when:**

1. CLAUDE.md §5 C.1 paragraph corrected to verbatim-port + appendix language (no "design document" framing)
2. `backend/core/trade_module.py` byte-identical to TracePoint source (`diff = 0`, SHA-1 match `d272f47d4ab9d32afe6beb7d38aa0b7f50f4ccbe`)
3. `backend/CROSS_TRADE_INTEGRATION_NOTES.md` created with the four named cross-trade interactions documented at medium scope (each entry: what the interaction is, what info has to flow, which phase decides). Not exhaustive — just the obvious ones.
4. Sacred floor held at 214 backend / 19 skipped / 0 failed, all frontend suites unchanged
5. Single commit at end of C.1.4
6. Single CLAUDE.md edit (the §5 C.1 paragraph correction at Step C.1.1)
7. No new tests — TracePoint has no `test_trade_module.py` and C.1 introduces no testable behavior beyond the dataclass shape (which Python's import system already validates by collection)

**C.1 explicitly does NOT ship:**
- Any concrete trade module (roofing, glazing, etc.) — that's C.2+
- The `build_trade_input()` assembly point — that's C.2 when the first concrete module needs it (port from `tracepoint_port/TracePoint/server/routes/trade.py`)
- A re-export in `backend/core/__init__.py` — kept empty per the §4.1 sacred-files rule
- Any wiring of `TradeModule` into `dispatch_gate.py`'s output — that's C.2
- A test file — TracePoint has none and C.1 adds no implementation
- Any change to v0.2 ported files, B.1/B.2/B.3/B.4 ported files, or `dispatch_gate.py` activation logic
- Any new dependency
- Any expansion of the appendix beyond the four named interactions (RTU/roofing-mechanical, storefront/glazing-roofing, siding-roofing transition, structural-deck/roofing)

---

## 3. Sacred Floor — Hold Each Line Item

Same rule as B.1/B.2/B.3/B.4: each line independent, no reconciliation to a single total.

**Start-of-session baseline (B.4's end-state):**

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
| Backend `test_geometry_matrix.py` (B.2) | 36/36 |
| Backend `test_polygon_scorers.py` (B.3) | 16/16 |
| Backend `test_architect_profile.py` (B.4) | 23/23 |
| Backend v0.1 baseline | 38/38 |
| Backend full suite | 214 passed, 19 skipped, 0 failed |

**Expected end-of-session:** 214 passed, 19 skipped, 0 failed. Every line unchanged. C.1 adds no new tests.

If anything regresses below baseline at any verification point, that's a §7 stop.

---

## 4. Constraints

### 4.1 — Sacred files (do not modify except as explicitly authorized)

- **Authorized modification:** `CLAUDE.md` (Step C.1.1 only — §5 C.1 paragraph)
- **Authorized creation:**
  - `backend/core/trade_module.py` (verbatim port)
  - `backend/CROSS_TRADE_INTEGRATION_NOTES.md` (new appendix)
- **Sacred (do not touch):** all TracePoint sources at `tracepoint_port/TracePoint/`, Phase 1 frontend HTML, all v0.2 ported files (`config.py`, `pdf_engine.py`, `zone_filter.py`, `context.py`, `dispatch_gate.py`, `roofing_spec_database.py`, `test_pdf_engine.py`, `test_dispatch.py`), B.1/B.2/B.3/B.4 ported files (`filter_pipeline.py`, `geometry_matrix.py`, `polygon_scorers.py`, `architect_profile.py`, `storage.py`, `correction_store.py`, and their tests), v0.1 schema (`shared/bidset_record.py`), seed files, `backend/core/__init__.py` (kept empty), all other docs (`MARCH_ORDERS_*.md`, `STEP_*.md`, `DISCOVERED_ISSUES.md`, `V0_2_VALIDATION.md`, observation/diagnostic docs, the now-existing `backend/INTAKE_DIAGNOSTIC*.md` and `backend/PUBLIC_CORPUS_OBSERVATIONS.md` and `backend/TRACEPOINT_DISCOVERY.md`)

### 4.2 — Do not expand scope

- DO NOT port `roofing_module.py`, `vocabulary.py`, or any concrete trade module — that's C.2
- DO NOT port `server/routes/trade.py` or build `build_trade_input()` — that's C.2
- DO NOT add a re-export to `backend/core/__init__.py`
- DO NOT add a `TradeModule` registration mechanism in `dispatch_gate.py`
- DO NOT migrate `BidsetRecord` to `PlanSetContext`
- DO NOT fix D-4 or D-5
- DO NOT add features "while we're in there"
- DO NOT touch frontend code
- DO NOT add new dependencies
- DO NOT write a `test_trade_module.py` — TracePoint has none and C.1 adds no testable implementation. The first behavior-bearing test arrives in C.2 with the first concrete trade module.

### 4.3 — Do not reinvent

- DO NOT redesign `TradeModuleInput` / `TradeModuleOutput` / `TradeFieldValue` / `TradeModule` — they are TracePoint canonical, port verbatim
- DO NOT change the `source` enum values in `TradeFieldValue` (`"auto_geometry"` | `"auto_text"` | `"auto_legend"` | `"manual_needed"`) — TracePoint convention
- DO NOT change the `polygon_*` field names or ordering — `build_trade_input()` (C.2) populates them by position/name
- DO NOT replace `dataclasses` with Pydantic — Pydantic enters at the wrapper-schema layer (Phase D), not the trade-module contract

### 4.4 — Cross-trade appendix scope (medium, not exhaustive)

Four cross-trade interactions get one entry each in `CROSS_TRADE_INTEGRATION_NOTES.md`. Each entry is roughly 100–200 words and contains:

1. **What the interaction is** — one-paragraph plain-English description of the boundary and why it exists in commercial construction
2. **What info has to flow** — concrete fields/signals each side needs from the other (e.g., "mechanical → roofing: per-RTU bbox + curb size; roofing → mechanical: parapet height + roof pitch")
3. **Which phase decides** — the architectural decision point (e.g., "C.4 cross-trade relationships layer," "Phase D job-folder schema," or "deferred — surfaces only when both trade modules ship")

Required entries (in order, all four):

- **RTU / roofing ↔ mechanical** — rooftop unit appears as both a mechanical scope item (the unit itself) and a roofing penetration (the curb, flashing, walkpads). Single source of truth lives in mechanical; roofing consumes the position to derive penetrations and walkway routing. Decision: C.4.
- **Storefront / glazing ↔ roofing** — at parapet/storefront junctions, glazing flashes against roofing. Glazing module specs the storefront extents; roofing module specs the counterflashing. Decision: C.4.
- **Siding ↔ roofing transition** — where wall siding terminates at the roofline (drip edge / step flashing / kick-out). Both modules carry a "transition detail" reference; only one of them owns the linear footage. Decision: C.4 (with C.3 glazing parking siding as a near neighbor).
- **Structural deck ↔ roofing** — the deck below the roof system (B22 metal deck, concrete, plywood) is structural's scope, but roofing needs deck type + gauge + span direction to specify fasteners and substrate. Decision: deferred — surfaces only when a structural trade module is on the roadmap.

Out of scope for this appendix (do not write entries for these in C.1):
- Plumbing roof drains' connection to interior plumbing risers (a real interaction, but not on the immediate C.2/C.3 path)
- Electrical conduit penetrations (real, but lower-priority than RTU)
- Fire sprinkler heads through roof (specialty, post-v1.0)
- Lightning protection / grounding (specialty)
- Solar PV on roof (specialty, future trade module)

These exclusions are intentional. The appendix is a starter map of the obvious cross-trade boundaries, not an architecture document. Phase C.4 will produce the architecture document when both sides of a boundary actually ship.

### 4.5 — Karpathy procedure (held on substance)

- Read first (full reads). State which files were read in the final gate report.
- Verbatim copy. `diff = 0` for the production file.
- Sacred floors held at every verification point.
- §7 stops surface Discovered Issues; do not silently resolve.
- No failing-test floor step in C.1 because the port is type definitions only — no behavior to fail. Sacred-floor regression is the only test signal C.1 can produce, and it must stay green.

### 4.6 — Autonomous execution

Same pattern as B.2/B.3/B.4. Steps C.1.0 through C.1.4 run in one session. Substantive gates only. ONE final gate report at the end.

---

## 5. Step List

### Step C.1.0 — Pre-flight

**Read:** This march orders document end-to-end. `CLAUDE.md` §5 (current C.1 paragraph that needs correcting) and §6 (hard guardrails refresh). `backend/TRACEPOINT_DISCOVERY.md` if it has a §3.13+ entry covering trade_module.py — record what it claims about imports.

**Verify (no writes):**
- Source file `tracepoint_port/TracePoint/core/trade_module.py` exists and is readable; record SHA-1 (expect `d272f47d4ab9d32afe6beb7d38aa0b7f50f4ccbe`); record line count (expect 90).
- Target `backend/core/trade_module.py` does NOT exist (B.4 did not create it).
- `backend/CROSS_TRADE_INTEGRATION_NOTES.md` does NOT exist.
- Backend baseline: `cd backend && python -m pytest -q` → 214 passed, 19 skipped, 0 failed.
- Frontend baseline: `node run_tests.js` → 107/107; `node spotcheck_10b.js` → 7/7; `node spotcheck_cricket.js` → 4/4; `node spotcheck_durolast.js` → 8/8; `node spotcheck_manufacturer.js` → 14/14; `node mutation_test_step11.js` → 8/8 mutations caught.
- Working tree state: branch `phase2-v0.3-C1-trade-module-interface` does not yet exist locally; HEAD of the project sits at B.4 commit `a8ee936` on `phase2-v0.3-B2-geometry-engine`. Stash any in-flight diagnostic docs the same way B.4 did, with the same B.4 caveat: if CLAUDE.md is uncommitted in working tree, the stash will capture it, and Step C.1.1 will need it back. Pop early if so.
- Branch state: create new branch `phase2-v0.3-C1-trade-module-interface` from `a8ee936`. Per the user's confirmed plan, C.1 is the start of a fresh branch (not a continuation of `phase2-v0.3-B2-geometry-engine` which already carries B.2+B.3+B.4). Phase C work lives on its own branch.
  ```
  git checkout -b phase2-v0.3-C1-trade-module-interface a8ee936
  ```

**Internal gate:** Pre-conditions green. Baseline recorded. Branch in place.

**§7 stop only if:** baseline mismatch, source file missing, working tree won't clean, branch creation conflicts with an existing branch of the same name.

### Step C.1.1 — CLAUDE.md correction

**Write:** One edit to `CLAUDE.md`.

**Edit — §5 C.1 paragraph.** Find the paragraph that begins:

> **C.1 — Define the trade module interface.**

Replace its full text with:

> **C.1 — Port the trade module Protocol verbatim, capture cross-trade integration cases.** TracePoint's `core/trade_module.py` is already the design Daniel's C.1 design pass would have produced — a Protocol (`TradeModule`) plus three dataclasses (`TradeFieldValue`, `TradeModuleInput`, `TradeModuleOutput`) defining the platform/trade boundary. C.1 ports that file verbatim (`diff = 0` against TracePoint source) into `backend/core/trade_module.py`, and adds `backend/CROSS_TRADE_INTEGRATION_NOTES.md` covering the four obvious cross-trade interactions TracePoint's single-trade contract does not address (RTU/roofing↔mechanical, storefront/glazing↔roofing, siding↔roofing transition, structural-deck↔roofing). The appendix names the interactions, the info each side needs, and which phase decides — it is not the C.4 architecture document. No tests in C.1 (TracePoint has no `test_trade_module.py`; the Protocol is exercised by concrete modules, starting in C.2). No registration mechanism, no `build_trade_input()` — those land in C.2 when the first concrete trade module (roofing) needs them.

**Run:** Sacred-floor check (no test impact expected from doc edits, but verify):
```
cd backend && python -m pytest -q
```

**Internal gate:** CLAUDE.md edit applied. Sacred floor unchanged.

**§7 stop only if:** any test regresses (would indicate something unexpected).

### Step C.1.2 — Read trade_module.py end-to-end

**Read:**
- `tracepoint_port/TracePoint/core/trade_module.py` (90 lines, full)

**Verify (no writes):**
- Imports: `from __future__ import annotations`, `from dataclasses import dataclass, field`, `from typing import Any, Optional, Protocol`. Confirm exactly that — stdlib only, zero `from core.*`, zero `from data.*`, zero third-party.
- Public surface: `TradeFieldValue`, `TradeModuleInput`, `TradeModuleOutput` (all `@dataclass`), and `TradeModule` (Protocol).
- `TradeFieldValue` fields: `value: Any`, `confidence: float`, `source: str`, `evidence: str`, `display_name: str = ""`, `unit: str = ""`. `source` enum is a free string but TracePoint convention is `"auto_geometry" | "auto_text" | "auto_legend" | "manual_needed"`.
- `TradeModuleInput` shape: geometry block (8 fields), interior text (3 list fields, `field(default_factory=list)`), dispatch context (3 fields with defaults), project_scope (Optional), page_number (Optional), plus two helper methods `to_sf` and `to_lf` that multiply by `scale_fpi` / `scale_fpi**2`.
- `TradeModuleOutput` fields: `fields: dict[str, TradeFieldValue]`, `warnings: list[str]`, `equipment_pins: list[dict]`.
- `TradeModule` Protocol: class-level `TRADE_NAME: str` and `FIELDS: list[str]`, plus `analyze(input: TradeModuleInput) -> TradeModuleOutput` method signature.

**Internal gate:** All imports as discovery anticipated. Public surface as documented above.

**§7 stop only if:** any unexpected import (e.g., a `from core.context` import the discovery missed), any name change versus the discovery, or any constraint discovered that contradicts §4.

### Step C.1.3 — Verbatim port + cross-trade appendix

**Write (in this order):**

1. **Verbatim copy.** Copy `tracepoint_port/TracePoint/core/trade_module.py` → `backend/core/trade_module.py`. Pure copy, verbatim, no edits.

2. **Verify port.**
   ```
   diff tracepoint_port/TracePoint/core/trade_module.py backend/core/trade_module.py
   sha1sum tracepoint_port/TracePoint/core/trade_module.py backend/core/trade_module.py
   ```
   Expected: `diff` produces zero output; SHA-1 pair matches `d272f47d4ab9d32afe6beb7d38aa0b7f50f4ccbe`.

   **§7 stop only if:** `diff` produces output or SHA-1 mismatch. Surface as Discovered Issue.

3. **Create appendix.** Write `backend/CROSS_TRADE_INTEGRATION_NOTES.md` with the four required entries per §4.4. Suggested skeleton (the executor fills in the prose; do not change the headings or order):

   ```markdown
   # Cross-Trade Integration Notes

   **Purpose.** The trade-module contract at `backend/core/trade_module.py`
   is single-trade by design — one module, one page, one `TradeModuleInput`,
   one `TradeModuleOutput`. Real commercial-construction takeoffs cross
   trade boundaries. This document names the obvious crossings and where
   each gets decided architecturally. It is NOT the cross-trade
   architecture document — that's Phase C.4. It is the starter map.

   **Status.** Authored 2026-04-27 in C.1, alongside the verbatim port of
   `trade_module.py`. Four interactions named; others (plumbing risers,
   electrical conduit, fire sprinkler, lightning, solar PV) are
   intentionally deferred per MARCH_ORDERS_C_1.md §4.4.

   ---

   ## 1. RTU / roofing ↔ mechanical

   **What the interaction is.** [one paragraph: rooftop unit is a
   mechanical scope item AND a roofing penetration; both modules see it,
   one owns the unit, the other owns the curb/flashing/walkpads]

   **What info has to flow.** [concrete: mechanical → roofing per-RTU
   bbox + curb size + weight class; roofing → mechanical parapet height
   + roof pitch + drainage path]

   **Which phase decides.** Phase C.4 — cross-trade relationships layer.
   Surfaces when the mechanical trade module ships (post-glazing per
   current C.2/C.3 ordering, so realistically post-v1.0).

   ---

   ## 2. Storefront / glazing ↔ roofing

   [same shape as §1]

   ---

   ## 3. Siding ↔ roofing transition

   [same shape as §1]

   ---

   ## 4. Structural deck ↔ roofing

   [same shape as §1; explicitly note "deferred — surfaces only when a
   structural trade module is on the roadmap"]

   ---

   ## What this document is NOT

   - Not the C.4 cross-trade relationships architecture document
   - Not exhaustive — see §4.4 of MARCH_ORDERS_C_1.md for explicit
     exclusions (plumbing risers, electrical conduit, fire sprinkler,
     lightning protection, solar PV)
   - Not a contract — the trade-module contract is `backend/core/trade_module.py`
     and stays single-trade
   - Not a roadmap — the phase decisions noted above are the canonical
     reference; this document records them in one place for convenience
   ```

**Run:** Sacred-floor check.
```
cd backend && python -m pytest -q
```

Backend should still be 214 / 19 / 0 — the new `core/trade_module.py` introduces no behavior, just types. If pytest's collection picks up the new file via any auto-discovery and surfaces an import error, that's a §7 stop.

**Internal gate:** Production file byte-identical, SHA-1 matches. Appendix in place with all four required entries. Sacred floor 214 / 19 / 0 unchanged.

**§7 stop only if:** any test regresses, any file size/SHA-1 diverges, or any required appendix entry is missing or off-shape (each entry must contain all three labelled subsections: "What the interaction is," "What info has to flow," "Which phase decides").

### Step C.1.4 — Final regression sweep + commit + final gate report

**Run (in order):**
```
# Backend full suite
cd backend && python -m pytest -v

# Frontend — every suite explicitly
node run_tests.js
node spotcheck_10b.js
node spotcheck_cricket.js
node spotcheck_durolast.js
node spotcheck_manufacturer.js
node mutation_test_step11.js
```

**Expected:** Backend at 214 passing / 19 skipped / 0 failed (unchanged from start). Frontend every suite at exact baseline.

**Write (commit):**
```
git add CLAUDE.md backend/core/trade_module.py backend/CROSS_TRADE_INTEGRATION_NOTES.md
git commit -m "Phase C.1: Port TracePoint trade_module.py Protocol verbatim, add cross-trade integration notes"
```

**Then (only if a stash was created in C.1.0 and not popped early):**
```
git stash pop
```
Verify post-pop: full backend pytest still at 214 / 19 / 0.

**Produce final gate report** in standard format, single report covering CLAUDE.md correction + verbatim port + appendix.

```
=== Phase C.1 Session Report — <date> ===

STEPS COMPLETED: C.1 — verbatim port of trade_module.py + cross-trade
integration notes appendix, with CLAUDE.md correction reframing C.1
from "design document" to "verbatim port + appendix."

FILES CHANGED:
  CLAUDE.md                                      MODIFIED (§5 C.1 paragraph)
  backend/core/trade_module.py                   NEW (90 lines, byte-identical, sha1 d272f47d4ab9d32afe6beb7d38aa0b7f50f4ccbe)
  backend/CROSS_TRADE_INTEGRATION_NOTES.md       NEW (4 cross-trade entries + framing + exclusions)
  Verbatim verification: diff against TracePoint source = zero output for trade_module.py. SHA-1 matches.

DEPENDENCIES: pyproject.toml unchanged. No new deps.

FILES NOT CHANGED (sacred):
  All TracePoint sources (read-only)
  Phase 1 frontend
  v0.2 ported files (none touched)
  B.1/B.2/B.3/B.4 ported files (none touched)
  backend/core/__init__.py (still empty)
  shared/bidset_record.py
  All other docs (MARCH_ORDERS_*, STEP_*, DISCOVERED_ISSUES, V0_2_VALIDATION, observations)
  dispatch_gate.py — no TradeModule registration wired; C.2 will wire it

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
| Backend full suite                   | 214     | 214     | unchanged (C.1 adds no tests) |

REGRESSIONS: none

KARPATHY DISCIPLINE:
  Read first: trade_module.py read end-to-end before any writes (90 lines)
  Failing test floor: skipped — C.1 is type definitions only, no behavior
    to fail; sacred-floor regression is the only signal C.1 can produce
    and it stayed green
  Minimum implementation: pure verbatim copy, zero edits. diff = 0.
  100% green floor: all sacred suites unchanged.
  CLAUDE.md correction reframes the phase cleanly with the §5 C.1
    paragraph rewrite.

DISCOVERED ISSUES: <none, OR D-N if any surfaced>

EXECUTION DETAIL:
  Branch: phase2-v0.3-C1-trade-module-interface (NEW; created from a8ee936
    per user's confirmed plan; C.1 starts a fresh Phase C branch rather
    than continuing on phase2-v0.3-B2-geometry-engine)
  Pre-flight stash: <stash@{0} ref or "none — working tree was clean">
  C.1 commit: <SHA> "Phase C.1: Port TracePoint trade_module.py Protocol verbatim, add cross-trade integration notes"
  Stash list at end: <empty, OR pop result>

git log (current branch):
  <C.1 SHA>  Phase C.1: ...
  a8ee936    Phase B.4: Port TracePoint architect_profile / storage / correction_store verbatim, ...
  70c1835    Phase B.3: Port TracePoint polygon_scorers.py verbatim
  4af872e    Phase B.2: Port TracePoint geometry_matrix.py verbatim, ...
  1c3fde4    Phase B.1: Port TracePoint filter_pipeline.py verbatim
  441896a    Phase 2 v0.2: Port TracePoint dispatch gate

PHASE C.1 COMPLETE: trade-module Protocol + dataclasses ported verbatim
into backend/core. Cross-trade integration notes captured for the four
obvious boundaries. C.2 (first concrete trade module — roofing) is now
unblocked.

NEXT STEP: Phase C.2 — port TracePoint's roofing module verbatim:
modules/roofing/vocabulary.py, modules/roofing/roofing_module.py, plus
server/routes/trade.py's build_trade_input() helper. C.2 march orders
draft is the next planning task. C.2 IS behavior-bearing (scope detection,
quantity derivation), so a failing-test floor + verbatim test port apply
the same way B.1–B.4 did.

AWAITING APPROVAL: yes — Daniel approves C.1 commit and confirms C.2
planning may begin.
```

---

## 6. §7 Stop Conditions

Stop and surface as Discovered Issue, ask Daniel:

1. **`diff` produces non-zero output** at C.1.3 for `trade_module.py`
2. **SHA-1 mismatch** between source and ported file (expected: `d272f47d4ab9d32afe6beb7d38aa0b7f50f4ccbe`)
3. **Any sacred floor count regresses** at any verification point (start = 214 backend / 19 skipped / 0 failed; +6 frontend suites at exact baseline)
4. **Unexpected import** surfaces beyond what discovery documented (e.g., a `from core.context` import in trade_module.py that discovery missed)
5. **Production file outside the C.1 targets gets modified** by accident (specifically: `dispatch_gate.py`, B.1–B.4 files, v0.2 files, frontend, seeds — all sacred)
6. **CLAUDE.md edit at C.1.1 introduces a regression**
7. **Stash pop produces conflicts** at end of C.1.4 (if a stash was created)
8. **Branch creation fails** because `phase2-v0.3-C1-trade-module-interface` already exists or `a8ee936` is unreachable
9. **The cross-trade appendix is asked to expand** mid-session (a fifth interaction surfaces during writing). Stop, document the candidate as a deferred entry under the "What this document is NOT" section, and ship the four named entries only. Do not silently grow the appendix.

§7 stops are documentation actions. Document in `backend/DISCOVERED_ISSUES.md` as next available D-number, pause, ask Daniel.

---

## 7. Done Definition

This session is done when:

- [ ] CLAUDE.md §5 C.1 paragraph corrected
- [ ] `backend/core/trade_module.py` byte-identical to source (sha1 `d272f47d4ab9d32afe6beb7d38aa0b7f50f4ccbe`)
- [ ] `backend/CROSS_TRADE_INTEGRATION_NOTES.md` exists with all four required entries (RTU, storefront, siding, structural deck), each containing all three labelled subsections (interaction / info flow / phase decides)
- [ ] All sacred floors held at every verification point
- [ ] No new dependencies
- [ ] No changes to `backend/core/__init__.py`
- [ ] No changes to `dispatch_gate.py`, B.1–B.4 files, v0.2 files, frontend, seeds
- [ ] No new test file created
- [ ] No D-tickets opened, OR all open ones resolved/deferred
- [ ] Single commit on the new `phase2-v0.3-C1-trade-module-interface` branch
- [ ] Stash popped cleanly (if a stash was created)
- [ ] Final gate report produced

When done, **Phase C.1 is complete** and the trade-module contract is in place. The next planning conversation is Phase C.2 — port the first concrete trade module (roofing) verbatim. C.2 is behavior-bearing and follows the full B.1–B.4 pattern (failing-test floor + verbatim test port + verbatim production port + sacred-floor verification).

---

**End of MARCH_ORDERS_C_1.md. Awaiting Daniel's review and Claude Code execution brief.**
