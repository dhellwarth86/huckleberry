# C.3a — Glazing Seed Validation Diagnostic

**Status:** Read-only observation. No production code touched. No vocabulary extended. No fix paths proposed in this document.
**Author:** Claude Code session, 2026-04-28
**Branch:** `phase2-v0.3-C2-roofing-module` (current; no new branch — observation task only)
**Prior reads in this session:** `PROJECT_CLAUDE.md`, `CLAUDE.md`, `tracepoint_port/TracePoint/CLAUDE.md` (debug-module-relevant sections noted but used in Task 2).

---

## 1. Files inspected

| File | Lines | SHA-1 |
|---|---:|---|
| `backend/seeds/glazing_assemblies.py` | 1,311 | `ea80ff5d83cb97e4155ae12b68dcf24c816b4e34` |
| `backend/seeds/glazing_materials.py` | 264 | `25c62bee7af80db5c198e16de205ecfc8a3d0051` |

Both read end-to-end. Both self-identify as compiled with AI assistance from public industry references and explicitly flag that they have not been reviewed by a practicing glazing estimator. `glazing_materials.py` self-identifies as a SKELETON / STUB; `glazing_assemblies.py` is more substantial but carries an "HONEST CAVEAT" warning at the top.

Top-level structure of `glazing_assemblies.py`:

| Section | Item count | Content |
|---|---:|---|
| GLAZING_COMPONENTS | 64 | universal vocab: frames, doors, glass types, coatings, perimeter/install, hardware, louvers, spandrel, interior trim |
| GLAZING_SYSTEMS | 23 | storefront (captured/SSG), curtain wall (captured / 2-side SSG / 4-side SSG), windows (alum fixed/operable, HM, vinyl), entrances (medium/narrow/wide-stile pair, automatic sliding, automatic swing), doors (HM single/pair, wood, overhead coiling/sectional), louver drainable, spandrel panel, interior office front, interior sidelite |
| HARDWARE_SETS | 7 | passage, privacy/storeroom, exterior single non-egress, exterior single egress, exterior pair egress, entrance pair medium-stile, ADA automatic entrance |
| ASSEMBLY_RELATIONSHIPS | 15 | door↔frame pairing, door↔hardware pairing, IBC 2406 safety glazing, IBC 1010 panic, automatic-door backup egress, sill receptor, HVHZ impact, spandrel back-pan, anchor wind zone, schedule mark balance, louver bird screen, fire-rated rating match, ADA clear opening, perimeter sealant, exterior threshold |
| FBC_CONSTRAINTS | 9 | HVHZ impact (TAS 201/202/203), non-HVHZ wind-borne debris, wind loads, safety glazing, energy code, egress hardware, fire-rated openings, accessibility, hurricane shutters |

Top-level structure of `glazing_materials.py`:

| Section | Item count | Content |
|---|---:|---|
| SPEC_SECTIONS | 30 | CSI 08-series → system type (08 11/14/31/33/34/36/38/42/4213/4229/51/5113/5123/5200/5300/43/4313/44/4413/80/8000/81/83/84/87/91/9100/95) |
| MANUFACTURERS | 12 | Kawneer, YKK AP, EFCO, Oldcastle BuildingEnvelope, Tubelite, Vistawall, Guardian Glass, Vitro, Cardinal, Steelcraft, Curries, VT Industries |
| MATERIAL_PROPERTIES | 4 sub-keys | glass thickness markers, coating markers, Florida HVHZ signals, drawing conventions (window/storefront/curtain wall/door) |
| GLAZING_PIN_TYPES | 8 | window, door, storefront, entrance, curtain_wall, louver, spandrel, height |

*Editor's note (2026-04-28): the original C.3a draft inventoried three counts incorrectly — `GLAZING_COMPONENTS` (60, actual 64), `GLAZING_SYSTEMS` (21, actual 23), and `SPEC_SECTIONS` (22, actual 30). Counts above corrected after mechanical re-verification (`len()` of the live dictionaries) during the D-8 follow-up session, 2026-04-28. The verdict (Section 5) and gap list do not depend on exact counts and are preserved as originally drafted; the verdict's narrative count cite ("60 components → 21 systems → 7 hardware sets → 15 cross-cutting relationship rules → 9 code constraints" in §5) reflects the original draft's numbers and is left as written. SHA-1 of both seed files is unchanged from the original C.3a inventory (`glazing_assemblies.py`: `ea80ff5d83cb97e4155ae12b68dcf24c816b4e34`; `glazing_materials.py`: `25c62bee7af80db5c198e16de205ecfc8a3d0051`) — the seeds themselves did not move.*

---

## 2. Bidset chosen and why

**Shoppes at Avalon — Spring Hill, FL — MEC** (`shoppes-at-avalon-spring-hill-mec`).
- 97 pages, STACK-produced PDF
- Already read end-to-end in this project's conversation history (per `CLAUDE.md` §2)
- Multi-parcel: at least Outparcel 4, Outparcel 5, Outparcel 6 in one bidset (mentioned in `CLAUDE.md` §2)
- Confirmed glazing content: "storefronts and pre-fabricated standing seam metal awnings" per the prompt and per the keyword scan run for this report
- Source PDF: `C:\huck stage 2\full bid sets\Shoppes at Avalon - Spring Hill - MEC.pdf` (per `pdf_path` field of `backend/test_fixtures/v0.2_outputs/shoppes-at-avalon-spring-hill-mec.json`)
- Project location: Spring Hill, Hernando County, Florida — wind-borne debris region but NOT HVHZ (HVHZ = Miami-Dade / Broward only). This is useful because the bidset exercises the FBC `non_hvhz_impact` branch of the seeds rather than the `hvhz_impact` branch.

**Caveat on choice:** This is one bidset, of one building typology (single-story retail strip outparcels with punched storefronts). It does not exercise curtain-wall systems, multi-story SSG, automatic sliding entrances, fire-rated glazing assemblies, or large louvers. Findings here cannot generalize to those scope shapes.

---

## 3. Glazing pages identified in the bidset

Method: full-PDF text extraction via `pdfplumber` for all 97 pages, then keyword filter against a 49-term list including DOOR SCHEDULE, WINDOW SCHEDULE, STOREFRONT, KAWNEER, YKK, EFCO, TEMPERED, LAMINATED, LOW-E, IGU, PANIC HARDWARE, MEDIUM STILE, HW-1, SF-1, CSI 08-series numbers, NOA, HVHZ, TAS 201/202/203, IMPACT, AWNING, CANOPY. 46 of 97 pages had at least one hit.

**Reconciliation against the dispatch-output sheet_map** (from `shoppes-at-avalon-spring-hill-mec.json`):

| Page idx | Sheet # | Title (sheet_map) | Glazing-relevant content (text-layer) |
|---:|---|---|---|
| 1 | A-601 | DOOR TYPES, SCHEDULES, AND DETAILS | Outparcel-4 Door Schedule (4 doors: 100/101/102 storefront, 103 HM dumpster); SET-1, SET-1A, SET-2 hardware definitions; DOOR TYPES A (HM) and B (medium-stile aluminum storefront, 3'-0"×7'-0"×1¾"); STOREFRONT THRESHOLD DTL, DOOR JAMB DETAIL, DOOR HEAD DTL; "ALL STOREFRONT DOORS TO HAVE 1/4" TEMPERED GLAZING" |
| 2 | G-003 | WALL TYPES | Wall sections — not glazing-primary |
| 18 | (A-601 of OP4) | (Outparcel 4 second sheet) | Same content as page 1 reconciled — OP4 door schedule with 4 doors |
| 19 | A-602 | WINDOW TYPES | Storefront window types A–G in elevation (heights 9'-4" to 9'-6", widths 4'-0" to ~18'-9"); STOREFRONT NOTES: "ALL STOREFRONT SYSTEMS TO BE HIGH IMPACT", "ALL GLASS TO BE TEMPERED", "ALL GLASS TO BE LOW-E", "REFER TO A-601 FOR DOOR INFORMATION" |
| 32 | (not in sheet_map) | (likely OP5 G-003) | Wall sections w/ HOLLOW METAL detail and IGU |
| 36 | A-100 | ARCHITECTURAL SITE PLAN | Site-level — multi-parcel layout |
| 37 | A-201 | EXTERIOR ELEVATIONS (OP4) | "ABOVE STOREFRONT" callouts × 4 bays; SF-1 mark x4; ST-1 cultured stone, EF-1 EIFS, M-2 standing-seam awning |
| 41 | A-303 | WALL SECTIONS (OP4 also) | Front/Rear elevations with SF-1 storefront marks at 9'-6" T.O. STOREFRONT; Keynote legend; **EXTERIOR FINISH SCHEDULE: SF-1 = STOREFRONT, YKK ALUMINUM STOREFRONT SYSTEM W/ TEMPERED GLAZING, COLOR DARK BRONZE**; M-2 = METAL PAC-CLAD PRE-FINISHED STANDING SEAM METAL AWNING (MATTE BLACK); M-4 = METAL MAPES PRE-FABRICATED PRE-FINISHED ALUM. FLAT CANOPY (PAC-CLAD GRAPHITE) |
| 46 | A-304 | WALL SECTIONS | HOLLOW METAL detail; ladder/hatch detail |
| 52 | (not in sheet_map by this number, but OP5 A-601 equivalent) | DOOR TYPES (Outparcel 5) | OP5 door schedule (9 doors: 1–4 ALUM/GLASS STOREFRONT TYPE A, 5–9 HOLLOW METAL TYPE B); SET-1 storefront and SET-2 HM hardware; OP5 storefront-elevation drawings showing dimension grids 12'-0" to 18'-5⅝" with EQ EQ EQ EQ mullion patterns; "INDICATES HIGH IMPACT TEMPERED GLAZING" hatching legend repeated |
| 65 | (not in sheet_map by this number) | (OP5 wall types or window types) | HOLLOW METAL + IGU |
| 70–77, 80–85 | (Outparcel 5/6 sheets) | EXTERIOR ELEVATIONS, KEYNOTE LEGENDS, EXTERIOR FINISH SCHEDULES | SF-1 YKK aluminum storefront repeats across both outparcels; M-2 PAC-CLAD standing-seam metal awning repeats; M-4 MAPES flat aluminum canopy repeats |

Pages 53–64 returned `text_len=0` from the text layer — likely rasterized structural sheets per the existing `CLAUDE.md` §2 observation about Shoppes ("~25–30 pages rasterized, zero text extraction"). Glazing scope on those pages would not be retrievable without OCR, but the schedule-driven information appears in the text-layer pages above and is sufficient for this validation.

---

## 4. Term-by-term comparison

### 4.1 Manufacturers (seed `MANUFACTURERS` vs bidset)

| Bidset term | In seed `MANUFACTURERS`? | Notes |
|---|---|---|
| YKK ALUMINUM STOREFRONT SYSTEM (SF-1, both outparcels) | ✅ Yes — `"YKK AP"` with alias `"YKK"` | Exact alias hit. The seed lists `YES 45` and `YES SSG` and `YHS 50` as YKK products; the bidset just says "YKK ALUMINUM STOREFRONT" without naming the YES line. Matches by manufacturer, not by line. |
| PAC-CLAD (M-1 coping, M-2 standing-seam awning, M-3 coping/scuppers) | ❌ No — not a glazing manufacturer in seed | PAC-CLAD is a metal-products manufacturer (Petersen Aluminum). Whether this belongs in the glazing seed is a trade-boundary judgment, not a defect of the seed. Standing-seam metal awnings often bid with the storefront/glazing package on small commercial; on larger jobs they bid with metal-panel scope. |
| MAPES (M-4 pre-fabricated flat aluminum canopy) | ❌ No | Same boundary observation. MAPES is a canopy manufacturer. |
| DRYVIT (EF-1…EF-5 EIFS) | n/a | Correctly NOT a glazing manufacturer; this is exterior-finish-system scope, not glazing. |
| SHERWIN-WILLIAMS (paints) | n/a | Not glazing. |
| CAL ROYAL (locksets, peep-hole) | ❌ No, but seed lists no hardware OEMs except door manufacturers (Steelcraft/Curries). The seed's `MANUFACTURERS` table for hardware OEMs is incomplete — it does not have any lockset/closer/exit-device OEM (Sargent, Schlage, Yale, Cal Royal, Von Duprin, Hager, etc.) | Bidset references "CAL ROYAL OR EQUAL" for keyed lever lock and door viewer. Hardware-OEM coverage gap is real but not surprising — `glazing_materials.py` self-flags hardware-set conventions and frame-finish vocabulary as missing in its TODO list (lines 257–263). |
| YALE SECURITY INC. (keyed lock set on OP5 SET-2) | ❌ No | Same gap as CAL ROYAL. |

**Observation:** the one storefront/curtain-wall manufacturer the bidset specifies (YKK) is in the seed and resolved by alias. Hardware OEMs are absent from the seed and present (in passing) in the bidset. Architectural metals (PAC-CLAD, MAPES) are absent from the seed; whether they belong is a trade-boundary question.

### 4.2 Glazing systems (seed `GLAZING_SYSTEMS` vs bidset systems)

| Bidset system | Closest seed system | Quality of match |
|---|---|---|
| Aluminum storefront framing with tempered glazing in punched openings (SF-1) | `storefront_captured` (or `storefront_ssg`) | Good. The bidset doesn't differentiate captured vs SSG in the schedule; that detail typically lives in the spec section 08 43 13 which is not in the page text I read. The seed's two-variant structure is correct in the abstract. |
| Aluminum entrance door, single, medium-stile, 3'-0"×7'-0"×1¾", SET-1 (single pivots, single cylinder strike, hydraulic closure, pull, thumb turn, silencers, weatherstrip/threshold/sweep) | `entrance_medium_stile_pair` | Mismatch on **single vs pair**. The bidset's storefront entrances on Shoppes are SINGLE doors at lobby and rears, not pairs. The seed has only `_pair` variants for medium/narrow/wide-stile entrance. The components for a single-leaf medium-stile entrance would be the same ÷ 2 ish, but there is no `entrance_medium_stile_single` slot in the seed. Real gap. |
| Aluminum entrance door + panic hardware (SET-1A) | implied by `entrance_medium_stile_pair` + `panic_hardware` conditional | Conceptually covered. |
| Hollow metal door, single, in HM frame, exterior, with deadbolt + lever lock + peep hole (SET-2 OP5) | `door_hollow_metal_single` | Reasonable match. Seed lists hinge, lockset, silencer as required and weatherstrip/sweep/closer/threshold as conditional — all present in bidset. Seed missing: explicit deadbolt slot (currently folds into lockset), explicit drip cap (seed has `head_flashing` which is adjacent), and viewer/peep-hole. |
| Storefront window types A–G — punched-opening storefront framing in elevation, no operable sashes | `window_aluminum_fixed` (closest) OR a "storefront window panel" that the seed does not have | Partial. The seed's `window_aluminum_fixed` describes a punched aluminum window. The bidset's "WINDOW TYPES A–G" are sections of the storefront framing system itself (mullion-divided wall panels at 9'-6" tall), not punched windows in CMU. They are storefront-style but tagged as "window types" on A-602. Vocabulary boundary issue more than a content gap. |
| Standing-seam metal awning (M-2) | ❌ Not present | Real gap if scoped to glazing. May correctly belong to roofing/metal scope per the cross-trade-integration-notes file (`backend/CROSS_TRADE_INTEGRATION_NOTES.md` is named in `CLAUDE.md` Phase B/C summary as covering "storefront/glazing↔roofing"). Awnings/canopies sit at the glazing↔roofing↔specialty-metal boundary. Not a defect of the glazing seed in isolation. |
| Pre-fabricated flat aluminum canopy (M-4) | ❌ Not present | Same trade-boundary issue. |
| Curtain wall (any variant) | seed has 3 variants | Not exercised by this bidset. |
| Operable aluminum window | seed has `window_aluminum_operable` | Not exercised by this bidset. |
| Vinyl window | seed has `window_vinyl` | Not exercised. |
| Hollow-metal pair | seed has `door_hollow_metal_pair` | Not exercised — all bidset HM doors are singles. |
| Wood door | seed has `door_wood_interior` | Not exercised. |
| Overhead coiling/sectional doors | seed has both | Not exercised. |
| Louver | seed has `louver_drainable` | Not exercised on the pages I read. |
| Spandrel | seed has `spandrel_panel` | Not exercised — single-story retail. |
| Interior office front / sidelite | seed has both | Not exercised. |

### 4.3 Glass types (seed `GLAZING_COMPONENTS` glass-* vs bidset)

| Bidset glass | Seed entry | Match |
|---|---|---|
| 1/4" tempered glazing in storefront doors | `glass_tempered` | ✅ |
| HIGH IMPACT TEMPERED — laminated impact-rated for non-HVHZ wind-borne debris | `glass_insulated_laminated` (HVHZ) or `glass_laminated` | Partial. The seed's `glass_insulated_laminated` is keyed to HVHZ (Miami-Dade NOA / TAS 201/202/203). Spring Hill is non-HVHZ wind-borne debris (FBC 1609 / ASCE 7 / ASTM E1886/E1996). The seed's `FBC_CONSTRAINTS["non_hvhz_impact"]` correctly distinguishes this branch. However the COMPONENT vocabulary doesn't have a non-HVHZ impact-laminated entry distinct from HVHZ — both would map to the same `glass_laminated` slot. Adequate at the component level; correctly distinguished at the FBC-constraint level. |
| Low-E glass | `coating_low_e` | ✅ — seed lists Solarban / LoE²-272 / SunGuard SN as typical products; bidset doesn't name the Low-E product line. |
| IGU mention on pages 32 / 65 | `glass_insulated_unit` | ✅ |
| Spandrel glass | `glass_spandrel` | Not exercised by this bidset. |

### 4.4 Hardware sets (seed `HARDWARE_SETS` vs bidset SET-1/SET-1A/SET-2)

| Bidset set | Closest seed entry | Match quality |
|---|---|---|
| SET-1 (single aluminum storefront, no panic): pivots, cylinder strike, hydraulic closure, pull handle + keyed cyl, thumb turn, silencers, weatherstrip+threshold+sweep | `hw_entrance_pair_medium_stile` (closest) — but it's specified for pair, two pivot sets, two closers, two sweeps, and no thumb turn | Off by single-vs-pair count. Components present in both lists. Seed missing a single-leaf entrance hardware set — and the SET-1 pattern (single pivot, single closer, exterior pull + interior thumb turn) is a common retail pattern that the seed does not have a one-line entry for. |
| SET-1A (SET-1 + panic) | `hw_exterior_single_egress` | Reasonable match conceptually — egress device on a single leaf — but SET-1A is also a storefront entrance, not a hollow metal egress door, so the frame and hinges are pivots not butts. Seed's `hw_exterior_single_egress` is more applicable to HM than to aluminum entrance. Real gap — bidset pattern (single aluminum entrance + panic) is not in the seed. |
| SET-2 (HM single, exterior, non-egress at OP4 dumpster; OP5 has 5 of these in mixed positions): 1.5 pair butt hinges, lever lock or keyed lock, hydraulic closure, latch guard, silencers, weatherstrip+threshold, drip cap, deadbolt; OP5 SET-2 also adds peep-hole | `hw_exterior_single_non_egress` | Good match on most components. Seed-side gaps: latch guard, drip cap, deadbolt as discrete items; viewer/peep-hole. |

### 4.5 Spec section / CSI numbers

The bidset's schedules and elevations did NOT print explicit CSI numbers like "08 43 13" on the pages I read. The schedule-page format is `MARK | CATEGORY | MANUF. | DESCRIPTION` (e.g. `SF-1 | STOREFRONT | YKK | ALUMINUM STOREFRONT SYSTEM W/ TEMPERED GLAZING, DARK BRONZE`). The CSI section number lives in the project specification book, not on the drawing sheets. This matches the seed's stated approach: "schedule-driven, not symbol-hunt." So the seed's `SPEC_SECTIONS` table is downstream-useful (for the spec book) but not directly exercised by reading drawing sheets. Cannot evaluate match quality here.

### 4.6 Florida code overlay (seed `FBC_CONSTRAINTS` vs bidset)

| Bidset signal | Seed constraint | Status |
|---|---|---|
| "ALL STOREFRONT SYSTEMS TO BE HIGH IMPACT" + "INDICATES HIGH IMPACT TEMPERED GLAZING" hatch legend on all storefront elevations | `non_hvhz_impact` (Spring Hill is Hernando County, non-HVHZ wind-borne debris) | ✅ Correct branch — bidset uses impact-rated tempered glazing rather than shutters; FBC 1609 / ASCE 7 / ASTM E1886/E1996 path. |
| "ALL GLASS TO BE LOW-E" + IGU references | `energy_code` (FBC Energy Conservation; ASHRAE 90.1; NFRC) | ✅ |
| Tempered glazing in doors and within 24" of door edge | `safety_glazing` (IBC 2406) | ✅ |
| ADA notes on hardware (lever, mounting height, max effort 5 lb interior / 8.5 lb exterior) | `accessibility` (ADA Standards 404) | ✅ — and the bidset's exterior 8.5 lb threshold matches FBC accessibility (vs ADA 5 lb), correctly noted as Florida-specific. |
| Panic hardware on storefront egress doors (SET-1A) | `egress_hardware` (IBC 1010.1.10) | ✅ |
| Project address / county on title block (Hernando County, FL) | sets the wind/HVHZ branch | The seed has the right FBC branches; whether the bidset is HVHZ vs non-HVHZ vs other isn't auto-extractable from the seed itself but the constraint text correctly distinguishes the branches. |

This section reads as the strongest part of the seed — the FBC overlay matches what the bidset actually does.

### 4.7 Drawing conventions (seed `MATERIAL_PROPERTIES["drawing_conventions"]`)

The seed claims storefronts appear with "multiple vertical mullions at regular spacing" on elevations; the bidset's elevations show exactly that on pages 41/74 (SF-1 marks at 9'-6" T.O. STOREFRONT with EQ EQ EQ mullion-spacing notation). Match.

The seed claims door schedules live "on architectural sheets (A-series)"; the bidset places them on A-601 — match.

The seed claims storefront detail callouts reference "08 43, series number, finish, glass spec"; the bidset references "REFER TO ELEVATIONS for storefront finish" and SF-1 in the exterior finish schedule supplies manufacturer, system, glass spec, and color. Same intent, slightly different format from what the seed describes — partial match.

### 4.8 Seed entries that look generic / aspirational vs grounded

Reading the seed honestly:

- The 60 components and 21 systems in `glazing_assemblies.py` are mostly grounded — every entry maps to a real component or system that an estimator would name. The exception class is items like `shadow_box`, `pivot_hinge` (vs continuous_hinge) priority, `glass_wired` (legacy), `entrance_automatic_sliding` — these are real but rare on small commercial.
- `glazing_materials.py` is openly a skeleton. Its 12-manufacturer list has six storefront/curtain-wall makers (Kawneer, YKK AP, EFCO, Oldcastle BE, Tubelite, Vistawall) and three glass coaters (Guardian, Vitro, Cardinal). That's reasonable coverage of the storefront market but is incomplete on the door side (only Steelcraft, Curries, VT — no Mesker, Republic Doors, Pioneer Industries, Marshfield, Eggers Industries, Algoma, Graham, et al.) and entirely absent on hardware OEMs.
- The 15 ASSEMBLY_RELATIONSHIPS rules are uniformly grounded in code or industry convention (IBC 2406, IBC 1010, ASHRAE 90.1, AAMA, BHMA, ADA 404, IBC 716/NFPA 80). None look fabricated.
- The 9 FBC_CONSTRAINTS are accurate as stated. The HVHZ impact tests (TAS 201/202/203), non-HVHZ wind-borne debris regions, FBC 1609, NFRC are correctly named.

---

## 5. Honest verdict

**Usable as a starting vocabulary, with documented additions needed.** Not "build from scratch."

**Reasoning:**

1. The big-ticket terminology in the bidset (STOREFRONT, TEMPERED, LOW-E, HOLLOW METAL, ALUMINUM ENTRANCE, MEDIUM STILE, PIVOTS, PANIC HARDWARE, HIGH IMPACT, IGU, YKK) appears in the seed in language that a parser could match.
2. The schedule-driven approach the seed claims (`glazing_assemblies.py` lines 22–32: "Table extractor finds Window/Door/Storefront schedules → OCR reads cells → cross-reference marks → assembly lookup → takeoff rows") is exactly the workflow this bidset's data structure (A-601 door schedules, A-602 window types, A-201 elevation SF-1 callouts, exterior-finish schedule) supports.
3. The Florida-code overlay is on-target. Both the HVHZ and non-HVHZ wind-borne debris branches are correctly distinguished, and Spring Hill exercises the non-HVHZ branch.
4. The component/system structure (60 components → 21 systems → 7 hardware sets → 15 cross-cutting relationship rules → 9 code constraints) is the right shape — it matches what `roof_assemblies.py` did for roofing scope. The architecture transfers.

**Documented gaps surfaced by this one bidset:**

- No `entrance_*_single` variants (only pairs). Bidset uses single aluminum storefront entrances.
- No hardware set for "single aluminum storefront entrance + panic" (SET-1A pattern).
- No standing-seam metal awning entry (M-2 PAC-CLAD); also no flat aluminum pre-fab canopy entry (M-4 MAPES). These may correctly belong to a metal/specialty-metal seed rather than glazing — that's a trade-boundary judgment.
- No discrete component slots for: deadbolt, drip cap, latch guard, peep-hole / door viewer.
- Hardware-OEM manufacturer table is empty (Cal Royal, Yale Security, Sargent, Schlage, Von Duprin, etc.).
- "Window types A–G" on A-602 are storefront-framing wall panels, not punched windows. Seed has `window_aluminum_fixed` for a punched window but no "storefront window panel" variant — naming-boundary issue.
- The materials skeleton's TODO list (lines 257–263) — review by glazing estimator, regional Florida distributors, hardware-set conventions, frame-finish vocabulary, impact-rated product flags, glass-type shorthand, real schedule-entry examples — remains unaddressed and self-flagged in the file.

**Strengths reinforced by this one bidset:**

- YKK manufacturer detection works via the alias table.
- FBC overlay structure (HVHZ vs non-HVHZ) is correct.
- Tempered / Low-E / IGU vocabulary aligns.
- Hollow-metal door + frame + hardware components decompose cleanly.
- The ASSEMBLY_RELATIONSHIPS and FBC_CONSTRAINTS sections are largely correct as written.

---

## 6. Explicit non-conclusions

This is one bidset, not ground truth. Whatever the verdict above, it is preliminary evidence — not calibration.

Specific non-conclusions:

1. **One bidset, one building typology.** Shoppes is single-story multi-parcel retail with punched storefronts. It does not exercise: curtain wall (any variant), structural silicone glazed systems, multi-story SSG, automatic sliding/swinging entrances, fire-rated openings, large louvers, spandrel back-pan/insulation, interior office fronts, vinyl windows, wood doors, overhead coiling/sectional doors, or operable windows. The seed's coverage of those system types may be excellent or terrible — this report cannot say.
2. **STACK-produced PDF.** Shoppes was processed through STACK (per the existing observations in `backend/INTAKE_DIAGNOSTIC.md` etc.). Some 25–30 of its pages are rasterized with zero text-layer extraction (per `CLAUDE.md` §2 Shoppes notes). Glazing scope ON those rasterized pages was not validated here. If glazing-relevant detail sheets are among the rasterized pages, this report missed them. The structural-deck pages 53–64 specifically returned `text_len=0`; glazing detail sheets typically would not be on structural pages but the gap is documented.
3. **Florida bias.** Both the bidset and the seed's `FBC_CONSTRAINTS` are Florida-weighted. Whether the seed generalizes to non-Florida code regions (Texas wind, California seismic, Northeast/Midwest energy code) is not testable from this one Florida bidset.
4. **Schedule-driven workflow not implemented.** This report read text-extracted page content and matched terms. The seed's stated workflow ("table extractor → OCR → mark cross-reference → assembly lookup") would behave differently on the same pages, especially on the rasterized ones, and especially on schedule-cell parsing where pdfplumber-table extraction may or may not pick up the column structure cleanly. This report did not run that workflow; it ran a keyword-presence test only.
5. **No measurement of false-positive rate.** This report tested whether seed terms find bidset terms, not whether the seed would mis-fire on non-glazing text in the same plan set. A real validation would also score precision (e.g. does "STOREFRONT" in a non-glazing context — like a finish-schedule reference — falsely activate a system).
6. **No estimator review.** Both seed files self-flag that they have not been reviewed by a practicing glazing estimator. This report does not substitute for that review. Whether the seeds are accurate from a glazing-bidder's perspective on issues like: anchor spacing wind-zone tables, frame-finish vocabulary (anodized vs Kynar 500 vs powder coat vs PVDF), hardware-set numbering conventions in the actual spec section 08 71 00, and HVHZ NOA-tracking workflow, this report cannot say.
7. **The "verdict" is preliminary.** It says: "the seeds are usable as a starting vocabulary, with documented gaps." It does NOT say: "the seeds are validated," "the seeds are calibrated," or "C.3 should reuse the seeds wholesale." Those are downstream decisions that require more bidsets, an estimator review, and a planning conversation about C.3's path (verbatim port vs build-against-contract vs hybrid).
8. **No fix paths in this document.** This is a diagnostic. It names what is in the seeds, what is in the bidset, and where they line up vs diverge. It does not propose a vocabulary expansion, a re-shape of the assemblies, or a path forward. Those decisions are for the C.3 planning conversation, not this report.

---

**End of C3_GLAZING_SEED_VALIDATION.md.**
