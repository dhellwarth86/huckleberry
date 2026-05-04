# Sweep Observation Report — Shoppes at Avalon — Spring Hill — MEC

**Date:** 2026-04-28
**Phase:** Three-bidset sweep (post-C.3c-build, post-C.5; modules vault-ruled)
**Bidset short name:** `shoppes-at-avalon`
**Bidset file:** `C:\huck stage 2\full bid sets\Shoppes at Avalon - Spring Hill - MEC.pdf`
**Page count:** 97
**File size:** 70,030,816 bytes (~66.8 MB)
**Wall-clock dispatch time:** 60.2s
**Wall-clock per-page module time (roofing+glazing combined):** 653.6s
**Wall-clock run_debug time:** 0.0s

**Type of artifact:** observation only. No grading. No correctness
comparison. No 'needs ground truth' labels. No fix lists. No tuning
recommendations. The roofing module, glazing module, and debug
module are vault-ruled per CLAUDE.md §3 Decision 15. This report
describes what the modules produced; the future tuning planning
conversation decides what to do with the data.

**Harness note (TradeModuleInput construction).** The standard
`build_trade_input()` in `core/trade_input_builder.py` requires a
`geometry_result` dict from Stages 6-9 (polygon, area, perimeter,
scale). Stages 6-9 geometry is ported (B.2/B.3) but the dispatch
→ geometry route is not wired (Phase D/E). The sweep harness
therefore constructs `TradeModuleInput` directly per page with
dispatch-side state available now: `page_legends`, `page_zones`,
`page_type`, `project_scope`, plus per-page text and tables
extracted via pdfplumber. `polygon_*` fields are zero/empty;
`scale_source = 'unwired'`. This is the 'C.2-established
equivalent' path explicitly permitted by `MARCH_ORDERS_three_
bidset_sweep.md §6` when the standard builder's preconditions
aren't met.

---

## §1 — Bidset Metadata

- Display name: Shoppes at Avalon — Spring Hill — MEC
- Short name: `shoppes-at-avalon`
- Filename: `Shoppes at Avalon - Spring Hill - MEC.pdf`
- Full path: `C:\huck stage 2\full bid sets\Shoppes at Avalon - Spring Hill - MEC.pdf`
- Page count: 97
- File size: 70,030,816 bytes (66.8 MB)
- Prior characterization: Prior C.3a glazing-seed characterization in backend/C3_GLAZING_SEED_VALIDATION.md (single-bidset glazing scope walkthrough). Sanity-check baseline only; not a comparison target.

## §2 — Dispatch Output (PlanSetContext)

### project_scope

- detected_system: `None`
- system_confidence: `0.0`
- system_evidence: `''`
- scope_pages: `[]`
- spec_sections: `[]`
- manufacturers: `[]`
- material_mentions: `[]`
- florida_signals: `[]`
- roof_shape_signal: `None`
- architect: `None`
- contractor: `None`

### dispatch_complete: `True`
### filters_completed: `['filter_1', 'filter_2', 'filter_4', 'filter_3', 'filter_5']`
### dispatch_warnings: `['Filter 4 quality gate: 2 of 3 legends removed (1 kept)']`
### total_pages: `97`
### sheet_count: `30`
### mapped_pages: `19`
### sheet_map_source: `drawing_index`

## §3 — Roofing Module Output

### Aggregated

- Total `fields` entries across all pages: 830
- Total warnings: 0
- Total equipment_pins: 0
- Pages with non-empty output: 97
- Pages with empty output: 0

### Per-page summary (only pages with non-empty output shown)

| Page | Sheet | Fields | Warnings | Equip pins |
|---:|---|---:|---:|---:|
| 0 | LS-101 | 8 | 0 | 0 |
| 1 | A-601 | 9 | 0 | 0 |
| 2 | G-003 | 8 | 0 | 0 |
| 3 | --- | 8 | 0 | 0 |
| 4 | A-402 | 8 | 0 | 0 |
| 5 | --- | 9 | 0 | 0 |
| 6 | A-102 | 8 | 0 | 0 |
| 7 | A-111 | 8 | 0 | 0 |
| 8 | A-101 | 11 | 0 | 0 |
| 9 | A-306 | 9 | 0 | 0 |
| 10 | A-301 | 10 | 0 | 0 |
| 11 | A-302 | 10 | 0 | 0 |
| 12 | --- | 10 | 0 | 0 |
| 13 | --- | 10 | 0 | 0 |
| 14 | --- | 10 | 0 | 0 |
| 15 | --- | 8 | 0 | 0 |
| 16 | A-401 | 8 | 0 | 0 |
| 17 | --- | 9 | 0 | 0 |
| 18 | --- | 8 | 0 | 0 |
| 19 | A-602 | 8 | 0 | 0 |
| 20 | --- | 8 | 0 | 0 |
| 21 | --- | 8 | 0 | 0 |
| 22 | --- | 8 | 0 | 0 |
| 23 | --- | 8 | 0 | 0 |
| 24 | --- | 8 | 0 | 0 |
| 25 | --- | 8 | 0 | 0 |
| 26 | --- | 8 | 0 | 0 |
| 27 | --- | 8 | 0 | 0 |
| 28 | --- | 8 | 0 | 0 |
| 29 | --- | 8 | 0 | 0 |
| 30 | --- | 8 | 0 | 0 |
| 31 | --- | 8 | 0 | 0 |
| 32 | --- | 9 | 0 | 0 |
| 33 | --- | 9 | 0 | 0 |
| 34 | --- | 8 | 0 | 0 |
| 35 | --- | 8 | 0 | 0 |
| 36 | A-100 | 10 | 0 | 0 |
| 37 | A-201 | 8 | 0 | 0 |
| 38 | --- | 8 | 0 | 0 |
| 39 | --- | 8 | 0 | 0 |
| 40 | A-121 | 10 | 0 | 0 |
| 41 | A-303 | 8 | 0 | 0 |
| 42 | --- | 8 | 0 | 0 |
| 43 | --- | 10 | 0 | 0 |
| 44 | --- | 10 | 0 | 0 |
| 45 | --- | 10 | 0 | 0 |
| 46 | A-304 | 8 | 0 | 0 |
| 47 | A-305 | 9 | 0 | 0 |
| 48 | --- | 8 | 0 | 0 |
| 49 | --- | 9 | 0 | 0 |
| 50 | --- | 10 | 0 | 0 |
| 51 | --- | 10 | 0 | 0 |
| 52 | --- | 9 | 0 | 0 |
| 53 | --- | 8 | 0 | 0 |
| 54 | --- | 8 | 0 | 0 |
| 55 | --- | 8 | 0 | 0 |
| 56 | --- | 8 | 0 | 0 |
| 57 | --- | 8 | 0 | 0 |
| 58 | --- | 8 | 0 | 0 |
| 59 | --- | 8 | 0 | 0 |
| 60 | --- | 8 | 0 | 0 |
| 61 | --- | 8 | 0 | 0 |
| 62 | --- | 8 | 0 | 0 |
| 63 | --- | 8 | 0 | 0 |
| 64 | --- | 8 | 0 | 0 |
| 65 | --- | 9 | 0 | 0 |
| 66 | --- | 9 | 0 | 0 |
| 67 | --- | 8 | 0 | 0 |
| 68 | --- | 8 | 0 | 0 |
| 69 | --- | 10 | 0 | 0 |
| 70 | --- | 8 | 0 | 0 |
| 71 | --- | 8 | 0 | 0 |
| 72 | --- | 8 | 0 | 0 |
| 73 | --- | 10 | 0 | 0 |
| 74 | --- | 8 | 0 | 0 |
| 75 | --- | 8 | 0 | 0 |
| 76 | --- | 10 | 0 | 0 |
| 77 | --- | 10 | 0 | 0 |
| 78 | --- | 10 | 0 | 0 |
| 79 | --- | 8 | 0 | 0 |
| 80 | --- | 9 | 0 | 0 |
| 81 | --- | 8 | 0 | 0 |
| 82 | --- | 9 | 0 | 0 |
| 83 | --- | 9 | 0 | 0 |
| 84 | --- | 10 | 0 | 0 |
| 85 | --- | 9 | 0 | 0 |
| 86 | --- | 8 | 0 | 0 |
| 87 | S-401 | 8 | 0 | 0 |
| 88 | --- | 8 | 0 | 0 |
| 89 | --- | 8 | 0 | 0 |
| 90 | --- | 8 | 0 | 0 |
| 91 | --- | 8 | 0 | 0 |
| 92 | --- | 8 | 0 | 0 |
| 93 | --- | 8 | 0 | 0 |
| 94 | --- | 8 | 0 | 0 |
| 95 | --- | 8 | 0 | 0 |
| 96 | --- | 8 | 0 | 0 |

### Per-page detail (only pages with non-empty output)

#### Page 0 (sheet `LS-101`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 1 (sheet `A-601`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "walkway_pads": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 enter manually",
      "display_name": "Walkway Pads",
      "unit": "LF"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "_scope": {
      "value": "PVC Single Ply",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'PVC'",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 2 (sheet `G-003`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 3 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 4 (sheet `A-402`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 5 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "walkway_pads": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 enter manually",
      "display_name": "Walkway Pads",
      "unit": "LF"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "_scope": {
      "value": "PVC Single Ply",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'PVC'",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 6 (sheet `A-102`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 7 (sheet `A-111`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 8 (sheet `A-101`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for TPO Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for TPO Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "walkway_pads": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for TPO Single Ply \u2014 enter manually",
      "display_name": "Walkway Pads",
      "unit": "LF"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for TPO Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for TPO Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for TPO Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for TPO Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for TPO Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "cricket": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Crickets",
      "unit": "SF"
    },
    "_scope": {
      "value": "TPO Single Ply",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'TPO'",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 9 (sheet `A-306`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "walkway_pads": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 enter manually",
      "display_name": "Walkway Pads",
      "unit": "LF"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "_scope": {
      "value": "PVC Single Ply",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'PVC'",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 10 (sheet `A-301`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "trim": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Trim",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 11 (sheet `A-302`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "trim": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Trim",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 12 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "trim": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Trim",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 13 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "trim": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Trim",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 14 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "trim": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Trim",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 15 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 16 (sheet `A-401`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 17 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "trim": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Trim",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 18 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 19 (sheet `A-602`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 20 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 21 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 22 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 23 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 24 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 25 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 26 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 27 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 28 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 29 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 30 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 31 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 32 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "walkway_pads": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 enter manually",
      "display_name": "Walkway Pads",
      "unit": "LF"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "_scope": {
      "value": "PVC Single Ply",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'PVC'",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 33 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "ridge_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Ridge Cap",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 34 (sheet `---`)

```json
{
  "fields": {
    "ridge_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Asphalt Shingle \u2014 enter manually",
      "display_name": "Ridge Cap",
      "unit": "LF"
    },
    "hip_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Asphalt Shingle \u2014 enter manually",
      "display_name": "Hip Cap",
      "unit": "LF"
    },
    "valley": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Asphalt Shingle \u2014 enter manually",
      "display_name": "Valley",
      "unit": "LF"
    },
    "ice_water_shield": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Asphalt Shingle \u2014 enter manually",
      "display_name": "Ice & Water Shield",
      "unit": "SF"
    },
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Asphalt Shingle \u2014 enter manually",
      "display_name": "Gutters",
      "unit": "LF"
    },
    "downspout": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Asphalt Shingle \u2014 no callouts found, enter manually",
      "display_name": "Downspouts",
      "unit": "EA"
    },
    "clips": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Panel Clips",
      "unit": "EA"
    },
    "_scope": {
      "value": "Asphalt Shingle",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'CERTAINTEED'",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 35 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 36 (sheet `A-100`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "walkway_pads": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 enter manually",
      "display_name": "Walkway Pads",
      "unit": "LF"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Gutters",
      "unit": "LF"
    },
    "_scope": {
      "value": "PVC Single Ply",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'PVC'",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 37 (sheet `A-201`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 38 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 39 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 40 (sheet `A-121`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "walkway_pads": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 enter manually",
      "display_name": "Walkway Pads",
      "unit": "LF"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for PVC Single Ply \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "_scope": {
      "value": "PVC Single Ply",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'PVC'",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 41 (sheet `A-303`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 42 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 43 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "ridge_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Ridge Cap",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 44 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "ridge_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Ridge Cap",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 45 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "ridge_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Ridge Cap",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 46 (sheet `A-304`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 47 (sheet `A-305`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 48 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 49 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "ridge_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Ridge Cap",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 50 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "ridge_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Ridge Cap",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 51 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "ridge_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Ridge Cap",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 52 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 53 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 54 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 55 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 56 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 57 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 58 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

#### Page 59 (sheet `---`)

```json
{
  "fields": {
    "drains": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Drains",
      "unit": "EA"
    },
    "scuppers": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Scuppers",
      "unit": "EA"
    },
    "hatches": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Roof Hatches",
      "unit": "EA"
    },
    "rtus": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Rooftop Units / RTUs",
      "unit": "EA"
    },
    "curbs": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Equipment Curbs",
      "unit": "EA"
    },
    "pipe_boots": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Pipe Boots / Vents",
      "unit": "EA"
    },
    "exhaust_fans": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Unknown \u2014 universal items only \u2014 no callouts found, enter manually",
      "display_name": "Exhaust Fans",
      "unit": "EA"
    },
    "_scope": {
      "value": "Unknown \u2014 universal items only",
      "confidence": 0.0,
      "source": "auto_text",
      "evidence": "no system keyword match",
      "display_name": "Roof System",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": null,
  "door_items": null,
  "storefront_items": null
}
```

*(37 more non-empty roofing pages truncated for artifact size)*

## §4 — Glazing Module Output

### Aggregated

- Total glazing_items across all pages: 43
- Total door_items: 22
- Total storefront_items: 22
- Pages with any glazing module content (any of the three lists non-empty): 22
- Pages with empty output: 75

### Per-page summary (only pages with non-empty output shown)

| Page | Sheet | glazing_items | door_items | storefront_items |
|---:|---|---:|---:|---:|
| 0 | LS-101 | 0 | 4 | 0 |
| 1 | A-601 | 6 | 0 | 0 |
| 2 | G-003 | 2 | 0 | 0 |
| 5 | --- | 1 | 0 | 0 |
| 6 | A-102 | 1 | 0 | 0 |
| 8 | A-101 | 3 | 0 | 0 |
| 9 | A-306 | 0 | 0 | 8 |
| 18 | --- | 0 | 6 | 0 |
| 31 | --- | 6 | 0 | 0 |
| 32 | --- | 6 | 0 | 0 |
| 37 | A-201 | 1 | 0 | 0 |
| 41 | A-303 | 0 | 0 | 1 |
| 42 | --- | 0 | 0 | 4 |
| 52 | --- | 0 | 6 | 0 |
| 64 | --- | 8 | 0 | 0 |
| 65 | --- | 6 | 0 | 0 |
| 69 | --- | 1 | 0 | 0 |
| 70 | --- | 1 | 0 | 1 |
| 73 | --- | 1 | 0 | 0 |
| 74 | --- | 0 | 0 | 5 |
| 75 | --- | 0 | 0 | 3 |
| 85 | --- | 0 | 6 | 0 |

### Per-page detail (only pages with non-empty output)

#### Page 0 (sheet `LS-101`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 4 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "4 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [
    {
      "mark": "101",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": 55.0,
      "height_ft": 24.0,
      "source_page": 0,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 0,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 0,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 0,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 1 (sheet `A-601`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 6 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "6 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 1,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 1,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 1,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 1,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 1,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 1,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 2 (sheet `G-003`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 2 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "2 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "101",
      "count": 0,
      "system": "curtain_wall_captured",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 12.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 2,
      "confidence": 0.4
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 2,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 5 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "102",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 5,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 6 (sheet `A-102`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "D-0",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 1.0,
      "height_ft": 1.0,
      "sqft": 1.0,
      "location": "",
      "source_page": 6,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 8 (sheet `A-101`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 3 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "3 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "173",
      "count": 0,
      "system": "window_hollow_metal",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 3.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 8,
      "confidence": 0.4
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 8,
      "confidence": 0.2
    },
    {
      "mark": "121",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 8,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 9 (sheet `A-306`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 0 door / 8 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "8 schedule rows parsed; 8 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-1",
      "count": 8,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 9,
      "confidence": 0.2
    },
    {
      "mark": "SF-1",
      "count": 8,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 9,
      "confidence": 0.2
    },
    {
      "mark": "SF-1",
      "count": 8,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 9,
      "confidence": 0.2
    },
    {
      "mark": "SF-1",
      "count": 8,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 9,
      "confidence": 0.2
    },
    {
      "mark": "SF-1",
      "count": 8,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 9,
      "confidence": 0.2
    },
    {
      "mark": "SF-1",
      "count": 8,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 9,
      "confidence": 0.2
    },
    {
      "mark": "SF-1",
      "count": 8,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 9,
      "confidence": 0.2
    },
    {
      "mark": "SF-1",
      "count": 8,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 9,
      "confidence": 0.2
    }
  ]
}
```

#### Page 18 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 6 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "6 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [
    {
      "mark": "DOOR-TYPE",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 18,
      "confidence": 0.2
    },
    {
      "mark": "DOOR-ALUM",
      "count": 0,
      "door_type": "aluminum_storefront",
      "frame_type": "aluminum_storefront",
      "manufacturer": null,
      "door_kind": "single",
      "material": "aluminum_storefront",
      "glass_door": true,
      "finish": null,
      "location": "",
      "width_ft": 3.0,
      "height_ft": 7.0,
      "source_page": 18,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-ALUM",
      "count": 0,
      "door_type": "aluminum_storefront",
      "frame_type": "aluminum_storefront",
      "manufacturer": null,
      "door_kind": "single",
      "material": "aluminum_storefront",
      "glass_door": true,
      "finish": null,
      "location": "",
      "width_ft": 3.0,
      "height_ft": 7.0,
      "source_page": 18,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-ALUM",
      "count": 0,
      "door_type": "aluminum_storefront",
      "frame_type": "aluminum_storefront",
      "manufacturer": null,
      "door_kind": "single",
      "material": "aluminum_storefront",
      "glass_door": true,
      "finish": null,
      "location": "",
      "width_ft": 3.0,
      "height_ft": 7.0,
      "source_page": 18,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-TYPE",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": null,
      "door_kind": "single",
      "material": "HM",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": 3.0,
      "height_ft": 7.0,
      "source_page": 18,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-HEAD",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 18,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 31 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 6 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "6 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "101",
      "count": 0,
      "system": "curtain_wall_captured",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 55.0,
      "height_ft": 25.0,
      "sqft": 1375.0,
      "location": "",
      "source_page": 31,
      "confidence": 0.4
    },
    {
      "mark": "DR-C",
      "count": 0,
      "system": "door_hollow_metal_single",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
      "width_ft": 6.0,
      "height_ft": 1.6667,
      "sqft": 10.0002,
      "location": "",
      "source_page": 31,
      "confidence": 0.4
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 31,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 31,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 31,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 31,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 32 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 6 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "6 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 32,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 32,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 32,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 32,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 32,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 32,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 37 (sheet `A-201`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "D-E",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 37,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 41 (sheet `A-303`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 0 door / 1 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 5 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-1",
      "count": 5,
      "system_type": "storefront_captured",
      "manufacturer": "YKK AP",
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": "Dark Bronze",
      "width_ft": null,
      "height_ft": null,
      "source_page": 41,
      "confidence": 0.7
    }
  ]
}
```

#### Page 42 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 0 door / 4 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "4 schedule rows parsed; 3 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-1",
      "count": 3,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 42,
      "confidence": 0.3
    },
    {
      "mark": "SF-1",
      "count": 3,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 42,
      "confidence": 0.3
    },
    {
      "mark": "SF-1",
      "count": 3,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 42,
      "confidence": 0.3
    },
    {
      "mark": "SF-1",
      "count": 3,
      "system_type": "storefront_captured",
      "manufacturer": "YKK AP",
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": "Dark Bronze",
      "width_ft": null,
      "height_ft": null,
      "source_page": 42,
      "confidence": 0.7
    }
  ]
}
```

#### Page 52 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 6 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "6 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [
    {
      "mark": "DOOR-B",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": null,
      "door_kind": "single",
      "material": "HM",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 52,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-B",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": null,
      "door_kind": "single",
      "material": "HM",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 52,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-B",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": null,
      "door_kind": "single",
      "material": "HM",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 52,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-B",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": null,
      "door_kind": "single",
      "material": "HM",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 52,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-B",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": null,
      "door_kind": "single",
      "material": "HM",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 52,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-HEAD",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 52,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 64 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 8 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "8 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "101",
      "count": 0,
      "system": "curtain_wall_captured",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 55.0,
      "height_ft": 25.0,
      "sqft": 1375.0,
      "location": "",
      "source_page": 64,
      "confidence": 0.4
    },
    {
      "mark": "D-4",
      "count": 0,
      "system": "door_hollow_metal_single",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
      "width_ft": 4.0,
      "height_ft": 6.0,
      "sqft": 24.0,
      "location": "",
      "source_page": 64,
      "confidence": 0.4
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 64,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 64,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 64,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 64,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 64,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 64,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 65 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 6 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "6 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 65,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 65,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 65,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 65,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 65,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 65,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 69 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 69,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 70 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 1 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "2 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "D-8",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 15.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 70,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "100",
      "count": 0,
      "system_type": "storefront_captured",
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 70,
      "confidence": 0.4
    }
  ]
}
```

#### Page 73 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 73,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 74 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 0 door / 5 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "5 schedule rows parsed; 5 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-1",
      "count": 5,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 74,
      "confidence": 0.2
    },
    {
      "mark": "SF-1",
      "count": 5,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 74,
      "confidence": 0.2
    },
    {
      "mark": "SF-1",
      "count": 5,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 74,
      "confidence": 0.2
    },
    {
      "mark": "SF-1",
      "count": 5,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 74,
      "confidence": 0.2
    },
    {
      "mark": "SF-1",
      "count": 5,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 74,
      "confidence": 0.2
    }
  ]
}
```

#### Page 75 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 0 door / 3 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "3 schedule rows parsed; 3 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-1",
      "count": 3,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 75,
      "confidence": 0.3
    },
    {
      "mark": "SF-1",
      "count": 3,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 75,
      "confidence": 0.3
    },
    {
      "mark": "SF-1",
      "count": 3,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 75,
      "confidence": 0.3
    }
  ]
}
```

#### Page 85 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 6 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "6 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [
    {
      "mark": "DOOR-B",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": null,
      "door_kind": "single",
      "material": "HM",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 85,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-B",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": null,
      "door_kind": "single",
      "material": "HM",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 85,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-B",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": null,
      "door_kind": "single",
      "material": "HM",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 85,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-B",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": null,
      "door_kind": "single",
      "material": "HM",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 85,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-B",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": null,
      "door_kind": "single",
      "material": "HM",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 85,
      "confidence": 0.5
    },
    {
      "mark": "DOOR-HEAD",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 85,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

## §5 — Debug Module Output

### Section 1 — dispatch_health

```json
{
  "dispatch_complete": true,
  "filters_completed": [
    "filter_1",
    "filter_2",
    "filter_4",
    "filter_3",
    "filter_5"
  ],
  "filter_count": 5,
  "warnings": [
    "Filter 4 quality gate: 2 of 3 legends removed (1 kept)"
  ],
  "warning_count": 1,
  "timestamp": "2026-04-29T02:52:20.878050+00:00",
  "total_pages": 97,
  "sheet_map_source": "drawing_index",
  "sheet_count": 30,
  "mapped_pages": 19
}
```

### Section 2 — scale_comparison (STUB)
- stub_marker confirmed: `True`

```json
{
  "stub_marker": "C.5_partial_port_pending_scale_engine_route",
  "reason": "Scale comparison requires the scale-engine output route; deferred to Phase D/E per DEBUG_MODULE_REPORT.md."
}
```

### Section 3 — page_intelligence
- Page entry count: 97

```json
[
  {
    "page": 0,
    "sheet": "LS-101",
    "title": "LIFE SAFETY PLAN",
    "discipline": "L",
    "type": "roof_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 1,
    "sheet": "A-601",
    "title": "DOOR TYPES, SCHEDULES, AND DETAILS",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 1
  },
  {
    "page": 2,
    "sheet": "G-003",
    "title": "WALL TYPES",
    "discipline": "G",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 3,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "ceiling_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 4,
    "sheet": "A-402",
    "title": "DUMPSTER ENCLOSURE PLANS AND DETAILS",
    "discipline": "A",
    "type": "general_notes",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 5,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "roof_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 6,
    "sheet": "A-102",
    "title": "DIMENSIONED BUILDING PLAN",
    "discipline": "A",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 7,
    "sheet": "A-111",
    "title": "REFLECTED CEILING PLAN",
    "discipline": "A",
    "type": "ceiling_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 8,
    "sheet": "A-101",
    "title": "OVERALL BUILDING PLAN",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 3
  },
  {
    "page": 9,
    "sheet": "A-306",
    "title": "BUILDING SECTIONS AND ROOF ACCESS LADDER DETAILS",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 10,
    "sheet": "A-301",
    "title": "WALL SECTIONS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 10,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 11,
    "sheet": "A-302",
    "title": "WALL SECTIONS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 8,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 12,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 6,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 13,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 8,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 14,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 15,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 8,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 16,
    "sheet": "A-401",
    "title": "PLAN DETAILS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 17,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 6,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 18,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 19,
    "sheet": "A-602",
    "title": "WINDOW TYPES",
    "discipline": "A",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 20,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 21,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 22,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 23,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 24,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 25,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 26,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 27,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 28,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 29,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 30,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 31,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "roof_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 32,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 33,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 34,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 35,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 36,
    "sheet": "A-100",
    "title": "ARCHITECTURAL SITE PLAN",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 37,
    "sheet": "A-201",
    "title": "EXTERIOR ELEVATIONS",
    "discipline": "A",
    "type": "floor_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 38,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 39,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "ceiling_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 40,
    "sheet": "A-121",
    "title": "ROOF PLAN",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 41,
    "sheet": "A-303",
    "title": "WALL SECTIONS",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 42,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 43,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 44,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 45,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 46,
    "sheet": "A-304",
    "title": "WALL SECTIONS",
    "discipline": "A",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 47,
    "sheet": "A-305",
    "title": "WALL SECTIONS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 48,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 49,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 9,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 50,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 7,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 51,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 52,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 53,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 54,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 55,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 56,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 57,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 58,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 59,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 60,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 61,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 62,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 63,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 64,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "roof_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 65,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 66,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 67,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 68,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 69,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 70,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 71,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 72,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "ceiling_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 73,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 74,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 75,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 76,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 77,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 78,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 79,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 80,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 81,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 82,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 9,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 83,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 6,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 84,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 85,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 4,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 86,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 87,
    "sheet": "S-401",
    "title": "FRAMING DETAILS",
    "discipline": "S",
    "type": "framing_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 88,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 89,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 90,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": true,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 1,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 91,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 92,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 93,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 94,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 95,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 96,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
    "has_drawing": false,
    "has_title_block": false,
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 0,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  }
]
```

### Section 4 — cross_reference_graph (STUB)
- stub_marker confirmed: `True`

```json
{
  "stub_marker": "C.5_partial_port_pending_networkx_and_sheet_index",
  "reason": "Cross-reference graph requires networkx + sheet-index parsing; deferred per DEBUG_MODULE_REPORT.md."
}
```

### Section 5 — geometry_diagnostics (STUB)
- stub_marker confirmed: `True`

```json
{
  "stub_marker": "C.5_partial_port_pending_geometry_results",
  "reason": "Geometry diagnostics requires geometry_results from Stages 6-9; deferred per DEBUG_MODULE_REPORT.md."
}
```

### Section 6 — legend_and_quality_flags
- Legend count: 1
- Quality flag count: 0

#### Quality flags raised

```json
[]
```

#### Legend contents (sample, truncated)

```json
[
  {
    "type": "schedule",
    "title": "F-X \nFOOTINS REFERENCE, 5EE FOOTINS SCHEDULE FOR 51ZE AND REINFORCINS. \n(X'-X\") ",
    "page": 87,
    "entry_count": 8,
    "confidence": 0.7,
    "source": "legend: F-X \nFOOTINS REFERENCE, 5EE FOOTINS SCHE",
    "entries_sample": [
      {
        "key": "5",
        "desc": "PROVIDE #5 VERT. REINFORCING G 24\" O.C. IN ALL EXTERIOR MASONRY HALL5."
      },
      {
        "key": "4",
        "desc": "REFER TO SEOTECHNICAL REPORT FOR PROPER INSTALLATION OF 5U6SRADE MATERIALS."
      },
      {
        "key": "3",
        "desc": "1-0\" X :3'-0\""
      },
      {
        "key": "5",
        "desc": "#5 EAGH HAY"
      },
      {
        "key": "4",
        "desc": "\"5 EACH HAY"
      },
      {
        "key": "5",
        "desc": "\"5 EAC.H HAY"
      },
      {
        "key": "11",
        "desc": "X 16"
      },
      {
        "key": "4",
        "desc": "#5 VERTICAL"
      }
    ]
  }
]
```

## §6 — Per-Page Errors (if any)

- Pages where module raised: 0
- Pages with module attempt: 97
- Roofing per-page error rate: 0.00%
- Glazing per-page error rate: 0.00%

(no per-page errors)

## §7 — Closing

Observation only. No grades. No fixes proposed. No tuning
recommendations. The roofing module and glazing module are
vault-ruled per CLAUDE.md §3 Decision 15. The debug module is
vault-ruled per the same. Tuning is a future phase with `core/`
frozen. Section 2/4/5 stub markers confirmed above; sections 1/3/6
ran on real input.

Mechanical observations:

- Observed: roofing module produced 830 `fields` entries across 97 pages with non-empty output (of 97 pages attempted), with 0 warnings and 0 equipment_pins.
- Observed: glazing module produced 43 glazing_items, 22 door_items, 22 storefront_items across 22 pages with non-empty output (of 97 pages attempted).
- Observed: dispatch project_scope detected_system = `None` with confidence `0.0`; scope_pages = `[]`; manufacturers = `[]`.
- Observed: debug section 6 emitted 1 legend entries and 0 legend quality flags.
- Observed: per-page module error rate roofing=0.00%, glazing=0.00% (§7 stop threshold = 25%; soft-observation band = 5–25%).

---

**End of report.** Vault rule active on `roofing_module.py`,
`roofing_vocabulary.py`, `glazing_module.py`, `glazing_vocabulary.py`,
and `debug_module.py`. The sweep modified zero `backend/core/` files
and added zero dependencies. This report is a descriptive artifact
for the future tuning planning conversation per Daniel's directive
2026-04-28 (PROJECT_CLAUDE.md §3).
