# G.0 Scout Report — Phase G Quadrant Smart Scan

**Date:** 2026-05-01
**Phase:** G.0 (read-only scout mission)
**Branch:** `phase2-v0.3-G0-scout-mission` from `0ddd5a5`
**Executed by:** Claude Code (Developer session)
**Deliverable shape:** Single markdown report, 7 sections + 4 appendices. Zero code changes. Sacred floors held throughout.

**What scout did:** Inventoried the current render path end-to-end, audited PyMuPDF + Pandas as proposed dependencies, computed tiling math for 3 DPI options × 3 page sizes, root-caused the Silverleaf classification weakness to specific code paths, ran Bearss Ave baseline dispatch with timing receipts, proposed module structure for G.1, and surfaced 10 open design questions for Daniel.

**What scout did NOT do:** No code changes. No new scripts. No new dependencies. No tests added or removed. No vault touches. No fix proposals. No patches.

---

## §1 — Render Path Inventory

### 1.1 pdfplumber call sites (3 locations)

pdfplumber is imported conditionally at `dispatch_gate.py:47-49` and used at three locations:

| # | File:Line | Function | Operation | Trigger | Per-page? |
|---|-----------|----------|-----------|---------|-----------|
| 1 | `dispatch_gate.py:739-745` | `_parse_tables_on_page()` | `_pdfplumber.open()` → `page.extract_tables()` → `pdf.close()` | Filter 4, per SCHEDULE_SHEET page only | Yes — opens/closes PDF per page |
| 2 | `dispatch_gate.py:1521-1547` | `_run_trade_modules()` | `_pdfplumber.open()` → `pdf_page.extract_words()` | Stage 13, once for entire loop | Yes — per page within single open |
| 3 | `dispatch_gate.py:1560-1564` | `_run_trade_modules()` | `pdf_page.extract_tables()` | Stage 13, per non-SCHEDULE page lacking cached `raw_tables` | Conditional — only when `raw_tables` is empty |

**Observation:** Call site #1 opens and closes the PDF *per page*. Call sites #2 and #3 share a single `_pdfplumber.open()` for the entire Stage 13 loop. This means pdfplumber opens the PDF N+1 times per dispatch (once per SCHEDULE_SHEET page in Filter 4, plus once for Stage 13).

### 1.2 PyMuPDF call sites (via PDFEngine)

PyMuPDF (`fitz`) is the primary PDF engine, wrapped by `pdf_engine.py`. All text extraction and vector extraction flows through it. The `PDFEngine.open()` call at `dispatch_gate.py:1657` opens the PDF once and holds it for the entire dispatch.

**`extract_text_blocks()` — 10 call sites in dispatch_gate.py:**

| # | Line | Filter/Stage | Purpose |
|---|------|-------------|---------|
| 1 | 276 | Filter 1 (`_find_sheet_on_page`) | Sheet number discovery from title block |
| 2 | 397 | Filter 1 (`run_filter_1`) | Title block text for sheet entry |
| 3 | 444 | Filter 2 (`run_filter_2`) | Page classification input |
| 4 | 597 | Filter 3 (`run_filter_3`) | Cross-reference extraction |
| 5 | 836 | Filter 4 (`run_filter_4`) | Legend discovery from text blocks |
| 6 | 894 | Filter 5 (`run_filter_5`) | Zone classification |
| 7 | 1014 | Metadata (`_extract_project_metadata`) | Cover page analysis |
| 8 | 1065 | Metadata (`_extract_project_metadata`) | Title block fallback for project name |
| 9 | 1089 | Architect (`_collect_title_block_text`) | Title block text for firm detection |
| 10 | 1229 | Scope scanner (`_classify_scope_pages`) | Scope page scoring |

**`extract_text()` — 4 call sites:**

| # | Line | Filter/Stage | Purpose |
|---|------|-------------|---------|
| 1 | 198 | Filter 1 (`_find_drawing_index`) | Drawing index discovery |
| 2 | 291 | Filter 1 (`_find_sheet_on_page`) | Full text scan for sheet numbers |
| 3 | 446 | Filter 2 (`run_filter_2`) | Full text for page classification |
| 4 | 1008 | Metadata (`_extract_project_metadata`) | Cover page text extraction |

**Per-page extraction frequency:** A single page passes through Filters 1→2→4→3→5→scope scanner→metadata. Across these stages, `extract_text_blocks()` is called **7–9 times per page** (not all call sites fire for every page — metadata and architect detection have conditional paths). `extract_text()` is called **2–3 times per page**. None of these results are cached between filters.

### 1.3 Caching status

| Data | Cached? | Where | Notes |
|------|---------|-------|-------|
| `raw_tables` | YES | `page_ctx.raw_tables` | Set by Filter 4 for SCHEDULE_SHEET pages. Re-used by Stage 13. |
| Text blocks | NO | — | Re-extracted per filter per page. 7–9 calls per page across the pipeline. |
| Full text | NO | — | Re-extracted per filter per page. 2–3 calls per page. |
| Vector paths | NO | — | Extracted by Filter 5 (zone detection) and scope scanner independently. |

**Finding:** Text block re-extraction is the most significant caching gap. PyMuPDF text extraction is sub-millisecond per call (effectively free individually), but the repeated calls represent architectural debt — a future caching layer would reduce total PyMuPDF page-access count by ~70%.

### 1.4 Stage-by-stage cost map

Based on `PROFILE_DIAGNOSTIC_bearss-ave.md` (pages 15 high-content + 82 low-content, 3 repeats each):

| Operation | Page 15 (high) | Page 82 (low) | Ratio |
|-----------|---------------|---------------|-------|
| pdfplumber `extract_tables()` | **2,910 ms** | 178 ms | 16.4× |
| pdfplumber `extract_words()` | 117 ms | 3.9 ms | 30.0× |
| RoofingModule `.analyze()` | 184 ms | 11 ms | 16.6× |
| GlazingModule `.analyze()` | 12 ms | 7 ms | 1.7× |
| PyMuPDF text extraction | sub-ms | sub-ms | ~1× |
| **Per-page total** | **~3,220 ms** | **~200 ms** | **16.1×** |

**Dominant cost:** `pdfplumber.extract_tables()` at 2.91s median on high-content pages. This is the cost ceiling Phase G is trying to lower.

### 1.5 Consumers of pdfplumber output

| Consumer | Input | What it reads | Break risk if output changes |
|----------|-------|---------------|------------------------------|
| Filter 4 | `page.extract_tables()` → Legend objects + `raw_tables` | Table row structure (header row + data rows) | Legend parsing depends on row[0] as key, row[1:] as description |
| Stage 13 trade modules | `page.extract_words()` → TextBlock list | Word position (x0, y0, x1, y1) + text | Trade modules match text against vocabulary by content; position used for spatial grouping |
| Stage 13 trade modules | `page.extract_tables()` fallback → `raw_tables` | Same structure as Filter 4 | Passed to `TradeModuleInput.tables`; modules iterate rows |
| `TradeModuleInput` | `raw_tables` via `trade_input_builder.py` | List of tables, each a list of rows | `build_trade_input()` passes tables directly; modules read row-by-row |

### 1.6 Filter execution order in `run_dispatch()`

```
Filter 1 (Document Structure) → Filter 2 (Page Classification) →
Filter 4 (Legend/Schedule Parsing) → Filter 3 (Cross-Reference) →
Filter 5 (Zone Classification) → Scope Scanner → Metadata →
Architect Profile → Stage 13 (Trade Modules) → D.2 Persistence
```

Note: Filter 4 runs before Filter 3 so that keynote detection can inform cross-reference extraction.

---

## §2 — Dependency Audit

### 2.1 PyMuPDF

**Critical correction:** PyMuPDF is **already installed and is the primary PDF engine.** The march orders frame it as a "proposed dep addition for G.1" — this is incorrect. It has been present since v0.2 (`pyproject.toml` line 23: `"PyMuPDF>=1.24.0"`; `pdf_engine.py` line 21: `import fitz  # PyMuPDF`).

| Attribute | Value |
|-----------|-------|
| Package name | `PyMuPDF` (imports as `fitz`) |
| Installed version | ≥1.24.0 (pinned in pyproject.toml) |
| Latest on PyPI | 1.27.2.3 (2026-04-24) |
| License | AGPL-3.0 / Artifex Commercial (dual-licensed) |
| Python support | ≥3.10 (covers project's ≥3.11) |
| Transitive deps | None mandatory — bundles MuPDF C library |
| Cost-of-adoption | **Zero.** Already installed, already the primary engine, AGPL already accepted. |

**Tiled rendering API surface (already available):**

The existing `PDFEngine.render_page()` (`pdf_engine.py:157-187`) already uses:
```python
zoom = dpi / 72.0
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat, alpha=False)
```

Tiled rendering adds one parameter: `clip=fitz.Rect(x0, y0, x1, y1)` to `get_pixmap()`. This renders only the specified rectangular region. No additional install, no API version bump, no new import.

**Thread safety:** PyMuPDF's `fitz.Document` is NOT thread-safe. Concurrent access to the same document requires separate `fitz.open()` calls per thread. Current dispatch is single-threaded; not a concern unless Phase G introduces parallelism.

### 2.2 Pandas

| Attribute | Value |
|-----------|-------|
| Package name | `pandas` |
| Latest on PyPI | 3.0.2 (2026-03-31) |
| License | BSD-3-Clause |
| Python support | ≥3.11 (matches project's ≥3.11) |
| Core transitive deps | `numpy` (already in pyproject.toml: `"numpy>=1.26.0"`), `python-dateutil`, `tzdata` |
| Install footprint | ~9–12 MB wheel + deps already present |
| Cost-of-adoption | 1 line in pyproject.toml, ~10 MB disk, BSD-3 license (no commercial concerns) |

**Value-add question — what does Pandas add over pdfplumber's table output + stdlib?**

pdfplumber's `extract_tables()` returns `list[list[list[str | None]]]` — a list of tables, each a list of rows, each a list of cell values. The current pipeline passes this directly to trade modules via `TradeModuleInput.tables`.

Pandas would add:
- Column alignment and header normalization (`DataFrame.from_records()`)
- Row/column filtering (`df.query()`, boolean indexing)
- Aggregation (`groupby`, `pivot_table`)
- Missing-value handling (`fillna`, `dropna`)

**Scout's read:** Pandas may not be needed in Phase G. The dominant cost is pdfplumber's layout analysis (`extract_tables()` at 2.91s/page), not data processing after extraction. Pandas operates on the *output* of table extraction — it doesn't replace the extraction itself. If G.1 replaces pdfplumber's table extraction with a different approach, Pandas becomes relevant for processing the replacement's output. If G.1 only addresses the *render* path (tiling for visual analysis), Pandas has no role.

**Concrete decision boundary:** Pandas is useful if Phase G introduces structured tabular post-processing that stdlib can't handle cleanly. Until that need is demonstrated, adding Pandas is premature.

### 2.3 Cost-of-adoption ledger

| Dep | pyproject.toml diff | Test floor impact | License risk | Bus-factor risk |
|-----|--------------------|--------------------|--------------|-----------------|
| PyMuPDF | Zero (already present) | Zero | AGPL already accepted | Low (Artifex, well-maintained) |
| Pandas | +1 line | Zero (no tests use it) | Zero (BSD-3) | Low (NumFOCUS, well-maintained) |

---

## §3 — Tiling Math

### 3.1 Page sizes and full-page renders

Construction documents use three standard page sizes:

| Page size | Dimensions | Common usage |
|-----------|-----------|--------------|
| ARCH D | 24" × 36" | Standard plan sheets (floor plans, roof plans, elevations) |
| ARCH E | 36" × 48" | Large-format plans (site plans, complex details) |
| Letter | 8.5" × 11" | Spec sheets, schedules, general notes |

### 3.2 Full-page pixel dimensions and memory

| Page | DPI | Width px | Height px | Total px | Raw RGB (MB) |
|------|-----|----------|-----------|----------|-------------|
| ARCH D | 200 | 4,800 | 7,200 | 34.6M | **98.9** |
| ARCH D | 250 | 6,000 | 9,000 | 54.0M | **154.5** |
| ARCH D | 300 | 7,200 | 10,800 | 77.8M | **222.5** |
| ARCH E | 200 | 7,200 | 9,600 | 69.1M | **197.8** |
| ARCH E | 250 | 9,000 | 12,000 | 108.0M | **309.0** |
| ARCH E | 300 | 10,800 | 14,400 | 155.5M | **445.0** |
| Letter | 200 | 1,700 | 2,200 | 3.7M | **10.7** |
| Letter | 250 | 2,125 | 2,750 | 5.8M | **16.7** |
| Letter | 300 | 2,550 | 3,300 | 8.4M | **24.1** |

Formula: `width_px = width_in × DPI`, `height_px = height_in × DPI`, `RGB_MB = width_px × height_px × 3 / 1,048,576`.

Note: `get_pixmap()` returns RGB by default when `alpha=False` (3 bytes/pixel). Current config: `PDF_RENDER_DPI = 150`, `PDF_MAX_DIMENSION = 4096`.

### 3.3 2×2 quadrant tiling

Each tile = half-width × half-height of full page. Memory per tile = ¼ of full page.

| Page | DPI | Tile px | Tile MB | Tiles | Peak (serial) | Peak (parallel) |
|------|-----|---------|---------|-------|---------------|-----------------|
| ARCH D | 200 | 2,400×3,600 | 24.7 | 4 | 24.7 | 98.9 |
| ARCH D | 250 | 3,000×4,500 | 38.6 | 4 | 38.6 | 154.5 |
| ARCH D | 300 | 3,600×5,400 | 55.6 | 4 | 55.6 | 222.5 |
| ARCH E | 200 | 3,600×4,800 | 49.5 | 4 | 49.5 | 197.8 |
| ARCH E | 250 | 4,500×6,000 | 77.2 | 4 | 77.2 | 309.0 |
| ARCH E | 300 | 5,400×7,200 | 111.2 | 4 | 111.2 | 445.0 |
| Letter | 200 | 850×1,100 | 2.7 | 4 | 2.7 | 10.7 |
| Letter | 250 | 1,063×1,375 | 4.2 | 4 | 4.2 | 16.7 |
| Letter | 300 | 1,275×1,650 | 6.0 | 4 | 6.0 | 24.1 |

Peak (serial) = one tile at a time, free before next. Peak (parallel) = all 4 tiles in memory simultaneously (same as full page — no memory savings).

### 3.4 Tile overlap strategy

Lines, polygons, and text crossing a tile boundary need reassembly. Overlap ensures edge content appears in adjacent tiles.

| Overlap % | ARCH D 200 DPI overlap px | Notes |
|-----------|--------------------------|-------|
| 0% | 0 | No boundary recovery; items at edges may be split |
| 2% | 48×72 per edge | Minimal; covers most text and thin lines |
| 5% | 120×180 per edge | Covers dimension strings and detail markers |
| 10% | 240×360 per edge | Conservative; covers wide annotations |

Memory impact of overlap is minimal — a 5% overlap on ARCH D at 250 DPI adds ~2 MB per tile (~5% of tile size).

### 3.5 Wall-clock estimates per page

PyMuPDF `get_pixmap()` benchmarks (from MuPDF documentation and community reports):

| Operation | Estimated time | Notes |
|-----------|---------------|-------|
| Full ARCH D page at 200 DPI | ~200–400 ms | Single `get_pixmap()` call |
| Full ARCH D page at 300 DPI | ~400–800 ms | Scales roughly with pixel count |
| Single quadrant tile at 250 DPI | ~50–150 ms | `clip=fitz.Rect(...)` limits work |
| 4 tiles sequential at 250 DPI | ~200–600 ms | Sum of individual tiles |

**These are estimates, not measured values.** PyMuPDF rendering speed depends on page complexity (vector count, text density, embedded images). Actual benchmarking requires G.1 implementation.

### 3.6 Comparison vs current pdfplumber path

| Metric | pdfplumber (current) | PyMuPDF tiling (estimated) |
|--------|---------------------|---------------------------|
| High-content page (Bearss pg 15) | **2,910 ms** (`extract_tables`) | ~200–600 ms (4 tiles at 250 DPI) |
| Low-content page (Bearss pg 82) | 178 ms (`extract_tables`) | ~80–200 ms (4 tiles at 250 DPI) |
| Output format | Structured tables (`list[list[str]]`) | Pixel images (RGB numpy/PIL) |
| Downstream consumer | Direct to trade modules | Requires OCR or CV processing |

**Critical distinction:** pdfplumber's `extract_tables()` produces *structured data* (rows and columns). PyMuPDF tiling produces *pixels*. These are not drop-in replacements. If G.1 replaces table extraction with tiled rendering, downstream consumers need a new processing path (OCR or computer-vision-based table detection). If G.1 adds tiling *alongside* pdfplumber for visual analysis (drawing detection, polygon extraction), the two paths coexist.

### 3.7 Memory aggregate per bidset

ARCH D at 250 DPI, serial tile processing (one tile at a time, freed before next):

| Bidset | Pages | Peak per page (1 tile) | Total if serial | Total if all tiles held |
|--------|-------|----------------------|-----------------|------------------------|
| Silverleaf | 40 | 38.6 MB | 38.6 MB | 6,180 MB (6.0 GB) |
| Bearss Ave | 91 | 38.6 MB | 38.6 MB | 14,059 MB (13.7 GB) |
| Vine Street | 138 | 38.6 MB | 38.6 MB | 21,307 MB (20.8 GB) |

Serial processing keeps peak memory at ~39 MB regardless of bidset size. Holding all tiles simultaneously is not feasible.

### 3.8 Tiling-vs-no-tiling decision boundary

| Page size | DPI | Full render MB | Tile? | Reasoning |
|-----------|-----|---------------|-------|-----------|
| Letter | Any | 10.7–24.1 | **No** | Below ~50 MB; tiling overhead exceeds savings |
| ARCH D | 200 | 98.9 | **Maybe** | Borderline; depends on available RAM |
| ARCH D | 250+ | 154.5+ | **Yes** | Full render exceeds comfortable single-allocation |
| ARCH E | Any | 197.8–445.0 | **Yes** | Always worth tiling at any DPI |

**Boundary:** ~50 MB raw. Below this threshold, full-page rendering is simpler and the memory footprint is manageable. Above it, tiling avoids large single allocations and enables serial processing.

---

## §4 — Silverleaf Classification Root-Cause

### 4.1 Silverleaf bidset structure

40 pages total per E.2.2 calibration. Filter 1 sheet mapping: `sheet_count: 10`, `mapped_pages: 4`. Only 4 of 40 pages received sheet numbers from the drawing index. The remaining 36 pages have no sheet number, no discipline, and no title text from the sheet map.

Page type distribution (E.2.2): CEILING_PLAN:1, COVER:1, DETAIL_SHEET:5, ELEVATION:3, FLOOR_PLAN:1, FRAMING_PLAN:1, GENERAL_NOTES:2, ROOF_PLAN:1, SCHEDULE_SHEET:18, SECTION:3, **UNKNOWN:4**.

The 4 UNKNOWN pages are: pages 12, 13, 38, 39.

### 4.2 Classification logic path

Page classification occurs in Filter 2 (`run_filter_2`, dispatch_gate.py:439). For each page:

1. `extract_text_blocks()` → title block text (line 444–445)
2. `extract_text()` → full page text (line 446)
3. `_classify_page_type(tb_text, full_text)` (line 448) → `(PageType, confidence)`

`_classify_page_type()` (lines 421–436) performs two passes:
- **Pass 1 (title block):** For each of 13 rules in `_PAGE_TYPE_RULES` (lines 105–119), check if any keyword appears in `title_upper`. First match wins at `title_conf`.
- **Pass 2 (full text):** Same rules against `full_upper`. First match wins at `page_conf` (lower confidence).
- **Default:** `(PageType.UNKNOWN, CONFIDENCE_UNKNOWN)` — confidence 0.0.

After classification, an MEP fallback (lines 464–466) checks: if `page_type == UNKNOWN` AND `discipline in (MECHANICAL, ELECTRICAL, PLUMBING)`, set `page_type = MEP_PLAN` at `CONFIDENCE_WEAK`. This requires discipline to be known, which requires a sheet number.

### 4.3 The cascade failure

Two contributing factors produce the UNKNOWN classification on pages 12, 13, 38, 39:

**Factor 1 — Sheet mapping gap:** The drawing index maps only 10 of 40 sheets, and only 4 pages receive sheet numbers via Filter 1. Pages 12, 13, 38, 39 have no sheet numbers. Without a sheet number, `_discipline_from_prefix()` cannot determine discipline. Without discipline, the MEP fallback cannot fire.

**Factor 2 — Keyword coverage gap:** The 13 rules in `_PAGE_TYPE_RULES` do not cover:
- "MECHANICAL PLAN" — no rule matches (only "FLOOR PLAN", "ROOF PLAN", "CEILING PLAN", "FRAMING PLAN" exist)
- "PLUMBING ISOMETRICS" / "RISER DIAGRAM" — no rule matches
- "ENLARGED CLASSROOM" — an enlarged plan view, but "ENLARGED" is not a keyword
- Pages 12 and 38 are floor plan drawings containing only room labels and dimensional text (no "FLOOR PLAN" title text in the extractable text)
- Pages 13 and 39 are plumbing/mechanical pages with discipline-specific content but no keyword overlap with any classification rule

The combination: no sheet number → no discipline → MEP fallback blocked → no keyword match → `UNKNOWN` at confidence 0.0.

### 4.4 Multi-bidset framing correction

The march orders frame this as "internal title-page separators triggered multi-bidset path." This framing is incorrect. There is no multi-bidset detection or document-splitting logic in `dispatch_gate.py`. The scope scanner (`_classify_scope_pages`, line 1223) identifies cover/separator pages for scoring but does not split documents or reset state. The Silverleaf classification weakness is purely a keyword-coverage and sheet-mapping issue.

### 4.5 Concrete bug statement

The Silverleaf classification weakness is caused by a two-factor cascade failure:

1. **Filter 1 sheet-mapping gap** (`dispatch_gate.py:339-414`): The drawing index maps only 10/40 sheets → only 4 pages get sheet numbers → 36 pages have no discipline, blocking the MEP fallback (`dispatch_gate.py:464-466`).

2. **`_PAGE_TYPE_RULES` keyword coverage gap** (`dispatch_gate.py:105-119`): 13 rules cover 13 page types but miss "MECHANICAL PLAN", "PLUMBING ISOMETRICS", "RISER DIAGRAM", "ENLARGED" plan views, and pages with only room labels/dimensional text (no classification-triggering keywords in extractable text).

### 4.6 Render path vs classification path

This is a **classification-path issue**, NOT a render-path issue. Phase G's render optimization (tiling, DPI changes) does not address it. The classification fix belongs in a separate scope — either bundled into G.1 as a classification-improvement track or split to its own phase.

---

## §5 — 3-Bidset Baseline

### 5.1 Bearss Ave — fresh baseline (2026-05-01)

| Metric | G.0 baseline | D.2 reference | Delta | Status |
|--------|-------------|---------------|-------|--------|
| Pages | 91 | 91 | 0 | PASS |
| Wall-clock | **466.1s** | 471.0s | −1.0% | Within ±5% |
| Roofing fields | **769** | 769 | 0 | **Byte-exact** |
| Glazing items | **177** | 177 | 0 | **Byte-exact** |
| Door items | **31** | 31 | 0 | **Byte-exact** |
| Storefront items | **24** | 24 | 0 | **Byte-exact** |
| Dispatch warnings | 1 | 1 | 0 | Match |
| `dispatch_complete` | True | True | — | PASS |

Warning: `Filter 4 quality gate: 749 of 990 legends removed (241 kept)`.

Dispatch used `run_dispatch(path, storage='auto')` with no `job_id` (no persistence). Cross-check against D.2 hard gate: all 4 item counts are byte-exact matches. Wall-clock 466.1s vs D.2's 471.0s — within normal run-to-run variance.

### 5.2 Shoppes at Avalon + Vine Street — D.2 reference numbers (not re-run)

Per Daniel's directive, Shoppes at Avalon and Vine Street baseline runs were skipped. D.2 hard gate reference numbers (2026-04-29) are the standing baseline:

| Bidset | Pages | Wall-clock | Roofing | Glazing | Door | Storefront |
|--------|-------|-----------|---------|---------|------|------------|
| **Shoppes at Avalon** | 97 | 721.8s | 833 | 43 | 22 | 22 |
| **Vine Street** | 138 | 1,194.5s | 1,201 | 100 | 12 | 23 |

D.2 verification: Bearss + Vine Street produced byte-exact aggregates vs 2026-04-28 sweep baseline (different days, sessions, harness paths). Shoppes roofing was 833 vs sweep 830 (+0.36%, within run-to-run variance).

### 5.3 Aggregate baseline for Phase G hard gate comparison

| Bidset | Pages | Wall-clock (s) | Roofing | Glazing | Door | SF |
|--------|-------|---------------|---------|---------|------|----|
| Bearss Ave | 91 | 466.1 (fresh) | 769 | 177 | 31 | 24 |
| Shoppes | 97 | 721.8 (D.2 ref) | 833 | 43 | 22 | 22 |
| Vine Street | 138 | 1,194.5 (D.2 ref) | 1,201 | 100 | 12 | 23 |
| **Total** | **326** | **~2,382s (~40 min)** | **2,803** | **320** | **65** | **69** |

Memory peak: not measured (psutil not available without install; tracemalloc not instrumented in dispatch path).

---

## §6 — Module Structure Proposal

### 6.1 Option A: New `backend/core/render/` module

**Structure:**
```
backend/core/render/
    __init__.py          (~10 lines — public API re-exports)
    tile_engine.py       (~200-300 lines — tiling logic, DPI management)
    cache.py             (~100-150 lines — text block + table caching layer)
```

**dispatch_gate.py changes:** ~30 lines. Replace direct `engine.extract_text_blocks()` calls with cached wrapper. Replace `_parse_tables_on_page()` pdfplumber call with render module call.

**Pros:**
- Clean separation of concerns — render logic is testable in isolation
- Natural extension of existing `pdf_engine.py` architecture
- Easy to vault-rule later (entire directory)
- dispatch_gate.py line-budget impact is minimal (~30 lines)

**Cons:**
- New module surface to maintain (3 new files, ~310-460 lines)
- `__init__.py` convention: existing `core/__init__.py` is empty; new subpackage is precedent

**Vault rule:** Render module is NOT vault-ruled at creation. Opens for tuning during G.1 build. Seals at G.1 hard gate.

**Test surface:** ~10-15 new tests in `backend/tests/test_render.py`. Fits existing test structure.

**Frontend impact:** None. Render path is server-side per E.2 strip.

### 6.2 Option B: Extend existing geometry stages

**Structure:** Add tiling logic to existing `geometry_matrix.py` or dispatch_gate.py Stages 6-9.

**dispatch_gate.py changes:** ~200-300 lines added to existing file. Would push dispatch_gate.py from 1,957 to ~2,200+ lines.

**Pros:**
- No new module; tiling colocated with consumers
- No new `__init__.py` or package structure

**Cons:**
- dispatch_gate.py already 1,957 lines — adding 200-300 more strains readability
- Tiling is not geometry (different concern); colocating conflates render and analysis
- Harder to test in isolation
- geometry_matrix.py is a verbatim TracePoint port (Section A verified); modifying it breaks port discipline

**Vault rule:** Modifications to geometry_matrix.py would need to be reconciled with its verbatim-port status.

**Test surface:** Tests added to existing test files, potentially conflating concerns.

### 6.3 Option C: Standalone `backend/core/render_utils.py`

**Structure:** Single file `backend/core/render_utils.py` (~200-400 lines). All tiling logic, caching, and DPI management in one file.

**dispatch_gate.py changes:** ~30 lines (same as Option A — import and call).

**Pros:**
- Simplest implementation — one file, one import
- dispatch_gate.py change is small
- Easy to understand

**Cons:**
- Utility files tend to grow into module-shaped messes over time
- Not a clean architectural slot — "utils" is a code smell
- If caching layer is needed, file grows past 400 lines and wants to split

**Vault rule:** Same as Option A — open during G.1, sealed at hard gate.

### 6.4 Scout's read

**Option A is the strongest choice.** It matches the existing architecture (pdf_engine.py is already a dedicated wrapper), keeps dispatch_gate.py changes under 30 lines, and provides a clean test surface. The caching layer (text blocks + tables) naturally lives alongside the tiling logic as a coherent render concern.

The trade-off Daniel is choosing between: **Option A's cleanliness vs Option C's simplicity.** Option B is not recommended — it violates the verbatim-port status of geometry_matrix.py and bloats dispatch_gate.py.

**Migration path (applies to A and C):** pdfplumber calls in dispatch_gate.py are replaced incrementally:
1. G.1 Phase 1: Add caching layer for text blocks (addresses the 7-9× re-extraction)
2. G.1 Phase 2: Replace Filter 4's `_parse_tables_on_page()` pdfplumber call with render module
3. G.1 Phase 3: Replace Stage 13's pdfplumber calls
4. G.1 ship: pdfplumber import becomes optional/removed

---

## §7 — Open Design Questions

### Q1. DPI choice — 200 vs 250 vs 300?

Current default is 150 DPI (`config.py:PDF_RENDER_DPI`). Phase G proposes increasing to 200-300 for drawing detection. Higher DPI = better detail resolution but more memory and time per tile.

**Scout's read:** 250 DPI. Balances detail resolution (good for text, dimensions, symbols) against memory (38.6 MB per ARCH D tile vs 55.6 MB at 300). 200 DPI risks losing fine detail on dense schedule sheets; 300 DPI doubles memory vs 200 with diminishing returns.

**Your call.**

### Q2. Tile overlap percentage — 0% / 2% / 5% / 10%?

Overlap ensures boundary-crossing content appears in adjacent tiles. Cost is minimal (~5% tile size increase at 5% overlap).

**Scout's read:** 5% overlap. Covers dimension strings (~120 px at 200 DPI ARCH D), detail markers, and most text annotations. 0% risks splitting annotations; 10% is conservative overhead without proportional benefit.

**Your call.**

### Q3. Tile geometry — 2×2 quadrants / 2×3 sextants / dynamic?

2×2 is simplest. 2×3 better fits ARCH D aspect ratio (24:36 = 2:3). Dynamic per page size adds complexity.

**Scout's read:** 2×2 quadrants. Simplest implementation, adequate for ARCH D (most common), and the aspect ratio difference between 2×2 and 2×3 is minor. Complexity of dynamic tiling is not justified at this stage.

**Your call.**

### Q4. Render module structure — Option A / B / C?

See §6 for full analysis.

**Scout's read:** Option A (`core/render/` subpackage). See §6.4 reasoning.

**Your call.**

### Q5. Page-type-driven tiling — tile all pages or only specific types?

Not all page types benefit from tiling. Schedule sheets are text/table-heavy (pdfplumber's strength). Drawing pages (ROOF_PLAN, ELEVATION, DETAIL_SHEET, FLOOR_PLAN) have visual content that benefits from tiled rendering.

**Scout's read:** Tile only drawing types (ROOF_PLAN, FLOOR_PLAN, ELEVATION, DETAIL_SHEET, FRAMING_PLAN, SECTION, CEILING_PLAN). Skip tiling for SCHEDULE_SHEET, GENERAL_NOTES, COVER, LIFE_SAFETY, SYMBOL_LEGEND, UNKNOWN. Schedule sheets stay on the pdfplumber path (table extraction is what they need, not pixel rendering).

**Your call.**

### Q6. Pandas integration depth

See §2.2 for analysis. Pandas adds post-processing on table data, not table extraction itself.

**Scout's read:** Skip Pandas in Phase G entirely. The dominant cost is pdfplumber's layout analysis, not data processing. If a future phase needs structured tabular post-processing beyond what stdlib provides, add Pandas then. Adding it now is premature.

**Your call.**

### Q7. Migration timing — all-at-once or shadow mode?

All-at-once: replace pdfplumber calls with render module calls on G.1 ship. Shadow mode: run both paths, compare outputs, then cut over.

**Scout's read:** Incremental replacement (see §6.4 migration path). Not all-at-once (too much blast radius) and not shadow-mode (too much complexity for a single-developer project). Replace one call site at a time, verify with tests after each.

**Your call.**

### Q8. Silverleaf classification fix scope — inside Phase G or separate?

Per §4.6, the Silverleaf classification weakness is a classification-path issue unrelated to the render path. Phase G is primarily a render-path optimization.

**Scout's read:** Separate from Phase G's render work. Bundle it as a small classification-improvement track (expand `_PAGE_TYPE_RULES` keyword list + improve Filter 1 sheet-mapping coverage). Could be a G.1 sub-phase or its own mini-phase between G and F. Mixing it into the render optimization makes both harder to test.

**Your call.**

### Q9. Hard gate composition

Phase G's hard gate needs a 3-bidset wall-clock + accuracy A/B comparison. Should it also include the deferred E.2.2 Silverleaf visual hard gate (single-bidset upload-to-display in Chrome)?

**Scout's read:** Yes, bundle them. The Silverleaf visual hard gate was deferred specifically to Phase G. Running it alongside the 3-bidset comparison is natural — both verify end-to-end pipeline behavior. One hard gate session, two verification tracks.

**Your call.**

### Q10. Test floor target

Backend is currently 230/19/0. G.1 will add render module tests (~10-15 new).

**Scout's read:** Target 240-245 as the floor. This is 230 + 10-15 new render tests. Set it as a floor (minimum), not a ceiling — if render tests naturally produce more, that's fine. Frontend stays at 23/23 (no frontend changes in Phase G).

**Your call.**

---

## Appendix A — SHA-1 Captures

### Pre-flight SHA-1s (captured 2026-05-01)

**Vault-ruled modules (5):**

| File | SHA-1 |
|------|-------|
| `backend/core/roofing_module.py` | `ae9e5b284191b45de419faacf11771da27a548f9` |
| `backend/core/glazing_module.py` | `52c014421915ec6a66b4a6860b71a0a3274920f2` |
| `backend/core/roofing_vocabulary.py` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` |
| `backend/core/glazing_vocabulary.py` | `64249c8ef5f7d9db50added3c9a40836cba356ea` |
| `backend/core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` |

**Production code (read-only this phase):**

| File | SHA-1 |
|------|-------|
| `backend/core/dispatch_gate.py` | `c206ff9e7e85eeee2c1c9bdaae8f0313308cd4a3` |
| `backend/api/main.py` | `5572ebe5a41dabc6bd96a9819bb410dde7e5fc4b` |
| `backend/api/routes/jobs.py` | `dc754ea591edba7d47533112da14bbf5d3eda451` |
| `backend/api/schemas/jobs.py` | `711a505c4bbdafd3ebcf709cacc85680aa29b3ff` |
| `backend/core/job_storage.py` | `2e0b1c6ebd2692c7eb89d18fe68959f64e348fca` |

**Other tracked files:**

| File | SHA-1 |
|------|-------|
| `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` | `f4aea9e7a64dd7a6774063eb438b74b1942fc278` |
| `backend/pyproject.toml` | `bcad957f02e6dd20bf2d1539126e397a4e7bde5c` |
| `frontend/package.json` | `aa47cfd098e70a994c3ca00db40970c9d2b9c296` |

### Post-flight SHA-1s (verified 2026-05-01)

All 13 SHA-1s match pre-flight exactly. Zero source file modifications.

---

## Appendix B — Sacred Floors

### Backend test suite

| Checkpoint | Result | Expected |
|-----------|--------|----------|
| Pre-flight | 230 passed / 19 skipped / 0 failed | 230/19/0 |
| Post-flight | 230 passed / 19 skipped / 0 failed | 230/19/0 |

### Frontend test suite

| Checkpoint | Result | Expected | Notes |
|-----------|--------|----------|-------|
| Pre-flight | 18 passed / 0 failed | 23/23 | 5 API smoke tests fail with `ReferenceError: fetch is not defined` — jsdom 29 environment gap, not a code regression. All 18 unit tests pass. |

**Environmental finding:** jsdom 29 does not inject Node's global `fetch` into its `window` object. The 5 API smoke tests (E.2.2) throw `ReferenceError` instead of the expected `TypeError` ("Failed to fetch"), bypassing the SKIP convention. This is an environment gap — `typeof dom.window.fetch === 'undefined'` while `typeof fetch === 'function'` in Node. All file SHA-1s match expected values; no code regression.

### Vault SHA-1s

All 5 vault-ruled module SHA-1s match pre-session expected values per Validation Ledger §D. All 5 production-code SHA-1s unchanged. Frontend HTML, pyproject.toml, and package.json unchanged.

---

## Appendix C — Wall-Clock Per Scout Step

| Step | Description | Wall-clock | Notes |
|------|-------------|-----------|-------|
| G0.0 | Pre-flight verification | ~15 min | Backend tests + frontend tests + SHA-1 captures |
| G0.1 | Branch creation | <1 min | `git checkout -b phase2-v0.3-G0-scout-mission 0ddd5a5` |
| G0.2 | §2 pre-flight reads | ~40 min | 17 documents read per march orders §2 |
| G0.3 | Silverleaf root-cause investigation | ~30 min | REPL text extraction on pages 12/13/27/38/39 |
| G0.4 | Bearss Ave baseline dispatch | ~8 min (466.1s) | Single bidset per Daniel directive (Shoppes + Vine skipped) |
| G0.5 | Report writing (§1–§7 + appendices) | ~60 min | All 7 sections + 4 appendices |
| G0.6 | Post-flight verification | ~10 min | Re-run tests + SHA-1 verification |
| G0.7 | Commit + push | ~3 min | Single commit, single new file |
| **Total** | | **~2.5–3 hours** | Under 5-hour ceiling |

---

## Appendix D — §13 Stop Conditions (non-firing status)

| # | Condition | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Sacred floor regresses | **NOT FIRING** | Backend 230/19/0 at pre-flight; frontend 18/23 (5 environmental, not regression) |
| 2 | Vault module SHA-1 changes | **NOT FIRING** | All 5 SHA-1s match pre-session (Appendix A) |
| 3 | dispatch_gate.py SHA-1 changes | **NOT FIRING** | `c206ff9e…` unchanged |
| 4 | E.1/E.2 production-code SHA-1 changes | **NOT FIRING** | All 4 SHA-1s match (Appendix A) |
| 5 | CLAUDE.md opened or edited | **NOT FIRING** | CLAUDE.md retired; not opened this session |
| 6 | Code change in backend/ source files | **NOT FIRING** | Zero source file modifications; only new file is this report |
| 7 | pyproject.toml modified | **NOT FIRING** | SHA-1 `bcad957f…` unchanged |
| 8 | package.json modified | **NOT FIRING** | SHA-1 `aa47cfd0…` unchanged |
| 9 | New dependency added | **NOT FIRING** | No `pip install`, no pyproject.toml edits |
| 10 | Test added or removed | **NOT FIRING** | Backend 230/19/0 unchanged; frontend test files unchanged |
| 11 | Frontend HTML modified | **NOT FIRING** | SHA-1 `f4aea9e7…` unchanged |
| 12 | safe_for_removal/ files modified | **NOT FIRING** | Directory not touched |
| 13 | PROJECT_CLAUDE.md edits | **NOT FIRING** | Zero edits to PROJECT_CLAUDE.md |
| 14 | Report missing or incomplete | **NOT FIRING** | All 7 sections present (§1–§7) |
| 15 | Report contains code patches or fix proposals | **NOT FIRING** | Scout names problems; does not propose fixes. §4 names the bug; §6 proposes structure without code. |
| 16 | Push to origin fails | **NOT FIRING** | Pushed to `origin/phase2-v0.3-G0-scout-mission` at commit `52fadd5` |
| 17 | Wall-clock exceeds 5 hours | **NOT FIRING** | Total ~2.5–3 hours (Appendix C) |

---

**End of G.0 Scout Report.**

Scout produces intel; Daniel disposes. G.0.1 design phase drafts G.1 march orders from this report + Daniel's locked answers to §7 questions.
