# Phase 2 v0.2 — Validation Report (Step 17)

**Date:** 2026-04-26
**Inputs:** 15 PlanSetContext JSONs at `backend/test_fixtures/v0.2_outputs/<bidset_id>.json`
**Rubric:** `huckleberry/STEP_17_REVIEW_CHECKLIST.md`
**Comparison script:** `backend/scripts/compare_v0.1_to_v0.2.py`
**Machine-readable summary:** `backend/test_fixtures/v0_2_validation_summary.json`

This report records measurements only. Per the checklist and the v0.2 march
orders §5 Step 17: do NOT propose fixes here. Fixes belong in
DISCOVERED_ISSUES.md or in the next-version planning, not in this document.

---

## TL;DR

| Symptom | Pass rate | Threshold | Status |
|---|---|---|---|
| 1 — `project.field_sources["project_name"].confidence` populated | n/a | n/a | **N/A** (unmeasurable from JSON; checklist §10 mismatch) |
| 2 — single `detected_system` (str or None, never list) | 7/7 binary questions YES | all questions YES | **PASS** |
| 3 — drawing pages and scope pages structurally separate | 0.2857 corpus ratio + Taco Bell page 18 in scope_pages | ratio > 0.1789, Taco Bell q YES | **PASS** |
| 4 — sheet_map cleanliness | Vine Street individual q YES; corpus duplicate-check FAILED on Hampshire (N19A × 7) | all individual + corpus YES | **FAIL** |

**Gate decision (per checklist threshold "≥3 of 4 PASS, ≥80% of applicable bidsets"):**

- Measurable symptoms passing: 2 of 3 (S2, S3)
- Symptom 1: unmeasurable (N/A)
- Symptom 4: FAIL (Hampshire duplicate-sheet-name)

Strict reading of the checklist's gate decision rule:

> **<3 of 4 PASS:** STOP. Open a Discovered Issue. Do NOT silently extend
> v0.2 scope to fix; that's a v0.2.1 conversation.

With S1 N/A and S4 FAIL, only 2 of 4 are confirmed PASS. The "<3 of 4"
case applies. Per the checklist this triggers STOP and Discovered-Issue
filing; Daniel decides what counts as N/A in the gate denominator.

---

## Symptom 1 — Project Metadata Field-Sources Tracking

**Status: N/A (unmeasurable from v0.2 JSONs)**

### What the rubric asks

The checklist (§ Symptom 1) inspects `project.project_name`,
`project.field_sources.project_name.source`, and
`project.field_sources.project_name.confidence` for every bidset where
`project_name` is non-null, expecting a numeric `confidence` value.

### What the JSONs actually contain

Sampling the 15 outputs, the top-level keys produced by
`PlanSetContext.to_json()` are:

```
['all_cross_refs', 'all_legends', 'architect_profile', 'dispatch_complete',
 'dispatch_timestamp', 'dispatch_warnings', 'filters_completed',
 'page_to_sheet', 'pages', 'pdf_hash', 'pdf_path', 'project_scope',
 'resolved_count', 'sheet_map', 'sheet_map_source', 'total_pages',
 'unresolved_count']
```

There is no `project` field. Inspecting `core/context.py` `to_json()`
body confirms: `PlanSetContext.project` (a `ProjectMetadata` dataclass
populated by `_extract_project_metadata()` during `run_dispatch()`) is
runtime-only. It is not serialized.

### What this means for the validation

Symptom 1's binary pass question requires the `project.field_sources` map.
That map is populated in memory during dispatch but never written to JSON.
The Step 17 outputs cannot be measured against the rubric without
re-running dispatch on each bidset and inspecting the runtime `ctx.project`
directly.

Per checklist §10 Caveat on field paths:

> If a path doesn't match what's in the JSONs, the fix is to grep
> `core/context.py` for the actual `to_json()` body and update this
> document. Do NOT modify the JSONs to match this document.

The right resolution is to update the checklist (or extend `to_json()` to
serialize `project`). I did not take either action — that's outside Step
17's scope. Recording the mismatch here for Daniel's decision.

### Per-bidset table

Not produced. Field unmeasurable. See per-bidset placeholders in
`backend/test_fixtures/v0_2_validation_summary.json` under
`symptom_1.rows`.

---

## Symptom 2 — Single Detected System Per Bidset

**Status: PASS (7 of 7 binary questions YES)**

### Per-bidset table

| bidset_id | detected_system | type | system_confidence | scope_pages count |
|---|---|---|---|---|
| auto-zone-10891-jacksonville-mec-24-others | `None` | NoneType | 0.0 | 0 |
| auto-zone-vero-beach-fl | `None` | NoneType | 0.0 | 0 |
| b2607-aea-silverleaf-st-augustine-accelerated-construction-services-6 | `None` | NoneType | 0.0 | 0 |
| bearss-ave-distribution-center-university-marcobay-construction-3 | `None` | NoneType | 0.0 | 0 |
| chewy-vet-care-london-square-miami-jdr-fixtures | `None` | NoneType | 0.0 | 0 |
| chipotle-tarpon-springs-shell-tarpon-springs-strategic-construction | `None` | NoneType | 0.0 | 0 |
| hampshire-self-storage | `None` | NoneType | 0.0 | 0 |
| panda-express-bradenton | `None` | NoneType | 0.0 | 0 |
| panda-express-hialeah-gardens | `None` | NoneType | 0.0 | 0 |
| panda-express-naples-cdo-visible-construction-corp | `None` | NoneType | 0.0 | 0 |
| panda-express-san-antonio-candito-construction-2 | `None` | NoneType | 0.0 | 0 |
| shoppes-at-avalon-spring-hill-mec | `None` | NoneType | 0.0 | 0 |
| **taco-bell-weeki-wachee-compass-construction-management-2** | **`"tpo"`** | **str** | **0.95** | **2** |
| vine-street-retail-center-kissimmee-great-southern-constructors | `None` | NoneType | 0.0 | 0 |
| wendy-s-fort-myers-great-southern-constructors-3 | `None` | NoneType | 0.0 | 0 |

### Binary question results

| Binary question | Answer |
|---|---|
| Taco Bell `detected_system` is one of {tpo, pvc, epdm, modified_bitumen, built_up, metal_panel} | YES (`"tpo"`) |
| Taco Bell `system_confidence >= 0.7` | YES (0.95) |
| AutoZone Jacksonville: `project_scope` null OR `detected_system` null | YES (`None`) |
| AutoZone Jacksonville: `scope_pages` empty | YES (`[]`) |
| AutoZone Vero Beach: `project_scope` null OR `detected_system` null | YES (`None`) |
| AutoZone Vero Beach: `scope_pages` empty | YES (`[]`) |
| Corpus: `type(detected_system)` never `list` across all 15 | YES (always `str` or `None`) |

All 7 questions: YES. **Symptom 2 PASS.**

---

## Symptom 3 — Drawing Pages and Scope Pages Separate

**Status: PASS**

### Aggregate counter table

| metric | v0.1 | v0.2 | pass? |
|---|---|---|---|
| roof_plan pages total | 95 | 56 | — |
| roof_plan pages with confidence ≥ 0.9 | 17 | 16 | — |
| ratio (explicit / total) | 0.1789 | 0.2857 | YES (> 0.1789) |

### Per-bidset roof-plan pages (count + explicit-confidence subset)

| bidset_id | roof_plan total | roof_plan with conf≥0.9 |
|---|---|---|
| auto-zone-10891-jacksonville-mec-24-others | 0 | 0 |
| auto-zone-vero-beach-fl | 0 | 0 |
| b2607-aea-silverleaf-st-augustine-accelerated-construction-services-6 | 2 | 1 |
| bearss-ave-distribution-center-university-marcobay-construction-3 | 2 | 2 |
| chewy-vet-care-london-square-miami-jdr-fixtures | 3 | 2 |
| chipotle-tarpon-springs-shell-tarpon-springs-strategic-construction | 5 | 0 |
| hampshire-self-storage | 2 | 1 |
| panda-express-bradenton | 7 | 0 |
| panda-express-hialeah-gardens | 7 | 2 |
| panda-express-naples-cdo-visible-construction-corp | 6 | 1 |
| panda-express-san-antonio-candito-construction-2 | 2 | 1 |
| shoppes-at-avalon-spring-hill-mec | 4 | 0 |
| taco-bell-weeki-wachee-compass-construction-management-2 | 6 | 2 |
| vine-street-retail-center-kissimmee-great-southern-constructors | 9 | 3 |
| wendy-s-fort-myers-great-southern-constructors-3 | 1 | 1 |
| **TOTAL** | **56** | **16** |

### Specific binary question

| Binary question | Answer |
|---|---|
| For Taco Bell, is page 18 in `project_scope.scope_pages`? | YES (Taco Bell scope_pages contains 18) |
| Corpus explicit-confidence ratio > v0.1's 0.1789 | YES (0.2857) |

Both questions: YES. **Symptom 3 PASS.**

### Note on corpus interpretation

v0.2's roof_plan absolute total dropped from 95 (v0.1) to 56 (v0.2). The
ratio improved (0.18 → 0.29) but on a smaller denominator. The drop in
absolute count is partly explainable by v0.2's stricter scope-page hard
gate filtering body-text-driven roof_plan classifications out of scope
evidence accumulation — but the same gate also affects raw page-type
classification at Filter 2. Whether the smaller denominator is "correct"
or "lossy" is not a Step 17 question per the checklist.

---

## Symptom 4 — Sheet Map Cleanliness

**Status: FAIL**

### Per-bidset table

| bidset_id | sheet_map_source | sheet_map size | max-dup count | most-common (count) | TS9D in keys? | TS9D in values? |
|---|---|---|---|---|---|---|
| auto-zone-10891-jacksonville-mec-24-others | drawing_index | 31 | 1 | T1.0 (1) | no | no |
| auto-zone-vero-beach-fl | **title_blocks** | 23 | 1 | C0.1 (1) | no | no |
| b2607-aea-silverleaf-st-augustine-accelerated-construction-services-6 | drawing_index | 10 | 1 | WD1 (1) | no | no |
| bearss-ave-distribution-center-university-marcobay-construction-3 | drawing_index | 47 | 1 | A-001 (1) | no | no |
| chewy-vet-care-london-square-miami-jdr-fixtures | drawing_index | 89 | 1 | G001 (1) | no | no |
| chipotle-tarpon-springs-shell-tarpon-springs-strategic-construction | drawing_index | 39 | 1 | G000 (1) | no | no |
| **hampshire-self-storage** | **title_blocks** | 37 | **7** | **N19A (7)** | no | **no, but see below** |
| panda-express-bradenton | drawing_index | 77 | 1 | S5 (1) | no | no |
| panda-express-hialeah-gardens | drawing_index | 20 | 1 | C01.0 (1) | no | no |
| panda-express-naples-cdo-visible-construction-corp | drawing_index | 86 | 1 | G-001 (1) | no | no |
| panda-express-san-antonio-candito-construction-2 | drawing_index | 31 | 1 | M6 (1) | no | no |
| shoppes-at-avalon-spring-hill-mec | drawing_index | 30 | 1 | A-100 (1) | no | no |
| taco-bell-weeki-wachee-compass-construction-management-2 | drawing_index | 92 | 1 | T1.1 (1) | no | no |
| vine-street-retail-center-kissimmee-great-southern-constructors | drawing_index | 44 | 1 | A-1.0 (1) | **no (PASSES)** | **no (PASSES)** |
| wendy-s-fort-myers-great-southern-constructors-3 | drawing_index | 11 | 1 | QP0222 (1) | no | no |

### Vine Street specific binary questions

| Binary question | Answer |
|---|---|
| Vine Street `sheet_map_source == "drawing_index"` | YES |
| Vine Street `sheet_map` contains real architectural sheet numbers (`A-1.0`, `A-1.3`, ...) | YES |
| Vine Street `sheet_map` excludes `"TS9D"` | YES |

All Vine Street binary questions PASS. The v0.1 `TS9D × 7` symptom is gone
on Vine Street.

### Corpus-wide max-duplicate-value check

| Binary question | Answer |
|---|---|
| For every bidset, `max(Counter(page_to_sheet.values())) <= 2`, except documented multi-building cases (Bearss) | **NO** |

**Hampshire Self Storage fails this check.** Pages 64, 67, 68, 69, 70, 71,
72 (7 pages) all map to the sheet number `N19A`. Pages 38, 39, 40 (3
pages) all map to `S3.3`. Hampshire's `sheet_map_source` is
`title_blocks`, not `drawing_index` — Filter 1's drawing-index detector
did not find a qualifying index page in Hampshire (the "10+ unique sheet
numbers in early pages" gate failed), so Filter 1 fell back to
title-block scanning. The fallback path produced the same character of
failure as v0.1's Vine Street `TS9D × 7` symptom: a non-sheet-number
string (likely an engineering license stamp or surveyor signature)
matched `_SHEET_NUM_RE` on multiple consecutive pages and propagated.

**Symptom 4: FAIL** because the corpus binary question returned NO.

---

## Aggregate observations (separate from binary pass criteria)

Per Daniel's Step 17 brief: aggregate-level observations belong here as
separate notes, **NOT** as modifications to any Symptom's pass criteria.

### Observation A — Step 16 corpus-detection-rate finding

Of 15 bidsets, **only 1 (Taco Bell Weeki Wachee)** had a non-null
`project_scope.detected_system`. The other 14 came back with
`detected_system=None` and `scope_pages=[]`. This is the inverse of
v0.1's "Taco Bell tagged with 6 systems" symptom — v0.1 was too eager,
v0.2's scope-page hard gate (vector_count > 500: continue) appears too
strict on STACK-produced PDFs.

This observation is NOT a Symptom 2 pass-criterion modification. The
checklist's Symptom 2 binary questions are about specific bidsets (Taco
Bell + AutoZones + corpus type-check), not corpus detection rate. All
those binary questions returned YES.

The aggregate finding is recorded here so Daniel sees it; the resolution
is a v0.2.1 / v0.3 conversation, not a v0.2 gate decision.

### Observation B — sheet_map_source distribution

| sheet_map_source | bidsets |
|---|---|
| drawing_index | 13 |
| title_blocks | 2 (auto-zone-vero-beach-fl, hampshire-self-storage) |

Both bidsets that fell back to `title_blocks` are also the two bidsets
that produced unhelpful results on adjacent symptoms:

- AutoZone Vero Beach: 0 roof_plan pages classified (confirmed
  non-roofing-primary, gate doing its job per Step 16 brief)
- Hampshire Self Storage: the Symptom 4 failure case

Pattern: when Filter 1's drawing-index detector fails, the title-block
fallback exhibits v0.1-style failure modes. Drawing-index detection is
the load-bearing path for sheet-map quality.

### Observation C — Filter 4 quality-gate aggressive removal

Across the 15 bidsets, the Filter 4 quality gate removed substantial
fractions of legend candidates:

| Bidset | Legends removed / proposed |
|---|---|
| chewy-vet-care | 651 / 823 (79% removed) |
| hampshire-self-storage | 52 / 89 (58%) |
| panda-express-naples-cdo-visible-construction-corp | various |
| (others) | proportionally less |

The gate is doing what TracePoint's CLAUDE.md Step 46 designed it to do,
but the fact that Chewy's 651 legends got proposed and then removed
suggests Filter 4's initial parsing is over-permissive. Not a Step 17
gate concern; flagged for v0.3.

### Observation D — Wendy's runtime outlier

Wendy's Fort Myers took 576 seconds (about 9 minutes) for a 64-page
bidset. TracePoint's CLAUDE.md Step 56 documents the same outlier ("one
roof page has abnormal vector count causing slow clustering"). The v0.2
sweep reproduces that behavior — runtime ~5x the corpus-average per-page
rate. Not a Step 17 gate concern; flagged for v0.3.

---

## Optional v0.3 trajectory notes (per Step 17 brief sample-read suggestion)

Daniel's Step 17 brief offered an optional, read-only inspection of
Hampshire and Chewy for `pages[i].vector_count` distribution and
`dispatch_warnings` content, "to sharpen the v0.3 trajectory ticket
without affecting v0.2 measurements." Findings:

### Hampshire Self Storage (86 pages, 0 scope_pages)

- `dispatch_warnings`: 1 warning — `Filter 4 quality gate: 52 of 89
  legends removed (37 kept)`
- Page-type histogram includes 11 schedule_sheet, 2 general_notes,
  2 cover, 23 detail_sheet, 13 unknown.
- Cross-references: only 12 of 86 pages have any cross-refs.
- Despite 11 schedule_sheets and 2 general_notes — both candidates for
  scope-page acceptance — none entered `project_scope.scope_pages`. The
  hard gate (vector_count > 500) appears to reject them.

### Chewy Vet Care (93 pages, 0 scope_pages)

- `dispatch_warnings`: 2 warnings — `Filter 4 quality gate: 651 of 823
  legends removed (172 kept)`, `LOW RESOLUTION: 7% cross-references
  resolved`.
- Page-type histogram includes 16 schedule_sheet, 6 general_notes,
  6 ceiling_plan, 25 elevation, 17 detail_sheet, 1 cover.
- Cross-references: 11 of 93 pages have any cross-refs (low resolution
  reflects a tenant-fitout pattern per TracePoint CLAUDE.md notes on
  Chewy).
- Same pattern: schedule_sheets and general_notes don't make it into
  `project_scope.scope_pages` despite high text density on those pages.

### Limitation in this sample-read

`pages[i].vector_count` is **not serialized** in `to_json()`. The hard
gate uses runtime `engine.extract_vectors(doc, page_num)` and the count
is never persisted to PageContext. Confirming the v0.3 hypothesis that
"the gate's threshold is too strict on STACK PDFs" requires either
extending `to_json()` to write vector_count or re-running dispatch with
debug instrumentation. Both are v0.3 work, not Step 17 work.

---

## Summary for Daniel's review checkpoint

- **3 of 4 symptoms have a measurable verdict:** S2 PASS, S3 PASS, S4 FAIL.
- **Symptom 1 is N/A** because `to_json()` doesn't serialize `project`.
  Resolving this is a checklist update or a one-line extension to
  `to_json()`. Not a v0.2 implementation problem.
- **The S4 FAIL is on a single bidset (Hampshire), exhibiting the same
  failure mode as v0.1's Vine Street (TS9D ×7).** v0.2's drawing-index
  path is reliable when it fires; the title-block fallback is not.
- **The Step 16 1/15 detection rate is recorded as Observation A**, NOT
  as a Symptom-2 criterion modification, per Daniel's brief.

Per the checklist's gate rule, "<3 of 4 PASS" triggers STOP. Strict
counting puts v0.2 at 2 of 4 measurable PASS (S2, S3). Daniel decides
how to count S1 in the gate denominator.

---

## Gate decision

**Date:** 2026-04-26
**Decided by:** Daniel

**Strict rubric reading:** 2 of 4 PASS (S2, S3); S1 N/A; S4 FAIL.
**Override:** path (a) — **v0.2 ships.**

### Override rationale (recorded verbatim from Daniel's direction):

1. **S1 N/A is verified as a TracePoint verbatim-port consequence.** Grep
   of TracePoint's `core/context.py` `to_json()` body confirms
   `PlanSetContext.project` is not serialized upstream (only
   `project_scope` is). v0.2's "DO NOT modify ported TracePoint files"
   discipline (§4.3) prevents fixing it inside this version. The
   ProjectMetadata data exists at runtime; the JSON is a faithful copy
   of TracePoint's serialization shape, not a port miss.

2. **S4's Hampshire failure is single-bidset and not fixable inside
   verbatim-port discipline.** Filter 1's title-block fallback path is
   pure TracePoint code; the failure mode (license-stamp string
   propagating across pages) requires either a regex change or a
   post-pass — both deviations from verbatim port. v0.2.1 work, not v0.2.

3. **The corpus is 100% STACK-produced PDFs.** TracePoint's research
   paper documents STACK as known-hard (operator-stream traversal,
   producer-specific overlays). Broader gate validity awaits non-STACK
   bidsets entering the corpus.

### Filed Discovered Issues

Both items pre-scoped for v0.2.1:

- **D-4** — `to_json()` does not serialize `PlanSetContext.project`.
  Symptom 1 unmeasurable from JSON. Filed in
  `backend/DISCOVERED_ISSUES.md`. Smallest fix: extend `to_json()` and
  `from_json()` in `core/context.py` to include the `project` block
  (deterministic field_sources). Re-run sweep produces measurable data
  without changing the runtime parser.

- **D-5** — Hampshire title-block fallback propagates "N19A" to 7
  pages. Filed in `backend/DISCOVERED_ISSUES.md`. Smallest fix: post-pass
  on `ctx.page_to_sheet` after Filter 1 — when `sheet_map_source ==
  "title_blocks"` and any sheet number maps to >2 pages, re-classify
  those pages as having no sheet number.

---

## Corpus caveat (STACK-only)

**The validation corpus is 15 of 15 STACK-produced PDFs.** Every bidset
in `backend/test_fixtures/v0.2_outputs/` came through the STACK
Construction Technologies / UniDoc pipeline. None of the 15 are
non-STACK (CAD-direct export, Adobe-original, Bluebeam, etc.).

**STACK is documented in the TracePoint research paper as a known-hard
PDF producer.** Operator-stream traversal cost is 10–30× a typical CAD
PDF (per CLAUDE.md note: "46k–92k path operators per page"); STACK
overlay pages strip scale labels and add producer-specific borders that
defeat several of the dispatch gate's heuristics.

**Aggregate observations recorded in this report carry an explicit
STACK-corpus caveat:**

- **The Step 16 1/15 detected_system rate** (only Taco Bell hit) is
  reported with the caveat that STACK overlay pages may push every
  bidset over the scope-scanner's `vector_count > 500` hard gate, even
  on pages that are textually scope-rich. Whether the gate threshold is
  "right" or "too strict" is not measurable on a STACK-only corpus.
- **The `sheet_map_source` distribution** (13 drawing_index, 2
  title_blocks) reflects how often STACK-produced bidsets clear
  Filter 1's drawing-index gate. Non-STACK producers may shift this
  distribution materially in either direction.
- **The Filter 4 quality-gate aggressive removal** (Chewy 651/823, etc.)
  may reflect STACK-overlay text-block proliferation that wouldn't
  appear on a CAD-direct PDF.
- **Wendy's runtime outlier** (576s for 64 pages) is a known STACK
  pathology per TracePoint CLAUDE.md Step 56.

**Tuning decisions, threshold adjustments, and v0.3 work await non-STACK
bidsets entering the corpus.** Do NOT propose changes — to gates,
thresholds, regex patterns, or the four-layer architecture — based on
this corpus alone. The next 15-bidset sweep should include at least 4
non-STACK producers before any aggregate finding from this report is
read as a v0.3 mandate.

---

— end of validation report —
