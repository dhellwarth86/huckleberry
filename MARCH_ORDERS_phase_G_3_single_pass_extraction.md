# MARCH ORDERS — Phase G.3: Single-pass-per-page extraction

**Date:** 2026-05-03
**Drafted by:** General (extended-thinking Claude in chat)
**Branch base:** Head of `phase2-v0.3-G2-classifier-upgrade` (the canon-update commit, NOT `170fcd7` — pull the actual head from `git log -1` after fetching)
**New branch:** `phase2-v0.3-G3-single-pass-extraction`
**Wall-clock budget:** 90 minutes ceiling

---

## Mission

Restore the TracePoint paper's "Layer 1 extracts once, Layers 2-4 consume" architecture in the ported pipeline. Three changes, all in `dispatch_gate.py` + `pdf_engine.py`, one branch, two commits (code, then canon).

The current pipeline calls `engine.extract_text_blocks(doc, page_idx)` 7-9 times per page across the 12 stages, calls `engine.extract_text(doc, page_idx)` 2-3 times per page, opens-and-closes `pdfplumber` per SCHEDULE_SHEET page in Filter 4, and then re-extracts every word via `pdfplumber.extract_words()` per page in Stage 13 trade-module wiring. Every extraction returns the same data the previous one returned. The paper's architecture says this should not happen.

This phase fixes it.

---

## What this phase is NOT

- **Not an accuracy test.** Daniel is the wall-clock. There is no automated byte-equivalence test, no multi-bidset hard gate, no `storage="auto"` re-runs against historical numbers. The hard gate is one dispatch run on Chipotle Tarpon Springs.
- **Not a refactor.** Don't restructure functions. Don't rename. Don't move code around for cleanliness. Make the three named changes and stop.
- **Not a place for new pytest validation tests against bidsets.** Pytest unit tests for the cache mechanism itself (in-process, no PDF) are appropriate per Karpathy. Pytest tests that load any bidset are NOT in scope this phase. Tests that `import git`, shell out to git/subprocess for any reason, or read commit history / branch state are an automatic phase fail.
- **Not a place to touch trade-module code.** `roofing_module.py` and `glazing_module.py` stay frozen. They're vault-ruled. Stage 13's input shape changes (PyMuPDF blocks instead of pdfplumber words), but the modules read whatever shape they're given via `TradeModuleInput.text_blocks`. If module behavior changes, that's data for review — not a Stage 13 rewrite.

---

## Pre-flight reads (mandatory)

1. `PROJECT_CLAUDE.md` (entry point + sacred floors + vault rule)
2. `PROJECT_ETIQUETTE.md` (how to talk to Daniel — including the cosmetic-improvement-as-drift trap)
3. `ITINERARY.md` (current state: Phase G.2 shipped, G.3 is Next-1)
4. `CHECKLIST.md` last 3 handoff entries
5. `backend/G_2_HARD_GATE_REPORT.md` — the prior phase's ship; gives you what shipped and what didn't
6. `backend/RECON_CASCADE_MAP.md` — for orientation on Filter execution order (1→2→4→3→5)
7. `backend/core/dispatch_gate.py` — read fully. The file is ~1965 lines. The 15 `engine.extract_text*` call sites and 2 `pdfplumber.open` call sites are all targets of this phase.
8. `backend/core/pdf_engine.py` — read fully. The cache lives here. Find the existing `extract_text` and `extract_text_blocks` implementations.
9. `backend/core/roofing_module.py` AND `backend/core/glazing_module.py` — read for understanding only (vault-ruled, do not edit). Specifically: how do they iterate `TradeModuleInput.text_blocks`? What fields do they expect on each block? This tells you whether PyMuPDF blocks (paragraph-level) versus pdfplumber words (word-level) will produce different module outputs.

---

## Pre-flight verification (Step 0)

Capture and document in the gate report:

```
git status                  (must be clean before branch creation)
git log -1                  (capture the actual head commit SHA)
pytest backend/tests        (must show 237 passed, 19 skipped, 0 failed)

sha1sum backend/core/dispatch_gate.py        → 09bc0340... (will change)
sha1sum backend/core/pdf_engine.py           → (capture; will change)
sha1sum backend/core/roofing_module.py       → ae9e5b28... (must hold)
sha1sum backend/core/glazing_module.py       → 52c01442... (must hold)
sha1sum backend/core/debug_module.py         → 78f71d90... (must hold)
sha1sum backend/core/roofing_vocabulary.py   → ec6c17f8... (must hold)
sha1sum backend/core/glazing_vocabulary.py   → 64249c8e... (must hold)
```

Create branch from the canon commit head: `git checkout -b phase2-v0.3-G3-single-pass-extraction <canon-head-sha>`.

---

## Step 1 — Capture the BEFORE wall-clock baseline (read-only, ~2 min)

**This step runs BEFORE any code change.** The whole point of this phase is wall-clock reduction. Without a before-number, the after-number is meaningless.

Run dispatch on Chipotle Tarpon ONCE on the current (pre-patch) code. Use this exact invocation:

```python
import time
from pathlib import Path
from core.pdf_engine import PDFEngine
from core.dispatch_gate import run_dispatch

CHIPOTLE = Path("backend/test_plans") / "Chipotle - Tarpon Springs (Shell) - Tarpon Springs - Strategic Construction.pdf"

t0 = time.perf_counter()
ctx = run_dispatch(str(CHIPOTLE))
t1 = time.perf_counter()
print(f"BEFORE: {t1 - t0:.2f}s ({len(ctx.pages)} pages)")
```

Run it twice. Record both times. The second run is the "warm" baseline (PyMuPDF/pdfplumber import time amortized). Use the second run as the canonical baseline.

Document in the gate report:
- Wall-clock time, run 1 (cold)
- Wall-clock time, run 2 (warm) — **this is the baseline number**
- Page count returned
- Any warnings printed by dispatch
- Hardware/environment context (just a line: "Windows 10, 32GB RAM" or whatever — for later reference)

Do NOT run the full pytest suite for timing. Do NOT run any other bidset. Chipotle Tarpon, twice, captured.

---

## Step 2 — Inventory the call sites (read-only, ~10 min)

In the gate report, document the current state. Do not skip — this is the "before" reference.

**`engine.extract_text` call sites in `dispatch_gate.py`:** lines 199, 292, 307, 453, 1017. For each: which function, which filter/stage, what does it do with the result.

**`engine.extract_text_blocks` call sites in `dispatch_gate.py`:** lines 277, 398, 451, 606, 845, 903, 1023, 1074, 1098, 1238. For each: which function, which filter/stage, what does it do with the result.

**`pdfplumber.open` call sites in `dispatch_gate.py`:**
- Line 748 (`_parse_tables_on_page`, called per-SCHEDULE-page from Filter 4) — this is the one to hoist.
- Line 1532 (Stage 13 trade-module wiring) — already correctly opened once outside the per-page loop. **Do not touch this one.** It's already correct.

**`pdf_page.extract_words` call site in `dispatch_gate.py`:** line 1556 (Stage 13 trade-module wiring). This is the one to retire — replace with cached PyMuPDF blocks.

**`PDFEngine.extract_text` and `PDFEngine.extract_text_blocks` implementations in `pd f_engine.py`:** read both. Note their current signatures, return types, and whether they hold any state across calls (they shouldn't — that's why we're adding the cache).

This step's output is one section of the gate report titled "Pre-patch call inventory." The numbers in this section get compared against the post-patch state in Step 7's gate-report verification.

---

## Step 3 — Karpathy step: failing unit tests for the cache (~15 min)

Cache logic is in-process and PDF-free. Pytest unit tests on the cache itself are appropriate — they're fast, deterministic, and don't violate Daniel's "no validation-test theater" rule.

Add a new test class to `backend/tests/test_pdf_engine.py` (create the file if it doesn't exist; otherwise append). The tests below MUST FAIL before Step 4 (the implementation):

| Test name | What it asserts |
|---|---|
| `test_cache_returns_same_object_on_repeat_call` | `engine.extract_text(doc, 0)` called twice returns the same object (`is` identity, not just equal) — proves the result was cached, not re-extracted |
| `test_cache_separates_pages` | `extract_text(doc, 0)` and `extract_text(doc, 1)` return different objects — cache key includes page index |
| `test_cache_separates_text_and_blocks` | `extract_text(doc, 0)` and `extract_text_blocks(doc, 0)` return different objects — cache key includes method |
| `test_cache_invalidates_on_doc_close` | After `doc.close()`, a new `engine.extract_text(doc2, 0)` on a fresh doc does not return the cached value from the old doc |
| `test_cache_separates_documents` | Two open documents at the same time have separate caches — `extract_text(docA, 0)` and `extract_text(docB, 0)` return different objects even if pages are identical |

Use a tiny synthetic PDF (1-2 pages, generated in-process via reportlab or PyMuPDF's own page-creation API) for these tests. **Do NOT** load any bidset from `backend/test_plans/`. **Do NOT** import git, subprocess, os.system, or any process-launching module.

Run the new tests. **All 5 must FAIL.** TypeError, AttributeError, or AssertionError — any failure shape is acceptable. If one passes immediately, the test is wrong (likely already covered by some accidental behavior); investigate before proceeding. Do not soften the test.

These failing tests stay in the working tree as the spec for Step 4.

---

## Step 4 — Implement the cache in PDFEngine (~20 min)

Add to `pdf_engine.py`:

1. **A cache attribute on `PDFEngine`.** Python dict, keyed by `(id(doc), page_idx, method_name)`, value = whatever the underlying extractor returned. Use `id(doc)` as the doc-identity key — `fitz.Document` objects don't reliably support `==` or `hash()`, but `id()` is unique while the doc is open.

2. **Wrap `extract_text` and `extract_text_blocks` with cache lookup.** First call extracts and stores. Subsequent calls return the stored value.

3. **Cache invalidation on document close.** Two paths:
   - Cleanest: `PDFEngine` exposes a `close_doc(doc)` method that purges all entries with that doc's `id()` from the cache, then closes the doc. Callers replace `doc.close()` with `engine.close_doc(doc)`.
   - Simpler if the close-call sites are few: a `__del__` or weak reference scheme. This is fine, but **only** if the close-call sites are easy to grep. If `doc.close()` appears in many places, take the explicit `close_doc(doc)` path.

   Pick whichever is less invasive. Document the choice in the gate report.

4. **No persistence.** No SQLite. No disk writes. The cache is RAM, instance-scoped to the `PDFEngine`, and dies when the engine instance is garbage-collected.

Run the 5 new unit tests. All must PASS. If any fails, the cache implementation has a bug — fix it before proceeding to Step 5.

Run the full pytest suite. Sacred floor: **must be ≥ 242/19/0** (was 237, +5 from new cache tests). Zero regressions on the prior 237.

If the full suite shows any test that was passing and is now failing, **STOP**. The cache implementation altered observable behavior somewhere that wasn't supposed to change. Investigate before continuing.

---

## Step 5 — Hoist Filter 4's pdfplumber lifecycle (~15 min)

Current shape (line 840-856):

```python
def run_filter_4(engine: PDFEngine, doc, ctx: PlanSetContext):
    raw_legends = []
    for page_idx in range(doc.page_count):
        blocks = engine.extract_text_blocks(doc, page_idx)
        legends = _find_legends_on_page(blocks, page_idx)
        page_ctx = ctx.pages.get(page_idx)
        if page_ctx and page_ctx.page_type == PageType.SCHEDULE_SHEET:
            table_legends, raw_tables = _parse_tables_on_page(ctx.pdf_path, page_idx)
            ...
```

`_parse_tables_on_page` (line 742) opens AND closes `pdfplumber` every call. On Bearss that's 24 opens/closes per dispatch.

Target shape:

1. Open `pdfplumber` ONCE at the top of `run_filter_4`, in a `try`/`finally` so it always closes.
2. Refactor `_parse_tables_on_page` to accept an open `pdf` object (the pdfplumber Document, not a path) and a page_idx.
3. The `try`/`finally` in `run_filter_4` ensures the pdf gets closed exactly once, even on exception.
4. Preserve the `if not _pdfplumber: return [], []` guard inside `_parse_tables_on_page` for the case where pdfplumber isn't installed.

**Do not** refactor anything else in `run_filter_4` while you're in there. No "while we're at it" cleanup.

After this change: pdfplumber opens once per dispatch in Filter 4 (was: once per SCHEDULE page).

---

## Step 6 — Retire Stage 13's pdfplumber word extraction (~20 min)

Current shape (lines 1528-1577 in trade-module wiring):

```python
use_pdfplumber = _pdfplumber is not None
pdf = None
if use_pdfplumber:
    pdf = _pdfplumber.open(ctx.pdf_path)

try:
    for page_idx in sorted(ctx.pages.keys()):
        page_ctx = ctx.pages[page_idx]
        text_blocks: list = []
        raw_tables = page_ctx.raw_tables
        if pdf is not None and page_idx < len(pdf.pages):
            try:
                pdf_page = pdf.pages[page_idx]
                words = pdf_page.extract_words() or []
                for w in words:
                    text_blocks.append(TextBlock(text=..., x0=..., y0=..., x1=..., y1=..., page=page_idx))
                if not raw_tables:
                    ext = pdf_page.extract_tables() or []
                    if ext: raw_tables = [t for t in ext if t]
            except Exception:
                text_blocks = []
        tinput = _build_dispatch_only_input(ctx, page_idx, text_blocks, raw_tables)
```

Target shape:

1. **Replace `pdf_page.extract_words()` with cached PyMuPDF blocks.** The cached call is `engine.extract_text_blocks(doc, page_idx)` — the same call Filters 1, 2, 4 already made. With the cache from Step 4, this is free.

2. **Build `TextBlock` objects from PyMuPDF block tuples.** PyMuPDF's `extract_text_blocks` returns blocks with text and bounding-box coordinates. Read `pdf_engine.py` to see the exact return shape and use it. Construct `TextBlock` objects with the same fields the trade modules already expect: `text`, `x0`, `y0`, `x1`, `y1`, `page`.

3. **Keep the pdfplumber `extract_tables()` fallback for non-schedule pages** (the `if not raw_tables: ext = pdf_page.extract_tables()` block). Filter 4 only ran tables on SCHEDULE pages; this path catches tables on non-schedule pages where Filter 4 didn't look. That's a separate concern from word extraction — leave it alone.

4. **The pdfplumber.open at line 1532 is still needed** (for the `extract_tables()` fallback in #3). Don't remove it. Just stop calling `extract_words()`.

5. **The `engine` parameter.** Check the signature of the function containing this code (likely `_run_trade_module_wiring` or similar). If `engine` and `doc` aren't already in scope, pass them. If they are, use them.

After this change: Stage 13 reuses cached PyMuPDF blocks. The 7th-9th extraction-per-page that used to happen here disappears.

**A note on what could change:** The trade modules (`roofing_module.py`, `glazing_module.py`) iterate `TradeModuleInput.text_blocks` looking for keywords. Pdfplumber's `extract_words()` returned word-level granularity (one TextBlock per word). PyMuPDF's `extract_text_blocks` returns paragraph-level granularity (one TextBlock per text block, often containing multiple words).

If the modules use `keyword in block.text` style matching, both granularities work — paragraph-level even works *better* for multi-word phrases like "TPO ROOFING" or "ALUMINUM STOREFRONT" that pdfplumber would split across two TextBlocks.

If the modules use `block.text == keyword` exact-match, then word-level loses to phrase-level on those multi-word matches.

**Do not modify the trade modules.** If outputs differ, document the difference in the gate report — that's data for Daniel to review, not a problem to fix in this phase.

---

## Step 7 — Capture the AFTER wall-clock and write the gate report (~10 min)

Run dispatch on Chipotle Tarpon TWICE on the patched code, exactly the same way as Step 1:

```python
import time
from pathlib import Path
from core.pdf_engine import PDFEngine
from core.dispatch_gate import run_dispatch

CHIPOTLE = Path("backend/test_plans") / "Chipotle - Tarpon Springs (Shell) - Tarpon Springs - Strategic Construction.pdf"

t0 = time.perf_counter()
ctx = run_dispatch(str(CHIPOTLE))
t1 = time.perf_counter()
print(f"AFTER: {t1 - t0:.2f}s ({len(ctx.pages)} pages)")
```

Document in the gate report:
- Wall-clock time, run 1 (cold)
- Wall-clock time, run 2 (warm) — **the comparison number**
- Page count returned (must equal Step 1's page count)
- Any new warnings or errors that didn't appear in Step 1

Write `backend/G_3_GATE_REPORT.md` with:
- Pre-patch sacred floor (237/19/0) and post-patch sacred floor (≥242/19/0)
- Pre-patch and post-patch vault SHA-1s (only `dispatch_gate.py` and `pdf_engine.py` should change)
- Step 2's pre-patch call inventory
- A post-patch call inventory showing how many distinct PyMuPDF extractions per page actually happen (likely 1) and how many pdfplumber opens per dispatch (likely 1, or 0 on Chipotle if it has no SCHEDULE pages)
- Step 1's BEFORE wall-clock and Step 7's AFTER wall-clock, both warm-run numbers
- Page count (must match)
- Any trade-module output deltas if you ran them — Chipotle has Structural and Architectural pages, so glazing/roofing modules will fire on at least some pages. Note any difference in module outputs vs the pre-patch run, with no opinion attached. Just the numbers.
- Any STOPs that fired, or "none"

The hard gate criterion is: **dispatch on Chipotle completes successfully with the same page count as before**. The wall-clock number is recorded but is not a pass/fail criterion — Daniel is the wall clock.

---

## Step 8 — Commit the code change (~5 min)

Single commit with these files:
- `backend/core/dispatch_gate.py` (modified — Filter 4 hoist + Stage 13 retire)
- `backend/core/pdf_engine.py` (modified — cache implementation)
- `backend/tests/test_pdf_engine.py` (new or modified — 5 cache tests)
- `backend/G_3_GATE_REPORT.md` (new)

Commit message:
```
Phase G.3 — single-pass-per-page extraction

PDFEngine now caches extract_text and extract_text_blocks per (doc, page).
Filter 4 opens pdfplumber once per dispatch (was: once per SCHEDULE page).
Stage 13 trade-module wiring reuses cached PyMuPDF blocks instead of
calling pdfplumber.extract_words() per page.

Sacred floor 237 → 242/19/0 (+5 cache unit tests).
Hard gate: Chipotle Tarpon dispatch completes with same page count.
Wall-clock recorded but not a gate criterion (see G_3_GATE_REPORT.md).
```

---

## Step 9 — Canon updates (~20 min)

Same shape as G.2's canon update step. Per Daniel's directive, Claude Code handles canon updates as part of the march orders.

Update these four files in a SECOND commit on the same branch:

### 9a — `CHECKLIST.md`

Add a row to the active phase section (currently "Phase F — Pre-Multi-Bidset Optimization" or wherever G.2 landed; read the file and match):

```markdown
| F11 | Phase G.3 — single-pass-per-page extraction (PDFEngine cache + Filter 4 hoist + Stage 13 retire) | Developer | 2026-05-XX | hard gate PASS (Chipotle dispatch completes, same page count); sacred floor 242/19/0 | `backend/G_3_GATE_REPORT.md` · commit `<sha>` |
```

Append a Handoff entry at the bottom following the existing template. Branch state, what shipped, sacred floors, stops fired (or "none"), what's pending, next-eligible work.

### 9b — `ITINERARY.md`

**Section 1 (Last 3 Completed):** Demote Last-3 (G.1) off the list. Promote Last-2 → Last-3, Last-1 → Last-2. Add Phase G.3 as the new Last-1.

Last-1 entry format:
- Branch: `phase2-v0.3-G3-single-pass-extraction` head `<commit-sha>`, pushed
- Shipped: PDFEngine cache + Filter 4 pdfplumber hoist + Stage 13 PyMuPDF reuse. 5 new cache unit tests.
- Floor delta: backend 237 → 242/19/0; frontend 23/23 unchanged
- Receipts: `backend/G_3_GATE_REPORT.md`, commit SHA, Chipotle wall-clock before/after
- Learning: TracePoint paper §2.1 architecture restored — Layer 1 (PyMuPDF) extracts once, Layers 2-4 consume cache. Was: 7-9 PyMuPDF extractions per page + per-SCHEDULE pdfplumber open + Stage 13 pdfplumber word re-extraction. Now: 1 PyMuPDF extraction per page (cached), 1 pdfplumber open per dispatch, 0 redundant Stage 13 extractions.
- Lesson banked: The ported pipeline accumulated a "extract again to be safe" pattern that the original TracePoint architecture explicitly forbade. Look for similar shapes elsewhere — anywhere the same source data is fetched twice in one logical pass is a candidate for cache.

**Section 2 (Next 6 Pipeline Steps):** Demote everything by one slot. The current Next-2 (G.4 Filter 4 hoist + Stage 13 retire) gets DELETED — its scope was absorbed into G.3. The next Next-1 is now the current Next-3 (G.5 render optimization), but rename it Next-1 and consider whether it still needs to be its own phase given that G.3 already collapsed the pdfplumber/PyMuPDF redundancy. If G.5's tiling work is still load-bearing for the auto-notation product, keep it. If G.3 made it redundant, mark it parked.

Pull the current Next-3, Next-4, Next-5, Next-6 forward by one slot. There is no new Next-6 unless something obvious surfaces — leave it open or list "TBD pending Phase F design."

**Section 3 (Blockers):** No new blockers. Remove any G.3-related awaiting-Daniel items. Leave the existing Silverleaf 12/13/38/39 deferred item — that's still its own phase later.

### 9c — `PROJECT_CLAUDE.md`

**Sacred floors block:** update backend test count from 237 → 242.

**Active phase status section:** add a new bullet:

```markdown
- **Phase G.3 shipped** (commit `<sha>`, 2026-05-XX): single-pass-per-page extraction. PDFEngine caches `extract_text` and `extract_text_blocks` per (doc, page). Filter 4 opens pdfplumber once per dispatch (was: per SCHEDULE page). Stage 13 trade-module wiring reuses cached PyMuPDF blocks instead of pdfplumber word re-extraction. TracePoint paper §2.1 architecture restored. Hard gate: Chipotle Tarpon dispatch completes successfully with same page count.
```

Update "Phase G.3 next-eligible" → either the new Next-1 from ITINERARY (likely "Phase G.5 render optimization" if it survived) or the next phase Daniel chooses.

Do not edit any other section.

### 9d — `backend/BLOCK_RUN.md`

Append a "Phase 12" section at the bottom (or whatever the next number is — read the file, increment from the highest existing). Match the existing format. Include:

- Branch
- Trigger (this phase's march orders)
- Files created (`G_3_GATE_REPORT.md`, `test_pdf_engine.py` if new)
- Files modified (`dispatch_gate.py`, `pdf_engine.py`, `test_pdf_engine.py` if existing, plus the four canon files)
- Vault SHA-1 verification (only `dispatch_gate.py` and `pdf_engine.py` change)
- Hard gate result (Chipotle completes, page count match)
- Sacred floor at session end (242/19/0)

### 9e — Commit canon updates

Single commit:
```
docs: G.3 canon updates

CHECKLIST: Phase G.3 row + handoff entry
ITINERARY: Section 1 (last 3) + Section 2 (next 6) refreshed; G.4 absorbed into G.3
PROJECT_CLAUDE: sacred floor 237→242, active phase block updated
BLOCK_RUN: Phase 12 entry added
```

---

## Step 10 — Push branch (~2 min)

```
git push -u origin phase2-v0.3-G3-single-pass-extraction
```

Verify push succeeded.

---

## Hard guardrails

1. **Sacred floor:** 237/19/0 at start, **≥242/19/0** at end (gain of at least 5 from new cache unit tests). New tests can only increase the count.
2. **Vault SHA-1s:** `roofing_module.py`, `roofing_vocabulary.py`, `glazing_module.py`, `glazing_vocabulary.py`, `debug_module.py` unchanged at session end. Only `dispatch_gate.py` and `pdf_engine.py` change.
3. **Two commits on this branch maximum:** code+tests+report (1) and canon updates (2). No mixed commits.
4. **No "while we're in there" cleanup:** No rename, no reformatting, no docstring polish, no type-hint additions outside the immediate changes.
5. **No git imports anywhere in test code:** if Claude Code's pytest tests `import git`, `import subprocess`, `os.system`, or read commit history / branch state, the phase is an automatic fail. Cache logic is in-process; no test needs git.
6. **No other bidsets touched in tests:** the 5 cache unit tests use synthetic PDFs. The hard gate uses Chipotle. No test loads Bearss, Silverleaf, Hampshire, or any other bidset.
7. **Wall-clock budget:** 90 minutes from branch creation. Exceed → STOP, ship what's clean, document partial progress.
8. **Karpathy step is mandatory:** failing cache tests in working tree before Step 4 implementation. If a test passes immediately, fix the test before proceeding.

---

## STOP conditions

1. **Page count differs between Step 1 baseline and Step 7 post-patch run.** That's a real regression — the cache or Filter 4 change altered dispatch behavior. STOP, do not commit, investigate.
2. **Sacred floor regresses** (any of the 237 prior tests now fails). Cache implementation altered behavior somewhere unexpected. STOP.
3. **Cache unit test passes immediately** before the implementation lands. Test was wrong. Fix the test, do not soften the spec.
4. **A vault SHA-1 changes** for any file other than `dispatch_gate.py` or `pdf_engine.py`. STOP, revert.
5. **Trade modules (`roofing_module.py`, `glazing_module.py`) get edited.** They're vault-ruled. STOP, revert. If their behavior needs adjustment for the new TextBlock granularity, that's a separate phase.
6. **Wall-clock budget exceeded** (90 min). STOP, document partial state, sign out with a "PARTIAL" header for Daniel review.
7. **You start drafting another scout.** This phase has zero scouts. The G.0.5 / G.0.8 reports are the input data. STOP and execute against them.
8. **You start writing a multi-bidset hard-gate harness.** Not in scope. Single bidset (Chipotle), single dispatch run. STOP if you find yourself iterating across bidsets in any way other than the unit tests' synthetic PDFs.

---

## Done when

- [ ] Branch `phase2-v0.3-G3-single-pass-extraction` exists on origin
- [ ] PDFEngine cache implemented and 5 unit tests passing
- [ ] Filter 4 pdfplumber lifecycle hoisted (single open per dispatch)
- [ ] Stage 13 trade-module wiring uses cached PyMuPDF blocks (no `extract_words` call)
- [ ] Sacred floor 242/19/0 (or higher if more tests added — never lower)
- [ ] Chipotle Tarpon dispatch runs successfully with same page count as pre-patch baseline
- [ ] BEFORE and AFTER wall-clock numbers documented in `backend/G_3_GATE_REPORT.md`
- [ ] Two commits on branch: code+tests+report (1), canon updates (2)
- [ ] CHECKLIST.md, ITINERARY.md, PROJECT_CLAUDE.md, BLOCK_RUN.md all updated
- [ ] Branch pushed
- [ ] Vault SHA-1s held except `dispatch_gate.py` and `pdf_engine.py`
- [ ] Sign-out announcement: "Signed out as Developer. Phase G.3 shipped clean. Chipotle dispatch verified. Wall-clock before: Xs, after: Ys. Canon updated. Branch pushed. Standing by."

---

## What this phase does NOT do (explicit non-goals)

- Does NOT add SQLite caching (that's PlanSetContext's job, already done; this phase is in-memory only)
- Does NOT modify trade modules (`roofing_module.py`, `glazing_module.py` stay frozen)
- Does NOT add a multi-bidset regression harness
- Does NOT fix Silverleaf 12/13/38/39 (separate Filter 1 phase, deferred)
- Does NOT touch frontend
- Does NOT add new dependencies (`pyproject.toml` stays unchanged)
- Does NOT fix any other slow path in dispatch beyond the three named changes

---

**End of march orders. Sign-in announcement first, then execute.**
