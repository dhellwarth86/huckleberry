# RECON CASCADE MAP

Read/write inventory of major `PlanSetContext` fields across `backend/core/`.
Produced on branch `phase2-v0.3-recon-cascade-map` from `7318d8b`.

Baseline: 230 passed, 19 skipped, 0 failed.

---

## 1. `ctx.sheet_map` and `ctx.page_to_sheet`

These two fields always travel together. `sheet_map` is the canonical sheet-number-to-SheetEntry dict; `page_to_sheet` is the reverse index (page_index → sheet_number).

### 1.1 `ctx.sheet_map` — WRITES

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 367 | `run_filter_1` | Sets `ctx.sheet_map_source = "drawing_index"` when drawing index found |
| dispatch_gate.py | 377 | `run_filter_1` | Writes `ctx.sheet_map[sn] = SheetEntry(...)` for each drawing index entry |
| dispatch_gate.py | 390 | `run_filter_1` | Sets `ctx.sheet_map_source = "title_blocks"` in fallback path |
| dispatch_gate.py | 402 | `run_filter_1` | Writes `ctx.sheet_map[sheet_num] = SheetEntry(...)` from title block scan |
| dispatch_gate.py | 459 | `run_filter_2` | Mutates `entry.page_type = page_type` on existing SheetEntry via `ctx.sheet_map[sheet_num]` |
| context.py | 675 | `PlanSetContext.from_json` | Restores `ctx.sheet_map_source` from serialized JSON |
| context.py | 702 | `PlanSetContext.from_json` | Restores `ctx.sheet_map[sn] = SheetEntry(...)` from serialized JSON |

### 1.2 `ctx.sheet_map` — READS

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 454–455 | `run_filter_2` | Reads `ctx.page_to_sheet.get(page_idx)` then `ctx.sheet_map[sheet_num]` to get discipline/title for page classification |
| dispatch_gate.py | 605–611 | `run_filter_3` | Reads `ctx.sheet_map.get(ref.target_sheet)` and iterates `ctx.sheet_map.items()` for dash-agnostic cross-ref resolution |
| dispatch_gate.py | 1759–1769 | `_ctx_to_dict` | Iterates `ctx.sheet_map.items()` to serialize to JSON dict |
| dispatch_gate.py | 1828–1829 | `_ctx_to_dict` | Reads `ctx.sheet_map_source` for JSON output |
| dispatch_gate.py | 1866–1867 | `_print_report` | Reads `len(ctx.sheet_map)`, `ctx.sheet_map_source`, iterates `ctx.sheet_map.items()` for CLI report |
| context.py | 398 | `DETERMINISTIC_FIELDS` | Listed as deterministic field for leak detection |
| context.py | 489 | `PlanSetContext.resolve_sheet` | Reads `self.sheet_map.get(sheet_number)` to resolve sheet to page index |
| context.py | 531–543 | `PlanSetContext.to_json` | Iterates `self.sheet_map.items()` for serialization |
| context.py | 619–620 | `PlanSetContext.to_json` | Reads `self.sheet_map_source` for serialization |
| debug_module.py | 155–156 | `_section_dispatch_health` | Reads `ctx.sheet_map_source` and `len(ctx.sheet_map)` for dispatch health diagnostic |

### 1.3 `ctx.page_to_sheet` — WRITES

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 387 | `run_filter_1` | Writes `ctx.page_to_sheet[page_idx] = sn` for each mapped index entry |
| dispatch_gate.py | 411 | `run_filter_1` | Writes `ctx.page_to_sheet[page_idx] = sheet_num` in title-block fallback path |
| context.py | 714 | `PlanSetContext.from_json` | Restores `ctx.page_to_sheet[int(k)] = v` from serialized JSON |

### 1.4 `ctx.page_to_sheet` — READS

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 451 | `run_filter_2` | Reads `ctx.page_to_sheet.get(page_idx)` to find sheet number for each page during classification |
| dispatch_gate.py | 1830 | `_ctx_to_dict` | Reads `ctx.page_to_sheet.items()` for JSON serialization |
| context.py | 398 | `DETERMINISTIC_FIELDS` | Listed as deterministic field for leak detection |
| context.py | 621 | `PlanSetContext.to_json` | Reads `self.page_to_sheet.items()` for serialization |
| debug_module.py | 157 | `_section_dispatch_health` | Reads `len(ctx.page_to_sheet)` for mapped-page count in diagnostic |

### 1.5 Cascade note

`sheet_map` is written exclusively by `run_filter_1`. `run_filter_2` reads it to look up discipline and title per page, and mutates the `page_type` field on existing SheetEntry objects (line 459). `run_filter_3` reads it to resolve cross-reference target sheets. No other filter writes to `sheet_map`. The cascade path is:

```
Filter 1 writes → Filter 2 reads (+ mutates entry.page_type) → Filter 3 reads (for resolution)
```

The MEP discipline fallback (dispatch_gate.py:464–466) reads `disc` which comes from `ctx.sheet_map[sheet_num].discipline` (line 455). This is the specific cascade path the G.1 hypothesis targeted: sheet_map discipline → MEP_PLAN page_type assignment. It fires only when `page_type == UNKNOWN` AND `disc in (MECHANICAL, ELECTRICAL, PLUMBING)`.

---

## 2. `ctx.pages` (PageContext dict)

### 2.1 WRITES

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 500 | `run_filter_2` | Writes `ctx.pages[page_idx] = page_ctx` — creates all PageContext objects |
| dispatch_gate.py | 619 | `run_filter_3` | Writes `ctx.pages[page_idx].cross_refs_out = refs` per page |
| dispatch_gate.py | 621 | `run_filter_3` | Writes `ctx.pages[page_idx].has_details = True` when refs found |
| dispatch_gate.py | 622 | `run_filter_3` | Writes `ctx.pages[page_idx].detail_count = len(...)` |
| dispatch_gate.py | 628 | `run_filter_3` | Appends to `ctx.pages[ref.target_page].cross_refs_in` for resolved refs |
| dispatch_gate.py | 845 | `run_filter_4` | Reads `ctx.pages.get(page_idx)` to set `page_ctx.raw_tables` on schedule pages |
| dispatch_gate.py | 869 | `run_filter_4` | Writes `ctx.pages[page_idx].legends = legends` |
| dispatch_gate.py | 871 | `run_filter_4` | Writes `ctx.pages[page_idx].has_legend = True` |
| dispatch_gate.py | 874 | `run_filter_4` | Writes `ctx.pages[page_idx].has_schedule = True` |
| dispatch_gate.py | 921 | `run_filter_5` | Writes `page_ctx.has_title_block = True` |
| dispatch_gate.py | 960 | `run_filter_5` | Writes `page_ctx.primary_zone = main_zone` and `page_ctx.has_drawing_area = True` |
| dispatch_gate.py | 971 | `run_filter_5` | Same as above, no-title-block path |
| dispatch_gate.py | 973 | `run_filter_5` | Writes `page_ctx.zones = zones` |
| dispatch_gate.py | 985–994 | `run_filter_5` | Appends to `page_ctx.spec_note_texts` and `page_ctx.callout_texts` |
| context.py | 807–811 | `PlanSetContext.from_json` | Restores `ctx.pages[idx] = pc` including cross_refs_out/in from serialized JSON |
| debug_module.py | 276 | `run_debug` | Writes `ctx.trade_contexts["debug"] = debug` (not `ctx.pages`, but reads pages to build debug context) |

### 2.2 READS

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 840 | `run_filter_4` | Reads `ctx.pages.get(page_idx)` to check if page is SCHEDULE_SHEET for pdfplumber table extraction |
| dispatch_gate.py | 867 | `run_filter_4` | Reads `page_idx in ctx.pages` to guard legend association |
| dispatch_gate.py | 895 | `run_filter_5` | Reads `ctx.pages.get(page_idx)` to get page_ctx for zone classification |
| dispatch_gate.py | 1085 | `_collect_title_block_text` | Iterates `ctx.pages.items()` to gather title_block zone text blocks |
| dispatch_gate.py | 1467–1475 | `_build_dispatch_only_input` | Reads `ctx.pages.get(page_idx)` for page_type, legends, zones |
| dispatch_gate.py | 1532–1533 | `_run_trade_modules` | Iterates `sorted(ctx.pages.keys())` and reads `ctx.pages[page_idx]` for per-page trade module execution |
| dispatch_gate.py | 1772–1791 | `_ctx_to_dict` | Iterates `ctx.pages.items()` for JSON serialization |
| dispatch_gate.py | 1875 | `_print_report` | Iterates `ctx.pages.values()` for page type counts |
| dispatch_gate.py | 1903 | `_print_report` | Iterates `sorted(ctx.pages.items())` for scale source report |
| context.py | 408 | `check_for_leaks` | Iterates `context.pages.items()` checking confidence/page_type for leak warnings |
| context.py | 483 | `PlanSetContext.get_pages_by_type` | Reads `self.pages.values()` |
| context.py | 486 | `PlanSetContext.get_pages_by_discipline` | Reads `self.pages.values()` |
| context.py | 544 | `PlanSetContext.to_json` | Iterates `self.pages.items()` for serialization |
| trade_input_builder.py | 137–143 | `build_trade_input` | Reads `dispatch_ctx.pages.get(page_num)` to extract page_type, legends, zones, raw_tables |
| debug_module.py | 177–178 | `_section_page_intelligence` | Iterates `sorted(ctx.pages.keys())` and reads each PageContext for diagnostic table |
| debug_module.py | 264 | `run_debug` | Reads `list(ctx.pages.keys())` for relevant_pages |
| job_storage.py | 230 | `persist_dispatch_result` | Iterates `sorted(ctx.pages.items())` to persist page-level dispatch results |

### 2.3 Cascade note

`ctx.pages` is created entirely by `run_filter_2`. Filters 3, 4, and 5 mutate the existing PageContext objects in-place (adding cross_refs, legends, zones, flags). The mutation chain is:

```
Filter 2 creates → Filter 4 adds legends/schedule/raw_tables
                 → Filter 3 adds cross_refs_out/in, has_details, detail_count
                 → Filter 5 adds zones, primary_zone, has_title_block, has_drawing_area, callout_texts, spec_note_texts
```

Note: Filter 4 runs before Filter 3 in `run_dispatch` (line 1676–1679) so keynote legend info is available for cross-ref extraction.

---

## 3. `ctx.project` (ProjectMetadata) and `ctx.project_scope` (ProjectScope)

### 3.1 `ctx.project` — WRITES

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 413 | `run_filter_1` | Writes `ctx.project.total_pages = doc.page_count` |
| dispatch_gate.py | 1027–1031 | `_extract_project_metadata` | Writes `ctx.project.project_name` and `ctx.project.field_sources["project_name"]` from cover page |
| dispatch_gate.py | 1036–1039 | `_extract_project_metadata` | Writes `ctx.project.project_address` and `ctx.project.field_sources["project_address"]` from address regex |
| dispatch_gate.py | 1051–1054 | `_extract_project_metadata` | Writes `ctx.project.total_building_sf` and `ctx.project.field_sources["total_building_sf"]` from SF regex |
| dispatch_gate.py | 1070–1072 | `_extract_project_metadata` | Writes `ctx.project.project_name` and `ctx.project.field_sources["project_name"]` from title block fallback |
| context.py | 454 | `PlanSetContext.__init__` | Default-constructed `ProjectMetadata()` |

### 3.2 `ctx.project` — READS

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 1027 | `_extract_project_metadata` | Reads `ctx.project.project_name` (guard: `if not`) before writing |
| dispatch_gate.py | 1036 | `_extract_project_metadata` | Reads `ctx.project.project_address` (guard: `if m and not`) before writing |
| dispatch_gate.py | 1051 | `_extract_project_metadata` | Reads `ctx.project.total_building_sf` (guard: `if not`) before writing |
| dispatch_gate.py | 1060 | `_extract_project_metadata` | Reads `ctx.project.project_name` to decide whether to try title block fallback |
| dispatch_gate.py | 1074 | `_extract_project_metadata` | Reads `ctx.project.project_name` to break out of title block scan loop |
| dispatch_gate.py | 1817–1821 | `_ctx_to_dict` | Reads `ctx.project.project_name`, `.project_address`, `.project_number`, `.total_pages`, `.total_building_sf` |
| dispatch_gate.py | 1914–1919 | `_print_report` | Reads `ctx.project.project_name`, `.project_address`, `.total_building_sf` for CLI output |
| context.py | 405 | `check_for_leaks` | Reads `context.project.field_sources.items()` to check for LLM leaks into deterministic fields |

### 3.3 `ctx.project_scope` (ProjectScope) — WRITES

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 1391 | `run_scope_scanner` | Writes `ctx.project_scope = ProjectScope()` when no scope pages found |
| dispatch_gate.py | 1429–1441 | `run_scope_scanner` | Writes `ctx.project_scope = ProjectScope(scope_pages=..., spec_sections=..., detected_system=..., ...)` with all accumulated scope data |
| context.py | 686–698 | `PlanSetContext.from_json` | Restores `ctx.project_scope = ProjectScope(...)` from serialized JSON |

### 3.4 `ctx.project_scope` — READS

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 1495 | `_build_dispatch_only_input` | Reads `getattr(ctx, "project_scope", None)` to pass to TradeModuleInput |
| dispatch_gate.py | 1685 | `run_dispatch` (comment) | Documents that scope scanner builds `PlanSetContext.project_scope` |
| context.py | 632–643 | `PlanSetContext.to_json` | Reads all fields of `self.project_scope` for serialization |
| trade_input_builder.py | 143 | `build_trade_input` | Reads `getattr(dispatch_ctx, "project_scope", None)` to pass to TradeModuleInput |
| trade_module.py | 73 | `TradeModuleInput` | Declares `project_scope: Optional[Any]` field (receives the value) |
| roofing_module.py | 153–158 | `RoofingModule.detect_scope` | Reads `inp.project_scope.detected_system`, `.system_confidence`, `.system_evidence` for system detection priority |
| roofing_module.py | 188–193 | `RoofingModule.detect_scope` | Reads `inp.project_scope.roof_shape_signal`, `.system_evidence` for flat/steep fallback |
| roofing_module.py | 353 | `RoofingModule.analyze` | Reads `inp.project_scope` for scope material enrichment |
| roofing_module.py | 369–377 | `RoofingModule.analyze` | Reads `.spec_sections`, `.manufacturers`, `.material_mentions`, `.florida_signals`, `.roof_shape_signal`, `.scope_pages`, `.architect`, `.contractor` from project_scope |

### 3.5 Cascade note

`ctx.project` is written by two sites: `run_filter_1` (total_pages only) and `_extract_project_metadata` (name, address, SF). The metadata extractor runs after all five filters and scope scanner in `run_dispatch` (line 1701). `ctx.project` is consumed by serializers and CLI output only — no filter or trade module reads it.

`ctx.project_scope` is written exclusively by `run_scope_scanner`. It flows to trade modules via `_build_dispatch_only_input` (dispatch path) or `build_trade_input` (geometry path). `RoofingModule` is the primary consumer; `GlazingModule` does not read project_scope.

```
run_scope_scanner writes ctx.project_scope
  → _build_dispatch_only_input reads ctx.project_scope → passes to TradeModuleInput
  → build_trade_input reads dispatch_ctx.project_scope → passes to TradeModuleInput
  → RoofingModule.detect_scope reads inp.project_scope (weight-3 priority for system detection)
  → RoofingModule.analyze reads inp.project_scope (scope material enrichment for _scope field)
```

---

## 4. `ctx.dispatch_warnings`

### 4.1 WRITES

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 854–857 | `run_filter_4` | Appends quality gate removal count: "Filter 4 quality gate: N of M legends removed" |
| dispatch_gate.py | 1525–1529 | `_run_trade_modules` | Appends "trade module wiring: pdfplumber.open failed" when pdfplumber fails to open |
| dispatch_gate.py | 1578–1580 | `_run_trade_modules` | Appends per-page roofing.analyze error: "trade module page N roofing.analyze raised ..." |
| dispatch_gate.py | 1587–1589 | `_run_trade_modules` | Appends per-page glazing.analyze error: "trade module page N glazing.analyze raised ..." |
| dispatch_gate.py | 1606–1609 | `_run_trade_modules` | Appends roofing error-rate threshold warning when >25% |
| dispatch_gate.py | 1611–1614 | `_run_trade_modules` | Appends glazing error-rate threshold warning when >25% |
| dispatch_gate.py | 1689 | `run_dispatch` | Appends "scope scanner failed: {e}" on scope scanner exception |
| dispatch_gate.py | 1698 | `run_dispatch` | Appends "architect_profile detection failed: {e}" on profile exception |
| dispatch_gate.py | 1712 | `run_dispatch` | Appends "trade module wiring failed: {e}" on trade module top-level exception |
| dispatch_gate.py | 1722 | `run_dispatch` | Appends "D.2 job persistence failed: {e}" on persistence exception |
| dispatch_gate.py | 1725 | `run_dispatch` | Extends with `check_for_leaks(ctx)` output (leak detection warnings) |
| context.py | 403–414 | `check_for_leaks` | Returns list of warning strings (consumed by dispatch_gate.py:1725 via `.extend()`) |
| context.py | 679 | `PlanSetContext.from_json` | Restores `ctx.dispatch_warnings` from serialized JSON |

### 4.2 READS

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 1843 | `_ctx_to_dict` | Reads `ctx.dispatch_warnings` for JSON serialization |
| dispatch_gate.py | 1923–1925 | `_print_report` | Reads `ctx.dispatch_warnings` for CLI warning output |
| context.py | 630 | `PlanSetContext.to_json` | Reads `self.dispatch_warnings` for serialization |
| debug_module.py | 151 | `_section_dispatch_health` | Reads `ctx.dispatch_warnings` for diagnostic warnings list |
| debug_module.py | 152 | `_section_dispatch_health` | Reads `len(ctx.dispatch_warnings)` for warning count |

### 4.3 Cascade note

`dispatch_warnings` is an append-only accumulator. It is written by many sites across the dispatch pipeline but is never read by any filter to influence control flow. It is purely an output/diagnostic channel. The writes come from:

```
Filter 4 (legend quality gate)
_run_trade_modules (pdfplumber open failure, per-page errors, error-rate thresholds)
run_dispatch (scope scanner failure, architect profile failure, trade module wiring failure, D.2 persistence failure)
check_for_leaks (deterministic field leaks, unscored pages, low cross-ref resolution)
```

No filter or trade module reads `dispatch_warnings` to make decisions.

---

## 5. `ctx.trade_module_outputs`

### 5.1 WRITES

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 1593 | `_run_trade_modules` | Writes `ctx.trade_module_outputs[page_idx] = per_page` where per_page is `{"roofing": TradeModuleOutput, "glazing": TradeModuleOutput}` |
| context.py | 464 | `PlanSetContext.__init__` | Default empty dict `field(default_factory=dict)` |

### 5.2 READS

| File | Line | Function | Description |
|------|------|----------|-------------|
| job_storage.py | 261 | `persist_trade_outputs` | Iterates `sorted(ctx.trade_module_outputs.items())` to persist per-page per-trade outputs to SQLite |

### 5.3 Cascade note

`trade_module_outputs` is a terminal write. It is populated by `_run_trade_modules` (Stage 13, D.1) only when `storage is not None`. It is consumed only by `persist_trade_outputs` (D.2 job persistence). No filter, trade module, or diagnostic reads this field to influence behavior.

```
_run_trade_modules writes ctx.trade_module_outputs[page_idx]
  → persist_trade_outputs reads ctx.trade_module_outputs (D.2 persistence only)
```

---

## 6. `ctx.project_scope.scope_pages`

Note: `PlanSetContext` does not have a top-level `scope_pages` field. The field is `ctx.project_scope.scope_pages` (a `list[int]` inside `ProjectScope`).

### 6.1 WRITES

| File | Line | Function | Description |
|------|------|----------|-------------|
| dispatch_gate.py | 1430 | `run_scope_scanner` | Writes `scope_pages=page_list` where `page_list = [sp.page_number for sp in pages]` (page indices of classified scope pages) |
| dispatch_gate.py | 1391 | `run_scope_scanner` | Writes `ctx.project_scope = ProjectScope()` (empty scope_pages=[]) when no scope pages found |
| context.py | 687 | `PlanSetContext.from_json` | Restores `scope_pages=ps_d.get("scope_pages", [])` from serialized JSON |

### 6.2 READS

| File | Line | Function | Description |
|------|------|----------|-------------|
| context.py | 633 | `PlanSetContext.to_json` | Reads `self.project_scope.scope_pages` for serialization |
| roofing_module.py | 374 | `RoofingModule.analyze` | Reads `getattr(ps, "scope_pages", [])` to include in scope material enrichment dict |

### 6.3 Cascade note

`scope_pages` is the list of page indices that `_classify_scope_pages` identified as scope/cover/separator pages. It is written once by `run_scope_scanner` and only read for serialization and for the RoofingModule's `_scope` pseudo-field enrichment (informational, not used for quantity derivation or system detection).

---

## 7. Filter chain trace: `dispatch_gate.py`

### 7.1 `run_filter_1` — Document Structure

| | |
|---|---|
| **Lines** | 359–414 |
| **ctx fields written** | `ctx.sheet_map_source`, `ctx.sheet_map[sn]`, `ctx.page_to_sheet[page_idx]`, `ctx.project.total_pages`, `ctx.filters_completed` |
| **ctx fields read** | None (reads PDF via engine, not ctx) |
| **Summary** | Builds the sheet map from a drawing index page (≥10 sheet numbers) or falls back to per-page title block scanning. Populates the reverse page_to_sheet index. Sets project.total_pages. |

### 7.2 `run_filter_2` — Page Classification

| | |
|---|---|
| **Lines** | 439–502 |
| **ctx fields written** | `ctx.pages[page_idx]` (creates PageContext), mutates `ctx.sheet_map[sheet_num].page_type` (line 459) |
| **ctx fields read** | `ctx.page_to_sheet.get(page_idx)`, `ctx.sheet_map[sheet_num]` (discipline, title) |
| **Summary** | Creates a PageContext for every page. Reads sheet_map to inherit discipline and title. Classifies page_type from title block keywords. Mutates the SheetEntry.page_type on the sheet_map entry. Contains the MEP fallback (lines 464–466): if page_type is UNKNOWN and discipline is M/E/P, assigns MEP_PLAN. |

### 7.3 `run_filter_3` — Cross-Reference Extraction

| | |
|---|---|
| **Lines** | 586–632 |
| **ctx fields written** | `ctx.all_cross_refs` (extends), `ctx.pages[page_idx].cross_refs_out`, `ctx.pages[page_idx].has_details`, `ctx.pages[page_idx].detail_count`, `ctx.pages[target_page].cross_refs_in`, `ctx.resolved_count`, `ctx.unresolved_count`, `ctx.filters_completed` |
| **ctx fields read** | `ctx.all_legends` (for keynote page detection), `ctx.sheet_map.get()` and `ctx.sheet_map.items()` (for cross-ref resolution), `ctx.pages` (to attach refs to PageContext) |
| **Summary** | Extracts detail refs, sheet refs, see-refs, and keynote refs from text blocks. Resolves target sheets against sheet_map. Populates cross_refs_out and cross_refs_in on PageContext objects. |

### 7.4 `run_filter_4` — Legend/Schedule Parsing

| | |
|---|---|
| **Lines** | 831–882 |
| **ctx fields written** | `ctx.pages[page_idx].raw_tables` (on SCHEDULE_SHEET pages), `ctx.dispatch_warnings` (quality gate message), `ctx.all_legends`, `ctx.pages[page_idx].legends`, `ctx.pages[page_idx].has_legend`, `ctx.pages[page_idx].has_schedule`, `ctx.legends_by_type`, `ctx.filters_completed` |
| **ctx fields read** | `ctx.pages.get(page_idx)` (to check page_type for schedule detection), `ctx.pdf_path` (for pdfplumber table extraction) |
| **Summary** | Finds numbered note/legend lists on every page via text block scanning. Supplements with pdfplumber table extraction on SCHEDULE_SHEET pages. Runs quality gate to remove noise. Associates legends with page contexts. Builds legends_by_type index. |

### 7.5 `run_filter_5` — Zone Classification

| | |
|---|---|
| **Lines** | 889–996 |
| **ctx fields written** | `page_ctx.has_title_block`, `page_ctx.primary_zone`, `page_ctx.has_drawing_area`, `page_ctx.zones`, `page_ctx.spec_note_texts`, `page_ctx.callout_texts`, `ctx.filters_completed` |
| **ctx fields read** | `ctx.pages.get(page_idx)` (to get existing PageContext), `page_ctx.legends` (to create legend_area zones) |
| **Summary** | Wraps zone_filter.py for detail zone detection and title block detection. Creates main_drawing, notes_area, legend_area, and detail_view zones. Classifies text blocks by zone (spec notes vs callouts). |

### 7.6 Execution order in `run_dispatch`

The filters run in this order (dispatch_gate.py lines 1669–1696):

```
1. run_filter_1        (sheet map)
2. run_filter_2        (page classification — reads sheet_map)
3. run_filter_4        (legends — reads pages for SCHEDULE_SHEET check)
4. run_filter_3        (cross-refs — reads all_legends for keynote detection, sheet_map for resolution)
5. run_filter_5        (zones — reads pages, reads page_ctx.legends)
6. run_scope_scanner   (scope pages — reads PDF, writes ctx.project_scope)
7. architect profile   (optional, reads title block zones from ctx.pages)
8. _extract_project_metadata (reads PDF, writes ctx.project)
9. _run_trade_modules  (optional, reads ctx.pages/project_scope, writes ctx.trade_module_outputs)
10. D.2 persistence    (optional, reads ctx.pages/trade_module_outputs)
11. check_for_leaks    (reads ctx.project, ctx.pages, writes to dispatch_warnings)
```

Note: Filters 4 and 3 are intentionally reordered (4 before 3) so that keynote legend detection is available when cross-references are extracted.

---

## 8. Trade module Protocol contract

Defined in `core/trade_module.py`.

### 8.1 Protocol: `TradeModule`

```python
class TradeModule(Protocol):
    TRADE_NAME: str
    FIELDS: list[str]

    def analyze(self, input: TradeModuleInput) -> TradeModuleOutput: ...
```

### 8.2 `TradeModuleInput` — what the module receives

| Field | Type | ctx source | Description |
|-------|------|------------|-------------|
| `polygon_area_sqin` | float | geometry result | Raw polygon area in square inches |
| `polygon_area_sf` | float | geometry result | Polygon area in square feet |
| `polygon_perimeter_in` | float | geometry result | Polygon perimeter in inches |
| `polygon_perimeter_lf` | float | geometry result | Polygon perimeter in linear feet |
| `polygon_bbox` | tuple | geometry result | (x0, y0, x1, y1) in PDF points |
| `polygon_vertices` | int | geometry result | Vertex count of building polygon |
| `scale_fpi` | float | geometry result | Feet per inch scale factor |
| `scale_source` | str | geometry result | Scale source method name |
| `scale_confidence` | float | geometry result | Scale confidence score |
| `detection_source` | str | geometry result | Detection method name |
| `interior_text_blocks` | list | filtered from text blocks | Text blocks inside polygon + margin |
| `equipment_callouts` | list | filtered from text blocks | Short text with equipment keywords |
| `dimension_strings` | list | filtered from text blocks | Text matching dimension patterns |
| `page_type` | str | `ctx.pages[N].page_type.value` | PageType enum value as string |
| `page_legends` | list | `ctx.pages[N].legends` | Legend objects for this page |
| `page_zones` | list | `ctx.pages[N].zones` | PageZone objects for this page |
| `tables` | Optional[list] | `ctx.pages[N].raw_tables` | pdfplumber table data |
| `project_scope` | Optional[Any] | `ctx.project_scope` | ProjectScope from scope scanner |
| `page_number` | Optional[int] | page index | 0-based page number |

**ctx fields read (indirectly via input construction):**
- `ctx.pages[page_num].page_type` — via `build_trade_input` (trade_input_builder.py:139) or `_build_dispatch_only_input` (dispatch_gate.py:1472)
- `ctx.pages[page_num].legends` — via both builders
- `ctx.pages[page_num].zones` — via both builders
- `ctx.pages[page_num].raw_tables` — via both builders
- `ctx.project_scope` — via both builders (trade_input_builder.py:143, dispatch_gate.py:1495)

### 8.3 `TradeModuleOutput` — what the module returns

| Field | Type | ctx destination | Description |
|-------|------|-----------------|-------------|
| `fields` | dict[str, TradeFieldValue] | `ctx.trade_module_outputs[page_idx][trade_name].fields` | Named field values with provenance |
| `warnings` | list[str] | `ctx.trade_module_outputs[page_idx][trade_name].warnings` | Relationship warnings |
| `equipment_pins` | list[dict] | `ctx.trade_module_outputs[page_idx][trade_name].equipment_pins` | Pin positions for overlay |
| `glazing_items` | Optional[list[dict]] | `ctx.trade_module_outputs[page_idx][trade_name].glazing_items` | GlazingModule only: per-item window records |
| `door_items` | Optional[list[dict]] | `ctx.trade_module_outputs[page_idx][trade_name].door_items` | GlazingModule only: per-item door records |
| `storefront_items` | Optional[list[dict]] | `ctx.trade_module_outputs[page_idx][trade_name].storefront_items` | GlazingModule only: per-item storefront records |

**ctx fields written (indirectly via `_run_trade_modules`):**
- `ctx.trade_module_outputs[page_idx]["roofing"]` — RoofingModule output (dispatch_gate.py:1575)
- `ctx.trade_module_outputs[page_idx]["glazing"]` — GlazingModule output (dispatch_gate.py:1584)

### 8.4 Concrete implementations

| Module | File | `TRADE_NAME` | ctx fields read via input | Notes |
|--------|------|-------------|---------------------------|-------|
| `RoofingModule` | roofing_module.py | `"roofing"` | `inp.project_scope` (system detection + scope enrichment), `inp.page_legends` (legend keyword scan), `inp.interior_text_blocks` / `inp.equipment_callouts` (callout scan), `inp.polygon_area_sf` / `inp.polygon_perimeter_lf` (quantity derivation), `inp.scale_fpi` / `inp.scale_confidence` (confidence gating) | Never touches PlanSetContext directly. All input via TradeModuleInput. |
| `GlazingModule` | glazing_module.py | `"glazing"` | `inp.tables` (schedule-first parsing), `inp.interior_text_blocks` (elevation reconciliation, title-page fallback, various-pages fallback), `inp.page_number` (source_page in output items) | Does NOT read `inp.project_scope`. Never touches PlanSetContext directly. |
| `DebugModule` | debug_module.py | `"debug"` | Receives full `PlanSetContext` (not TradeModuleInput). Reads `ctx.dispatch_complete`, `ctx.filters_completed`, `ctx.dispatch_warnings`, `ctx.dispatch_timestamp`, `ctx.total_pages`, `ctx.sheet_map_source`, `ctx.sheet_map`, `ctx.page_to_sheet`, `ctx.pages`, `ctx.all_legends`, `ctx.all_cross_refs` (implicit via pages). Writes `ctx.trade_contexts["debug"]`. | DebugModule does NOT follow the TradeModule protocol — it receives PlanSetContext directly. |

### 8.5 Input builders

Two paths construct `TradeModuleInput`:

| Builder | File | When used | ctx fields read |
|---------|------|-----------|-----------------|
| `build_trade_input` | trade_input_builder.py:71 | Geometry route (server/API) — receives geometry_result + dispatch_ctx | `dispatch_ctx.pages.get(page_num)` → page_type, legends, zones, raw_tables; `dispatch_ctx.project_scope` |
| `_build_dispatch_only_input` | dispatch_gate.py:1455 | Dispatch path (Stage 13) — no geometry available | `ctx.pages.get(page_idx)` → page_type, legends, zones; `ctx.project_scope`; geometry fields zeroed |

---

## Vault SHA-1 verification (pre-deliverable)

```
2a708d193ac5247472d589252bbc3766ced9041f  dispatch_gate.py
ae9e5b284191b45de419faacf11771da27a548f9  roofing_module.py
52c014421915ec6a66b4a6860b71a0a3274920f2  glazing_module.py
78f71d9030cde3b173389603f5f39bd6bedaac07  debug_module.py
```
