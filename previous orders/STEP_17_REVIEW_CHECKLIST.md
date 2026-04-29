# Phase 2 v0.2 — Step 17 Review Checklist

**Inputs:** 15 JSONs at `backend/test_fixtures/v0.2_outputs/<bidset_id>.json`, each a `PlanSetContext.to_json()` dump from Step 16.
**Source authority:** `MARCH_ORDERS_v0_2.md` §0 (symptoms) and §5 Step 17 (pass criteria).
**Final output:** `backend/V0_2_VALIDATION.md` with per-bidset PASS/FAIL tables and any anomalies.
**Gate threshold (per §5 Step 17 close):** ≥3 of 4 symptoms PASS on ≥80% of applicable bidsets. The 4th may have remaining issues; document, do NOT fix in v0.2.

---

## Caveat on field paths

This checklist is constructed from §0 + §5 Step 17 of the march orders, which describe schema shape in prose. The literal JSON keys produced by `PlanSetContext.to_json()` should be verified against the first Step 16 JSON before Daniel works the full 15. Field-path mismatches (e.g., `field_sources.project_name.confidence` vs `field_confidences.project_name`) are mechanical — fix in this checklist, not in the JSONs.

If a path doesn't match what's in the JSONs, the fix is to grep `core/context.py` for the actual `to_json()` body and update this document. Do NOT modify the JSONs to match this document.

---

## Symptom 1 — Project Metadata Quality

**v0.1 baseline:** 13/15 had `project_name` populated with garbage strings ("DIRECTORY", "TEAM", "SITE", "INFORMATION") because field-presence promotion was based on populated-not-quality.

**v0.2 expected:** `project.field_sources` tracks origin AND confidence per populated field. Cover-page parsing yields confidence 0.5; title-block fallback yields 0.3. The string values may still be imperfect — TracePoint acknowledges cover-page parsing is the long-term fix and v0.2 doesn't ship that.

### Fields to inspect (per JSON)

- `project.project_name` — string or null
- `project.field_sources.project_name.source` — string identifier
- `project.field_sources.project_name.confidence` — float

### Confidence constants (from `core/context.py`)

| Constant | Value | Meaning |
|---|---|---|
| CONFIDENCE_EXPLICIT | 0.9 | title-block keyword match |
| CONFIDENCE_INFERRED | 0.5 | cover-page parsing |
| CONFIDENCE_WEAK | 0.3 | title-block fallback |

### Binary pass question (per bidset)

> When `project.project_name` is non-null, is `project.field_sources["project_name"].confidence` populated with a numeric value?

### Pass criterion

YES on all 15 bidsets where `project_name` is non-null.

### EXPLICIT NON-CRITERION

Do NOT assert on string quality. `"DIRECTORY"` with `confidence=0.3` is still a Symptom-1 PASS for v0.2. The string-quality fix is a v0.3 ticket against cover-page parsing.

### Per-bidset row format

| bidset_id | project_name | source | confidence | pass? |
|---|---|---|---|---|

---

## Symptom 2 — One Detected System Per Bidset

**v0.1 baseline:** Taco Bell tagged with 6 distinct membrane chemistries simultaneously; ~40 of 47 detected systems across the corpus had the wrong attachment.

**v0.2 expected:** `project_scope.detected_system` is a SINGLE STRING (or None). `_resolve_scope_system` does weighted voting and produces ONE winner.

### Fields to inspect

- `project_scope` — object or null
- `project_scope.detected_system` — string or null (NEVER a list)
- `project_scope.system_confidence` — float
- `project_scope.scope_pages` — list of page indices

### Binary pass questions

**For Taco Bell Weeki Wachee:**
> Is `project_scope.detected_system` exactly ONE of `"tpo"`, `"pvc"`, `"epdm"`, `"modified_bitumen"`, `"built_up"`, or `"metal_panel"`? (Not a list. Not null.)

> Is `project_scope.system_confidence >= 0.7`?

**For AutoZone Jacksonville AND AutoZone Vero Beach (both):**
> Is `project_scope` either null OR has `detected_system == null`?

> Is `project_scope.scope_pages` an empty list (or absent)?

These two are the negative case — correctly identifying that no roofing scope exists, because both bidsets are for non-roofing-primary work.

**For all 15 bidsets in aggregate:**
> Across every bidset, is `type(project_scope.detected_system)` either `str` or `None`? (Never `list`.)

### Pass criterion

All four questions return YES on the relevant bidsets.

### Per-bidset row format

| bidset_id | detected_system | type | system_confidence | scope_pages count | pass? |
|---|---|---|---|---|---|

---

## Symptom 3 — Drawing Pages and Scope Pages Are Separate Categories

**v0.1 baseline:** 78 of 95 (82%) `roof_plan` classifications came from page-text matches, not title-block matches. Spec-book pages mentioning "ROOF PLAN" got classified as roof plans, then harvested for scope evidence — which is how Taco Bell ended up with 6 membrane chemistries.

**v0.2 expected:** Scope evidence comes from `project_scope.scope_pages` (built by `run_scope_scanner` with the `vector_count > 500: continue` HARD GATE), NOT from `pages[i].page_type == ROOF_PLAN`. The two are now separate categories.

### Fields to inspect

- `pages[i].page_type` — string (e.g., "roof_plan", "site_plan", "spec_book")
- `pages[i].confidence` — float (only `0.9` when keyword matched title block)
- `pages[i].vector_count` — int (used by scope scanner's hard gate)
- `project_scope.scope_pages` — list of page indices

### Binary pass questions

**For Taco Bell page 18 specifically (the spec book):**
> Does `18` appear in `project_scope.scope_pages`?

(Whether `pages["18"].page_type == "roof_plan"` is acceptable either way — page 18 may legitimately match as a roof_plan keyword AND be in scope_pages because the scope scanner accepted it via the text-heavy path. The two channels are independent.)

**For all 15 bidsets in aggregate:**

Compute:
```
total_roof_plan_pages = sum across all 15 JSONs of (pages where page_type == "roof_plan")
explicit_roof_plan_pages = same, filtered to confidence >= 0.9
ratio = explicit_roof_plan_pages / total_roof_plan_pages
```

> Is `ratio > 0.18`? (v0.1 was 17/95 ≈ 0.18.)

### Pass criterion

Taco Bell page 18 in `scope_pages` AND aggregate explicit-confidence ratio higher than v0.1's baseline.

### Aggregate counter table

| metric | v0.1 | v0.2 | pass? |
|---|---|---|---|
| roof_plan pages total | 95 | ? |  |
| roof_plan pages with confidence ≥ 0.9 | 17 | ? |  |
| ratio | 0.18 | ? |  |

---

## Symptom 4 — Sheet Number Extraction Reliability

**v0.1 baseline:** Vine Street had 7 pages reporting sheet `TS9D` (a firm name, not a sheet number). AutoZone Vero pages reported `LC0000298` and `LA6667318` (license numbers). A6.1 ROOF PLAN was absent from sheet_map entirely.

**v0.2 expected:** Filter 1 first attempts drawing-index parsing (requires 10+ unique sheet numbers in early pages), then falls back to title-block scanning. Sheet numbers come from a structured source, not OCR-style scraping.

### Fields to inspect

- `sheet_map` — dict, page index → sheet number string
- `sheet_map_source` — string identifier ("drawing_index", "title_block_scan", or other)

### Binary pass questions

**For Vine Street Retail Center:**
> Is `sheet_map_source == "drawing_index"`?

> Does `sheet_map` contain real architectural sheet numbers (e.g., `A-1.0`, `A-1.3`, `A6.1`)?

> Does `sheet_map` exclude the string `"TS9D"` from its values?

**For all 15 bidsets:**

For each bidset, compute `max(Counter(sheet_map.values()).values())` — the highest count of any single string value.

> Is `max-value-count <= 2` for every bidset, EXCEPT the known legitimate multi-building cases (Bearss campus)?

### Pass criterion

Vine Street: sheet_map_source is `drawing_index`, real sheet numbers present, no `TS9D`. Across all 15, max-duplicate-value count ≤ 2 except documented multi-building cases.

### Per-bidset row format

| bidset_id | sheet_map_source | sheet_map size | max-value-count | TS9D present? | pass? |
|---|---|---|---|---|---|

---

## Final Roll-Up

| Symptom | Pass rate | Threshold | Status |
|---|---|---|---|
| 1 — project metadata field_sources tracking | x/15 | ≥80% (≥12/15) |  |
| 2 — single detected_system, list never | x/x relevant | 100% on listed cases |  |
| 3 — explicit-confidence roof_plan ratio | aggregate | > 0.18 |  |
| 4 — sheet_map cleanliness | x/15 | ≥80% (≥12/15) |  |

### Gate decision

- **≥3 of 4 PASS at the listed thresholds:** Step 17 ships. Document the 4th in V0_2_VALIDATION.md as a known issue, do NOT fix in v0.2.
- **<3 of 4 PASS:** STOP. Open a Discovered Issue. Do NOT silently extend v0.2 scope to fix; that's a v0.2.1 conversation.

---

## Things to write down in V0_2_VALIDATION.md

For every bidset:
- The four per-symptom rows above
- Any anomalies (unexpected null fields, crashed run_dispatch outputs, dispatch_warnings worth flagging)
- Runtime per bidset if obviously outlier (TracePoint baseline ~22 min for 15 = ~1.5 min/bidset average)

Do NOT write proposed fixes in V0_2_VALIDATION.md. Per §5 Step 17: "Do NOT propose fixes — just record measurements." Fixes belong in DISCOVERED_ISSUES.md or in the next version's planning, not in the validation document.

---

## What this checklist deliberately does NOT do

- Does not assert string quality of `project_name` (Symptom 1) — v0.3 territory
- Does not validate the contents of `attachment` per system (Symptom 2 surrogate, replaced by single-detected_system check)
- Does not inspect `cross_refs`, `legends`, or `dispatch_warnings` for correctness — those are Step 16 sweep-completion checks, already gated
- Does not compare runtime against any v0.1 baseline — v0.2 is a port, not a perf optimization

If anything in this list looks like it should be checked, it isn't in v0.2 scope. Park it for v0.2.1 or v0.3 per the §10 trajectory.
