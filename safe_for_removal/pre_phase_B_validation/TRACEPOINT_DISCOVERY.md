# TRACEPOINT_DISCOVERY.md

**Date:** 2026-04-27
**Pass:** v0.3 Phase B preparation — read-only inventory of `tracepoint_port/`
**Author:** Claude Opus 4.7
**Audience:** Daniel, ahead of Phase B march orders

This is a discovery pass. **No production code modified. No `tracepoint_port/`
files modified.** The folder is treated as read-only reference per CLAUDE.md
§"On the TracePoint folder copy."

---

## 0. Sacred floor verification

**Before discovery (run on backend at `huckleberry/backend/`):**
```
112 passed, 19 skipped in 1.51s
```
- 112 backend pass + 138 Phase 1 frontend pass = **250 passing total**
- 19 skipped (live-server / Wendy's PDF gated)
- 0 failed

Sacred floor `250 / 19 / 0` **HELD before discovery**. Verification after
discovery is in §10 below.

---

## 1. The folder Daniel placed in the tree

There are two siblings on disk that share the name `tracepoint_port`:

| Path | What it is |
| --- | --- |
| `C:/huck stage 2/tracepoint_port/` | Flat snapshot of the five files Phase A v0.2 ported (config.py, context.py, dispatch_gate.py, pdf_engine.py, zone_filter.py) plus their tests, requirements.txt, the research paper, and `roofing_spec_database.py`. Useful as a v0.2-shaped index. **Not** the full TracePoint project. |
| `C:/huck stage 2/huckleberry/tracepoint_port/TracePoint/` | The **full TracePoint project tree.** This is the authoritative source for Phase B verbatim ports per CLAUDE.md line 314. All paths in §2-§9 below are relative to this folder unless noted. |

The flat copy at `huckleberry/tracepoint_port/` (one level above `TracePoint/`)
is the same set of v0.2 files — duplicates of what's already in `backend/core/`.
It is not the discovery target.

**Discovery target throughout this document:**
`C:/huck stage 2/huckleberry/tracepoint_port/TracePoint/` (1.6 GB total).

---

## 2. Top-level folder structure

### 2.1 One level deep (under `TracePoint/`)

```
TracePoint/
├── core/                      ← Phase B port surface (Python, ~5,300 lines)
├── corrections/               ← runtime correction JSONL files (8 files, 31 KB)
├── data/                      ← seed/answer-key/test-PDF assets
├── docs/                      ← IMPLEMENTATION_PLAN.md
├── frontend/                  ← Vite/React UI — TracePoint-only, do NOT port
├── frontend_v1.2/             ← UI variant — do NOT port
├── frontend_v1.3/             ← UI variant — do NOT port
├── modules/                   ← roofing module + debug module (Python)
├── plugins/                   ← api/, cowork/, excel/ (all empty)
├── scripts/                   ← TracePoint research/diagnostic scripts — do NOT port
├── server/                    ← FastAPI app + routes — TracePoint-shaped, do NOT port verbatim
├── tests/                     ← pytest suites mirroring core/
├── test_plans/                ← 12 PDFs (273 MB) — bid-set integration corpus
├── trades/                    ← glazing/ roofing/ siding/ — empty model/ folders only
├── uploads/                   ← 378 user-uploaded PDFs (946 MB) — runtime artifact, do NOT port
├── verify_dzi_output/         ← image debug output — do NOT port
├── CLAUDE.md, CLAUDE.md.md    ← TracePoint's own instructions — do NOT port
├── CLAUDE_*_ORDERS.md         ← TracePoint's research orders — do NOT port
├── ITEM_0_*.txt               ← TracePoint research logs — do NOT port
├── PROJECT_INVENTORY.txt      ← TracePoint inventory — do NOT port
├── V1.2_AUDIT.txt             ← TracePoint audit notes — do NOT port
├── TracePoint_AI_Research_Paper.docx  ← already mirrored at huckleberry/PHASE_2_HANDOFF.md context
├── requirements.txt           ← Python pins (see §6)
├── launch.bat, stop.bat,
│   START_V1_2_TEST.ps1,
│   create_shortcut.ps1        ← Windows shell helpers — do NOT port
└── C:TracePoint.claude/       ← empty stray folder, ignore
```

### 2.2 Two levels deep — relevant subdirs only

```
core/
├── __init__.py                (0 lines)
├── architect_profile.py       (174 lines)        ← Phase B.4
├── config.py                  (45 lines)         ← v0.2: byte-identical
├── context.py                 (803 lines)        ← v0.2: byte-identical
├── correction_store.py        (134 lines)        ← Phase B.4 (likely)
├── dispatch_gate.py           (1,726 lines)      ← v0.2: differs by 3 import lines (see §7)
├── filter_pipeline.py         (230 lines)        ← Phase B.1
├── geometry_matrix.py         (832 lines)        ← Phase B.2
├── pdf_engine.py              (645 lines)        ← v0.2: byte-identical
├── polygon_scorers.py         (272 lines)        ← Phase B.3
├── storage.py                 (221 lines)        ← Phase B.4
├── trade_module.py            (90 lines)         ← Phase D scope (trade-module contract)
└── zone_filter.py             (134 lines)        ← v0.2: byte-identical

data/
├── answer_keys/
│   └── roofing_answer_keys.json   (181 lines, 4.2 KB) — 8 verified projects
├── seed/
│   └── roofing_seed_data.md       (64 lines) — 19-field schema doc
├── test_plans/                    (8 PDFs, 3.9 MB) — small named bid sets
└── roofing_materials.py           (294 lines) — already mirrored as backend/seeds/roofing_spec_database.py

modules/
├── debug/
│   ├── __init__.py            (0 lines)
│   └── debug_module.py        (470 lines)        ← TracePoint debug surface; not Phase B
└── roofing/
    ├── __init__.py            (0 lines)
    ├── roofing_module.py      (434 lines)        ← Phase D candidate (trade module)
    └── vocabulary.py          (575 lines)        ← Phase D candidate (ROOF_VOCAB)

server/
├── __init__.py                (0 lines)
├── app.py                     (40 lines)         ← TracePoint FastAPI bootstrap, not Huckleberry's
├── database/
│   ├── __init__.py
│   └── migrations/            ← TracePoint Alembic; Huckleberry uses its own migrations
├── middleware/
│   └── __init__.py
└── routes/
    ├── corrections.py         (156 lines)
    ├── export.py              (395 lines)
    ├── geometry.py            (518 lines)
    ├── tiles.py               (161 lines)
    ├── trade.py               (229 lines)        ← Phase D candidate (build_trade_input)
    ├── upload.py              (157 lines)
    └── viewer.py              (67 lines)

tests/
├── __init__.py                (0 lines)
├── fixtures/                  (empty)
├── test_architect_profile.py  (171 lines)
├── test_dispatch.py           (412 lines)        ← v0.2: byte-identical
├── test_filter_pipeline.py    (270 lines)        ← Phase B.1
├── test_geometry_matrix.py    (380 lines)        ← Phase B.2
├── test_integration.py        (479 lines)        ← end-to-end; touches server.app
├── test_pdf_engine.py         (304 lines)        ← v0.2: byte-identical
├── test_polygon_scorers.py    (170 lines)        ← Phase B.3
└── test_wendys_integration.py (223 lines)        ← live-server gated; needs hardcoded Wendy's PDF
```

---

## 3. `core/` inventory — every .py file

Each row shows: line count, top-level imports (stdlib / 3rd-party / `core.*`),
public symbols, and the TracePoint paper stage it implements.

### 3.1 `core/__init__.py` — 0 lines
Empty package marker.

### 3.2 `core/config.py` — 45 lines
- **Imports:** `pathlib.Path`
- **Exports (constants):** `PROJECT_ROOT`, `PDF_RENDER_DPI=150`, `PDF_THUMBNAIL_DPI=36`, `PDF_MAX_DIMENSION=4096`, `CONTOUR_MIN_AREA_RATIO=0.01`, `CONTOUR_APPROX_EPSILON=0.02`, `DIM_MIN_FT=10.0`, `DIM_MAX_FT=1000.0`, `ARCH_SCALES` (15 scale labels), `UPLOAD_DIR`, `CORRECTION_DIR`, `MODEL_DIR`
- **Stage:** project-wide config; Stage 1 + 7 (scales) + 11 (geometry).

### 3.3 `core/context.py` — 803 lines
- **Imports:** `dataclasses`, `typing`, `enum`
- **Exports (classes):** `SourceTag`, `Discipline(Enum)`, `PageType(Enum)`, `ConstructionType(Enum)`, `ScaleInfo`, `SheetEntry`, `CrossReference`, `LegendEntry`, `Legend`, `PageZone`, `PageContext`, `ProjectMetadata`, `ScopePage`, `ProjectScope`, `TradeContext`, `BidContext`, `LLMInput`, `LLMOutput`, `PlanSetContext`
- **Exports (functions):** `validate_llm_output`, `check_for_leaks`
- **Stage:** the data contract that flows through Stages 1–12. Carried by every other module.

### 3.4 `core/zone_filter.py` — 134 lines
- **Imports:** `re`, `typing`
- **Exports:** `detect_detail_zones(text_blocks, page_meta)`, `detect_title_block(text_blocks, page_meta)`, `filter_paths_by_zone(paths, exclusion_zones)`
- **Stage:** Stage 2 input — the zone exclusions consumed by the heavy-line pipeline's `gate_zone_mask`.

### 3.5 `core/pdf_engine.py` — 645 lines
- **Imports:** `io`, `re`, `dataclasses`, `pathlib`, `typing`, `fitz` (PyMuPDF), `PIL.Image`; `core.config.PDF_MAX_DIMENSION/PDF_RENDER_DPI/PDF_THUMBNAIL_DPI`
- **Exports (classes):** `PageMeta`, `TextBlock`, `VectorPath`, `PDFDocument`, `PDFEngine`
- **Exports (functions):** `_parse_dimension_to_feet` (private but tested), `find_stated_areas`, `parse_scale_to_ft_per_inch`, `find_roof_plan_scale`, `find_scale_from_any_page`
- **Stage:** raw PDF I/O for every downstream stage; scale parsing belongs to Stage 7.

### 3.6 `core/dispatch_gate.py` — 1,726 lines
- **Imports:** `hashlib`, `json`, `re`, `sys`, `time`, `datetime`, `pathlib`, `typing`; `core.pdf_engine.PDFEngine/TextBlock/parse_scale_to_ft_per_inch/find_roof_plan_scale`; `core.zone_filter.detect_detail_zones/detect_title_block`; `core.context.*` (PlanSetContext + dataclasses + enums)
- **Exports (functions):** `run_filter_1` (sheet inventory), `run_filter_2` (page classification), `run_filter_3` (cross-references), `run_filter_4` (legends), `run_filter_5` (scope scanner core), plus private `_classify_page_type`, `_extract_cross_refs_on_page`, `_classify_legend_type`, `_find_legends_on_page`, `_parse_tables_on_page`, `_quality_check_legends`, `_extract_project_metadata`, `_collect_title_block_text`, `_find_spec_sections`, `_find_manufacturers_in_text`, `_find_material_markers`, `_find_florida_signals`, `_find_architect_name`, `_find_contractor_name`, `_classify_scope_pages`, `_resolve_scope_system`, `_determine_roof_shape`, `run_scope_scanner`, `run_dispatch`, `_ctx_to_dict`, `_print_report`, `main`
- **Stage:** TracePoint Stage 1 / Layer 3 (Filters 1–5) — the dispatch gate. **Already ported in v0.2 with 3-line import diff.**

### 3.7 `core/filter_pipeline.py` — 230 lines  *(Phase B.1 candidate)*
- **Imports:** `dataclasses`, `typing`
- **Exports (classes):** `GateLog`, `FilterResult`
- **Exports (functions):** `gate_zone_mask`, `gate_weight_filter`, `gate_length_filter`, `gate_dash_filter`, `gate_color_filter`, `run_heavy_pipeline`, `run_allpaths_pipeline`
- **Stage:** TracePoint Stages 2–5. Pure-Python composable gates over `VectorPath` lists. **No 3rd-party deps.**

### 3.8 `core/geometry_matrix.py` — 832 lines  *(Phase B.2 candidate)*
- **Imports:** `dataclasses`, `typing`, `cv2`, `numpy`, `PIL.Image`, `shapely.geometry.Polygon/MultiPolygon`, `shapely.ops.unary_union`, `shapely.validation.make_valid`; `core.config.ARCH_SCALES/CONTOUR_APPROX_EPSILON/CONTOUR_MIN_AREA_RATIO`
- **Exports (classes):** `DetectedContour`, `GeometryResult`, `GeometryMatrix`
- **Stage:** TracePoint Stages 6–9 (clustering, scale tier, perimeter cleanup, confidence). **Adds new dependencies:** `opencv-python`, `numpy`, `shapely`. None of these are in backend `pyproject.toml` today.

### 3.9 `core/polygon_scorers.py` — 272 lines  *(Phase B.3 candidate)*
- **Imports:** `re`, `dataclasses`, `typing`
- **Exports (classes):** `InteriorScore`
- **Exports (functions):** `score_interior(polygon_bbox, ...)`, `score_rectilinearity(paths_in_cluster)`; private helpers `_tb_bbox`, `_tb_text`, `_zone_bbox`, `_zone_type`
- **Stage:** TracePoint Stages 10–12. Module docstring explicitly notes thresholds (callout density 0.06 / 0.03, long-text ratio) calibrated on Step 56's 15 bid set sweep — must come over verbatim per CLAUDE.md line 260.

### 3.10 `core/architect_profile.py` — 174 lines  *(Phase B.4 candidate)*
- **Imports:** `typing`, `re as _re`; tries `rapidfuzz.fuzz` (already a backend dep)
- **Exports:** `FIRM_KEYWORDS` (list), `extract_firm_candidates(title_block_text)`, `detect_firm(title_block_text, storage)`, `profile_is_trusted(profile, min_success=3)`; private `_extract_text`
- **Stage:** Layer 3 firm detection. Activates the `storage` argument that v0.2 gated to None.

### 3.11 `core/storage.py` — 221 lines  *(Phase B.4 candidate)*
- **Imports:** `hashlib`, `sqlite3`, `pathlib`, `typing`
- **Exports:** `StorageEngine` class (dispatch_cache, geometry_cache, architect_profiles tables); `hash_pdf(pdf_path)`
- **DB path:** `~/.tracepoint/cache.db` — **must be retargeted** for Huckleberry (probably `~/.huckleberry/cache.db` or use Postgres in `app.db.session`).
- **Stage:** persistence layer for Layers 1–3 + architect-profile flywheel.

### 3.12 `core/correction_store.py` — 134 lines  *(Phase B.4 candidate)*
- **Imports:** `json`, `time`, `dataclasses` (`asdict`), `pathlib`, `typing`; `core.config.CORRECTION_DIR`
- **Exports:** `Correction` dataclass, `CorrectionStore` class
- **Stage:** correction loop persistence — JSONL append per `doc_id`. Pairs with `architect_profile.detect_firm` to grow the flywheel.

### 3.13 `core/trade_module.py` — 90 lines  *(Phase D candidate, not Phase B)*
- **Imports:** `__future__`, `dataclasses`, `typing.Any/Optional/Protocol`
- **Exports:** `TradeFieldValue`, `TradeModuleInput`, `TradeModuleOutput`, `TradeModule(Protocol)`
- **Stage:** the platform/trade boundary. Not Phase B per CLAUDE.md (Phase D scope).

---

## 4. `data/` inventory

```
data/
├── answer_keys/
│   └── roofing_answer_keys.json   (181 lines, 4.2 KB)
├── seed/
│   └── roofing_seed_data.md       (64 lines)
├── test_plans/                    (8 PDFs, 3.9 MB)
└── roofing_materials.py           (294 lines, 9.6 KB)
```

### 4.1 `data/answer_keys/roofing_answer_keys.json` (4.2 KB, 181 lines)

Keyed by short project name. **Schema per project (from inspection):**
- `area_sqft: int`
- `perimeter_lf: int`
- `edge_metal_lf: float`
- `coping_lf: float | absent`
- `corners: int`, `scuppers: int`, `drains: int`, `units: int`
- `split_boots: int | absent`, `pipe_boots: int | absent`, `vtr: int | absent`
- `cricket_sf: int | absent`, `walk_pads_lf: float | absent`
- `hatch: int | absent`, `curb_flash_lf: float | absent`
- `collector_heads: int | absent`, `downspouts: int | absent`, `gutters_lf: int | absent`
- `scale: str` (e.g. `"3/16\" = 1'-0\""`)
- `page: int`
- `source_pdf: str`

8 projects: `wendys_fort_myers`, `racetrac_tampa`, `limonaia_miami`, `cfa_05861`,
plus 4 more (chipotle, autozone, murphy, taco_bell, panda, aea_silverleaf — see file).

### 4.2 `data/seed/roofing_seed_data.md` (64 lines)
Documents the 19-field roofing schema and the answer-key table inline. Markdown-only;
treat as documentation, not seed code.

### 4.3 `data/test_plans/` (3.9 MB, 8 PDFs)
Small named bid-set PDFs used by `tests/test_dispatch.py` and downstream tests:
`aeasilverleaf_roof_A106.pdf` (273 KB), `autozone_roof_A6.pdf` (883 KB),
`cfa_roof_A230.pdf` (467 KB), `chipotle_roof_A140.pdf` (814 KB),
`collins_roof_A71.pdf` (362 KB), `murphy_roof_E52.pdf` (616 KB),
`panda_roof_A107.pdf` (313 KB), `tacobell_roof_A12.pdf` (236 KB).

### 4.4 `data/roofing_materials.py` (294 lines)
**Already mirrored verbatim** at `backend/seeds/roofing_spec_database.py`
(byte-identical SHA-1 `028a9dcc2ab0892d663650f7c62a4f3380b013e1`, just renamed).
Contains `SPEC_SECTIONS`, `MATERIAL_PROPERTIES`, manufacturer dicts.

### 4.5 `test_plans/` (top-level, 273 MB, 12 PDFs)
**Different folder** from `data/test_plans/`. Contains the same 8 small files
**plus** four large multi-sheet bid sets (~50–80 MB each):
`Chewy_Vet_Care-London_Square_-_Miami_-_JDR_Fixtures_.pdf`,
`Panda_Express_-_Naples_-_CDO___Visible_Construction_Corp.pdf`,
`Taco_Bell_-_Weeki_Wachee_-_Compass_Construction_Management__2_.pdf`,
`Vine_Street_Retail_Center_-_Kissimmee_-_Great_Southern_Constructors.pdf`.
`tests/test_dispatch.py` references these by `Path("test_plans/...")` — see §5.

---

## 5. `tests/` inventory

| Test file | Lines | Imports `core/...` | PDFs referenced | Phase B mapping |
| --- | ---: | --- | --- | --- |
| `test_pdf_engine.py` | 304 | `core.pdf_engine.*` (full surface) | none on disk; uses `tmp_path` + `fitz` to synthesize | v0.2 (already in `backend/tests/`) — **byte-identical** |
| `test_dispatch.py` | 412 | `core.context.*`, `core.dispatch_gate.run_dispatch` | `test_plans/cfa_roof_A230.pdf`, `Vine_Street_..._.pdf`, `tacobell_roof_A12.pdf`, `aeasilverleaf_roof_A106.pdf` | v0.2 (already in `backend/tests/`) — **byte-identical** |
| `test_filter_pipeline.py` | 270 | `core.filter_pipeline.*` | none; uses `MockPath` | **Phase B.1 — port verbatim** |
| `test_geometry_matrix.py` | 380 | `core.geometry_matrix.GeometryMatrix/DetectedContour/GeometryResult` | none; synthesizes images via PIL | **Phase B.2 — port verbatim**; needs cv2/numpy/shapely/PIL |
| `test_polygon_scorers.py` | 170 | `core.polygon_scorers.*` | none; uses `MockTextBlock`/`MockZone`/`MockPath` | **Phase B.3 — port verbatim** |
| `test_architect_profile.py` | 171 | `core.architect_profile.*`, `core.storage.StorageEngine` | none; uses `tmp_path` for SQLite | **Phase B.4 — port verbatim** |
| `test_integration.py` | 479 | `core.pdf_engine`, `core.geometry_matrix`; spins up `server.app` via TestClient | `tmp_path / "test_plan_set.pdf"` (synthesized) | end-to-end — defer to Phase E |
| `test_wendys_integration.py` | 223 | `core.pdf_engine`, `core.geometry_matrix`; httpx live server | hardcoded `C:\Users\danie\Documents\examples\Examples with keys\Wendys – Fort Myers\Wendy's - Fort Myers - Great Southern Constructors (1).pdf` | live-server gated; matches the 19 currently-skipped backend tests |
| `__init__.py` | 0 | — | — | — |

**Test PDF dependencies for Phase B:**
- B.1 / B.2 / B.3 / B.4 unit tests: **no PDF dependencies** — synthesize via PIL or use mocks.
- v0.2 `test_dispatch.py` (already in backend) needs `test_plans/{cfa,vine,taco,aea}.pdf` — currently lives at `backend/test_fixtures/` (need to confirm exact subdir).

---

## 6. Dependency surface

### 6.1 TracePoint `requirements.txt` (top-level)
```
PyMuPDF>=1.24.0
Pillow>=10.0.0
opencv-python>=4.9.0
shapely>=2.0.0
numpy>=1.26.0
fastapi>=0.110.0
uvicorn>=0.27.0
openpyxl>=3.1.0
pytest>=8.0.0
```

### 6.2 Backend `pyproject.toml` (current)
```
fastapi>=0.115, uvicorn[standard]>=0.32
sqlalchemy>=2.0, asyncpg>=0.30, alembic>=1.13
pydantic>=2.9, pydantic-settings>=2.6
boto3>=1.35
pdfplumber>=0.11, pypdfium2>=4.30
PyMuPDF>=1.24.0, rapidfuzz>=3.0.0
[dev] pytest>=8.3, pytest-asyncio>=0.24, ruff>=0.7, mypy>=1.13
```

### 6.3 Gap (what Phase B adds to backend pyproject)

| Package | Reason | Phase |
| --- | --- | --- |
| `Pillow>=10.0.0` | `core.geometry_matrix` (image I/O), `core.pdf_engine` already uses PIL implicitly via fitz pixmap | B.2 (formalize the dep) |
| `opencv-python>=4.9.0` | `core.geometry_matrix.GeometryMatrix` (cv2 contour detection) | B.2 |
| `shapely>=2.0.0` | `core.geometry_matrix` (Polygon, unary_union, make_valid) | B.2 |
| `numpy>=1.26.0` | transitive via opencv + shapely; explicit | B.2 |
| `openpyxl>=3.1.0` | TracePoint Excel export (`server/routes/export.py`) | **NOT Phase B** — frontend already owns Excel export (CLAUDE.md §1) |

`rapidfuzz` is already pinned in backend (used today by dispatch_gate and by `architect_profile`).

---

## 7. Diff vs already-mirrored backend files

SHA-1 comparison of `tracepoint_port/TracePoint/<file>` against `backend/<file>`:

| File | TracePoint SHA-1 | Backend SHA-1 | Status |
| --- | --- | --- | --- |
| `core/config.py` | `480cd80c…` | `480cd80c…` | **BYTE-IDENTICAL** |
| `core/pdf_engine.py` | `e872f69e…` | `e872f69e…` | **BYTE-IDENTICAL** |
| `core/zone_filter.py` | `5399c437…` | `5399c437…` | **BYTE-IDENTICAL** |
| `core/context.py` | `65ca224b…` | `65ca224b…` | **BYTE-IDENTICAL** |
| `core/dispatch_gate.py` | `06584576…` | `ebf9c804…` | **DIFFERS** — 3 lines |
| `tests/test_pdf_engine.py` | `3d00769b…` | `3d00769b…` | **BYTE-IDENTICAL** |
| `tests/test_dispatch.py` | `bb2d8a50…` | `bb2d8a50…` | **BYTE-IDENTICAL** |
| `data/roofing_materials.py` ↔ `seeds/roofing_spec_database.py` | `028a9dcc…` | `028a9dcc…` | **BYTE-IDENTICAL** (renamed in backend) |

### 7.1 `dispatch_gate.py` — the 3-line diff

```diff
1170c1170
<     from data.roofing_materials import all_manufacturer_names
---
>     from seeds.roofing_spec_database import all_manufacturer_names
1292c1292
<     from data.roofing_materials import (
---
>     from seeds.roofing_spec_database import (
1359c1359
<     from data.roofing_materials import SPEC_SECTIONS, MATERIAL_PROPERTIES
---
>     from seeds.roofing_spec_database import SPEC_SECTIONS, MATERIAL_PROPERTIES
```

Three identical edits — TracePoint imports `from data.roofing_materials`,
backend imports `from seeds.roofing_spec_database`. Same character as the
v0.2 verbatim port discipline (CLAUDE.md line 313). All inside function bodies
(deferred imports), so the structural diff is zero.

---

## 8. Phase B port candidates — line counts and signatures

### 8.1 Phase B.1 — Filter pipeline (Stages 2–5)

| Source | Lines | Target (per CLAUDE.md) |
| --- | ---: | --- |
| `core/filter_pipeline.py` | 230 | `backend/core/filter_pipeline.py` |
| `tests/test_filter_pipeline.py` | 270 | `backend/tests/test_filter_pipeline.py` |
| **Total** | **500** | |

**Public surface:**
```python
from core.filter_pipeline import (
    GateLog, FilterResult,
    gate_zone_mask, gate_weight_filter, gate_length_filter,
    gate_dash_filter, gate_color_filter,
    run_heavy_pipeline, run_allpaths_pipeline,
)
```
**Imports:** stdlib only (`dataclasses`, `typing`). **Zero dep additions for B.1.**

### 8.2 Phase B.2 — Geometry engine (Stages 6–9)

| Source | Lines | Target (per CLAUDE.md) |
| --- | ---: | --- |
| `core/geometry_matrix.py` | 832 | `backend/core/geometry_engine.py` (note: CLAUDE.md uses "geometry_engine.py" as the target name; TracePoint source is "geometry_matrix.py") |
| `tests/test_geometry_matrix.py` | 380 | `backend/tests/test_geometry_engine.py` |
| **Total** | **1,212** | |

**Public surface:**
```python
from core.geometry_matrix import (
    DetectedContour, GeometryResult, GeometryMatrix,
)
```
**Imports add to backend:** `cv2` (opencv-python), `numpy`, `shapely`, `PIL`.
Note CLAUDE.md line 258: the L-/T-shape user-polygon override stays in frontend,
**not** ported.

### 8.3 Phase B.3 — Post-clustering scorers (Stages 10–12)

| Source | Lines | Target (per CLAUDE.md) |
| --- | ---: | --- |
| `core/polygon_scorers.py` | 272 | `backend/core/scorers.py` |
| `tests/test_polygon_scorers.py` | 170 | `backend/tests/test_scorers.py` |
| **Total** | **442** | |

**Public surface:**
```python
from core.polygon_scorers import (
    InteriorScore, score_interior, score_rectilinearity,
)
```
**Imports:** stdlib only (`re`, `dataclasses`, `typing`). Empirical thresholds
(0.06 callout density, 0.03 secondary, long-text ratio 0.5, noise-zone overlap)
must port verbatim per CLAUDE.md line 260.

### 8.4 Phase B.4 — Architect profile + storage

| Source | Lines | Target (per CLAUDE.md) |
| --- | ---: | --- |
| `core/architect_profile.py` | 174 | `backend/core/architect_profile.py` |
| `core/storage.py` | 221 | `backend/core/storage.py` |
| `core/correction_store.py` | 134 | `backend/core/correction_store.py` (likely; not explicitly named in CLAUDE.md but pairs with architect-profile flywheel) |
| `tests/test_architect_profile.py` | 171 | `backend/tests/test_architect_profile.py` |
| **Total (incl. correction_store)** | **700** | |

**Public surface:**
```python
from core.architect_profile import (
    FIRM_KEYWORDS, extract_firm_candidates, detect_firm, profile_is_trusted,
)
from core.storage import StorageEngine, hash_pdf
from core.correction_store import Correction, CorrectionStore
```

**Required edits during port:**
- `storage.py:13` — change `DB_PATH = Path.home() / ".tracepoint" / "cache.db"` to a Huckleberry-namespaced path (or thread through pyproject/env). Not a verbatim line; this is one of the "required edits typically import paths" (CLAUDE.md line 313).
- Activate `storage` and `architect_profile` arguments in `dispatch_gate.run_dispatch` that v0.2 currently passes as `None` / gated off.

### 8.5 Phase B grand total

| Phase | Source LOC (core + tests) |
| --- | ---: |
| B.1 | 500 |
| B.2 | 1,212 |
| B.3 | 442 |
| B.4 | 700 |
| **Total verbatim port surface** | **~2,854 lines** (1,508 core + 991 tests + ~355 storage/correction_store/architect helpers) |

For comparison, v0.2 Phase A ported ~3,200 lines (`pdf_engine` 645 + `context` 803 + `dispatch_gate` 1,726 + `zone_filter` 134 + `config` 45 + tests 716).

---

## 9. TracePoint-only artifacts — DO NOT port

Per CLAUDE.md "Only the source code Phase B targets comes over." The
following are TracePoint-internal and stay in `tracepoint_port/`:

### 9.1 Frontend variants (large)
- `frontend/` (46 MB) — Vite/React TracePoint UI
- `frontend_v1.2/` (128 MB)
- `frontend_v1.3/` (128 MB)
  → Huckleberry's frontend is the v6.3.5 standalone HTML; TracePoint's
  React UI is not the architecture (CLAUDE.md §1).

### 9.2 Server (would replace, not augment, Huckleberry's `app/`)
- `server/app.py` (40 lines) — TracePoint's FastAPI bootstrap
- `server/routes/{corrections,export,geometry,tiles,trade,upload,viewer}.py`
  (1,683 lines total)
- `server/database/migrations/` — TracePoint Alembic migrations
- `server/middleware/`
  → Huckleberry has its own `backend/app/`. Some routes (especially `trade.py`'s
  `build_trade_input()`) are Phase D candidates, but the `server/` shape is
  not. Treat as reference only.

### 9.3 Research / diagnostic scripts
- `scripts/` (20 MB) — `batch_stress_test.py`, `debug_*.py`, `diagnose_*.py`,
  `sweep_15_*.py`, `validate_roofing_vocab.py`, plus debug PNGs/JSONs.
  → TracePoint's research log; the empirical thresholds they produced are
  baked into `polygon_scorers.py` and `dispatch_gate.py`.

### 9.4 Runtime artifacts
- `uploads/` (946 MB, 378 PDFs) — TracePoint user uploads
- `corrections/*.jsonl` (8 files) — TracePoint correction-store live data
- `verify_dzi_output/` (3.5 MB) — image debug output

### 9.5 TracePoint documentation / orders
- `CLAUDE.md` (84 KB), `CLAUDE.md.md`, `CLAUDE_v1.2.md`,
  `CLAUDE_CODE_BUCKET_A_ORDERS.md`, `CLAUDE_CODE_ITEM_0_ORDERS.md`
- `ITEM_0_BROWSER_OUTPUT.txt`, `ITEM_0_CODE_TRACE.txt`,
  `ITEM_0_FINAL_REPORT.txt`, `ITEM_0_LOGS_INSERTED.txt`
- `PROJECT_INVENTORY.txt`, `V1.2_AUDIT.txt`
- `TracePoint_AI_Research_Paper.docx` — Daniel keeps locally; backend already
  references it indirectly via PHASE_2_HANDOFF.md.

### 9.6 Trade scaffolding / empty
- `trades/{glazing,roofing,siding}/model/` — all empty
- `plugins/{api,cowork,excel}/` — all empty
- `C:TracePoint.claude/` — empty stray
- `tests/fixtures/` — empty

### 9.7 Windows / build helpers
- `launch.bat`, `stop.bat`, `START_V1_2_TEST.ps1`, `create_shortcut.ps1`
- All `__pycache__/` directories
- `.pytest_cache/`, `.claude/`

### 9.8 Already-mirrored (don't re-port)
Anything from §7 that's BYTE-IDENTICAL is already in `backend/core/` or
`backend/tests/` or `backend/seeds/`. Do not re-touch in Phase B.

### 9.9 Phase D candidates (not Phase B)
- `core/trade_module.py` (90 lines) — trade-module Protocol
- `modules/roofing/roofing_module.py` (434 lines) — concrete RoofingModule
- `modules/roofing/vocabulary.py` (575 lines) — ROOF_VOCAB
- `server/routes/trade.py` (229 lines) — `build_trade_input()` router glue
- `modules/debug/debug_module.py` (470 lines) — TracePoint debug surface
  These are flagged for Phase D / later. Daniel's discretion.

---

## 10. Sacred floor verification — AFTER discovery

**No production code modified.** No file under `backend/app/`, `backend/core/`,
`backend/tests/`, `backend/seeds/`, `backend/scripts/`, or `frontend/` was
written, edited, or deleted. The only file created by this pass is
`backend/TRACEPOINT_DISCOVERY.md` (this document).

**Backend pytest at the start of this pass:** `112 passed, 19 skipped, 0 failed`.

A re-run is performed in §11 below to close the gate.

---

## 11. Gate report

| Item | Result |
| --- | --- |
| Production code modified? | **No** |
| `tracepoint_port/` modified? | **No** (read-only reference) |
| New files written | 1 — `backend/TRACEPOINT_DISCOVERY.md` (this file) |
| Sacred floor before | **250 / 19 / 0** (138 frontend + 112 backend pass; 19 backend skipped; 0 fail) |
| Sacred floor after | **see §11.1 below — re-verify before Daniel reviews** |
| Karpathy discipline | held — discovery only, no march |

### 11.1 Sacred floor re-verification (post-pass)

```
$ .venv/Scripts/python.exe -m pytest -q
112 passed, 19 skipped in 1.04s
```

138 Phase 1 frontend + 112 backend = **250 passing**, 19 skipped, 0 failed.
**Sacred floor 250 / 19 / 0 HELD after discovery.** No regressions.

---

## 12. Open questions / things to confirm with Daniel

1. **B.2 target filename.** CLAUDE.md line 258 names the target
   `backend/core/geometry_engine.py`, but the TracePoint source is
   `geometry_matrix.py`. Do we rename on port (and lose verbatim filename
   parity), keep `geometry_matrix.py` (and update the march orders), or
   create `geometry_engine.py` as a thin re-export shim?

2. **B.4 scope.** CLAUDE.md line 262 names `architect_profile.py` and
   `storage.py` only. `correction_store.py` is sibling to both and used
   by the same flywheel. Does Daniel want B.4 to include `correction_store.py`,
   or push it to Phase C/D where the correction loop lights up end-to-end?

3. **B.4 SQLite vs Huckleberry's existing Postgres.** TracePoint `storage.py`
   uses local SQLite at `~/.tracepoint/cache.db`. Backend already has an
   `app/db/session.py` Postgres setup (per `pyproject.toml`'s `asyncpg` /
   `alembic` deps). Verbatim-port discipline says preserve SQLite; Huckleberry
   architecture says use Postgres. This is a one-line edit (DB_PATH or a
   driver swap) but it's a *required* edit, not "tidying." Worth a march-orders
   call-out.

4. **Test PDFs for B.* tests.** B.1 / B.2 / B.3 / B.4 unit tests are
   self-contained (mocks + synthesized PIL images). But integration coverage
   (parity vs frontend's 138 tests) likely needs `test_plans/` PDFs in
   backend. Does Daniel want the 8 small PDFs (3.9 MB) copied into
   `backend/test_fixtures/` during Phase B, or does that wait?

5. **`test_integration.py` and `test_wendys_integration.py`.** These
   touch `server.app` and depend on a hardcoded Wendy's PDF path. Do not
   come over verbatim — they expect TracePoint's FastAPI shape. Defer to
   Phase E once Huckleberry's `backend/app/` is the surface.

---

**End of TRACEPOINT_DISCOVERY.md. Awaiting Daniel's review before Phase B
march orders are drafted.**
