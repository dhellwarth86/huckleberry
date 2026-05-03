# Phase G.3 — Single-pass-per-page extraction — Gate Report

**Branch:** `phase2-v0.3-G3-single-pass-extraction`
**Base commit:** `e7a3884` (`docs: G.2 canon updates`)
**Date:** 2026-05-03
**Hard gate:** Chipotle Tarpon dispatch completes successfully with same page count.

---

## Sacred floor

| Stage | Backend tests |
|---|---|
| Pre-patch | 237 passed, 19 skipped, 0 failed |
| Post-patch | **242 passed, 19 skipped, 0 failed** |
| Delta | +5 (new `TestPDFEngineCache` class — see `backend/tests/test_pdf_engine.py`) |

Zero regressions on the prior 237. Sacred floor 237 → 242/19/0.

---

## Vault SHA-1s

| File | Pre-patch | Post-patch | Status |
|---|---|---|---|
| `backend/core/dispatch_gate.py` | `09bc0340de08f588ba1afc1f95e339489d9e79ba` | `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` | **changed** (intentional) |
| `backend/core/pdf_engine.py` | `e872f69eb60f99d84dca0085c86ee48900b4e74e` | `daf06dd266d52983a0c761669f8af1ed825088a7` | **changed** (intentional) |
| `backend/core/roofing_module.py` | `ae9e5b284191b45de419faacf11771da27a548f9` | `ae9e5b284191b45de419faacf11771da27a548f9` | held ✓ |
| `backend/core/glazing_module.py` | `52c014421915ec6a66b4a6860b71a0a3274920f2` | `52c014421915ec6a66b4a6860b71a0a3274920f2` | held ✓ |
| `backend/core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | held ✓ |
| `backend/core/roofing_vocabulary.py` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` | held ✓ |
| `backend/core/glazing_vocabulary.py` | `64249c8ef5f7d9db50added3c9a40836cba356ea` | `64249c8ef5f7d9db50added3c9a40836cba356ea` | held ✓ |

Only the two files this phase scopes were touched.

---

## Pre-patch call inventory (read from `e7a3884`)

### `engine.extract_text` call sites in `dispatch_gate.py`

| Line | Function / Filter | Use of result |
|---|---|---|
| 199 | `_classify_page_type_for_filter_2` (Filter 2 helper) | full-text scan for page-type keywords |
| 292 | `run_filter_2` | full-text scan for known title-block keys |
| 307 | `run_filter_2` (fallback path) | full-text used when no known keys hit |
| 453 | `run_filter_3` | full-text for trade scoring |
| 1017 | cover-page inference helper | full-text on cover page |

5 call sites total.

### `engine.extract_text_blocks` call sites in `dispatch_gate.py`

| Line | Function / Filter | Use of result |
|---|---|---|
| 277 | `run_filter_2` | structured blocks for title-block analysis |
| 398 | `run_filter_2` (per-trade scoring loop) | structured blocks for trade-keyword counting |
| 451 | `run_filter_3` | structured blocks for trade scoring |
| 606 | `run_filter_1` | structured blocks for cross-ref extraction |
| 845 | `run_filter_4` | structured blocks for legend detection |
| 903 | `run_filter_5` | structured blocks for zone classification |
| 1023 | cover-page inference helper | structured blocks on cover page |
| 1074 | scope-detection helper | structured blocks for project scope |
| 1098 | scope-detection helper (sister page) | structured blocks for project scope |
| 1238 | post-filter aggregation | structured blocks for cross-page reconciliation |

10 call sites total. On a 39-page PDF (Chipotle), that's up to 390 PyMuPDF block extractions when each call re-extracts. Most pages run through Filters 1-5 + helpers, hitting the same blocks 6-9 times.

### `pdfplumber.open` call sites in `dispatch_gate.py`

| Line | Function | Lifecycle |
|---|---|---|
| 748 | `_parse_tables_on_page` | opened + closed per call (called per SCHEDULE_SHEET page from Filter 4) — **hoist target** |
| 1532 | `_run_trade_modules` | opened once outside per-page loop — already correct (Stage 13 wiring) |

### `pdf_page.extract_words` call site in `dispatch_gate.py`

| Line | Function | Use of result |
|---|---|---|
| 1556 | `_run_trade_modules` per-page loop | builds `text_blocks` for `TradeModuleInput` — **retire target** |

### `PDFEngine.extract_text` and `PDFEngine.extract_text_blocks` (pre-patch)

- `extract_text` (`pdf_engine.py:198`): `return page.get_text("text")` — fresh extraction every call, no cache.
- `extract_text_blocks` (`pdf_engine.py:204`): builds a fresh `list[TextBlock]` from `page.get_text("blocks")` every call, no cache.

---

## Post-patch state

### Three changes landed

1. **`PDFEngine` cache** (`pdf_engine.py`): `self._extract_cache: dict` keyed on `(id(pdf_doc), page_num, method_name)`. `extract_text` and `extract_text_blocks` consult the cache before extracting; on hit they return the same Python object as the prior call. `engine.close(pdf_doc)` purges all entries with that doc's `id()` before closing the underlying fitz doc.

   **Invalidation choice:** hooked into the existing `engine.close(pdf_doc)` method rather than introducing a new `close_doc(doc)` name. Single call site in dispatch (`dispatch_gate.py:1740`), so the explicit-close path was already in place — no cosmetic rename needed.

2. **Filter 4 pdfplumber hoist** (`dispatch_gate.py`): `run_filter_4` now opens pdfplumber **once at the top** of the per-page loop with a `try`/`finally` guaranteeing close-once. `_parse_tables_on_page` was refactored to accept the open pdfplumber Document instead of a path. The `if not _pdfplumber: return [], []` guard remains for environments without pdfplumber installed; an exception during the top-level `open` is now surfaced as a single dispatch warning rather than failing per-page.

3. **Stage 13 retire `extract_words`** (`dispatch_gate.py`): `_run_trade_modules` now uses `engine.extract_text_blocks(doc, page_idx)` for `TradeModuleInput.interior_text_blocks` (was: `pdf_page.extract_words()`). The cached call is free because Filters 1, 2, 4 already extracted those blocks earlier in the same dispatch. The pdfplumber `extract_tables()` fallback for non-schedule pages is preserved unchanged — only the word extraction was retired.

### Post-patch call counts per dispatch (Chipotle, 39 pages)

| Resource | Pre-patch | Post-patch |
|---|---|---|
| PyMuPDF `extract_text` calls per dispatch | up to 5 × 39 = 195 | **39 max** (one per page; cache hit thereafter) |
| PyMuPDF `extract_text_blocks` calls per dispatch | up to 10 × 39 = 390 | **39 max** (one per page; cache hit thereafter) |
| `pdfplumber.open` calls per dispatch (Filter 4) | once per SCHEDULE page | **1** (hoisted) |
| `pdfplumber.open` calls per dispatch (Stage 13) | 1 (was already correct) | 1 (unchanged) |
| `pdf_page.extract_words()` calls per dispatch | 39 | **0** (retired) |
| `pdf_page.extract_tables()` calls (non-schedule fallback) | up to 39 | unchanged (only when `not raw_tables`) |

Chipotle had **0 SCHEDULE_SHEET pages** in this dispatch, so the Filter 4 pdfplumber.open in pre-patch was actually 0 here, but the hoist still removes the per-call open/close for any bidset that does have schedule pages.

---

## Wall-clock — Chipotle Tarpon

Single bidset, single PDF, two runs each (cold + warm). Hardware: Windows 11, local Python 3.14.

| Run | Pre-patch | Post-patch | Delta |
|---|---|---|---|
| Cold | 58.36s | 50.26s | −8.10s (−13.9%) |
| **Warm (canonical)** | **58.72s** | **50.05s** | **−8.67s (−14.8%)** |

Page count: 39 (BEFORE) = 39 (AFTER) ✓

Per the march orders, wall-clock is **recorded but is not a pass/fail criterion** — Daniel is the wall clock.

---

## Hard gate

**Pass.** Dispatch on Chipotle Tarpon (Shell) completes successfully both pre- and post-patch, returning 39 pages either way. Single dispatch warning is byte-identical between the two runs:

```
Filter 4 quality gate: 21 of 53 legends removed (32 kept)
```

No new warnings, no new errors, no STOPs fired post-patch.

---

## Trade-module output delta

Pre-patch and post-patch dispatch on Chipotle both produce **0 entries** in `ctx.trade_module_outputs`. Trade modules were not firing on Chipotle's pages even on the unmodified pipeline — this is a pre-existing condition, not a regression introduced by Phase G.3. Recorded here without opinion attached, as the march orders specified ("That's data for Daniel to review, not a problem to fix in this phase").

The shape change (pdfplumber word-level → PyMuPDF paragraph-level `TextBlock`s on `TradeModuleInput.interior_text_blocks`) had no observable effect on Chipotle outputs because the modules weren't firing here regardless. On bidsets where they do fire, the new granularity should match keyword phrases (e.g. "TPO ROOFING", "ALUMINUM STOREFRONT") at least as well as the prior word-by-word feed — `_callout_blob` and `_interior_blob` flatten via `_tb_text(tb)` and search via `keyword in blob`-style matching, so paragraph-level blocks are if anything *better* for multi-word phrases.

---

## STOPs fired

None.

---

## Sacred-floor verification, end of phase

```
242 passed, 19 skipped, 1 warning in 3.31s
```

`242 ≥ 242` ✓. Floor held on every prior test. New tests (`TestPDFEngineCache` × 5) pass.

---

## Done-when checklist

- [x] Branch `phase2-v0.3-G3-single-pass-extraction` exists locally (push pending)
- [x] PDFEngine cache implemented and 5 unit tests passing
- [x] Filter 4 pdfplumber lifecycle hoisted (single open per dispatch)
- [x] Stage 13 trade-module wiring uses cached PyMuPDF blocks (no `extract_words` call)
- [x] Sacred floor 242/19/0
- [x] Chipotle Tarpon dispatch runs successfully with same page count as pre-patch baseline (39 = 39)
- [x] BEFORE and AFTER wall-clock numbers documented
- [ ] Two commits on branch (code+tests+report = next step; canon updates after)
- [ ] CHECKLIST / ITINERARY / PROJECT_CLAUDE / BLOCK_RUN updated (next commit)
- [ ] Branch pushed (final step)
- [x] Vault SHA-1s held except `dispatch_gate.py` and `pdf_engine.py`
