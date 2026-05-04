# MARCH ORDERS — Phase G.2: Discipline-based page-type fallback

**Date:** 2026-05-03
**Drafted by:** Developer (this chat) — note: drafting march orders crosses into General territory; lane discipline drift acknowledged in 2026-05-03 handoff. Daniel accepted this for sign-out delivery.
**Branch base:** Current head of `phase2-v0.3-recon-cascade-map` (`cef1ca7`)
**New branch:** `phase2-v0.3-G2-discipline-fallback`

---

## Mission

Extend the MEP discipline fallback at `dispatch_gate.py:463-466` to cover all CSI disciplines, with a corpus survey scout deciding what page-type each discipline maps to. Single short phase. Two-track: corpus scout (read-only) → patch (single function modification).

---

## Base context Claude Code needs to internalize before starting

The recon at `backend/RECON_CASCADE_MAP.md` §1.5 and §7.2 is the load-bearing reference. Read it first.

The cascade you're extending lives at `dispatch_gate.py:463-466`:

```python
if page_type == PageType.UNKNOWN and disc in (Discipline.MECHANICAL, Discipline.ELECTRICAL, Discipline.PLUMBING):
    page_type = PageType.MEP_PLAN
    confidence = CONFIDENCE_WEAK
```

This fires only when keyword-based classification (`_PAGE_TYPE_RULES` at line 105) returns UNKNOWN AND the sheet number prefix maps to M/E/P via `_DISCIPLINE_MAP` (line 92). For Silverleaf's four UNKNOWN pages (12, 13, 38, 39), the sheet-number discipline is `S` (Structural), which has no fallback, so they stay UNKNOWN. The fix is to extend coverage to other disciplines.

**Vault status:** `dispatch_gate.py` is integration-frozen but vault rule allows dedicated tuning phases. This is dedicated tuning of the file, not integration work touching it incidentally. Vault SHA-1 will change on this branch; that is expected and authorized for this phase. The other vault files (`roofing_module.py`, `roofing_vocabulary.py`, `glazing_module.py`, `glazing_vocabulary.py`, `debug_module.py`) must remain unchanged.

---

## Track 1 — Corpus survey scout (read-only, ~45 min)

**Objective:** For each non-MEP discipline (`S`, `A`, `C`, `L`, `G`, `FP`), determine what `PageType` should be the UNKNOWN fallback when sheet-number prefix matches and keyword classification fails.

**Method:**

1. Run `run_dispatch` against all 15 bidsets in `C:\huck stage 2\full bid sets\` with `--debug` flag (or invoke `run_debug` directly). Use the existing `dispatch_gate.py` CLI or write a one-shot harness script in a temp directory — do NOT add a script to the repo.

2. For each bidset, collect every page where:
   - `page_type == UNKNOWN` (after Filter 2 ran)
   - `sheet_number is not None` (sheet was identified)
   - Discipline (derived from sheet prefix) is not MECHANICAL/ELECTRICAL/PLUMBING

3. For each (discipline, page) tuple, examine the title_block_text and full_text (use `engine.extract_text` and `engine.extract_text_blocks`) to infer what the page actually IS. Roof plan? Foundation plan? Site plan? Detail sheet? You're looking for: do these pages cluster into one obvious type per discipline, or do they scatter?

4. Decision matrix output: for each discipline, recommend either:
   - A specific `PageType` fallback (e.g. `S → STRUCTURAL_PLAN` if a new enum value is needed, OR an existing one like `FRAMING_PLAN`)
   - "No fallback recommended" if pages scatter too widely to assign meaningfully

5. Note: `PageType` enum is defined in `core/context.py`. Adding new enum values is allowed if the corpus justifies them, but defaults to **using existing values where possible** to minimize blast radius.

**Deliverable:** `backend/G_2_CORPUS_SCOUT_REPORT.md`. Sections:
- Bidset list and per-bidset UNKNOWN-with-sheet count
- Discipline-by-discipline breakdown: how many UNKNOWN pages, what the title/full text shows, recommended fallback
- Final decision matrix table: discipline → PageType fallback (or "none")
- New enum values needed (if any) with rationale
- Specific Silverleaf check: do pages 12, 13, 38, 39 land in fallback coverage with the recommended matrix?

**No code changes in Track 1.** Read-only. Sacred floor must hold (230/19/0). Vault SHA-1s must hold (including `dispatch_gate.py`).

---

## Track 2 — Patch (~1 hour after Track 1 ratifies)

**Hold for explicit go-ahead from Daniel via chat.** Do NOT proceed from Track 1 to Track 2 without confirmation. Track 1 may surface findings that change Track 2's scope.

**Objective:** Implement the discipline-to-page-type fallback table per Track 1's recommendation.

**Method:**

1. If Track 1 recommends new `PageType` enum values, add them to `core/context.py` first. Single commit.

2. In `dispatch_gate.py`, after the `_PAGE_TYPE_RULES` table (around line 119), add a new constant:

   ```python
   # Discipline-based page-type fallback when keywords return UNKNOWN
   _DISCIPLINE_FALLBACK = {
       Discipline.MECHANICAL: PageType.MEP_PLAN,
       Discipline.ELECTRICAL: PageType.MEP_PLAN,
       Discipline.PLUMBING: PageType.MEP_PLAN,
       # Track 1 recommendations land here:
       Discipline.STRUCTURAL: PageType.<TBD>,
       Discipline.ARCHITECTURAL: PageType.<TBD>,
       # ...etc per Track 1 matrix
   }
   ```

3. Replace lines 463-466 with:

   ```python
   if page_type == PageType.UNKNOWN and disc in _DISCIPLINE_FALLBACK:
       page_type = _DISCIPLINE_FALLBACK[disc]
       confidence = CONFIDENCE_WEAK
   ```

4. Behavioral equivalence requirement: M/E/P disciplines MUST continue to map to `MEP_PLAN` exactly as before. Bearss byte-equivalence on `roofing_fields=769`, `glazing_items=177`, `door_items=31`, `storefront_items=24` MUST hold.

5. Add a focused test in `backend/tests/test_dispatch.py` (or wherever Filter 2 tests live — check existing structure first). Test the dispatch table directly: for each discipline in `_DISCIPLINE_FALLBACK`, assert that a synthetic UNKNOWN-keyword page with that discipline prefix gets the correct fallback page_type. **Failing test before fix** — write the test first, watch it fail, then make the patch turn it green. This is the Karpathy step the prior chain skipped.

---

## Hard guardrails

1. **Sacred floor:** 230/19/0 at start, ≥230/19/0 at end. New tests can only INCREASE the pass count, never reduce it.
2. **Bearss byte-equivalence:** `run_dispatch(BEARSS)` must produce identical `len(per_page['roofing'].fields)` sums as G.0.9 baseline (769/177/31/24).
3. **Vault SHA-1s:** `roofing_module.py`, `roofing_vocabulary.py`, `glazing_module.py`, `glazing_vocabulary.py`, `debug_module.py` unchanged at session end. Only `dispatch_gate.py` SHA changes (and `context.py` IF new enum values needed).
4. **Silverleaf success criterion:** Post-patch, Silverleaf's UNKNOWN page count must DROP from 4 to a lower number, AND the previously-UNKNOWN pages must land on the discipline-fallback values from Track 1's matrix. If UNKNOWN doesn't drop, the patch didn't do what it claimed.
5. **One commit per track.** Track 1 is one commit. Track 2 is one or two commits (enum addition + patch+test). No mixed commits.
6. **No "while we're in there" cleanup.** No rename of existing constants, no reformatting, no comment additions outside the immediate fix area.
7. **Wall-clock budget:** Track 1: 45 min. Track 2: 60 min. Total session ceiling: 2 hours. If Track 1 exceeds, ship what you have with a "PARTIAL" header and STOP for Daniel review.

## STOP conditions

1. Track 1 corpus survey can't run (bidset folder missing, dispatch failing on a bidset). STOP, report blocker.
2. Track 1 finds that pages within a discipline scatter so widely that no single fallback PageType makes sense. STOP, report — Daniel may want to defer or rescope.
3. Bearss byte-equivalence breaks on Track 2. STOP immediately, this is a regression.
4. Silverleaf UNKNOWN count doesn't drop post-patch. STOP, Track 1's matrix was wrong, do not housekeep.
5. Sacred floor regresses. STOP, fix the test before continuing.
6. Test count cannot decrease. If a test starts failing because of expected behavior changes, the test itself was wrong — fix the test, don't delete it.

## Done when

- Track 1: `backend/G_2_CORPUS_SCOUT_REPORT.md` exists on the branch, pushed, with decision matrix populated.
- Track 2: `dispatch_gate.py:463-466` replaced with `_DISCIPLINE_FALLBACK` table lookup, Silverleaf UNKNOWN count drops, Bearss byte-equivalent, sacred floor holds with at least one new test added covering the fallback dispatch.
- Gate report: `backend/G_2_GATE_REPORT.md` documents pre/post sacred floor, vault SHA-1 deltas, Bearss equivalence proof, Silverleaf UNKNOWN-count delta, and any STOPs that fired.
