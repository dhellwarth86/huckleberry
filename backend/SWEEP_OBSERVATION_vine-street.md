# Sweep Observation Report — Vine Street Retail Center — Kissimmee — Great Southern Constructors

**Date:** 2026-04-28
**Phase:** Three-bidset sweep (post-C.3c-build, post-C.5; modules vault-ruled)
**Bidset short name:** `vine-street`
**Bidset file:** `C:\huck stage 2\full bid sets\Vine Street Retail Center - Kissimmee - Great Southern Constructors.pdf`
**Page count:** 138
**File size:** 80,836,373 bytes (~77.1 MB)
**Wall-clock dispatch time:** 82.0s
**Wall-clock per-page module time (roofing+glazing combined):** 654.6s
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

- Display name: Vine Street Retail Center — Kissimmee — Great Southern Constructors
- Short name: `vine-street`
- Filename: `Vine Street Retail Center - Kissimmee - Great Southern Constructors.pdf`
- Full path: `C:\huck stage 2\full bid sets\Vine Street Retail Center - Kissimmee - Great Southern Constructors.pdf`
- Page count: 138
- File size: 80,836,373 bytes (77.1 MB)
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
### dispatch_warnings: `['Filter 4 quality gate: 8 of 54 legends removed (46 kept)']`
### total_pages: `138`
### sheet_count: `44`
### mapped_pages: `35`
### sheet_map_source: `drawing_index`

## §3 — Roofing Module Output

### Aggregated

- Total `fields` entries across all pages: 1201
- Total warnings: 0
- Total equipment_pins: 0
- Pages with non-empty output: 138
- Pages with empty output: 0

### Per-page summary (only pages with non-empty output shown)

| Page | Sheet | Fields | Warnings | Equip pins |
|---:|---|---:|---:|---:|
| 0 | G-0.0 | 8 | 0 | 0 |
| 1 | G-0.1 | 8 | 0 | 0 |
| 2 | G-2.0 | 10 | 0 | 0 |
| 3 | --- | 8 | 0 | 0 |
| 4 | A-2.4 | 8 | 0 | 0 |
| 5 | G-4.0 | 11 | 0 | 0 |
| 6 | G-5.0 | 8 | 0 | 0 |
| 7 | A-0.1 | 8 | 0 | 0 |
| 8 | A-1.0 | 8 | 0 | 0 |
| 9 | A-1.1 | 8 | 0 | 0 |
| 10 | A-1.2 | 11 | 0 | 0 |
| 11 | A-1.3 | 12 | 0 | 0 |
| 12 | --- | 9 | 0 | 0 |
| 13 | A-2.2 | 10 | 0 | 0 |
| 14 | A-2.3 | 10 | 0 | 0 |
| 15 | --- | 10 | 0 | 0 |
| 16 | A-3.0 | 9 | 0 | 0 |
| 17 | A-4.0 | 9 | 0 | 0 |
| 18 | S-0.1 | 9 | 0 | 0 |
| 19 | S-0.2 | 8 | 0 | 0 |
| 20 | S-0.3 | 8 | 0 | 0 |
| 21 | A1 | 9 | 0 | 0 |
| 22 | S-2.0 | 8 | 0 | 0 |
| 23 | S-3.0 | 8 | 0 | 0 |
| 24 | S-4.0 | 8 | 0 | 0 |
| 25 | E-0.0 | 10 | 0 | 0 |
| 26 | E-1.0 | 8 | 0 | 0 |
| 27 | E-2.0 | 9 | 0 | 0 |
| 28 | E-3.0 | 8 | 0 | 0 |
| 29 | P-0.1 | 8 | 0 | 0 |
| 30 | P-0.2 | 11 | 0 | 0 |
| 31 | P-1.0 | 8 | 0 | 0 |
| 32 | P-2.0 | 8 | 0 | 0 |
| 33 | P-3.0 | 8 | 0 | 0 |
| 34 | P-4.0 | 11 | 0 | 0 |
| 35 | M-1.0 | 8 | 0 | 0 |
| 36 | --- | 8 | 0 | 0 |
| 37 | --- | 8 | 0 | 0 |
| 38 | --- | 8 | 0 | 0 |
| 39 | --- | 8 | 0 | 0 |
| 40 | --- | 8 | 0 | 0 |
| 41 | --- | 8 | 0 | 0 |
| 42 | --- | 8 | 0 | 0 |
| 43 | --- | 8 | 0 | 0 |
| 44 | --- | 8 | 0 | 0 |
| 45 | --- | 8 | 0 | 0 |
| 46 | --- | 8 | 0 | 0 |
| 47 | --- | 8 | 0 | 0 |
| 48 | --- | 8 | 0 | 0 |
| 49 | --- | 8 | 0 | 0 |
| 50 | --- | 8 | 0 | 0 |
| 51 | --- | 8 | 0 | 0 |
| 52 | --- | 8 | 0 | 0 |
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
| 65 | --- | 8 | 0 | 0 |
| 66 | --- | 8 | 0 | 0 |
| 67 | --- | 8 | 0 | 0 |
| 68 | --- | 8 | 0 | 0 |
| 69 | --- | 8 | 0 | 0 |
| 70 | --- | 10 | 0 | 0 |
| 71 | --- | 8 | 0 | 0 |
| 72 | --- | 8 | 0 | 0 |
| 73 | --- | 11 | 0 | 0 |
| 74 | --- | 8 | 0 | 0 |
| 75 | --- | 8 | 0 | 0 |
| 76 | --- | 9 | 0 | 0 |
| 77 | --- | 11 | 0 | 0 |
| 78 | A-1.4 | 11 | 0 | 0 |
| 79 | --- | 9 | 0 | 0 |
| 80 | A-2.1 | 10 | 0 | 0 |
| 81 | --- | 10 | 0 | 0 |
| 82 | --- | 10 | 0 | 0 |
| 83 | --- | 9 | 0 | 0 |
| 84 | --- | 9 | 0 | 0 |
| 85 | --- | 8 | 0 | 0 |
| 86 | --- | 8 | 0 | 0 |
| 87 | --- | 9 | 0 | 0 |
| 88 | --- | 8 | 0 | 0 |
| 89 | --- | 8 | 0 | 0 |
| 90 | --- | 8 | 0 | 0 |
| 91 | --- | 10 | 0 | 0 |
| 92 | --- | 8 | 0 | 0 |
| 93 | --- | 9 | 0 | 0 |
| 94 | --- | 9 | 0 | 0 |
| 95 | --- | 8 | 0 | 0 |
| 96 | --- | 11 | 0 | 0 |
| 97 | --- | 8 | 0 | 0 |
| 98 | --- | 8 | 0 | 0 |
| 99 | --- | 8 | 0 | 0 |
| 100 | --- | 11 | 0 | 0 |
| 101 | --- | 8 | 0 | 0 |
| 102 | --- | 8 | 0 | 0 |
| 103 | --- | 8 | 0 | 0 |
| 104 | --- | 10 | 0 | 0 |
| 105 | --- | 8 | 0 | 0 |
| 106 | --- | 8 | 0 | 0 |
| 107 | --- | 11 | 0 | 0 |
| 108 | --- | 8 | 0 | 0 |
| 109 | --- | 8 | 0 | 0 |
| 110 | --- | 8 | 0 | 0 |
| 111 | --- | 8 | 0 | 0 |
| 112 | --- | 11 | 0 | 0 |
| 113 | --- | 12 | 0 | 0 |
| 114 | --- | 9 | 0 | 0 |
| 115 | --- | 10 | 0 | 0 |
| 116 | --- | 10 | 0 | 0 |
| 117 | --- | 10 | 0 | 0 |
| 118 | --- | 9 | 0 | 0 |
| 119 | --- | 9 | 0 | 0 |
| 120 | --- | 9 | 0 | 0 |
| 121 | --- | 8 | 0 | 0 |
| 122 | --- | 8 | 0 | 0 |
| 123 | --- | 9 | 0 | 0 |
| 124 | --- | 8 | 0 | 0 |
| 125 | --- | 8 | 0 | 0 |
| 126 | --- | 8 | 0 | 0 |
| 127 | --- | 10 | 0 | 0 |
| 128 | --- | 8 | 0 | 0 |
| 129 | --- | 9 | 0 | 0 |
| 130 | --- | 9 | 0 | 0 |
| 131 | --- | 8 | 0 | 0 |
| 132 | --- | 11 | 0 | 0 |
| 133 | --- | 8 | 0 | 0 |
| 134 | --- | 8 | 0 | 0 |
| 135 | --- | 8 | 0 | 0 |
| 136 | --- | 11 | 0 | 0 |
| 137 | --- | 8 | 0 | 0 |

### Per-page detail (only pages with non-empty output)

#### Page 0 (sheet `G-0.0`)

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

#### Page 1 (sheet `G-0.1`)

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

#### Page 2 (sheet `G-2.0`)

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

#### Page 4 (sheet `A-2.4`)

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

#### Page 5 (sheet `G-4.0`)

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
    "gutter": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Gutters",
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

#### Page 6 (sheet `G-5.0`)

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

#### Page 7 (sheet `A-0.1`)

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

#### Page 8 (sheet `A-1.0`)

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

#### Page 9 (sheet `A-1.1`)

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

#### Page 10 (sheet `A-1.2`)

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
    "trim": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Trim",
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

#### Page 11 (sheet `A-1.3`)

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

#### Page 13 (sheet `A-2.2`)

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
    "_scope": {
      "value": "TPO Single Ply",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'THERMOPLASTIC'",
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

#### Page 14 (sheet `A-2.3`)

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
    "_scope": {
      "value": "TPO Single Ply",
      "confidence": 0.7,
      "source": "auto_legend",
      "evidence": "interior callout 'THERMOPLASTIC'",
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

#### Page 16 (sheet `A-3.0`)

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

#### Page 17 (sheet `A-4.0`)

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
      "evidence": "interior callout 'THERMOPLASTIC'",
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

#### Page 18 (sheet `S-0.1`)

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
    "walkway_pads": {
      "value": null,
      "confidence": 0.0,
      "source": "manual_needed",
      "evidence": "detected in scope \u2014 enter quantity manually",
      "display_name": "Walkway Pads",
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

#### Page 19 (sheet `S-0.2`)

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

#### Page 20 (sheet `S-0.3`)

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

#### Page 21 (sheet `A1`)

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

#### Page 22 (sheet `S-2.0`)

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

#### Page 23 (sheet `S-3.0`)

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

#### Page 24 (sheet `S-4.0`)

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

#### Page 25 (sheet `E-0.0`)

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
      "evidence": "interior callout 'THERMOPLASTIC'",
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

#### Page 26 (sheet `E-1.0`)

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

#### Page 27 (sheet `E-2.0`)

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
      "confidence": 0.9,
      "source": "auto_legend",
      "evidence": "legend match 'THERMOPLASTIC'",
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

#### Page 28 (sheet `E-3.0`)

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

#### Page 29 (sheet `P-0.1`)

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

#### Page 30 (sheet `P-0.2`)

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

#### Page 31 (sheet `P-1.0`)

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

#### Page 32 (sheet `P-2.0`)

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

#### Page 33 (sheet `P-3.0`)

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

#### Page 34 (sheet `P-4.0`)

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

#### Page 35 (sheet `M-1.0`)

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

#### Page 36 (sheet `---`)

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

#### Page 37 (sheet `---`)

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

#### Page 40 (sheet `---`)

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

#### Page 41 (sheet `---`)

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

*(78 more non-empty roofing pages truncated for artifact size)*

## §4 — Glazing Module Output

### Aggregated

- Total glazing_items across all pages: 100
- Total door_items: 12
- Total storefront_items: 23
- Pages with any glazing module content (any of the three lists non-empty): 47
- Pages with empty output: 91

### Per-page summary (only pages with non-empty output shown)

| Page | Sheet | glazing_items | door_items | storefront_items |
|---:|---|---:|---:|---:|
| 2 | G-2.0 | 1 | 0 | 0 |
| 3 | --- | 10 | 0 | 5 |
| 4 | A-2.4 | 0 | 3 | 0 |
| 8 | A-1.0 | 1 | 0 | 3 |
| 9 | A-1.1 | 0 | 2 | 0 |
| 16 | A-3.0 | 2 | 0 | 0 |
| 17 | A-4.0 | 1 | 0 | 0 |
| 18 | S-0.1 | 2 | 0 | 1 |
| 20 | S-0.3 | 1 | 0 | 0 |
| 26 | E-1.0 | 2 | 0 | 0 |
| 27 | E-2.0 | 1 | 0 | 0 |
| 28 | E-3.0 | 8 | 0 | 0 |
| 29 | P-0.1 | 1 | 0 | 0 |
| 30 | P-0.2 | 1 | 1 | 0 |
| 31 | P-1.0 | 7 | 0 | 0 |
| 34 | P-4.0 | 1 | 0 | 0 |
| 69 | --- | 0 | 0 | 1 |
| 70 | --- | 0 | 1 | 0 |
| 71 | --- | 7 | 0 | 1 |
| 74 | --- | 1 | 0 | 0 |
| 76 | --- | 0 | 2 | 0 |
| 83 | --- | 1 | 0 | 0 |
| 84 | --- | 2 | 0 | 3 |
| 86 | --- | 1 | 0 | 0 |
| 88 | --- | 1 | 0 | 0 |
| 92 | --- | 3 | 0 | 0 |
| 93 | --- | 1 | 0 | 0 |
| 95 | --- | 3 | 0 | 0 |
| 96 | --- | 2 | 0 | 0 |
| 100 | --- | 1 | 0 | 0 |
| 103 | --- | 1 | 0 | 1 |
| 104 | --- | 1 | 0 | 0 |
| 105 | --- | 10 | 0 | 3 |
| 110 | --- | 0 | 0 | 3 |
| 111 | --- | 0 | 2 | 0 |
| 118 | --- | 2 | 0 | 0 |
| 119 | --- | 1 | 0 | 0 |
| 120 | --- | 2 | 0 | 2 |
| 122 | --- | 1 | 0 | 0 |
| 124 | --- | 9 | 0 | 0 |
| 128 | --- | 3 | 0 | 0 |
| 129 | --- | 1 | 0 | 0 |
| 130 | --- | 1 | 0 | 0 |
| 131 | --- | 3 | 0 | 0 |
| 132 | --- | 1 | 1 | 0 |
| 133 | --- | 1 | 0 | 0 |
| 136 | --- | 1 | 0 | 0 |

### Per-page detail (only pages with non-empty output)

#### Page 2 (sheet `G-2.0`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 1 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "D-1010",
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

#### Page 3 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 10 window / 0 door / 5 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "15 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
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
    },
    {
      "mark": "160",
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
      "mark": "180",
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
    },
    {
      "mark": "D-164",
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
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 75.0,
      "height_ft": 100.0,
      "sqft": 7500.0,
      "location": "",
      "source_page": 3,
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
  "storefront_items": [
    {
      "mark": "SF-60",
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
      "source_page": 3,
      "confidence": 0.3
    },
    {
      "mark": "SF-60",
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
      "source_page": 3,
      "confidence": 0.3
    },
    {
      "mark": "SF-60",
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
      "source_page": 3,
      "confidence": 0.3
    },
    {
      "mark": "SF-60",
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
      "source_page": 3,
      "confidence": 0.3
    },
    {
      "mark": "SF-60",
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
      "source_page": 3,
      "confidence": 0.3
    }
  ]
}
```

#### Page 4 (sheet `A-2.4`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 3 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "3 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [
    {
      "mark": "100",
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
      "source_page": 4,
      "confidence": 0.5
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
      "source_page": 4,
      "confidence": 0.2
    },
    {
      "mark": "DOOR-IN",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": 3.0,
      "height_ft": 7.0,
      "source_page": 4,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 8 (sheet `A-1.0`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 3 storefront items",
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
      "mark": "D-1010",
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
      "width_ft": 7.5,
      "height_ft": null,
      "source_page": 8,
      "confidence": 0.3
    },
    {
      "mark": "101",
      "count": 0,
      "system_type": "curtain_wall_captured",
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": 7.5,
      "height_ft": null,
      "source_page": 8,
      "confidence": 0.4
    },
    {
      "mark": "101",
      "count": 0,
      "system_type": "curtain_wall_captured",
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": 7.5,
      "height_ft": null,
      "source_page": 8,
      "confidence": 0.4
    }
  ]
}
```

#### Page 9 (sheet `A-1.1`)

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
      "mark": "DOOR-LEAF",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": 75.0,
      "height_ft": 36.0,
      "source_page": 9,
      "confidence": 0.2
    },
    {
      "mark": "DOOR-WAY",
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
      "source_page": 9,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 16 (sheet `A-3.0`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 2 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "2 schedule rows parsed; 2 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "165",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 16,
      "confidence": 0.2
    },
    {
      "mark": "W-1",
      "count": 2,
      "system": "interior_office_front",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 16,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 17 (sheet `A-4.0`)

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
      "mark": "W-RG",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
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

#### Page 18 (sheet `S-0.1`)

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
      "mark": "W-C",
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
    },
    {
      "mark": "124",
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
  "storefront_items": [
    {
      "mark": "SF-100",
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
      "source_page": 18,
      "confidence": 0.3
    }
  ]
}
```

#### Page 20 (sheet `S-0.3`)

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
      "source_page": 20,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 26 (sheet `E-1.0`)

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
      "mark": "120",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 26,
      "confidence": 0.4
    },
    {
      "mark": "W-WIRE",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 26,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 27 (sheet `E-2.0`)

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
      "mark": "W-RG",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 27,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 28 (sheet `E-3.0`)

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
      "source_page": 28,
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
      "source_page": 28,
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
      "source_page": 28,
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
      "source_page": 28,
      "confidence": 0.4
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
      "source_page": 28,
      "confidence": 0.4
    },
    {
      "mark": "125",
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
      "source_page": 28,
      "confidence": 0.2
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 75.0,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 28,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 29 (sheet `P-0.1`)

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
      "mark": "W-M",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 29,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 30 (sheet `P-0.2`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 1 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "2 schedule rows parsed; 1 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "W-1",
      "count": 1,
      "system": "interior_office_front",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 30,
      "confidence": 0.4
    }
  ],
  "door_items": [
    {
      "mark": "DOOR-B65",
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
      "source_page": 30,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 31 (sheet `P-1.0`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 7 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "7 schedule rows parsed; 7 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "W-1",
      "count": 7,
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
      "mark": "W-1",
      "count": 7,
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
      "mark": "W-1",
      "count": 7,
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
      "mark": "W-1",
      "count": 7,
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
      "mark": "W-1",
      "count": 7,
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
      "mark": "W-1",
      "count": 7,
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
      "mark": "W-1",
      "count": 7,
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

#### Page 34 (sheet `P-4.0`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 1 elevation marks counted",
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
      "source_page": 34,
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
      "mark": "W-N",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": 2525.0,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": 50.0,
      "height_ft": 50.5,
      "source_page": 69,
      "confidence": 0.3
    }
  ]
}
```

#### Page 70 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 1 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 1 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [],
  "door_items": [
    {
      "mark": "D-2",
      "count": 1,
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
      "source_page": 70,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 71 (sheet `---`)

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
      "source_page": 71,
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
      "source_page": 71,
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
      "source_page": 71,
      "confidence": 0.2
    },
    {
      "mark": "D-164",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 71,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 75.0,
      "height_ft": 100.0,
      "sqft": 7500.0,
      "location": "",
      "source_page": 71,
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
      "source_page": 71,
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
      "source_page": 71,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-FBC",
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
      "source_page": 71,
      "confidence": 0.3
    }
  ]
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
      "mark": "D-I",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 74,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 76 (sheet `---`)

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
      "mark": "DOOR-LEAF",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": 75.0,
      "height_ft": 36.0,
      "source_page": 76,
      "confidence": 0.2
    },
    {
      "mark": "DOOR-WAY",
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
      "source_page": 76,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 83 (sheet `---`)

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
      "mark": "W-RG",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
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
      "value": "Glazing scope: 2 window / 0 door / 3 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "5 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "W-C",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 84,
      "confidence": 0.2
    },
    {
      "mark": "124",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 84,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-100",
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
      "source_page": 84,
      "confidence": 0.3
    },
    {
      "mark": "SF-20",
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
      "source_page": 84,
      "confidence": 0.3
    },
    {
      "mark": "SF-100",
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
      "source_page": 84,
      "confidence": 0.3
    }
  ]
}
```

#### Page 86 (sheet `---`)

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
      "source_page": 86,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 88 (sheet `---`)

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
      "source_page": 88,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 92 (sheet `---`)

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
      "mark": "120",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 92,
      "confidence": 0.4
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 92,
      "confidence": 0.2
    },
    {
      "mark": "W-WIRE",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 92,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 93 (sheet `---`)

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
      "mark": "W-RG",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 93,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 95 (sheet `---`)

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
      "mark": "W-M",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 95,
      "confidence": 0.2
    },
    {
      "mark": "W-LP",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 95,
      "confidence": 0.2
    },
    {
      "mark": "W-M",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 95,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 96 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 2 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "2 schedule rows parsed; 2 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "W-1",
      "count": 2,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 96,
      "confidence": 0.2
    },
    {
      "mark": "W-1",
      "count": 2,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 96,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 100 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 1 elevation marks counted",
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
      "source_page": 100,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 103 (sheet `---`)

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
      "mark": "W-M",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 103,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "W-N",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": 2525.0,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": 50.0,
      "height_ft": 50.5,
      "source_page": 103,
      "confidence": 0.3
    }
  ]
}
```

#### Page 104 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 1 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "D-1010",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 104,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 105 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 10 window / 0 door / 3 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "13 schedule rows parsed; 0 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
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
      "source_page": 105,
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
      "source_page": 105,
      "confidence": 0.2
    },
    {
      "mark": "160",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 105,
      "confidence": 0.2
    },
    {
      "mark": "180",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 105,
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
      "source_page": 105,
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
      "source_page": 105,
      "confidence": 0.2
    },
    {
      "mark": "D-164",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 105,
      "confidence": 0.2
    },
    {
      "mark": "100",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 75.0,
      "height_ft": 100.0,
      "sqft": 7500.0,
      "location": "",
      "source_page": 105,
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
      "source_page": 105,
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
      "source_page": 105,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-FBC",
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
      "source_page": 105,
      "confidence": 0.3
    },
    {
      "mark": "SF-60",
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
      "source_page": 105,
      "confidence": 0.3
    },
    {
      "mark": "SF-60",
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
      "source_page": 105,
      "confidence": 0.3
    }
  ]
}
```

#### Page 110 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 0 window / 0 door / 3 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "3 schedule rows parsed; 0 elevation marks counted",
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
      "mark": "102",
      "count": 0,
      "system_type": null,
      "manufacturer": null,
      "sqft_per_segment": 400.0,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": 20.0,
      "height_ft": 20.0,
      "source_page": 110,
      "confidence": 0.3
    },
    {
      "mark": "SF-46",
      "count": 0,
      "system_type": "curtain_wall_captured",
      "manufacturer": null,
      "sqft_per_segment": 56.25,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": 7.5,
      "height_ft": 7.5,
      "source_page": 110,
      "confidence": 0.4
    },
    {
      "mark": "101",
      "count": 0,
      "system_type": "curtain_wall_captured",
      "manufacturer": null,
      "sqft_per_segment": null,
      "door_in_segment": false,
      "double_door_in_segment": false,
      "location": "",
      "finish": null,
      "width_ft": 7.5,
      "height_ft": null,
      "source_page": 110,
      "confidence": 0.4
    }
  ]
}
```

#### Page 111 (sheet `---`)

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
      "mark": "DOOR-LEAF",
      "count": 0,
      "door_type": null,
      "frame_type": null,
      "manufacturer": null,
      "door_kind": "single",
      "material": "unknown",
      "glass_door": false,
      "finish": null,
      "location": "",
      "width_ft": 75.0,
      "height_ft": 36.0,
      "source_page": 111,
      "confidence": 0.2
    },
    {
      "mark": "DOOR-WAY",
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
      "source_page": 111,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 118 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 2 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "2 schedule rows parsed; 2 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "165",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 118,
      "confidence": 0.2
    },
    {
      "mark": "W-1",
      "count": 2,
      "system": "interior_office_front",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 118,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 119 (sheet `---`)

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
      "mark": "W-RG",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 119,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 120 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 2 window / 0 door / 2 storefront items",
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
      "mark": "W-C",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 120,
      "confidence": 0.2
    },
    {
      "mark": "124",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 120,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": [
    {
      "mark": "SF-20",
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
      "source_page": 120,
      "confidence": 0.3
    },
    {
      "mark": "SF-100",
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
      "source_page": 120,
      "confidence": 0.3
    }
  ]
}
```

#### Page 122 (sheet `---`)

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
      "source_page": 122,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 124 (sheet `---`)

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
      "mark": "123",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 1.5,
      "height_ft": 2.1667,
      "sqft": 3.25,
      "location": "",
      "source_page": 124,
      "confidence": 0.2
    },
    {
      "mark": "191",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 9.1667,
      "height_ft": 10.5,
      "sqft": 96.2504,
      "location": "",
      "source_page": 124,
      "confidence": 0.2
    },
    {
      "mark": "174",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 10.0,
      "height_ft": 11.3333,
      "sqft": 113.333,
      "location": "",
      "source_page": 124,
      "confidence": 0.2
    },
    {
      "mark": "155",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 11.1667,
      "height_ft": 12.5,
      "sqft": 139.5838,
      "location": "",
      "source_page": 124,
      "confidence": 0.2
    },
    {
      "mark": "143",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 12.0,
      "height_ft": 12.6667,
      "sqft": 152.0004,
      "location": "",
      "source_page": 124,
      "confidence": 0.2
    },
    {
      "mark": "139",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 13.3333,
      "height_ft": 14.6667,
      "sqft": 195.5555,
      "location": "",
      "source_page": 124,
      "confidence": 0.2
    },
    {
      "mark": "132",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 14.0,
      "height_ft": 15.3333,
      "sqft": 214.6662,
      "location": "",
      "source_page": 124,
      "confidence": 0.2
    },
    {
      "mark": "115",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 16.0,
      "height_ft": 17.3333,
      "sqft": 277.3328,
      "location": "",
      "source_page": 124,
      "confidence": 0.2
    },
    {
      "mark": "101",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": 18.0,
      "height_ft": 19.3333,
      "sqft": 347.9994,
      "location": "",
      "source_page": 124,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 128 (sheet `---`)

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
      "mark": "120",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 128,
      "confidence": 0.4
    },
    {
      "mark": "120",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 128,
      "confidence": 0.2
    },
    {
      "mark": "W-WIRE",
      "count": 0,
      "system": "spandrel_panel",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 128,
      "confidence": 0.4
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 129 (sheet `---`)

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
      "mark": "W-RG",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": "White",
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 129,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 130 (sheet `---`)

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
      "source_page": 130,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 131 (sheet `---`)

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
      "mark": "W-M",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 131,
      "confidence": 0.2
    },
    {
      "mark": "W-WM",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 131,
      "confidence": 0.2
    },
    {
      "mark": "W-M",
      "count": 0,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 131,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 132 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 1 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "2 schedule rows parsed; 3 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "W-1",
      "count": 3,
      "system": "interior_office_front",
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 132,
      "confidence": 0.4
    }
  ],
  "door_items": [
    {
      "mark": "DOOR-B65",
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
      "source_page": 132,
      "confidence": 0.2
    }
  ],
  "storefront_items": []
}
```

#### Page 133 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 7 elevation marks counted",
      "display_name": "Glazing Scope",
      "unit": ""
    }
  },
  "warnings": [],
  "equipment_pins": [],
  "glazing_items": [
    {
      "mark": "W-1",
      "count": 7,
      "system": null,
      "glass_type": null,
      "manufacturer": null,
      "color_finish": null,
      "width_ft": null,
      "height_ft": null,
      "sqft": null,
      "location": "",
      "source_page": 133,
      "confidence": 0.2
    }
  ],
  "door_items": [],
  "storefront_items": []
}
```

#### Page 136 (sheet `---`)

```json
{
  "fields": {
    "_scope": {
      "value": "Glazing scope: 1 window / 0 door / 0 storefront items",
      "confidence": 0.5,
      "source": "auto_text",
      "evidence": "1 schedule rows parsed; 1 elevation marks counted",
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
      "source_page": 136,
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
    "Filter 4 quality gate: 8 of 54 legends removed (46 kept)"
  ],
  "warning_count": 1,
  "timestamp": "2026-04-29T03:24:28.813416+00:00",
  "total_pages": 138,
  "sheet_map_source": "drawing_index",
  "sheet_count": 44,
  "mapped_pages": 35
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
- Page entry count: 138

```json
[
  {
    "page": 0,
    "sheet": "G-0.0",
    "title": "COVER SHEET",
    "discipline": "G",
    "type": "section",
    "confidence": 0.5,
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
    "page": 1,
    "sheet": "G-0.1",
    "title": "SITE PLOT PLAN",
    "discipline": "G",
    "type": "site_plan",
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
    "page": 2,
    "sheet": "G-2.0",
    "title": "CODE ANALYSIS",
    "discipline": "G",
    "type": "roof_plan",
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
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
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
    "page": 4,
    "sheet": "A-2.4",
    "title": "EXTERIOR DETAILS AND SECTIONS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 35,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 35,
    "refs_in": 90
  },
  {
    "page": 5,
    "sheet": "G-4.0",
    "title": "WALL TYPES",
    "discipline": "G",
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
    "refs_in": 6
  },
  {
    "page": 6,
    "sheet": "G-5.0",
    "title": "UL RATINGS - 1 HOUR FIRE WALL",
    "discipline": "G",
    "type": "general_notes",
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
    "page": 7,
    "sheet": "A-0.1",
    "title": "BUILDING B SLAB PLAN",
    "discipline": "A",
    "type": "floor_plan",
    "confidence": 0.7,
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
    "page": 8,
    "sheet": "A-1.0",
    "title": "BUILDING B - NOTED FRAMING PLAN",
    "discipline": "A",
    "type": "floor_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 15,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 15,
    "refs_in": 2
  },
  {
    "page": 9,
    "sheet": "A-1.1",
    "title": "BUILDING B - LIFESAFETY PLAN/ OCCUPANCY",
    "discipline": "A",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 10,
    "sheet": "A-1.2",
    "title": "BUILDING B - WALL SECTIONS",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 10,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 12,
    "refs_in": 45
  },
  {
    "page": 11,
    "sheet": "A-1.3",
    "title": "BUILDING B - ROOF PLAN",
    "discipline": "A",
    "type": "roof_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 5,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 5,
    "refs_in": 26
  },
  {
    "page": 12,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 26,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 28,
    "refs_in": 0
  },
  {
    "page": 13,
    "sheet": "A-2.2",
    "title": "EXTERIOR DETAILS AND SECTIONS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 57
  },
  {
    "page": 14,
    "sheet": "A-2.3",
    "title": "EXTERIOR DETAILS AND SECTIONS",
    "discipline": "A",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 5,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 5,
    "refs_in": 39
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
    "has_details": false,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 16,
    "sheet": "A-3.0",
    "title": "PLUMBING FIXTURES AND  ACCESSORIES",
    "discipline": "A",
    "type": "schedule_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 3,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 17,
    "sheet": "A-4.0",
    "title": "BUILDING B - REFLECTIVE CEILING PLAN",
    "discipline": "A",
    "type": "ceiling_plan",
    "confidence": 0.7,
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
    "page": 18,
    "sheet": "S-0.1",
    "title": "GENERAL NOTES",
    "discipline": "S",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 3
  },
  {
    "page": 19,
    "sheet": "S-0.2",
    "title": "GENERAL NOTES",
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
    "page": 20,
    "sheet": "S-0.3",
    "title": "GENERAL NOTES",
    "discipline": "S",
    "type": "framing_plan",
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
    "page": 21,
    "sheet": "A1",
    "title": "---",
    "discipline": "A",
    "type": "elevation",
    "confidence": 0.7,
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
    "page": 22,
    "sheet": "S-2.0",
    "title": "BLOCK AND LINTEL PLAN",
    "discipline": "S",
    "type": "detail_sheet",
    "confidence": 0.7,
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
    "page": 23,
    "sheet": "S-3.0",
    "title": "ROOF FRAMING PLAN",
    "discipline": "S",
    "type": "framing_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 24,
    "sheet": "S-4.0",
    "title": "WALL SECTIONS AND STRUCTURAL DETAILS",
    "discipline": "S",
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
    "refs_in": 12
  },
  {
    "page": 25,
    "sheet": "E-0.0",
    "title": "ELECTRICAL GENERAL NOTES",
    "discipline": "E",
    "type": "detail_sheet",
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
    "page": 26,
    "sheet": "E-1.0",
    "title": "BUILDING B ELECTRICAL POWER PLAN",
    "discipline": "E",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 27,
    "sheet": "E-2.0",
    "title": "BUILDING B ELECTRICAL LIGHTING PLAN",
    "discipline": "E",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 28,
    "sheet": "E-3.0",
    "title": "ELECTRICAL RISER AND SUB-PANELS",
    "discipline": "E",
    "type": "ceiling_plan",
    "confidence": 0.7,
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
    "page": 29,
    "sheet": "P-0.1",
    "title": "PLUMBING SITE PLAN",
    "discipline": "P",
    "type": "site_plan",
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
    "page": 30,
    "sheet": "P-0.2",
    "title": "PLUMBING GENERAL NOTES",
    "discipline": "P",
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
    "page": 31,
    "sheet": "P-1.0",
    "title": "BUILDING B - WATER - PLUMBING PLAN",
    "discipline": "P",
    "type": "mep_plan",
    "confidence": 0.3,
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
    "page": 32,
    "sheet": "P-2.0",
    "title": "BUILDING B - SANITARY - PLUMBING PLAN",
    "discipline": "P",
    "type": "mep_plan",
    "confidence": 0.3,
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
    "page": 33,
    "sheet": "P-3.0",
    "title": "BUILDING B - ROOF PLAN",
    "discipline": "P",
    "type": "roof_plan",
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
    "page": 34,
    "sheet": "P-4.0",
    "title": "PLUMBING DETAILS",
    "discipline": "P",
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
    "page": 35,
    "sheet": "M-1.0",
    "title": "MECHANICAL LAYOUT",
    "discipline": "M",
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
    "page": 37,
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
    "page": 38,
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
    "page": 40,
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
    "page": 41,
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
    "page": 42,
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
    "page": 43,
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
    "page": 44,
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
    "page": 45,
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
    "page": 46,
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
    "page": 47,
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
    "page": 48,
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
    "page": 49,
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
    "page": 50,
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
    "page": 51,
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
    "page": 52,
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
    "page": 61,
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
    "page": 62,
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
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 63,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
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
    "page": 64,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
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
    "page": 65,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
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
    "page": 66,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
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
    "page": 67,
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
    "page": 68,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.5,
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
    "type": "site_plan",
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
    "type": "roof_plan",
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
    "type": "section",
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
    "page": 72,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 35,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 35,
    "refs_in": 0
  },
  {
    "page": 73,
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
    "page": 74,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.7,
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
    "page": 75,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 12,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 12,
    "refs_in": 0
  },
  {
    "page": 76,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 77,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 12,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 14,
    "refs_in": 0
  },
  {
    "page": 78,
    "sheet": "A-1.4",
    "title": "BUILDING A - ROOF PLAN",
    "discipline": "A",
    "type": "roof_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 3,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 3,
    "refs_in": 3
  },
  {
    "page": 79,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 18,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 20,
    "refs_in": 0
  },
  {
    "page": 80,
    "sheet": "A-2.1",
    "title": "BUILDING B - EXTERIOR ELEVATIONS",
    "discipline": "A",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 8
  },
  {
    "page": 81,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 5,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 5,
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
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 83,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "ceiling_plan",
    "confidence": 0.7,
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
    "page": 84,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.7,
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
    "page": 85,
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
    "page": 86,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "framing_plan",
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
    "page": 87,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
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
    "page": 88,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.5,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 4,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 4,
    "refs_in": 0
  },
  {
    "page": 89,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 4,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 5,
    "refs_in": 0
  },
  {
    "page": 90,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "framing_plan",
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
    "page": 91,
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
    "zone_count": 5,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 92,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 93,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 94,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "ceiling_plan",
    "confidence": 0.7,
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
    "page": 95,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "site_plan",
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
    "page": 96,
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
    "page": 97,
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
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 98,
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
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 99,
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
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 100,
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
    "page": 101,
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
    "page": 102,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.5,
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
    "page": 103,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "site_plan",
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
    "page": 104,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "roof_plan",
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
    "page": 105,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
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
    "page": 106,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": true,
    "detail_count": 35,
    "zone_count": 4,
    "legend_count": 1,
    "refs_out": 35,
    "refs_in": 0
  },
  {
    "page": 107,
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
    "page": 108,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "general_notes",
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
    "page": 109,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.7,
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
    "page": 110,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "floor_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 15,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 15,
    "refs_in": 0
  },
  {
    "page": 111,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 112,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 10,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 12,
    "refs_in": 0
  },
  {
    "page": 113,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "roof_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 5,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 5,
    "refs_in": 0
  },
  {
    "page": 114,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.9,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 26,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 28,
    "refs_in": 0
  },
  {
    "page": 115,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 1,
    "zone_count": 3,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 116,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 5,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 5,
    "refs_in": 0
  },
  {
    "page": 117,
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
    "page": 118,
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
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 119,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "ceiling_plan",
    "confidence": 0.7,
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
    "page": 120,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "section",
    "confidence": 0.7,
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
    "page": 121,
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
    "page": 122,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "framing_plan",
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
    "page": 123,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "elevation",
    "confidence": 0.7,
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
    "page": 124,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "detail_sheet",
    "confidence": 0.7,
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
    "page": 125,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "framing_plan",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": true,
    "has_legend": false,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 1,
    "refs_in": 0
  },
  {
    "page": 126,
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
    "page": 127,
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
    "zone_count": 5,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 128,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 2,
    "legend_count": 1,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 129,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "schedule_sheet",
    "confidence": 0.7,
    "has_drawing": true,
    "has_title_block": true,
    "has_details": false,
    "has_legend": true,
    "detail_count": 0,
    "zone_count": 4,
    "legend_count": 2,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 130,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "ceiling_plan",
    "confidence": 0.7,
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
    "page": 131,
    "sheet": "---",
    "title": "---",
    "discipline": "?",
    "type": "site_plan",
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
    "page": 132,
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
    "page": 133,
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
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 134,
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
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 135,
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
    "zone_count": 2,
    "legend_count": 0,
    "refs_out": 0,
    "refs_in": 0
  },
  {
    "page": 136,
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
    "page": 137,
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
- Legend count: 46
- Quality flag count: 0

#### Quality flags raised

```json
[]
```

#### Legend contents (sample, truncated)

```json
[
  {
    "type": "door_schedule",
    "title": "DOOR AND FRAME NOTES:\n1.  INTERIOR HM FRAMES SHALL BE 16 GA. SHOP PRIMED STEEL.\n",
    "page": 4,
    "entry_count": 10,
    "confidence": 0.7,
    "source": "legend: DOOR AND FRAME NOTES:\n1.  INTERIOR HM FR",
    "entries_sample": [
      {
        "key": "1",
        "desc": "INTERIOR HM FRAMES SHALL BE 16 GA. SHOP PRIMED STEEL."
      },
      {
        "key": "2",
        "desc": "EXTERIOR HM FRAMES SHALL BE 14 GA. GALVANIZED SHOP PRIMED"
      },
      {
        "key": "3",
        "desc": "ALL CORNERS OF EXTERIOR HM FRAMES SHALL BE SHOP (FULL)"
      },
      {
        "key": "4",
        "desc": "FLOOR ANCHORS ARE REQUIRED AT EACH HM FRAME."
      },
      {
        "key": "5",
        "desc": "THRESHOLDS SHALL BE 1/2\" MAXIMUM HEIGHT."
      },
      {
        "key": "6",
        "desc": "HEAD ANCHORS: TWO ANCHORS PER HEAD FOR FRAMES MORE THAN"
      },
      {
        "key": "42",
        "desc": "INCHES (1067 MM) WIDE AND MOUNTED IN METAL-STUD PARTITIONS."
      },
      {
        "key": "7",
        "desc": "HARDWARE PREPARATION: FACTORY PREPARE HOLLOW-METAL WORK"
      },
      {
        "key": "8",
        "desc": "MULLIONS AND TRANSOM BARS: JOIN TO ADJACENT MEMBERS BY"
      },
      {
        "key": "9",
        "desc": "PROVIDE SMOKE SEALS AROUND DOOR PERIMETER AS REQUIRED."
      }
    ]
  },
  {
    "type": "finish_schedule",
    "title": "NOTE: EXTERIOR FINISH\nPER WALL SECTIONS AND\nELEVATIONS",
    "page": 6,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTE: EXTERIOR FINISH\nPER WALL SECTIONS ",
    "entries_sample": [
      {
        "key": "1",
        "desc": "1/2\" = 1'-0\""
      },
      {
        "key": "1",
        "desc": "03"
      },
      {
        "key": "8",
        "desc": "AT FIRE BARRIERS"
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "EGRESS DATA LI\n* MIN\nEXITS * EXI\nVIS\nREQUIRED EXITS = 2 PER UNIT\n* EM\nPROVIDED E",
    "page": 9,
    "entry_count": 3,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "EMERGENCY LIGHT\nEXIT",
        "desc": ""
      },
      {
        "key": "",
        "desc": "OMPLIANCE STATEMENT\nE SAFETY PLAN SHALL COMPLY WITH ALL PROVISIONS OF THE LIFE S"
      },
      {
        "key": "",
        "desc": ".C. COMPLIANCE NOTES\nPARATE PERMIT REQUIRED FOR NEW FIRE ALARM SYSTEM.\nERMIT BY "
      }
    ]
  },
  {
    "type": "schedule",
    "title": "TOILET ACCESSORIES SCHEDULE",
    "page": 16,
    "entry_count": 6,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "TAG",
        "desc": "ITEM MANUFACTURER MODEL NO. DESCRIPTION"
      },
      {
        "key": "TA-1",
        "desc": "Framed Mirror Bobrick Washroom Equipment, Inc. B-165 Stainless Steel Frame"
      },
      {
        "key": "TA-2",
        "desc": "Surface Mounted Toilet Tissue Dispenser Bobrick Washroom Equipment, Inc. B-2746 "
      },
      {
        "key": "TA-3",
        "desc": "Classic Series Surface Mounted Soap Dispenser Bobrick Washroom Equipment, Inc. B"
      },
      {
        "key": "TA-4\nTA-5",
        "desc": "1 1/4\" Diameter Stainless Steel Grab Bars with Snap Flange 36\"\nWall Mounted Pape"
      },
      {
        "key": "TA-6",
        "desc": "Sanitary Dispenser TBD\nTBD TBD\nTBD White"
      }
    ]
  },
  {
    "type": "notes",
    "title": "54\" min\n42\" min\nCL\n.nim\n\"51",
    "page": 16,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "xam\n\"84"
      },
      {
        "key": "",
        "desc": "7\"-9\""
      }
    ]
  },
  {
    "type": "schedule",
    "title": "OTHER FIXTURE SCHEDULE",
    "page": 17,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: OTHER FIXTURE SCHEDULE",
    "entries_sample": [
      {
        "key": "17",
        "desc": "9"
      },
      {
        "key": "277",
        "desc": "VAC"
      },
      {
        "key": "277",
        "desc": "VAC"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:",
    "page": 18,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: NOTES:",
    "entries_sample": [
      {
        "key": "3000",
        "desc": "PSI"
      },
      {
        "key": "3000",
        "desc": "PSI"
      },
      {
        "key": "3000",
        "desc": "PSI"
      },
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "28",
        "desc": "DAY"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:",
    "page": 19,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES:",
    "entries_sample": [
      {
        "key": "4",
        "desc": "MAXIMUM WALL HEIGHT FROM TOP OF FOOTING OR PREVIOUS GROUT"
      },
      {
        "key": "3",
        "desc": "PLACE GROUT WITHIN 90 MINUTES FROM INTRODUCING WATER IN THE"
      },
      {
        "key": "2",
        "desc": "DO NOT GROUT UNTIL MORTAR HAS SET SUFFICIENTLY TO WITHSTAND"
      }
    ]
  },
  {
    "type": "notes",
    "title": "LAP SPLICE LENGTH SHALL BE PER FOLLOWING TABLE MODIFIED PER NOTES BELOW",
    "page": 20,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: LAP SPLICE LENGTH SHALL BE PER FOLLOWING",
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
        "key": "5000",
        "desc": "PSI"
      },
      {
        "key": "6000",
        "desc": "PSI"
      },
      {
        "key": "7000",
        "desc": "PSI"
      },
      {
        "key": "8000",
        "desc": "PSI"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "TENSION BAR CLASS B LAP SPLICE SCHEDULE",
    "page": 20,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: TENSION BAR CLASS B LAP SPLICE SCHEDULE",
    "entries_sample": [
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "5000",
        "desc": "PSI"
      },
      {
        "key": "6000",
        "desc": "PSI"
      },
      {
        "key": "7000",
        "desc": "PSI"
      },
      {
        "key": "8000",
        "desc": "PSI"
      },
      {
        "key": "9000",
        "desc": "PSI"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "2.  A SCHEDULED BASIS THAT TURNS LIGHTING OFF AT A PROGRAMMED\nTIME OF DAY. PROVI",
    "page": 25,
    "entry_count": 22,
    "confidence": 0.7,
    "source": "legend: 2.  A SCHEDULED BASIS THAT TURNS LIGHTIN",
    "entries_sample": [
      {
        "key": "2.17",
        "desc": "SITE LIGHTING"
      },
      {
        "key": "2.16",
        "desc": "SPECIFIC APPLIANCES"
      },
      {
        "key": "1",
        "desc": "AUTOMOTIVE VACUUM MACHINES"
      },
      {
        "key": "2",
        "desc": "DRINKING WATER COOLERSAND BOTTLE FILL STATIONS"
      },
      {
        "key": "3",
        "desc": "CORD-AND-PLUG CONNECTED HIGH-PRESSURE SPRAY WASHING"
      },
      {
        "key": "4",
        "desc": "TIRE INFLATION MACHINES"
      },
      {
        "key": "5",
        "desc": "VENDING MACHINES"
      },
      {
        "key": "6",
        "desc": "SUMP PUMPS"
      },
      {
        "key": "7",
        "desc": "DISHWASHERS"
      },
      {
        "key": "150",
        "desc": "VOLTS OR LESS TO GROUND, 50 AMPERE OR LESS, AND ALL"
      }
    ]
  },
  {
    "type": "finish_schedule",
    "title": "C.       WHERE CONDUIT MOTION DUE TO EXPANSION AND CONTRACTION WILL\nOCCUR, PROVI",
    "page": 25,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: C.       WHERE CONDUIT MOTION DUE TO EXP",
    "entries_sample": [
      {
        "key": "3.07",
        "desc": "PENETRATIONS"
      },
      {
        "key": "1",
        "desc": "TERMINATE SLEEVES FLUSH WITH WALLS, PARTITIONS AND CEILING."
      },
      {
        "key": "2",
        "desc": "IN AREAS WHERE CONDUIT IS CONCEALED, AS IN CHASES, TERMINATE"
      },
      {
        "key": "3",
        "desc": "IN AREAS WHERE CONDUIT IS EXPOSED, EXTEND SLEEVES 2\" ABOVE"
      },
      {
        "key": "4",
        "desc": "SLEEVES SHALL BE CONSTRUCTED OF SCHEDULE 40 STEEL PIPE."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "RECEPTACLE/ SWITCH/ OTHER SCHEDULE",
    "page": 26,
    "entry_count": 5,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "SYMBOL",
        "desc": "DEVICE DEVICE RATING MANUF. # QUANTITY DESCRIPTION"
      },
      {
        "key": "GFI",
        "desc": "OUTLET 20A., 110VAC, 40W MIN.\n20A., 110VAC, 40W MIN. 7\n7 120\nX10, WHITE, LINE VO"
      },
      {
        "key": "",
        "desc": "SWITCH SINGLE\n3-WAY LIGHT SWITCH 9\n16 SWITCH"
      },
      {
        "key": "",
        "desc": "WATER\nHEATER 120V EEMAX\nSP3512 7 INSTA HOT WATER HEATER\nEEMAX SP3512 OR EQUAL"
      },
      {
        "key": "",
        "desc": "SUB-PANEL 120\nWYE - 200 AMP\n208\n3 PHASE - W WIRE - 7 SUB PANEL - AIC RATING = 22"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "OTHER FIXTURE SCHEDULE",
    "page": 27,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: OTHER FIXTURE SCHEDULE",
    "entries_sample": [
      {
        "key": "17",
        "desc": "9"
      },
      {
        "key": "277",
        "desc": "VAC"
      },
      {
        "key": "277",
        "desc": "VAC"
      }
    ]
  },
  {
    "type": "notes",
    "title": "FIXTURE\nTYPE FIXTURE\nDESCRIPTION MANUFACTURERS QTY LAMPS FIXTURE\nWATTAGE",
    "page": 27,
    "entry_count": 4,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "UNIVERSAL MOUNTED DUAL EMERGENCY HEADS\nEXIT SIGN W/ RED LED ON WHITE THERMOPLAST"
      },
      {
        "key": "",
        "desc": "8', 8000 LUMEN, 4K TEMP., LED STRIP LIGHT,\n22 GA. STEEL, ALL PARTS PAF, WIRE GUA"
      },
      {
        "key": "",
        "desc": "SURFACE MOUNTED WALL LIGHT FIXTURE,\n1000 LUMEN LED, BLACK METAL HOUSING,\nUV RESI"
      },
      {
        "key": "",
        "desc": "SURFACE MOUNTED WALL LIGHT FIXTURE,\n800 LUMEN LED, BLACK METAL HOUSING,\nUV RESIS"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:\n1.     ALL CONDUCTORS SHALL BE COPPER\n2.     ALL CONDUIT SHALL HAVE EQUIP",
    "page": 28,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: NOTES:\n1.     ALL CONDUCTORS SHALL BE CO",
    "entries_sample": [
      {
        "key": "7",
        "desc": "WHERE MC CABLE IS ALLOWED BY THE AUTHORITY HAVING JURISDICTION, THE"
      },
      {
        "key": "1",
        "desc": "1/4\""
      },
      {
        "key": "1",
        "desc": "1/4\""
      },
      {
        "key": "1",
        "desc": "1/4\""
      },
      {
        "key": "2",
        "desc": "ALL CONDUIT SHALL HAVE EQUIPMENT GROUNDING CONDUCTOR INSTALLED."
      },
      {
        "key": "3",
        "desc": "CONDUIT BELOW GRADE OUTSIDE OF BUILDING SHALL BE 1\" MINIMUM."
      },
      {
        "key": "4",
        "desc": "SIZING OF CONDUCTORS SHALL BE ALTERED FOR DERATING PER N.E.C. OR VOLTAGE"
      },
      {
        "key": "5",
        "desc": "SEE RISER DIAGRAM FOR SIZING OF CIRCUITS GREATER THAN 100A."
      },
      {
        "key": "6",
        "desc": "USE #10 AWG, COPPER CONDUCTORS FOR 20 AMPERE, 120 VOLT BRANCH CIRCUITS"
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "DOOR AND FRAME NOTES:\n1.  INTERIOR HM FRAMES SHALL BE 16 GA. SHOP PRIMED STEEL.\n",
    "page": 72,
    "entry_count": 10,
    "confidence": 0.7,
    "source": "legend: DOOR AND FRAME NOTES:\n1.  INTERIOR HM FR",
    "entries_sample": [
      {
        "key": "1",
        "desc": "INTERIOR HM FRAMES SHALL BE 16 GA. SHOP PRIMED STEEL."
      },
      {
        "key": "2",
        "desc": "EXTERIOR HM FRAMES SHALL BE 14 GA. GALVANIZED SHOP PRIMED"
      },
      {
        "key": "3",
        "desc": "ALL CORNERS OF EXTERIOR HM FRAMES SHALL BE SHOP (FULL)"
      },
      {
        "key": "4",
        "desc": "FLOOR ANCHORS ARE REQUIRED AT EACH HM FRAME."
      },
      {
        "key": "5",
        "desc": "THRESHOLDS SHALL BE 1/2\" MAXIMUM HEIGHT."
      },
      {
        "key": "6",
        "desc": "HEAD ANCHORS: TWO ANCHORS PER HEAD FOR FRAMES MORE THAN"
      },
      {
        "key": "42",
        "desc": "INCHES (1067 MM) WIDE AND MOUNTED IN METAL-STUD PARTITIONS."
      },
      {
        "key": "7",
        "desc": "HARDWARE PREPARATION: FACTORY PREPARE HOLLOW-METAL WORK"
      },
      {
        "key": "8",
        "desc": "MULLIONS AND TRANSOM BARS: JOIN TO ADJACENT MEMBERS BY"
      },
      {
        "key": "9",
        "desc": "PROVIDE SMOKE SEALS AROUND DOOR PERIMETER AS REQUIRED."
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "EGRESS DATA\nEXITS\nREQUIRED EXITS = 2 PER UNIT\nPROVIDED EXITS = 2 PER UNIT\nCOMMON",
    "page": 76,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "EMERGENCY LIGHT\nEXIT",
        "desc": ""
      },
      {
        "key": "",
        "desc": "CODE 2023, 8TH EDITION AND OTHER APPLICABLE CODES AND ORDINANCES.\nH.C. COMPLIANC"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "OTHER FIXTURE SCHEDULE",
    "page": 83,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: OTHER FIXTURE SCHEDULE",
    "entries_sample": [
      {
        "key": "17",
        "desc": "9"
      },
      {
        "key": "277",
        "desc": "VAC"
      },
      {
        "key": "277",
        "desc": "VAC"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:",
    "page": 84,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: NOTES:",
    "entries_sample": [
      {
        "key": "3000",
        "desc": "PSI"
      },
      {
        "key": "3000",
        "desc": "PSI"
      },
      {
        "key": "3000",
        "desc": "PSI"
      },
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "28",
        "desc": "DAY"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:",
    "page": 85,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES:",
    "entries_sample": [
      {
        "key": "3",
        "desc": "PLACE GROUT WITHIN 90 MINUTES FROM INTRODUCING WATER IN THE"
      },
      {
        "key": "2",
        "desc": "DO NOT GROUT UNTIL MORTAR HAS SET SUFFICIENTLY TO WITHSTAND"
      },
      {
        "key": "4",
        "desc": "MAXIMUM WALL HEIGHT FROM TOP OF FOOTING OR PREVIOUS GROUT"
      }
    ]
  },
  {
    "type": "notes",
    "title": "LAP SPLICE LENGTH SHALL BE PER FOLLOWING TABLE MODIFIED PER NOTES BELOW",
    "page": 86,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: LAP SPLICE LENGTH SHALL BE PER FOLLOWING",
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
        "key": "5000",
        "desc": "PSI"
      },
      {
        "key": "6000",
        "desc": "PSI"
      },
      {
        "key": "7000",
        "desc": "PSI"
      },
      {
        "key": "8000",
        "desc": "PSI"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "TENSION BAR CLASS B LAP SPLICE SCHEDULE",
    "page": 86,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: TENSION BAR CLASS B LAP SPLICE SCHEDULE",
    "entries_sample": [
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "5000",
        "desc": "PSI"
      },
      {
        "key": "6000",
        "desc": "PSI"
      },
      {
        "key": "7000",
        "desc": "PSI"
      },
      {
        "key": "8000",
        "desc": "PSI"
      },
      {
        "key": "9000",
        "desc": "PSI"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "2.  A SCHEDULED BASIS THAT TURNS LIGHTING OFF AT A PROGRAMMED\nTIME OF DAY. PROVI",
    "page": 91,
    "entry_count": 22,
    "confidence": 0.7,
    "source": "legend: 2.  A SCHEDULED BASIS THAT TURNS LIGHTIN",
    "entries_sample": [
      {
        "key": "2.17",
        "desc": "SITE LIGHTING"
      },
      {
        "key": "2.16",
        "desc": "SPECIFIC APPLIANCES"
      },
      {
        "key": "1",
        "desc": "AUTOMOTIVE VACUUM MACHINES"
      },
      {
        "key": "2",
        "desc": "DRINKING WATER COOLERSAND BOTTLE FILL STATIONS"
      },
      {
        "key": "3",
        "desc": "CORD-AND-PLUG CONNECTED HIGH-PRESSURE SPRAY WASHING"
      },
      {
        "key": "4",
        "desc": "TIRE INFLATION MACHINES"
      },
      {
        "key": "5",
        "desc": "VENDING MACHINES"
      },
      {
        "key": "6",
        "desc": "SUMP PUMPS"
      },
      {
        "key": "7",
        "desc": "DISHWASHERS"
      },
      {
        "key": "150",
        "desc": "VOLTS OR LESS TO GROUND, 50 AMPERE OR LESS, AND ALL"
      }
    ]
  },
  {
    "type": "finish_schedule",
    "title": "C.       WHERE CONDUIT MOTION DUE TO EXPANSION AND CONTRACTION WILL\nOCCUR, PROVI",
    "page": 91,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: C.       WHERE CONDUIT MOTION DUE TO EXP",
    "entries_sample": [
      {
        "key": "3.07",
        "desc": "PENETRATIONS"
      },
      {
        "key": "1",
        "desc": "TERMINATE SLEEVES FLUSH WITH WALLS, PARTITIONS AND CEILING."
      },
      {
        "key": "2",
        "desc": "IN AREAS WHERE CONDUIT IS CONCEALED, AS IN CHASES, TERMINATE"
      },
      {
        "key": "3",
        "desc": "IN AREAS WHERE CONDUIT IS EXPOSED, EXTEND SLEEVES 2\" ABOVE"
      },
      {
        "key": "4",
        "desc": "SLEEVES SHALL BE CONSTRUCTED OF SCHEDULE 40 STEEL PIPE."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "RECEPTACLE/ SWITCH/ OTHER SCHEDULE",
    "page": 92,
    "entry_count": 5,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "SYMBOL",
        "desc": "DEVICE DEVICE RATING\n20A., 110VAC, 40W MIN. MANUF. # QUANTITY\n7 DESCRIPTION\n120\n"
      },
      {
        "key": "GFI",
        "desc": "OUTLET 20A., 110VAC, 40W MIN. 7 120\nX10, WHITE, LINE VOLTAGE - IN RESTROOM\n277"
      },
      {
        "key": "",
        "desc": "SWITCH\nSWITCH\nW/ OS\nPHOTO\nCELL SINGLE\n3-WAY LIGHT SWITCH W/\nOCCUPANCY SENSOR\nPHO"
      },
      {
        "key": "",
        "desc": "WATER\nHEATER 120V EEMAX\nSP3512 7 INSTA HOT WATER HEATER\nEEMAX SP3512 OR EQUAL"
      },
      {
        "key": "",
        "desc": "SUB-PANEL 120\nWYE - 200 AMP\n208\n3 PHASE - W WIRE - 7 SUB PANEL - AIC RATING = 22"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "OTHER FIXTURE SCHEDULE",
    "page": 93,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: OTHER FIXTURE SCHEDULE",
    "entries_sample": [
      {
        "key": "17",
        "desc": "9"
      },
      {
        "key": "277",
        "desc": "VAC"
      },
      {
        "key": "277",
        "desc": "VAC"
      }
    ]
  },
  {
    "type": "notes",
    "title": "FIXTURE\nTYPE FIXTURE\nDESCRIPTION MANUFACTURERS QTY LAMPS FIXTURE\nWATTAGE",
    "page": 93,
    "entry_count": 4,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "UNIVERSAL MOUNTED DUAL EMERGENCY HEADS\nEXIT SIGN W/ RED LED ON WHITE THERMOPLAST"
      },
      {
        "key": "",
        "desc": "8', 8000 LUMEN, 4K TEMP., LED STRIP LIGHT,\n22 GA. STEEL, ALL PARTS PAF, WIRE GUA"
      },
      {
        "key": "",
        "desc": "SURFACE MOUNTED WALL LIGHT FIXTURE,\n1000 LUMEN LED, BLACK METAL HOUSING,\nUV RESI"
      },
      {
        "key": "",
        "desc": "SURFACE MOUNTED WALL LIGHT FIXTURE,\n800 LUMEN LED, BLACK METAL HOUSING,\nUV RESIS"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:\n1.     ALL CONDUCTORS SHALL BE COPPER\n2.     ALL CONDUIT SHALL HAVE EQUIP",
    "page": 94,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: NOTES:\n1.     ALL CONDUCTORS SHALL BE CO",
    "entries_sample": [
      {
        "key": "7",
        "desc": "WHERE MC CABLE IS ALLOWED BY THE AUTHORITY HAVING JURISDICTION, THE"
      },
      {
        "key": "1",
        "desc": "1/4\""
      },
      {
        "key": "1",
        "desc": "1/4\""
      },
      {
        "key": "1",
        "desc": "1/4\""
      },
      {
        "key": "2",
        "desc": "ALL CONDUIT SHALL HAVE EQUIPMENT GROUNDING CONDUCTOR INSTALLED."
      },
      {
        "key": "3",
        "desc": "CONDUIT BELOW GRADE OUTSIDE OF BUILDING SHALL BE 1\" MINIMUM."
      },
      {
        "key": "4",
        "desc": "SIZING OF CONDUCTORS SHALL BE ALTERED FOR DERATING PER N.E.C. OR VOLTAGE"
      },
      {
        "key": "5",
        "desc": "SEE RISER DIAGRAM FOR SIZING OF CIRCUITS GREATER THAN 100A."
      },
      {
        "key": "6",
        "desc": "USE #10 AWG, COPPER CONDUCTORS FOR 20 AMPERE, 120 VOLT BRANCH CIRCUITS"
      }
    ]
  },
  {
    "type": "notes",
    "title": "Note 1 \u2014 Service sizing basis",
    "page": 94,
    "entry_count": 4,
    "confidence": 0.7,
    "source": "legend: Note 1 \u2014 Service sizing basis",
    "entries_sample": [
      {
        "key": "721",
        "desc": "kVA (service capacity) > 692 kVA (calculated demand) \u2192 2000A Service Is Adequate"
      },
      {
        "key": "220.60",
        "desc": "at the time of tenant build-out."
      },
      {
        "key": "643.4",
        "desc": "kVA"
      },
      {
        "key": "692.4",
        "desc": "kVA"
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "DOOR AND FRAME NOTES:\n1.  INTERIOR HM FRAMES SHALL BE 16 GA. SHOP PRIMED STEEL.\n",
    "page": 106,
    "entry_count": 10,
    "confidence": 0.7,
    "source": "legend: DOOR AND FRAME NOTES:\n1.  INTERIOR HM FR",
    "entries_sample": [
      {
        "key": "1",
        "desc": "INTERIOR HM FRAMES SHALL BE 16 GA. SHOP PRIMED STEEL."
      },
      {
        "key": "2",
        "desc": "EXTERIOR HM FRAMES SHALL BE 14 GA. GALVANIZED SHOP PRIMED"
      },
      {
        "key": "3",
        "desc": "ALL CORNERS OF EXTERIOR HM FRAMES SHALL BE SHOP (FULL)"
      },
      {
        "key": "4",
        "desc": "FLOOR ANCHORS ARE REQUIRED AT EACH HM FRAME."
      },
      {
        "key": "5",
        "desc": "THRESHOLDS SHALL BE 1/2\" MAXIMUM HEIGHT."
      },
      {
        "key": "6",
        "desc": "HEAD ANCHORS: TWO ANCHORS PER HEAD FOR FRAMES MORE THAN"
      },
      {
        "key": "42",
        "desc": "INCHES (1067 MM) WIDE AND MOUNTED IN METAL-STUD PARTITIONS."
      },
      {
        "key": "7",
        "desc": "HARDWARE PREPARATION: FACTORY PREPARE HOLLOW-METAL WORK"
      },
      {
        "key": "8",
        "desc": "MULLIONS AND TRANSOM BARS: JOIN TO ADJACENT MEMBERS BY"
      },
      {
        "key": "9",
        "desc": "PROVIDE SMOKE SEALS AROUND DOOR PERIMETER AS REQUIRED."
      }
    ]
  },
  {
    "type": "finish_schedule",
    "title": "NOTE: EXTERIOR FINISH\nPER WALL SECTIONS AND\nELEVATIONS",
    "page": 108,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTE: EXTERIOR FINISH\nPER WALL SECTIONS ",
    "entries_sample": [
      {
        "key": "1",
        "desc": "1/2\" = 1'-0\""
      },
      {
        "key": "1",
        "desc": "03"
      },
      {
        "key": "8",
        "desc": "AT FIRE BARRIERS"
      }
    ]
  },
  {
    "type": "door_schedule",
    "title": "EGRESS DATA LI\n* MI\nEXITS * EX\nVI\nREQUIRED EXITS = 2 PER UNIT\n* EM\nPROVIDED EXIT",
    "page": 111,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "EMERGENCY LIGHT\nEXIT",
        "desc": ""
      },
      {
        "key": "",
        "desc": "DE 2023, 8TH EDITION AND OTHER APPLICABLE CODES AND ORDINANCES.\n.C. COMPLIANCE N"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "TOILET ACCESSORIES SCHEDULE",
    "page": 118,
    "entry_count": 4,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "TAG",
        "desc": "ITEM MANUFACTURER MODEL NO. DESCRIPTION"
      },
      {
        "key": "TA-1",
        "desc": "Framed Mirror Bobrick Washroom Equipment, Inc. B-165 Stainless Steel Frame"
      },
      {
        "key": "TA-2\nTA-3\nTA-4",
        "desc": "Surface Mounted Toilet Tissue Dispenser\nClassic Series Surface Mounted Soap Disp"
      },
      {
        "key": "TA-5\nTA-6",
        "desc": "Wall Mounted Paper Towel\nSanitary Dispenser TBD\nTBD TBD\nTBD White\nWhite"
      }
    ]
  },
  {
    "type": "notes",
    "title": "54\" min\n42\" min\nCL\n.nim\n\"51",
    "page": 118,
    "entry_count": 2,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "xam\n\"84"
      },
      {
        "key": "",
        "desc": "7\"-9\""
      }
    ]
  },
  {
    "type": "schedule",
    "title": "OTHER FIXTURE SCHEDULE",
    "page": 119,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: OTHER FIXTURE SCHEDULE",
    "entries_sample": [
      {
        "key": "17",
        "desc": "9"
      },
      {
        "key": "277",
        "desc": "VAC"
      },
      {
        "key": "277",
        "desc": "VAC"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:",
    "page": 120,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: NOTES:",
    "entries_sample": [
      {
        "key": "3000",
        "desc": "PSI"
      },
      {
        "key": "3000",
        "desc": "PSI"
      },
      {
        "key": "3000",
        "desc": "PSI"
      },
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "28",
        "desc": "DAY"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:",
    "page": 121,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: NOTES:",
    "entries_sample": [
      {
        "key": "3",
        "desc": "PLACE GROUT WITHIN 90 MINUTES FROM INTRODUCING WATER IN THE"
      },
      {
        "key": "2",
        "desc": "DO NOT GROUT UNTIL MORTAR HAS SET SUFFICIENTLY TO WITHSTAND"
      },
      {
        "key": "4",
        "desc": "MAXIMUM WALL HEIGHT FROM TOP OF FOOTING OR PREVIOUS GROUT"
      }
    ]
  },
  {
    "type": "notes",
    "title": "LAP SPLICE LENGTH SHALL BE PER FOLLOWING TABLE MODIFIED PER NOTES BELOW",
    "page": 122,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: LAP SPLICE LENGTH SHALL BE PER FOLLOWING",
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
        "key": "5000",
        "desc": "PSI"
      },
      {
        "key": "6000",
        "desc": "PSI"
      },
      {
        "key": "7000",
        "desc": "PSI"
      },
      {
        "key": "8000",
        "desc": "PSI"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "TENSION BAR CLASS B LAP SPLICE SCHEDULE",
    "page": 122,
    "entry_count": 6,
    "confidence": 0.7,
    "source": "legend: TENSION BAR CLASS B LAP SPLICE SCHEDULE",
    "entries_sample": [
      {
        "key": "4000",
        "desc": "PSI"
      },
      {
        "key": "5000",
        "desc": "PSI"
      },
      {
        "key": "6000",
        "desc": "PSI"
      },
      {
        "key": "7000",
        "desc": "PSI"
      },
      {
        "key": "8000",
        "desc": "PSI"
      },
      {
        "key": "9000",
        "desc": "PSI"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "2.  A SCHEDULED BASIS THAT TURNS LIGHTING OFF AT A PROGRAMMED\nTIME OF DAY. PROVI",
    "page": 127,
    "entry_count": 22,
    "confidence": 0.7,
    "source": "legend: 2.  A SCHEDULED BASIS THAT TURNS LIGHTIN",
    "entries_sample": [
      {
        "key": "2.17",
        "desc": "SITE LIGHTING"
      },
      {
        "key": "2.16",
        "desc": "SPECIFIC APPLIANCES"
      },
      {
        "key": "1",
        "desc": "AUTOMOTIVE VACUUM MACHINES"
      },
      {
        "key": "2",
        "desc": "DRINKING WATER COOLERSAND BOTTLE FILL STATIONS"
      },
      {
        "key": "3",
        "desc": "CORD-AND-PLUG CONNECTED HIGH-PRESSURE SPRAY WASHING"
      },
      {
        "key": "4",
        "desc": "TIRE INFLATION MACHINES"
      },
      {
        "key": "5",
        "desc": "VENDING MACHINES"
      },
      {
        "key": "6",
        "desc": "SUMP PUMPS"
      },
      {
        "key": "7",
        "desc": "DISHWASHERS"
      },
      {
        "key": "150",
        "desc": "VOLTS OR LESS TO GROUND, 50 AMPERE OR LESS, AND ALL"
      }
    ]
  },
  {
    "type": "finish_schedule",
    "title": "C.       WHERE CONDUIT MOTION DUE TO EXPANSION AND CONTRACTION WILL\nOCCUR, PROVI",
    "page": 127,
    "entry_count": 5,
    "confidence": 0.7,
    "source": "legend: C.       WHERE CONDUIT MOTION DUE TO EXP",
    "entries_sample": [
      {
        "key": "3.07",
        "desc": "PENETRATIONS"
      },
      {
        "key": "1",
        "desc": "TERMINATE SLEEVES FLUSH WITH WALLS, PARTITIONS AND CEILING."
      },
      {
        "key": "2",
        "desc": "IN AREAS WHERE CONDUIT IS CONCEALED, AS IN CHASES, TERMINATE"
      },
      {
        "key": "3",
        "desc": "IN AREAS WHERE CONDUIT IS EXPOSED, EXTEND SLEEVES 2\" ABOVE"
      },
      {
        "key": "4",
        "desc": "SLEEVES SHALL BE CONSTRUCTED OF SCHEDULE 40 STEEL PIPE."
      }
    ]
  },
  {
    "type": "schedule",
    "title": "RECEPTACLE/ SWITCH/ OTHER SCHEDULE",
    "page": 128,
    "entry_count": 5,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "SYMBOL",
        "desc": "DEVICE DEVICE RATING\n20A., 110VAC, 40W MIN. MANUF. # QUANTITY\n7 DESCRIPTION\n120\n"
      },
      {
        "key": "GFI",
        "desc": "OUTLET 20A., 110VAC, 40W MIN. 7 120\nX10, WHITE, LINE VOLTAGE - IN RESTROOM\n277"
      },
      {
        "key": "",
        "desc": "SWITCH SINGLE\n3-WAY LIGHT SWITCH 9\n16 SWITCH"
      },
      {
        "key": "",
        "desc": "WATER\nHEATER 120V EEMAX\nSP3512 7 INSTA HOT WATER HEATER\nEEMAX SP3512 OR EQUAL"
      },
      {
        "key": "",
        "desc": "SUB-PANEL 120\nWYE - 200 AMP\n208\n3 PHASE - W WIRE - 7 SUB PANEL - AIC RATING = 22"
      }
    ]
  },
  {
    "type": "schedule",
    "title": "OTHER FIXTURE SCHEDULE",
    "page": 129,
    "entry_count": 3,
    "confidence": 0.7,
    "source": "legend: OTHER FIXTURE SCHEDULE",
    "entries_sample": [
      {
        "key": "17",
        "desc": "9"
      },
      {
        "key": "277",
        "desc": "VAC"
      },
      {
        "key": "277",
        "desc": "VAC"
      }
    ]
  },
  {
    "type": "notes",
    "title": "FIXTURE\nTYPE FIXTURE\nDESCRIPTION MANUFACTURERS QTY LAMPS FIXTURE\nWATTAGE",
    "page": 129,
    "entry_count": 4,
    "confidence": 0.5,
    "source": "table extraction",
    "entries_sample": [
      {
        "key": "",
        "desc": "UNIVERSAL MOUNTED DUAL EMERGENCY HEADS\nEXIT SIGN W/ RED LED ON WHITE THERMOPLAST"
      },
      {
        "key": "",
        "desc": "8', 8000 LUMEN, 4K TEMP., LED STRIP LIGHT,\n22 GA. STEEL, ALL PARTS PAF, WIRE GUA"
      },
      {
        "key": "",
        "desc": "SURFACE MOUNTED WALL LIGHT FIXTURE,\n1000 LUMEN LED, BLACK METAL HOUSING,\nUV RESI"
      },
      {
        "key": "",
        "desc": "SURFACE MOUNTED WALL LIGHT FIXTURE,\n800 LUMEN LED, BLACK METAL HOUSING,\nUV RESIS"
      }
    ]
  },
  {
    "type": "notes",
    "title": "NOTES:\n1.     ALL CONDUCTORS SHALL BE COPPER\n2.     ALL CONDUIT SHALL HAVE EQUIP",
    "page": 130,
    "entry_count": 9,
    "confidence": 0.7,
    "source": "legend: NOTES:\n1.     ALL CONDUCTORS SHALL BE CO",
    "entries_sample": [
      {
        "key": "7",
        "desc": "WHERE MC CABLE IS ALLOWED BY THE AUTHORITY HAVING JURISDICTION, THE"
      },
      {
        "key": "1",
        "desc": "1/4\""
      },
      {
        "key": "1",
        "desc": "1/4\""
      },
      {
        "key": "1",
        "desc": "1/4\""
      },
      {
        "key": "2",
        "desc": "ALL CONDUIT SHALL HAVE EQUIPMENT GROUNDING CONDUCTOR INSTALLED."
      },
      {
        "key": "3",
        "desc": "CONDUIT BELOW GRADE OUTSIDE OF BUILDING SHALL BE 1\" MINIMUM."
      },
      {
        "key": "4",
        "desc": "SIZING OF CONDUCTORS SHALL BE ALTERED FOR DERATING PER N.E.C. OR VOLTAGE"
      },
      {
        "key": "5",
        "desc": "SEE RISER DIAGRAM FOR SIZING OF CIRCUITS GREATER THAN 100A."
      },
      {
        "key": "6",
        "desc": "USE #10 AWG, COPPER CONDUCTORS FOR 20 AMPERE, 120 VOLT BRANCH CIRCUITS"
      }
    ]
  }
]
```

## §6 — Per-Page Errors (if any)

- Pages where module raised: 0
- Pages with module attempt: 138
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

- Observed: roofing module produced 1201 `fields` entries across 138 pages with non-empty output (of 138 pages attempted), with 0 warnings and 0 equipment_pins.
- Observed: glazing module produced 100 glazing_items, 12 door_items, 23 storefront_items across 47 pages with non-empty output (of 138 pages attempted).
- Observed: dispatch project_scope detected_system = `None` with confidence `0.0`; scope_pages = `[]`; manufacturers = `[]`.
- Observed: debug section 6 emitted 46 legend entries and 0 legend quality flags.
- Observed: per-page module error rate roofing=0.00%, glazing=0.00% (§7 stop threshold = 25%; soft-observation band = 5–25%).

---

**End of report.** Vault rule active on `roofing_module.py`,
`roofing_vocabulary.py`, `glazing_module.py`, `glazing_vocabulary.py`,
and `debug_module.py`. The sweep modified zero `backend/core/` files
and added zero dependencies. This report is a descriptive artifact
for the future tuning planning conversation per Daniel's directive
2026-04-28 (PROJECT_CLAUDE.md §3).
