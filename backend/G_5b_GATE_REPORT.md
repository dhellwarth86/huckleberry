# Phase G.5b — Soft Gate Report

**Branch:** `phase2-v0.3-G5b-render-tile-and-filter4` (HEAD = `<theater-cut commit pending>`, +canon commit pending)
**Predecessor:** `phase2-v0.3-G5a-annotation-persistence` head `3d4fdca`
**Started:** 2026-05-08
**Soft gate executed:** 2026-05-09 (no live dispatch needed — backend-only cuts)
**Verdict: SOFT GATE PASS — CP1 shipped (tile API plumbing); CP2 retired during fact-find; surgical theater cut shipped instead.**

---

## 1. Honest summary

Phase G.5b shipped **the PyMuPDF tile-rendering API in `pdf_engine.py`** (CP1, plumbing for G.6 Stage 6 contour detection) and a **surgical theater cut** of the `detect_firm` / `architect_profile` dispatch invocation. The original CP2 (Filter 4 tile consumer) was **retired during fact-find** when scout work confirmed Filter 4 has zero rendering operations to optimize via tiling. A pipeline-wide theater audit (3 parallel Explore agents, this session) established the full picture: the pipeline order is correct, TracePoint port is complete (no pandas, no OCR — those memories were false), theater is shallow not deep, and the genuine compute ceiling (`pdfplumber.extract_tables()` at 2.91s on Bearss p15) is **algorithmic, not rendering-bound** — banked as Phase 10 post-hard-gate (Daniel directive 2026-05-09: Taco Bell currently dispatches in <400s, no current pain).

Two commits on the branch:
- CP1 (`36017fb`): `render_page_tiled()` + `_estimate_render_memory_mb()` + `_compute_tile_rects()` + 4 module constants in `pdf_engine.py`. 5 RED tests written + run before implementation, all GREEN post-implementation. Floor 273 → 278/19/0.
- CP2-replacement (this commit): cut `detect_firm` invocation block from `dispatch_gate.py:1711-1718`. ~20-50ms saved per dispatch when storage is active. Floor 278/19/0 held (no test asserted on the dispatch invocation's side effect).

Vault re-locks at 2 new SHA-1s (`pdf_engine.py`, `dispatch_gate.py`); 4 trade-knowledge files + `debug_module.py` HELD at G.5a baseline.

The bigger value of G.5b isn't the tile API itself (it has no consumer until G.6 lands) — it's the **pipeline theater audit** that established what the pipeline actually does vs what's been theater since the Phase B port. The audit's findings rewrite the next two phases' shape (G.6 = real wins; Phase 10 = parked compute work). See §3 for the audit and §4 for the cut rationale.

---

## 2. Commit chain

| Commit | CP | One-line summary |
|---|---|---|
| `36017fb` | CP1 | PyMuPDF tile rendering API in `pdf_engine.py` — `render_page_tiled()` + 2 helpers + 4 module constants; 5 RED→GREEN tests; G.0 scout math (250 DPI, 50 MB threshold, 5% overlap, 2x2 grid) |
| `<canon>` | CP2-replacement + canon | Cut `detect_firm` invocation from `dispatch_gate.py:1711-1718` (theater — `ctx.architect_profile` had no downstream consumer); + this gate report + CHECKLIST + ITINERARY + PROJECT_CLAUDE updates |

---

## 3. Pipeline theater audit (the real deliverable)

### 3.1 — Pandas / OCR claim resolved FALSE

Daniel's recollection that TracePoint used "pandas OCR" for tables was investigated via grep across `tracepoint_port/TracePoint/`:

- `import pandas`, `pd.DataFrame`, `pd.read_*`, `.to_csv`, `.to_excel` — **zero hits, all of them**
- `tesseract`, `pytesseract`, `easyocr`, `paddleocr`, `image_to_string`, `image_to_data` — **zero hits, all of them**

The render-to-image path that exists (`pdf_engine.render_page` + `geometry_matrix.detect_contours` via OpenCV) is **isolated to the geometry engine for scanned-PDF fallback** — it never touches dispatch and never touches Filter 4. Memory was conflating pdfplumber's vector table extraction with image-based table extraction; they're unrelated.

### 3.2 — Pipeline order is CORRECT

TracePoint and Huckleberry both run: F1 → F2 → F4 → F3 → F5 → scope_scanner → metadata → Stage 13 → persist. Filter 4 before Filter 3 is intentional (Filter 3's keynote detection consumes Filter 4's legend output). Every dependency is satisfied before its consumer runs. **Zero re-ordering bugs.** Huckleberry is a strict superset of TracePoint dispatch — Stage 13 (D.1 trade modules) and persistence (D.2) are additive.

### 3.3 — Theater inventory (concrete)

| # | Item | Necessity | Cut decision |
|---|---|---|---|
| 1 | `_extract_project_metadata` (project_name / project_address / total_building_sf) | UNNECESSARY today; will be needed for invoice/proposal export (Phase H8) | **BANKED** — `test_dispatch.py:408-409 test_building_sf_found` asserts `ctx.project.total_building_sf == 5746.0` after dispatch on Silverleaf (currently SKIPPED on missing AEA fixture, but the assertion is the spec). Cutting silently turns the (skipped) test into a future-fail. Honest cut requires retiring the test too — separate decision. |
| 2 | `detect_firm` / `ctx.architect_profile` | UNNECESSARY today; `architect_profile flywheel` was a TracePoint phase that never connected to a UI in Huckleberry | **CUT THIS CP** — zero test cascade (`test_architect_profile.py` tests function directly via storage mocks, not via dispatch invocation). `ctx.architect_profile` field declaration in `context.py` stays (always None); `to_json`/`from_json` already supports None. ~20-50ms saved per dispatch when storage is active. |
| 3 | `dispatch_warnings` (17+ append sites) | NECESSARY but MISWIRED — real signal but no API/UI consumer | **DON'T CUT — WIRE INSTEAD.** Future phase. Add to `JobResultsResponse`; render in frontend warning panel. |
| 4 | `raw_tables_json` DB persistence | Half-necessary (Stage 13 consumes in-process; persisted JSON is dead until something reads it) | **PARTIAL CUT later.** Keep extraction; drop DB column unless a "table inspector" UI lands. ~30 KB/page DB savings. Future phase. |
| 5 | `dispatch_results` per-page fields (`sheet_num`, `sheet_title`, `has_legend`, `legends_count`, `has_schedule`) | Half-necessary (real outputs of F1/F2/F4; persistence cheap) | **DON'T CUT.** Frontend should EVENTUALLY render these. |
| 6 | Glazing module per-page outputs (`glazing_items`, `door_items`, `storefront_items`) | NECESSARY — the glazing trade's data; falls on floor because frontend handler waits on Phase C.3c follow-on | **DO NOT CUT.** Ship glazing UI in C.3c follow-on. |
| 7 | RoofingModule polygon-derived fields | NECESSARY in design; idle today because Stages 6-9 unwired | **DO NOT CUT.** G.6 enables. |
| 8 | Equipment pins | NECESSARY in design; auto-pin extractor wired (G.5a CP1) and idle | **DO NOT CUT.** G.6 turns on. |
| 9 | `project_scope.scope_pages / system_evidence / manufacturers / material_mentions / florida_signals / roof_shape_signal` | Half-necessary (rendered subset = scope_pages + system_evidence; rest unrendered) | **DON'T CUT EXTRACTION.** Could surface in evidence detail row. Future phase. |
| 10 | `_pre_populate_auto_annotations` | NECESSARY by design (G.5a CP1 wired this); idle pending G.6 | **DO NOT CUT.** |

### 3.4 — Phase 10 parked: algorithmic Filter 4 replacement

The genuine cost ceiling — `pdfplumber.extract_tables()` at 2.91s/page on Bearss p15 — is **vector-bound algorithmic work** (grid-line detection in vector space + text positioning), NOT rendering-bound. Tiling does not help. Replacement candidates (PyMuPDF `Page.find_tables()` added in v1.23+, or a custom vector-direct grid finder) require a parity gate (legends + raw_tables shape match) and bidset-wide wall-clock measurement.

**Daniel directive 2026-05-09:** "Taco Bell Weeki Wachee currently <400s; algorithmic processing returns at Phase 10 after gate 9." Phase 10 = post-closing-hard-gate (3-bidset). No work this CP, no design draft, no scout.

---

## 4. CP2 retirement rationale (why the original plan changed)

The original G.5b plan called for "Tile API + Filter 4 consumer." Fact-find on the call site uncovered:

- `dispatch_gate.py:742-791 _parse_tables_on_page` calls `pdfplumber.Page.extract_tables()` directly on the pdfplumber page object. **No image is involved.** pdfplumber is vector-bound (PDF text stream + grid-line detection), not rasterization-bound.
- The G.0 scout report (`backend/G_0_SCOUT_REPORT.md`) had connected two independent findings — "pdfplumber.extract_tables() is the cost ceiling" and "PyMuPDF tiling is ready" — that don't actually intersect. Tiling helps **rasterization-bound** work; Filter 4 is **vector-bound**.
- Substituting tiles into `_parse_tables_on_page` (via `pdfplumber.Page.crop()` and 4 extract_tables calls) would be **slower per-page** (4 algorithm runs vs 1) and would risk losing tables that span tile boundaries.

Karpathy procedure step 5 (§7 stop on uncertainty) fired. Daniel chose the algorithmic-pivot path; pipeline-wide scout was launched instead; full theater audit produced (§3); CP2 retired in favor of the surgical `detect_firm` cut + Phase 10 parking of algorithmic Filter 4 replacement.

---

## 5. Soft-gate verification

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Backend pytest sacred floor | **CP MET** | `273 → 278 passed, 19 skipped, 0 failed` (+5 net: tile API tests). Cut #2 (detect_firm invocation) held at 278; no test cascade. |
| 2 | Vault SHA-1s — 2 NEW values captured | **CP MET** | `pdf_engine.py` re-locked at `eb5b8372f6f0c52de5a81b452399035c2b720551` (was `daf06dd266d52983a0c761669f8af1ed825088a7` post-G.3); `dispatch_gate.py` re-locked at `71e409a27caf78525d663fa6ca11d0e7a0c9b7ca` (was `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` post-G.3). HELD: 4 trade-knowledge files at G.5a baseline; `debug_module.py 78f71d9030cde3b173389603f5f39bd6bedaac07`. |
| 3 | Tile API ready for G.6 consumer | **CP MET** | `render_page_tiled(pdf_doc, page_num, dpi=PDF_TILE_DPI=250, force_tiles=False)` + `_estimate_render_memory_mb` + `_compute_tile_rects` callable from any module that imports `core.pdf_engine`. G.6 Stage 6 contour detection will consume directly. |
| 4 | `detect_firm` invocation removed | **CP MET** | `dispatch_gate.py:1711-1718` (the entire `if storage is not None: try: from core.architect_profile import detect_firm; tb_text = …; ctx.architect_profile = detect_firm(...)` block) replaced with a docstring stub explaining the cut. `ctx.architect_profile` field declaration in `context.py` unchanged (still defined, always None post-cut). `core/architect_profile.py` itself unchanged (function + helpers stay; unit tests in `test_architect_profile.py` still pass). |
| 5 | No live dispatch verification needed | **CP MET (NOTE)** | Cuts are backend-only with no frontend impact; no Daniel-driven live dispatch required. The backend pytest floor + cascade-test verification (test_dispatch.py + test_architect_profile.py + test_pipeline_dispatch.py: 78 passed, 19 skipped) is the soft gate. |

**Result: 5/5 CP MET. Soft gate PASS.**

---

## 6. Vault SHA-1 verification + re-lock

| File | Pre-G.5b (G.5a re-lock) | Post-G.5b (re-lock baseline) | Status |
|---|---|---|---|
| `backend/core/roofing_module.py` | `9a6085d4a3fbe7bbafa4b920c75868261f3c3a60` | `9a6085d4a3fbe7bbafa4b920c75868261f3c3a60` | ✅ HELD |
| `backend/core/roofing_vocabulary.py` | `863ffb01de05ed8a55b1975268c3ff3a9c1d4252` | `863ffb01de05ed8a55b1975268c3ff3a9c1d4252` | ✅ HELD |
| `backend/core/glazing_module.py` | `1b449e9716ef2fe83ee0f2546ad2281deef5ac55` | `1b449e9716ef2fe83ee0f2546ad2281deef5ac55` | ✅ HELD |
| `backend/core/glazing_vocabulary.py` | `008ed1914422e7f63a8fe90833bcda9e0cb3b44a` | `008ed1914422e7f63a8fe90833bcda9e0cb3b44a` | ✅ HELD |
| `backend/core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | ✅ HELD |
| `backend/core/dispatch_gate.py` (integration-frozen) | `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` | `71e409a27caf78525d663fa6ca11d0e7a0c9b7ca` | ✅ **RE-LOCKED at new SHA-1** |
| `backend/core/pdf_engine.py` (integration-frozen) | `daf06dd266d52983a0c761669f8af1ed825088a7` | `eb5b8372f6f0c52de5a81b452399035c2b720551` | ✅ **RE-LOCKED at new SHA-1** |

**Vault rule re-engages at the post-G.5b SHA-1s.** Same protocol G.3 (precedent for `dispatch_gate.py` + `pdf_engine.py` unfreeze) and G.5a (precedent for the 4 trade-knowledge files).

---

## 7. Sacred floor verification

| Stage | Backend | Frontend |
|---|---|---|
| Pre-phase (G.5a close) | 273 passed, 19 skipped, 0 failed | 28/28 |
| Post-CP1 (`36017fb`) | 278 passed, 19 skipped, 0 failed (+5 tile API tests) | 28/28 |
| Post-cut #2 (canon commit) | 278 passed, 19 skipped, 0 failed (no test cascade) | 28/28 |
| **Post-canon (this report)** | **278 passed, 19 skipped, 0 failed** | **28/28** |

Backend +5 net tests; frontend held. No regressions. Notably: the `detect_firm` cut held the floor at 278 (zero tests asserted on the dispatch invocation's side effect); the cascade analysis (§3.3 row #2) was the load-bearing pre-cut step.

---

## 8. Banked observations (out of G.5b scope; tracked for later)

These came out of the pipeline theater audit. Surfaced here so future phases inherit them with context.

### 8.1 — Phase 10: algorithmic Filter 4 replacement (parked)

`pdfplumber.extract_tables()` is the genuine cost ceiling at 2.91s on Bearss p15 (G.0 scout receipt). Replacement candidates: PyMuPDF `Page.find_tables()` (native to current dep), custom vector-direct grid finder, or hybrid. Phase 10 = post-closing-hard-gate (3-bidset). Daniel directive 2026-05-09: Taco Bell currently <400s, no current pain.

### 8.2 — Theater cuts not taken this CP

- `_extract_project_metadata` (theater #1) — banked. Test cascade at `test_dispatch.py:408-409` (currently SKIPPED on missing AEA fixture). Honest cut requires retiring the test too. Future "documented theater removal" phase decision.
- `dispatch_warnings` API exposure (theater #3) — wire to `JobResultsResponse` + frontend warning panel. Future UX phase.
- `raw_tables_json` DB persistence (theater #4 partial) — ~30 KB/page DB savings if dropped. Future cleanup.
- Glazing module unrendered outputs (theater #6) — ship glazing tab UI. Phase C.3c follow-on (already banked).

### 8.3 — TracePoint port complete; no pandas, no OCR

Resolved false claim. TracePoint port is a strict superset of TracePoint dispatch + D.1/D.2/G-series additions. Nothing was dropped during the port. The render-to-image path in TracePoint exists only in the geometry engine for scanned-PDF fallback (OpenCV contours), never in dispatch. This audit eliminates a false hypothesis that was distorting G.5b planning.

---

## 9. What's NOT in G.5b (explicit, so future phases don't claim coverage)

- **Filter 4 algorithmic replacement** — Phase 10 (post-hard-gate).
- **`_extract_project_metadata` cut** — banked, requires test retirement co-decision.
- **`dispatch_warnings` API/UI exposure** — future UX phase.
- **`raw_tables_json` DB persistence cleanup** — future cleanup.
- **Glazing UI** — Phase C.3c follow-on.
- **Stages 6-9 geometry wiring** — G.6 (next phase, immediately).
- **Auto-pin INSTANCES on viewer** — G.6 unlocks (extractor already wired, idle).
- **3-bidset closing hard gate** — Next-2 (Bearss + Silverleaf + Vine Street + deferred E.2.2 visual).

---

## 10. Receipts index

- **Plan file:** `~/.claude/plans/a-but-i-want-valiant-moler.md` (G.5b → G.6 plan with Karpathy-procedure overlay; CP2 explicitly retired during execution per §4 above)
- **Predecessor gate report:** `backend/G_5a_GATE_REPORT.md`
- **Code commits:** `36017fb` (CP1) + canon commit at end of this sign-out (theater cut + canon)
- **Pipeline theater audit:** in-conversation 3-Explore-agent recon; full agent reports preserved in session transcript
- **Daniel directive verbatim 2026-05-09:** *"A ! lets go Karpathy logic ! C is moved to 10 after hard gate because wiki waki taco bell is 400< seconds currently so algorithmic processing idea lets return to it at 10 after gate 9"*

---

**End of Phase G.5b soft gate report.** Daniel reviews this, the canon updates ship in a single commit, branch awaits Daniel's explicit push approval.
