# Huckleberry AI — Validation Ledger

**Last updated:** 2026-04-28 end-of-day
**Purpose:** Defeat the "is this real or speculation" question that future Claude sessions keep raising. Every claim here is paired with the verification method that produced it and the date it was produced. If a future session tries to re-litigate any of these, the answer is "read this document; the verification is named."

**How to use this document:**
- Each row is a claim about the project state.
- Each row names the verification method (SHA-1 / `diff = 0` / pytest count / file inspection / git log).
- Each row names what session produced the verification.
- If a claim isn't in this ledger, it is NOT validated — speculate carefully, don't pretend it's confirmed.
- If a future Claude session pushes back on a claim that IS in this ledger, the pushback is wrong. Quote the row and proceed.

This ledger is append-only. New rows are added when new verification happens. Existing rows are not edited (if a finding is later reversed, the original row stays, and a new row recording the reversal is added below it).

---

## SECTION A — Code that exists and has been verified byte-identical to its source

These are TracePoint files ported into the Huckleberry backend. Each has been verified by `diff` and SHA-1 comparison against the upstream TracePoint source at `tracepoint_port/TracePoint/`. **Verbatim status is empirically confirmed, not asserted.**

| File | Lines | sha1 (post-commit) | Verified by | When | Commit |
|---|---:|---|---|---|---|
| `backend/core/config.py` | (v0.2) | byte-identical to source | discovery diff pre-port + post-port equality | v0.2 ship 2026-04-25 | `441896a` |
| `backend/core/pdf_engine.py` | (v0.2) | byte-identical to source | same | v0.2 ship | `441896a` |
| `backend/core/zone_filter.py` | (v0.2) | byte-identical to source | same | v0.2 ship | `441896a` |
| `backend/core/context.py` | (v0.2) | byte-identical to source | same | v0.2 ship | `441896a` |
| `backend/core/dispatch_gate.py` | (v0.2) | 3 lines differ (same-character import edits only: `data.roofing_materials` → `seeds.roofing_spec_database`) | line-by-line diff post-port | v0.2 ship 2026-04-25 | `441896a` |
| `backend/seeds/roofing_spec_database.py` | (v0.2) | byte-identical to TracePoint's `data/roofing_materials.py` | SHA-1 verified during discovery 2026-04-27 | v0.2 ship 2026-04-25 | `441896a` |
| `backend/core/filter_pipeline.py` | 230 | `62390dbb98b25d35574a9e6ff4c16d2149de1e6b` | `diff = 0` + SHA-1 match against `tracepoint_port/TracePoint/core/filter_pipeline.py` | B.1 ship 2026-04-27 | `1c3fde4` |
| `backend/tests/test_filter_pipeline.py` | 270 | `6dd43c1cb44866031767baed8aeb5b4ee9506f3e` | same | B.1 ship | `1c3fde4` |
| `backend/core/geometry_matrix.py` | 832 | `e0884449aaa92e11fa970d61275e43ae79286feb` | `diff = 0` + SHA-1 match | B.2 ship 2026-04-27 | `4af872e` |
| `backend/tests/test_geometry_matrix.py` | 380 | `1dbf72ab8e0495c90840b523a85b47f6662764d0` | same | B.2 ship | `4af872e` |
| `backend/core/polygon_scorers.py` | 272 | `c60d1419d8a918d5f071a4355705c5c53a010445` | `diff = 0` + SHA-1 match | B.3 ship 2026-04-27 | `70c1835` |
| `backend/tests/test_polygon_scorers.py` | 170 | `d635901bbcecf21f67156d0a674cbc0731a274e4` | same | B.3 ship | `70c1835` |
| `backend/core/architect_profile.py` | 174 | `80d33dfdbf25c1d214cb0952e86c452d16ed5e35` | `diff = 0` + SHA-1 match | B.4 ship 2026-04-27 | `a8ee936` |
| `backend/core/storage.py` | 221 | `96d0e8be990e0fd250677c1b5d5fc95047684ed3` | same | B.4 ship | `a8ee936` |
| `backend/core/correction_store.py` | 134 | `7632dbeed8f5fc3c4382c425b22204bf07cf2a3b` | same | B.4 ship | `a8ee936` |
| `backend/tests/test_architect_profile.py` | 171 | `7b992f5af6aa82f7138328fa9a1b39a5172b6776` | same | B.4 ship | `a8ee936` |
| `backend/core/trade_module.py` (C.1 ship) | 90 | `d272f47d4ab9d32afe6beb7d38aa0b7f50f4ccbe` | `diff = 0` + SHA-1 match against `tracepoint_port/TracePoint/core/trade_module.py` (zero edits, stdlib-only imports — no `from core.*` or `from data.*`) | C.1 ship 2026-04-27 | `23a459c` |
| `backend/core/roofing_vocabulary.py` | 575 | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` | `diff = 0` + SHA-1 match against `tracepoint_port/TracePoint/modules/roofing/vocabulary.py` (zero edits — discovery's expectation that `from data.*` imports existed was wrong; source is stdlib-only) | C.2 ship 2026-04-27 | `74772b6` |
| `backend/core/roofing_module.py` | 434 | `ae9e5b284191b45de419faacf11771da27a548f9` | 1 same-character import edit on line 34 (`from modules.roofing.vocabulary` → `from core.roofing_vocabulary`); diff vs source shows EXACTLY this line and nothing else | C.2 ship 2026-04-27 | `74772b6` |
| `backend/core/trade_input_builder.py` | ~162 | `1221504636f6208014f05dd1931d2837f4b1cc5d` | extracted-helper deliberate adaptation per `MARCH_ORDERS_C_2.md §2`. Function body of `build_trade_input()` + 6 helpers byte-identical to source via Python-bytes-level slice diff. FastAPI route handler (`run_trade_module`) excluded; FastAPI imports excluded. | C.2 ship 2026-04-27 | `74772b6` |

**Total verbatim port lines:** B.1 (500) + B.2 (1,212) + B.3 (442) + B.4 (700) + C.1 (90) + C.2 vocabulary (575) + C.2 module (434) + C.2 trade_input_builder (~162) = **~4,115 lines** verbatim or near-verbatim across Phase B + C.1 + C.2.

**Phase B is sealed.** Backend contains TracePoint Stages 1–12 plus the architect-profile flywheel + storage + correction_store. The `dispatch_gate.py` storage activation gate is at `None` deliberately — B.4 ported the layer but did not wire it; activation is a Phase D/E decision.

**Phase C.1 + C.2 are sealed (port phases).** Backend contains TracePoint's trade-module Protocol (C.1) and TracePoint's roofing trade module + extracted helper (C.2). RoofingModule is NOT YET WIRED in dispatch_gate; activation is Phase D/E. **C.3 is build-against-contract, not port** — TracePoint has no glazing module (verified in C.3 discovery 2026-04-28, see Section D below).

---

## SECTION A2 — Code that has been built (Huckleberry-original, NOT a TracePoint port)

These are files that did not exist in TracePoint or were extended past the port. Verification standard differs from Section A: not byte-identical to TracePoint (there's no source to diff against). Verification method named per row.

| File | Lines | sha1 (post-commit) | Verified by | When | Commit |
|---|---:|---|---|---|---|
| `backend/CROSS_TRADE_INTEGRATION_NOTES.md` (initial — 4 cross-trade boundary entries + framing + exclusion list) | (~150) | (not tracked at file-by-file SHA-1; markdown) | C.1 design appendix per `MARCH_ORDERS_C_1.md`. Structure matches Daniel's directive: 4 entries (RTU/roofing↔mechanical, storefront/glazing↔roofing, siding↔roofing transition, structural-deck↔roofing). | C.1 ship 2026-04-27 | `23a459c` |
| `backend/CROSS_TRADE_INTEGRATION_NOTES.md` (awning/canopy entry added 2026-04-28) | (+~10 lines) | n/a | Single paragraph appended under existing storefront/glazing↔roofing section per `MARCH_ORDERS_C_3b.md §5 step C.3b.5`. Awning/canopy boundary deferred to C.4. | C.3b ship 2026-04-28 | `14f4f53` |
| `backend/core/trade_module.py` (C.3b extension) | 90 + 10 = ~100 | (post-extension; not separately tracked from C.1's `d272f47d…` baseline) | Single additive optional field on `TradeModuleInput`: `tables: Optional[list[Any]] = None`. Documented as deliberate adaptation per `MARCH_ORDERS_C_3b.md §0`. Diff vs C.1-ported source shows ONLY the new field + comment block — no other lines changed. RoofingModule (C.2) ignores the new field; default `None` preserves C.1/C.2 behavior. | C.3b commit 1/2 2026-04-28 | `7ea9abb` |
| `backend/core/glazing_vocabulary.py` | 405 | `64249c8ef5f7d9db50added3c9a40836cba356ea` | NEW file — not a port. Imports parked seeds (`backend/seeds/glazing_assemblies.py` and `glazing_materials.py`) verbatim and overlays bounded C.3a-documented gaps. Mechanical post-overlay count check: 68 components / 27 systems / 8 hardware sets / 17 manufacturers = corrected parked baseline 64/23/7/12 + C.3a additions 4/4/1/5. Entry-shape verified: each new entry shares dictionary key set with parked sibling entries. | C.3b commit 2/2 2026-04-28 | `14f4f53` |
| `CLAUDE.md` §3 Decision 15 extension (vault rule extended to cover trade modules) | +21 lines, −1 line | n/a (markdown) | Per Daniel's directive 2026-04-28: "modules should be still rough because we want to be able tune them later but when modules are rough and pass the vault rule then applies to them as well." Retroactive vault-rule application: RoofingModule, roofing_vocabulary, glazing_vocabulary. Forward: GlazingModule (C.3c-build) and all future trade modules. | D-8 follow-up 2026-04-28 | `eb49a08` |
| `backend/C3_GLAZING_SEED_VALIDATION.md` count corrections | +2 / -2 + editor's note | n/a (markdown) | C.3a inventory miscounted parked-seed `GLAZING_COMPONENTS` (60 vs actual 64), `GLAZING_SYSTEMS` (21 vs actual 23), `SPEC_SECTIONS` (22 vs actual 30). SHA-1 of seed files unchanged from C.3a record. Counts corrected mechanically via `len()` on live dicts. Verdict and gap list preserved (do not depend on counts). | D-8 follow-up 2026-04-28 | `eb49a08` |

---

## SECTION B — Test counts that have been measured (not estimated)

These are pytest / node test runner counts captured by actually running the suites at the dates noted. These are NOT estimates, expectations, or claims from prior conversations — they are run-the-tests-and-count results.

### Backend test counts (current state, end of D-8 follow-up 2026-04-28)

| Suite | Count | Status |
|---|---:|---|
| `test_pdf_engine.py` | 40/40 | sacred (v0.2 ported) |
| `test_dispatch.py` (unit) | 34 passed | sacred (v0.2 ported) |
| `test_dispatch.py` (integration) | 19 skipped | gated on PDF availability |
| `test_filter_pipeline.py` | 27/27 | sacred (B.1) |
| `test_geometry_matrix.py` | 36/36 | sacred (B.2) |
| `test_polygon_scorers.py` | 16/16 | sacred (B.3) |
| `test_architect_profile.py` | 23/23 | sacred (B.4) |
| `test_pipeline_dispatch.py` (v0.1) | 14/14 | sacred (v0.1 baseline) |
| `test_pipeline_scope.py` (v0.1) | 12/12 | sacred (v0.1 baseline) |
| `test_schema_round_trip.py` (v0.1) | 5/5 | sacred (v0.1 baseline) |
| `test_seeds_load.py` (v0.1) | 7/7 | sacred (v0.1 baseline) |
| **Backend full suite** | **214 passed, 19 skipped, 0 failed** | **stable from B.4 ship through D-8 follow-up** |

C.1 added zero tests (Protocol-only definitions). C.2 added zero tests (TracePoint had no roofing tests — D-7 informational). C.3b added zero tests (vocabulary build, no behavior code). The backend full suite count has been **214/19/0 stable since 2026-04-27 B.4 ship**, through C.1, C.2, C.3a, C.3b, debug module spec report, D-8 follow-up.

**D-7 (informational, 2026-04-27).** TracePoint has zero roofing-module tests. Verified by enumeration: 8 test files in `tracepoint_port/TracePoint/tests/`, none reference `RoofingModule`, `vocabulary`, or `build_trade_input`. Behavior-level tests for the roofing module deferred to a future phase when ground-truth bidsets exist or sweep data drives test authoring.

**D-8 (informational, closed 2026-04-28).** C.3a inventory miscounts (60→64 components, 21→23 systems, 22→30 spec sections); SHA-1 of seed files unchanged. Verdict and gap list preserved; documentation patch in commit `eb49a08`. All 14 C.3b additions independently re-verified as genuinely missing from parked seeds. `flashing_drip_cap` is near-neighbor of parked `head_flashing` but judged distinct (membrane vs visible metal cap, routinely distinguished in commercial schedules; tightening the description further is tuning, declined per vault rule).

### Frontend test counts (consistent across all 2026-04-27 and 2026-04-28 ships)

| Runner | Count | Last verified |
|---|---:|---|
| `node run_tests.js` | 107/107 (88 unit + 19 integration) | D-8 follow-up 2026-04-28 |
| `node spotcheck_10b.js` | 7/7 | D-8 follow-up 2026-04-28 |
| `node spotcheck_cricket.js` | 4/4 | D-8 follow-up 2026-04-28 |
| `node spotcheck_durolast.js` | 8/8 | D-8 follow-up 2026-04-28 |
| `node spotcheck_manufacturer.js` | 14/14 | D-8 follow-up 2026-04-28 |
| `node mutation_test_step11.js` | 8/8 mutations caught | D-8 follow-up 2026-04-28 |

**Frontend version note (2026-04-28).** The file in workspace per `PROJECT_CLAUDE.md §6` is `Huckleberry_AI_6_3_1_Scope.html` (v6.3.1, 107 tests). The D-8 follow-up gate report referenced `Huckleberry_AI_6.3.0_Scope.html` (v6.3.0) — small naming discrepancy in that report; the substantive count is 107/107 either way and held throughout. Earlier conversation notes referenced "138/138 v6.3.5" — that file is NOT in the current workspace. The empirical truth is 107/107. Future Claude: do NOT try to reconcile to 138; the floor is what the runner produces.

---

## SECTION C — Bidsets that have actually been processed by v0.2 dispatch

These are real PDFs that real `run_dispatch()` calls were run against, with output JSONs persisted to disk. The processing happened; the JSONs exist; future Claude can read them.

### STACK corpus (15 bidsets)
- Source: `C:/huck stage 2/full bid sets/`
- Processed: 2026-04-25 to 2026-04-26 during v0.2 ship
- Outputs: `backend/test_fixtures/v0.2_outputs/<id>.json` (committed to repo on `phase2-v0.2-dispatch-port` branch)
- Symptom validation results: `backend/V0_2_VALIDATION.md` (sealed)

| Bidset ID | Pages | Detected system | scope_pages |
|---|---:|---|---|
| auto-zone-10891-jacksonville-mec-24-others | 28 | None | empty |
| auto-zone-vero-beach-fl | 61 | None | empty |
| b2607-aea-silverleaf-st-augustine-accelerated-construction-services-6 | 40 | None | empty |
| bearss-ave-distribution-center-university-marcobay-construction-3 | 91 | None | empty |
| chewy-vet-care-london-square-miami-jdr-fixtures | 93 | None | empty |
| chipotle-tarpon-springs-shell-tarpon-springs-strategic-construction | 39 | None | empty |
| hampshire-self-storage | 86 | None | empty |
| panda-express-bradenton | 59 | None | empty |
| panda-express-hialeah-gardens | 101 | None | empty |
| panda-express-naples-cdo-visible-construction-corp | 98 | None | empty |
| panda-express-san-antonio-candito-construction-2 | 38 | None | empty |
| shoppes-at-avalon-spring-hill-mec | 97 | None | empty |
| **taco-bell-weeki-wachee-compass-construction-management-2** | 88 | **`tpo`** (conf 0.95) | **[18, 19]** |
| vine-street-retail-center-kissimmee-great-southern-constructors | 138 | None | empty |
| wendy-s-fort-myers-great-southern-constructors-3 | 64 | None | empty |

**1 of 15 STACK bidsets** had non-null `detected_system` (Taco Bell). This is the empirical baseline. Whether 1/15 is correct, low, or high is unknown without ground truth.

### Public corpus (4 bidsets)
- Source: `C:/huck stage 2/not_stack-bidsets/`
- Processed: 2026-04-26
- Outputs: `backend/test_fixtures/public_corpus_outputs/<id>.json` (gitignored, exists on Daniel's machine)
- Sweep doc: `backend/PUBLIC_CORPUS_OBSERVATIONS.md` (uncommitted)

| Bidset ID | Pages | Detected system | scope_pages |
|---|---:|---|---|
| holabird-academy-elementary-middle-school | 96 | None | empty |
| sanibel-fire-and-rescue-station-172 | 90 | None | empty |
| suwannee-county-school-board-suwannee-high-school-courtyard-renovation | 31 | None | empty |
| uccs-cybersecurity-and-space-ecosystem-expansion | 133 | None | empty |

**0 of 4 public-corpus bidsets** had non-null `detected_system`. This is the empirical baseline.

### Shoppes-at-Avalon page-by-page read (roofing scope, 2026-04-26)

- Read by: Claude (extended-thinking) on 2026-04-26
- Method: PyMuPDF text extraction + per-page rasterization at 80–100 DPI for visual inspection
- Findings recorded in conversation; not in a separate document
- Real roofing scope confirmed visually: 60 mil TPO Carlisle (Firestone/Duro-Last NOT acceptable), R-30 polyiso, B22 metal deck (rasterized only, structural sheet S-201), parapet w/ metal coping, 4,173 SF roof per drainage calc, multiple RTUs, standing-seam awnings (distinct from main roof), 3 outparcel buildings bundled in one PDF
- ~25–30 pages of 97 are rasterized images with zero extractable text — the metal deck spec exists ONLY on those rasterized pages

This visual read is a single-bidset ground-truth observation. It is the most direct evidence we have of what's actually IN a STACK PDF on the roofing side.

### Shoppes-at-Avalon glazing scope read (C.3a, 2026-04-28)

- Read by: Claude Code (autonomous diagnostic, read-only) per `backend/C3_GLAZING_SEED_VALIDATION.md`
- Method: full-PDF text extraction via pdfplumber, 49-keyword scan, cross-referenced against `backend/test_fixtures/v0.2_outputs/shoppes-at-avalon-spring-hill-mec.json` sheet_map; identified A-601 (door schedule), A-602 (window types), A-201 (exterior elevations with SF-1 marks), A-303/A-202 (wall sections)
- 46 of 97 pages flagged glazing-relevant
- Real glazing scope confirmed: YKK aluminum storefront SF-1, aluminum medium-stile entrance doors (singles, NOT pairs), hollow metal exterior doors, hardware sets SET-1/SET-1A/SET-2, PAC-CLAD M-2 standing-seam metal awnings, MAPES M-4 pre-fabricated flat aluminum canopies, tempered + Low-E "high impact" glazing (non-HVHZ Florida code, Hernando County Spring Hill location)
- Verdict: parked seeds are **usable as starting vocabulary, with documented gaps** (4 components, 4 systems, 1 hardware set, 5 hardware-OEM manufacturers).

This is independent visual confirmation of glazing scope on the same bidset whose roofing scope was confirmed in the 2026-04-26 read. Two different content domains, same bidset, both confirmed visually.

---

## SECTION D — Diagnostics that have been run (not just discussed)

These are read-only diagnostic scripts or extended-thinking sessions that were executed against real data and produced real output files.

| Diagnostic | Script / Method | Output | Run date |
|---|---|---|---|
| Public corpus sweep | `backend/scripts/run_dispatch_on_public_corpus.py` | 4 JSONs in `backend/test_fixtures/public_corpus_outputs/` (gitignored) + `backend/PUBLIC_CORPUS_OBSERVATIONS.md` | 2026-04-26 |
| Intake Diagnostic Pass 1 | `backend/scripts/intake_diagnostic.py` | 19 per-page CSVs in `backend/test_fixtures/intake_diagnostic_outputs/` (gitignored) + `backend/test_fixtures/intake_diagnostic_summary.json` (gitignored) + `backend/INTAKE_DIAGNOSTIC.md` (uncommitted) | 2026-04-26 |
| Intake Diagnostic Pass 2 | `backend/scripts/intake_diagnostic_pass2.py` | `backend/test_fixtures/intake_diagnostic_pass2_summary.json` (gitignored) + `backend/INTAKE_DIAGNOSTIC_PASS2.md` (uncommitted) | 2026-04-26 |
| TracePoint folder discovery | (interactive Claude Code session) | `backend/TRACEPOINT_DISCOVERY.md` (uncommitted) | 2026-04-27 |
| C.3 glazing-module discovery | (interactive Claude Code session, read-only) | `/tmp/c3_discovery.md` (ephemeral); contents pasted into conversation 2026-04-28 | 2026-04-28 |
| C.3a glazing seed validation | (interactive Claude Code session against Shoppes-at-Avalon) | `backend/C3_GLAZING_SEED_VALIDATION.md` (committed via `eb49a08` after D-8 patches) | 2026-04-28 |
| Debug module spec report | (interactive Claude Code session, read-only of `tracepoint_port/TracePoint/modules/debug/`) | `backend/DEBUG_MODULE_REPORT.md` (uncommitted) | 2026-04-28 |
| D-8 mechanical re-verification + gap-list re-verification | (interactive Claude Code session, mechanical `len()` against parked seeds + SHA-1 verification + 14-entry duplicate check) | Documentation patch via commit `eb49a08`; CLAUDE.md §3 Decision 15 extended to cover trade modules; vault rule applied retroactively to RoofingModule, roofing_vocabulary, glazing_vocabulary | 2026-04-28 |
| Three-bidset sweep (Shoppes-at-Avalon / Vine Street / Bearss Ave) | `backend/scripts/sweep_three_bidsets.py` (untracked one-shot harness) — `run_dispatch` + per-page `RoofingModule().analyze` + per-page `GlazingModule().analyze` + `run_debug(ctx)` | `backend/SWEEP_OBSERVATION_shoppes-at-avalon.md` + `backend/SWEEP_OBSERVATION_vine-street.md` + `backend/SWEEP_OBSERVATION_bearss-ave.md` (committed via `cf107dd`) | 2026-04-28 |
| Bearss Ave profile diagnostic (pages 15 high-content + 82 low-content) | `backend/scripts/profile_diagnostic.py` (tracked reusable harness) — `time.perf_counter()` × 3 repeats × 4 ops × 2 pages | `backend/PROFILE_DIAGNOSTIC_bearss-ave.md` (committed via `112bca7`) | 2026-04-29 |

### Pass 1 headline numbers (measured, not estimated)

- 11 of 15 STACK bidsets had at least one positive manufacturer evidence hit
- 10 of 15 STACK bidsets had positive manufacturer evidence AND empty scope_pages
- 1 of 15 STACK bidsets had a negation-context manufacturer hit (Shoppes, "Firestone NOT ACCEPTABLE")
- 95 of 1,121 STACK pages had zero extractable text
- 79 of 350 public-corpus pages had roofing keyword evidence

### Pass 2 headline numbers (measured)

- 35 manufacturer hits inspected across the 10 "positive mfr, empty scope" STACK bidsets
- **29 of 35 hits were manufacturers in NON-roofing contexts** (sealants, drywall, ceiling insulation, electrical conduit) — same brand names, different product lines
- 0 of 35 had a Division 7 spec-section reference within ±200 chars
- 1 of 35 was in a negation context (Shoppes, the same one Pass 1 found)
- 5–6 of 35 appeared to be in explicit roofing-spec context (qualitative read of the snippets)

### Three-bidset sweep headline numbers (measured 2026-04-28)

- 3/3 real bidsets (Shoppes-at-Avalon, Vine Street, Bearss Ave) produced `project_scope.detected_system = None` despite presence of roofing scope.
- Per-bidset module wall-clocks: Shoppes 60.2s dispatch + 653.6s modules / Vine Street 82.0s + 654.6s / Bearss Ave 95.0s + 824.9s. Total 326 pages × 2 modules = 652 module calls; 0 exceptions.
- Roofing module produced 830 / 1,201 / 769 `fields` entries respectively; glazing module produced 43+22+22 / 100+12+23 / 177+31+24 (glazing/door/storefront items).
- Debug section 6 emitted 1 / 46 / 145 legend entries respectively; 0 / 0 / 1 quality flag.
- All 3 × 3 = 9 stub markers (sections 2, 4, 5 across the three bidsets) confirmed exact.
- **Replicates the intake-diagnostic Pass 2 finding** that the dispatch gate's detected_system path produces `None` on STACK-corpus bidsets where roofing scope is present but the manufacturer-mention paths sit in negation, non-roofing, or non-Division-7-proximate contexts. NOT graded as bug or feature; the receipt is replication, not correctness adjudication. Compare Taco Bell's 2026-04-28 C.5 run-through: `detected_system="tpo"` confidence 0.95, `scope_pages=[18, 19]` — clean positive on the bidset whose Division 7 spec sits at known coordinates. The sweep adds three negative receipts to that one positive.

### Bearss Ave profile diagnostic headline numbers (measured 2026-04-29)

- Page 15 (S-103 SPECIAL INSPECTIONS, top section-3 signal score 60): pdfplumber text 117.28ms median; pdfplumber tables **2,910.18ms** median (dominant); RoofingModule.analyze 184.31ms; GlazingModule.analyze 11.57ms. Per-page total 3.22s.
- Page 82 (unknown sheet, section-3 score 3, type=unknown, conf=0.0): pdfplumber text 3.93ms; pdfplumber tables 177.91ms (dominant); RoofingModule.analyze 11.09ms; GlazingModule.analyze 6.92ms. Per-page total 0.20s.
- High/low ratios: text 29.83×, table 16.36×, roofing 16.61×, glazing 1.67×. Per-page total ratio 16.13×.
- pdfplumber.extract_tables was the largest-median operation on both target pages. Sweep-average per-page (824.9s / 91 = 9.07s, modules only) is consistent with a Bearss-Ave bidset where a substantial fraction of pages exercise table extraction at the page-15 end of the spectrum.
- Dispatch this run 72.25s vs sweep reference 95.0s (-23.8% delta, run-to-run variance not investigated; not §7 stop).
- Three repeats per measurement; median is headline; ranges captured for sanity-check (`time.perf_counter`, stdlib only).

### TracePoint folder discovery numbers (2026-04-27)

- TracePoint folder location: `C:/huck stage 2/huckleberry/tracepoint_port/TracePoint/` (1.6 GB, full project tree)
- 5 v0.2 ported files SHA-1-verified byte-identical to source (or 3-line same-character diff for `dispatch_gate.py`)
- Phase B port surface measured: 2,854 lines source (B.1: 500, B.2: 1,212, B.3: 442, B.4: 700)
- 4 new backend dependencies needed for B.2: `opencv-python`, `numpy`, `shapely`, `Pillow` — installed cleanly on Daniel's Windows environment 2026-04-27 (versions: 4.13.0.92, 2.4.4, 2.1.2, 12.2.0)

### C.3 glazing-discovery numbers (measured against the TracePoint folder, 2026-04-28)

- `tracepoint_port/TracePoint/modules/glazing/` does NOT exist. `modules/` contains only `debug/` and `roofing/`.
- Zero `.py` files anywhere in TracePoint with "glazing" in the filename.
- Zero glazing test files. Zero glazing seed/data files in TracePoint.
- 5 files mention "glazing" — all documentation/planning prose, none are runnable code. TracePoint scoped glazing as Phase 5 future work but never coded it.
- Consequence: C.3 is build-against-contract, not verbatim port. First Huckleberry-original phase since v0.2 began.

### C.3a Shoppes-at-Avalon glazing seed validation (2026-04-28, with D-8 corrections 2026-04-28)

- Parked seed files inspected: `backend/seeds/glazing_assemblies.py` (1,311 lines, sha1 `ea80ff5d83cb97e4155ae12b68dcf24c816b4e34`), `backend/seeds/glazing_materials.py` (264 lines, sha1 `25c62bee7af80db5c198e16de205ecfc8a3d0051`)
- C.3a originally claimed 60 components / 21 systems / 22 spec sections. D-8 mechanical re-verification (2026-04-28) corrected to **64 components / 23 systems / 30 spec sections**. SHA-1 of seed files unchanged — seeds did not move; original C.3a counts were eyeball-walked, not mechanical.
- All 5 FBC constraints map correctly to bidset (Hernando County non-HVHZ branch).
- C.3a verdict: parked seeds are **usable as starting vocabulary, with documented gaps** — NOT "build from scratch."
- 14 documented gaps for C.3b to add: 4 components, 4 systems, 1 hardware set, 5 hardware-OEM manufacturers.
- D-8 follow-up confirmed all 14 are genuinely missing from parked seeds (mechanical re-verification, none are duplicates under different names — `flashing_drip_cap` is a near-neighbor of parked `head_flashing` but judged distinct).

### Debug module spec numbers (measured against TracePoint, 2026-04-28)

- `tracepoint_port/TracePoint/modules/debug/__init__.py` is empty.
- `tracepoint_port/TracePoint/modules/debug/debug_module.py` is 470 lines, sha1 `b5a4cf93ca7c02116fc00f6dc5a1514da1b18b60`.
- Zero tests reference debug_module in TracePoint.
- Public surface: `DEBUG_MODULE_VERSION`, `DebugContext` dataclass, `run_debug(ctx, geometry_results=None) -> DebugContext`, `print_report` CLI helper, `__main__` CLI block.
- Six diagnostic sections: dispatch health, scale comparison (geometry per page), page intelligence (per-page classification table), cross-reference graph (optional networkx), geometry diagnostics (when geometry_results passed), legend contents + quality flags.
- 1 new optional dependency required for full functionality: `networkx`. Sections 4 (cross-reference graph) and 5 (geometry diagnostics) require external state Huckleberry doesn't yet have (geometry route, networkx). Sections 1 (dispatch health), 3 (page intelligence), 6 (legend + quality flags) are immediately portable.
- Recommendation in `backend/DEBUG_MODULE_REPORT.md`: port partially, deferred to standalone C.5 sub-phase between C.4 and Phase D, with sections 1/3/6 immediate and sections 2/4/5 stubbed pending external state.

These numbers are not from memory or extrapolation. They are from actual output files that exist on disk.

---

## SECTION E — Decisions that have been made (with the date and reasoning)

The 18 ratified Phase 2 architectural decisions live in `CLAUDE.md` §3. They are not re-litigated here. The decisions listed below are session-specific decisions that came up since the realignment and that future Claude needs to NOT re-ask.

| Decision | When | Reasoning |
|---|---|---|
| v0.2 will be pushed to remote, eventually | Daniel's call, not a blocker | branches don't expire; pushing not blocking |
| v0.2.1 (D-4 + D-5 + schema migration) is queued, not started | Daniel chose to prioritize Phase B over v0.2.1 | 2026-04-27 |
| Phase A → Phase B sequencing is reversed in practice | Same — Daniel chose to start B without finishing A | 2026-04-27 |
| TracePoint folder pattern: read-only reference at `tracepoint_port/TracePoint/`, gitignored, deleted from working tree only after Phase B is sealed (Daniel's call) | Same as v0.2 used `C:/TracePoint/` | 2026-04-27 |
| `geometry_matrix.py` source filename preserved (NOT renamed to `geometry_engine.py`) | verbatim port discipline | Q1 2026-04-27 |
| `correction_store.py` includes in B.4 alongside architect_profile and storage | trio is load-bearing together | Q2 2026-04-27 |
| **SQLite stays verbatim in storage.py. Postgres deferred to Phase D.** | Daniel reversed earlier "Postgres adaptation" decision after seeing the layering more clearly. Backend cache for dispatch/profile is one concern (local SQLite, fine); multi-tenant job-folder Postgres is a different concern (Phase D). | 2026-04-27 |
| 8 small test PDFs (~3.9 MB) copy into `backend/test_fixtures/test_plans/`; 4 large PDFs gitignored | Q4 2026-04-27 |
| `test_integration.py` and `test_wendys_integration.py` defer to Phase E | TracePoint-FastAPI-shaped, not Huckleberry-shaped yet | Q5 2026-04-27 |
| Flat snapshot folder `C:/huck stage 2/tracepoint_port/` deleted; preserved tree at `huckleberry/tracepoint_port/TracePoint/` only | redundancy, ambiguity removal | Q6 2026-04-27 |
| `backend/core/__init__.py` stays empty per TracePoint convention | no re-exports added during Phase B | B.1 2026-04-27 |
| Single commit per phase, not per step | matches v0.2 convention | B.1 2026-04-27 |
| Phase B sub-phases shared one branch (`phase2-v0.3-B2-geometry-engine`) for B.2 + B.3 + B.4 | simpler than per-sub-phase branches | B.2+B.3 2026-04-27 |
| Autonomous big-run pattern for verbatim ports | match gate density to actual risk | B.2+B.3 2026-04-27 |
| §7 stops are for surprises requiring human judgment, not for surprises that can be mechanically verified in-session | precedent set during B.4 with `core.config` import in correction_store.py | B.4 2026-04-27 |
| Storage activation gate stays at `None` post-B.4 | B.4 ports the layer; activation is Phase D/E call | B.4 2026-04-27 |
| `dispatch_gate.py` is sacred; storage activation in `run_dispatch()` calls is NOT changed by B.4 | preserves v0.2 ship state | B.4 2026-04-27 |
| C.1 goes on its own branch, fresh from B.4 head — Phase C is conceptually distinct from Phase B | per-phase isolation pattern | C.1 2026-04-27 |
| C.1 ships as verbatim Protocol port + cross-trade integration notes appendix | smallest Phase C deliverable that unblocks C.2 | C.1 2026-04-27 |
| C.2 splits roofing port into 3 files: vocabulary, roofing_module, trade_input_builder (extracted helper) | preserves verbatim discipline by extracting build_trade_input from FastAPI route file | C.2 2026-04-27 |
| `build_trade_input()` extracted from `server/routes/trade.py` into standalone `trade_input_builder.py` | deliberate adaptation per `MARCH_ORDERS_C_2.md §2`; FastAPI route belongs to Phase E | C.2 2026-04-27 |
| RoofingModule NOT activated in dispatch_gate post-C.2; storage gate also still at None | preserves v0.2/B.4 ship state | C.2 2026-04-27 |
| C.3 path is build-against-contract, NOT verbatim port — TracePoint has no glazing module | C.3 discovery 2026-04-28 confirmed `tracepoint_port/TracePoint/modules/glazing/` does not exist | 2026-04-28 |
| C.3 splits into three sub-phases: C.3a (seed validation diagnostic, read-only), C.3b (contract extension + vocabulary build), C.3c-build (rough module + smoke test) | matches diagnostic-first principle: each phase makes the next decidable from data | 2026-04-28 |
| Parked glazing seeds stay parked. C.3b does NOT modify them. Vocabulary file overlays additions on parked seed content via import-and-overlay. | preserves "parked seeds are authoritative for what's already in them" discipline | C.3b 2026-04-28 |
| TradeModuleInput contract extension to add `tables` field is additive-only, non-breaking, well-bounded | first deliberate adaptation of a Phase-C ported file; per CLAUDE.md §3 Decision 15 contract evolution clause | C.3b 2026-04-28 |
| Awning/canopy trade-boundary question deferred from C.3b to C.4 | scope bounded by C.3a evidence; cross-trade decisions belong to C.4 cross-trade relationships layer | C.3b 2026-04-28 |
| **Vault rule extends to cover trade modules (CLAUDE.md §3 Decision 15 extended)** | Daniel's directive 2026-04-28: "modules should be still rough because we want to be able tune them later but when modules are rough and pass the vault rule then applies to them as well" | 2026-04-28 |
| Vault-ruled retroactively (2026-04-28): RoofingModule, roofing_vocabulary, glazing_vocabulary | per the vault rule extension | D-8 follow-up 2026-04-28 |
| Trade modules ship rough; tuning is gated to dedicated sessions with `core/` frozen | rough modules are diagnostic surfaces; tuning in same session as `core/` work makes prior diagnostic findings stale | 2026-04-28 |
| Three-bidset sweep (Shoppes, Vine Street, Bearss Ave) is the next data-gathering phase after C.3c-build + C.5 ship | Daniel's call: see what modules produce on real bidsets before deciding architecture; no tuning during sweep | 2026-04-28 |
| Sequencing for next sessions: C.3c-build → CLAUDE doc updates → C.5 (debug module port) → CLAUDE doc updates → three-bidset sweep | debug module is the diagnostic lens for the sweep; both should be in place before runs | 2026-04-28 |
| Observation reports (sweep deliverables) are descriptive only; no grading, no "correctness" comparison, no "needs ground truth" labels | Daniel's call: "if its pulling glazing scope even +20% leave it for now because thats a starting point for another time because i do think glazing will be solved by software and ml" | 2026-04-28 |
| All Phase 2 work pushed to remote 2026-04-28: `phase2-v0.2-dispatch-port`, `phase2-v0.3-B1-filter-pipeline`, `phase2-v0.3-B2-geometry-engine`, `phase2-v0.3-C1-trade-module-interface`, `phase2-v0.3-C2-roofing-module`, `phase2-v0.3-C3b-glazing-vocabulary` | 6/6 branches pushed via `git push -u origin <branch>`, all SHAs verified on remote vs local | 2026-04-28 |
| GitHub `main` lineage (`ca0f3ef367815a9e59d379709dbced448e8833a2`) is unrelated to Huckleberry feature branches; no reconciliation done | Push-time finding; not blocking | 2026-04-28 |

---

## SECTION F — What hasn't been validated (be honest)

These are claims, hypotheses, or open questions that exist in the project narrative but have NOT been verified empirically. Future Claude: be careful with these. They are speculative until the ledger marks them otherwise.

| Claim | Status | What would validate it |
|---|---|---|
| The 1/15 STACK detection rate is approximately correct | NOT VALIDATED | ground-truth review of each bidset (none done) |
| The dispatch gate's empty-scope rejections are correct on the 14 empty STACK bidsets | NOT VALIDATED | same — would need page-by-page read of each + scope ground truth |
| The 5–6 explicit-roofing-context manufacturer hits in Pass 2 that didn't detect scope are correct rejections by design | NOT VALIDATED | requires reading the 5–6 specific pages + cross-referencing with TracePoint paper §9's intended position-based filtering |
| The Postgres adaptation will be the right call when Phase D arrives | NOT VALIDATED | Phase D design conversation hasn't happened |
| Auto-notation will achieve "user spends less time correcting than typing from scratch" | NOT VALIDATED — this is the product hypothesis | A/B comparison with real estimators against a ground-truth corpus |
| The trade module interface design will generalize to glazing | PARTIALLY VALIDATED | C.1 Protocol satisfied by C.2 RoofingModule; contract extended additively in C.3b for glazing's table-driven needs. Full validation requires C.3c-build smoke test (mechanical) + sweep (descriptive) |
| Multi-building bundled PDFs (Shoppes pattern) appear at non-trivial frequency in real bidsets | NOT VALIDATED | only n=1 (Shoppes) confirms the pattern; supplier corpus would expand evidence |
| TracePoint paper §9's "filter text blocks to inside building polygon" approach actually works on STACK PDFs | NOT VALIDATED | sweep will produce first evidence of this in action (descriptive only, not graded) |
| Frontend file is v6.3.1 vs v6.3.5 | DOCUMENTED ENVIRONMENTAL FACT | the file in workspace is `Huckleberry_AI_6_3_1_Scope.html` (or 6.3.0 per one D-8 gate-report mention) and reports 107/107; v6.3.5 file with 138 tests is not in workspace |
| Parked glazing seeds (`glazing_assemblies.py`, `glazing_materials.py`) match real-world commercial glazing scope at the field level | PARTIALLY VALIDATED — C.3a Shoppes diagnostic evidence; one bidset only | full validation would require estimator review (C.3a non-conclusion #6) |
| RoofingModule (C.2) produces correct roofing scope on real bidsets | NOT VALIDATED — verbatim port from TracePoint, no upstream tests, no Huckleberry tests, never run on Huckleberry bidsets | sweep (descriptive only, observation not grading) |
| GlazingModule (when built in C.3c-build) produces correct glazing scope on real bidsets | NOT YET BUILT — C.3c-build is the next phase | sweep, then dedicated tuning session(s) after sweep observations exist |
| The vault rule (extended 2026-04-28 to cover trade modules) will preserve module diagnostic value over time | NOT VALIDATED — first concrete demonstration was D-8 follow-up declining the `flashing_drip_cap` description tuning impulse | multi-session experience over time |
| The 0/3 `detected_system=None` rate on the three sweep bidsets (Shoppes, Vine Street, Bearss Ave) is approximately correct | NOT VALIDATED — sweep replicates the Pass-2 finding (manufacturer mentions in negation/non-roofing/non-Division-7-proximate contexts, plus the full Bearss page-by-page read shows real roofing scope on rasterized structural sheets where dispatch's text-extraction can't see anything anyway) but the sweep is observation only, not adjudication | ground-truth review of each bidset's actual scope sheets vs. the manufacturer-mention paths the dispatch gate took on those pages. Compare against the Taco Bell C.5 run-through (`detected_system="tpo"` 0.95 confidence, `scope_pages=[18,19]`) which is the single positive baseline. Three negative receipts + one positive is n=4 — not a corpus |
| pdfplumber.extract_tables is the dominant per-page cost on at least some pages of at least one bidset | OBSERVED 2026-04-29 — Bearss Ave page 15 (high-content) measured at 2.91s table-extraction median, ~16× the next-largest per-page op. n=2 pages, n=1 bidset; not a corpus claim. Receipts in `backend/PROFILE_DIAGNOSTIC_bearss-ave.md` | extending the profile to Shoppes + Vine Street + 2-3 more bidsets at varied page-density would let the claim generalize. NOT scheduled this phase |

If a future session tries to claim any of these as verified, the answer is "no — point to where it was verified, or it isn't." Don't accept "obvious" or "the conversation said so."

---

## SECTION G — Files that should not be modified, with the verification that they haven't been

This is the inverse of Section A. These are sacred files. The ledger records that they remain untouched at the dates listed.

| Sacred file | Last verified untouched | Verification method |
|---|---|---|
| Phase 1 frontend HTML (v6.3.x in workspace) | D-8 follow-up 2026-04-28 | `node run_tests.js` produces 107/107 unchanged from B.1 baseline |
| All TracePoint sources at `tracepoint_port/TracePoint/` | D-8 follow-up 2026-04-28 | folder mtime / SHA-1 of files used as port source; debug module SHA-1 confirmed unchanged 2026-04-28 |
| `backend/core/config.py` | D-8 follow-up 2026-04-28 | sacred-floor check passes; git status shows unmodified |
| `backend/core/pdf_engine.py` | D-8 follow-up 2026-04-28 | same |
| `backend/core/zone_filter.py` | D-8 follow-up 2026-04-28 | same |
| `backend/core/context.py` | D-8 follow-up 2026-04-28 | same |
| `backend/core/dispatch_gate.py` | D-8 follow-up 2026-04-28 — storage gate STILL at `None`, RoofingModule NOT wired, GlazingModule NOT wired | same; activation explicitly not changed by B.4, C.2, C.3b, or D-8 |
| `backend/core/__init__.py` | D-8 follow-up 2026-04-28 | empty, verified via `wc -l` |
| `backend/seeds/roofing_spec_database.py` | D-8 follow-up 2026-04-28 | same |
| `backend/seeds/roofing_materials.py` (21-item ROOFING_SEED_ITEMS, Phase 2 v0.1) | D-8 follow-up 2026-04-28 | same |
| `backend/seeds/roof_assemblies.py` | D-8 follow-up 2026-04-28 | no consumer yet; untouched |
| `backend/seeds/glazing_assemblies.py` | D-8 follow-up 2026-04-28 | parked; sha1 `ea80ff5d83cb97e4155ae12b68dcf24c816b4e34` unchanged from C.3a record |
| `backend/seeds/glazing_materials.py` | D-8 follow-up 2026-04-28 | parked; sha1 `25c62bee7af80db5c198e16de205ecfc8a3d0051` unchanged from C.3a record |
| `shared/bidset_record.py` | D-8 follow-up 2026-04-28 | v0.1 schema; v0.2.1 ticket scope; untouched |
| `backend/tests/test_pdf_engine.py` | D-8 follow-up 2026-04-28 | 40/40 unchanged |
| `backend/tests/test_dispatch.py` | D-8 follow-up 2026-04-28 | 34 + 19 skipped unchanged |
| `backend/tests/test_filter_pipeline.py` | D-8 follow-up 2026-04-28 | 27/27 unchanged after B.1 |
| `backend/tests/test_geometry_matrix.py` | D-8 follow-up 2026-04-28 | 36/36 unchanged after B.2 |
| `backend/tests/test_polygon_scorers.py` | D-8 follow-up 2026-04-28 | 16/16 unchanged after B.3 |
| `backend/tests/test_architect_profile.py` | D-8 follow-up 2026-04-28 | 23/23 unchanged after B.4 |
| `backend/core/roofing_vocabulary.py` (C.2) | D-8 follow-up 2026-04-28 | vault-ruled 2026-04-28; sha1 `ec6c17f8…` unchanged from C.2 ship |
| `backend/core/roofing_module.py` (C.2) | D-8 follow-up 2026-04-28 | vault-ruled 2026-04-28; sha1 `ae9e5b28…` unchanged from C.2 ship |
| `backend/core/trade_input_builder.py` (C.2) | D-8 follow-up 2026-04-28 | sha1 `12215046…` unchanged from C.2 ship |
| `backend/core/glazing_vocabulary.py` (C.3b) | D-8 follow-up 2026-04-28 | vault-ruled 2026-04-28; sha1 `64249c8e…` unchanged from C.3b commit `14f4f53` |

### Vault-ruled files (CLAUDE.md §3 Decision 15, extended 2026-04-28)

These files are vault-ruled — they MUST NOT be modified in the same session that modifies any `backend/core/` file. Tuning happens in dedicated sessions with `core/` frozen.

| Vault-ruled file | Vault-rule applied | Date |
|---|---|---|
| TracePoint debug module (when ported in C.5) | inherit from TracePoint paper §7.5 + CLAUDE.md §3 Decision 15 (original) | future C.5 |
| `backend/core/roofing_module.py` (C.2) | retroactive vault-rule application via D-8 follow-up | 2026-04-28 |
| `backend/core/roofing_vocabulary.py` (C.2) | retroactive vault-rule application via D-8 follow-up | 2026-04-28 |
| `backend/core/glazing_vocabulary.py` (C.3b) | retroactive vault-rule application via D-8 follow-up | 2026-04-28 |
| `backend/core/glazing_module.py` (C.3c-build, when built) | applied at sealing per CLAUDE.md §3 Decision 15 | future C.3c-build |

---

## SECTION H — Where each verification artifact lives

If future Claude needs to RE-verify any claim in this document, here's where to look.

| Artifact | Location |
|---|---|
| Backend test outputs | `pytest backend/tests/ -v` (live execution) |
| Frontend test outputs | `node run_tests.js` etc. (live execution) |
| v0.2 STACK output JSONs | `backend/test_fixtures/v0.2_outputs/` (committed, on `phase2-v0.2-dispatch-port` branch and forward) |
| Public-corpus output JSONs | `backend/test_fixtures/public_corpus_outputs/` (gitignored, on Daniel's machine) |
| Pass 1 per-page CSVs | `backend/test_fixtures/intake_diagnostic_outputs/` (gitignored) |
| Pass 1 summary | `backend/test_fixtures/intake_diagnostic_summary.json` (gitignored) |
| Pass 2 summary | `backend/test_fixtures/intake_diagnostic_pass2_summary.json` (gitignored) |
| Pass 1 doc | `backend/INTAKE_DIAGNOSTIC.md` (uncommitted) |
| Pass 2 doc | `backend/INTAKE_DIAGNOSTIC_PASS2.md` (uncommitted) |
| Public corpus doc | `backend/PUBLIC_CORPUS_OBSERVATIONS.md` (uncommitted) |
| Discovery doc | `backend/TRACEPOINT_DISCOVERY.md` (uncommitted) |
| C.3 glazing-discovery doc | `/tmp/c3_discovery.md` (ephemeral, ran 2026-04-28; contents pasted into conversation) |
| C.3a glazing seed validation | `backend/C3_GLAZING_SEED_VALIDATION.md` (committed via `eb49a08` after D-8 patches) |
| Debug module spec | `backend/DEBUG_MODULE_REPORT.md` (uncommitted) |
| v0.2 validation receipt | `backend/V0_2_VALIDATION.md` (committed at v0.2 ship) |
| Discovered Issues register | `backend/DISCOVERED_ISSUES.md` (committed) |
| Cross-trade integration notes | `backend/CROSS_TRADE_INTEGRATION_NOTES.md` (committed via `23a459c`, extended via `14f4f53`) |
| TracePoint source | `tracepoint_port/TracePoint/` (gitignored, 1.6 GB) |
| TracePoint research paper | `TracePoint_AI_Research_Paper.docx` (sealed, source-of-truth for architectural decisions) |
| Branches on remote | https://github.com/dhellwarth86/huckleberry.git, all 6 Phase 2 feature branches verified 2026-04-28 |

---

## SECTION I — Discipline reminder for future Claude

If you find yourself thinking "this seems too tidy, maybe Daniel is overstating what's been done":

**You are wrong.** This ledger lists empirical verifications. Each row names the verification method. Re-run any verification you doubt — the test runners are still on disk, the PDFs are still on disk, the output files are still on disk, the TracePoint source is still in `tracepoint_port/`, the branches are on GitHub at https://github.com/dhellwarth86/huckleberry.git. Verification is reproducible. Speculation is not needed.

If you find yourself thinking "let me run another diagnostic to check":

**Read this ledger first.** Most diagnostics worth running have been run. Re-running them produces the same numbers (which is what reproducibility means) — re-running them is not progress unless you have a specific new question that the existing diagnostics can't answer.

If you find yourself thinking "Daniel hasn't validated this, let me re-verify it":

**Quote the row from this ledger that you want to re-verify, name the verification method, and tell Daniel why you don't trust the existing verification.** Don't make Daniel re-explain the project. He has explained it many times across many sessions. The cost of unnecessary re-verification is real.

If you find yourself thinking "the modules need to be tuned":

**STOP.** Read CLAUDE.md §3 Decision 15 (extended 2026-04-28). Trade modules ship ROUGH and are vault-ruled at sealing. They are diagnostic surfaces. Tuning happens in dedicated sessions with `core/` frozen, AFTER sweep data exists, NOT in the session you're currently in. The sweep is the data-gathering phase. Until that runs and observation reports exist, every tuning impulse is speculation.

If you find yourself thinking "the work isn't validated because the modules don't have behavior tests":

**Read Section F honestly.** Module correctness is in the NOT VALIDATED column. That is by design. The platform's path is: build rough, vault-rule, sweep against real bidsets, observe, tune in dedicated sessions later. Behavior validation is a future phase. The current work is verbatim port discipline (where validation IS byte-identical-to-source) plus rough-build-and-vault-rule for Huckleberry-original modules. Both are real engineering disciplines; neither is "untested code shipped without validation." Read the row, understand the verification method named, don't conflate "no behavior tests" with "no validation."

If something genuinely isn't in this ledger and you need to know whether it's true:

**Ask Daniel. Don't speculate. Don't probe. Don't run unauthorized diagnostics.** Say "this isn't in the ledger; should we add a verification step?" That's the right question.

The discipline of this ledger is the discipline of trust-but-verify-once. Verify once, write it down, point future readers at the verification. That's all this document is.

---

## End of validation ledger

This document is part of the canonical project artifacts. Read it after `CLAUDE.md` and before any new architectural conversation. Append new rows when new verifications happen. Don't edit existing rows.
