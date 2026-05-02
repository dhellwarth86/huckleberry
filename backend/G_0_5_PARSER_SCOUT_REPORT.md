# G.0.5 Parser Scout Report — Phase G Pre-Design Diagnostic

**Date:** 2026-05-01
**Phase:** G.0.5 (read-only parser observation)
**Branch:** `phase2-v0.3-G0-5-parser-scout` from `91f2e1c` (G.0 head)
**Executed by:** Claude Code (Developer session)
**Deliverable shape:** Single markdown report, 3 sections + 1 appendix. Zero code changes. Zero new tracked files except this report. Sacred floors held.

**What scout did:** Instrumented `dispatch_gate.run_dispatch` via runtime monkey-patching (no tracked code modified) on Silverleaf (broken case) and Bearss Ave (working case). Captured Filter 1 drawing-index parser behavior, audited every text-extraction call site by caller_func + caller_line + page + result-length, ran a parser-surface grep across `backend/core/`. Names three concrete bugs.

**What scout did NOT do:** No code changes. No new scripts in tracked paths (instrumentation script lives in `%TEMP%` and is not committed). No fix proposals.

---

## §1 — Drawing-Index Parser

### 1.1 What Filter 1 reads, where, and how

`_find_drawing_index_page()` at `dispatch_gate.py:187-261` is the index discoverer. It:

1. Scans the first `min(doc.page_count, 10)` pages (line 196).
2. For each page, calls `engine.extract_text(doc, page_idx)` (line 198) — full PyMuPDF text extraction.
3. Splits text by `\n` and walks line-by-line.
4. For each line, applies regex `_SHEET_NUM_RE` (`\b([A-Z]{1,2})-?(\d+[\.\d]*[A-Za-z]?)\b`, line 57) to detect candidate sheet numbers.
5. If a candidate matches, captures the rest-of-line as title (same-line format) or scans following lines for a title (split-line format).
6. **Validation:** if `len(unique_sheets) >= 10` (line 251), declares this page the drawing index and returns `(page_idx, deduped_entries)`.
7. If no page in the scan range hits 10 unique matches, returns `None` and Filter 1 falls back to per-page title-block scanning (lines 388-411).

If a page IS chosen as index, `_build_sheet_map_from_index()` at `dispatch_gate.py:336-356`:

1. Builds canonical-key lookup from index entries (`A-1.3` → `A1.3`).
2. Calls `_find_sheet_on_page(engine, doc, page_idx, known_keys=index_keys)` for **every page** in the document.
3. Only retains a page→sheet mapping if the returned sheet's canonical key appears in `index_keys` (line 351).
4. Pages whose returned sheet is NOT in `index_keys` are silently dropped from the sheet map.

### 1.2 Silverleaf (broken case) observed behavior

Instrumented run on `B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf`:

| Metric | Observed |
|--------|----------|
| Dispatch wall-clock | 137.2 s |
| Total pages | 40 |
| Sheet map source | `drawing_index` |
| Sheet map size | 10 |
| `page_to_sheet` size | **4** (10 − 6 unmapped) |

**Drawing index "found" on page 5.** Silverleaf has no real cover sheet or drawing index — page 5 is sheet `S101` (ROOF FRAMING PLAN). The 10 entries the parser captured:

| Entry | Title text returned | What it actually is |
|-------|--------------------|--------------------|
| `WD1` | (empty) | Window-detail callout marker |
| `L1` | (empty) | Line marker / level marker |
| `L2` | (empty) | Line marker |
| `L3` | (empty) | Line marker |
| `SW-3S` | (empty) | Shear-wall identifier |
| `HD8` | `2` | Hold-down mark + adjacent text |
| `MW-1` | (empty) | Mark-wall identifier |
| `S502` | `6` | Real sheet ref + adjacent text |
| `HD1` | `INDICATES SHEAR WALL HOLD-DOWN. SEE HOLD-DOWN` | Hold-down legend entry |
| `S101` | `ROOF FRAMING PLAN` | The page's own title block |

Eight of 10 entries are component markers from a structural framing/detail page, not sheet numbers. Only `S101` and `S502` are real sheets in the bidset. Most entries have **empty or junk `title_text`** — a real index would describe each sheet.

**Mapping result:** of 10 (mostly bogus) index entries, 4 mapped to pages:

| Index entry | Mapped to page | Reality |
|-------------|---------------|---------|
| `S502` | 4 | Real (page 4 is sheet S502) |
| `S101` | 5 | Real (page 5 is sheet S101) |
| `SW-3S` | 9 | Coincidental — page 9 contains "SW-3S" text but isn't sheet "SW-3S" |
| `WD1` | 25 | Coincidental — page 25 contains "WD1" callout |

The other 6 (`L1`, `L2`, `L3`, `HD8`, `MW-1`, `HD1`) were never matched on any page.

**The discarded data:** `_find_sheet_on_page()` was called on all 40 pages with `known_keys` set. It successfully parsed sheet numbers from **32 of 40 pages**:

```
page 0→S001, page 1→S002, page 2→S003, page 3→S010, page 4→S502,
page 5→S101, page 6→S501, page 7→S502, page 8→S503, page 9→SW-3S,
page 14→S101, page 15→G002, page 16→G003, page 17→G004, page 18→G101,
page 19→G101.1, page 20→G102, page 21→A001, page 22→A101, page 23→A102,
page 24→A103, page 25→WD1, page 26→A105, page 27→A106, page 28→WD1,
page 29→WD1, page 30→A301, page 31→A401, page 32→A501, page 33→WD1,
page 34→A601, page 35→A603
```

**Of these 32 successful page→sheet parses, 28 were discarded** because their canonical keys (`S001`, `S010`, `S501`, `S503`, `G002`, `G003`, `G004`, `G101`, `G101.1`, `G102`, `A001`, `A101`, `A102`, `A103`, `A105`, `A106`, `A301`, `A401`, `A501`, `A601`, `A603`, `S002`, `S003`) do not appear in the bogus index_keys set (`{WD1, L1, L2, L3, SW3S, HD8, MW1, S502, HD1, S101}`).

Eight pages (10, 11, 12, 13, 36, 37, 38, 39) returned `None` from `_find_sheet_on_page()` — these have no parseable sheet number on the page (per E.2.2 page types these are GENERAL_NOTES, SCHEDULE_SHEET, GENERAL_NOTES, DETAIL_SHEET, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN). The 4 UNKNOWN pages from §4 of the G.0 scout report are within this set.

### 1.3 Bearss Ave (working case) observed behavior

Instrumented run on `Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf`:

| Metric | Observed |
|--------|----------|
| Dispatch wall-clock | 544.2 s |
| Total pages | 91 |
| Sheet map source | `drawing_index` |
| Sheet map size | 47 |
| `page_to_sheet` size | **44** |

**Drawing index found on page 0 (the real cover sheet).** 47 entries, all real sheet numbers with substantive descriptive titles:

```
A-001 → COVER SHEET ...           A-101 → OVERALL FLOOR PLAN & ROOF PLANS
A-002 → CODE & LIFE SAFETY        A-201 → EXTERIOR ELEVATIONS
A-003 → ARCHITECTURAL SITE PLAN   A-401 → ROOF MISC. DETAILS
S-000 → COVER                     S-100 → GENERAL NOTES
S-200 → OVERALL FOUNDATION PLAN   S-210 → OVERALL ROOF FRAMING PLAN
M-001 → MECHANICAL GENERAL        M-100 → MECHANICAL PLANS
P-100 → PLUMBING FLOOR PLAN       E-101 → ELECTRICAL SITE PLAN
... (47 total)
```

44 of 47 entries mapped to pages. All 91 pages had `_find_sheet_on_page()` succeed (zero `None` returns). Only 3 entries (`C123`, `A-121`, `S-320`) failed to map — these likely don't appear at expected sheet-number positions in any page.

### 1.4 Why Silverleaf breaks and Bearss works — concrete

| Property | Bearss (works) | Silverleaf (breaks) |
|----------|---------------|---------------------|
| Has real cover/index page in first 10 pages? | Yes (page 0) | **No** |
| Index page detected by parser | page 0 | page 5 (S101 framing plan) |
| Number of `_SHEET_NUM_RE` regex matches on detected page | 47 | 10 (just over threshold) |
| Entries with empty/junk `title_text` | 0 of 47 | 8 of 10 |
| Entries that are real sheet numbers | 47 of 47 | 2 of 10 (S101, S502) |
| Pages parsed as having real sheet numbers | 91 of 91 | 32 of 40 |
| Of those, retained in sheet map | 44 (after dedup) | **4** (rest discarded for not matching bogus keys) |

### 1.5 Bug name (Bug 1)

**The Silverleaf drawing-index parser bug is caused by `_find_drawing_index_page()` (`dispatch_gate.py:187-261`) misidentifying a structural detail page (Silverleaf page 5, sheet `S101 ROOF FRAMING PLAN`) as the drawing index because the page contains ≥10 short alphanumeric tokens (component markers `HD1`, `HD8`, `MW-1`, `L1`, `L2`, `L3`, `WD1`, `SW-3S`, plus sheet refs `S101`, `S502`) that match the `_SHEET_NUM_RE` regex (`dispatch_gate.py:57`). The validation at line 251 (`len(unique_sheets) >= 10`) is the parser's only acceptance criterion — there is no check that the page resembles a tabular index, that entries have descriptive titles, or that the captured tokens actually correspond to sheets in the document.**

**Compounding cascade in `_build_sheet_map_from_index()` (`dispatch_gate.py:336-356`):** once a non-index page is accepted, every legitimate per-page sheet-number parse is filtered through `index_keys` at line 351. Of 32 pages where `_find_sheet_on_page()` returned a valid sheet number on Silverleaf, **28 were silently discarded** because the parsed sheet's canonical key (`S001`, `A101`, `G002`, etc.) does not appear in the bogus index_keys set built from the framing-plan markers. The Filter 1 fallback path (`run_filter_1` lines 388-411) that would have correctly mapped these 32 pages **never fires** because it is gated on `index_result is None` at line 388 — and `index_result` was non-None.

---

## §2 — Text Extractor Call Audit

### 2.1 Aggregate call counts

| Bidset | Pages | `extract_text_blocks` total | `extract_text` total | Total per-page |
|--------|-------|----------------------------|---------------------|----------------|
| Silverleaf | 40 | 274 | 85 | 8.97 |
| Bearss Ave | 91 | 636 | 96 | 8.04 |

### 2.2 Per-page call distribution

**`extract_text_blocks` calls per page:**

| Bidset | Min | Max | Avg | Distribution |
|--------|-----|-----|-----|--------------|
| Silverleaf | 6 | 8 | 6.85 | `{6: 7, 7: 32, 8: 1}` |
| Bearss | 6 | 8 | 6.99 | `{6: 2, 7: 88, 8: 1}` |

**`extract_text` calls per page:**

| Bidset | Min | Max | Avg | Distribution |
|--------|-----|-----|-----|--------------|
| Silverleaf | 1 | 4 | 2.12 | `{1: 1, 2: 34, 3: 4, 4: 1}` |
| Bearss | 1 | 3 | 1.05 | `{1: 87, 2: 3, 3: 1}` |

The 7-9 per-page estimate from G.0 is confirmed empirically: `extract_text_blocks` averages ~7 calls/page across both bidsets. `extract_text` per-page count differs because Silverleaf hits Strategy 2 of `_find_sheet_on_page` (line 291) more often (full-text fallback when title-block scan fails); Bearss's title blocks resolve at Strategy 1 with rare fallbacks.

### 2.3 Call sites observed (matches §1.1 of G.0 inventory)

**`extract_text_blocks` (10 sites observed via runtime tracing — matches G.0 §1.2 inventory exactly):**

| Caller `func:line` | Silverleaf calls | Bearss calls | Filter / stage |
|-------------------|------------------|--------------|----------------|
| `_find_sheet_on_page:276` | 40 | 91 | Filter 1 |
| `run_filter_2:444` | 40 | 91 | Filter 2 |
| `run_filter_4:836` | 40 | 91 | Filter 4 |
| `run_filter_3:597` | 40 | 91 | Filter 3 |
| `run_filter_5:894` | 40 | 91 | Filter 5 |
| `_classify_scope_pages:1229` | 40 | 91 | Scope scanner |
| `_collect_title_block_text:1089` | 33 | 89 | Architect profile (conditional on title_block zone existing) |
| `_extract_project_metadata:1014` | 1 | 1 | Metadata (cover page only) |
| `_find_sheet_on_page:397` | (not observed in this run) | — | Filter 1 fallback path (only fires when `index_result is None`) |
| `_extract_project_metadata:1065` | (not observed in this run) | — | Title-block fallback for project name (only fires when cover-page extraction failed) |

The 8 conditional sites that fire on every page produce 6×40 = 240 unconditional calls plus conditional `_collect_title_block_text` (33) plus `_extract_project_metadata` (1) = 274 — matches observed total exactly.

**`extract_text` (4 sites observed — matches G.0 §1.2 inventory):**

| Caller `func:line` | Silverleaf calls | Bearss calls | Filter / stage |
|-------------------|------------------|--------------|----------------|
| `run_filter_2:446` | 40 | 91 | Filter 2 (full text for classification) |
| `_find_sheet_on_page:291` | 38 | 3 | Filter 1 Strategy 2 (full-text scan for known key) |
| `_find_drawing_index_page:198` | 6 | 1 | Filter 1 index discovery |
| `_extract_project_metadata:1008` | 1 | 1 | Metadata (cover page) |
| `_find_sheet_on_page:306` | (not observed) | — | Strategy 4 fallback (last 10 lines) |

Strategy 2's high call count on Silverleaf (38) reflects the cascading damage: with bogus `index_keys`, almost every page exhausts Strategy 1's title-block search and falls through to a full-text scan that also fails. On Bearss (3 calls), title blocks resolve cleanly at Strategy 1.

### 2.4 Variance check — DO same-page calls return identical results?

This is the load-bearing question for whether a cache fix is trivial or has to handle variants.

**Silverleaf (40 pages):**
- Pages with VARYING `extract_text_blocks` block counts: **0 of 40**
- Pages with VARYING `extract_text_blocks` total character counts: **0 of 40**
- Pages with VARYING `extract_text` string lengths: **0 of 40**

**Bearss Ave (91 pages):**
- Pages with VARYING `extract_text_blocks` block counts: **0 of 91**
- Pages with VARYING `extract_text_blocks` total character counts: **0 of 91**
- Pages with VARYING `extract_text` string lengths: **0 of 91**

**Combined: 131 pages, ~910 same-page extraction calls, zero variance.** Every same-page call returns the same number of blocks AND the same total character count — both block-list shape and text content are identical across all calls in a single dispatch.

This is mechanical: PyMuPDF's `page.get_text("blocks")` and `page.get_text("text")` are deterministic stateless reads against an immutable `fitz.Document` — there is no caching layer to invalidate, no per-call randomness, no input that varies (only `(doc, page_num)` is passed and PyMuPDF holds the document open via `pdf_engine.PDFEngine.open` for the lifetime of the dispatch).

### 2.5 Cache-fix implication

A trivial memoization layer (e.g., `dict[page_idx, list[TextBlock]]` keyed by page index, populated on first call, served on subsequent calls) would be **safe** — no variants to handle, no invalidation needed, no edge cases for partial-extraction or per-caller customization (every caller passes the same `(doc, page_idx)` and gets the same result, full-stop).

Reduction in per-bidset call count if memoized:
- Silverleaf: 274 → 40 `extract_text_blocks` calls (-85.4%); 85 → ~40 `extract_text` calls (-53%)
- Bearss: 636 → 91 calls (-85.7%); 96 → ~91 calls (-5%)

PyMuPDF text extraction is sub-millisecond per call (per `PROFILE_DIAGNOSTIC_bearss-ave.md`), so the absolute time saving is small. The architectural value is removing a 7× redundancy that the code currently masks with cheap calls — and making future render-path changes simpler by reducing the call-site count from 14 to 2 (one cached read per kind per page).

---

## §3 — Parser Surface Sweep

Grep target: `backend/core/` for any text or PDF parsing that doesn't go through `PDFEngine` (PyMuPDF wrapper) or `pdfplumber`.

### 3.1 PDF library imports

```
fitz (PyMuPDF):
    backend/core/pdf_engine.py:21      import fitz  # PyMuPDF
    backend/core/pdf_engine.py:128     fitz.open(str(pdf_path))
    backend/core/pdf_engine.py:176     fitz.Matrix(zoom, zoom)
    backend/core/pdf_engine.py:183     fitz.Matrix(zoom * scale_down, ...)
    backend/core/pdf_engine.py:253     fitz.Rect(q)

pdfplumber:
    backend/core/dispatch_gate.py:47   import pdfplumber as _pdfplumber

Other PDF libraries (PdfReader, PdfFileReader, pypdf, pikepdf):
    NONE FOUND.
```

**Single fitz user:** `pdf_engine.py` — clean wrapper. No other module imports fitz.
**Single pdfplumber user:** `dispatch_gate.py` — confirmed three call sites from G.0 scout report §1.1.

### 3.2 Functions named like parsers/extractors — are they PDF parsers?

I grepped `backend/core/` for function names containing `text|page|extract|parse|read`. 30+ matches across the directory. Categorized below — none open or read PDFs.

**Post-processors on already-extracted text strings (regex helpers, not PDF parsers):**

| Function | File:line | Input | Notes |
|----------|-----------|-------|-------|
| `_find_spec_sections(text)` | dispatch_gate.py:1158 | `str` | Division 07 spec-section regex |
| `_find_manufacturers_in_text(text)` | dispatch_gate.py:1172 | `str` | Manufacturer-name regex against canonical list |
| `_find_material_markers(text)` | dispatch_gate.py:1187 | `str` | Membrane/insulation/metal markers regex |
| `_find_florida_signals(text)` | dispatch_gate.py:1198 | `str` | Florida regulatory tokens regex |
| `_find_architect_name(text)` | dispatch_gate.py:1203 | `str` | Architect-line regex |
| `_find_contractor_name(text)` | dispatch_gate.py:1213 | `str` | Contractor-line regex |
| `_classify_page_type(title_text, full_text)` | dispatch_gate.py:421 | `str, str` | Keyword classification |
| `_extract_cross_refs_on_page(text_blocks, ...)` | dispatch_gate.py:509 | `list[TextBlock]` | Operates on already-extracted blocks |
| `_find_legends_on_page(text_blocks, ...)` | dispatch_gate.py:665 | `list[TextBlock]` | Operates on already-extracted blocks |
| `_get_title_block_text(text_blocks, ...)` | dispatch_gate.py:161 | `list[TextBlock]` | Geometric filter on blocks |
| `_get_title_block_blocks(text_blocks, ...)` | dispatch_gate.py:174 | `list[TextBlock]` | Same |
| `_parse_dimension_to_feet(text)` | pdf_engine.py:422 | `str` | Architectural-dimension regex |
| `find_stated_areas(text)` | pdf_engine.py:468 | `str` | SF-string regex |
| `parse_scale_to_ft_per_inch(text)` | pdf_engine.py:498 | `str` | Scale-string regex |
| `find_roof_plan_scale(text_blocks)` | pdf_engine.py:514 | `list[TextBlock]` | Operates on already-extracted blocks |
| `_extract_text(item)` | architect_profile.py:62 | `str|list|dict|tuple` | **Not a PDF parser — a list/dict-to-string normalizer** |
| `extract_firm_candidates(title_block_text)` | architect_profile.py:77 | `str|list` | Firm-name regex |
| `_parse_dimension(text)` | glazing_module.py:137 | `Any` (via `_tb_text`) | Dimension regex on TextBlock text |
| `_extract_marks(text, kinds)` | glazing_module.py:217 | `str` | Mark-prefix regex |
| `_match_manufacturer(text)`, `_match_system(text)`, `_match_glass_type(text)`, `_classify_door_kind(text)`, etc. | glazing_module.py:243-323 | `str` | Vocabulary lookups |
| `_tb_text(tb)` | glazing_module.py:341 | `TextBlock-like` | Field accessor — calls `tb.text` |
| `_safe_print(text)` | debug_module.py:284 | `str` | Stdout writer |
| `_parse_source_tag(d)`, `_parse_scale(d)` | context.py:654-659 | `dict` | JSON-from-dict reconstructors (not PDF) |
| `from_json(cls, json_str)` | context.py:649 | `str` | JSON deserializer |

**Geometry analyzers operating on vector paths (not text or PDF directly):**

- `geometry_matrix.py:cluster_and_union_polygons(vector_paths, ...)` — operates on `VectorPath` objects produced by `pdf_engine.PDFEngine.extract_vectors`
- `geometry_matrix.py:find_area_from_dimensions(dimensions, ...)` — pure-math from dimension list

**Trade-module analyzers:**

- `roofing_module.RoofingModule.analyze(input)` and `glazing_module.GlazingModule.analyze(input)` consume `TradeModuleInput` objects containing already-extracted `text_blocks` and `tables`. They never open PDFs and never call PyMuPDF or pdfplumber directly.

### 3.3 Two indirect parser-shaped behaviors worth naming

**Bug 2 — Stage 13 redundant pdfplumber pass.** Stage 13 (`_run_trade_modules` at `dispatch_gate.py:1500-1616`) calls `pdf_page.extract_words()` (line 1547) on every page — this re-extracts word-level text from pdfplumber **after** PyMuPDF has already extracted blocks for that page 7× via Filters 1-5 + scope scanner + metadata. The pdfplumber word-list is structurally distinct from PyMuPDF's block list (per-word vs per-block, slightly different bbox semantics) so it's not a literal duplicate, but the *information* is fully present in the PyMuPDF blocks already in memory. Reuse of PyMuPDF blocks would eliminate this pass (~117 ms / page on high-content pages per `PROFILE_DIAGNOSTIC_bearss-ave.md`).

**Bug 3 — Filter 4 pdfplumber-per-page open/close.** `_parse_tables_on_page()` at `dispatch_gate.py:733-781` opens and closes pdfplumber once **per SCHEDULE_SHEET page** (line 739: `_pdfplumber.open(pdf_path)`, line 745: `pdf.close()`). Stage 13 takes the better path — single open at line 1523, single close at line 1597, all pages within. The Filter 4 path is ~N redundant opens for an N-schedule-page bidset (Silverleaf: 18 schedule pages → 18 opens; Bearss: 24 schedule pages → 24 opens). Each pdfplumber open re-parses the PDF object catalog. These two pdfplumber consumers (Filter 4 + Stage 13) could share a single open lifecycle.

These are not "rogue parsers" in the sense the question asked — they go through pdfplumber, the documented second engine. They are *redundant uses of the same engines*, named here because the surface sweep made them visible.

### 3.4 Verdict

**Two extraction families. No rogue parsers.**

1. **PyMuPDF (`fitz`) via `core.pdf_engine.PDFEngine`** — single import, single wrapper, used by every dispatch_gate filter for text/blocks/vectors/rendering.
2. **pdfplumber via `core.dispatch_gate`** — single import (line 47), three call sites (lines 739, 1523, 1547+1562).

Everything else operating on "text" or "pages" in `backend/core/` is post-processing of strings already extracted by one of these two engines, or analysis of structured objects (`TextBlock`, `VectorPath`, `Legend`, `TradeModuleInput`) downstream of the extraction. There is no third PDF engine, no custom binary PDF walker, no `open(path, "rb")` on PDFs anywhere in `backend/core/`.

---

## Appendix — Sacred-Floor Verification

### Pre-flight (2026-05-01, branch `phase2-v0.3-G0-5-parser-scout` from `91f2e1c`)

**Backend:** 230 passed, 19 skipped, 0 failed.

**SHA-1s (13 tracked files):**

| File | SHA-1 |
|------|-------|
| `backend/core/roofing_module.py` | `ae9e5b284191b45de419faacf11771da27a548f9` |
| `backend/core/glazing_module.py` | `52c014421915ec6a66b4a6860b71a0a3274920f2` |
| `backend/core/roofing_vocabulary.py` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` |
| `backend/core/glazing_vocabulary.py` | `64249c8ef5f7d9db50added3c9a40836cba356ea` |
| `backend/core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` |
| `backend/core/dispatch_gate.py` | `c206ff9e7e85eeee2c1c9bdaae8f0313308cd4a3` |
| `backend/api/main.py` | `5572ebe5a41dabc6bd96a9819bb410dde7e5fc4b` |
| `backend/api/routes/jobs.py` | `dc754ea591edba7d47533112da14bbf5d3eda451` |
| `backend/api/schemas/jobs.py` | `711a505c4bbdafd3ebcf709cacc85680aa29b3ff` |
| `backend/core/job_storage.py` | `2e0b1c6ebd2692c7eb89d18fe68959f64e348fca` |
| `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` | `f4aea9e7a64dd7a6774063eb438b74b1942fc278` |
| `backend/pyproject.toml` | `bcad957f02e6dd20bf2d1539126e397a4e7bde5c` |
| `frontend/package.json` | `aa47cfd098e70a994c3ca00db40970c9d2b9c296` |

### Post-flight (2026-05-01, end of session)

**Backend:** 230 passed, 19 skipped, 0 failed. **Match.**

**SHA-1s:** all 13 unchanged. **Match.**

### Instrumentation discipline note

Runtime monkey-patching was used to observe `_find_drawing_index_page`, `_build_sheet_map_from_index`, `_find_sheet_on_page`, `PDFEngine.extract_text_blocks`, and `PDFEngine.extract_text`. Patches were applied to the in-memory module objects from a temporary script at `%TEMP%\g05_silverleaf_trace.py` (NOT in any tracked path). The script does not modify tracked source files. Instrumentation persists only for the lifetime of the Python process. SHA-1 verification at session end confirms zero source modifications.

### Bidsets exercised

| Bidset | Wall-clock | Pages | Storage | Purpose |
|--------|-----------|-------|---------|---------|
| Silverleaf (B2607 AEA) | 137.2 s | 40 | `auto` | Broken-case observation |
| Bearss Ave Distribution Center | 544.2 s | 91 | `auto` | Working-case comparison |

`storage='auto'` was passed (no `job_id`), so Stage 13 trade modules ran but D.2 persistence was skipped.

---

**End of G.0.5 Parser Scout Report.**

Three concrete bugs named (drawing-index parser misidentification + cascade discard, Stage 13 pdfplumber word re-extraction, Filter 4 per-page pdfplumber open/close). Cache-fix path verified trivial via 131-page zero-variance check across two bidsets. Parser surface confirmed clean: two extraction families, no rogue PDF readers. Sacred floors held.
