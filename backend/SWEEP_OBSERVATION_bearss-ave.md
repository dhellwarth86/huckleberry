# Sweep Observation Report — Bearss Ave Distribution Center — University — Marcobay Construction (3)

**Date:** 2026-04-28
**Phase:** Three-bidset sweep (post-C.3c-build, post-C.5; modules vault-ruled)
**Bidset short name:** `bearss-ave`
**Bidset file:** `C:\huck stage 2\full bid sets\Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf`
**Page count:** 91
**File size:** 71,350,367 bytes (~68.0 MB)
**Wall-clock dispatch time:** 95.0s
**Wall-clock per-page module time (roofing+glazing combined):** 824.9s
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

- Display name: Bearss Ave Distribution Center — University — Marcobay Construction (3)
- Short name: `bearss-ave`
- Filename: `Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf`
- Full path: `C:\huck stage 2\full bid sets\Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf`
- Page count: 91
- File size: 71,350,367 bytes (68.0 MB)
- Prior characterization: Uncharacterized.

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
### dispatch_warnings: `['Filter 4 quality gate: 196 of 341 legends removed (145 kept)']`
### total_pages: `91`
### sheet_count: `47`
### mapped_pages: `44`
### sheet_map_source: `drawing_index`

## §3 — Roofing Module Output

### Aggregated

- Total `fields` entries across all pages: 769
- Total warnings: 0
- Total equipment_pins: 0
- Pages with non-empty output: 91
- Pages with empty output: 0

### Per-page summary (only pages with non-empty output shown)

| Page | Sheet | Fields | Warnings | Equip pins |
|---:|---|---:|---:|---:|
| 0 | A-001 | 9 | 0 | 0 |
| 1 | A-002 | 8 | 0 | 0 |
| 2 | A-003 | 8 | 0 | 0 |
| 3 | A-202 | 10 | 0 | 0 |
| 4 | A-402 | 9 | 0 | 0 |
| 5 | A-201 | 10 | 0 | 0 |
| 6 | --- | 10 | 0 | 0 |
| 7 | A-401 | 11 | 0 | 0 |
| 8 | --- | 9 | 0 | 0 |
| 9 | A-501 | 8 | 0 | 0 |
| 10 | A-601 | 8 | 0 | 0 |
| 11 | S-000 | 8 | 0 | 0 |
| 12 | S-100 | 8 | 0 | 0 |
| 13 | S-101 | 8 | 0 | 0 |
| 14 | S-102 | 8 | 0 | 0 |
| 15 | S-103 | 8 | 0 | 0 |
| 16 | S-200 | 8 | 0 | 0 |
| 17 | S-210 | 8 | 0 | 0 |
| 18 | S-300 | 9 | 0 | 0 |
| 19 | S-301 | 8 | 0 | 0 |
| 20 | S-310 | 8 | 0 | 0 |
| 21 | S-311 | 8 | 0 | 0 |
| 22 | S-312 | 8 | 0 | 0 |
| 23 | S-313 | 8 | 0 | 0 |
| 24 | --- | 8 | 0 | 0 |
| 25 | S-321 | 8 | 0 | 0 |
| 26 | S-322 | 8 | 0 | 0 |
| 27 | S-323 | 8 | 0 | 0 |
| 28 | S-400 | 8 | 0 | 0 |
| 29 | S-500 | 8 | 0 | 0 |
| 30 | S-501 | 8 | 0 | 0 |
| 31 | S-510 | 8 | 0 | 0 |
| 32 | S-520 | 9 | 0 | 0 |
| 33 | S-530 | 8 | 0 | 0 |
| 34 | M-001 | 9 | 0 | 0 |
| 35 | M-002 | 10 | 0 | 0 |
| 36 | M-100 | 8 | 0 | 0 |
| 37 | P-001 | 8 | 0 | 0 |
| 38 | P-002 | 10 | 0 | 0 |
| 39 | P-100 | 8 | 0 | 0 |
| 40 | E-001 | 10 | 0 | 0 |
| 41 | E-002 | 8 | 0 | 0 |
| 42 | E-101 | 8 | 0 | 0 |
| 43 | E-201 | 8 | 0 | 0 |
| 44 | E-301 | 8 | 0 | 0 |
| 45 | E-401 | 8 | 0 | 0 |
| 46 | --- | 9 | 0 | 0 |
| 47 | --- | 8 | 0 | 0 |
| 48 | --- | 8 | 0 | 0 |
| 49 | A-101 | 9 | 0 | 0 |
| 50 | --- | 9 | 0 | 0 |
| 51 | --- | 10 | 0 | 0 |
| 52 | --- | 10 | 0 | 0 |
| 53 | --- | 11 | 0 | 0 |
| 54 | --- | 9 | 0 | 0 |
| 55 | --- | 8 | 0 | 0 |
| 56 | --- | 8 | 0 | 0 |
| 57 | --- | 8 | 0 | 0 |
| 58 | --- | 8 | 0 | 0 |
| 59 | --- | 8 | 0 | 0 |
| 60 | --- | 8 | 0 | 0 |
| 61 | --- | 8 | 0 | 0 |
| 62 | --- | 8 | 0 | 0 |
| 63 | --- | 8 | 0 | 0 |
| 64 | --- | 9 | 0 | 0 |
| 65 | --- | 8 | 0 | 0 |
| 66 | --- | 8 | 0 | 0 |
| 67 | --- | 8 | 0 | 0 |
| 68 | --- | 8 | 0 | 0 |
| 69 | --- | 8 | 0 | 0 |
| 70 | --- | 8 | 0 | 0 |
| 71 | --- | 8 | 0 | 0 |
| 72 | --- | 8 | 0 | 0 |
| 73 | --- | 8 | 0 | 0 |
| 74 | --- | 8 | 0 | 0 |
| 75 | --- | 8 | 0 | 0 |
| 76 | --- | 8 | 0 | 0 |
| 77 | --- | 8 | 0 | 0 |
| 78 | --- | 9 | 0 | 0 |
| 79 | --- | 8 | 0 | 0 |
| 80 | --- | 9 | 0 | 0 |
| 81 | --- | 10 | 0 | 0 |
| 82 | --- | 8 | 0 | 0 |
| 83 | --- | 8 | 0 | 0 |
| 84 | --- | 10 | 0 | 0 |
| 85 | --- | 8 | 0 | 0 |
| 86 | --- | 10 | 0 | 0 |
| 87 | --- | 8 | 0 | 0 |
| 88 | --- | 8 | 0 | 0 |
| 89 | --- | 8 | 0 | 0 |
| 90 | --- | 8 | 0 | 0 |

### Per-page detail (only pages with non-empty output)

#### Page 0 (sheet `A-001`)

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

#### Page 1 (sheet `A-002`)

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

#### Page 2 (sheet `A-003`)

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

#### Page 3 (sheet `A-202`)

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
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Gutters",
      "unit": "LF"
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

#### Page 4 (sheet `A-402`)

```json
{
  "fields": {
    "ridge_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Ridge Cap",
      "unit": "LF"
    },
    "hip_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Hip Cap",
      "unit": "LF"
    },
    "valley": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Valley",
      "unit": "LF"
    },
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Gutters",
      "unit": "LF"
    },
    "downspout": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 no callouts found, enter manually",
      "display_name": "Downspouts",
      "unit": "EA"
    },
    "clips": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Panel Clips",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "trim": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Trim",
      "unit": "LF"
    },
    "_scope": {
      "value": "Standing Seam Metal",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'KYNAR'",
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

#### Page 5 (sheet `A-201`)

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
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Gutters",
      "unit": "LF"
    },
    "_scope": {
      "value": "TPO Single Ply",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'TREMCO'",
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

#### Page 6 (sheet `---`)

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
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Gutters",
      "unit": "LF"
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

#### Page 7 (sheet `A-401`)

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
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Gutters",
      "unit": "LF"
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

#### Page 8 (sheet `---`)

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
    "clips": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Panel Clips",
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

#### Page 9 (sheet `A-501`)

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

#### Page 10 (sheet `A-601`)

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

#### Page 11 (sheet `S-000`)

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

#### Page 12 (sheet `S-100`)

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

#### Page 13 (sheet `S-101`)

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

#### Page 14 (sheet `S-102`)

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

#### Page 15 (sheet `S-103`)

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

#### Page 16 (sheet `S-200`)

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

#### Page 17 (sheet `S-210`)

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

#### Page 18 (sheet `S-300`)

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

#### Page 19 (sheet `S-301`)

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

#### Page 20 (sheet `S-310`)

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

#### Page 21 (sheet `S-311`)

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

#### Page 22 (sheet `S-312`)

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

#### Page 23 (sheet `S-313`)

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

#### Page 25 (sheet `S-321`)

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

#### Page 26 (sheet `S-322`)

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

#### Page 27 (sheet `S-323`)

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

#### Page 28 (sheet `S-400`)

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

#### Page 29 (sheet `S-500`)

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

#### Page 30 (sheet `S-501`)

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

#### Page 31 (sheet `S-510`)

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

#### Page 32 (sheet `S-520`)

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

#### Page 33 (sheet `S-530`)

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

#### Page 34 (sheet `M-001`)

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

#### Page 35 (sheet `M-002`)

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
    "clips": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Panel Clips",
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

#### Page 36 (sheet `M-100`)

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

#### Page 37 (sheet `P-001`)

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

#### Page 38 (sheet `P-002`)

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
    "trim": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Trim",
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

#### Page 39 (sheet `P-100`)

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

#### Page 40 (sheet `E-001`)

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
    "trim": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Trim",
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

#### Page 41 (sheet `E-002`)

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

#### Page 42 (sheet `E-101`)

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

#### Page 43 (sheet `E-201`)

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

#### Page 44 (sheet `E-301`)

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

#### Page 45 (sheet `E-401`)

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

#### Page 46 (sheet `---`)

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

#### Page 47 (sheet `---`)

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

#### Page 49 (sheet `A-101`)

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

#### Page 50 (sheet `---`)

```json
{
  "fields": {
    "ridge_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Ridge Cap",
      "unit": "LF"
    },
    "hip_cap": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Hip Cap",
      "unit": "LF"
    },
    "valley": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Valley",
      "unit": "LF"
    },
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Gutters",
      "unit": "LF"
    },
    "downspout": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 no callouts found, enter manually",
      "display_name": "Downspouts",
      "unit": "EA"
    },
    "clips": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Panel Clips",
      "unit": "EA"
    },
    "flashing": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Flashing",
      "unit": "LF"
    },
    "trim": {
      "value": null,
      "confidence": 0.0,
      "source": "assembly_expected",
      "evidence": "expected for Standing Seam Metal \u2014 enter manually",
      "display_name": "Trim",
      "unit": "LF"
    },
    "_scope": {
      "value": "Standing Seam Metal",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'KYNAR'",
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
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Gutters",
      "unit": "LF"
    },
    "_scope": {
      "value": "TPO Single Ply",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'TREMCO'",
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
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Gutters",
      "unit": "LF"
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

#### Page 53 (sheet `---`)

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
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Gutters",
      "unit": "LF"
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
    "clips": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Panel Clips",
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

*(31 more non-empty roofing pages truncated for artifact size)*

## §4 — Glazing Module Output

### Aggregated

- Total glazing_items across all pages: 177
- Total door_items: 31
- Total storefront_items: 24
- Pages with any glazing module content (any of the three lists non-empty): 58
- Pages with empty output: 33

### Per-page summary (only pages with non-empty output shown)

| Page | Sheet | glazing_items | door_items | storefront_items |
|---:|---|---:|---:|---:|
| 0 | A-001 | 0 | 9 | 0 |
| 1 | A-002 | 1 | 0 | 2 |
| 3 | A-202 | 3 | 0 | 0 |
| 4 | A-402 | 1 | 0 | 0 |
| 5 | A-201 | 7 | 0 | 1 |
| 10 | A-601 | 0 | 5 | 0 |
| 12 | S-100 | 12 | 0 | 0 |
| 13 | S-101 | 9 | 0 | 0 |
| 14 | S-102 | 1 | 0 | 0 |
| 15 | S-103 | 2 | 0 | 4 |
| 16 | S-200 | 1 | 0 | 0 |
| 17 | S-210 | 6 | 0 | 0 |
| 18 | S-300 | 1 | 0 | 0 |
| 20 | S-310 | 1 | 0 | 0 |
| 21 | S-311 | 1 | 0 | 0 |
| 23 | S-313 | 1 | 0 | 0 |
| 28 | S-400 | 1 | 0 | 0 |
| 33 | S-530 | 2 | 0 | 0 |
| 34 | M-001 | 2 | 0 | 1 |
| 35 | M-002 | 4 | 0 | 2 |
| 36 | M-100 | 2 | 0 | 0 |
| 37 | P-001 | 11 | 0 | 0 |
| 38 | P-002 | 0 | 2 | 0 |
| 39 | P-100 | 2 | 0 | 0 |
| 40 | E-001 | 4 | 2 | 0 |
| 42 | E-101 | 2 | 0 | 0 |
| 44 | E-301 | 1 | 0 | 0 |
| 45 | E-401 | 8 | 0 | 0 |
| 46 | --- | 0 | 7 | 0 |
| 47 | --- | 1 | 0 | 2 |
| 48 | --- | 0 | 0 | 1 |
| 49 | A-101 | 1 | 0 | 1 |
| 50 | --- | 1 | 0 | 1 |
| 51 | --- | 7 | 0 | 1 |
| 56 | --- | 0 | 2 | 0 |
| 58 | --- | 11 | 0 | 0 |
| 59 | --- | 10 | 0 | 1 |
| 60 | --- | 3 | 0 | 0 |
| 61 | --- | 2 | 0 | 4 |
| 62 | --- | 1 | 0 | 0 |
| 63 | --- | 8 | 0 | 0 |
| 64 | --- | 1 | 0 | 0 |
| 66 | --- | 1 | 0 | 0 |
| 67 | --- | 1 | 0 | 0 |
| 68 | --- | 1 | 0 | 0 |
| 69 | --- | 1 | 0 | 0 |
| 74 | --- | 1 | 0 | 0 |
| 79 | --- | 1 | 0 | 0 |
| 80 | --- | 2 | 0 | 1 |
| 81 | --- | 4 | 0 | 2 |
| 82 | --- | 2 | 0 | 0 |
| 83 | --- | 11 | 0 | 0 |
| 84 | --- | 0 | 2 | 0 |
| 85 | --- | 4 | 0 | 0 |
| 86 | --- | 4 | 2 | 0 |
| 88 | --- | 3 | 0 | 0 |
| 89 | --- | 1 | 0 | 0 |
| 90 | --- | 8 | 0 | 0 |

### Per-page detail (only pages with non-empty output)

#### Page 0 (sheet `A-001`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 9 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "9 schedule rows parsed; 0 elevation marks counted",
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
      "width_ft": null,
      "height_ft": null,
      "source_page": 0,
      "confidence": 0.2
    },
    {
      "mark": "121",
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
      "mark": "102",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": "Clear",
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 0,
      "confidence": 0.2
    },
    {
      "mark": "103",
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
    }
  ],
  "storefront_items": []
}
```

#### Page 1 (sheet `A-002`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 2 storefront items",
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
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-500",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 1,
      "confidence": 0.3
    },
    {
      "mark": "143",
      "count": 0,
      "system_type": "window_aluminum_fixed",
      "manufacturer": null,
      "sqft_per_segment": 7932.9773,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": 55.25,
      "height_ft": 143.5833,
      "source_page": 1,
      "confidence": 0.4
    }
  ]
}
```

#### Page 3 (sheet `A-202`)

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
      "source_page": 3,
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
      "source_page": 3,
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
      "source_page": 3,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 4 (sheet `A-402`)

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
      "source_page": 4,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 5 (sheet `A-201`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 7 window / 0 door / 1 storefront items",
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
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "Painted",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 5,
      "confidence": 0.2
    },
    {
      "mark": "102",
      "count": 0,
      "system": "window_hollow_metal",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "Painted",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 5,
      "confidence": 0.4
    },
    {
      "mark": "107",
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
    },
    {
      "mark": "108",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "Painted",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 5,
      "confidence": 0.2
    },
    {
      "mark": "109",
      "count": 0,
      "system": "window_hollow_metal",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "Painted",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 5,
      "confidence": 0.4
    },
    {
      "mark": "110",
      "count": 0,
      "system": "window_hollow_metal",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "Clear Anodized",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 5,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "105",
      "count": 0,
      "system_type": "storefront_captured",
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": "Clear Anodized",
      "width_ft": null,
      "height_ft": null,
      "source_page": 5,
      "confidence": 0.4
    }
  ]
}
```

#### Page 10 (sheet `A-601`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 5 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "5 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [
    {
      "mark": "DOOR-DOCK",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": "Schlage",
      "door_kind": "pair",
      "material": "HM",
      "glass_door": true,
      "finish": "Painted",
      "location": "",
      "width_ft": 6.0,
      "height_ft": 7.0,
      "source_page": 10,
      "confidence": 0.7
    },
    {
      "mark": "152",
      "count": 0,
      "door_type": "aluminum_storefront",
      "frame_type": "aluminum_storefront",
      "manufacturer": null,
      "door_kind": "single",
      "material": "aluminum_storefront",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": 16.0,
      "height_ft": 9.5,
      "source_page": 10,
      "confidence": 0.5
    },
    {
      "mark": "152",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": 16.0,
      "height_ft": 9.5,
      "source_page": 10,
      "confidence": 0.2
    },
    {
      "mark": "152",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": 16.0,
      "height_ft": 9.5,
      "source_page": 10,
      "confidence": 0.2
    },
    {
      "mark": "114",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": 12.0,
      "height_ft": 9.5,
      "source_page": 10,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 12 (sheet `S-100`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 12 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "12 schedule rows parsed; 0 elevation marks counted",
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
      "source_page": 12,
      "confidence": 0.2
    },
    {
      "mark": "138",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 12,
      "confidence": 0.2
    },
    {
      "mark": "177",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 12,
      "confidence": 0.2
    },
    {
      "mark": "113",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 12,
      "confidence": 0.2
    },
    {
      "mark": "106",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 12,
      "confidence": 0.2
    },
    {
      "mark": "150",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 12,
      "confidence": 0.2
    },
    {
      "mark": "150",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 12,
      "confidence": 0.2
    },
    {
      "mark": "150",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 12,
      "confidence": 0.2
    },
    {
      "mark": "110",
      "count": 0,
      "system": "window_hollow_metal",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 12,
      "confidence": 0.4
    },
    {
      "mark": "150",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 12,
      "confidence": 0.4
    },
    {
      "mark": "157",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 12,
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
      "source_page": 12,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 13 (sheet `S-101`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 9 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "9 schedule rows parsed; 0 elevation marks counted",
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
      "source_page": 13,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 50.0,
      "sqft": 1000.0,
      "location": "",
      "source_page": 13,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 50.0,
      "sqft": 1000.0,
      "location": "",
      "source_page": 13,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 50.0,
      "sqft": 1000.0,
      "location": "",
      "source_page": 13,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 50.0,
      "sqft": 1000.0,
      "location": "",
      "source_page": 13,
      "confidence": 0.2
    },
    {
      "mark": "103",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 13,
      "confidence": 0.2
    },
    {
      "mark": "141",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 13,
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
      "source_page": 13,
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
      "source_page": 13,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 14 (sheet `S-102`)

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
      "source_page": 14,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 15 (sheet `S-103`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 2 window / 0 door / 4 storefront items",
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
      "source_page": 15,
      "confidence": 0.2
    },
    {
      "mark": "103",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 15,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-OF",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 15,
      "confidence": 0.3
    },
    {
      "mark": "SF-OF",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 15,
      "confidence": 0.3
    },
    {
      "mark": "SF-OF",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 15,
      "confidence": 0.3
    },
    {
      "mark": "SF-OF",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 15,
      "confidence": 0.3
    }
  ]
}
```

#### Page 16 (sheet `S-200`)

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
      "mark": "D-6",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 2.0,
      "height_ft": 1.0,
      "sqft": 2.0,
      "location": "",
      "source_page": 16,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 17 (sheet `S-210`)

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
      "mark": "123",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 17,
      "confidence": 0.2
    },
    {
      "mark": "117",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 17,
      "confidence": 0.2
    },
    {
      "mark": "123",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 17,
      "confidence": 0.2
    },
    {
      "mark": "117",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 17,
      "confidence": 0.2
    },
    {
      "mark": "123",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 17,
      "confidence": 0.2
    },
    {
      "mark": "117",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 17,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 18 (sheet `S-300`)

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
      "mark": "117",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 18,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 20 (sheet `S-310`)

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
      "mark": "101",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 20,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 21 (sheet `S-311`)

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
      "mark": "101",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 21,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 23 (sheet `S-313`)

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
      "mark": "101",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 23,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 28 (sheet `S-400`)

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
      "mark": "D-GC",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 28,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 33 (sheet `S-530`)

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
      "mark": "D-TO",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 33,
      "confidence": 0.2
    },
    {
      "mark": "W-F",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 33,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 34 (sheet `M-001`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 2 window / 0 door / 1 storefront items",
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
      "mark": "D-PIPE",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 34,
      "confidence": 0.2
    },
    {
      "mark": "D-PIPE",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 34,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "D-AND",
      "count": 0,
      "system_type": "door_hollow_metal_single",
      "manufacturer": null,
      "sqft_per_segment": 120.0,
      "door_in_segment": true,
      "double_door_in_segment": true,
      "location": "",
      "finish": "Black",
      "width_ft": 8.0,
      "height_ft": 15.0,
      "source_page": 34,
      "confidence": 0.4
    }
  ]
}
```

#### Page 35 (sheet `M-002`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 4 window / 0 door / 2 storefront items",
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
      "source_page": 35,
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
      "source_page": 35,
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
      "source_page": 35,
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
      "source_page": 35,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-300",
      "count": 0,
      "system_type": "door_hollow_metal_single",
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": 5.0,
      "height_ft": null,
      "source_page": 35,
      "confidence": 0.4
    },
    {
      "mark": "SF-300",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 35,
      "confidence": 0.3
    }
  ]
}
```

#### Page 36 (sheet `M-100`)

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
      "mark": "100",
      "count": 0,
      "system": "curtain_wall_captured",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 1.0,
      "sqft": 20.0,
      "location": "",
      "source_page": 36,
      "confidence": 0.4
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
      "source_page": 36,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 37 (sheet `P-001`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 11 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "11 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "D-S",
      "count": 0,
      "system": "curtain_wall_ssg_two_side",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 25.0,
      "height_ft": 50.0,
      "sqft": 1250.0,
      "location": "",
      "source_page": 37,
      "confidence": 0.4
    },
    {
      "mark": "W-PIPE",
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
      "source_page": 37,
      "confidence": 0.2
    },
    {
      "mark": "D-E",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 25.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 37,
      "confidence": 0.2
    },
    {
      "mark": "D-E",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 50.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 37,
      "confidence": 0.2
    },
    {
      "mark": "D-61",
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
    },
    {
      "mark": "D-AE",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 75.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 37,
      "confidence": 0.2
    },
    {
      "mark": "D-E",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 100.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 37,
      "confidence": 0.2
    },
    {
      "mark": "D-F",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 125.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 37,
      "confidence": 0.2
    },
    {
      "mark": "D-E",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 150.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 37,
      "confidence": 0.2
    },
    {
      "mark": "150",
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

#### Page 38 (sheet `P-002`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 2 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "2 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [
    {
      "mark": "DOOR-AND",
      "count": 0,
      "door_type": "wood",
      "frame_type": "wood",
      "manufacturer": null,
      "door_kind": "single",
      "material": "wood",
      "glass_door": false,
      "finish": "Painted",
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 38,
      "confidence": 0.5
    },
    {
      "mark": "D-WV",
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
      "source_page": 38,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 39 (sheet `P-100`)

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
      "mark": "W-4",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 1.0,
      "height_ft": 1.0,
      "sqft": 1.0,
      "location": "",
      "source_page": 39,
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
      "source_page": 39,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 40 (sheet `E-001`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 4 window / 2 door / 0 storefront items",
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
      "mark": "125",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 40,
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
      "source_page": 40,
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
      "source_page": 40,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": "curtain_wall_captured",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 40,
      "confidence": 0.4
    }
  ],
  "door_items": [
    {
      "mark": "DOOR-WITH",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": "Black",
      "location": "",
      "width_ft": 60.0,
      "height_ft": null,
      "source_page": 40,
      "confidence": 0.2
    },
    {
      "mark": "DOOR-WITH",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": "Black",
      "location": "",
      "width_ft": 60.0,
      "height_ft": null,
      "source_page": 40,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 42 (sheet `E-101`)

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
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 1.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 42,
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
      "source_page": 42,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 44 (sheet `E-301`)

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
      "mark": "D-L1A",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 1.0,
      "sqft": 20.0,
      "location": "",
      "source_page": 44,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 45 (sheet `E-401`)

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
      "mark": "102",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 10.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 45,
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
      "source_page": 45,
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
      "source_page": 45,
      "confidence": 0.2
    },
    {
      "mark": "125",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 45,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 45,
      "confidence": 0.4
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
      "source_page": 45,
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
      "source_page": 45,
      "confidence": 0.2
    },
    {
      "mark": "125",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 45,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 46 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 7 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "7 schedule rows parsed; 0 elevation marks counted",
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
      "width_ft": null,
      "height_ft": null,
      "source_page": 46,
      "confidence": 0.2
    },
    {
      "mark": "121",
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
      "source_page": 46,
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
      "source_page": 46,
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
      "source_page": 46,
      "confidence": 0.2
    },
    {
      "mark": "102",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": "Clear",
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 46,
      "confidence": 0.2
    },
    {
      "mark": "103",
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
      "source_page": 46,
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
      "source_page": 46,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 47 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 2 storefront items",
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
      "source_page": 47,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-500",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 47,
      "confidence": 0.3
    },
    {
      "mark": "143",
      "count": 0,
      "system_type": "window_aluminum_fixed",
      "manufacturer": null,
      "sqft_per_segment": 9667.9374,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": 67.3333,
      "height_ft": 143.5833,
      "source_page": 47,
      "confidence": 0.4
    }
  ]
}
```

#### Page 48 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 0 door / 1 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 0 elevation marks counted",
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
      "mark": "SF-14",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 48,
      "confidence": 0.3
    }
  ]
}
```

#### Page 49 (sheet `A-101`)

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
      "source_page": 49,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "121",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 49,
      "confidence": 0.3
    }
  ]
}
```

#### Page 50 (sheet `---`)

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
      "source_page": 50,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "101",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 50,
      "confidence": 0.3
    }
  ]
}
```

#### Page 51 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 7 window / 0 door / 1 storefront items",
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
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 10.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 51,
      "confidence": 0.2
    },
    {
      "mark": "102",
      "count": 0,
      "system": "window_hollow_metal",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "Painted",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 51,
      "confidence": 0.4
    },
    {
      "mark": "105",
      "count": 0,
      "system": "window_hollow_metal",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 51,
      "confidence": 0.4
    },
    {
      "mark": "106",
      "count": 0,
      "system": "window_aluminum_fixed",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 51,
      "confidence": 0.4
    },
    {
      "mark": "108",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "Painted",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 51,
      "confidence": 0.2
    },
    {
      "mark": "109",
      "count": 0,
      "system": "window_hollow_metal",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "Painted",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 51,
      "confidence": 0.4
    },
    {
      "mark": "110",
      "count": 0,
      "system": "window_hollow_metal",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "Clear Anodized",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 51,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "107",
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
      "source_page": 51,
      "confidence": 0.4
    }
  ]
}
```

#### Page 56 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 2 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "2 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [
    {
      "mark": "DOOR-DOCK",
      "count": 0,
      "door_type": "HM",
      "frame_type": "HM",
      "manufacturer": "Schlage",
      "door_kind": "pair",
      "material": "HM",
      "glass_door": true,
      "finish": "Painted",
      "location": "",
      "width_ft": 6.0,
      "height_ft": 7.0,
      "source_page": 56,
      "confidence": 0.7
    },
    {
      "mark": "152",
      "count": 0,
      "door_type": "aluminum_storefront",
      "frame_type": "aluminum_storefront",
      "manufacturer": null,
      "door_kind": "single",
      "material": "aluminum_storefront",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": 16.0,
      "height_ft": 9.5,
      "source_page": 56,
      "confidence": 0.5
    }
  ],
  "storefront_items": []
}
```

#### Page 58 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 11 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "11 schedule rows parsed; 0 elevation marks counted",
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
      "source_page": 58,
      "confidence": 0.2
    },
    {
      "mark": "138",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 58,
      "confidence": 0.2
    },
    {
      "mark": "177",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 58,
      "confidence": 0.2
    },
    {
      "mark": "113",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 58,
      "confidence": 0.2
    },
    {
      "mark": "106",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 58,
      "confidence": 0.2
    },
    {
      "mark": "150",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 58,
      "confidence": 0.2
    },
    {
      "mark": "150",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 58,
      "confidence": 0.2
    },
    {
      "mark": "150",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 58,
      "confidence": 0.2
    },
    {
      "mark": "110",
      "count": 0,
      "system": "window_hollow_metal",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 58,
      "confidence": 0.4
    },
    {
      "mark": "157",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 58,
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
      "source_page": 58,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 59 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 10 window / 0 door / 1 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "11 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "D-3",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 59,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 50.0,
      "sqft": 1000.0,
      "location": "",
      "source_page": 59,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 50.0,
      "sqft": 1000.0,
      "location": "",
      "source_page": 59,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 50.0,
      "sqft": 1000.0,
      "location": "",
      "source_page": 59,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 50.0,
      "sqft": 1000.0,
      "location": "",
      "source_page": 59,
      "confidence": 0.2
    },
    {
      "mark": "103",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 59,
      "confidence": 0.2
    },
    {
      "mark": "103",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 59,
      "confidence": 0.2
    },
    {
      "mark": "141",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 59,
      "confidence": 0.2
    },
    {
      "mark": "141",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 59,
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
      "source_page": 59,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-H",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 59,
      "confidence": 0.3
    }
  ]
}
```

#### Page 60 (sheet `---`)

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
      "source_page": 60,
      "confidence": 0.2
    },
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
      "source_page": 60,
      "confidence": 0.2
    },
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
      "source_page": 60,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 61 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 2 window / 0 door / 4 storefront items",
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
      "source_page": 61,
      "confidence": 0.2
    },
    {
      "mark": "103",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 61,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-OF",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 61,
      "confidence": 0.3
    },
    {
      "mark": "SF-OF",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 61,
      "confidence": 0.3
    },
    {
      "mark": "SF-OF",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 61,
      "confidence": 0.3
    },
    {
      "mark": "SF-OF",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 61,
      "confidence": 0.3
    }
  ]
}
```

#### Page 62 (sheet `---`)

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
      "mark": "W-IDTH",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 62,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 63 (sheet `---`)

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
      "mark": "122",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 63,
      "confidence": 0.2
    },
    {
      "mark": "115",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 63,
      "confidence": 0.2
    },
    {
      "mark": "114",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 10.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 63,
      "confidence": 0.2
    },
    {
      "mark": "114",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 63,
      "confidence": 0.2
    },
    {
      "mark": "108",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 63,
      "confidence": 0.2
    },
    {
      "mark": "114",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 63,
      "confidence": 0.2
    },
    {
      "mark": "114",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 63,
      "confidence": 0.2
    },
    {
      "mark": "108",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 63,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 64 (sheet `---`)

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
      "mark": "117",
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

#### Page 66 (sheet `---`)

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
      "mark": "101",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 66,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 67 (sheet `---`)

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
      "mark": "101",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 67,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 68 (sheet `---`)

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
      "source_page": 68,
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
      "mark": "101",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 69,
      "confidence": 0.4
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
      "mark": "D-GC",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 74,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 79 (sheet `---`)

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
      "mark": "D-TO",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 79,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 80 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 2 window / 0 door / 1 storefront items",
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
      "mark": "D-PIPE",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 80,
      "confidence": 0.2
    },
    {
      "mark": "D-PIPE",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 80,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "D-AND",
      "count": 0,
      "system_type": "door_hollow_metal_single",
      "manufacturer": null,
      "sqft_per_segment": 120.0,
      "door_in_segment": true,
      "double_door_in_segment": true,
      "location": "",
      "finish": "Black",
      "width_ft": 8.0,
      "height_ft": 15.0,
      "source_page": 80,
      "confidence": 0.4
    }
  ]
}
```

#### Page 81 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 4 window / 0 door / 2 storefront items",
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
      "mark": "115",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 81,
      "confidence": 0.2
    },
    {
      "mark": "115",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 81,
      "confidence": 0.2
    },
    {
      "mark": "115",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 81,
      "confidence": 0.2
    },
    {
      "mark": "115",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 81,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-300",
      "count": 0,
      "system_type": "door_hollow_metal_single",
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": 5.0,
      "height_ft": null,
      "source_page": 81,
      "confidence": 0.4
    },
    {
      "mark": "SF-300",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": null,
      "height_ft": null,
      "source_page": 81,
      "confidence": 0.3
    }
  ]
}
```

#### Page 82 (sheet `---`)

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
      "mark": "108",
      "count": 0,
      "system": "curtain_wall_captured",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 1.0,
      "sqft": 20.0,
      "location": "",
      "source_page": 82,
      "confidence": 0.4
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
      "source_page": 82,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 83 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 11 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "11 schedule rows parsed; 0 elevation marks counted",
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
      "system": "curtain_wall_ssg_two_side",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 25.0,
      "height_ft": 50.0,
      "sqft": 1250.0,
      "location": "",
      "source_page": 83,
      "confidence": 0.4
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
      "source_page": 83,
      "confidence": 0.2
    },
    {
      "mark": "D-E",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 25.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 83,
      "confidence": 0.2
    },
    {
      "mark": "D-E",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 50.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 83,
      "confidence": 0.2
    },
    {
      "mark": "D-61",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 83,
      "confidence": 0.2
    },
    {
      "mark": "D-AE",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 75.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 83,
      "confidence": 0.2
    },
    {
      "mark": "D-E",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 100.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 83,
      "confidence": 0.2
    },
    {
      "mark": "D-F",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 125.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 83,
      "confidence": 0.2
    },
    {
      "mark": "155",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 83,
      "confidence": 0.2
    },
    {
      "mark": "D-E",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 150.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 83,
      "confidence": 0.2
    },
    {
      "mark": "150",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 83,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 84 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 2 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "2 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [
    {
      "mark": "DOOR-AND",
      "count": 0,
      "door_type": "wood",
      "frame_type": "wood",
      "manufacturer": null,
      "door_kind": "single",
      "material": "wood",
      "glass_door": false,
      "finish": "Painted",
      "location": "",
      "width_ft": null,
      "height_ft": null,
      "source_page": 84,
      "confidence": 0.5
    },
    {
      "mark": "D-WV",
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
      "source_page": 84,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 85 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 4 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "4 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "W-4",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 1.0,
      "height_ft": 1.0,
      "sqft": 1.0,
      "location": "",
      "source_page": 85,
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
      "source_page": 85,
      "confidence": 0.2
    },
    {
      "mark": "W-4",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 85,
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
      "source_page": 85,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 86 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 4 window / 2 door / 0 storefront items",
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
      "mark": "125",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 86,
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
      "source_page": 86,
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
      "source_page": 86,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": "curtain_wall_captured",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 86,
      "confidence": 0.4
    }
  ],
  "door_items": [
    {
      "mark": "DOOR-WITH",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": "Black",
      "location": "",
      "width_ft": 60.0,
      "height_ft": null,
      "source_page": 86,
      "confidence": 0.2
    },
    {
      "mark": "DOOR-WITH",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": "Black",
      "location": "",
      "width_ft": 60.0,
      "height_ft": null,
      "source_page": 86,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 88 (sheet `---`)

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
      "mark": "101",
      "count": 0,
      "system": "door_overhead_coiling",
      "glass_type": "glass_wired",
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 5.0,
      "sqft": 100.0,
      "location": "",
      "source_page": 88,
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
      "source_page": 88,
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
      "source_page": 88,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 89 (sheet `---`)

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
      "mark": "D-FIRE",
      "count": 0,
      "system": "door_overhead_coiling",
      "glass_type": "glass_wired",
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 20.0,
      "height_ft": 1.0,
      "sqft": 20.0,
      "location": "",
      "source_page": 89,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 90 (sheet `---`)

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
      "mark": "102",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 10.0,
      "height_ft": 1.0,
      "sqft": 10.0,
      "location": "",
      "source_page": 90,
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
      "source_page": 90,
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
      "source_page": 90,
      "confidence": 0.2
    },
    {
      "mark": "125",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 90,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 90,
      "confidence": 0.4
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
      "source_page": 90,
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
      "source_page": 90,
      "confidence": 0.2
    },
    {
      "mark": "125",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 90,
      "confidence": 0.2
    }
  ],
  "door_items": [],
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
    "Filter 4 quality gate: 196 of 341 legends removed (145 kept)"
  ],
  "warning_count": 1,
  "timestamp": "2026-04-29T03:39:55.911178+00:00",
  "total_pages": 91,
  "sheet_map_source": "drawing_index",
  "sheet_count": 47,
  "mapped_pages": 44
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
- Page entry count: 91

```json
[
  {
    "page": 0,
    "sheet": "A-001",
    "title": "COVER SHEET  SHEET NUMBER: A-001  PROJECT NAME: BEARSS AVENUE DISTRIBUTION CENTER - BUILDING 1",
    "discipline": "A",
    "type": "cover",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 8
  },
  {
    "page": 1,
    "sheet": "A-002",
    "title": "CODE & LIFE SAFETY",
    "discipline": "A",
    "type": "life_safety",
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
    "page": 2,
    "sheet": "A-003",
    "title": "ARCHITECTURAL SITE PLAN",
    "discipline": "A",
    "type": "site_plan",
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
    "page": 3,
    "sheet": "A-202",
    "title": "PANEL ELEVATIONS, WALL SECTIONS, & DETAILS",
    "discipline": "A",
    "type": "roof_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 7,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 9,
    "refs_in": 24
  },
  {
    "page": 4,
    "sheet": "A-402",
    "title": "MISC. DETAILS",
    "discipline": "A",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 6,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 8,
    "refs_in": 12
  },
  {
    "page": 5,
    "sheet": "A-201",
    "title": "EXTERIOR ELEVATIONS",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 2,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 6,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
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
    "page": 7,
    "sheet": "A-401",
    "title": "ROOF MISC. DETAILS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 15
  },
  {
    "page": 8,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 8,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 8,
    "refs_in": 0
  },
  {
    "page": 9,
    "sheet": "A-501",
    "title": "UL DETAILS",
    "discipline": "A",
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
    "page": 10,
    "sheet": "A-601",
    "title": "DOOR & WINDOW SCHEDULES, FRAMES & DETAILS",
    "discipline": "A",
    "type": "elevation",
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
    "page": 11,
    "sheet": "S-000",
    "title": "COVER",
    "discipline": "S",
    "type": "cover",
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
    "page": 12,
    "sheet": "S-100",
    "title": "GENERAL NOTES",
    "discipline": "S",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 12,
    "legend_count": 8,
    "refs_out": 1,
    "refs_in": 1
  },
  {
    "page": 13,
    "sheet": "S-101",
    "title": "GRAVITY & LATERAL LOADING",
    "discipline": "S",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 2,
    "refs_out": 2,
    "refs_in": 4
  },
  {
    "page": 14,
    "sheet": "S-102",
    "title": "BUILDING CLEAR HEIGHT ELEVATIONS",
    "discipline": "S",
    "type": "elevation",
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
    "page": 15,
    "sheet": "S-103",
    "title": "SPECIAL INSPECTIONS",
    "discipline": "S",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 11,
    "legend_count": 8,
    "refs_out": 41,
    "refs_in": 0
  },
  {
    "page": 16,
    "sheet": "S-200",
    "title": "OVERALL FOUNDATION PLAN",
    "discipline": "S",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 5,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 17,
    "sheet": "S-210",
    "title": "OVERALL ROOF  FRAMING PLAN",
    "discipline": "S",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 2,
    "refs_out": 20,
    "refs_in": 0
  },
  {
    "page": 18,
    "sheet": "S-300",
    "title": "OVERALL TILT PANEL PLAN",
    "discipline": "S",
    "type": "elevation",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 7,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 7,
    "refs_in": 0
  },
  {
    "page": 19,
    "sheet": "S-301",
    "title": "TILT PANEL EMBED/REINF SECTIONS & DETAILS",
    "discipline": "S",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 8
  },
  {
    "page": 20,
    "sheet": "S-310",
    "title": "NORTH TILT PANEL ELEVATIONS",
    "discipline": "S",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 2,
    "refs_in": 6
  },
  {
    "page": 21,
    "sheet": "S-311",
    "title": "EAST TILT PANEL ELEVATIONS",
    "discipline": "S",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 2,
    "refs_in": 2
  },
  {
    "page": 22,
    "sheet": "S-312",
    "title": "SOUTH TILT PANEL ELEVATIONS",
    "discipline": "S",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 2,
    "refs_in": 6
  },
  {
    "page": 23,
    "sheet": "S-313",
    "title": "WEST TILT PANEL ELEVATIONS",
    "discipline": "S",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 24,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
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
    "page": 25,
    "sheet": "S-321",
    "title": "TILT REBAR ELEVATION",
    "discipline": "S",
    "type": "elevation",
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
    "page": 26,
    "sheet": "S-322",
    "title": "TILT REBAR ELEVATION",
    "discipline": "S",
    "type": "elevation",
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
    "page": 27,
    "sheet": "S-323",
    "title": "TILT REBAR ELEVATION",
    "discipline": "S",
    "type": "elevation",
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
    "page": 28,
    "sheet": "S-400",
    "title": "CMU SECTIONS AND DETAILS",
    "discipline": "S",
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
    "page": 29,
    "sheet": "S-500",
    "title": "FOUNDATION SECTIONS AND DETAILS",
    "discipline": "S",
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
    "page": 30,
    "sheet": "S-501",
    "title": "FOUNDATION SECTIONS AND DETAILS",
    "discipline": "S",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 6,
    "legend_count": 3,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 31,
    "sheet": "S-510",
    "title": "SLAB ON GRADE SECTIONS AND DETAILS",
    "discipline": "S",
    "type": "detail_sheet",
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
    "page": 32,
    "sheet": "S-520",
    "title": "STEEL FRAMING SECTIONS AND DETAILS",
    "discipline": "S",
    "type": "detail_sheet",
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
    "page": 33,
    "sheet": "S-530",
    "title": "BRACE FRAMING SECTIONS & DETAILS",
    "discipline": "S",
    "type": "detail_sheet",
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
    "page": 34,
    "sheet": "M-001",
    "title": "MECHANICAL GENERAL",
    "discipline": "M",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 35,
    "sheet": "M-002",
    "title": "MECHANICAL SCHEDULES & DETAILS",
    "discipline": "M",
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
    "page": 36,
    "sheet": "M-100",
    "title": "MECHANICAL PLANS",
    "discipline": "M",
    "type": "mep_plan",
    "confidence": 0.3,
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
    "page": 37,
    "sheet": "P-001",
    "title": "PLUMBING GENERAL",
    "discipline": "P",
    "type": "floor_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 6,
    "legend_count": 3,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 38,
    "sheet": "P-002",
    "title": "PLUMBING SPECIFICATIONS",
    "discipline": "P",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 7,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 39,
    "sheet": "P-100",
    "title": "PLUMBING FLOOR PLAN",
    "discipline": "P",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 40,
    "sheet": "E-001",
    "title": "ELECTRICAL GENERAL",
    "discipline": "E",
    "type": "floor_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 9,
    "legend_count": 6,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 41,
    "sheet": "E-002",
    "title": "LIGHTING GENERAL",
    "discipline": "E",
    "type": "floor_plan",
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
    "page": 42,
    "sheet": "E-101",
    "title": "ELECTRICAL SITE PLAN",
    "discipline": "E",
    "type": "site_plan",
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
    "page": 43,
    "sheet": "E-201",
    "title": "ELECTRICAL PLAN - LIGHTING",
    "discipline": "E",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 44,
    "sheet": "E-301",
    "title": "FLOOR PLAN - POWER",
    "discipline": "E",
    "type": "floor_plan",
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
    "page": 45,
    "sheet": "E-401",
    "title": "ELECTRICAL RISER & SCHEDULES",
    "discipline": "E",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 9,
    "legend_count": 9,
    "refs_out": 5,
    "refs_in": 0
  },
  {
    "page": 46,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "cover",
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
    "page": 47,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "life_safety",
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
    "page": 48,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "site_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 3,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 3,
    "refs_in": 0
  },
  {
    "page": 49,
    "sheet": "A-101",
    "title": "OVERALL FLOOR PLAN & ROOF PLANS",
    "discipline": "A",
    "type": "roof_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 10,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 12,
    "refs_in": 0
  },
  {
    "page": 50,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 4,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 6,
    "refs_in": 0
  },
  {
    "page": 51,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 3,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 3,
    "refs_in": 0
  },
  {
    "page": 52,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
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
    "page": 53,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
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
    "page": 54,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 8,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 8,
    "refs_in": 0
  },
  {
    "page": 55,
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
    "page": 56,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
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
    "page": 57,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "cover",
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
    "page": 58,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 11,
    "legend_count": 7,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 59,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 2,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 60,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
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
    "page": 61,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 11,
    "legend_count": 8,
    "refs_out": 41,
    "refs_in": 0
  },
  {
    "page": 62,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 5,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 63,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 2,
    "refs_out": 22,
    "refs_in": 0
  },
  {
    "page": 64,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 7,
    "zone_count": 4,
    "legend_count": 6,
    "refs_out": 7,
    "refs_in": 0
  },
  {
    "page": 65,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
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
    "page": 66,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 67,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 68,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 69,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 2,
    "refs_in": 0
  },
  {
    "page": 70,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
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
    "page": 71,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
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
    "page": 72,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
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
    "page": 73,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
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
    "page": 74,
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
    "page": 75,
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
    "page": 76,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 6,
    "legend_count": 3,
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
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 78,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
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
    "page": 79,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
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
    "page": 80,
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
    "zone_count": 3,
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
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 8,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 82,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "unknown",
    "confidence": 0.0,
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
    "page": 83,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 6,
    "legend_count": 3,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 84,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 7,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 85,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 86,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 9,
    "legend_count": 6,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 87,
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
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 88,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 89,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 5,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 90,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 7,
    "legend_count": 8,
    "refs_out": 4,
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
- Legend count: 145
- Quality flag count: 1

#### Quality flags raised

```json
[
  "WARNING: unusually high legend count (145) \u2014 possible pdfplumber noise"
]
```

#### Legend contents (sample, truncated)

```json
[
  {
    "type": "general_notes",
    "title": "S-100\nGENERAL NOTES",
    "page": 0,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: S-100\nGENERAL NOTES",
    "entries_sample": [
      {
        "key": "51",
        "desc": "- MECHANICAL"
      },
      {
        "key": "61",
        "desc": "- PLUMBING"
      },
      {
        "key": "81",
        "desc": "- ELECTRICAL"
      }
    ]
  },
  {
    "type": "legend",
    "title": "GRAPHIC LEGEND",
    "page": 1,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: GRAPHIC LEGEND",
    "entries_sample": [
      {
        "key": "05",
        "desc": "= 1/2 HOUR"
      },
      {
        "key": "1",
        "desc": "= 1 HOUR"
      },
      {
        "key": "2",
        "desc": "= 2 HOUR"
      },
      {
        "key": "3",
        "desc": "= 3 HOUR"
      },
      {
        "key": "4",
        "desc": "= 4 HOUR"
      },
      {
        "key": "300",
        "desc": "GSF"
      },
      {
        "key": "000",
        "desc": "SF"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:\n1.  DO NOT OVERLAP THE FLANGES FROM ADJACENT PIPE FLASHINGS\n2.  ANY SEAM ",
    "page": 7,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES:\n1.  DO NOT OVERLAP THE FLANGES FR",
    "entries_sample": [
      {
        "key": "1",
        "desc": "WITH MECHANICALLY FASTENED SPEC, MEMBRANE MUST BE MECHANICALLY ATTACHED WITH T.P"
      },
      {
        "key": "2",
        "desc": "DO NOT OVERLAP THE FLANGES FROM ADJACENT PIPE FLASHINGS."
      },
      {
        "key": "3",
        "desc": "15 YEAR AND 20 YEAR GUARANTEES REQUIRE DOUBLE WRAP."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "STOREFRONT SCHEDULE",
    "page": 10,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: STOREFRONT SCHEDULE",
    "entries_sample": [
      {
        "key": "152.00",
        "desc": "SF"
      },
      {
        "key": "152.00",
        "desc": "SF"
      },
      {
        "key": "49.00",
        "desc": "SF"
      },
      {
        "key": "95.00",
        "desc": "SF"
      },
      {
        "key": "114.00",
        "desc": "SF"
      },
      {
        "key": "45.00",
        "desc": "SF"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "ANCHORS AND PROXIMITY OF ANCHORS TO EDGE OF CONCRETE. \nINSTALL ANCHORS IN ACCORD",
    "page": 12,
    "entry_count": 14,
    "confidence": 0.7,
    "source": "legend: ANCHORS AND PROXIMITY OF ANCHORS TO EDGE",
    "entries_sample": [
      {
        "key": "1",
        "desc": "CONTRACTOR REVIEW THE EXISTING STRUCTURAL DRAWINGS AND"
      },
      {
        "key": "1",
        "desc": "PROVIDE CALCULATIONS THAT ARE PREPARED & SEALED BY A"
      },
      {
        "key": "2",
        "desc": "PROVIDE CALCULATIONS THAT DEMONSTRATE THE SUBSTITUTED"
      },
      {
        "key": "3",
        "desc": "INCLUDE CONSIDERATION OF CREEP, IN-SERVICE TEMPERATURE AND"
      },
      {
        "key": "4",
        "desc": "EVALUATION OF SUBSTITUTIONS WILL BE BASED ON THEIR HAVING AN ICC"
      },
      {
        "key": "2",
        "desc": "CONCRETE ANCHORS"
      },
      {
        "key": "1",
        "desc": "HILTI KWIK BOLT-TZ EXPANSION ANCHORS (ICC ESR-1917)"
      },
      {
        "key": "2",
        "desc": "HILTI KWIK HUS-EZ AND KWIK HUS EZ-I SCREW ANCHORS (ICC ESR-3027)"
      },
      {
        "key": "3",
        "desc": "SIMPSON STRONG-TIE \u201cTITEN-HD\u201d SCREW ANCHORS (ICC ESR-2713)"
      },
      {
        "key": "4",
        "desc": "SIMPSON STRONG-TIE \u201cSTRONG-BOLT 2\u201d EXPANSION ANCHORS (ICC"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "UNDERTAKE TO LOCATE THE POSITION OF MATERIAL EMBEDDED IN THE \nCONCRETE AT THE LO",
    "page": 12,
    "entry_count": 17,
    "confidence": 0.7,
    "source": "legend: UNDERTAKE TO LOCATE THE POSITION OF MATE",
    "entries_sample": [
      {
        "key": "1",
        "desc": "PROVIDE CALCULATIONS THAT ARE PREPARED & SEALED BY A"
      },
      {
        "key": "2",
        "desc": "PROVIDE CALCULATIONS THAT DEMONSTRATE THE SUBSTITUTED"
      },
      {
        "key": "3",
        "desc": "INCLUDE CONSIDERATION OF CREEP, IN-SERVICE TEMPERATURE AND"
      },
      {
        "key": "4",
        "desc": "EVALUATION OF SUBSTITUTIONS WILL BE BASED ON THEIR HAVING AN ICC"
      },
      {
        "key": "2",
        "desc": "CONCRETE ANCHORS"
      },
      {
        "key": "1",
        "desc": "HILTI KWIK BOLT-TZ EXPANSION ANCHORS (ICC ESR-1917)"
      },
      {
        "key": "2",
        "desc": "HILTI KWIK HUS-EZ AND KWIK HUS EZ-I SCREW ANCHORS (ICC ESR-3027)"
      },
      {
        "key": "3",
        "desc": "SIMPSON STRONG-TIE \u201cTITEN-HD\u201d SCREW ANCHORS (ICC ESR-2713)"
      },
      {
        "key": "4",
        "desc": "SIMPSON STRONG-TIE \u201cSTRONG-BOLT 2\u201d EXPANSION ANCHORS (ICC"
      },
      {
        "key": "5",
        "desc": "DEWALT / POWERS POWER-STUD + SD2 EXPANSION ANCHORS (ICC ESR"
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "ELECTRICAL, PLUMBING, AND CIVIL DRAWINGS.  NOTIFY STRUCTURAL ENGINEER OF \nANY CO",
    "page": 12,
    "entry_count": 13,
    "confidence": 0.7,
    "source": "legend: ELECTRICAL, PLUMBING, AND CIVIL DRAWINGS",
    "entries_sample": [
      {
        "key": "12",
        "desc": "CONTRACT DOCUMENTS SHALL GOVERN IN THE EVENT OF A CONFLICT WITH THE"
      },
      {
        "key": "13",
        "desc": "ELECTRONIC DRAWING FILES WILL NOT BE PROVIDED TO THE CONTRACTOR."
      },
      {
        "key": "14",
        "desc": "STRUCTURAL ENGINEER IS NOT RESPONSIBLE FOR THE DESIGN OF STEEL STAIRS,"
      },
      {
        "key": "15",
        "desc": "IT IS EXPECTED THAT THE GENERAL CONTRACTOR IS EXPERIENCED IN THE TYPE OF"
      },
      {
        "key": "16",
        "desc": "PROVIDE CONTINGENCY FOR REPAIRING 2700 LINEAR FEET OF CRACKS IN THE FLOOR"
      },
      {
        "key": "17",
        "desc": "SPECIAL INSPECTIONS SHALL BE IN ACCORDANCE WITH CHAPTER 17 OF THE"
      },
      {
        "key": "18",
        "desc": "INSPECTION REPORTS SHALL BE FURNISHED TO THE BUILDING OFFICIAL, ARCHITECT"
      },
      {
        "key": "19",
        "desc": "SPECIAL INSPECTOR SHALL SUBMIT A FINAL REPORT STATING THAT THE STRUCTURAL"
      },
      {
        "key": "20",
        "desc": "CONTRACTOR HAS SOLE RESPONSIBILITY FOR MEANS, METHODS, SAFETY,"
      },
      {
        "key": "21",
        "desc": "THE STRUCTURE IS STABLE ONLY IN ITS COMPLETED FORM.  TEMPORARY SUPPORTS"
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "GENERAL NOTES  SHEET NUMBER: S-100  PROJECT NAME: BEARSS AVENUE DISTRIBUTION CEN",
    "page": 12,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: GENERAL NOTES  SHEET NUMBER: S-100  PROJ",
    "entries_sample": [
      {
        "key": "16",
        "desc": "PROVIDE CONTINGENCY FOR REPAIRING 2700 LINEAR FEET OF CRACKS IN THE FLOOR"
      },
      {
        "key": "17",
        "desc": "SPECIAL INSPECTIONS SHALL BE IN ACCORDANCE WITH CHAPTER 17 OF THE"
      },
      {
        "key": "18",
        "desc": "INSPECTION REPORTS SHALL BE FURNISHED TO THE BUILDING OFFICIAL, ARCHITECT"
      },
      {
        "key": "19",
        "desc": "SPECIAL INSPECTOR SHALL SUBMIT A FINAL REPORT STATING THAT THE STRUCTURAL"
      },
      {
        "key": "20",
        "desc": "CONTRACTOR HAS SOLE RESPONSIBILITY FOR MEANS, METHODS, SAFETY,"
      },
      {
        "key": "21",
        "desc": "THE STRUCTURE IS STABLE ONLY IN ITS COMPLETED FORM.  TEMPORARY SUPPORTS"
      },
      {
        "key": "22",
        "desc": "CONTRACTOR SHALL SUBMIT SHOP DRAWINGS WITH EDGE OF SLAB DIMENSIONS,"
      },
      {
        "key": "23",
        "desc": "STRUCTURAL DOCUMENTS ARE BEING RELEASED PRIOR TO DOCUMENTS BY OTHER"
      },
      {
        "key": "1",
        "desc": "THE DESIGN SOIL BEARING PRESSURE IS 2000 PSF FOR COLUMN FOOTINGS AND WALL"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "CONSTRUCTION REQUIRED; THEREFORE IT IS EXPECTED THAT THE GENERAL \nCONTRACTOR WIL",
    "page": 12,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: CONSTRUCTION REQUIRED; THEREFORE IT IS E",
    "entries_sample": [
      {
        "key": "17",
        "desc": "SPECIAL INSPECTIONS SHALL BE IN ACCORDANCE WITH CHAPTER 17 OF THE"
      },
      {
        "key": "18",
        "desc": "INSPECTION REPORTS SHALL BE FURNISHED TO THE BUILDING OFFICIAL, ARCHITECT"
      },
      {
        "key": "19",
        "desc": "SPECIAL INSPECTOR SHALL SUBMIT A FINAL REPORT STATING THAT THE STRUCTURAL"
      },
      {
        "key": "20",
        "desc": "CONTRACTOR HAS SOLE RESPONSIBILITY FOR MEANS, METHODS, SAFETY,"
      },
      {
        "key": "21",
        "desc": "THE STRUCTURE IS STABLE ONLY IN ITS COMPLETED FORM.  TEMPORARY SUPPORTS"
      },
      {
        "key": "22",
        "desc": "CONTRACTOR SHALL SUBMIT SHOP DRAWINGS WITH EDGE OF SLAB DIMENSIONS,"
      },
      {
        "key": "23",
        "desc": "STRUCTURAL DOCUMENTS ARE BEING RELEASED PRIOR TO DOCUMENTS BY OTHER"
      },
      {
        "key": "1",
        "desc": "THE DESIGN SOIL BEARING PRESSURE IS 2000 PSF FOR COLUMN FOOTINGS AND WALL"
      },
      {
        "key": "16",
        "desc": "PROVIDE CONTINGENCY FOR REPAIRING 2700 LINEAR FEET OF CRACKS IN THE FLOOR"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "CONCRETE MIXTURE SCHEDULE",
    "page": 12,
    "entry_count": 20,
    "confidence": 0.7,
    "source": "legend: CONCRETE MIXTURE SCHEDULE",
    "entries_sample": [
      {
        "key": "3000",
        "desc": "PSI"
      },
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "150",
        "desc": "PCF"
      },
      {
        "key": "4000",
        "desc": "PSI AT 28-DAYS"
      },
      {
        "key": "4500",
        "desc": "PSI AT 56-DAYS"
      },
      {
        "key": "0",
        "desc": "45"
      },
      {
        "key": "4",
        "desc": "5% \u00b1 1.5%"
      },
      {
        "key": "150",
        "desc": "PCF"
      },
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "1",
        "desc": "1/2\""
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOMINAL MAXIMUM\nAGGREGATE SIZE\n(NOTE 3)\nMAXIMUM CONCRETE\nWEIGHT\nFOOTINGS\nBRACED ",
    "page": 12,
    "entry_count": 18,
    "confidence": 0.7,
    "source": "legend: NOMINAL MAXIMUM\nAGGREGATE SIZE\n(NOTE 3)\n",
    "entries_sample": [
      {
        "key": "4000",
        "desc": "PSI AT 28-DAYS"
      },
      {
        "key": "4500",
        "desc": "PSI AT 56-DAYS"
      },
      {
        "key": "0",
        "desc": "45"
      },
      {
        "key": "4",
        "desc": "5% \u00b1 1.5%"
      },
      {
        "key": "150",
        "desc": "PCF"
      },
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "1",
        "desc": "1/2\""
      },
      {
        "key": "150",
        "desc": "PCF"
      },
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "110",
        "desc": "PCF"
      }
    ]
  },
  {
    "type": "notes",
    "title": "SLAB-ON-GRADE\n4000 PSI\nSEE NOTE 1\n3% MAX\n1 1/2\"\n150 PCF\nLIGHTWEIGHT ELEVATED\nSLA",
    "page": 12,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: SLAB-ON-GRADE\n4000 PSI\nSEE NOTE 1\n3% MAX",
    "entries_sample": [
      {
        "key": "150",
        "desc": "PCF"
      },
      {
        "key": "1",
        "desc": "WHERE NO MAXIMUM WATER CEMENT RATIO IS NOTED FOR DURABILITY. PROPORTIONING OF WA"
      },
      {
        "key": "2",
        "desc": "WHERE AIR ENTRAINMENT IS NOT REQUIRED BY DESIGN, THE CONTRACTOR, INSTALLER, AND "
      },
      {
        "key": "3",
        "desc": "COARSE AGGREGATE SHALL BE ASTM C 33, GRADED.  SELECT GRADING CLASS PER TYPE OF C"
      },
      {
        "key": "4",
        "desc": "FINE AGGREGATE FOR INTERIOR CONCRETE SLAB SHALL CONSIST OF A MINIMUM 70% NATURAL"
      },
      {
        "key": "5",
        "desc": "MIX DESIGN SUBMITTAL FOR CONCRETE WITH BLENDED AGGREGATES SHALL INCLUDE AGGREGAT"
      },
      {
        "key": "6",
        "desc": "FLY ASH IS NOT PERMITTED IN CONCRETE SLAB OR TILT-UP WALL PANEL MIX DESIGNS."
      },
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "110",
        "desc": "PCF"
      }
    ]
  },
  {
    "type": "notes",
    "title": "JOIST LOAD NOTES:\n1. ALL LOADS SHOWN ARE UNFACTORED\n2. ALL CODE LOAD COMBINATION",
    "page": 13,
    "entry_count": 13,
    "confidence": 0.7,
    "source": "legend: JOIST LOAD NOTES:\n1. ALL LOADS SHOWN ARE",
    "entries_sample": [
      {
        "key": "1.0",
        "desc": "SECOND PERIOD MAPPED SPECTRAL RESPONSE ACCELERATION"
      },
      {
        "key": "1.0",
        "desc": "SECOND PERIOD SPECTRAL RESPONSE COEFFICIENT"
      },
      {
        "key": "1",
        "desc": "0"
      },
      {
        "key": "140",
        "desc": "MPH (FIG. 1609.3 (1) - FBC 2023)"
      },
      {
        "key": "108",
        "desc": "MPH (SECT.1609.3.1 - FBC 2023)"
      },
      {
        "key": "49.22",
        "desc": "PSF"
      },
      {
        "key": "50.03",
        "desc": "PSF"
      },
      {
        "key": "0",
        "desc": "85"
      },
      {
        "key": "1.00",
        "desc": "(FIG 26.8-1 ASCE)"
      },
      {
        "key": "0.85",
        "desc": "(TABLE 26.6-1 ASCE)"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NET WIND UPLIFT FOR GIRDERS NOTES:",
    "page": 13,
    "entry_count": 8,
    "confidence": 0.7,
    "source": "legend: NET WIND UPLIFT FOR GIRDERS NOTES:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "H = 31'-6\""
      },
      {
        "key": "2",
        "desc": "GIRDERS ARE PART OF MAIN WIND FORCE RESISTING SYSTEM."
      },
      {
        "key": "3",
        "desc": "SUSTAINED DEAD LOAD OF 8 PSF USED FOR NET UPLIFT."
      },
      {
        "key": "4",
        "desc": "NO INCREASE IN ALLOWABLE STRESS IS PERMITTED."
      },
      {
        "key": "5",
        "desc": "ALL LOADS ARE SERVICE LOADS (0.6Dmin+0.6W)."
      },
      {
        "key": "6",
        "desc": "SEE SHEET S-101 FOR MWFRS WIND PRESSURES."
      },
      {
        "key": "0",
        "desc": "6*H"
      },
      {
        "key": "0",
        "desc": "2*H"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "SCHEDULE OF SPECIAL INSPECTION SERVICES",
    "page": 15,
    "entry_count": 8,
    "confidence": 0.7,
    "source": "legend: SCHEDULE OF SPECIAL INSPECTION SERVICES",
    "entries_sample": [
      {
        "key": "1704.2",
        "desc": "Inspection of Fabricators"
      },
      {
        "key": "1705.1",
        "desc": "1 Special Cases"
      },
      {
        "key": "1705.2",
        "desc": "Steel Construction"
      },
      {
        "key": "1",
        "desc": "Fabricator and erector documents (Verify  reports"
      },
      {
        "key": "2",
        "desc": "Material verification of structural steel"
      },
      {
        "key": "3",
        "desc": "Embedments (Verify diameter, grade, type, length,"
      },
      {
        "key": "4",
        "desc": "Verify member locations, braces, stiffeners, and"
      },
      {
        "key": "5",
        "desc": "Structural steel welding:"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "SCHEDULE OF SPECIAL INSPECTION SERVICES",
    "page": 15,
    "entry_count": 11,
    "confidence": 0.7,
    "source": "legend: SCHEDULE OF SPECIAL INSPECTION SERVICES",
    "entries_sample": [
      {
        "key": "4",
        "desc": "Inspection of anchors and reinforcing steel post-"
      },
      {
        "key": "5",
        "desc": "Verify use of approved design mix"
      },
      {
        "key": "6",
        "desc": "Fresh concrete sampling, perform slump and air"
      },
      {
        "key": "7",
        "desc": "Inspection for concrete and shotcrete  placement"
      },
      {
        "key": "8",
        "desc": "Inspection for maintenance of specified curing"
      },
      {
        "key": "9",
        "desc": "Inspection of prestressed concrete:"
      },
      {
        "key": "10",
        "desc": "Erection of precast concrete members"
      },
      {
        "key": "1705",
        "desc": "2"
      },
      {
        "key": "11",
        "desc": "Verification of in-situ concrete strength, prior to"
      },
      {
        "key": "12",
        "desc": "Inspection of formwork for shape, lines,"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "SCHEDULE OF SPECIAL INSPECTION SERVICES",
    "page": 15,
    "entry_count": 15,
    "confidence": 0.7,
    "source": "legend: SCHEDULE OF SPECIAL INSPECTION SERVICES",
    "entries_sample": [
      {
        "key": "3",
        "desc": "For high-load diaphragms, verify nominal size of"
      },
      {
        "key": "4",
        "desc": "Metal-plate-connected wood trusses spanning 60"
      },
      {
        "key": "1705.6",
        "desc": "Soils"
      },
      {
        "key": "1",
        "desc": "Verify materials below shallow foundations are"
      },
      {
        "key": "2",
        "desc": "Verify excavations are extended to proper depth"
      },
      {
        "key": "3",
        "desc": "Perform classification and testing of controlled fit"
      },
      {
        "key": "4",
        "desc": "Verify use of proper materials, densities, and lift"
      },
      {
        "key": "5",
        "desc": "Prior to placement of controlled fill, observe"
      },
      {
        "key": "1705.7",
        "desc": "Driven Deep Foundations"
      },
      {
        "key": "1",
        "desc": "Verify element materials, sizes and lengths"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "MATERIAL / ACTIVITY\nSERVICE\nY/N\nEXTENT\nAGENT*\nDATE \nCOMPLETED",
    "page": 15,
    "entry_count": 8,
    "confidence": 0.7,
    "source": "legend: MATERIAL / ACTIVITY\nSERVICE\nY/N\nEXTENT\nA",
    "entries_sample": [
      {
        "key": "1704.2",
        "desc": "Inspection of Fabricators"
      },
      {
        "key": "1705.1",
        "desc": "1 Special Cases"
      },
      {
        "key": "1705.2",
        "desc": "Steel Construction"
      },
      {
        "key": "1",
        "desc": "Fabricator and erector documents (Verify  reports"
      },
      {
        "key": "2",
        "desc": "Material verification of structural steel"
      },
      {
        "key": "3",
        "desc": "Embedments (Verify diameter, grade, type, length,"
      },
      {
        "key": "4",
        "desc": "Verify member locations, braces, stiffeners, and"
      },
      {
        "key": "5",
        "desc": "Structural steel welding:"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "MATERIAL / ACTIVITY\nSERVICE\nY/N\nEXTENT\nAGENT*\nDATE \nCOMPLETED",
    "page": 15,
    "entry_count": 12,
    "confidence": 0.7,
    "source": "legend: MATERIAL / ACTIVITY\nSERVICE\nY/N\nEXTENT\nA",
    "entries_sample": [
      {
        "key": "4",
        "desc": "Inspection of anchors and reinforcing steel post-"
      },
      {
        "key": "5",
        "desc": "Verify use of approved design mix"
      },
      {
        "key": "6",
        "desc": "Fresh concrete sampling, perform slump and air"
      },
      {
        "key": "7",
        "desc": "Inspection for concrete and shotcrete  placement"
      },
      {
        "key": "8",
        "desc": "Inspection for maintenance of specified curing"
      },
      {
        "key": "9",
        "desc": "Inspection of prestressed concrete:"
      },
      {
        "key": "10",
        "desc": "Erection of precast concrete members"
      },
      {
        "key": "1705",
        "desc": "2"
      },
      {
        "key": "11",
        "desc": "Verification of in-situ concrete strength, prior to"
      },
      {
        "key": "12",
        "desc": "Inspection of formwork for shape, lines,"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "MATERIAL / ACTIVITY\nSERVICE\nY/N\nEXTENT\nAGENT*\nDATE \nCOMPLETED",
    "page": 15,
    "entry_count": 15,
    "confidence": 0.7,
    "source": "legend: MATERIAL / ACTIVITY\nSERVICE\nY/N\nEXTENT\nA",
    "entries_sample": [
      {
        "key": "3",
        "desc": "For high-load diaphragms, verify nominal size of"
      },
      {
        "key": "4",
        "desc": "Metal-plate-connected wood trusses spanning 60"
      },
      {
        "key": "1705.6",
        "desc": "Soils"
      },
      {
        "key": "1",
        "desc": "Verify materials below shallow foundations are"
      },
      {
        "key": "2",
        "desc": "Verify excavations are extended to proper depth"
      },
      {
        "key": "3",
        "desc": "Perform classification and testing of controlled fit"
      },
      {
        "key": "4",
        "desc": "Verify use of proper materials, densities, and lift"
      },
      {
        "key": "5",
        "desc": "Prior to placement of controlled fill, observe"
      },
      {
        "key": "1705.7",
        "desc": "Driven Deep Foundations"
      },
      {
        "key": "1",
        "desc": "Verify element materials, sizes and lengths"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "2. Material verification of structural steel",
    "page": 15,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: 2. Material verification of structural s",
    "entries_sample": [
      {
        "key": "3",
        "desc": "Embedments (Verify diameter, grade, type, length,"
      },
      {
        "key": "4",
        "desc": "Verify member locations, braces, stiffeners, and"
      },
      {
        "key": "5",
        "desc": "Structural steel welding:"
      },
      {
        "key": "6",
        "desc": "Structural steel bolting:"
      },
      {
        "key": "2",
        "desc": "Material verification of structural steel"
      }
    ]
  },
  {
    "type": "notes",
    "title": "Notes: 1. The inspection and testing agent(s) shall be engaged by the Owner or t",
    "page": 15,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: Notes: 1. The inspection and testing age",
    "entries_sample": [
      {
        "key": "2",
        "desc": "The list of Special Inspectors may be submitted as a separate document, if noted"
      },
      {
        "key": "3",
        "desc": "Special Inspections as required by Section 1704.2.5 are not required where the f"
      },
      {
        "key": "4",
        "desc": "Observe on a random basis, operations need not be delayed pending these inspecti"
      },
      {
        "key": "5",
        "desc": "NDT of welds competed in an approved fabricator's shop may be performed by that"
      }
    ]
  },
  {
    "type": "notes",
    "title": "FOUNDATION PLAN NOTES:",
    "page": 16,
    "entry_count": 8,
    "confidence": 0.7,
    "source": "legend: FOUNDATION PLAN NOTES:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "TOP OF SLAB ON GRADE ELEVATION = SEE CIVIL , REFERENCE LEVEL (+0'-0\")"
      },
      {
        "key": "2",
        "desc": "CONTROL JOINTS WILL BE SPACED AT EACH COLUMN AND 15 FEET OC MAXIMUM."
      },
      {
        "key": "3",
        "desc": "TOP OF COLUMN FOOTING ELEVATION = (-) 1 FOOT BELOW TOP OF SLAB (UNLESS"
      },
      {
        "key": "4",
        "desc": "SLAB ON GRADE TO BE 6 INCH UNREINFORCED SLAB BEARING ON COMPACTED"
      },
      {
        "key": "2000",
        "desc": "PSF"
      },
      {
        "key": "2000",
        "desc": "PSF"
      },
      {
        "key": "2000",
        "desc": "PSF"
      },
      {
        "key": "2000",
        "desc": "PSF"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "FOOTING SCHEDULE",
    "page": 16,
    "entry_count": 5,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "MARK",
        "desc": "LENGTH x WIDTH DEPTH REINFORCEMENT SOIL BEARING REMARKS"
      },
      {
        "key": "F6.0",
        "desc": "6' - 0\" X 6' - 0\" 1' - 2\" (7)#5 EW BOTT 2000 PSF"
      },
      {
        "key": "F7.5",
        "desc": "7' - 6\" X 7' - 6\" 1' - 6\" (10)#5 EW BOTT 2000 PSF"
      },
      {
        "key": "F8.0",
        "desc": "8' - 0\" X 8' - 0\" 1' - 6\" (11)#5 EW BOTT 2000 PSF"
      },
      {
        "key": "F20",
        "desc": "20' - 0\" X 20' - 0\" 3' - 6\" (23)#8 EW T&B 2000 PSF"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "GRADE BEAM SCHEDULE",
    "page": 16,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "MARK",
        "desc": "WIDTH x DEPTH SOIL BEARING REINFORCEMEN T REMARKS"
      },
      {
        "key": "GB3.5",
        "desc": "3' - 6\" X 3' - 6\" 2000 PSF (4)#8 T&B; #4 TIES\n12\" @ *NOTE: EXTEND LONGITUDINTAL "
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "(SEE GENERAL NOTES)",
    "page": 16,
    "entry_count": 9,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "INDICATES THICKENED ",
        "desc": ""
      },
      {
        "key": "INDICATES TURNED DOW",
        "desc": ""
      },
      {
        "key": "INDICATES FOOTING MA",
        "desc": ""
      },
      {
        "key": "(SEE FOOTING SCHEDU",
        "desc": ""
      },
      {
        "key": "INDICATES CONTINUOUS",
        "desc": ""
      },
      {
        "key": "CONTINIOUS WALL FOOT",
        "desc": ""
      },
      {
        "key": "(SEE WALL FOOTING SC",
        "desc": ""
      },
      {
        "key": "INDICATES GRADE BEAM",
        "desc": ""
      },
      {
        "key": "(SEE GRADE BEAM SCHE",
        "desc": ""
      }
    ]
  },
  {
    "type": "notes",
    "title": "GB#",
    "page": 16,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "(-X",
        "desc": "' - X\")"
      },
      {
        "key": "SIZE (BP#)",
        "desc": ""
      }
    ]
  },
  {
    "type": "roof_notes",
    "title": "ROOF PLAN NOTES:",
    "page": 17,
    "entry_count": 12,
    "confidence": 0.7,
    "source": "legend: ROOF PLAN NOTES:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "ROOF METAL DECK WILL BE 1-1/2 INCH DEEP, 20 GAGE, TYPE B (80 KSI), WIDE RIB"
      },
      {
        "key": "2",
        "desc": "STEEL JOISTS SHALL BE BRACED BY HORIZONTAL AND/OR DIAGONAL BRIDGING"
      },
      {
        "key": "3",
        "desc": "STEEL JOIST SEATS SHALL BE 1/4 INCH MINIMUM AT WALLS."
      },
      {
        "key": "4",
        "desc": "SEE GENERAL NOTES FOR ADDITIONAL INFORMATION."
      },
      {
        "key": "5",
        "desc": "ELEVATIONS SHOWN ON PLAN ARE BOTTOM OF DECK."
      },
      {
        "key": "6",
        "desc": "SEE TYPICAL ROOF OPENING DETAIL FOR FRAMING OF THE OPENINGS THROUGH"
      },
      {
        "key": "7",
        "desc": "JOIST SHOP DRAWINGS SHALL INDICATE WHERE THE BOLTED DIAGONAL"
      },
      {
        "key": "8",
        "desc": "ROOF STRUCTURE SHOWN AS REQUIRED TO MAINTAIN MIN VERTICAL CLEARANCE"
      },
      {
        "key": "9",
        "desc": "ROOF SLOPE BASED ON 1/4 INCH PER FOOT."
      },
      {
        "key": "10",
        "desc": "JOISTS AND JOIST GIRDERS SHALL BE CAMBERED PER SJI SPECIFICATIONS."
      }
    ]
  },
  {
    "type": "legend",
    "title": "13. JOISTS AND JOIST GIRDERS SHALL BE DESIGNED FOR ADDITIONAL LOADS DUE TO \nROOF",
    "page": 17,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: 13. JOISTS AND JOIST GIRDERS SHALL BE DE",
    "entries_sample": [
      {
        "key": "13",
        "desc": "JOISTS AND JOIST GIRDERS SHALL BE DESIGNED FOR ADDITIONAL LOADS DUE TO"
      },
      {
        "key": "14",
        "desc": "FOR BIDDING PURPOSES ASSUME 10% OF JOISTS WILL REQUIRE ADDITIONAL 30"
      },
      {
        "key": "15",
        "desc": "ALLOWANCE TO BE MADE FOR FUTURE RTU. IMPACT WILL BE MINIMAL IF ALIGNED"
      },
      {
        "key": "16",
        "desc": "GENERAL CONTRACTOR TO COORDINATE FIXED EXPANSION SIDE WITH"
      },
      {
        "key": "17",
        "desc": "MINIMUM EXPANSION JOINT AND STRUCTURAL SEPARATION AS REQUIRED BY"
      }
    ]
  },
  {
    "type": "notes",
    "title": "TILT PANEL PLAN NOTES:",
    "page": 18,
    "entry_count": 19,
    "confidence": 0.7,
    "source": "legend: TILT PANEL PLAN NOTES:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "TILT PANELS ARE DRAWN IN ELEVATION FROM THE INSIDE OF THE BUILDING."
      },
      {
        "key": "2",
        "desc": "TILT PANELS SHOULD REMAIN BRACED UNTIL THE ENTIRETY OF THE ROOF DECK AND ROOF FR"
      },
      {
        "key": "3",
        "desc": "REFER TO THE ARCHITECTURAL DRAWINGS FOR CONFIRMATION OF ALL PANEL DIMENSIONS, AN"
      },
      {
        "key": "4",
        "desc": "SEE TILT PANEL ELEVATIONS FOR PANEL THICKNESSES."
      },
      {
        "key": "5",
        "desc": "SEE TILT PANEL REBAR ELEVATIONS FOR PANEL REINFORCEMENT."
      },
      {
        "key": "6",
        "desc": "ALL REINFORCEMENT TO BE EA FACE UNLESS NOTED OTHERWISE."
      },
      {
        "key": "7",
        "desc": "TYPICAL REINFORCING UNLESS NOTED OTHERWISE ON PANEL REBAR ELEVATIONS:"
      },
      {
        "key": "8",
        "desc": "SEE DETAILS ON S-520  FOR DETAILS AT GIRDER BEARING."
      },
      {
        "key": "9",
        "desc": "TILT PANEL SHALL BE NORMAL WEIGHT WITH f'c = 4000 PSI MINIMUM AT 28 DAYS, UNLESS"
      },
      {
        "key": "10",
        "desc": "REINFORCEMENT SHALL BE CONTINUOUS THROUGH KNOCKOUT AREA (FUTURE OPENING)."
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:\n1. SEE PANEL REBAR ELEVATIONS FOR REINFORCING.\n2. SEE ARCHITECTURAL DRAWI",
    "page": 19,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES:\n1. SEE PANEL REBAR ELEVATIONS FOR",
    "entries_sample": [
      {
        "key": "1",
        "desc": "SEE PANEL REBAR ELEVATIONS FOR REINFORCING."
      },
      {
        "key": "2",
        "desc": "SEE ARCHITECTURAL DRAWINGS FOR JOINT ORIENTATION."
      },
      {
        "key": "3",
        "desc": "SEE PANEL ELEVATIONS FOR EMBED LOCATIONS."
      }
    ]
  },
  {
    "type": "legend",
    "title": "TILT PANEL ELEVATION LEGEND:",
    "page": 20,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: TILT PANEL ELEVATION LEGEND:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "HATCH INDICATES PILASTER OR RETURN PANEL, SEE"
      },
      {
        "key": "2",
        "desc": "DIMENSIONS TO VERTICAL EMBEDS ARE (TYP-UNO)"
      },
      {
        "key": "4",
        "desc": "HATCH INDICATES FAR SIDE EMBEDS."
      }
    ]
  },
  {
    "type": "legend",
    "title": "TILT PANEL ELEVATION LEGEND:",
    "page": 21,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: TILT PANEL ELEVATION LEGEND:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "HATCH INDICATES PILASTER OR RETURN PANEL, SEE"
      },
      {
        "key": "2",
        "desc": "DIMENSIONS TO VERTICAL EMBEDS ARE (TYP-UNO)"
      },
      {
        "key": "4",
        "desc": "HATCH INDICATES FAR SIDE EMBEDS."
      }
    ]
  },
  {
    "type": "legend",
    "title": "TILT PANEL ELEVATION LEGEND:",
    "page": 22,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: TILT PANEL ELEVATION LEGEND:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "HATCH INDICATES PILASTER OR RETURN PANEL, SEE"
      },
      {
        "key": "2",
        "desc": "DIMENSIONS TO VERTICAL EMBEDS ARE (TYP-UNO)"
      },
      {
        "key": "4",
        "desc": "HATCH INDICATES FAR SIDE EMBEDS."
      }
    ]
  },
  {
    "type": "legend",
    "title": "TILT PANEL ELEVATION LEGEND:",
    "page": 23,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: TILT PANEL ELEVATION LEGEND:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "HATCH INDICATES PILASTER OR RETURN PANEL, SEE"
      },
      {
        "key": "2",
        "desc": "DIMENSIONS TO VERTICAL EMBEDS ARE (TYP-UNO)"
      },
      {
        "key": "4",
        "desc": "HATCH INDICATES FAR SIDE EMBEDS."
      }
    ]
  },
  {
    "type": "notes",
    "title": "SEAM FOAM TO ALIGN WITH JOINT, NOT \nCORNER OF COLUMN SLEEVE (SEE NOTE 6)",
    "page": 30,
    "entry_count": 8,
    "confidence": 0.7,
    "source": "legend: SEAM FOAM TO ALIGN WITH JOINT, NOT \nCORN",
    "entries_sample": [
      {
        "key": "1",
        "desc": "1/2\""
      },
      {
        "key": "1",
        "desc": "BOTTOM OF COLUMN MUST FULLY BEAR AGAINST BASE PLATE."
      },
      {
        "key": "2",
        "desc": "BASE PLATE AND COLUMN SLEEVE MUST BE PLUMBED PRIOR TO PLACING SLAB ON GRADE"
      },
      {
        "key": "3",
        "desc": "COLUMN SLEEVE MUST BE FREE FROM STANDING WATER PRIOR TO CAULKING."
      },
      {
        "key": "4",
        "desc": "PROVIDE 3 INCHES MINIMUM CONCRETE COVER FOR ALL STEEL."
      },
      {
        "key": "5",
        "desc": "IF CONCRETE COVER IS LESS THAN 3 INCHES, THEN APPLY (1) COAT BITUMOUS MASTIC"
      },
      {
        "key": "6",
        "desc": "ACCEPTABLE FLEXIBLE FOAM ISOLATION JOINT FILLER PRODUCTS:"
      },
      {
        "key": "7",
        "desc": "5 INCHES MAXIMUM ANCHOR BOLT PROJECTION. GENERAL CONTRACTOR COORDINATE"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "FOR FTG SIZE, REINF & T/FTG EL\nSEE FOUNDATION PLAN & SCHEDULE",
    "page": 30,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: FOR FTG SIZE, REINF & T/FTG EL\nSEE FOUND",
    "entries_sample": [
      {
        "key": "1",
        "desc": "BOTTOM OF COLUMN MUST FULLY BEAR AGAINST BASE PLATE."
      },
      {
        "key": "2",
        "desc": "BASE PLATE AND COLUMN SLEEVE MUST BE PLUMBED PRIOR TO PLACING SLAB ON GRADE"
      },
      {
        "key": "3",
        "desc": "COLUMN SLEEVE MUST BE FREE FROM STANDING WATER PRIOR TO CAULKING."
      },
      {
        "key": "4",
        "desc": "PROVIDE 3 INCHES MINIMUM CONCRETE COVER FOR ALL STEEL."
      },
      {
        "key": "5",
        "desc": "IF CONCRETE COVER IS LESS THAN 3 INCHES, THEN APPLY (1) COAT BITUMOUS MASTIC"
      },
      {
        "key": "6",
        "desc": "ACCEPTABLE FLEXIBLE FOAM ISOLATION JOINT FILLER PRODUCTS:"
      },
      {
        "key": "7",
        "desc": "5 INCHES MAXIMUM ANCHOR BOLT PROJECTION. GENERAL CONTRACTOR COORDINATE"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:\n1. FOR FOOTING SIZE, REINFORCEMENT & ELEVATIONS",
    "page": 30,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES:\n1. FOR FOOTING SIZE, REINFORCEMEN",
    "entries_sample": [
      {
        "key": "2",
        "desc": "FOR FOOTING STEPS LOCATIONS (SEE FOUNDATION PLAN)."
      },
      {
        "key": "3",
        "desc": "FOOTING TIES NOT SHOWN FOR CLARITY."
      },
      {
        "key": "1",
        "desc": "1/2\" CLR"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:\n1. JOINT IN SLAB TO BE SAW CUT AS SOON AS THE CONCRETE",
    "page": 31,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES:\n1. JOINT IN SLAB TO BE SAW CUT AS",
    "entries_sample": [
      {
        "key": "1",
        "desc": "JOINT IN SLAB TO BE SAW CUT AS SOON AS THE CONCRETE"
      },
      {
        "key": "2",
        "desc": "DOWELS TO BE AT RIGHT ANGLE TO JOINT."
      },
      {
        "key": "3",
        "desc": "LOAD PLATE BASKETS BY PNA."
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:\n1. IF JOIST BEARING OCCURS AT PANEL JOINT, PROVIDE EMBEDDED",
    "page": 32,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES:\n1. IF JOIST BEARING OCCURS AT PAN",
    "entries_sample": [
      {
        "key": "2",
        "desc": "2 1/2\" JOIST SEATS @ WALLS. JOIST SEAT THICKNESS = 1/4\" MINIMUM,"
      },
      {
        "key": "3",
        "desc": "SIDES"
      },
      {
        "key": "1",
        "desc": "IF JOIST BEARING OCCURS AT PANEL JOINT, PROVIDE EMBEDDED"
      }
    ]
  },
  {
    "type": "notes",
    "title": "BRACED FRAME NOTES:",
    "page": 33,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: BRACED FRAME NOTES:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "ALL BRACE FORCES ARE ULTIMATE (UNFACTORED LRFD) AND REVERSIBLE."
      },
      {
        "key": "2",
        "desc": "OMEGA FACTORS NOT INCLUDED WITH EQ LOADS."
      },
      {
        "key": "3",
        "desc": "(-)"
      },
      {
        "key": "4",
        "desc": "(+) INDICATES FORCES ACTING DOWNWARD OR TO THE RIGHT OR COMPRESSION."
      },
      {
        "key": "5",
        "desc": "BRACE FRAME CONNECTIONS ARE DELEGATED DESIGN. PROVIDE ENGINEER OF RECORD WITH"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "A.\nMechanical equipment shall be as indicated in the equipment schedule",
    "page": 34,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: A.\nMechanical equipment shall be as indi",
    "entries_sample": [
      {
        "key": "31.1",
        "desc": "OA-69.  Sizing and spacing of hangers shall be per these standards,"
      },
      {
        "key": "3.3",
        "desc": "EQUIPMENT & MATERIALS INSTALLATION:"
      },
      {
        "key": "0",
        "desc": "25, self adhesive longitudinal seams with self adhesive lap strip, AP"
      },
      {
        "key": "2.3",
        "desc": "DUCTWORK AND ACCESSORIES:"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "WATER HAMMER ARRESTER SCHEDULE",
    "page": 37,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: WATER HAMMER ARRESTER SCHEDULE",
    "entries_sample": [
      {
        "key": "1",
        "desc": "1/4\""
      },
      {
        "key": "1",
        "desc": "1/2\""
      },
      {
        "key": "1",
        "desc": "WATER HAMMER ARRESTERS SHALL BE INSTALLED IN ACCORDANCE WITH"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "23.\nDEFECTIVE WORK IF INSPECTION OR TESTS SHOW DEFECTS, SUCH DEFECTIVE WORK OR\nM",
    "page": 37,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: 23.\nDEFECTIVE WORK IF INSPECTION OR TEST",
    "entries_sample": [
      {
        "key": "1070",
        "desc": "LISTED TEMPERATURE LIMITING DEVICE AS REQUIRED BY LOCAL PLUMBING CODE."
      },
      {
        "key": "2023",
        "desc": "FLORIDA BUILDING CODE, BUILDING, WITH FL AMENDMENTS"
      },
      {
        "key": "2023",
        "desc": "FLORIDA BUILDING CODE, PLUMBING, WITH FL AMENDMENTS"
      },
      {
        "key": "2023",
        "desc": "FLORIDA BUILDING CODE, FUEL GAS, WITH FL AMENDMENTS"
      },
      {
        "key": "2023",
        "desc": "FLORIDA BUILDING CODE, ENERGY CONSERVATION, WITH FL AMENDMENTS"
      }
    ]
  },
  {
    "type": "notes",
    "title": "24.\nCONTRACTOR TO SUBMIT ADDITIONAL SET OF GAS DRAWINGS TO HVAC PLANS\nREVIEWER. ",
    "page": 37,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: 24.\nCONTRACTOR TO SUBMIT ADDITIONAL SET ",
    "entries_sample": [
      {
        "key": "1070",
        "desc": "LISTED TEMPERATURE LIMITING DEVICE AS REQUIRED BY LOCAL PLUMBING CODE."
      },
      {
        "key": "2023",
        "desc": "FLORIDA BUILDING CODE, BUILDING, WITH FL AMENDMENTS"
      },
      {
        "key": "2023",
        "desc": "FLORIDA BUILDING CODE, PLUMBING, WITH FL AMENDMENTS"
      },
      {
        "key": "2023",
        "desc": "FLORIDA BUILDING CODE, FUEL GAS, WITH FL AMENDMENTS"
      },
      {
        "key": "2023",
        "desc": "FLORIDA BUILDING CODE, ENERGY CONSERVATION, WITH FL AMENDMENTS"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "PLUMBING AND FIRE SPRINKLER SPECIFICATIONS\nPART 1.0 GENERAL E. This project may ",
    "page": 38,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "\u0394 DESCRIPTION DATE"
      },
      {
        "key": "",
        "desc": "CHECKED BY DRAWN BY\nMBB Author\nSHEET NAME\nPLUMBING\nSPECIFICATIONS\nSHEET NUMBER R"
      }
    ]
  },
  {
    "type": "notes",
    "title": "Atlanta",
    "page": 38,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "3200 Windy Hill Road",
        "desc": ""
      },
      {
        "key": "Atlanta, GA 30339",
        "desc": ""
      }
    ]
  },
  {
    "type": "notes",
    "title": "A. These plans are diagrammatic in nature and are intended to establish",
    "page": 38,
    "entry_count": 7,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "size, general routin",
        "desc": ""
      },
      {
        "key": "show all possible co",
        "desc": ""
      },
      {
        "key": "trades to insure the",
        "desc": ""
      },
      {
        "key": "the space allotted. ",
        "desc": ""
      },
      {
        "key": "materials necessary,",
        "desc": ""
      },
      {
        "key": "of complete, functio",
        "desc": ""
      },
      {
        "key": "the drawings and des",
        "desc": ""
      }
    ]
  },
  {
    "type": "notes",
    "title": "I. Condensate drain lines shall be sized to match unit connection size",
    "page": 38,
    "entry_count": 10,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "(3/4\" minimum) and a",
        "desc": ""
      },
      {
        "key": "minimum 2\" deep wate",
        "desc": ""
      },
      {
        "key": "1/8\" per foot. Drain",
        "desc": ""
      },
      {
        "key": "or floor drains on b",
        "desc": ""
      },
      {
        "key": "wells/French drains ",
        "desc": ""
      },
      {
        "key": "in walls and below c",
        "desc": ""
      },
      {
        "key": "lavatory, should suc",
        "desc": ""
      },
      {
        "key": "At the Contractor\u2019",
        "desc": "s option, or where minimum slope cannot be maintaine"
      },
      {
        "key": "from the coil to the",
        "desc": ""
      },
      {
        "key": "provided. Discharge ",
        "desc": ""
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "A. All plumbing and fire protection equipment and materials (piping, valv",
    "page": 38,
    "entry_count": 8,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "etc.) with cold (bel",
        "desc": ""
      },
      {
        "key": "shall be insulated p",
        "desc": ""
      },
      {
        "key": "All cold fluid pipin",
        "desc": ""
      },
      {
        "key": "of staples for faste",
        "desc": ""
      },
      {
        "key": "be plenum rated with",
        "desc": ""
      },
      {
        "key": "developed rating of ",
        "desc": ""
      },
      {
        "key": "is measured at 75 de",
        "desc": ""
      },
      {
        "key": "Btu/hour, sq. ft., d",
        "desc": ""
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "affixed to unit, located adjacent to nameplate or adjacent to access door i",
    "page": 38,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "nameplate is mounted",
        "desc": ""
      },
      {
        "key": "name, and floor.",
        "desc": ""
      }
    ]
  },
  {
    "type": "notes",
    "title": "I. All piping is to be labeled with plastic labels, permanently strapped to",
    "page": 38,
    "entry_count": 13,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "piping, outside of a",
        "desc": ""
      },
      {
        "key": "building standards. ",
        "desc": ""
      },
      {
        "key": "coded, unique for ea",
        "desc": ""
      },
      {
        "key": "identification lette",
        "desc": ""
      },
      {
        "key": "easily readable from",
        "desc": ""
      },
      {
        "key": "readable from floor ",
        "desc": ""
      },
      {
        "key": "piping branch connec",
        "desc": ""
      },
      {
        "key": "wall and floor penet",
        "desc": ""
      },
      {
        "key": "systems shall be ide",
        "desc": ""
      },
      {
        "key": "domestic hot water H",
        "desc": ""
      }
    ]
  },
  {
    "type": "legend",
    "title": "ELECTRICAL GENERAL SYMBOLS LEGEND",
    "page": 40,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: ELECTRICAL GENERAL SYMBOLS LEGEND",
    "entries_sample": [
      {
        "key": "1",
        "desc": "UNLESS NOTED OTHERWISE, MOUNTING HEIGHT DIMENSIONS ARE TO THE CENTERLINE OF THE "
      },
      {
        "key": "2",
        "desc": "ALL SYMBOLS INDICATED IN THE LEGEND MAY NOT NECESSARILY BE USED ON THE PLANS."
      },
      {
        "key": "3",
        "desc": "DEVICE MOUNTING HEIGHT SHALL COMPLY WITH NFPA 72. SEE ELECTRICAL GENERAL NOTE #7"
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "ELECTRICAL GENERAL NOTES",
    "page": 40,
    "entry_count": 10,
    "confidence": 0.7,
    "source": "legend: ELECTRICAL GENERAL NOTES",
    "entries_sample": [
      {
        "key": "1",
        "desc": "ALL WORK SHALL BE COORDINATED WITH THE WORK OF OTHER TRADES TO AVOID"
      },
      {
        "key": "2",
        "desc": "THE WORK SHALL BE COORDINATED WITH THE ARCHITECTURAL DOCUMENTS FOR THE"
      },
      {
        "key": "3",
        "desc": "THE CONTRACTOR SHALL VERIFY ALL EQUIPMENT BEING INSTALLED PRIOR TO"
      },
      {
        "key": "4",
        "desc": "CONDUIT HOMERUNS MAY BE COMBINED TO INCLUDE UP TO FOUR (4) CIRCUITS.  PROVIDE"
      },
      {
        "key": "5",
        "desc": "SPECIFIC REQUIREMENTS REGARDING MATERIALS, WORKMANSHIP AND THE WORK TO BE"
      },
      {
        "key": "6",
        "desc": "COORDINATE ALL CUSTOM RECEPTACLES AND CIRCUITS WITH EQUIPMENT FURNISHED"
      },
      {
        "key": "7",
        "desc": "PROVIDE FIRE ALARM CONTROL PANEL AT LOCATION SHOWN IN ACCORDANCE WITH NFPA"
      },
      {
        "key": "72",
        "desc": "PROVIDE ADEQUATE ALARM RECEIVING AND OUTPUT MODULES TO ACCOMMODATE"
      },
      {
        "key": "8",
        "desc": "SUPPORT ALL ELECTRICAL CONDUIT, RACEWAY, OUTLET AND JUNCTION BOXES VIA"
      },
      {
        "key": "9",
        "desc": "ALL CONDUIT PENETRATIONS OF FIRE RATED WALLS, FLOORS, AND PARTITIONS SHALL BE"
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "DOOR LOCKS TO ALLOW FOR FULL EGRESS PATH AS \nNOTED ON ARCHITECTURAL LIFE SAFETY ",
    "page": 40,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: DOOR LOCKS TO ALLOW FOR FULL EGRESS PATH",
    "entries_sample": [
      {
        "key": "1",
        "desc": "HORN/STROBE DEVICE"
      },
      {
        "key": "2",
        "desc": "STROBE ONLY VISUAL DEVICE"
      },
      {
        "key": "3",
        "desc": "SPEAKER/STROBE DEVICE"
      },
      {
        "key": "4",
        "desc": "SMOKE DETECTOR"
      },
      {
        "key": "5",
        "desc": "HEAT DETECTOR"
      },
      {
        "key": "2.09",
        "desc": "TRANSFORMERS:"
      },
      {
        "key": "3.01",
        "desc": "COORDINATION:"
      },
      {
        "key": "1",
        "desc": "NO PIPING OR DUCTWORK, OTHER THAN"
      },
      {
        "key": "2",
        "desc": "NO PIPES OR DUCTS SHALL BE RUN WITHIN"
      }
    ]
  },
  {
    "type": "notes",
    "title": "FIRE ALARM AUDIO/VISUAL SIGNALING DEVICE - NOTE 3",
    "page": 40,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: FIRE ALARM AUDIO/VISUAL SIGNALING DEVICE",
    "entries_sample": [
      {
        "key": "1",
        "desc": "UNLESS NOTED OTHERWISE, MOUNTING HEIGHT DIMENSIONS ARE TO THE CENTERLINE OF THE "
      },
      {
        "key": "2",
        "desc": "ALL SYMBOLS INDICATED IN THE LEGEND MAY NOT NECESSARILY BE USED ON THE PLANS."
      },
      {
        "key": "3",
        "desc": "DEVICE MOUNTING HEIGHT SHALL COMPLY WITH NFPA 72. SEE ELECTRICAL GENERAL NOTE #7"
      },
      {
        "key": "1",
        "desc": "UNLESS NOTED OTHERWISE, MOUNTING HEIGHT DIMENSIONS ARE TO THE CENTERLINE OF THE "
      },
      {
        "key": "2",
        "desc": "ALL SYMBOLS INDICATED IN THE LEGEND MAY NOT NECESSARILY BE USED ON THE PLANS."
      },
      {
        "key": "3",
        "desc": "REFER TO PANEL SCHEDULES AND RISER DIAGRAM."
      }
    ]
  },
  {
    "type": "legend",
    "title": "ELECTRICAL GENERAL SYMBOLS LEGEND NOTES:",
    "page": 40,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: ELECTRICAL GENERAL SYMBOLS LEGEND NOTES:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "UNLESS NOTED OTHERWISE, MOUNTING HEIGHT DIMENSIONS ARE TO THE CENTERLINE OF THE "
      },
      {
        "key": "2",
        "desc": "ALL SYMBOLS INDICATED IN THE LEGEND MAY NOT NECESSARILY BE USED ON THE PLANS."
      },
      {
        "key": "3",
        "desc": "DEVICE MOUNTING HEIGHT SHALL COMPLY WITH NFPA 72. SEE ELECTRICAL GENERAL NOTE #7"
      },
      {
        "key": "1",
        "desc": "UNLESS NOTED OTHERWISE, MOUNTING HEIGHT DIMENSIONS ARE TO THE CENTERLINE OF THE "
      },
      {
        "key": "2",
        "desc": "ALL SYMBOLS INDICATED IN THE LEGEND MAY NOT NECESSARILY BE USED ON THE PLANS."
      },
      {
        "key": "3",
        "desc": "REFER TO PANEL SCHEDULES AND RISER DIAGRAM."
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "3. DEVICE MOUNTING HEIGHT SHALL COMPLY WITH NFPA 72. SEE ELECTRICAL GENERAL NOTE",
    "page": 40,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: 3. DEVICE MOUNTING HEIGHT SHALL COMPLY W",
    "entries_sample": [
      {
        "key": "1",
        "desc": "UNLESS NOTED OTHERWISE, MOUNTING HEIGHT DIMENSIONS ARE TO THE CENTERLINE OF THE "
      },
      {
        "key": "2",
        "desc": "ALL SYMBOLS INDICATED IN THE LEGEND MAY NOT NECESSARILY BE USED ON THE PLANS."
      },
      {
        "key": "3",
        "desc": "REFER TO PANEL SCHEDULES AND RISER DIAGRAM."
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "GENERAL NOTES:",
    "page": 42,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: GENERAL NOTES:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "SPECIFIC REQUIREMENTS REGARDING MATERIALS,"
      },
      {
        "key": "2",
        "desc": "REFER TO LIGHT FIXTURE SCHEDULE ON E-002."
      },
      {
        "key": "3",
        "desc": "ALL EXTERIOR ELECTRICAL DEVICES SHALL BE WEATHER"
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "GENERAL NOTES:",
    "page": 43,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: GENERAL NOTES:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "REFER TO ARCHITECTURAL REFLECTED CEILING PLAN FOR"
      },
      {
        "key": "2",
        "desc": "REFER TO LIGHTING FIXTURE SCHEDULE ON E-002."
      },
      {
        "key": "3",
        "desc": "ALL EMERGENCY LIGHTING FIXTURES SHOWN SHALL OPERATE"
      },
      {
        "key": "4",
        "desc": "PROVIDE ADDITIONAL, UNSWITCHED, \"HOT\" CONDUCTOR,"
      },
      {
        "key": "5",
        "desc": "ALL OVERHEAD CONDUIT WHERE CEILING IS OPEN TO"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "2. REFER TO LIGHTING FIXTURE SCHEDULE ON E-002.",
    "page": 43,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: 2. REFER TO LIGHTING FIXTURE SCHEDULE ON",
    "entries_sample": [
      {
        "key": "3",
        "desc": "ALL EMERGENCY LIGHTING FIXTURES SHOWN SHALL OPERATE"
      },
      {
        "key": "4",
        "desc": "PROVIDE ADDITIONAL, UNSWITCHED, \"HOT\" CONDUCTOR,"
      },
      {
        "key": "5",
        "desc": "ALL OVERHEAD CONDUIT WHERE CEILING IS OPEN TO"
      },
      {
        "key": "2",
        "desc": "REFER TO LIGHTING FIXTURE SCHEDULE ON E-002."
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "GENERAL NOTES:",
    "page": 44,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: GENERAL NOTES:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "SPECIFIC REQUIREMENTS REGARDING MATERIALS,"
      },
      {
        "key": "2",
        "desc": "ALL OVERHEAD CONDUIT WHERE CEILING IS OPEN TO"
      },
      {
        "key": "3",
        "desc": "REFER TO MECHANICAL DRAWINGS FOR EXACT LOCATIONS OF"
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "GENERAL NOTES:",
    "page": 45,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: GENERAL NOTES:",
    "entries_sample": [
      {
        "key": "1",
        "desc": "COORDINATE WITH UTILITY PROVIDER FOR ALL REQUIREMENTS"
      },
      {
        "key": "2",
        "desc": "COORDINATE FIRE PUMP SERVICE CONDUCTOR SIZES WITH"
      },
      {
        "key": "3",
        "desc": "ALL CONDUCTOR SIZES ARE BASED ON COPPER. CONTRACTOR"
      },
      {
        "key": "4",
        "desc": "SEE GROUNDING DETAIL 2/E-401 FOR ADDITIONAL"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:",
    "page": 45,
    "entry_count": 16,
    "confidence": 0.7,
    "source": "legend: NOTES:",
    "entries_sample": [
      {
        "key": "22.0",
        "desc": "MCA"
      },
      {
        "key": "34.0",
        "desc": "MCA"
      },
      {
        "key": "34.0",
        "desc": "MCA"
      },
      {
        "key": "5",
        "desc": "HP (x2)"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "\u0394\nDESCRIPTION\nDATE\nELECTRICAL-MECHANICAL EQUIPMENT CONNECTION SCHEDULE",
    "page": 45,
    "entry_count": 19,
    "confidence": 0.7,
    "source": "legend: \u0394\nDESCRIPTION\nDATE\nELECTRICAL-MECHANICAL",
    "entries_sample": [
      {
        "key": "22.0",
        "desc": "MCA"
      },
      {
        "key": "34.0",
        "desc": "MCA"
      },
      {
        "key": "34.0",
        "desc": "MCA"
      },
      {
        "key": "5",
        "desc": "HP (x2)"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      }
    ]
  },
  {
    "type": "roof_notes",
    "title": "ITEM#\nDESCRIPTION\nWIRING\nVOLTAGE/PHASE\nHP/FLA/KW\nPANEL\nCIRCUIT #\nDISCONNECT/FUSE",
    "page": 45,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: ITEM#\nDESCRIPTION\nWIRING\nVOLTAGE/PHASE\nH",
    "entries_sample": [
      {
        "key": "1",
        "desc": "INSTALL OVERCURRENT PROTECTION AND BRANCH CIRCUITS PER UL LISTED REQUIREMENTS FO"
      },
      {
        "key": "2",
        "desc": "PROVIDE WP DEVICES (NEMA 3R RATING) IN ALL EXTERIOR OR DAMP LOCATIONS."
      },
      {
        "key": "3",
        "desc": "DISCONNECT PROVIDED WITH EQUIPMENT OR BY MECHANICAL/PLUMBING CONTRACTOR."
      },
      {
        "key": "4",
        "desc": "PROVIDE WEATHER PROOF DUPLEX RECEPTACLE WITH IN-USE COVER ON ROOF PER REQUIREMEN"
      },
      {
        "key": "5",
        "desc": "INDOOR UNIT POWERED BY OUTDOOR UNIT."
      },
      {
        "key": "22.0",
        "desc": "MCA"
      },
      {
        "key": "34.0",
        "desc": "MCA"
      },
      {
        "key": "5.9",
        "desc": "MCA"
      },
      {
        "key": "1.0",
        "desc": "MCA"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "MECHANICAL EQUIPMENT ELECTRICAL CONNECTION SCHEDULE NOTES:",
    "page": 45,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: MECHANICAL EQUIPMENT ELECTRICAL CONNECTI",
    "entries_sample": [
      {
        "key": "1",
        "desc": "INSTALL OVERCURRENT PROTECTION AND BRANCH CIRCUITS PER UL LISTED REQUIREMENTS FO"
      },
      {
        "key": "2",
        "desc": "PROVIDE WP DEVICES (NEMA 3R RATING) IN ALL EXTERIOR OR DAMP LOCATIONS."
      },
      {
        "key": "3",
        "desc": "DISCONNECT PROVIDED WITH EQUIPMENT OR BY MECHANICAL/PLUMBING CONTRACTOR."
      },
      {
        "key": "4",
        "desc": "PROVIDE WEATHER PROOF DUPLEX RECEPTACLE WITH IN-USE COVER ON ROOF PER REQUIREMEN"
      },
      {
        "key": "5",
        "desc": "INDOOR UNIT POWERED BY OUTDOOR UNIT."
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "FIRE PUMP ROOM 09 ELECRICAL ROOM 08 TL1A\nNEUTRAL BUS IN SERVICE EQUIPMENT 30 KVA",
    "page": 45,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "\u0394 DESCRIPTION DATE"
      },
      {
        "key": "",
        "desc": "CHECKED BY DRAWN BY\nCBC MD\nSHEET NAME\nELECTRICAL\nRISER &\nSCHEDULES\nSHEET NUMBER "
      }
    ]
  },
  {
    "type": "notes",
    "title": "SEE GROUNDING DETAIL 2/E- 401 FOR ADDITIONAL",
    "page": 45,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "INFORMATION ON SERVI",
        "desc": ""
      },
      {
        "key": "DISCONNECT SWITCH AN",
        "desc": ""
      }
    ]
  },
  {
    "type": "notes",
    "title": "Branch Panel: H1A\nSUPPLY FROM: VOLTS: 480/277 Wye A.I.C. RATING: 42000\nMOUNTING:",
    "page": 45,
    "entry_count": 31,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "CKT",
        "desc": "CIRCUIT DESCRIPTION TRIP POL... A B C POL... TRIP CIRCUIT DESCRIPTION CKT"
      },
      {
        "key": "1",
        "desc": "STUMBLE LIGHTING 20 1 1047 5013 3 25 BOOSTER PUMP (DBP-1) 2"
      },
      {
        "key": "3",
        "desc": "STUMBLE LIGHTING 20 1 1047 5013 -- -- -- 4"
      },
      {
        "key": "5",
        "desc": "ELEC/PUMP ROOM LIGHTING 20 1 246 5013 -- -- -- 6"
      },
      {
        "key": "7",
        "desc": "EXHAUST FAN (EF-1) 15 3 1634 1234 3 20 JOCKEY PUMP (JP-1) 8"
      },
      {
        "key": "9",
        "desc": "-- -- -- 1634 1234 -- -- -- 10"
      },
      {
        "key": "11",
        "desc": "-- -- -- 1634 1234 -- -- -- 12"
      },
      {
        "key": "13",
        "desc": "EXHAUST FAN (EF-2) 15 3 1634 1634 3 15 EXHAUST FAN (EF-5) 14"
      },
      {
        "key": "15",
        "desc": "-- -- -- 1634 1634 -- -- -- 16"
      },
      {
        "key": "17",
        "desc": "-- -- -- 1634 1634 -- -- -- 18"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "ELECTRICAL-MECHANICAL EQUIPMENT CONNECTION SCHEDULE",
    "page": 45,
    "entry_count": 15,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "ITEM#",
        "desc": "DESCRIPTION WIRING VOLTAGE/PHASE HP/FLA/KW PANEL CIRCUIT # DISCONNECT/FUSES LOCA"
      },
      {
        "key": "CU-1",
        "desc": "OUTDOOR UNIT 2#10, #10G - 1/2\"C 208/1 22.0 MCA L1A 6,8 30A/2P/3R/NF ON ROOF 1,2,"
      },
      {
        "key": "CU-2",
        "desc": "OUTDOOR UNIT 2#6, #10G - 3/4\"C 208/1 34.0 MCA L1A 2,4 60A/2P/3R/NF ON ROOF 1,2,4"
      },
      {
        "key": "CU-3",
        "desc": "OUTDOOR UNIT 2#6, #10G - 3/4\"C 208/1 34.0 MCA L1A 7,9 60A/2P/3R/NF ON ROOF 1,2,4"
      },
      {
        "key": "DBP-1",
        "desc": "BOOSTER PUMP 3#10, #10G - 1/2\"C 480/3 5 HP (x2) H1A 2,4,6 NOTE 3 FIRE PUMP ROOM "
      },
      {
        "key": "EF-1",
        "desc": "ROOFTOP EXHAUST FAN 3#12, #12G - 1/2\"C 480/3 5.9 MCA H1A 7,9,11 30A/3P/3R/NF ON "
      },
      {
        "key": "EF-2",
        "desc": "ROOFTOP EXHAUST FAN 3#12, #12G - 1/2\"C 480/3 5.9 MCA H1A 13,15,17 30A/3P/3R/NF O"
      },
      {
        "key": "EF-3",
        "desc": "ROOFTOP EXHAUST FAN 3#12, #12G - 1/2\"C 480/3 5.9 MCA H1A 19,21,23 30A/3P/3R/NF O"
      },
      {
        "key": "EF-4",
        "desc": "ROOFTOP EXHAUST FAN 3#12, #12G - 1/2\"C 480/3 5.9 MCA H1A 25,27,29 30A/3P/3R/NF O"
      },
      {
        "key": "EF-5",
        "desc": "ROOFTOP EXHAUST FAN 3#12, #12G - 1/2\"C 480/3 5.9 MCA H1A 14,16,18 30A/3P/3R/NF O"
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "S-100\nGENERAL NOTES",
    "page": 46,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: S-100\nGENERAL NOTES",
    "entries_sample": [
      {
        "key": "51",
        "desc": "- MECHANICAL"
      },
      {
        "key": "61",
        "desc": "- PLUMBING"
      },
      {
        "key": "81",
        "desc": "- ELECTRICAL"
      }
    ]
  },
  {
    "type": "legend",
    "title": "GRAPHIC LEGEND",
    "page": 47,
    "entry_count": 7,
    "confidence": 0.7,
    "source": "legend: GRAPHIC LEGEND",
    "entries_sample": [
      {
        "key": "05",
        "desc": "= 1/2 HOUR"
      },
      {
        "key": "1",
        "desc": "= 1 HOUR"
      },
      {
        "key": "2",
        "desc": "= 2 HOUR"
      },
      {
        "key": "3",
        "desc": "= 3 HOUR"
      },
      {
        "key": "4",
        "desc": "= 4 HOUR"
      },
      {
        "key": "300",
        "desc": "GSF"
      },
      {
        "key": "000",
        "desc": "SF"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:\n1.  DO NOT OVERLAP THE FLANGES FROM ADJACENT PIPE FLASHINGS\n2.  ANY SEAM ",
    "page": 53,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES:\n1.  DO NOT OVERLAP THE FLANGES FR",
    "entries_sample": [
      {
        "key": "1",
        "desc": "WITH MECHANICALLY FASTENED SPEC, MEMBRANE MUST BE MECHANICALLY ATTACHED WITH T.P"
      },
      {
        "key": "2",
        "desc": "DO NOT OVERLAP THE FLANGES FROM ADJACENT PIPE FLASHINGS."
      },
      {
        "key": "3",
        "desc": "15 YEAR AND 20 YEAR GUARANTEES REQUIRE DOUBLE WRAP."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "STOREFRONT SCHEDULE",
    "page": 56,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: STOREFRONT SCHEDULE",
    "entries_sample": [
      {
        "key": "152.00",
        "desc": "SF"
      },
      {
        "key": "152.00",
        "desc": "SF"
      },
      {
        "key": "49.00",
        "desc": "SF"
      },
      {
        "key": "95.00",
        "desc": "SF"
      },
      {
        "key": "114.00",
        "desc": "SF"
      },
      {
        "key": "45.00",
        "desc": "SF"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "ANCHORS AND PROXIMITY OF ANCHORS TO EDGE OF CONCRETE. \nINSTALL ANCHORS IN ACCORD",
    "page": 58,
    "entry_count": 14,
    "confidence": 0.7,
    "source": "legend: ANCHORS AND PROXIMITY OF ANCHORS TO EDGE",
    "entries_sample": [
      {
        "key": "1",
        "desc": "CONTRACTOR REVIEW THE EXISTING STRUCTURAL DRAWINGS AND"
      },
      {
        "key": "1",
        "desc": "PROVIDE CALCULATIONS THAT ARE PREPARED & SEALED BY A"
      },
      {
        "key": "2",
        "desc": "PROVIDE CALCULATIONS THAT DEMONSTRATE THE SUBSTITUTED"
      },
      {
        "key": "3",
        "desc": "INCLUDE CONSIDERATION OF CREEP, IN-SERVICE TEMPERATURE AND"
      },
      {
        "key": "4",
        "desc": "EVALUATION OF SUBSTITUTIONS WILL BE BASED ON THEIR HAVING AN ICC"
      },
      {
        "key": "2",
        "desc": "CONCRETE ANCHORS"
      },
      {
        "key": "1",
        "desc": "HILTI KWIK BOLT-TZ EXPANSION ANCHORS (ICC ESR-1917)"
      },
      {
        "key": "2",
        "desc": "HILTI KWIK HUS-EZ AND KWIK HUS EZ-I SCREW ANCHORS (ICC ESR-3027)"
      },
      {
        "key": "3",
        "desc": "SIMPSON STRONG-TIE \u201cTITEN-HD\u201d SCREW ANCHORS (ICC ESR-2713)"
      },
      {
        "key": "4",
        "desc": "SIMPSON STRONG-TIE \u201cSTRONG-BOLT 2\u201d EXPANSION ANCHORS (ICC"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "UNDERTAKE TO LOCATE THE POSITION OF MATERIAL EMBEDDED IN THE \nCONCRETE AT THE LO",
    "page": 58,
    "entry_count": 17,
    "confidence": 0.7,
    "source": "legend: UNDERTAKE TO LOCATE THE POSITION OF MATE",
    "entries_sample": [
      {
        "key": "1",
        "desc": "PROVIDE CALCULATIONS THAT ARE PREPARED & SEALED BY A"
      },
      {
        "key": "2",
        "desc": "PROVIDE CALCULATIONS THAT DEMONSTRATE THE SUBSTITUTED"
      },
      {
        "key": "3",
        "desc": "INCLUDE CONSIDERATION OF CREEP, IN-SERVICE TEMPERATURE AND"
      },
      {
        "key": "4",
        "desc": "EVALUATION OF SUBSTITUTIONS WILL BE BASED ON THEIR HAVING AN ICC"
      },
      {
        "key": "2",
        "desc": "CONCRETE ANCHORS"
      },
      {
        "key": "1",
        "desc": "HILTI KWIK BOLT-TZ EXPANSION ANCHORS (ICC ESR-1917)"
      },
      {
        "key": "2",
        "desc": "HILTI KWIK HUS-EZ AND KWIK HUS EZ-I SCREW ANCHORS (ICC ESR-3027)"
      },
      {
        "key": "3",
        "desc": "SIMPSON STRONG-TIE \u201cTITEN-HD\u201d SCREW ANCHORS (ICC ESR-2713)"
      },
      {
        "key": "4",
        "desc": "SIMPSON STRONG-TIE \u201cSTRONG-BOLT 2\u201d EXPANSION ANCHORS (ICC"
      },
      {
        "key": "5",
        "desc": "DEWALT / POWERS POWER-STUD + SD2 EXPANSION ANCHORS (ICC ESR"
      }
    ]
  },
  {
    "type": "general_notes",
    "title": "ELECTRICAL, PLUMBING, AND CIVIL DRAWINGS.  NOTIFY STRUCTURAL ENGINEER OF \nANY CO",
    "page": 58,
    "entry_count": 13,
    "confidence": 0.7,
    "source": "legend: ELECTRICAL, PLUMBING, AND CIVIL DRAWINGS",
    "entries_sample": [
      {
        "key": "12",
        "desc": "CONTRACT DOCUMENTS SHALL GOVERN IN THE EVENT OF A CONFLICT WITH THE"
      },
      {
        "key": "13",
        "desc": "ELECTRONIC DRAWING FILES WILL NOT BE PROVIDED TO THE CONTRACTOR."
      },
      {
        "key": "14",
        "desc": "STRUCTURAL ENGINEER IS NOT RESPONSIBLE FOR THE DESIGN OF STEEL STAIRS,"
      },
      {
        "key": "15",
        "desc": "IT IS EXPECTED THAT THE GENERAL CONTRACTOR IS EXPERIENCED IN THE TYPE OF"
      },
      {
        "key": "16",
        "desc": "PROVIDE CONTINGENCY FOR REPAIRING 2700 LINEAR FEET OF CRACKS IN THE FLOOR"
      },
      {
        "key": "17",
        "desc": "SPECIAL INSPECTIONS SHALL BE IN ACCORDANCE WITH CHAPTER 17 OF THE"
      },
      {
        "key": "18",
        "desc": "INSPECTION REPORTS SHALL BE FURNISHED TO THE BUILDING OFFICIAL, ARCHITECT"
      },
      {
        "key": "19",
        "desc": "SPECIAL INSPECTOR SHALL SUBMIT A FINAL REPORT STATING THAT THE STRUCTURAL"
      },
      {
        "key": "20",
        "desc": "CONTRACTOR HAS SOLE RESPONSIBILITY FOR MEANS, METHODS, SAFETY,"
      },
      {
        "key": "21",
        "desc": "THE STRUCTURE IS STABLE ONLY IN ITS COMPLETED FORM.  TEMPORARY SUPPORTS"
      }
    ]
  },
  {
    "type": "material_notes",
    "title": "CONSTRUCTION REQUIRED; THEREFORE IT IS EXPECTED THAT THE GENERAL \nCONTRACTOR WIL",
    "page": 58,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: CONSTRUCTION REQUIRED; THEREFORE IT IS E",
    "entries_sample": [
      {
        "key": "17",
        "desc": "SPECIAL INSPECTIONS SHALL BE IN ACCORDANCE WITH CHAPTER 17 OF THE"
      },
      {
        "key": "18",
        "desc": "INSPECTION REPORTS SHALL BE FURNISHED TO THE BUILDING OFFICIAL, ARCHITECT"
      },
      {
        "key": "19",
        "desc": "SPECIAL INSPECTOR SHALL SUBMIT A FINAL REPORT STATING THAT THE STRUCTURAL"
      },
      {
        "key": "20",
        "desc": "CONTRACTOR HAS SOLE RESPONSIBILITY FOR MEANS, METHODS, SAFETY,"
      },
      {
        "key": "21",
        "desc": "THE STRUCTURE IS STABLE ONLY IN ITS COMPLETED FORM.  TEMPORARY SUPPORTS"
      },
      {
        "key": "22",
        "desc": "CONTRACTOR SHALL SUBMIT SHOP DRAWINGS WITH EDGE OF SLAB DIMENSIONS,"
      },
      {
        "key": "23",
        "desc": "STRUCTURAL DOCUMENTS ARE BEING RELEASED PRIOR TO DOCUMENTS BY OTHER"
      },
      {
        "key": "1",
        "desc": "THE DESIGN SOIL BEARING PRESSURE IS 2000 PSF FOR COLUMN FOOTINGS AND WALL"
      },
      {
        "key": "16",
        "desc": "PROVIDE CONTINGENCY FOR REPAIRING 2700 LINEAR FEET OF CRACKS IN THE FLOOR"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "CONCRETE MIXTURE SCHEDULE",
    "page": 58,
    "entry_count": 21,
    "confidence": 0.7,
    "source": "legend: CONCRETE MIXTURE SCHEDULE",
    "entries_sample": [
      {
        "key": "3000",
        "desc": "PSI"
      },
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "150",
        "desc": "PCF"
      },
      {
        "key": "4000",
        "desc": "PSI AT 28-DAYS"
      },
      {
        "key": "4500",
        "desc": "PSI AT 56-DAYS"
      },
      {
        "key": "0",
        "desc": "45"
      },
      {
        "key": "4",
        "desc": "5% \u00b1 1.5%"
      },
      {
        "key": "150",
        "desc": "PCF"
      },
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "1",
        "desc": "1/2\""
      }
    ]
  },
  "... (65 more items truncated for artifact readability)"
]
```

## §6 — Per-Page Errors (if any)

- Pages where module raised: 0
- Pages with module attempt: 91
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

- Observed: roofing module produced 769 `fields` entries across 91 pages with non-empty output (of 91 pages attempted), with 0 warnings and 0 equipment_pins.
- Observed: glazing module produced 177 glazing_items, 31 door_items, 24 storefront_items across 58 pages with non-empty output (of 91 pages attempted).
- Observed: dispatch project_scope detected_system = `None` with confidence `0.0`; scope_pages = `[]`; manufacturers = `[]`.
- Observed: debug section 6 emitted 145 legend entries and 1 legend quality flags.
- Observed: per-page module error rate roofing=0.00%, glazing=0.00% (§7 stop threshold = 25%; soft-observation band = 5–25%).

---

**End of report.** Vault rule active on `roofing_module.py`,
`roofing_vocabulary.py`, `glazing_module.py`, `glazing_vocabulary.py`,
and `debug_module.py`. The sweep modified zero `backend/core/` files
and added zero dependencies. This report is a descriptive artifact
for the future tuning planning conversation per Daniel's directive
2026-04-28 (PROJECT_CLAUDE.md §3).
