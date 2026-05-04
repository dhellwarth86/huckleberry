# Profile Diagnostic — Bearss Ave

**Date:** 2026-04-29
**Phase:** Profile diagnostic + housekeeping
**Bidset:** Bearss Ave Distribution Center — University — Marcobay Construction (3)
**PDF:** `C:\huck stage 2\full bid sets\Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf`
**Page count:** 91
**Sweep wall-clock reference:** 824.9s modules / 95.0s dispatch (per `SWEEP_OBSERVATION_bearss-ave.md`)

**Type of artifact:** observation only. No grading, no fix lists, no tuning recommendations, no extractor-alternative benchmarks. Times the existing stack (pdfplumber + RoofingModule + GlazingModule + debug_module sections 1/3/6) on two debug-driven target pages. The vault rule is active on all five vault-ruled modules per CLAUDE.md §3 Decision 15; this run modified zero `backend/core/` files.

---

## §1 — Page Selection Rationale

**High-content page:** 15

Top section-3 signal score (60), tied with page 61 which has unmapped sheet/title; page 15 chosen for clearer identity. Sheet S-103 'SPECIAL INSPECTIONS', type=section, 8 legends, 11 zones, 41 refs_out, confidence 0.7. Section-typed = notes-heavy spec/inspections page; exercises pdfplumber text + module text-scanning paths.

**Low-content page:** 82

Section-3 signal score 3 (legends 0, zones 3, refs in/out 0). type=unknown, confidence 0.0, sheet '---', title '---'. The page debug section 3 has no opinion about — module behavior on a page with no dispatch-side classification signal.

Page selection was driven by debug section 3 (page_intelligence) signal density per `SWEEP_OBSERVATION_bearss-ave.md`. Combined signal proxy = `legend_count + zone_count + refs_in + refs_out`. Page 15 ranked highest among pages with mapped sheet identity (score 60); page 82 ranked among the lowest (score 3) and was selected as the section-3-unclassified counterpoint.

## §2 — Dispatch Timing (whole bidset)

- run_dispatch wall-clock: `72.25s`
- Reference from sweep (2026-04-28): `95.0s`
- Delta vs sweep: `-22.75s` (`-23.9%`)

## §3 — Per-Page Timing (3 repeats; median in headline; range below)

| Operation | Page 15 (high) | Page 82 (low) | Ratio (high/low) |
|---|---:|---:|---:|
| pdfplumber text extraction | 117.28ms | 3.93ms | 29.83× |
| pdfplumber table extraction | 2.910s | 177.91ms | 16.36× |
| RoofingModule.analyze | 184.31ms | 11.09ms | 16.61× |
| GlazingModule.analyze | 11.57ms | 6.92ms | 1.67× |
| **Total per-page (sum of medians)** | **3.223s** | **199.85ms** | **16.13×** |

**Ranges (min–max across 3 repeats) for sanity-check:**

- Page 15 text: 72.42ms–1.702s; table: 2.907s–2.919s; roofing: 182.60ms–189.77ms; glazing: 11.54ms–15.40ms.
- Page 82 text: 3.47ms–1.314s; table: 163.04ms–208.82ms; roofing: 10.70ms–11.54ms; glazing: 6.77ms–7.06ms.

**Per-page wall-clock budget vs sweep average:** sweep modules averaged `9.06s/page` across 91 pages × 2 modules + per-page text/table extraction. This profile breaks that down on two specific pages.

## §4 — Module Output Summary

### Page 15 (high-content)

- pdfplumber text blocks extracted: `7083`
- pdfplumber tables extracted: `10`
- Roofing fields: `8`; warnings: `0`; equipment_pins: `0`
- Glazing items: `2 glazing` / `0 door` / `4 storefront`

### Page 82 (low-content)

- pdfplumber text blocks extracted: `316`
- pdfplumber tables extracted: `15`
- Roofing fields: `8`; warnings: `0`; equipment_pins: `0`
- Glazing items: `2 glazing` / `0 door` / `0 storefront`

## §5 — Debug Cross-Reference

### Page 15 (high-content)

**Section 3 (page_intelligence) entry for this page:**

```json
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
}
```

**Section 6 legends attributed to this page:** 8

```json
[
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
  }
]
```

**Section 6 quality flags (bidset-wide; not page-attributed):** 1 flags

```json
[
  "WARNING: unusually high legend count (145) \u2014 possible pdfplumber noise"
]
```

### Page 82 (low-content)

**Section 3 (page_intelligence) entry for this page:**

```json
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
}
```

**Section 6 legends attributed to this page:** 0

(none)

**Section 6 quality flags (bidset-wide; not page-attributed):** 1 flags

```json
[
  "WARNING: unusually high legend count (145) \u2014 possible pdfplumber noise"
]
```

**Section 1 (dispatch_health, bidset-wide) for context:**

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
  "timestamp": "2026-04-29T13:11:46.988878+00:00",
  "total_pages": 91,
  "sheet_map_source": "drawing_index",
  "sheet_count": 47,
  "mapped_pages": 44
}
```

## §6 — Observations (no fixes, no recommendations)

- Observed: pdfplumber text extraction medians were `117.28ms` on page 15 (high-content) and `3.93ms` on page 82 (low-content); ratio 29.83×.
- Observed: pdfplumber table extraction medians were `2.910s` on page 15 and `177.91ms` on page 82; ratio 16.36×.
- Observed: RoofingModule.analyze medians were `184.31ms` on page 15 and `11.09ms` on page 82; ratio 16.61×.
- Observed: GlazingModule.analyze medians were `11.57ms` on page 15 and `6.92ms` on page 82; ratio 1.67×.
- Observed: per-page total (sum of four operation medians) was `3.223s` on page 15 and `199.85ms` on page 82; per-page ratio 16.13×. Sweep-average per-page was `9.06s` (modules only across 91 pages; this profile additionally captures pdfplumber).
- Observed: on page 15 (high), the largest-median operation was `table` at `2.910s`; second was `roofing` at `184.31ms`. On page 82 (low), the largest-median operation was `table` at `177.91ms`; second was `roofing` at `11.09ms`.
- Observed: debug section 3's per-page entry for page 15 reported type=`section`, confidence=`0.7`, legend_count=`8`, zone_count=`11`, refs_out=`41`, refs_in=`0`. For page 82 it reported type=`unknown`, confidence=`0.0`, legend_count=`0`, zone_count=`3`, refs_out=`0`, refs_in=`0`.

Closing observation on page-selection utility of debug section 3: the per-page combined signal proxy (`legend_count + zone_count + refs_in + refs_out`) ordered the bidset's pages from a 60-point top to a 1-point bottom, with `confidence=0.0` distinguishing the unclassified low-end pages from low-but-confidently-classified pages — sufficient to drive this run's high (page 15) / low (page 82) selection without guessing.

## §7 — Closing

Diagnostic only. Profile data feeds the future planning conversation about Path (a) module tuning vs (b) C.4 design vs other directions. No tuning was performed. No fixes were attempted. The roofing module, glazing module, and debug module are vault-ruled per CLAUDE.md §3 Decision 15. The `backend/scripts/profile_diagnostic.py` harness is tracked (commit 1 of this phase) and reusable for future profile diagnostics on other bidsets.

---

**End of report.**
