# MARCH ORDERS — Phase G.2: Corpus-wide Classifier Upgrade

**Date:** 2026-05-03
**Drafted by:** General (extended-thinking Claude in chat)
**Branch base:** `dec0af5` (head of `phase2-v0.3-G2-discipline-fallback` — the corpus scout commit)
**New branch:** `phase2-v0.3-G2-classifier-upgrade`
**Wall-clock budget:** 120 min ceiling

---

## Rescope notice (read first)

Phase G.2 was originally drafted as "discipline-based page-type fallback" (extending `_DISCIPLINE_FALLBACK` for non-MEP disciplines). Track 1 corpus scout shipped at `dec0af5` and produced `backend/G_2_CORPUS_SCOUT_REPORT.md`. The scout findings invalidated the discipline-fallback premise:

1. Silverleaf's four UNKNOWN-with-sheet pages (12/13/38/39) have `discipline=UNKNOWN` and `sheet_number=None`, so no discipline-fallback table can reach them.
2. Across the 14 other bidsets, only `FP → MEP_PLAN` had clean corpus support (4 pages, 1 bidset). All other disciplines scattered.
3. The actual signal in the corpus is in the page TITLES, not the discipline prefixes. The classifier reads `tb_text` + `full_text` but **not `pc.title`**, even when Filter 1 successfully extracted the title.

**This phase rescopes G.2 from discipline fallback to classifier upgrade.** The corpus scout report is load-bearing input. The discipline-fallback march orders are abandoned (preserved in git history at `dec0af5`).

This phase does NOT fix Silverleaf 12/13/38/39. Those pages have `pc.title=""` because Filter 1 missed their sheet numbers — a separate Filter 1 surface, deferred to a later phase.

---

## Mission

Upgrade `_classify_page_type` in `dispatch_gate.py` to (a) read `pc.title` in addition to `tb_text` and `full_text`, and (b) extend `_PAGE_TYPE_RULES` with corpus-validated keywords. Single function, one file, two changes, one logical commit. No new dependencies. No vault touches outside `dispatch_gate.py`.

**Success criterion:** UNKNOWN-with-sheet page count drops on Hampshire (4→0), Chipotle Tarpon (3→0), Shoppes Avalon (2→0). Bearss byte-equivalent. No bidset's UNKNOWN-with-sheet count increases.

---

## Pre-flight reads (mandatory)

1. `PROJECT_CLAUDE.md` (entry point + sacred floors + vault rule)
2. `PROJECT_ETIQUETTE.md` (how to talk to Daniel — including the cosmetic-improvement-as-drift trap)
3. `ITINERARY.md` (current state + next 6 steps)
4. `CHECKLIST.md` last 3 handoff entries
5. `backend/G_2_CORPUS_SCOUT_REPORT.md` — load-bearing input. §2 (per-discipline breakdowns with named pages, titles, and recommended classifications) is the corpus data this phase commits to.
6. `backend/RECON_CASCADE_MAP.md` — how `pc.title` is set by Filter 1 and consumed downstream.
7. `backend/core/dispatch_gate.py` — read fully. Lines 105 (`_PAGE_TYPE_RULES`), 421 (`_classify_page_type` definition), 444-446 (Filter 2 caller of `_classify_page_type`).
8. `backend/core/context.py` — `PageContext.title` field declaration.
9. `backend/tests/test_dispatch.py` — find the existing structure for classifier tests; new tests must match the existing pattern.

---

## Pre-flight verification

Capture and document in the gate report:

```
git status     (must be clean on dec0af5 before branch creation)
git log -1     (must be dec0af5)
pytest backend/tests   (must show 230 passed, 19 skipped, 0 failed)

sha1sum backend/core/dispatch_gate.py        → c206ff9e... (will change)
sha1sum backend/core/roofing_module.py       → ae9e5b28... (must hold)
sha1sum backend/core/glazing_module.py       → 52c01442... (must hold)
sha1sum backend/core/debug_module.py         → 78f71d90... (must hold)
sha1sum backend/core/roofing_vocabulary.py   → ec6c17f8... (must hold)
sha1sum backend/core/glazing_vocabulary.py   → 64249c8e... (must hold)
```

Then create branch: `git checkout -b phase2-v0.3-G2-classifier-upgrade dec0af5`.

---

## Implementation (single track)

### Step 1 — Inventory existing classifier behavior (read-only, ~10 min)

In the gate report draft, document:

- Current `_PAGE_TYPE_RULES` contents at line 105 — every key (PageType enum value) and its keyword list.
- Current `_classify_page_type` signature at line 421 — exact parameters and what string corpus the keyword search runs against.
- Current Filter 2 call site at line 444-446 — what gets passed to `_classify_page_type`.

This is intel for the gate report, not a deliverable. Skip this and the report has no anchoring.

### Step 2 — Karpathy step: failing tests BEFORE the fix (~15 min)

Write the new tests FIRST. Run pytest. Watch them fail. Then write the fix. This is the discipline gap that bit the prior chain — do not skip it.

Add these tests to `backend/tests/test_dispatch.py` (match existing test structure — likely a new test class `TestClassifierUpgrade` or appended to an existing classifier test class):

| Test name | Input PageContext | Expected page_type | Currently returns |
|---|---|---|---|
| `test_classify_reads_pc_title_framing_plan` | `title="ROOF FRAMING PLAN"`, `tb_text=""`, `full_text=""` | `FRAMING_PLAN` | `UNKNOWN` |
| `test_classify_reads_pc_title_general_notes` | `title="STRUCTURAL NOTES"`, `tb_text=""`, `full_text=""` | `GENERAL_NOTES` | `UNKNOWN` |
| `test_classify_dimensioned_building_plan` | `full_text="DIMENSIONED BUILDING PLAN"` | `FLOOR_PLAN` | `UNKNOWN` |
| `test_classify_window_types_schedule` | `full_text="WINDOW TYPES"` | `SCHEDULE_SHEET` | `UNKNOWN` |
| `test_classify_fire_sprinkler_plan` | `full_text="FIRST FLOOR FIRE SPRINKLER PLAN"` | `MEP_PLAN` | `UNKNOWN` |
| `test_classify_steel_elevations_details` | `title="STEEL ELEVATIONS AND DETAILS"`, `full_text=""` | `DETAIL_SHEET` | `UNKNOWN` |
| `test_classify_utility_notes` | `full_text="UTILITY NOTES"` | `GENERAL_NOTES` | `UNKNOWN` |

Run `pytest backend/tests/test_dispatch.py -k TestClassifierUpgrade -v`. **All 7 must FAIL.** If one passes, the input was wrong or the existing rules already cover that case — investigate, do not soften the test.

Commit-not-yet — these failing tests stay in the working tree as the spec for Step 3.

### Step 3 — Code changes (~20 min)

**Change A:** Modify `_classify_page_type` (dispatch_gate.py:421) to include `pc.title` in the search corpus.

The current function signature reads `tb_text` and `full_text`. It needs `pc.title` too. The minimal-blast-radius change is to add `title` as a parameter and update the Filter 2 caller (line 444-446) to pass `page_ctx.title`. The function's internal keyword-search logic then unions all three string sources before applying `_PAGE_TYPE_RULES`.

**Do not** restructure the function. **Do not** rename existing parameters. **Do not** add type hints to lines you didn't otherwise touch. Karpathy minimum-viable.

**Change B:** Extend `_PAGE_TYPE_RULES` (dispatch_gate.py:105) with the keyword additions below. Read the existing rules first; place additions to match the existing style (alphabetical, list-of-strings, etc.).

| PageType | New keywords to add |
|---|---|
| `FLOOR_PLAN` | `"BUILDING PLAN"`, `"DIMENSIONED BUILDING PLAN"` |
| `SCHEDULE_SHEET` | `"WINDOW TYPES"`, `"DOOR TYPES"` |
| `FRAMING_PLAN` | `"FRAMING PLAN"`, `"ROOF FRAMING PLAN"`, `"FOUNDATION PLAN"` |
| `DETAIL_SHEET` | `"ELEVATIONS AND DETAILS"`, `"STEEL ELEVATIONS"` |
| `GENERAL_NOTES` | `"STRUCTURAL NOTES"`, `"UTILITY NOTES"`, `"FIRE SPRINKLER SPECIFICATIONS"` |
| `MEP_PLAN` | `"FIRE SPRINKLER PLAN"`, `"PLUMBING SANITARY PLAN"` |

**Order matters in the rules table** — Filter 2's matching is first-match-wins per existing structure. Place new entries so longer/more-specific keywords match before shorter substrings (`"ROOF FRAMING PLAN"` before `"FRAMING PLAN"` if both go in the same list; `"DIMENSIONED BUILDING PLAN"` before `"BUILDING PLAN"`).

If existing rules already contain any of these keywords, do not duplicate. Skip the duplicate, note in the gate report.

### Step 4 — Tests pass, sacred floor verification (~10 min)

```
pytest backend/tests -v
```

Expect:
- Sacred floor: **237 passed, 19 skipped, 0 failed** (was 230, +7 new tests)
- All 7 new tests PASS
- All 230 prior tests still PASS
- Zero failures, zero new skips

If sacred floor regresses (any prior test now fails), **STOP**. The fix changed pre-existing behavior. Investigate before continuing — do not soften any prior test.

### Step 5 — Bearss byte-equivalence regression check (~10 min)

Run `run_dispatch` on Bearss in-process (not via API):

```python
from core.dispatch_gate import run_dispatch
result = run_dispatch(BEARSS_PDF_PATH, storage="auto", job_id=None)
# Sum across all pages
roofing_fields = sum(len(pc.trade_module_outputs.get("roofing", {}).get("fields", [])) for pc in result.pages.values())
glazing_items = sum(len(pc.trade_module_outputs.get("glazing", {}).get("items", [])) for pc in result.pages.values())
door_items = ...
storefront_items = ...
```

**Required:** `(roofing_fields, glazing_items, door_items, storefront_items) == (769, 177, 31, 24)` byte-identical.

If not byte-identical, **STOP**. The classifier change altered Filter 2 output on a bidset that should not have been touched (Bearss has no UNKNOWN-with-sheet pages per G.2 scout §1).

### Step 6 — 4-bidset hard gate harness (~20 min)

Create `backend/scripts/g2_classifier_hardgate.py` (tracked file). It runs `run_dispatch` on 4 bidsets and compares UNKNOWN-with-sheet counts vs G.2 scout baseline.

Bidsets to verify:

| Bidset | Baseline UNKNOWN-with-sheet | Required post-patch | Reason |
|---|---:|---:|---|
| Bearss Ave Distribution Center | 0 | 0 | Regression control + byte-equivalence proof |
| Hampshire Self Storage | 4 (FP × 4) | 0 | New `"FIRE SPRINKLER PLAN"` + `"FIRE SPRINKLER SPECIFICATIONS"` keywords |
| Chipotle Tarpon Springs | 3 (S × 3) | 0 | New `"STRUCTURAL NOTES"` + `"STEEL ELEVATIONS"` + `"ROOF FRAMING PLAN"` |
| Shoppes at Avalon | 2 (A × 2) | 0 | New `"DIMENSIONED BUILDING PLAN"` + `"WINDOW TYPES"` |

Harness output: `backend/G_2_HARD_GATE_REPORT.md` with:
- Pre/post sacred floor (237/19/0)
- Pre/post vault SHA-1s (only `dispatch_gate.py` changes)
- Bearss byte-equivalence proof (769/177/31/24 verbatim)
- Per-bidset UNKNOWN-with-sheet table (baseline | post-patch | delta | passed?)
- Per-page detail for the 9 named pages above (sheet_number, title, baseline page_type, post-patch page_type, expected page_type)
- Wall-clock per bidset

**Hard gate criteria (all must PASS):**
1. Bearss: UNKNOWN-with-sheet 0→0 AND trade outputs byte-identical (769/177/31/24)
2. Hampshire: UNKNOWN-with-sheet 4→0
3. Chipotle Tarpon: UNKNOWN-with-sheet 3→0
4. Shoppes Avalon: UNKNOWN-with-sheet 2→0
5. No bidset's UNKNOWN-with-sheet count INCREASES vs baseline (regression on the other 11 bidsets is also a stop — harness does not need to run them, but if it does, no increase is allowed)

If any criterion fails → **STOP**. Do not housekeep, do not commit, document in the gate report and report up to Daniel.

### Step 7 — Commit code change (~5 min)

Single commit on this branch with these files:
- `backend/core/dispatch_gate.py` (modified — `_classify_page_type` + `_PAGE_TYPE_RULES`)
- `backend/tests/test_dispatch.py` (modified — 7 new tests)
- `backend/scripts/g2_classifier_hardgate.py` (new)
- `backend/G_2_HARD_GATE_REPORT.md` (new)

Commit message:
```
Phase G.2 — corpus-wide classifier upgrade

_classify_page_type now reads pc.title alongside tb_text and full_text.
_PAGE_TYPE_RULES extended with corpus-validated keywords from G.2 scout
(FLOOR_PLAN, SCHEDULE_SHEET, FRAMING_PLAN, DETAIL_SHEET, GENERAL_NOTES,
MEP_PLAN extensions). 7 new unit tests + 4-bidset hard gate.

Sacred floor 230→237/19/0. Bearss byte-equivalent (769/177/31/24).
Hampshire 4→0 UNKNOWN-with-sheet. Chipotle Tarpon 3→0. Shoppes Avalon 2→0.

Does NOT fix Silverleaf 12/13/38/39 — those pages have empty pc.title
because Filter 1 missed their sheet numbers (separate phase).
```

### Step 8 — Canon updates (~20 min)

**These are part of the same phase. Do not skip. Do not defer.**

Daniel's standing canon-update protocol (PROJECT_CLAUDE.md, §"Canon update protocol"): the phase-shipping role produces complete updated canon files at sign-out. Per Daniel's directive in this phase's draft request, Claude Code handles the canon updates as part of the march orders.

Update these four files in a separate commit:

#### 8a — `CHECKLIST.md`

Add a new row to the appropriate phase section. Phase G.2 belongs under "Phase F — Pre-Multi-Bidset Optimization" (or whichever section currently houses Phase G work — read the file first; the section may be labeled differently).

Row format (matching existing G.1 row):
```markdown
| G2 | Phase G.2 — corpus-wide classifier upgrade (pc.title read + _PAGE_TYPE_RULES extended) | Developer | 2026-05-03 | hard gate 4/4 PASS | `backend/G_2_HARD_GATE_REPORT.md` |
```

Append a Handoff entry at the bottom of CHECKLIST.md following the existing template. Branch state, what shipped, sacred floors, stops fired, what's pending, next-eligible work.

#### 8b — `ITINERARY.md`

**Section 1 (Last 3 Completed):** Demote Last-3 (Phase D.2) off the list. Promote Last-2 → Last-3, Last-1 → Last-2. Add Phase G.2 as the new Last-1.

Last-1 entry format:
- Branch: `phase2-v0.3-G2-classifier-upgrade` head `<commit-sha>`, pushed
- Shipped: classifier reads pc.title + _PAGE_TYPE_RULES extended with corpus-validated keywords. 7 new unit tests + 4-bidset hard gate.
- Floor delta: backend 230 → 237/19/0; frontend 23/23 unchanged
- Receipts: `backend/G_2_HARD_GATE_REPORT.md`, commit SHA, hard-gate proof on Bearss/Hampshire/Chipotle/Shoppes
- Learning: Filter 1's `pc.title` write was load-bearing input the classifier never read. The corpus scout's discipline-fallback approach was wrong; the keyword-and-title approach was the corpus-validated path. Two full-chain scout cycles (G.0.5/6/7/8/9/G.1 regex; G.2 fallback) finally located classification's actual lever — `_classify_page_type`'s string corpus.
- Lesson banked: When a downstream layer doesn't react to an upstream fix, the next scout's "extend the downstream layer" framing is usually wrong. The right next move is to find which layer actually drives the user-visible output.

**Section 2 (Next 6 Pipeline Steps):** Renumber. The next-eligible work is now Phase G.3 (single-pass-per-page extraction — the "filters out of whack" performance regression fix).

New Next-1 (Phase G.3):
- Depends on: G.2 (this phase)
- Scope: Cache `extract_text` and `extract_text_blocks` per page in PDFEngine. Consolidate pdfplumber to single open-per-dispatch lifecycle (Filter 4 + Stage 13 share). Reuse PyMuPDF blocks in Stage 13 instead of `pdfplumber.extract_words()`.
- Floor target: Backend 237/19/0; cache tests likely add 5-10 (target 242-247)
- Gate: Hard gate vs Bearss byte-equivalence (cache must not change behavior) + wall-clock target (≤3 min vs current ~8 min)
- Risk: Cache invalidation timing. Single open-per-dispatch changes pdfplumber lifecycle — must verify Filter 4 and Stage 13 still see the same data.
- Run: General drafts after G.2 ships clean

Demote everything else by one slot. Phase G (quadrant tiling at 250 DPI, original concept) drops to Next-3 or later.

**Section 3 (Blockers):** No new blockers from this phase. Remove any G.2-related awaiting-Daniel items (the G.2 corpus scout's three options are no longer pending — Daniel locked the corpus-wide approach).

#### 8c — `PROJECT_CLAUDE.md`

Surgical updates only:

**Sacred floors block:** update backend test count from 230 → 237.

**Active phase status section:** add a new bullet:
```markdown
- **Phase G.2 shipped** (commit `<sha>`, 2026-05-03): classifier upgrade — `_classify_page_type` reads `pc.title` alongside `tb_text` + `full_text`; `_PAGE_TYPE_RULES` extended with corpus-validated keywords from G.2 scout. UNKNOWN-with-sheet drops on Hampshire (4→0), Chipotle Tarpon (3→0), Shoppes Avalon (2→0). Bearss byte-equivalent. Silverleaf 12/13/38/39 NOT fixed (Filter 1 sheet-detection gap, separate phase).
```

Update "Phase G.2 next-eligible" → "Phase G.3 next-eligible: single-pass-per-page extraction (caching layer + pdfplumber consolidation)."

Do not edit any other section.

#### 8d — `backend/BLOCK_RUN.md`

Append a new "Phase 11" (or whichever number is next — read the file first, find the highest existing phase number, increment) section at the bottom following the existing format:

```markdown
## Phase <N>: G.2 — Corpus-wide classifier upgrade (2026-05-03)

**Branch:** `phase2-v0.3-G2-classifier-upgrade` (from `dec0af5`)
**Trigger:** MARCH ORDERS Phase G.2 — rescoped from discipline fallback after corpus scout invalidated the original premise.

### Files created
- `backend/scripts/g2_classifier_hardgate.py` — 4-bidset hard gate harness
- `backend/G_2_HARD_GATE_REPORT.md` — hard gate report (PASS)

### Files modified
- `backend/core/dispatch_gate.py` — `_classify_page_type` reads `pc.title`; `_PAGE_TYPE_RULES` extended (FLOOR_PLAN, SCHEDULE_SHEET, FRAMING_PLAN, DETAIL_SHEET, GENERAL_NOTES, MEP_PLAN)
- `backend/tests/test_dispatch.py` — 7 new classifier tests
- `CHECKLIST.md` — Phase G.2 row + handoff
- `ITINERARY.md` — Section 1 + 2 updated
- `PROJECT_CLAUDE.md` — sacred floor 230→237, active phase block updated

### Files deleted / renamed
None.

### Commits
- Code change: `<sha-1>`
- Canon updates: `<sha-2>`

### Vault-ruled files touched
None outside `dispatch_gate.py` (which is integration-frozen + allowed in dedicated tuning phases per PROJECT_CLAUDE.md vault rule). SHA-1 verification at session end:
- `roofing_module.py`: ae9e5b28... (unchanged)
- `glazing_module.py`: 52c01442... (unchanged)
- `roofing_vocabulary.py`: ec6c17f8... (unchanged)
- `glazing_vocabulary.py`: 64249c8e... (unchanged)
- `debug_module.py`: 78f71d90... (unchanged)
- `dispatch_gate.py`: c206ff9e → <new-sha> (expected change)

### Hard gate result
4/4 PASS per `backend/G_2_HARD_GATE_REPORT.md`. Bearss byte-equivalent (769/177/31/24). Hampshire 4→0. Chipotle Tarpon 3→0. Shoppes Avalon 2→0.

### Sacred floor at session end
Backend 237/19/0; frontend 23/23 (untouched).
```

#### 8e — Commit canon updates

Single commit:
```
docs: G.2 canon updates

CHECKLIST: Phase G.2 row + handoff entry
ITINERARY: Section 1 (last 3) + Section 2 (next 6) refreshed
PROJECT_CLAUDE: sacred floor 230→237, active phase block updated
BLOCK_RUN: Phase <N> entry added
```

### Step 9 — Push branch (~2 min)

```
git push -u origin phase2-v0.3-G2-classifier-upgrade
```

Verify push succeeded. Capture remote ref and tag in the gate report.

---

## Hard guardrails

1. **Sacred floor:** 230/19/0 at start, **≥237/19/0** at end (gain of at least 7 from new classifier tests). New tests can only INCREASE the pass count.
2. **Bearss byte-equivalence:** `(roofing_fields, glazing_items, door_items, storefront_items) == (769, 177, 31, 24)`. Any drift = STOP.
3. **No bidset UNKNOWN-with-sheet INCREASE:** Hard-gate harness verifies 4 bidsets explicitly; no other bidset may be made worse. (If you have wall-clock budget, run all 15 from G.2 scout corpus and append per-bidset deltas to the gate report — but this is bonus, not required.)
4. **Vault SHA-1s:** `roofing_module.py`, `roofing_vocabulary.py`, `glazing_module.py`, `glazing_vocabulary.py`, `debug_module.py` unchanged at session end. Only `dispatch_gate.py` SHA changes.
5. **Two commits on this branch maximum:** code+harness+report (1) and canon updates (2). No mixed commits, no third "fix-up" commit.
6. **No "while we're in there" cleanup:** No rename of existing constants, no reformatting, no comment additions outside the immediate fix area, no docstring polish.
7. **Karpathy step is not optional:** Failing tests must exist in the working tree and demonstrably fail against current `dispatch_gate.py` BEFORE the code change. If a test passes immediately, the test is wrong — fix the test, do not soft-pedal the spec.
8. **Wall-clock ceiling:** 120 min from branch creation. If you exceed, STOP, ship what's clean, document in the gate report, and tag the work with a "PARTIAL" header for Daniel review.

---

## STOP conditions

1. **Failing test passes against current code** — your test was wrong. Fix the test (likely pulled in something already covered by existing rules), then proceed. Do not soften the spec.
2. **Bearss byte-equivalence breaks** post-patch — your change altered Filter 2 output on a bidset that has zero UNKNOWN-with-sheet pages. Regression. STOP, do not commit, investigate which keyword change unexpectedly fired on Bearss content.
3. **Hard gate fails on any of the 4 named bidsets** — your keyword set or your `pc.title` wiring missed the named pages. STOP, dump the per-page debug data into the gate report, escalate to Daniel.
4. **Sacred floor regresses** (any of the 230 prior tests fails) — STOP. Your change broke pre-existing behavior. Do not silence the test.
5. **Vault SHA-1 changes** for any file other than `dispatch_gate.py` — you touched a vault module by accident. STOP, revert, restart.
6. **Wall-clock exceeds 120 min** — STOP, ship-what's-clean discipline. Don't grind through over budget.
7. **You find yourself reaching for a "while we're in there" cleanup** — STOP that thought. Out of scope. Out of scope. Out of scope.
8. **You start drafting another scout** — this phase has zero scouts. The corpus data is in `G_2_CORPUS_SCOUT_REPORT.md`. STOP and execute against it.

---

## Done when

- [ ] Branch `phase2-v0.3-G2-classifier-upgrade` exists locally and on origin
- [ ] `dispatch_gate.py` has both changes (pc.title read + _PAGE_TYPE_RULES extended)
- [ ] 7 new tests in `test_dispatch.py`, all passing
- [ ] Sacred floor 237/19/0 (or higher if more tests added — never lower)
- [ ] Bearss byte-equivalence verified (769/177/31/24) — proof in gate report
- [ ] Hard gate 4/4 PASS — proof in `backend/G_2_HARD_GATE_REPORT.md`
- [ ] Hard-gate harness committed at `backend/scripts/g2_classifier_hardgate.py`
- [ ] Two commits on branch: code+harness+report (1), canon updates (2)
- [ ] CHECKLIST.md, ITINERARY.md, PROJECT_CLAUDE.md, BLOCK_RUN.md all updated
- [ ] Branch pushed to origin
- [ ] Vault SHA-1s held except `dispatch_gate.py` (expected)
- [ ] Sign-out announcement: "Signed out as Developer. Phase G.2 shipped clean. Hard gate 4/4 PASS. Canon updated. Branch pushed. Standing by."

---

## What this phase does NOT do (explicit non-goals)

- Does NOT fix Silverleaf 12/13/38/39 (separate Filter 1 phase)
- Does NOT touch Filter 1 sheet detection
- Does NOT add the `FP → MEP_PLAN` discipline fallback the original G.2 proposed (the new keyword `"FIRE SPRINKLER PLAN"` covers Hampshire's 3 plan pages; the spec page FP0.1 is covered by `"FIRE SPRINKLER SPECIFICATIONS"` → `GENERAL_NOTES`)
- Does NOT extend `_DISCIPLINE_MAP` to recognize H/QP prefixes (deferred — corpus signal is 3 pages, low priority)
- Does NOT add caching, pdfplumber consolidation, or any performance work (that's Phase G.3)
- Does NOT touch any frontend file
- Does NOT modify `pyproject.toml` or any dependency declaration

---

**End of march orders. Sign-in announcement first, then execute.**
