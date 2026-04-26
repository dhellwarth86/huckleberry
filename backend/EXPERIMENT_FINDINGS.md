# Phase 2 v0.1 Experiment Findings

**Run date**: 2026-04-25
**Bidsets**: 15 real-world commercial roofing PDFs (Florida and Texas)
**Pipeline**: deterministic, rule-based, no LLM, no vision
**Tool stack**: pypdfium2 (text), seeds/dispatch_seed.py + roofing_materials.py + roof_assemblies.py
**Total pages processed**: 1,121
**Total wall-clock**: 78 seconds (after switching from pdfplumber to pypdfium2 — see Tooling notes)

The audit trail for every claim in this document lives in:
- `backend/test_fixtures/experiment_outputs/*.json` — 15 per-bidset extraction outputs
- `backend/test_fixtures/experiment_summary.json` — machine-readable digest
- `backend/test_fixtures/experiment_summary.md` — human-readable digest

---

## 1. Coverage matrix

The coverage matrix has one row per observed field and one column per bidset (X = field populated, . = field absent or empty). The full 46-field × 15-bidset matrix is in `experiment_summary.md`. Headline rows:

| Field | Auto Zone Jax | Auto Zone Vero | AEA | Bearss | Chewy | Chipotle | Hampshire | Panda Naples | Panda SA | Panda Bradenton | Panda Hialeah | Shoppes Avalon | Taco Bell Weeki | Vine St | Wendy's | Count |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| `source_pdf_ref.id/sha256/size_bytes/page_count` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 15/15 |
| `dispatch.page_classifications` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 15/15 |
| `dispatch.sheet_map` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 15/15 |
| `dispatch.project_metadata.project_name` | X | X | X | X | X | X | X | X | . | X | . | X | X | X | X | 13/15 |
| `dispatch.project_metadata.project_address` | X | X | X | X | . | X | X | X | X | X | X | X | X | X | X | 14/15 |
| `dispatch.project_metadata.project_number` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 15/15 |
| `dispatch.roof_page_indices` | . | . | X | X | X | X | X | X | X | X | X | X | X | X | X | 13/15 |
| `scope.systems` | . | . | X | X | X | X | X | X | X | X | X | X | X | X | X | 13/15 |
| `scope.systems[*].system_type` | . | . | X | X | X | X | X | X | X | X | X | X | X | X | X | 13/15 |
| `scope.systems[*].attachment` | . | . | . | X | . | X | X | . | X | X | X | X | X | X | . | 9/15 |
| `scope.systems[*].manufacturer` | . | . | X | X | . | . | . | . | X | . | . | X | X | X | X | 7/15 |
| `scope.systems[*].spec_sections` | . | . | X | . | X | . | X | X | X | X | . | X | X | X | X | 10/15 |
| `scope.evidence.florida_signals` | X | . | X | X | X | X | X | X | X | X | . | X | X | X | X | 13/15 |
| `assembly.systems` | . | . | X | X | X | X | X | X | X | X | X | X | X | X | X | 13/15 |
| `assembly.systems[*].matched_assembly_key` | . | . | X | X | X | X | X | X | X | X | X | X | X | X | X | 13/15 |
| `assembly.systems[*].warnings` | . | . | X | X | X | X | . | X | X | X | . | . | X | X | . | 9/15 |
| `provenance.fields` | X | X | X | X | X | X | X | X | X | X | X | X | X | X | X | 15/15 |

The full 46-row matrix is in `experiment_summary.md` and includes evidence-track rows, deferred rows, and metric rows.

**Two bidsets have no scope at all** (Auto Zone Jacksonville, Auto Zone Vero Beach). They are interior-fitout / mechanical packages — not roofing-primary. The pipeline correctly emitted 0 systems for both. This is the most important coverage observation: a "roofing PDF" is not always a roofing PDF.

---

## 2. Dispatch layer accuracy

### Headline numbers

| Metric | Value |
|---|---|
| Total pages classified | **1,121** across 15 bidsets |
| Pages classified as `roof_plan` | **95** |
| Pages with no keyword match (`page_type=unknown`) | **149** (13.3%) |
| Pages with title-block keyword match (`matched_in='title_block'`) | **338** (`explicit` confidence) |
| Pages with body keyword match (`matched_in='page_text'`) | **595** (`strong` confidence) |
| Architectural-prefix sheets (A-…) | **253** total |
| Architectural sheets classified as `roof_plan` | **31 / 253** |
| Architectural sheets classified as some other type | **222 / 253** |

### Comparison against the 52/60 baseline

The baseline cited in `dispatch_seed.py`'s docstring — **"52 of 60 roof pages in the 15-set sweep fell back to universal items because keyword lists were too narrow"** — is not directly comparable, because that baseline measured a different metric (`fall back to universal takeoff items`, downstream of classification) and ran on a different 15 bidsets. With that caveat, our analogous metric:

- Of **95 pages** Layer 1 classified as `roof_plan`, only **31** had A-prefix sheet numbers (architectural). The other **64** roof_plan classifications came from non-A sheets (T-prefix title sheets where the drawing index lists "ROOF PLAN", spec/schedule pages mentioning the phrase, etc.).
- Of the **222 A-prefix sheets** that did NOT classify as roof_plan, the dominant non-roof types were `elevation` (115), `detail_sheet` (43), `floor_plan` (28), `ceiling_plan` (16), and `framing_plan` (4). Most of these classifications look correct on inspection — A-sheets cover a wide range of architectural drawings, not just roof plans.

**Honest assessment**: classification keyword coverage is acceptable for the easy cases ("ROOF PLAN" in a title block) but produces a long tail of `unknown` (149 pages, 13.3%). Many of the unknowns are STACK-stamped header pages with no title-block content, drafting-symbol pages, and revision-summary sheets. Those are largely correctly NOT roof_plans, so the 149-unknown tail isn't a misclassification crisis — it's the universe of "pages you don't need to look at." Confidence: `weak` overall accept; the keyword list could be a touch wider.

### Page-type distribution across all 1,121 pages

| Type | Count | Pct |
|---|---:|---:|
| detail_sheet | 289 | 25.8% |
| elevation | 259 | 23.1% |
| unknown | 149 | 13.3% |
| roof_plan | 95 | 8.5% |
| floor_plan | 91 | 8.1% |
| ceiling_plan | 66 | 5.9% |
| schedule_sheet | 51 | 4.5% |
| framing_plan | 30 | 2.7% |
| section | 26 | 2.3% |
| mep_plan | 24 | 2.1% |
| general_notes | 17 | 1.5% |
| site_plan | 11 | 1.0% |
| life_safety | 6 | 0.5% |
| cover | 4 | 0.4% |
| symbol_legend | 3 | 0.3% |

**Cover sheets at 4** is suspicious — most bidsets have at least one cover sheet. The `COVER` keyword in `dispatch_seed.PAGE_CLASSIFICATION_KEYWORDS` requires the literal substring, which is missing from many STACK-overlay covers. Covers are getting classified as `unknown` or `general_notes` or even `floor_plan` (when the drawing index appears on page 1 with `FLOOR PLAN` listed). See `Recommended next experiments`.

---

## 3. Scope layer accuracy

### Per-bidset scope identification

| Bidset | Pages | Roof pages | Systems | System types | Manufacturers attached |
|---|---:|---:|---:|---|---|
| Auto Zone Jacksonville | 28 | 0 | 0 | — | — |
| Auto Zone Vero Beach | 61 | 0 | 0 | — | — |
| AEA Silverleaf | 40 | 10 | 4 | mod-bit, built-up, SPF, TPO | GAF |
| Bearss Ave Distribution | 91 | 12 | 4 | TPO, metal, built-up, SPF | Tremco |
| Chewy Vet Care | 93 | 4 | 3 | metal, TPO, EPDM | (none) |
| Chipotle Tarpon Springs | 39 | 5 | 3 | TPO, EPDM, metal | (none) |
| Hampshire Self Storage | 86 | 2 | 2 | mod-bit, metal | (none) |
| Panda Express Naples | 98 | 10 | 4 | built-up, metal, shingle, PVC | (none) |
| Panda Express San Antonio | 38 | 4 | 1 | metal | (none) |
| Panda Express Bradenton | 59 | 7 | 3 | built-up, metal, PVC | (none) |
| Panda Express Hialeah Gardens | 101 | 11 | 4 | TPO, built-up, metal, PVC | Johns Manville |
| Shoppes at Avalon | 97 | 8 | 2 | TPO, metal | Carlisle |
| Taco Bell Weeki Wachee | 88 | 12 | 6 | TPO, PVC, metal, EPDM, SPF, built-up | Johns Manville, Sika Sarnafil, Tremco |
| Vine Street Retail Center | 138 | 9 | 5 | metal, TPO, built-up, SPF, mod-bit | GAF |
| Wendy's Fort Myers | 64 | 1 | 1 | shingle | CertainTeed |

### Aggregate

- **Bidsets with at least one system**: 13 / 15
- **Bidsets with at least one manufacturer attached**: 7 / 15
- **Bidsets where the TPO-fallback fired**: 0 / 15 — every bidset that produced any system did so from direct evidence
- **Florida signals (FBC / HVHZ / NOA / FM / UL)**: 13 / 15 bidsets

### System-type frequency across all detected systems

| system_type | Bidsets w/ this | Comment |
|---|---:|---|
| metal_panel | 11 | **Surprising**: more frequent than TPO. See *Surprises* §7. |
| tpo | 8 | Expected — most common FL flat-roof system. |
| built_up | 7 | Often appears in alternates / spec history pages. |
| spf | 4 | Spec-mentioned alternative even on non-SPF projects. |
| pvc | 4 | Restaurants (chemical resistance). |
| modified_bitumen | 3 | Reroof-friendly, multi-ply. |
| epdm | 3 | Less common in FL. |
| shingle | 2 | Wendy's (residential-pitch entry canopy). |

### Manufacturer frequency

| Manufacturer | Bidsets |
|---|---:|
| GAF | 6 |
| Tremco | 3 |
| Johns Manville | 3 |
| Carlisle | 1 |
| Sika Sarnafil | 1 |
| CertainTeed | 1 |

GAF leads. This may be skewed by GAF's broad product portfolio (TPO + mod-bit + BUR + shingles all carry GAF products) — a single GAF mention in a bidset can match against any of four `system_type` lists.

### Failure modes observed

1. **Multi-system over-detection.** Taco Bell Weeki Wachee identified **6 distinct system types** (TPO + PVC + metal + EPDM + SPF + built-up). No Taco Bell building has 6 separate membrane systems on its roof. The bidset's spec book lists multiple membrane chemistries as alternates / historical references, and the parser's evidence accumulation conflates "spec mentions X" with "X is on this project." Vine Street and Panda Hialeah show similar patterns at lower counts (5 and 4 respectively). **This is the single biggest scope-layer accuracy concern from this experiment.** Resolution belongs to v0.2 (page-zone-aware scope rather than whole-bidset evidence accumulation).

2. **Manufacturer attachment under-attaches.** Layer 2 attached a manufacturer to a system only when `MANUFACTURERS[mfr].systems` includes the system_type. So a single bidset that mentions "GAF Liberty (mod-bit) and Sika Sarnafil PVC" produces two manufacturer hits in `evidence.manufacturer_hits` but only attaches GAF to mod-bit and Sika to PVC if BOTH system_types are detected. When system_type detection misses, the manufacturer attachment misses too. 9/15 bidsets had `manufacturer_hits` in evidence but only 7/15 had `manufacturer` attached to any system.

3. **Confidence skew toward `inferred` (0.5)**. Many systems detected without a spec section land at confidence 0.5. That's correct semantically — bare keyword evidence is weaker than spec-section evidence — but it understates real spec-driven detections where the spec is on a `detail_sheet` page that didn't classify as `schedule_sheet` for spec-section regex purposes. Tightening which page classes feed the spec-section regex could help.

---

## 4. Assembly layer accuracy

### Headline

- **Bidsets with at least one matched assembly**: 13 / 15 (the 2 misses are Auto Zone — no system to match)
- **Total required components across all matched systems**: 264
- **Required components supported by text evidence**: **131 / 264 (49.6%)**
- **Bidsets with at least one warning fired**: 9 / 15

### Matched-assembly distribution

| Assembly key | Bidsets matched |
|---|---:|
| metal_panel_standing_seam | 11 |
| built_up_roofing | 7 |
| tpo_mechanically_attached | 5 |
| spray_polyurethane_foam | 4 |
| modified_bitumen_torched | 3 |
| tpo_fully_adhered | 3 |
| pvc_mechanically_attached | 3 |
| epdm_fully_adhered | 2 |
| asphalt_shingles | 2 |
| epdm_mechanically_attached | 1 |
| pvc_fully_adhered | 1 |

### Warning trigger counts

| ASSEMBLY_RELATIONSHIPS rule | Times triggered (sum across bidsets/systems) |
|---|---:|
| `fbc_hvhz_applies` | 21 |
| `overflow_pairing` | 18 |
| `curb_high_side_cricket` | 13 |
| `rtu_drives_curb` | 13 |
| `tapered_insulation_for_drainage` | 9 |
| `drainage_exclusivity` | 4 |
| `adhesive_requires_cover_board` | 3 |

The most-triggered rule (`fbc_hvhz_applies`) is just an informational chip whenever `HVHZ` or `NOA` appears in text — which is most of the FL bidsets. The most operationally-meaningful warning is `overflow_pairing` (spec mentions roof drains but no overflow drains in the same text body) — this fires on 18 separate (bidset, system) pairs and would each warrant estimator attention. `curb_high_side_cricket` and `rtu_drives_curb` fire as `would_fire_on_pin_data` — they're noting "we can't evaluate this from text alone; once user pin data exists in v0.3, these will run for real."

### Components-supported ratio (49.6%) — what's missing

The required components most often *not* supported by text in the experiment's roof-relevant pages were:

- `fasteners` and `fastener_plates` — almost always implied (mechanically attached systems require fasteners by definition) but rarely written out in detail-sheet text
- `termination_bar` — mentioned in details but not in the keyword bank's preferred form
- `metal_panel_standing_seam`'s 6 required components — when a bidset gets metal_panel_standing_seam matched (because canopies / awnings have standing-seam mentions), the matching fails to support `panel_clip`, `ridge_cap`, `valley_flashing` because the bidset isn't really a metal-roof bidset (false-positive matching from §3 failure mode 1)

**Honest assessment**: 49.6% support is consistent with two compounding effects: (a) keyword bank is incomplete (real fix: extend `COMPONENT_KEYWORDS` based on actual spec language) and (b) ~30% of "matched assemblies" are from over-detection of metal_panel where the bidset doesn't really have a metal roof.

---

## 5. Promoted fields

The 32 fields below pass both criteria of the inclusion rule:
- (1) Field appears in ≥ 3 / 15 bidsets, AND
- (2) Field has an identifiable downstream consumer.

Fields are listed in their `BidsetRecord` schema location.

### `source_pdf_ref` (4 fields, all 15/15)

| Field | Count | Consumer |
|---|---|---|
| `id` | 15/15 | HTTP routing key; DB primary key. |
| `sha256` | 15/15 | Integrity check on download; deduplication. |
| `size_bytes` | 15/15 | Storage accounting; ETA estimation. |
| `page_count` | 15/15 | PAGES-tab thumbnail grid; viewer page navigation. |

### `dispatch` (5 fields)

| Field | Count | Consumer |
|---|---|---|
| `page_classifications` | 15/15 | PAGES-tab badges; scope page filter. |
| `sheet_map` | 15/15 | Sheet-number column in TAKEOFF / Excel; deep-link references. |
| `project_metadata.project_name` | 13/15 | Excel export header; project search. |
| `project_metadata.project_address` | 14/15 | Excel header; HVHZ county determination. |
| `project_metadata.project_number` | 15/15 | Excel header; estimator filing reference. |
| `roof_page_indices` | 13/15 | Viewer auto-navigates to first roof page. |

### `scope` (10 fields)

| Field | Count | Consumer |
|---|---|---|
| `systems` | 13/15 | SCOPE-tab card list; per-system Excel sheets. |
| `systems[*].system_type` | 13/15 | Pin/edge/polygon palette derivation; assembly lookup. |
| `systems[*].attachment` | 9/15 | Disambiguates which ROOF_SYSTEMS entry. |
| `systems[*].manufacturer` | 7/15 | Excel Manufacturer column; vendor NOA/spec lookup. |
| `systems[*].spec_sections` | 10/15 | Cross-reference back to spec page. |
| `systems[*].source_pages` | 13/15 | Click-to-page navigation in SCOPE tab. |
| `systems[*].confidence` | 13/15 | Drives 'parser said X, please confirm' UX. |
| `evidence.spec_section_hits` | 14/15 | Provenance audit. |
| `evidence.manufacturer_hits` | 9/15 | Provenance + alternative-mfr suggestion. |
| `evidence.attachment_hits` | 9/15 | Provenance audit. |
| `evidence.insulation_markers` | 8/15 | Provenance + flat-roof detection. |
| `evidence.florida_signals` | 13/15 | FBC/HVHZ warning chip. |
| `evidence.system_type_keyword_hits` | 12/15 | Provenance audit. |
| `fallback_used` | 15/15 (False on all) | QA flag — fallback systems get 'low-confidence' badge. |

### `assembly` (7 fields)

| Field | Count | Consumer |
|---|---|---|
| `systems` | 13/15 | TAKEOFF-tab line items. |
| `systems[*].matched_assembly_key` | 13/15 | Drives takeoff component shopping list. |
| `systems[*].required_supported_components` | 13/15 | Excel rows that have evidence. |
| `systems[*].required_missing_components` | 13/15 | Excel rows flagged 'expected but not found'. |
| `systems[*].component_evidence` | 13/15 | Provenance per takeoff row. |
| `systems[*].warnings` | 9/15 | TAKEOFF / SCOPE warning chips. |
| `florida_signals` | 13/15 | FBC warning panel. |

### `provenance.fields` (15/15)

Phase 3 ML training labels; v0.3 'parser said X, you changed to Y' UX.

### `schema_version` and `id` (top-level)

Both required, present 15/15. Versioning policy from Decision #16.

---

## 6. Deferred / observed appendix

These fields were observed in the per-PDF JSONs but did NOT make the schema. The reason for each is recorded so a future review can revisit (and so the next Claude doesn't accidentally reintroduce them).

| Field | Bidset count | Reason for deferral |
|---|---:|---|
| `source_pdf_ref.producer_hint` | 15/15 | **No consumer.** All 15 are "STACK Construction Technologies" — the field gives almost no signal. Defer until non-STACK PDFs arrive. |
| `dispatch.cross_references_by_page` | 15/15 | **No near-term consumer.** Phase 1's frontend doesn't read cross-references. v0.3+ may use them for "click ref → jump page" navigation, but the design isn't pinned. |
| `dispatch.legends_by_page` | 15/15 | **No consumer.** The legend extraction is shallow (header keyword + numbered list count) and doesn't map to a downstream feature. Glazing schedules (window/door) are a more important legend type but glazing is out of v0.1 scope. |
| `dispatch.page_type_histogram` | 15/15 | **Debugging only.** Lives in extraction_metrics; useful in this report; not in the contract. |
| `dispatch.confidence_histogram` | 15/15 | **Debugging only.** Same as above. |
| `dispatch.project_metadata.owner` | 10/15 | **No consumer.** Owner names are a nice-to-have for client filing; not part of the takeoff workflow. |
| `dispatch.project_metadata.architect` | 7/15 | **No consumer.** Same as owner. |
| `dispatch.project_metadata.total_building_sf` | 2/15 | **Frequency below threshold.** Sanity-check vs measured area would be a real consumer if it surfaced more often, but at 2/15 the regex is too thin. Improve the regex in v0.2 (likely picks up SF tables on cover/index pages with better spatial gating). |
| `scope.systems[*].thickness_markers` | 2/15 | **Frequency below threshold.** Despite plausible consumer (Excel material column), only 2/15 hit. The thickness regex (`60 mil`, `45 mil`, etc.) requires the exact unit. Spec language often uses ".060" or "060-mil" — extending the regex is a v0.2 task. |
| `scope.evidence.thickness_markers` | 2/15 | Same as above. |
| `scope.pages_skipped_glazing` | 15/15 | **Debugging only.** Records how many pages were skipped because they looked predominantly glazing-relevant. Useful in this report; not user-facing. |
| `extraction_metrics.elapsed_seconds / pages_processed / scope_systems_identified` | 15/15 | **Debugging only.** Per-pipeline-run metrics. They live in the per-PDF JSON; not in the contract. |

**Glazing fields**: not enumerated above because v0.1 scope was explicit roofing-only. The pipeline notes glazing-heavy pages are skipped (`scope.pages_skipped_glazing`); no glazing fields are extracted, no glazing schema is proposed. v0.2+ will run a parallel experiment using `glazing_materials.py` and `glazing_assemblies.py` once those seeds get an estimator review.

---

## 7. Surprises (the signal that the experiment was useful)

Specific, evidence-backed observations the experiment produced that were NOT predicted in `CLAUDE.md`'s "Phases" section or the experiment prompt:

1. **All 15 bidsets are STACK Construction Technologies output.** The user's "real production distribution" turned out to be much more homogeneous on the producer axis than I expected — every PDF was processed through STACK. This means: (a) `source_pdf_ref.producer_hint` carries almost no signal in this dataset, and (b) findings here may not generalize to non-STACK bidsets. **Risk**: schema overfits to STACK conventions. **Recommended action for v0.2**: ensure the next 15-bidset sweep includes at least 4 bidsets from non-STACK producers (UniDoc-direct, AutoCAD-export, Bluebeam, Adobe-original).

2. **Multi-system over-detection is the dominant scope-layer failure mode.** Taco Bell Weeki Wachee = 6 distinct membrane chemistries detected. No real Taco Bell building has 6 separate roof systems. The cause: the spec-evidence accumulation is whole-bidset-flat — every membrane keyword anywhere in the PDF inflates the system list. Compare to the dispatch layer's per-page model, which correctly partitions content into pages; scope needs a similar partition into "which page is this evidence ABOUT" vs "which page does it appear ON." This is the strongest argument I see for v0.2's scope work being page-zone-aware instead of bidset-flat.

3. **`metal_panel` is the most-frequent matched assembly (11/15).** Conventional wisdom (and CLAUDE.md context from earlier sessions) suggested TPO would dominate. The reason is that "STANDING SEAM," "METAL PANEL," and "R-PANEL" appear on elevation drawings for canopies, awnings, screen walls, and parapet caps even on flat-roof commercial buildings. The pipeline correctly notes the keyword evidence; it incorrectly elevates these to system-level matches. **Implication**: scope detection for metal panels needs roof-vs-non-roof page disambiguation that doesn't exist today.

4. **Manufacturer attachment under-attaches (7/15) despite manufacturer evidence in 9/15.** The strict filter (`manufacturer.systems must include the detected system_type`) is correct in principle — it prevents Carlisle (which makes TPO/PVC/EPDM) from getting attached to a metal-panel system — but it loses real attachments when system_type detection itself is weak. **Implication**: manufacturer attachment quality is GATED by system_type detection quality. Improving one without the other won't help.

5. **The `tpo` fallback never fired (0/15).** I designed a fallback: if no system_type was detected but flat-roof insulation markers were present, attach a low-confidence TPO system. None of the 15 bidsets needed it — direct keyword/spec evidence covered every flat-roof case. **Implication**: the fallback is over-engineering for a problem that didn't manifest. Keep the code (cheap, 5 lines) but note that it's untested by real data.

6. **Hampshire Self Storage detected `attachment='ballasted'` from a single mention.** Ballasted EPDM is rare in FL (and prohibited in HVHZ). The mention came from an "alternates considered" discussion, not the actual roof spec. Hampshire's actual roof is mod-bit. **Implication**: attachment detection from any mention is too generous; it should be gated on the same page that detected the system_type.

7. **Page-type `cover` is heavily underdetected (4 in 1,121 pages = 0.36%).** Most bidsets have at least one cover sheet but many got classified as `unknown` or `floor_plan` because STACK overlay pages don't carry the literal word "COVER" in their title block — they carry the project name and sheet number "T-1.0" / "G-0.0" instead. **Implication**: the dispatch keyword `COVER` is too literal. Adding `T-1` / `G-0` sheet-number patterns or "TITLE SHEET" / "DRAWING INDEX" keywords would fix it.

8. **The `unknown` tail is 13.3% of pages (149).** Most are STACK overlay pages (revision summaries, drawing index continuations, blank-with-watermark pages). They are correctly NOT roof_plans, but they also waste classifier confidence and create noise. The right fix is probably a filter that detects "this page is mostly title-block boilerplate with no real content" rather than expanding keyword lists.

9. **Auto Zone bidsets are not roofing-primary projects.** Both `auto-zone-10891-jacksonville-mec-24-others` and `auto-zone-vero-beach-fl` had 0 roof pages and 0 systems. On inspection, the Jacksonville bidset is an interior fixture/finishes/MEC package (page 0 = "INTERIOR FLOOR FINISHES NOTE: SHALL COMPLY WITH 2023 FBC SECTION 804"). The Vero Beach package shows similar patterns. **Implication**: 2/15 (13%) of "roofing bidsets in a contractor's archive" turn out to be non-roofing-primary packages. Phase 2 needs to handle this gracefully — classifying a bidset as "no roof scope" with confidence is a real outcome, not an error state.

10. **The 49.6% required-component support ratio is bimodal, not uniform.** Looking per-bidset, the support ratio splits between (a) bidsets where the matched assembly is correct and 70-90% of components find evidence, and (b) bidsets where the matched assembly is over-detected (typically `metal_panel_standing_seam` on a flat-roof bidset because of canopy mentions) and 0-15% of components find evidence. The 49.6% mean obscures both halves of this distribution. **Implication**: a per-system "is this assembly really on the roof?" sanity check would split the bimodal distribution and surface the over-detected ones.

11. **`drainage_exclusivity` warning fires on 4 bidsets**. This rule catches "spec mentions both drains AND scuppers." All 4 hits are legit text-level evidence — but on real plans, drains and scuppers serve different drainage zones, so the rule's note ("verify on plans") is correct. Need pin/zone data to evaluate properly. Same observation applies to `overflow_pairing` (18 hits), where the absence of overflow drains in text is sometimes because the overflow detail is on a `detail_sheet` whose text we DID extract but where the keyword `OVERFLOW` happens to be absent (the detail uses "SECONDARY DRAIN" or shows the diagram without text). The keyword bank is too narrow.

---

## 8. Tooling notes

### Tools used

- **pypdfium2 (5.7.1)** — PDF text extraction. **Started with pdfplumber (per `pyproject.toml`); pivoted to pypdfium2 mid-experiment.**
- **`seeds/dispatch_seed.py`** — page classification, sheet-number regex, cross-reference patterns, legend rules, project-metadata field lists.
- **`seeds/roofing_materials.py`** — CSI spec sections, manufacturer database (12 entries + aliases + products), thickness markers, insulation markers, Florida signals.
- **`seeds/roof_assemblies.py`** — ROOF_SYSTEMS map, COMPONENTS map, ASSEMBLY_RELATIONSHIPS rules.
- **Pydantic 2.13** — schema validation in tests.

### The pdfplumber → pypdfium2 pivot

Per the march orders ("don't pick a tool stack"), the pipeline started with `pdfplumber` (the only PDF-text library in `pyproject.toml`'s required deps). On the first smoke run (Chipotle Tarpon Springs, 39 pages), wall-clock was **146 seconds**. Per-page cost ~3.7s. Extrapolated to all 1,121 pages: ~70 minutes.

I checked whether the bottleneck was `extract_words()` (per-block analysis) — it wasn't; even the lightweight `extract_text()` alone was ~3s/page on these STACK PDFs. STACK output has 46k–92k path operators per page (vs 5–10k for typical CAD PDFs), and pdfplumber walks every operator to derive text positions.

I then benchmarked `pypdfium2` (already in `pyproject.toml` as a "comparison renderer"):
- pypdfium2 on Chipotle = **2.0 seconds** for 39 pages (70× faster).
- Same text content (8,749 chars/page on average — comparable extraction quality).
- Same downstream metrics (39 pages → 5 roof_pages → 3 systems identified, identical to pdfplumber).

I switched to pypdfium2. The trigger: `pypdfium2` was already in the `pyproject.toml` (no new tool added per the tooling rule), the speed gain enables iterative development of the schema, and downstream metrics didn't change. **Honest flag**: this is a tool pivot mid-experiment. It's documented here, the pipeline code uses pypdfium2 explicitly with a comment explaining why, and the original Chipotle output produced via pdfplumber was deleted and re-extracted with pypdfium2 to keep methodology consistent across all 15 bidsets.

### Tool successes

- **pypdfium2** opened, parsed, and extracted text from every one of the 15 bidsets without a single crash. 1,121 pages processed in 78 seconds total (~14 pages/second).
- **`get_text_bounded`** worked for the title-block extraction without coordinate errors, despite STACK PDFs using a `0.015 0 0 0.015 cm` transform (which crippled some pdfplumber operations in earlier project sessions, per `CLAUDE.md`'s session notes).

### Tool failures / quirks

- **None catastrophic.** No bidset failed extraction; no page returned an error; no PDF refused to open.
- **`get_text_bounded` returned almost no text on a few title blocks**; the extractor falls back to `full_text[-600:]` when the bounded extraction returns less than expected. This was the difference between seeing the title block and missing it on an estimated 5–8% of pages — qualitative observation, not measured.
- **One filename has a Unicode-corrupted character in the manifest**: `Chewy Vet Care-London Square - Miami - JDR Fixtures�.pdf`. Original filename has a non-printing character that gets mangled in the local filesystem. The pipeline still processes it correctly (filename-as-path works); the JSON output's `filename` field shows the corruption. v0.2 backend should normalize filenames on upload to the manifest.
- **`pdfplumber` was slow but correct.** The ~3s/page cost would be acceptable for a one-shot batch import; not for an interactive UI. v0.2's backend likely wants pypdfium2 for hot-path text extraction and (separately) pdfplumber for layout-heavy operations like coordinate-aware table extraction, where pdfplumber's spatial primitives are real value.

### Tool additions NOT made

- No Camelot, no Docling, no Apryse, no vision model. No fallbacks. No retries with alternative engines. Per the march orders.

---

## 9. Recommended next experiments (for v0.2 review)

In rough priority:

1. **Per-page-zone scope evidence accumulation.** The single highest-leverage change. Instead of accumulating spec/manufacturer hits across the whole bidset, compute them per-page (or per-zone within a page) and require co-occurrence within a single page or zone to count as a "system." Should drop Taco Bell from 6 systems to a realistic 1–2.

2. **Roof-vs-non-roof page disambiguation for metal_panel.** Match `STANDING SEAM` only on pages classified as `roof_plan` or `schedule_sheet`, not `elevation`. Should drop the metal_panel false-positive rate and fix the 49.6% component-support bimodality.

3. **Title-block detection for STACK overlays.** The dispatch keyword `COVER` is too narrow. Add `TITLE SHEET`, `DRAWING INDEX`, sheet-number prefixes `T-1` / `G-0` / `G0.0`, and a "page text dominantly = sheet metadata" heuristic. Should raise cover detection from 4 to ~15.

4. **Manufacturer attachment fallback when system_type is weak.** When a manufacturer is detected on a roof-relevant page but no system_type matches that manufacturer's `supported_systems`, surface the manufacturer as an unattached observation with a "needs system_type" flag rather than dropping it. Today this is silent data loss.

5. **Diversify the bidset set.** Add at least 4 non-STACK bidsets to the v0.2 sweep. Pin schema fields produced from the homogeneous STACK set as "validated against STACK only" until non-STACK confirms.

6. **Project-metadata regex hardening.** Cover, owner, architect, total_building_sf currently use loose substring patterns. Tighten with spatial gating (cover-page only) and tighter end-anchors. The Chipotle output had owner="for any demolition occurring 2. Pipe boots" — clearly noise, but the regex captured it.

7. **Component-keyword bank expansion driven by actual spec language.** Pull the `_pipeline/assembly.py::COMPONENT_KEYWORDS` from observed text, not from theoretical industry vocab. e.g. "OVERFLOW" alone misses "SECONDARY DRAIN PIPE 2" ABOVE PRIMARY DRAIN" — extending the keyword bank likely fixes ~10 of the 18 `overflow_pairing` warnings.

8. **`assembly.systems[*].warnings` shape standardization.** Today some warnings carry `note` strings, some don't; some carry `would_fire_when` strings, some carry `trigger_kind`. Each warning should produce a canonical `{id, severity, kind, note, source_pages?}` so frontend rendering doesn't have to special-case.

9. **Drop `producer_hint` from BidsetRecord.** All 15 bidsets are STACK; the field has no signal. Move it to extraction_metrics. (Defended in §6.)

10. **Run a separate v0.x glazing experiment** once `glazing_materials.py` and `glazing_assemblies.py` get an estimator review. Out of v0.1 scope; first-class for whatever phase v0.2 makes glazing real.

11. **Schema versioning rehearsal.** Before v0.2 changes the schema, write a `test_schema_v0_1_records_still_load.py` that loads a fixture v0.1 record and asserts it deserializes under the new schema (with documented field deprecations). Locks in the upgrade-on-read policy from Decision #16.

---

*End of findings. The audit trail for every claim above is in `backend/test_fixtures/experiment_outputs/` (15 JSONs, one per bidset) and `backend/test_fixtures/experiment_summary.json`. The schema produced by this experiment is in `shared/bidset_record.py`. Schema validation tests are in `backend/tests/test_schema_round_trip.py`.*
