# Intake Diagnostic — what dispatch saw vs what scope scanner detected

**Date:** 2026-04-26
**Scope:** 19 bidsets total: 15 STACK (from `backend/test_fixtures/v0.2_outputs/`) + 4 public-corpus (from `backend/test_fixtures/public_corpus_outputs/`).
**Pipeline state:** v0.2 dispatch outputs already produced; this is a read-only diagnostic over those JSONs plus their source PDFs.
**Diagnostic script:** `backend/scripts/intake_diagnostic.py`
**Per-page outputs:** `backend/test_fixtures/intake_diagnostic_outputs/<bidset_id>.csv` (19 CSVs)
**Machine-readable summary:** `backend/test_fixtures/intake_diagnostic_summary.json`
**Source PDFs:** `C:/huck stage 2/full bid sets/` (STACK) and `C:/huck stage 2/not_stack-bidsets/` (public)

This document is observation only. It does NOT propose tuning, fixes, or
v0.3 work. The v0.2 dispatch port shipped at commit `441896a`; nothing in
this diagnostic alters that ship state.

---

## Vocabulary scope (what was scanned for)

All keyword scanning used `seeds/roofing_spec_database.py` verbatim, with
no extensions. Categories actually present in that file:

| Category in this diagnostic | Source in `roofing_spec_database.py` | Tokens / count |
|---|---|---|
| `system_signal` | `SPEC_SECTIONS` values' `system` field + `MANUFACTURERS.systems` | 7 tokens: `built_up`, `epdm`, `metal_panel`, `modified_bitumen`, `pvc`, `shingle`, `tpo` (plus a small alias map: "modified bitumen", "built up", "BUR", "standing seam", etc.) |
| `spec_section` | `SPEC_SECTIONS` keys (Division 7 only) | 34 keys |
| `manufacturer` | `MANUFACTURERS` canonical + aliases + product names | 12 canonical / 61 search names |
| `material_thickness` | `MATERIAL_PROPERTIES.thickness_markers` | 5: `45 mil`, `60 mil`, `80 mil`, `90 mil`, `115 mil` |
| `material_insulation` | `MATERIAL_PROPERTIES.insulation_markers` | 11 (polyiso, EPS, XPS, R-20…R-38, cover board, DensDeck, SecurShield) |
| `material_metal` | `MATERIAL_PROPERTIES.metal_markers` | 3: Galvalume, Kynar, PVDF |
| `florida_signal` | `MATERIAL_PROPERTIES.florida_signals` | 15 (HVHZ, NOA, FBC, TAS, FM ratings, UL 580/790, FRSA, NRCA, SMACNA, SPRI) |
| `accessory` | Subset of `SPEC_SECTIONS` keys whose `system` is null and that aren't insulation signals: 07 71 (Roof Specialties), 07 72 (Roof Accessories), 07 84 (Firestopping), 07 92 (Joint Sealants) | 4 keys |

### Categories Daniel's brief mentioned that are NOT in this seed

These were **not scanned** because the verbatim seed does not contain
their vocabulary, and the brief explicitly says "do NOT extend or modify
the vocabulary":

- **penetration** — drains, scuppers, RTUs, vent stacks, pipe boots, splitters, hatches. These keywords live in `data/roof_assemblies.py` (`COMPONENT_KEYWORDS`), which is a different reference file Phase 2 ships but which the brief did not authorize for this diagnostic.
- **edge** — coping, edge metal, drip edge, gravel stop, termination bar, counterflashing. Same source: `data/roof_assemblies.py`. Not scanned here.

The `accessory` category is partially covered (the four spec-section
names listed above), but accessory line items in the broader takeoff
sense (walkway pads, expansion joints, lightning protection, etc.) are
also in `roof_assemblies.py` and are not scanned here.

### Negation detection

For each manufacturer hit on a page, the diagnostic checks whether any
of these phrases appears within ±50 characters (configurable; this run
used 50): `NOT ACCEPTABLE`, `NOT PERMITTED`, `NOT APPROVED`. These are
the three phrases Daniel's brief named exactly. Other "shall not be" /
"is not" patterns were not scanned.

A manufacturer hit is recorded as `negated` when the negation phrase is
within the radius. It is recorded as `positive` otherwise. The
diagnostic does NOT attempt to determine semantic correctness — a hit
at position X with "NOT ACCEPTABLE" 60 chars away is `positive` here,
even if a human reader would judge the spec text as a negation. The
50-char radius is mechanical.

---

## STACK corpus — per-bidset rows (15)

| bidset_id | pages | zero-text pages | evidence pages | scope_pages count | detected_system | conf | mfr_pos | mfr_neg | accessory pages |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| auto-zone-10891-jacksonville-mec-24-others | 28 | 11 | 4 | 0 | None | 0.00 | 0 | 0 | 0 |
| auto-zone-vero-beach-fl | 61 | 23 | 10 | 0 | None | 0.00 | 0 | 0 | 2 |
| b2607-aea-silverleaf-st-augustine-accelerated-construction-services-6 | 40 | 0 | 9 | 0 | None | 0.00 | 3 | 0 | 0 |
| bearss-ave-distribution-center-university-marcobay-construction-3 | 91 | 0 | 26 | 0 | None | 0.00 | 4 | 0 | 0 |
| chewy-vet-care-london-square-miami-jdr-fixtures | 93 | 0 | 25 | 0 | None | 0.00 | 9 | 0 | 5 |
| chipotle-tarpon-springs-shell-tarpon-springs-strategic-construction | 39 | 0 | 20 | 0 | None | 0.00 | 3 | 0 | 1 |
| hampshire-self-storage | 86 | 0 | 5 | 0 | None | 0.00 | 0 | 0 | 0 |
| panda-express-bradenton | 59 | 0 | 12 | 0 | None | 0.00 | 1 | 0 | 1 |
| panda-express-hialeah-gardens | 101 | 0 | 50 | 0 | None | 0.00 | 1 | 0 | 0 |
| panda-express-naples-cdo-visible-construction-corp | 98 | 0 | 35 | 0 | None | 0.00 | 0 | 0 | 1 |
| panda-express-san-antonio-candito-construction-2 | 38 | 0 | 13 | 0 | None | 0.00 | 1 | 0 | 0 |
| shoppes-at-avalon-spring-hill-mec | 97 | 29 | 40 | 0 | None | 0.00 | 3 | **1** | 0 |
| **taco-bell-weeki-wachee-compass-construction-management-2** | 88 | 0 | 29 | **2** | **`tpo`** | **0.95** | 8 | 0 | 3 |
| vine-street-retail-center-kissimmee-great-southern-constructors | 138 | 23 | 47 | 0 | None | 0.00 | 3 | 0 | 0 |
| wendy-s-fort-myers-great-southern-constructors-3 | 64 | 9 | 9 | 0 | None | 0.00 | 6 | 0 | 0 |

**Reading the columns**

- `pages` — total pages in the PDF
- `zero-text pages` — pages where PyMuPDF text extraction returned 0 words. Five bidsets have non-zero counts (Auto Zone Jacksonville 11, Auto Zone Vero 23, Shoppes at Avalon 29, Vine Street 23, Wendy's 9). On these pages the dispatch gate has nothing to scan against — they're effectively raster sheets from this diagnostic's perspective.
- `evidence pages` — pages with at least one keyword hit in any of the categories above (system, spec section, manufacturer, material thickness, material insulation, material metal, florida signal). NOT a measure of correctness — many evidence pages on STACK PDFs are spec books or details where the keyword is in body text, not a takeoff signal.
- `scope_pages count` — number of pages the dispatch scope scanner accepted (`project_scope.scope_pages` length). Comes from the JSON, not from this scan.
- `mfr_pos` / `mfr_neg` — count of unique manufacturer canonicals seen across the bidset, split into positive vs negation-context (per the 50-char window rule above). One canonical can be reported once per page; a single bidset can have a manufacturer counted multiple times if it appears on multiple pages.
- `accessory pages` — count of pages whose `spec_section_hits` includes at least one of the 4 accessory section keys.

### STACK aggregate

| Metric | STACK total |
|---|---:|
| Bidsets | 15 |
| Total pages | 1,121 |
| Zero-text pages | 95 (8.5%) |
| Pages with any roofing evidence | 334 (29.8%) |
| Bidsets with `detected_system` non-null | **1 / 15** (Taco Bell, `tpo` conf 0.95) |
| Bidsets with `scope_pages` non-empty | **1 / 15** (Taco Bell, 2 scope_pages: indices 18, 19) |
| Total positive manufacturer hits (sum of unique canonicals across pages) | 42 |
| Total negation manufacturer hits | 1 |
| Bidsets with any positive manufacturer hit | 11 / 15 (73%) |
| Bidsets with any negation manufacturer hit | 1 / 15 (Shoppes at Avalon) |
| **Bidsets with positive mfr hits BUT scope_pages = 0** | **10 / 15** |
| Total accessory pages | 13 (across 6 bidsets) |

### STACK observations (read-only, no causal claims)

1. The scope scanner accepted at least one page on exactly 1 of 15 STACK bidsets (Taco Bell). Every other STACK bidset has empty `scope_pages`.
2. Manufacturer evidence exists in 11 of the 15 STACK bidsets when scanning the same text dispatch had access to. 10 of those 11 have empty `scope_pages` despite the manufacturer evidence being present.
3. The only negation hit corpus-wide was on Shoppes at Avalon (1 manufacturer found within 50 chars of one of the three negation phrases). The other 41 positive manufacturer hits across STACK had no negation phrase in the 50-char window.
4. Zero-text page counts vary from 0 (most bidsets) to 29 (Shoppes). Whether these are scanned-image pages, intentionally blank, or PyMuPDF text-extraction misses is not determined by this diagnostic.
5. Hampshire Self Storage (the bidset that triggered Symptom 4 FAIL in V0_2_VALIDATION.md) has 5 evidence pages and 0 manufacturer hits in this scan — distinct from Symptom 4's failure mode (sheet-name propagation, not scope detection).

---

## Public corpus — per-bidset rows (4)

| bidset_id | pages | zero-text pages | evidence pages | scope_pages count | detected_system | conf | mfr_pos | mfr_neg | accessory pages |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| holabird-academy-elementary-middle-school | 96 | 0 | 35 | 0 | None | 0.00 | 0 | 0 | 2 |
| sanibel-fire-and-rescue-station-172 | 90 | 0 | 26 | 0 | None | 0.00 | 0 | 0 | 0 |
| suwannee-county-school-board-suwannee-high-school-courtyard-renovation | 31 | 10 | 7 | 0 | None | 0.00 | 1 | 0 | 0 |
| uccs-cybersecurity-and-space-ecosystem-expansion | 133 | 0 | 11 | 0 | None | 0.00 | 0 | 0 | 0 |

### Public-corpus aggregate

| Metric | Public total |
|---|---:|
| Bidsets | 4 |
| Total pages | 350 |
| Zero-text pages | 10 (Suwannee only) |
| Pages with any roofing evidence | 79 (22.6%) |
| Bidsets with `detected_system` non-null | 0 / 4 |
| Bidsets with `scope_pages` non-empty | 0 / 4 |
| Total positive manufacturer hits | 1 (Suwannee) |
| Total negation manufacturer hits | 0 |
| Bidsets with any positive manufacturer hit | 1 / 4 |
| Bidsets with any negation manufacturer hit | 0 / 4 |
| Bidsets with positive mfr hits BUT scope_pages = 0 | 1 / 4 |
| Total accessory pages | 2 (Holabird only) |

### Public-corpus observations (read-only, no causal claims)

1. The scope scanner accepted no pages on any of the 4 public bidsets.
2. Manufacturer evidence is much sparser than STACK: 1 hit total across 350 pages, vs STACK's 42 hits across 1,121 pages.
3. Holabird, Sanibel, and UCCS (all 3 Bluebeam-produced) had zero manufacturer hits across 319 combined pages despite having 72 combined evidence pages from other categories (system signal / spec section / material markers / florida signals).
4. Suwannee (Adobe Acrobat / AutoCAD Architecture) has the most-text-poor PDF in either corpus by ratio (10 of 31 pages = 32% zero-text).
5. UCCS (133 pages) has only 11 evidence pages (8.3% — the sparsest among the 19 bidsets) despite being the largest in the public corpus.

---

## Cross-corpus side-by-side

| Metric | STACK (15) | Public (4) |
|---|---:|---:|
| Total pages | 1,121 | 350 |
| Zero-text pages | 95 (8.5%) | 10 (2.9%) |
| Pages with roofing evidence | 334 (29.8%) | 79 (22.6%) |
| Bidsets with `detected_system` non-null | 1 / 15 (6.7%) | 0 / 4 (0%) |
| Bidsets with `scope_pages` non-empty | 1 / 15 (6.7%) | 0 / 4 (0%) |
| Total positive mfr hits | 42 | 1 |
| Bidsets with any positive mfr hit | 11 / 15 (73%) | 1 / 4 (25%) |
| Total negation mfr hits | 1 | 0 |
| Bidsets with mfr_pos > 0 AND scope_pages = 0 | 10 / 15 | 1 / 4 |
| Per-page evidence rate | 30% | 23% |
| Per-page manufacturer-hit rate | 3.7% | 0.3% |

This table is a side-by-side recording. It is not a calibration input.

---

## Per-page detail

The per-page measurements (sheet number, discipline prefix, page_type,
confidence, word count, in_scope_pages, system_hits, spec_section_hits,
manufacturer_hits with positive/negation split, manufacturer_hit_names,
material_thickness/insulation/metal hits, florida_signal_hits,
accessory_hit, unresolved_xrefs_on_page) are written to one CSV per
bidset:

```
backend/test_fixtures/intake_diagnostic_outputs/<bidset_id>.csv
```

19 CSVs total, one per bidset. They are structurally identical (same
column set, same delimiters) so they can be loaded together for cross-
bidset comparison if desired. Total CSV-row count: 1,471 (1,121 STACK +
350 public).

---

## Explicit non-conclusions

These observations describe v0.2 dispatch's intake on this 19-bidset
sample (15 STACK + 4 public-corpus). They do not establish what correct
behavior should be — that requires page-by-page ground-truth review of
each plan set, which has not happened. No tuning decisions, threshold
adjustments, vocabulary extensions, or fix paths are proposed based on
this data.

The diagnostic only scans for the categories actually present in
`seeds/roofing_spec_database.py`. Two categories Daniel's brief
mentioned (`penetration`, `edge`) are NOT in that seed and were
NOT scanned. A future ground-truth study or a vocabulary-extension
ticket would be required to surface those signals; both are out of
scope here.

The public-corpus side has only 4 bidsets. Cross-corpus comparisons
between STACK (n=15) and public (n=4) are descriptive only.
Distributional claims at this scale cannot distinguish gate behavior
from sample artifacts.

The Symptom-2 result from V0_2_VALIDATION.md (1 of 15 STACK bidsets
had `detected_system` non-null) is reproduced here on the same data
and remains unmodified. This document does not redefine Symptom 2's
pass criteria.
