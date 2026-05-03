# G.2 Track 1 — Corpus Scout Report

Branch: `phase2-v0.3-G2-discipline-fallback` from `cef1ca7` (head of `phase2-v0.3-recon-cascade-map`).
Mode: read-only. Sacred floor 230/19/0 at start, 230/19/0 at end. Vault SHA-1s unchanged for all four.

**Headline finding**: the march-orders premise about Silverleaf is incorrect. Pages 12/13/38/39 have `sheet_number=None` and `discipline=?` (UNKNOWN) — not `S` — so the proposed `_DISCIPLINE_FALLBACK` patch *cannot* drop Silverleaf's UNKNOWN count and the Track 2 Silverleaf success criterion as written is not achievable by this patch alone. Track 2 should be rescoped or paused for Daniel's review before proceeding.

The corpus signal supports a fallback for `FP → MEP_PLAN` and an extension of `_DISCIPLINE_MAP` (separate from the proposed patch). It does not support fallbacks for `S`, `A`, `C`, `G`, or `L` — those scatter too widely or have insufficient samples.

---

## 1. Bidset list and per-bidset UNKNOWN counts

| Bidset | Total pages | All UNKNOWN | UNKNOWN with sheet | Non-MEP UNKNOWN-with-sheet | Disciplines |
|--------|------------:|------------:|-------------------:|---------------------------:|-------------|
| Auto Zone #10891 — Jacksonville | 28 | 15 | 1 | 1 | A |
| Auto Zone Vero Beach, FL | 61 | 30 | 0 | 0 | — |
| **B2607 AEA Silverleaf** | 40 | 4 | **0** | **0** | — (all four pages have `sheet_number=None`) |
| Bearss Ave Distribution Center | 91 | 1 | 0 | 0 | — |
| Chewy Vet Care — London Square | 93 | 3 | 0 | 0 | — |
| Chipotle — Tarpon Springs (Shell) | 39 | 3 | 3 | 3 | S × 3 |
| Hampshire Self Storage | 86 | 13 | 4 | 4 | FP × 4 |
| Panda Express — Naples | 98 | 1 | 1 | 1 | A |
| Panda Express — San Antonio | 38 | 0 | 0 | 0 | — |
| Panda Express Bradenton | 59 | 0 | 0 | 0 | — |
| Panda Express Hialeah Gardens | 101 | 4 | 1 | 1 | C |
| Shoppes at Avalon — Spring Hill | 97 | 34 | 2 | 2 | A × 2 |
| Taco Bell — Weeki Wachee | 88 | 3 | 2 | 2 | ? × 2 (H prefix) |
| Vine Street Retail Center | 138 | 32 | 0 | 0 | — |
| Wendy's — Fort Myers | 64 | 14 | 1 | 1 | ? × 1 (QP prefix) |
| **TOTALS** | 1121 | 157 | 15 | 15 | A=4, S=3, C=1, FP=4, ?=3 |

Filters completed on every bidset: `[filter_1, filter_2, filter_4, filter_3, filter_5]`. No dispatch errors.

Note: the recon-cited Silverleaf premise ("four UNKNOWN pages 12/13/38/39, sheet-number discipline is S") does not match the actual dispatch output. The four pages are UNKNOWN, but they have `sheet_number=None` and `discipline=?` (see §5).

---

## 2. Discipline-by-discipline breakdown

### 2.1 Architectural (A) — 4 pages, 3 bidsets, **scatter**

| Bidset | Sheet | Title (pc.title) | Apparent type from page text |
|--------|-------|------------------|-----------------------------|
| Auto Zone Jacksonville | AR96268 | "T" | Cover/title shell page (HELT DESIGN architects boilerplate, no plan content) |
| Panda Express Naples | A-102 | "ROUGH - IN PLUMBING PLAN" | Floor plan with plumbing overlay (dimensions, room layout, floor sinks) |
| Shoppes at Avalon | A-102 | "DIMENSIONED BUILDING PLAN" | Floor plan (heavy dimension callouts) |
| Shoppes at Avalon | A-602 | "WINDOW TYPES" | Window type schedule / elevation page |

Three different "should-be" page types across four pages: COVER, FLOOR_PLAN, FLOOR_PLAN, SCHEDULE_SHEET (or ELEVATION). Architectural is also the broadest discipline in any bid set — a wrong fallback misclassifies large numbers of pages downstream when keyword classification fails on schedule sheets, elevations, sections, details, life-safety pages, etc.

**Recommendation: no fallback for A.** Risk of misclassification outweighs benefit on this corpus.

The classification miss for "DIMENSIONED BUILDING PLAN" is interesting — the keyword rules at `_PAGE_TYPE_RULES` (line 105) include `["FLOOR PLAN", "SLAB PLAN"]` for FLOOR_PLAN. "DIMENSIONED BUILDING PLAN" doesn't match either. Likewise "WINDOW TYPES" doesn't match `["SCHEDULE"]`. These are keyword-rule gaps, not fallback gaps.

### 2.2 Structural (S) — 3 pages, 1 bidset (Chipotle), **scatter**

| Bidset | Sheet | Title (pc.title) | Apparent type |
|--------|-------|------------------|---------------|
| Chipotle Tarpon | S001 | "STRUCTURAL NOTES" | General notes / specs sheet |
| Chipotle Tarpon | S301 | "STEEL ELEVATIONS AND DETAILS" | Detail / elevation sheet |
| Chipotle Tarpon | S200 | "ROOF FRAMING PLAN" | Framing plan |

Three different "should-be" types across three pages: GENERAL_NOTES (or SCHEDULE_SHEET), DETAIL_SHEET (or ELEVATION), FRAMING_PLAN. Single-bidset sample.

The classification misses here trace to a `_classify_page_type` quirk: it reads `tb_text` (title-block-quadrant text only) and `full_text`, not `pc.title`. For Chipotle's S-series pages, the title block quadrant is either empty or contains only `"S301"` etc., and the full-text first match doesn't carry the title keywords. So `"ROOF FRAMING PLAN"` gets classified UNKNOWN even though the title attribute has it.

**Recommendation: no fallback for S.** Three pages, three different types, one bidset — not enough signal to commit to any single fallback. Forcing `S → FRAMING_PLAN` would be 1/3 right. Forcing `S → DETAIL_SHEET` would be 1/3 right. The keyword-rule fix (extend `_PAGE_TYPE_RULES` with structural keywords or read `pc.title`) is a better lever than a discipline fallback.

### 2.3 Civil (C) — 1 page, 1 bidset, **insufficient sample**

| Bidset | Sheet | Title | Apparent type |
|--------|-------|-------|---------------|
| Panda Express Hialeah | C04.2 | "UTILITY NOTES" | Utility notes / general-notes sheet |

One sample. Cannot generalize.

**Recommendation: no fallback for C.** Defer to a larger civil sample.

### 2.4 Fire Protection (FP) — 4 pages, 1 bidset (Hampshire), **clusters on MEP_PLAN**

| Bidset | Sheet | Title (pc.title) | Apparent type |
|--------|-------|------------------|---------------|
| Hampshire | FP0.1 | "" (full text: "FIRE SPRINKLER SPECIFICATIONS") | Spec sheet (general notes / specifications) |
| Hampshire | FP1.1 | "" (full text: "FIRST FLOOR FIRE SPRINKLER PLAN") | MEP-style plan |
| Hampshire | FP1.2 | "" (full text: "SECOND FLOOR FIRE SPRINKLER PLAN") | MEP-style plan |
| Hampshire | FP1.3 | "" (full text: "THIRD FLOOR FIRE SPRINKLER PLAN") | MEP-style plan |

Three of four are sprinkler plans, structurally identical to MEP plans. The fourth (FP0.1) is a spec sheet but `MEP_PLAN` for it is not catastrophic — fire-protection specs are MEP-domain work.

**Recommendation: `FP → MEP_PLAN`.** 4/4 acceptable. Single bidset is a weak sample, but the convergence is consistent with the existing MEP fallback rationale (M/E/P all map to MEP_PLAN even though their specific page types differ).

### 2.5 General (G) — 0 pages, **no signal**

No qualifying UNKNOWN-with-sheet pages in the corpus for the G prefix.

**Recommendation: no fallback for G.**

### 2.6 Landscape (L) — 0 pages, **no signal**

No qualifying UNKNOWN-with-sheet pages in the corpus for the L prefix.

**Recommendation: no fallback for L.**

### 2.7 Unmapped (`?` — prefix not in `_DISCIPLINE_MAP`) — 3 pages, **better fixed via `_DISCIPLINE_MAP` extension**

| Bidset | Sheet | Title | Apparent type |
|--------|-------|-------|---------------|
| Taco Bell Weeki Wachee | H5.2 | "CAPTIVEAIRE DRAWINGS" | HVAC equipment cut-sheets (mechanical) |
| Taco Bell Weeki Wachee | H5.3 | "CAPTIVEAIRE DRAWINGS" | HVAC equipment cut-sheets (mechanical) |
| Wendy's Fort Myers | QP0222 | "" (full text: "PLUMBING SANITARY PLAN") | Plumbing plan |

`H` prefix → mechanical/HVAC. `QP` prefix → quarry-plumbing or some shop-drawing plumbing convention.

**Recommendation: extend `_DISCIPLINE_MAP` rather than add `Discipline.UNKNOWN → MEP_PLAN` to the fallback.** Adding `Discipline.UNKNOWN → MEP_PLAN` would fire on every page with no recognized prefix, which over-shoots the corpus signal. A targeted `_DISCIPLINE_MAP` extension (`"H" → MECHANICAL`, `"QP" → PLUMBING`) lets the existing MEP fallback catch them via the M/E/P branch.

This recommendation is **out of scope for Track 2's proposed patch** but is the higher-leverage change for these three pages. Daniel's call: include or defer.

---

## 3. Final decision matrix

| Discipline | Discipline enum | Sample count | Recommendation | PageType fallback |
|------------|-----------------|--------------|----------------|-------------------|
| MECHANICAL | `Discipline.MECHANICAL` | (existing) | Keep | `PageType.MEP_PLAN` |
| ELECTRICAL | `Discipline.ELECTRICAL` | (existing) | Keep | `PageType.MEP_PLAN` |
| PLUMBING | `Discipline.PLUMBING` | (existing) | Keep | `PageType.MEP_PLAN` |
| FIRE_PROTECTION | `Discipline.FIRE_PROTECTION` | 4 pages, 1 bidset | **Add** | `PageType.MEP_PLAN` |
| ARCHITECTURAL | `Discipline.ARCHITECTURAL` | 4 pages, 3 bidsets | No fallback (scatter) | — |
| STRUCTURAL | `Discipline.STRUCTURAL` | 3 pages, 1 bidset | No fallback (scatter) | — |
| CIVIL | `Discipline.CIVIL` | 1 page | No fallback (insufficient) | — |
| GENERAL | `Discipline.GENERAL` | 0 pages | No fallback | — |
| LANDSCAPE | `Discipline.LANDSCAPE` | 0 pages | No fallback | — |
| UNKNOWN | `Discipline.UNKNOWN` | 3 pages (`H`, `QP`) | No fallback (handle via `_DISCIPLINE_MAP` extension instead) | — |

**Net change vs. current behavior**: +1 entry (`FP → MEP_PLAN`) covering 4 pages on 1 bidset (Hampshire). Zero coverage delta for the other 14 bidsets.

---

## 4. New PageType enum values needed

**None.** The single recommended new fallback (`FP → MEP_PLAN`) reuses an existing enum value.

---

## 5. Silverleaf check

> **Specific Silverleaf check: do pages 12, 13, 38, 39 land in fallback coverage with the recommended matrix?**

**No.** The proposed `_DISCIPLINE_FALLBACK` table cannot reach Silverleaf pages 12/13/38/39 because:

| Page | `pc.sheet_number` | `pc.discipline` | Why fallback misses |
|------|-------------------|-----------------|---------------------|
| 12 | `None` | `?` (UNKNOWN) | Not keyed in `_DISCIPLINE_FALLBACK` |
| 13 | `None` | `?` (UNKNOWN) | Not keyed in `_DISCIPLINE_FALLBACK` |
| 38 | `None` | `?` (UNKNOWN) | Not keyed in `_DISCIPLINE_FALLBACK` |
| 39 | `None` | `?` (UNKNOWN) | Not keyed in `_DISCIPLINE_FALLBACK` |

The patch's gating condition is `disc in _DISCIPLINE_FALLBACK`. With `disc = Discipline.UNKNOWN` for all four pages, none of them qualify for fallback under any matrix that doesn't include `Discipline.UNKNOWN` — and including `Discipline.UNKNOWN` would over-shoot (every page with an unrecognized or missing prefix would be relabeled).

### 5.1 Root cause: Filter 1 sheet detection

The actual problem on Silverleaf 12/13/38/39 is in **Filter 1**, not Filter 2's discipline fallback:

Verified via `_SHEET_NUM_RE.finditer(full_text)` on each page:

| Page | Sheet number present in page text | `_find_sheet_on_page` result | Title-block-quadrant blocks |
|------|-----------------------------------|------------------------------|------------------------------|
| 12 | `P201` | `None` | 0 |
| 13 | `P301` | `None` | 0 |
| 38 | `M101` | `None` | 1 (only "NOTES:") |
| 39 | `M102` | `None` | 1 (only "NOTES:") |

The sheet numbers are present in the page text (one match each), but `_find_sheet_on_page` returns `None` because:
- Strategy 3 (short title-block text) fails — the bottom-right quadrant is empty or contains unrelated text on these pages
- Strategy 4 (last 10 lines, short text) fails — the sheet number is not in the trailing lines of the full text

Silverleaf's `sheet_map_source` is `"title_blocks"` (no drawing index found), so strategies 1, 2, and 5 (which depend on `known_keys`) are skipped.

If those four pages had a populated `sheet_number` after Filter 1, then a `P → MEP_PLAN` (existing) and `M → MEP_PLAN` (existing) fallback would catch them — but Track 2 as scoped only modifies Filter 2's fallback, not Filter 1's detection.

### 5.2 Implication for Track 2

Track 2's Silverleaf success criterion ("UNKNOWN page count must DROP from 4 to a lower number") is **not achievable** by the proposed patch alone. Three options for Daniel:

**Option A — Proceed with reduced scope.** Ship `FP → MEP_PLAN` for the 4 Hampshire pages. Drop the Silverleaf success criterion from this phase. Filter 1 detection becomes a separate phase (G.3 or similar).

**Option B — Pause Track 2 and rescope.** Re-frame the phase as "Filter 1 sheet-detection improvements" using Silverleaf as the test case. The discipline fallback table becomes a smaller follow-up.

**Option C — Combine.** Ship both: (1) Filter 1 fix that finds sheet numbers in non-quadrant locations on Silverleaf 12/13/38/39, then (2) the small `FP → MEP_PLAN` fallback. Two commits, both small. The Filter 1 fix is the larger surface-area change and should drive its own scout work first.

**Recommendation**: B or C. Option A still ships value (Hampshire FP coverage) but breaks the success criterion as written, which is a stop condition.

---

## 6. Bearss byte-equivalence note

The Bearss bidset has 1 total UNKNOWN page and **0 non-MEP UNKNOWN-with-sheet pages**. Adding `FP → MEP_PLAN` cannot affect Bearss because there are no FP pages in that bidset. Bearss byte-equivalence (769/177/31/24) is preserved by Track 2 as long as no other code paths change. Verified pre-patch only via the corpus survey; no dispatch run was executed against Bearss specifically in Track 1.

---

## 7. Vault SHA-1 verification (post-Track-1)

```
2a708d193ac5247472d589252bbc3766ced9041f  backend/core/dispatch_gate.py
ae9e5b284191b45de419faacf11771da27a548f9  backend/core/roofing_module.py
52c014421915ec6a66b4a6860b71a0a3274920f2  backend/core/glazing_module.py
78f71d9030cde3b173389603f5f39bd6bedaac07  backend/core/debug_module.py
```

All four unchanged from session start. Sacred floor 230/19/0 unchanged.

---

## 8. STOP — pending Daniel's call

Track 2 was conditionally gated ("hold for explicit go-ahead from Daniel via this chat"). The Silverleaf premise mismatch is a stop signal under the spirit of:

> Track 1 finds that pages within a discipline scatter so widely that no single fallback PageType makes sense. STOP, report — Daniel may want to defer or rescope.

…and under the harder Track-2 stop:

> Silverleaf UNKNOWN count doesn't drop post-patch. STOP, Track 1's matrix was wrong, do not housekeep.

Track 2's Silverleaf criterion would fail with any matrix this corpus supports. Reporting and stopping. Awaiting direction.

### Files that would need to change for each option (for planning)

| Option | core/context.py | core/dispatch_gate.py | tests |
|--------|-----------------|------------------------|-------|
| A — FP fallback only | unchanged | `_DISCIPLINE_FALLBACK` dict added, lines 463–466 replaced | one new test in `test_dispatch.py` |
| B — pause | unchanged | unchanged | unchanged |
| C — Filter 1 fix + FP fallback | unchanged | `_find_sheet_on_page` extended (search non-quadrant areas), plus A | tests for both fixes |

No code changes have been made on this branch yet. `git status` shows only `backend/G_2_CORPUS_SCOUT_REPORT.md` as new.
