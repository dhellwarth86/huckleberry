# Page-Type Verification — Block 3: Filter 4 Cache Audit (static read)

**Date:** 2026-04-29
**Phase:** Page-type verification + coupling diagnostic
**Scope:** static read of `core/context.py` PlanSetContext + PageContext field lists; static read of `core/dispatch_gate.py` `_parse_tables_on_page` + `run_filter_4` body lines.

This report is one-shot, not per-bidset. It documents the Bug 3 architectural surface — whether dispatch caches raw tables anywhere on `PlanSetContext` / `PageContext`. The answer determines what shape the eventual Bug 3 fix must take.

---

## §1 — Field enumeration

**`PlanSetContext` fields (21):**

```
pdf_path, pdf_hash, total_pages, sheet_map, page_to_sheet, sheet_map_source, pages, all_cross_refs, resolved_count, unresolved_count, all_legends, legends_by_type, project, trade_contexts, bid, architect_profile, project_scope, filters_completed, dispatch_complete, dispatch_timestamp, dispatch_warnings
```

**`PageContext` fields (21):**

```
page_index, sheet_number, title, discipline, page_type, scale, confidence, zones, primary_zone, legends, cross_refs_out, cross_refs_in, callout_texts, spec_note_texts, has_drawing_area, has_title_block, has_details, has_schedule, has_legend, detail_count, source_tag
```

## §2 — Table-field search

- Fields containing 'table' in `PlanSetContext`: []
- Fields containing 'table' in `PageContext`: []
- **`any_raw_tables_cached`: False**

## §3 — Evidence lines (from dispatch_gate.py)

- dispatch_gate.py line 744: tables = page.extract_tables() — local-scope
- dispatch_gate.py line 768-776: legends.append(Legend(...)) — wraps each table into a Legend object
- dispatch_gate.py line 777: return legends — returns Legend objects, not raw tables
- dispatch_gate.py line 840-841: legends.extend(table_legends) — only Legend objects propagated
- dispatch_gate.py line 855: ctx.all_legends = clean_legends — only filtered Legend objects stored
- context.py PlanSetContext + PageContext — no 'tables' or 'raw_tables' field; field lists enumerated above

## §4 — Implication for Bug 3 fix path

raw tables not cached anywhere on PlanSetContext or PageContext; the eventual fix needs either (a) cache add to PlanSetContext or PageContext (touches dispatch's data contract), (b) per-page re-extraction in trade_input_builder (the harness pattern the sweep + profile already use; pays extract_tables cost twice if Filter 4 also runs on the same page), or (c) extension of _parse_tables_on_page in dispatch_gate.py to optionally cache raw tables alongside the Legend objects (one-touch, dispatch-side).

## §5 — Raw payload

```json
##DIAG_START:filter4_cache_audit##
{
  "plan_set_context_fields": [
    "pdf_path",
    "pdf_hash",
    "total_pages",
    "sheet_map",
    "page_to_sheet",
    "sheet_map_source",
    "pages",
    "all_cross_refs",
    "resolved_count",
    "unresolved_count",
    "all_legends",
    "legends_by_type",
    "project",
    "trade_contexts",
    "bid",
    "architect_profile",
    "project_scope",
    "filters_completed",
    "dispatch_complete",
    "dispatch_timestamp",
    "dispatch_warnings"
  ],
  "page_context_fields": [
    "page_index",
    "sheet_number",
    "title",
    "discipline",
    "page_type",
    "scale",
    "confidence",
    "zones",
    "primary_zone",
    "legends",
    "cross_refs_out",
    "cross_refs_in",
    "callout_texts",
    "spec_note_texts",
    "has_drawing_area",
    "has_title_block",
    "has_details",
    "has_schedule",
    "has_legend",
    "detail_count",
    "source_tag"
  ],
  "table_field_search": {
    "fields_with_table_in_name_planset": [],
    "fields_with_table_in_name_pagectx": [],
    "any_raw_tables_cached": false,
    "evidence_lines": [
      "dispatch_gate.py line 744: tables = page.extract_tables() \u2014 local-scope",
      "dispatch_gate.py line 768-776: legends.append(Legend(...)) \u2014 wraps each table into a Legend object",
      "dispatch_gate.py line 777: return legends \u2014 returns Legend objects, not raw tables",
      "dispatch_gate.py line 840-841: legends.extend(table_legends) \u2014 only Legend objects propagated",
      "dispatch_gate.py line 855: ctx.all_legends = clean_legends \u2014 only filtered Legend objects stored",
      "context.py PlanSetContext + PageContext \u2014 no 'tables' or 'raw_tables' field; field lists enumerated above"
    ]
  },
  "implication_for_bug3_fix": "raw tables not cached anywhere on PlanSetContext or PageContext; the eventual fix needs either (a) cache add to PlanSetContext or PageContext (touches dispatch's data contract), (b) per-page re-extraction in trade_input_builder (the harness pattern the sweep + profile already use; pays extract_tables cost twice if Filter 4 also runs on the same page), or (c) extension of _parse_tables_on_page in dispatch_gate.py to optionally cache raw tables alongside the Legend objects (one-touch, dispatch-side)."
}
##DIAG_END:filter4_cache_audit##
```

## §6 — Closing

Static read only. No code execution dependent on this block. The eventual Bug 3 fix path is named in §4 above as an architectural observation, NOT a recommendation. Daniel and extended-thinking Claude make the call about which fix path to pursue.
