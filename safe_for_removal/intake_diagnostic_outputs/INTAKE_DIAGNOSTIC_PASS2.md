# Intake Diagnostic — Pass 2 (per-hit context inspection)

**Date:** 2026-04-27
**Scope:** 10 STACK bidsets where pass 1 reported `manufacturer_hits_positive_total > 0` AND `scope_pages = []`. 35 per-page-unique manufacturer hits total.
**Pipeline state:** v0.2 dispatch outputs unchanged from commit `441896a`; this pass scans the same source PDFs with the same vocabulary.
**Diagnostic script:** `backend/scripts/intake_diagnostic_pass2.py`
**Machine-readable summary:** `backend/test_fixtures/intake_diagnostic_pass2_summary.json`

This document is observation only. It does NOT propose tuning, fixes, or
v0.3 work.

---

## What pass 2 measures

For each manufacturer hit identified in pass 1, this pass captures:

| Field | What it records |
|---|---|
| `bidset_id`, `page_index`, `sheet_number`, `page_type` | Identity + classification (from existing JSON) |
| `canonical`, `matched_name` | Manufacturer canonical (from `MANUFACTURERS`) and the literal substring that matched (canonical, alias, or product name) |
| `context_80` | 40 chars before + match + 40 chars after, whitespace-collapsed |
| `is_in_title_block_zone` | Bbox center in bottom-right quadrant (x ≥ 60% of page width AND y ≥ 60% of page height — same fractions used by `dispatch_gate._get_title_block_text()`) |
| `is_in_drawing_index` | Page is the bidset's drawing-index page, replicated from Filter 1's gate (10+ unique sheet-number patterns within first 10 pages) |
| `is_repeating_text` | Same canonical appears on >5 distinct pages of the same bidset (boilerplate threshold) |
| `nearby_spec_section_ref` | Any Division 7 section reference within ±200 chars of the match |
| `negated` | Any of {"NOT ACCEPTABLE", "NOT PERMITTED", "NOT APPROVED"} within ±50 chars (verbatim from pass 1's negation rule) |

Heuristics used (none extend the seed vocabulary):

- Title-block zone: `x_center / page_w ≥ 0.6` AND `y_center / page_h ≥ 0.6`. Matches `dispatch_gate._get_title_block_text()`'s quadrant.
- Drawing-index page: replicates `_find_drawing_index_page()`'s 10-unique-sheets-in-first-10-pages gate.
- Repeating text: per-canonical page count > 5.
- Spec-section radius: 200 chars.
- Negation radius: 50 chars (matches pass 1).

---

## Aggregate — where do manufacturer hits actually live?

Single-label classification, priority order: drawing_index_page > title_block_zone > repeating_text_boilerplate > near_spec_section > negation_window > body_text_other.

| Location | Hits | % of 35 |
|---|---:|---:|
| body_text_other | 31 | 88.6% |
| title_block_zone | 2 | 5.7% |
| drawing_index_page | 1 | 2.9% |
| negation_window | 1 | 2.9% |
| repeating_text_boilerplate | 0 | 0.0% |
| near_spec_section | 0 | 0.0% |

Of the 35 hits across 10 bidsets:
- 0 of 35 manufacturer hits had a Division 7 spec-section reference within ±200 chars
- 0 of 35 manufacturer canonicals appeared on more than 5 pages of the same bidset
- 1 of 35 fell within a negation window (Shoppes Firestone, the same hit pass 1 caught)
- 3 of 35 had spatial signals (1 drawing-index, 2 title-block-zone), all on Bearss

---

## Per-bidset sections

### chewy-vet-care-london-square-miami-jdr-fixtures

`drawing_index_page=0`, `sheet_map_source=drawing_index`. 9 hits, all `body_text_other`.

| page | sheet | page_type | canonical | matched | flags | context (40 before / 40 after) |
|---:|---|---|---|---|---|---|
| 40 | A908 | elevation | Tremco | Tremco | - | …Corporation - Building Components. c. **Tremco** Incorporated. C. Silicone, Nonstaining,… |
| 40 | A908 | elevation | Sika Sarnafil | Sika | - | …he following: a. Pecora Corporation. b. **Sika** Corporation - Building Components. c.… |
| 43 | A911 | schedule_sheet | CertainTeed | Saint-Gobain | - | …mited to the following: a. CertainTeed; **SAINT-GOBAIN**. b. Georgia-Pacific Gypsum LLC. c. US… |
| 60 | P-600 | cover | Tremco | Tremco | - | …es Inc., United States Gypsum Company, **Tremco**, or 3M Corp. Through and Membrane Penet… |
| 61 | P-601 | elevation | Johns Manville | Johns Manville | - | …CertainTeed Corp., Knauf Insulation, **Johns Manville** or Owens Corning. Provide Insulation th… |
| 61 | P-601 | elevation | CertainTeed | CertainTeed | - | …provide a continuous vapor barrier by **CertainTeed** Corp., Knauf Insulation, Johns Manvill… |
| 74 | ? | ceiling_plan | Johns Manville | Johns Manville | - | …inteed Corp. "Toughgard" or equivalent, **Johns Manville**, Owens-Corning, or Knauf. Provide round… |
| 74 | ? | ceiling_plan | CertainTeed | CertainTeed | - | …ck, 1-1/2 pound density, minimum R-6.3 **Certainteed** Corp. "Toughgard" or equivalent, Johns… |
| 90 | E-701 | detail_sheet | CertainTeed | CertainTeed | - | …ional, Anamet Electrical, Amco, Cantex, **Certainteed**, Condux International, Elecsys, Electri… |

Reading the contexts: the 9 Chewy hits are sealant approved-manufacturers lists (Tremco/Sika in silicone/polyurethane spec), drywall manufacturer lists (CertainTeed/Saint-Gobain gypsum), fire-stopping (Tremco/3M), thermal/acoustic ceiling insulation (Johns Manville/Owens Corning fiberglass), and electrical conduit (CertainTeed conduit). None are in roof-membrane spec context. The manufacturers exist in the `MANUFACTURERS` seed because they make roofing products, but on these pages they're being cited for non-roofing materials.

### wendy-s-fort-myers-great-southern-constructors-3

`drawing_index_page=6`, `sheet_map_source=drawing_index`. 6 hits, all `body_text_other`.

| page | sheet | page_type | canonical | matched | flags | context |
|---:|---|---|---|---|---|---|
| 5 | ? | detail_sheet | CertainTeed | CertainTeed | - | …NS-CORNING. EQUAL PRODUCT BY ARMSTRONG, **CERTAINTEED**, SCHULLER OR KNAUF MAY BE PROVIDED AT C… |
| 10 | ? | schedule_sheet | CertainTeed | CertainTeed | - | …E SCHULLER. EQUAL PRODUCT BY ARMSTRONG, **CERTAINTEED**, OWENS-CORNING OR KNAUF MAY BE FURNISHE… |
| 14 | ? | cover | CertainTeed | CertainTeed | - | …- FINISHES SUSPENDED ACOUSTICAL CEILING **CERTAINTEED** ORDERING: Hamilton Parker/CBC and HJC… |
| 14 | ? | cover | Sika Sarnafil | Sarnafil | - | …ussell@holcim.com Updated 7.15.24 (Mia) **SARNAFIL** ROOFING SYSTEMS CANTON, MA 608-270-0053… |
| 52 | ? | elevation | Johns Manville | Johns Manville | - | …BOARDS. 'ENRGY 3' INSULATION BOARDS BY **JOHNS MANVILLE** ARE AN ACCEPTABLE EQUAL. PERIMETER INSU… |
| 52 | ? | elevation | Tremco | Tremco | - | …MANUFACTURED BY BOSTIK, INC., PECORA OR **TREMCO**. (JS-4) SINGLE-COMPONENT, PURABLE, MOIS… |

Mixed: the page-14 Sarnafil ("SARNAFIL ROOFING SYSTEMS") and page-52 Johns Manville ("ENRGY 3 INSULATION BOARDS") are roofing-context. The page-5/10/14 CertainTeed entries are acoustical ceiling spec. Page-52 Tremco is sealant (BOSTIK/PECORA/TREMCO are sealant manufacturers).

### bearss-ave-distribution-center-university-marcobay-construction-3

`drawing_index_page=0`, `sheet_map_source=drawing_index`. 4 hits.

| page | sheet | page_type | canonical | matched | flags | context |
|---:|---|---|---|---|---|---|
| 0 | A-001 | cover | Tremco | Tremco | DI | …AULKED TO FULL HEIGHT, BOTH SIDES, WITH **TREMCO** DYMERIC POLYURETHANE OR EQUAL WITH BACK… |
| 5 | A-201 | elevation | Tremco | Tremco | TB | …Y DYMERIC / DYMERIC 511 COLOR: TO MATCH **TREMCO** ANODIZED ALUMINUM (ALTERNATE - BLACK) A… |
| 46 | ? | cover | Tremco | Tremco | - | …AULKED TO FULL HEIGHT, BOTH SIDES, WITH **TREMCO** DYMERIC POLYURETHANE OR EQUAL WITH BACK… |
| 51 | ? | elevation | Tremco | Tremco | TB | …Y DYMERIC / DYMERIC 511 COLOR: TO MATCH **TREMCO** ANODIZED ALUMINUM (ALTERNATE - BLACK) A… |

All 4 hits are Tremco. None are roofing-context — all are sealant ("DYMERIC polyurethane caulk") or paint-color ("MATCH TREMCO ANODIZED ALUMINUM" — paint color match reference, not a roofing system). The two title-block-zone hits (pages 5 and 51) are color-match notes that happen to live in the bottom-right elevation legend area; the bbox center is at ~(2500, 1900) on a 3024×2160 page → 83% width, 88% height, in the title-block quadrant.

The drawing-index-page hit on page 0 is the same caulking note appearing on the cover sheet, which Filter 1 also identified as the drawing-index page.

Pass 2 flag: `is_repeating_text` would have been 4 if Tremco appeared on >5 pages, but it's exactly 4 here (boilerplate caulking note on 4 sheets). Below the threshold (>5).

### b2607-aea-silverleaf-st-augustine-accelerated-construction-services-6

`drawing_index_page=1`, `sheet_map_source=drawing_index`. 3 hits, all `body_text_other`.

| page | sheet | page_type | canonical | matched | flags | context |
|---:|---|---|---|---|---|---|
| 14 | ? | cover | GAF | EverGuard | - | …EEL DOORS 16355.2 4 ROOFING PRODUCT GAF **EVERGUARD** TPO 5293.1 5 PANEL WALLS NOT USED 6 SHU… |
| 16 | ? | detail_sheet | GAF | EverGuard | - | (similar EverGuard reference) |
| 38 | ? | detail_sheet | GAF | EverGuard | - | (similar EverGuard reference) |

These are roofing-context hits — "GAF EVERGUARD TPO" is an explicit roofing product callout. The scope scanner rejected the pages (vector_count > 500 hard gate, presumably).

### chipotle-tarpon-springs-shell-tarpon-springs-strategic-construction

`drawing_index_page=0`, `sheet_map_source=drawing_index`. 3 hits, all `body_text_other`, all on the same page (pass 1 noted Chewy had multiple pages with hits, Chipotle has all three on one page).

(Per-hit detail in `backend/test_fixtures/intake_diagnostic_pass2_summary.json`.)

### shoppes-at-avalon-spring-hill-mec

`drawing_index_page=0`, `sheet_map_source=drawing_index`. 4 hits, including the corpus's only `negation_window` hit.

| page | sheet | page_type | canonical | matched | flags | context |
|---:|---|---|---|---|---|---|
| 8 | A-101 | elevation | Firestone | Firestone | NEG | …ELOW 60 MIL TPO BY CARLISLE OR EQUAL - (**FIRESTONE** AND DUROLAST ARE NOT ACCEPTABLE MANUFA… |
| (other 3 hits in `body_text_other`) | | | | | | |

Page 8 caught the explicit "(FIRESTONE AND DUROLAST ARE NOT ACCEPTABLE MANUFACTURER…" negation. This is real roofing-spec text — Carlisle is the approved manufacturer, Firestone and Duro-Last are explicitly excluded.

### vine-street-retail-center-kissimmee-great-southern-constructors

`drawing_index_page=2`, `sheet_map_source=drawing_index`. 3 hits, all `body_text_other`. (Per-hit detail in summary JSON.)

### panda-express-san-antonio-candito-construction-2

`drawing_index_page=1`, `sheet_map_source=drawing_index`. 1 hit, `body_text_other`. (Per-hit detail in summary JSON.)

### panda-express-bradenton

`drawing_index_page=0`, `sheet_map_source=drawing_index`. 1 hit, `body_text_other`. (Per-hit detail in summary JSON.)

### panda-express-hialeah-gardens

`drawing_index_page=0`, `sheet_map_source=drawing_index`. 1 hit, `body_text_other`. (Per-hit detail in summary JSON.)

---

## Where the hits actually live (descriptive read-only summary)

Reading the 35 captured contexts side-by-side:

**Hits in non-roofing spec context (most of `body_text_other`):**

- Sealant approved-manufacturers lists (Pecora / Sika / Tremco / 3M / Bostik): Chewy p.40, p.60; Wendy's p.52; Bearss p.0/5/46/51 (Tremco "DYMERIC polyurethane caulk").
- Gypsum / drywall (CertainTeed gypsum + Saint-Gobain + Georgia-Pacific): Chewy p.43.
- Fire-stopping (Tremco / 3M / United States Gypsum): Chewy p.60.
- Acoustical / thermal ceiling insulation (Johns Manville fiberglass + Owens-Corning + Knauf + Armstrong): Chewy p.61, p.74; Wendy's p.5, p.10, p.14.
- Electrical conduit (Certainteed conduit + Anamet + Amco + Cantex): Chewy p.90.
- Paint color references (Tremco anodized aluminum color match): Bearss p.5, p.51.

**Hits in roofing-spec context (a minority):**

- AEA Silverleaf p.14, p.16, p.38: "GAF EverGuard TPO" — explicit roofing product callout.
- Wendy's p.14: "SARNAFIL ROOFING SYSTEMS CANTON, MA" — explicit roofing manufacturer header.
- Wendy's p.52: "ENRGY 3 INSULATION BOARDS BY JOHNS MANVILLE ARE AN ACCEPTABLE EQUAL" — explicit roofing insulation spec.
- Shoppes p.8: "(FIRESTONE AND DUROLAST ARE NOT ACCEPTABLE MANUFACTURER…" — explicit roofing-spec negation, captured by negation_window classification.

The descriptive split: of 35 hits, roughly 5–6 fall in roofing-spec context based on reading the captured 80-char windows; the remaining ~29–30 are in spec language for adjacent trades (sealants, drywall, ceiling tile, electrical, paint).

This is a descriptive observation only. No claim is made about which classification (roofing vs non-roofing context) is "correct" — that requires page-by-page ground-truth review which has not happened. The 80-char window can clip context that would change a reading.

---

## Cross-cutting flag observations

| Flag | Hit count | Interpretation (descriptive only) |
|---|---:|---|
| `is_in_drawing_index` | 1 | Bearss p.0 — sealant note on the cover/index page that Filter 1 also identified as the drawing-index page. |
| `is_in_title_block_zone` | 2 | Bearss p.5 + p.51 — both color-match annotations for "TREMCO ANODIZED ALUMINUM" appearing in the bottom-right of elevation drawings. |
| `is_repeating_text` (canonical on >5 pages) | 0 | No canonical hit the >5-page boilerplate threshold within any single bidset. Closest: Bearss Tremco appeared on 4 distinct pages. |
| `nearby_spec_section_ref` (Division 7 within ±200 chars) | 0 | None of the 35 hits had a Division 7 spec-section reference in the 200-char window. |
| `negated` | 1 | Shoppes p.8 Firestone — same hit pass 1 flagged. |

---

## Explicit non-conclusions

These observations describe what dispatch's text intake contained on
35 manufacturer hits across 10 STACK bidsets where `scope_pages = []`.
They do NOT establish what the scanner should have done with these
pages. Whether 5 or 6 of the 35 are "real roofing manufacturer
mentions" that ought to have produced a `detected_system` is a
ground-truth question, not a measurement question.

Specifically:

1. The 80-char context window can clip semantic context. A hit whose
   80 chars look like a sealant spec might continue into a roofing
   spec section 60 chars further along.
2. The `near_spec_section` flag (0 of 35 hits) does NOT mean none of
   these pages contain Division 7 references — it means none appear
   within ±200 chars of the *manufacturer* match. A page can have a
   Division 7 spec section heading at the top and a manufacturer name
   at the bottom and the diagnostic would not link them.
3. The `is_in_drawing_index` flag fires on the page Filter 1 identified
   as the index. It does NOT mean the manufacturer was listed AS a
   sheet entry — Bearss p.0 is the cover/index page that also carries
   a project-wide caulking note, and the manufacturer name is in that
   note, not in the index entries.
4. The repetition threshold (>5 pages) is mechanical. A canonical
   appearing on exactly 5 pages of the same bidset would not flag as
   repeating; one appearing on 7 would. The threshold was chosen to
   match Daniel's brief; it is not calibrated against any ground truth.
5. The 10-bidset sample is the subset of STACK bidsets matching the
   pass-1 condition (mfr_pos > 0 AND scope_pages = []). It is not a
   random sample. Pass 1's only positive-detection bidset (Taco Bell)
   is excluded by definition.
6. The public-corpus 4 bidsets are NOT included in this pass — pass 1
   recorded only 1 manufacturer hit across those 4 (Suwannee, 1 hit).
   That hit was not inspected here.

No tuning decisions, threshold adjustments, vocabulary extensions, or
fix paths are proposed based on this data. Conclusions about what the
scope scanner should have detected on these pages require both
(a) ground-truth per-page review and (b) a corpus large enough to
distinguish gate behavior from sample artifacts. This 35-hit pass-2
inspection meets neither criterion.
