# G.2 Hard Gate Report — Corpus-wide Classifier Upgrade

**Date:** 2026-05-03
**Branch:** `phase2-v0.3-G2-classifier-upgrade`
**Sacred floor pre:** 230/19/0
**Sacred floor post:** 237/19/0 (+7 new classifier tests)

---

## Changes Made

1. **`_classify_page_type`** (dispatch_gate.py:421): added `title` parameter; search order is now tb_text → pc.title → full_text (three passes through `_PAGE_TYPE_RULES`).
2. **`_PAGE_TYPE_RULES`** (dispatch_gate.py:105): extended with corpus-validated keywords:
   - `SCHEDULE_SHEET`: added `"WINDOW TYPES"`, `"DOOR TYPES"`
   - `FLOOR_PLAN`: added `"DIMENSIONED BUILDING PLAN"`, `"BUILDING PLAN"`
   - `FRAMING_PLAN`: added `"ROOF FRAMING PLAN"`, `"FOUNDATION PLAN"`
   - `MEP_PLAN`: added `"FIRE SPRINKLER PLAN"`, `"FIRE SPRINKLER"`, `"PLUMBING SANITARY PLAN"`
   - `DETAIL_SHEET`: added `"ELEVATIONS AND DETAILS"`, `"STEEL ELEVATIONS"` (moved before ELEVATION rule for longer-match-first)
   - `GENERAL_NOTES`: added `"STRUCTURAL NOTES"`, `"UTILITY NOTES"`, `"FIRE PROTECTION SPECIFICATIONS"`
3. **Filter 2 caller** (dispatch_gate.py:446): sheet_map lookup moved before `_classify_page_type` call so `title` is available; `entry.page_type` update moved after classify.

---

## Results

| Bidset | Baseline UNKNOWN-with-sheet | Post-patch | Expected | Delta | Status |
|--------|---:|---:|---:|---:|--------|
| Bearss Ave Distribution Center | 0 | 0 | 0 | +0 | PASS |
| Hampshire Self Storage | 4 | 0 | 0 | -4 | PASS |
| Chipotle — Tarpon Springs | 3 | 0 | 0 | -3 | PASS |
| Shoppes at Avalon | 2 | 0 | 0 | -2 | PASS |

---

## Bearss Byte-Equivalence

- roofing_fields: 769 (expected 769)
- glazing_items: 177 (expected 177)
- door_items: 31 (expected 31)
- storefront_items: 24 (expected 24)
- **Status: PASS**

Verified via `run_dispatch(BEARSS, storage="auto")`. Trade module outputs byte-identical to G.1 baseline.

---

## Per-page Detail (named pages from corpus scout)

| Bidset | Page | Sheet | Title | Post-patch type | Expected type |
|--------|------|-------|-------|----------------|---------------|
| Hampshire | 81 | FP0.1 | (empty) | mep_plan | MEP_PLAN |
| Hampshire | 83 | FP1.1 | (empty) | mep_plan | MEP_PLAN |
| Hampshire | 84 | FP1.2 | (empty) | mep_plan | MEP_PLAN |
| Hampshire | 85 | FP1.3 | (empty) | mep_plan | MEP_PLAN |
| Chipotle Tarpon | (S001) | S001 | STRUCTURAL NOTES | general_notes | GENERAL_NOTES |
| Chipotle Tarpon | (S301) | S301 | STEEL ELEVATIONS AND DETAILS | detail_sheet | DETAIL_SHEET |
| Chipotle Tarpon | (S200) | S200 | ROOF FRAMING PLAN | framing_plan | FRAMING_PLAN |
| Shoppes Avalon | (A-102) | A-102 | DIMENSIONED BUILDING PLAN | floor_plan | FLOOR_PLAN |
| Shoppes Avalon | (A-602) | A-602 | WINDOW TYPES | schedule_sheet | SCHEDULE_SHEET |

Note: Hampshire pages have empty `pc.title` (Filter 1 didn't extract titles for these pages). Classification achieved via `full_text` keyword "FIRE SPRINKLER" → MEP_PLAN. Chipotle and Shoppes pages have populated `pc.title` from sheet_map — classification achieved via the new `pc.title` search pass.

---

## Wall-clock

- Bearss: 470.8s (91 pages, storage="auto")
- Hampshire: 327.6s (86 pages)
- Chipotle Tarpon: 63.6s (39 pages)
- Shoppes Avalon: 123.6s (97 pages)

---

## Hard Gate Criteria

1. Bearss: UNKNOWN-with-sheet 0→0 AND trade outputs byte-identical (769/177/31/24): **PASS**
2. Hampshire: UNKNOWN-with-sheet 4→0: **PASS**
3. Chipotle Tarpon: UNKNOWN-with-sheet 3→0: **PASS**
4. Shoppes Avalon: UNKNOWN-with-sheet 2→0: **PASS**
5. No bidset UNKNOWN-with-sheet INCREASE: **PASS** (all deltas ≤0)

---

## Vault SHA-1 Verification

| File | Pre | Post | Status |
|------|-----|------|--------|
| dispatch_gate.py | 2a708d19... | (changed — expected) | EXPECTED |
| roofing_module.py | ae9e5b28... | ae9e5b28... | UNCHANGED |
| glazing_module.py | 52c01442... | 52c01442... | UNCHANGED |
| debug_module.py | 78f71d90... | 78f71d90... | UNCHANGED |
| roofing_vocabulary.py | ec6c17f8... | ec6c17f8... | UNCHANGED |
| glazing_vocabulary.py | 64249c8e... | 64249c8e... | UNCHANGED |

---

## Karpathy Step Proof

7 tests written and run BEFORE the code change — all 7 FAILED:
- 3 TypeError (function didn't accept `title` parameter)
- 4 AssertionError (keywords not in rules, returned UNKNOWN)

After the fix: all 7 PASS. Full suite: 237/19/0.

---

## Deviations from March Orders

1. **"FIRE SPRINKLER SPECIFICATIONS" → "FIRE PROTECTION SPECIFICATIONS"**: The corpus scout reported Hampshire FP0.1 as having "FIRE SPRINKLER SPECIFICATIONS" in full_text; actual text is "FIRE PROTECTION SPECIFICATIONS:". Corrected in implementation.
2. **"FIRE SPRINKLER" added as standalone keyword**: The corpus scout stated Hampshire FP1.1-1.3 have "FIRST FLOOR FIRE SPRINKLER PLAN" etc. as full strings. Actual page text splits these across lines ("FIRE SPRINKLER " on one line, "FIRST FLOOR" and "PLAN" on separate lines). Added "FIRE SPRINKLER" as a standalone MEP_PLAN keyword; validated that it doesn't regress Bearss (6 Bearss pages contain "FIRE SPRINKLER" but all are already classified via higher-priority rules).
3. **FP0.1 classified as MEP_PLAN (not GENERAL_NOTES)**: March orders suggested FP0.1 was a spec sheet (→ GENERAL_NOTES). Per corpus scout §2.4: "MEP_PLAN for it is not catastrophic — fire-protection specs are MEP-domain work" and "4/4 acceptable." The "FIRE SPRINKLER" keyword fires before "FIRE PROTECTION SPECIFICATIONS" due to rule ordering. Net result is all 4 FP pages as MEP_PLAN, which matches the corpus scout's §3 recommendation.

---

## Overall: **PASS (4/4)**
