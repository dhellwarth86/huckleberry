# G.0.8 Pre-Implementation Reconnaissance Report

**Date:** 2026-05-01
**Phase:** G.0.8 (read-only pre-implementation recon)
**Branch:** `phase2-v0.3-G0-8-pre-implementation-recon` from `cfdb806` (G.0.7 head)
**Executed by:** Claude Code (Developer session)
**Deliverable shape:** Single markdown report, 4 scout sections + consolidated recommendations. Zero code changes. Zero tracked files modified. Sacred floors held (230/19/0).

**Karpathy discipline:** Observe before proposing, name what's there, stop at uncertainty. Three of the four scouts are pure static reads of the codebase. Scout 3 includes one instrumented Bearss dispatch via `/tmp` monkey-patch script (the G.0.5 precedent — instrumentation script never enters the tree). All counts and timings reported are empirical, not estimated.

---

## §1 — Scout 1: Cache Detail Map

### 1.1 Method signatures

| Method | File:line | Signature | What it returns |
|--------|-----------|-----------|-----------------|
| `extract_text` | `pdf_engine.py:198-202` | `(pdf_doc: PDFDocument, page_num: int) -> str` | Full page text via PyMuPDF `page.get_text("text")` |
| `extract_text_blocks` | `pdf_engine.py:204-227` | `(pdf_doc: PDFDocument, page_num: int) -> list[TextBlock]` | List of `TextBlock` (text + bbox) via PyMuPDF `page.get_text("blocks")` |

Neither method takes any parameter beyond `(pdf_doc, page_num)`. No mode flags, no region filters, no rotation. The output is deterministic given a page index.

### 1.2 Call site inventory

| # | File:line | Caller | Filter/Stage | Page argument | Field usage downstream | Stored? |
|---|-----------|--------|--------------|---------------|------------------------|---------|
| 1 | `dispatch_gate.py:198` | `_find_drawing_index_page` | Filter 1 | loop `range(min(doc.page_count, 10))` | full text → split by `\n` → regex match | discarded after scan |
| 2 | `dispatch_gate.py:276` | `_find_sheet_on_page` | Filter 1 | single `page_idx` (Strategy 1) | filtered to title block region; `.text` only | local |
| 3 | `dispatch_gate.py:284` | `_find_sheet_on_page` | Filter 1 | (extract_text on title-block-collected text) | regex search | local |
| 4 | `dispatch_gate.py:291` | `_find_sheet_on_page` | Filter 1 (Strategy 2) | single `page_idx` (full-text fallback) | regex finditer | local |
| 5 | `dispatch_gate.py:301` | `_find_sheet_on_page` | Filter 1 (Strategy 3) | (extract_text on raw blocks) | regex search | local |
| 6 | `dispatch_gate.py:306` | `_find_sheet_on_page` | Filter 1 (Strategy 4) | conditional re-extract if `known_keys` was falsy | last 10 lines reverse scan | local |
| 7 | `dispatch_gate.py:311` | `_find_sheet_on_page` | Filter 1 (Strategy 4 inner) | (uses already-extracted text) | regex match | local |
| 8 | `dispatch_gate.py:320` | `_find_sheet_on_page` | Filter 1 | (text from blocks for last-10-lines) | regex search | local |
| 9 | `dispatch_gate.py:397` | `run_filter_1` (fallback) | Filter 1 fallback | loop `range(doc.page_count)` | passed to `_get_title_block_text` | local |
| 10 | `dispatch_gate.py:444` | `run_filter_2` | Filter 2 | loop all pages | passed to `_get_title_block_text` (filter to bottom-right 40%×40%) | local |
| 11 | `dispatch_gate.py:446` | `run_filter_2` | Filter 2 | same `page_idx` | classified for page type; passed to `parse_scale_to_ft_per_inch` | local |
| 12 | `dispatch_gate.py:597` | `run_filter_3` | Filter 3 | loop all pages | iterated for cross-ref patterns; uses `.text`, `.x0`, `.y0`, `.x1`, `.y1` | local |
| 13 | `dispatch_gate.py:836` | `run_filter_4` | Filter 4 | loop all pages | passed to `_find_legends_on_page` (sorted by position) | local |
| 14 | `dispatch_gate.py:894` | `run_filter_5` | Filter 5 | loop all pages | passed to zone-detection helpers | local |
| 15 | `dispatch_gate.py:1008` | `_extract_project_metadata` | Metadata | `range(min(2, doc.page_count))` | upper-cased for "COVER"/"PROJECT" keyword check | local |
| 16 | `dispatch_gate.py:1014` | `_extract_project_metadata` | Metadata | same | filtered to top half; text concatenation | local |
| 17 | `dispatch_gate.py:1065` | `_extract_project_metadata` | Metadata fallback | `range(min(5, doc.page_count))` | passed to `_get_title_block_blocks` | local |
| 18 | `dispatch_gate.py:1089` | `_collect_title_block_text` | Architect profile | iterate `ctx.pages` keys | filtered by zone bbox | local |
| 19 | `dispatch_gate.py:1229` | `_classify_scope_pages` | Scope scanner | loop all pages | counted; `" ".join(b.text)` concatenation | local |
| 20 | `pdf_engine.py:270` | `find_dimensions` | helper | single `page_num` | `.text` parsed for dimensions | filtered list |
| 21 | `pdf_engine.py:588` | `find_scale_from_any_page` | helper (scale fallback) | loop all pages | scanned for scale + "ROOF PLAN" | accumulated locally |

**Observed pattern:** every call uses only `(doc, page_idx)`. No call site passes a filter mode, region, or any other parameter that would alter the output for the same page.

### 1.3 Cache key shape

**Verdict: `dict[(pdf_path, page_idx), result]` is sufficient.**

- Key: `(pdf_path: str, page_idx: int)` — two values both methods already receive
- Value: `str` for `extract_text`, `list[TextBlock]` for `extract_text_blocks` (separate cache per method)
- No variant handling needed — no call site passes anything that changes the output shape
- Cache lifetime: per-dispatch (close cache when document closes)

### 1.4 Per-page call density (from G.0.5 §2.2)

For Bearss (91 pages):
- `extract_text_blocks`: 636 total calls = 6.99 per page
- `extract_text`: 96 total calls = 1.05 per page

A naive page-keyed cache would turn ~7 calls per page into 1 call per page — savings ≈ 6× reduction in PyMuPDF text-extraction work. Per G.0.5 §2.4, same-page calls return identical bytes (already verified), so cache safety is not in question.

---

## §2 — Scout 2: Regex Patch Blast Radius

### 2.1 Tests that touch sheet-number parsing

| Test | File:line | Asserts | Skipped? | Hybrid impact |
|------|-----------|---------|----------|---------------|
| `TestSinglePageCFA.*` (4 tests) | `test_dispatch.py:206-228` | Page classification, scale, dispatch completion on 1-page CFA roof | **SKIPPED** (`CFA_PDF` not in `test_plans/`) | N/A — does not run |
| `TestMultiPageVineStreet.test_sheet_map_populated` | `test_dispatch.py:245` | `len(ctx.sheet_map) >= 25` | **SKIPPED** (`VINE_PDF` not in `test_plans/`) | N/A — does not run |
| `TestMultiPageVineStreet.test_sheet_map_source_is_drawing_index` | `test_dispatch.py:248` | `ctx.sheet_map_source == "drawing_index"` | **SKIPPED** | N/A |
| `TestMultiPageVineStreet.test_roof_plan_classified` | `test_dispatch.py:251` | `>= 1` ROOF_PLAN page | **SKIPPED** | N/A |
| `TestMultiPageVineStreet.test_cross_references_resolved` | `test_dispatch.py:256` | resolution rate `> 0.40` | **SKIPPED** | N/A |
| `TestMultiPageVineStreet.test_legend_count` | `test_dispatch.py:263` | `>= 5` legends | **SKIPPED** | N/A |
| `TestMultiPageVineStreet.test_multiple_disciplines` | `test_dispatch.py:266` | `>= 3` disciplines | **SKIPPED** | N/A |
| `TestTacoBell.*` (4 tests) | `test_dispatch.py:375-392` | Page type, cross-refs, legend, scale | **SKIPPED** (`TACO_BELL_PDF` not in `test_plans/`) | N/A |
| `TestAEA.*` (4 tests) | `test_dispatch.py:395-412` | Page type, scale, building SF, legends | **SKIPPED** (`AEA_PDF` not in `test_plans/`) | N/A |
| `test_pipeline_dispatch.py::test_extract_sheet_number_typical` | `test_pipeline_dispatch.py:30-34` | `extract_sheet_number("DRAWING TITLE A-1.3")` etc. | runs | All test cases use `A-1.3`/`A-2.0`/`M-1.0` (decimal format) — **all match hybrid**. **No impact.** |
| `test_pipeline_dispatch.py::test_classify_page_roof_plan_title` | `test_pipeline_dispatch.py:49` | sheet_number == `"A-2.0"` | runs | A-2.0 has decimal — matches hybrid. **No impact.** |
| `test_pipeline_dispatch.py` (other tests) | various | discipline, classify, cross-refs, legends | runs | Synthetic fixtures; none use sub-3-digit no-decimal patterns. **No impact.** |
| `test_seeds_load.py::test_dispatch_seed_loads` | `test_seeds_load.py:28` | `isinstance(d.SHEET_NUMBER_REGEX, str)` | runs | Type check only. **No impact.** |
| `test_schema_round_trip.py::test_all_experiment_outputs_pass_schema` | runs | Validates 15 experiment JSONs against schema | runs | Schema validates structure, not regex behavior. JSONs are pre-built fixtures, not regenerated. **No impact on test runs.** |

**Confirmed via live pytest collection** (`pytest --collect-only`, then `-v` to see SKIPPED markers): all `TestSinglePageCFA`, `TestMultiPageVineStreet`, `TestTacoBell`, `TestAEA` tests are SKIPPED because the gating PDFs are not present in `test_plans/`. These tests contribute to the 19 skipped count, not the 230 passed count.

### 2.2 References to `_SHEET_NUM_RE` outside `dispatch_gate.py`

```
backend/core/dispatch_gate.py:57    _SHEET_NUM_RE = re.compile(...)    [definition]
backend/core/dispatch_gate.py:213   _SHEET_NUM_RE.match              [_find_drawing_index_page]
backend/core/dispatch_gate.py:234   _SHEET_NUM_RE.match              [_find_drawing_index_page]
backend/core/dispatch_gate.py:284   _SHEET_NUM_RE.search             [_find_sheet_on_page Strategy 1]
backend/core/dispatch_gate.py:292   _SHEET_NUM_RE.finditer           [_find_sheet_on_page Strategy 2]
backend/core/dispatch_gate.py:301   _SHEET_NUM_RE.search             [_find_sheet_on_page Strategy 3]
backend/core/dispatch_gate.py:311   _SHEET_NUM_RE.match              [_find_sheet_on_page Strategy 4]
backend/core/dispatch_gate.py:320   _SHEET_NUM_RE.search             [_find_sheet_on_page Strategy 4 inner]
```

The regex is module-private. **No external references exist** in `backend/core/` or `backend/tests/`.

### 2.3 Parallel pattern in `seeds/dispatch_seed.py`

A separate but pattern-equivalent regex lives at `backend/seeds/dispatch_seed.py:134`:

```python
SHEET_NUMBER_REGEX = r"[A-Z]{1,2}-?\d+[\.\d]*[A-Za-z]?"
```

Used by `backend/scripts/_pipeline/dispatch.py:50` (a Layer 1 / older pipeline path). **Hybrid does NOT touch this file.** This creates an inconsistency: Layer 1 retains the broad pattern; Layer 3 (`dispatch_gate.py`) gets the hybrid. Whether to harmonize is a separate decision — flagging here, not fixing.

### 2.4 Predicted test impact

**Under the current sacred floor (230/19/0): zero test failures expected from the hybrid change.**

All tests that exercise full dispatch on real PDFs are skipped because the PDFs aren't shipped with the repo. The synthetic-fixture tests in `test_pipeline_dispatch.py` use only well-formed sheet numbers (`A-1.3`, `A-2.0`, `M-1.0`) that the hybrid still matches.

**Uncertainty (Karpathy):** if the team later places `Vine_Street_Retail_Center_-_Kissimmee_-_Great_Southern_Constructors.pdf` in `backend/test_plans/`, the Vine Street tests would become live. Per G.0.7 §1.2, hybrid yields 42 unique tokens on Vine Street p2 (vs. 44 current) — well above the ≥10 detection threshold. The `test_sheet_map_populated` assertion is `>= 25`. The current experiment fixture (which is a JSON snapshot, not generated live by the test) shows `dispatch.sheet_map` has 106 entries with values like `"TS9D"`. Whether per-page sheet-number extraction (`_find_sheet_on_page`) drops below 25 mapped pages under the hybrid cannot be predicted from static analysis — would require running the dispatch with the hybrid applied. **Documented as uncertainty, not asserted.**

---

## §3 — Scout 3: Filter 4 Open/Close Cost

### 3.1 Static analysis of `_parse_tables_on_page`

Function at `dispatch_gate.py:733-781`. Pure-per-page: takes `(pdf_path, page_idx)`, opens pdfplumber, accesses `pdf.pages[page_idx]`, calls `extract_tables()`, closes, then constructs `Legend` objects from the materialized list. No state escapes the function — both `legends` and `raw_tables` are detached from the document handle.

Reuse barriers checklist:
- Document/page reference retention after `with` block: **none** (data converted to list before close)
- Cross-page state dependency: **none** (pure-per-page)
- Concurrent access: **none** (single-threaded, called sequentially in `run_filter_4` loop at line 835)
- Repeated same-page calls: **none** (one call per SCHEDULE_SHEET page per dispatch)
- pdfplumber internal state: **opaque, but Stage 13 already demonstrates safe single-handle reuse** (lines 1523-1597 open once, access pages 0..91 of Bearss without issue)

### 3.2 Empirical timing — instrumented Bearss dispatch

Method: `/tmp` monkey-patch wrapping `_parse_tables_on_page` to record per-call wall-clock; ran `run_dispatch(bearss_pdf)` once. No tracked code changes.

| Metric | Value |
|--------|-------|
| Total dispatch wall-clock | **184.2 s** |
| Total pages in Bearss | 91 |
| SCHEDULE_SHEET pages | 24 |
| Filter 4 calls | 24 |
| **Total time inside `_parse_tables_on_page`** | **145.0 s** |
| Filter 4 share of total dispatch | **78.7%** |
| Avg per call | 6.04 s |
| Min per call | 0.45 s (page 87) |
| Max per call | 17.64 s (page 12) |

Per-call breakdown (sample of higher-cost pages):

| page | elapsed | legends | tables |
|------|---------|---------|--------|
| 12 | 17.6 s | 85 | 101 |
| 58 | 17.1 s | 83 | 106 |
| 34 | 14.9 s | 53 | 69 |
| 80 | 14.3 s | 54 | 70 |
| 38 | 9.5 s | 55 | 90 |
| 84 | 9.1 s | 55 | 90 |
| 86 | 7.7 s | 91 | 107 |
| 40 | 7.6 s | 88 | 102 |

The per-call cost scales with table count, not just open-overhead. Cost includes: pdfplumber.open (object catalog parse) + pdfplumber.pages array build + `page.extract_tables()` (the heavy lift). Hoisting `pdfplumber.open()` only eliminates the open-overhead component (~ object catalog parse). It does not eliminate `extract_tables()` itself.

### 3.3 Reuse barriers verdict

**No mechanical barriers to hoisting `pdfplumber.open()` out of `_parse_tables_on_page` and into `run_filter_4`.** Stage 13 (`dispatch_gate.py:1523-1597`) is the proven precedent: same pdfplumber, all pages, no issues.

**Uncertainty (Karpathy):** The expected savings from open-hoisting is the per-open object-catalog parse cost, which is unknown from this measurement (the timing data lumps open + extract_tables together). The total Filter 4 savings could be modest (a fraction of 145 s) or substantial (most of 145 s if open is dominant). **Empirical confirmation requires implementing the change and re-measuring.**

### 3.4 Note on Bearss timing variance

This run measured Bearss at 184.2 s. G.0.5 §1.3 measured 544.2 s. The 3× difference is unexplained from the data available — possibly cold cache vs warm, machine load, or other transient factors. Filter 4's share-of-total stays load-bearing regardless: even at 184 s total, 145 s in Filter 4 is the dominant cost in this run.

---

## §4 — Scout 4: Stage 13 pdfplumber Retire Path

### 4.1 What Stage 13 actually consumes

Stage 13 (`_run_trade_modules`, `dispatch_gate.py:1500-1616`) opens pdfplumber, then for each page:

```python
pdf_page = pdf.pages[page_idx]
words = pdf_page.extract_words() or []
for w in words:
    text_blocks.append(TextBlock(
        text=str(w.get("text", "")),
        x0=float(w.get("x0", 0.0)),
        y0=float(w.get("top", 0.0)),
        x1=float(w.get("x1", 0.0)),
        y1=float(w.get("bottom", 0.0)),
        page=page_idx,
    ))
```

**Five fields read:** `text`, `x0`, `top`, `x1`, `bottom`. All other pdfplumber word fields (`fontname`, `size`, `direction`, `upright`, `doctop`, `width`, `height`, `object_type`) are **never accessed**.

Downstream, trade modules (`roofing_module.py`, `glazing_module.py`) consume `TextBlock` via two helpers: `_tb_text(tb)` reads `.text`; `_tb_center(tb)` computes `((x0+x1)/2, (y0+y1)/2)` from the bbox. No font, size, or direction usage anywhere.

### 4.2 Field comparison

| pdfplumber `extract_words()` field | Read by Stage 13? | PyMuPDF source | Gap |
|-------------------------------------|-------------------|----------------|-----|
| `text` | yes | `get_text("words")` tuple[4]; `get_text("dict")` span `.text` | none |
| `x0` | yes | `get_text("words")` tuple[0]; span `.bbox[0]` | none |
| `top` (→ `y0`) | yes | `get_text("words")` tuple[1]; span `.bbox[1]` | none |
| `x1` | yes | `get_text("words")` tuple[2]; span `.bbox[2]` | none |
| `bottom` (→ `y1`) | yes | `get_text("words")` tuple[3]; span `.bbox[3]` | none |
| `fontname` | no | span `.font` (in "dict" mode) | unused |
| `size` | no | span `.size` (in "dict" mode) | unused |
| `direction`, `upright`, `doctop`, `width`, `height`, `object_type` | no | n/a | unused |

### 4.3 Verdict — PyMuPDF is sufficient

All five fields Stage 13 reads are available from PyMuPDF. The cleanest swap is:

- **Option A (word-level):** `page.get_text("words")` returns word-level tuples `(x0, y0, x1, y1, text, block_no, line_no, word_no)`. This is the closest match to pdfplumber's per-word output. No font/size, but those aren't read.
- **Option B (block-level reuse):** Reuse the `extract_text_blocks` results already cached/computed in Filters 1-5 — these are PyMuPDF "blocks" output, slightly coarser than words but already in memory. `TextBlock` already has the right shape (text + bbox). This is the path the Scout 1 cache enables.

**Granularity caveat (Karpathy):** PyMuPDF "blocks" returns paragraph-level text chunks; "words" returns individual words. Stage 13 currently uses pdfplumber words (individual). Trade module logic (e.g., `roofing_module._count_callouts` dedupes by 5-pt position tolerance) is calibrated to word-level positions. **If switching to "blocks" granularity, the dedup tolerance and clustering may need recalibration.** "words" granularity should drop in cleanly. Confirming this is a runtime experiment, not a static-analysis finding.

### 4.4 Path forward summary

Either replacement path eliminates Stage 13's pdfplumber dependency. The "words" path is the safe drop-in (same granularity); the "blocks" path is faster (data already extracted) but needs trade-module verification. **Stop here per Karpathy:** observation done, decision belongs to the implementation phase.

---

## §5 — Consolidated Recommendations

### 5.1 Three candidate fixes from G.0.5

| Bug | Fix | Status after recon |
|-----|-----|--------------------|
| Bug 1 (drawing-index parser misidentifies framing-plan as index) | Hybrid regex at `dispatch_gate.py:57` | Static-validated and corpus-validated (G.0.6, G.0.7); blast radius confirmed minimal (§2) |
| Bug 2 (Stage 13 pdfplumber for word data) | Replace `pdf_page.extract_words()` with PyMuPDF `get_text("words")` or reuse cached blocks | API gap is zero (§4); granularity caveat for "blocks" path; "words" path is drop-in |
| Bug 3 (Filter 4 pdfplumber per-page open/close) | Hoist `pdfplumber.open()` out of `_parse_tables_on_page` into `run_filter_4` | No mechanical barriers (§3); savings magnitude unmeasured |

### 5.2 Ship-first recommendation: Bug 1 (hybrid regex)

**Why first:**
- Smallest blast radius — single-line change, regex is module-private (zero external references), all real-PDF tests are skip-gated and won't surface a regression in the 230/19/0 floor
- Greatest validation depth — three prior phases (G.0.5 diagnostic, G.0.6 paper experiment, G.0.7 corpus sweep) confirm the hybrid is corpus-clean across all 15 bidsets
- No new dependencies, no test changes, no architectural disruption
- Inversely-correlated with the other two fixes: doesn't depend on caching or pdfplumber retirement to land

**Caveat to flag at PR time:** Layer 1 (`seeds/dispatch_seed.py:134`) retains the broad regex. The hybrid creates a Layer1/Layer3 inconsistency. Decision belongs to the team — harmonize, leave separate, or deprecate Layer 1.

### 5.3 Hidden-risk fix: Bug 3 (Filter 4 open/close)

Filter 4 is **78.7% of dispatch wall-clock on Bearss** (145.0 s of 184.2 s). The optimization target is huge — but the savings ceiling is unknown:

- The 145 s lumps `pdfplumber.open()` + `extract_tables()`. Hoisting eliminates only the open portion.
- If `extract_tables()` is the dominant cost (likely on table-heavy pages 12, 58, 34, 80 which take 14-17 s each), savings could be modest — perhaps 10-30%.
- If `open()` per-page is dominant on cheaper pages (pages 41, 87 at 0.45 s each — close to pure open cost), savings on those pages could be near-100%, but the absolute time saved is small.

**The investigation needed before shipping:** measure `pdfplumber.open()` alone vs. `extract_tables()` alone in isolation, on one Bearss page. If open is <1 s and `extract_tables()` is 5-15 s, the bug is real but the headline-savings is bounded. Static analysis doesn't answer this.

### 5.4 Defer-without-consequence fix: Bug 2 (Stage 13 pdfplumber retire)

Per the G.0.5 audit (Stage 13 uses one open for all pages), Bug 2's open-overhead is already O(1) per dispatch — not per-page. The cost is one `pdfplumber.open()` call total in Stage 13. Retiring it saves a one-time PDF object-catalog parse. **This is rounding error compared to Filter 4's 145 s.** Bug 2's value is not performance — it's removing a dependency. Reasonable to defer.

### 5.5 Cross-cutting: Scout 1 caching layer

The cache shape is trivial (`dict[(pdf_path, page_idx), result]`) and the call density is ~7 `extract_text_blocks` per page across filters. A single cache shared across Filters 1-5 + scope scanner + metadata extraction would reduce text-extraction work ~6×. This is independent of Bugs 1-3 and orthogonal to all of them. **It's a clean, testable, isolated change.** Lower risk than Bug 3, less validated than Bug 1.

### 5.6 Suggested ship order

1. **Bug 1 (hybrid regex)** — ready to ship. Most-validated, lowest risk.
2. **Cache layer** — ready to design, low risk, well-scoped. Can land independently.
3. **Bug 3 (Filter 4 hoist)** — needs one micro-benchmark (open vs extract_tables in isolation) before committing.
4. **Bug 2 (Stage 13 pdfplumber retire)** — defer until trade-module granularity is verified at runtime.

### 5.7 What this report does not say

Karpathy: name what's there, don't propose fixes you can't validate.

- **Not measured:** isolated `pdfplumber.open()` cost vs `extract_tables()` cost. Only the lumped total.
- **Not measured:** dispatch wall-clock variance (this run 184.2 s vs G.0.5's 544.2 s — 3× spread, cause unknown).
- **Not validated:** real-PDF test impact of the hybrid (the gating PDFs aren't in `test_plans/` — would need them present to run live).
- **Not analyzed:** whether `seeds/dispatch_seed.py` Layer 1 path is still alive and shipping data, or vestigial. The hybrid may or may not need to harmonize there.
- **Not evaluated:** trade-module granularity sensitivity to swapping pdfplumber words → PyMuPDF words/blocks. Static analysis confirms field coverage; runtime confirms behavior equivalence.

These are honest gaps, not scope failures. Each should be closed before the corresponding fix ships.
