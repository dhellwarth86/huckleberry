# Phase G.5a — Soft Gate Report

**Branch:** `phase2-v0.3-G5a-annotation-persistence` (HEAD = `364e6d0`, +canon commit pending)
**Predecessor:** `phase2-v0.3-G4-scope-fix-and-backend-storage` head `a1d8ded`
**Started:** 2026-05-07
**Soft gate executed:** 2026-05-08 (Daniel-driven empirical run on Taco Bell)
**Verdict: SOFT GATE PASS — all checkpoints clean.**

---

## 1. Honest summary

Phase G.5a ships **annotation persistence** end-to-end (baseline items 5+6) plus the architectural correction Daniel locked mid-phase: **trade-specific knowledge — item names, system types, expected items, units, vocabulary — lives INSIDE the trade module; `core/job_storage.py` and `api/` are trade-agnostic and call Protocol methods, never importing per-trade constants.** Six commits across four checkpoints + two follow-on patches, sacred floor moved 255 → 273/19/0 backend (+18 tests net), frontend held 28/28 (mutation tests still authoritative — viewer rewire validated by Daniel-driven empirical run, not new automated tests).

Two baseline items moved from NOT MET to MET; one from PARTIAL to MET:
- **Item 5** (viewer tools save to DB): MET via new `annotations` SQLite table (`type` discriminator + JSON `data_json` blob) + 5 CRUD endpoints under `/jobs/{id}/annotations` + frontend viewer tools (line/pin/polygon) rewired to API relay (optimistic-push + async POST + refetch). Delete-cascade on `scope_systems` removal via explicit cleanup helper. Auto-pin extraction wired through `_extract_auto_pins_from_trade_output` reading `RoofingModule.equipment_pins` (currently empty until Stages 6-9 ship; banked).
- **Item 6** (takeoff reads from DB): MET via takeoff tab reading `App.currentResults.annotations` + `scope_systems` (rehydrated through `loadAnnotationsFromApi`) instead of in-memory state. Page-number labels per row added (CP3).
- **Item 8** (browser refresh persists everything): now MET (was PARTIAL) — `loadAnnotationsFromApi` runs at boot alongside `loadScopeFromApi`, viewer overlays rebuild from API state via `Viewer.rebuildOverlayFromState()`.

The mid-phase architectural correction (CP4 — TradeModule Protocol vocabulary unfreeze) is the load-bearing piece: when chat-Claude's draft of CP4 proposed importing `roofing_vocabulary.SYSTEMS/ITEMS` from `core/job_storage.py`, Daniel forbade it ("hardcoding roofing verbiage and systems outside of module is forbidden") and authorized vault unfreeze of the 4 trade-knowledge files for this CP only ("roofing module unlock vault is my command to make"; "1 then test if we have to change anything when test clears this gate vault rule goes back into effect"). The right fix shipped: 3 new `@classmethod` methods on the `TradeModule` Protocol (`get_palette_seed`, `get_expected_items`, `get_systems_catalog`) implemented inside each trade module, with `_resolve_trade_module(trade)` doing lazy LOCAL imports inside `job_storage.py` so per-trade constants never leak across the module boundary. A grep-assertion test now enforces this at the test floor (`test_no_per_trade_imports_in_job_storage`).

Empirical verification: Daniel drove Taco Bell live through the running stack across 3 iterations of CP4 follow-on patches (CP4.1 routing fix, CP4.2 DELETE race-condition fix). Final receipt verbatim: **"all clean good to go"**.

Per the unfreeze contract: vault re-locks at the new SHA-1 baseline. PROJECT_CLAUDE.md §4 updated.

---

## 2. Commit chain

| Commit | CP | One-line summary |
|---|---|---|
| `dd65940` | CP1 | backend annotations table + CRUD + auto-pin extractor (5 endpoints under `/jobs/{id}/annotations`; type discriminator + JSON data_json; cascade-delete on scope_systems removal; `_extract_auto_pins_from_trade_output` reading `RoofingModule.equipment_pins`) |
| `cebb58b` | CP2 | frontend annotations rewire — viewer tools (line/pin/polygon) relay through API; `loadAnnotationsFromApi` + `_flattenAnnotationRow` + `_bucketAnnotationsByType` + `Viewer.rebuildOverlayFromState()`; optimistic-push + async POST + refetch pattern |
| `19783ca` | CP3 | takeoff page-number labels per row + AUTO-DETECTED scope section + auto-pin distinct visual (dotted ring + 🤖 prefix) |
| `e6a2ef5` | CP4 | TradeModule Protocol vocabulary methods (`get_palette_seed`/`get_expected_items`/`get_systems_catalog`) + auto-seeded palettes via `_seed_palette_via_protocol` + EXPECTS checklist + line tool draft fix |
| `d8def62` | CP4.1 | route palette by `unit` (was `derive_from`) — fixes Cricket SF/manual + Equipment Curbs (vocabulary EA→SF, derive_from callout_count→manual; Cricket added to typical_items for tpo/pvc/epdm/modified_bitumen/built_up) |
| `364e6d0` | CP4.2 | viewer DELETE race-condition fix — pre-refetch in `viewerDeleteSelected`/`viewerClearAnnotations` + local-id fallback for optimistic-pushed entries that lack `_annId` until POST completes |

---

## 3. Soft-gate verification matrix

Daniel drove the gate live on Taco Bell on 2026-05-08. Each row labelled CP MET / CP MET WITH NOTE / CP BROKEN per etiquette norm.

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | Backend pytest sacred floor | **CP MET** | `255 → 273 passed, 19 skipped, 0 failed` (+18 net: +6 annotations CRUD/cascade, +1 auto-pin extractor, +3 Protocol classmethods (roofing palette/expected/catalog), +1 glazing skeletal, +2 `_seed_palette_via_protocol` (roofing+grep-assert), +1 create_scope_system auto-seed, +1 dispatch auto-seed, +1 cricket polygon, +1 equipment curbs SF, +1 grep-assert no per-trade imports). Final pytest receipt confirmed pre-canon. |
| 2 | Vault re-lock baseline captured | **CP MET** | 4 vault files NEW SHA-1s captured (per Daniel's contract: "1 then test if we have to change anything when test clears this gate vault rule goes back into effect"): `roofing_module 9a6085d4…`, `roofing_vocabulary 863ffb01…`, `glazing_module 1b449e97…`, `glazing_vocabulary 008ed191…`. UNCHANGED: `debug_module 78f71d90…`, `dispatch_gate 8b39fd0e…`, `pdf_engine daf06dd2…`. PROJECT_CLAUDE.md §4 updated to reflect the new baseline; vault rule re-engages at these values. |
| 3 | No per-trade imports in `core/job_storage.py` | **CP MET** | Test `test_no_per_trade_imports_in_job_storage` greps the file and asserts no `roofing_*` / `glazing_*` top-level imports. Lazy LOCAL imports inside `_resolve_trade_module(trade)` are the only path — verified by reading the helper directly. Architectural rule "hardcoding roofing verbiage and systems outside of module is forbidden" enforced at test floor. |
| 4 | Taco Bell live: TPO Single Ply scope card auto-seeded palette | **CP MET** | Daniel-driven dispatch, Scope tab → TPO Single Ply card shows: pinPalette = Drains/Scuppers/RTUs/Hatches/VTRs/Pipe Boots/Skylights (EA-routed); edgeTypes = Coping/Edge Metal/Gutter/Expansion Joint/Walk Pad (LF-routed); polygonTypes = Cricket (SF-routed; Equipment Curbs also SF after CP4.1). All seeded via `RoofingModule.get_palette_seed("tpo")` Protocol classmethod, no `roofing_vocabulary` import outside the module. Daniel-confirmed: "all clean good to go". |
| 5 | EXPECTS checklist renders below palette | **CP MET** | `_renderExpectsChecklist(s)` reads `App.currentResults.trade_outputs[*][trade].fields` filtered to `source='assembly_expected'`, dedupes across pages, renders one checkbox row per item. Empty state hides section. Slot in `renderSystemCard` between palette and AUTO-DETECTED sections. Daniel-confirmed during live run. |
| 6 | PIN tool: drop Drain pin → Takeoff drain row 0 → 1 with PAGE label | **CP MET** | Optimistic-push: pin entry appears immediately on overlay; async POST; refetch via `loadAnnotationsFromApi` updates `_annId`. Takeoff row updates with page-number label (CP3 addition). Round-trip survives F5. |
| 7 | LINE tool: pick line → click first point → click off-target → draft persists | **CP MET** | CP4 line tool draft fix: removed `Viewer.tempState = null` on validation-failure branches in `TOOL_HANDLERS.line.onDown`. Daniel-confirmed during live run after CP4 ship. |
| 8 | Manual ADD SYSTEM: palette auto-seeds with default (no system_code) | **CP MET** | `create_scope_system` extended: when `user_fields` is None/empty, calls `_seed_palette_via_protocol(sys_id, trade, system_code=None)`. Roofing module's `get_palette_seed(None)` returns the universal-typical-item palette. Test `test_create_scope_system_auto_seeds_when_user_fields_omitted` asserts both branches (omitted → auto-seeded; provided → no clobber). |
| 9 | DELETE button works first-click | **CP MET** | CP4.2 race fix: `viewerDeleteSelected` and `viewerClearAnnotations` now pre-refetch annotations before the destructive call so optimistic-pushed entries (which lack `_annId` until POST completes ~100-300ms) get their server IDs first. Local-id fallback covers entries created during the refetch window. Daniel-confirmed: "clean run delete button is a little wonky" → fixed in CP4.2 → final "all clean good to go". |
| 10 | Cricket polygon tool present in palette | **CP MET** | CP4.1 vocabulary fix: `cricket` added to `typical_items` for `tpo/pvc/epdm/modified_bitumen/built_up` systems. CP4.1 routing fix: palette dispatch by `unit` (SF → polygonTypes) not `derive_from` (which had skipped `manual` items). Daniel-confirmed: "crickets are a polygon tool that doesnt show up in auto or manual i need that to be able to get my crickets sqft just that everything else is good" → fixed in CP4.1. |
| 11 | Equipment Curbs measured as SF (was incorrectly EA) | **CP MET** | CP4.1 vocabulary fix: `curbs` ITEMS entry changed `unit` EA → SF, `derive_from` callout_count → manual. Now routes to polygonTypes. Test `test_equipment_curbs_routes_to_polygon_via_unit` asserts the placement. Daniel-confirmed: "equipment curbs should be a sqft too not a count but sqft as they are an unspecified size and have to be measured" → fixed in CP4.1. |
| 12 | Frontend Tests tab | **CP MET** | 28/28 (frontend test surface unchanged this CP — viewer rewire validated by Daniel-driven empirical run, not new automated tests; the existing scope-API tests assert API shape, which still holds). |

**Result: 12/12 CP MET. Soft gate PASS.** Daniel verbatim: *"all clean good to go"*.

---

## 4. Banked observations (out of G.5a scope; tracked for later)

These came out during execution but aren't G.5a fixes. Surfaced here so future phases inherit them with context.

### 4.1 — Stages 6-9 geometry wiring deferred since D.1, never picked back up

Recon (this session) confirmed: `RoofingModule._scope` populated, `assembly_expected` placeholders present for typical TPO items, BUT `equipment_pins=[]` and `fields[name].value=None` because dispatch_gate passes `equipment_callouts=[]` and `polygon_*=0.0`. This is by design — Stages 6-9 (geometry/scale/callout extraction) were deferred D.1 → "D.2 or E" per `dispatch_gate.py:1482-1485`, but D.2 did job-folder work, E did API + frontend strip, G.0-G.4 did optimization/scope work — none scheduled the geometry wiring.

**G.5a CP1 ships the auto-pin extractor (`_extract_auto_pins_from_trade_output`) wired and ready** — currently produces 0 rows on Taco Bell because RoofingModule's `equipment_pins` is empty. Once Stages 6-9 land, the extractor immediately starts producing rows; no further frontend work needed. The extractor's output flows through the same `annotations` table + frontend overlay rehydration that G.5a CP2 already wired.

This is a separate scheduled phase. Banked as **Phase G.6 — Stages 6-9 geometry wiring** (TBD scope).

### 4.2 — Glazing palette seeding is skeletal

`GlazingModule.get_palette_seed/get_expected_items/get_systems_catalog` ship as skeletal stubs returning entries from `GLAZING_PIN_TYPES` + `COMPONENTS` + `SYSTEMS`. The methods exist + are tested, so the Protocol contract is satisfied symmetrically with roofing. Real implementation waits on **Phase C.3c follow-on** (glazing as a first-class trade equivalent to roofing in the scope-detection path — already banked in G.4 §4.3). Once C.3c-follow ships, the glazing module's classmethods get real bodies; no other code changes needed because the Protocol is already in place.

### 4.3 — `_resolve_trade_module` knows trade NAMES but no per-trade vocabulary

The dispatch helper `_resolve_trade_module("roofing")` does a lazy LOCAL import of `RoofingModule` and returns the class. It knows the string `"roofing"` maps to the roofing module, and `"glazing"` maps to the glazing module. **This name-to-module mapping is the only "per-trade knowledge" that lives outside a trade module.** A future fourth-trade addition (e.g., siding) needs to add one branch to this helper and implement the Protocol — nothing else in `job_storage.py` or `api/` changes. Banked: when a third trade ships, consider whether a registry pattern (modules self-register via decorator) is worth the indirection. Premature for two trades.

### 4.4 — Viewer optimistic-push race window is real, not theoretical

CP4.2's DELETE race fix surfaced a 100-300ms window where optimistic-pushed annotations exist on the overlay (`_annId === undefined`) before the POST returns and assigns the server ID. CP4.2 handles DELETE; the same pattern likely applies to other operations Daniel hasn't exercised in the wonky-window yet (e.g., editing a freshly-pushed annotation before POST resolves). Banked: when a future phase adds annotation editing UI, audit the optimistic-push pattern across all mutation paths. The fix recipe is the same: pre-refetch before destructive/mutating call + local-id fallback.

---

## 5. What's NOT in G.5a (explicit, so future phases don't claim coverage)

- **Stages 6-9 geometry wiring** — see §4.1. Auto-pin INSTANCES (drain/scupper/RTU rows from PDF callouts) wait on this. Auto-pin TYPES (palette seeding) shipped in CP4.
- **Auto-pin promote-to-manual UI button** — when an auto-detected pin is wrong, user can't currently re-classify it inline. Banked as UX additive.
- **Color-picker UX for user-customizable palette colors** — colors are deterministic from `PIN_PALETTE_COLORS` + hash fallback. User can't override. Banked as UX additive.
- **Annotation editing UI** — user can create + delete annotations through viewer tools, but mid-life edits (rename, recategorize, retype) aren't wired. Banked.
- **Glazing palette seeding (real implementation)** — see §4.2. Waits on C.3c follow-on.
- **Excel export reads from DB** (baseline item 7) — annotations are now in the DB but Excel still client-side. Future phase.
- **Page reclassify writes to DB** (baseline item 4) — still parked.
- **Render optimization (PyMuPDF tiling)** — original Phase G/F1 scope, parked as next G phase.
- **3-bidset closing hard gate** — still parked.

---

## 6. Vault SHA-1 verification + re-lock

Per Daniel's unfreeze contract — *"1 then test if we have to change anything when test clears this gate vault rule goes back into effect"* — the 4 unfrozen files are now re-locked at NEW SHA-1 baseline values.

| File | Pre-G.5a (G.4 close) | Post-G.5a (re-lock baseline) | Status |
|---|---|---|---|
| `backend/core/roofing_module.py` | `ae9e5b284191b45de419faacf11771da27a548f9` | `9a6085d4a3fbe7bbafa4b920c75868261f3c3a60` | ✅ **RE-LOCKED at new SHA-1** |
| `backend/core/roofing_vocabulary.py` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` | `863ffb01de05ed8a55b1975268c3ff3a9c1d4252` | ✅ **RE-LOCKED at new SHA-1** |
| `backend/core/glazing_module.py` | `52c014421915ec6a66b4a6860b71a0a3274920f2` | `1b449e9716ef2fe83ee0f2546ad2281deef5ac55` | ✅ **RE-LOCKED at new SHA-1** |
| `backend/core/glazing_vocabulary.py` | `64249c8ef5f7d9db50added3c9a40836cba356ea` | `008ed1914422e7f63a8fe90833bcda9e0cb3b44a` | ✅ **RE-LOCKED at new SHA-1** |
| `backend/core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | `78f71d9030cde3b173389603f5f39bd6bedaac07` | ✅ HELD (not unfrozen) |
| `backend/core/dispatch_gate.py` (integration-frozen) | `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` | `8b39fd0eb4fa6e5a3a61f8da7f9a095be7bd091a` | ✅ HELD (not unfrozen) |
| `backend/core/pdf_engine.py` (integration-frozen) | `daf06dd266d52983a0c761669f8af1ed825088a7` | `daf06dd266d52983a0c761669f8af1ed825088a7` | ✅ HELD (not unfrozen) |
| `backend/core/trade_module.py` (Protocol — not vault) | (Protocol extension — not vault-tracked) | `676f4f32330b43e0e96410e73cf6dd5a72744e86` | ⚪ Not vault — Protocol contract |

**Vault rule re-engages at the post-G.5a SHA-1s.** Future sessions verify against this baseline. Same protocol G.3 used for `dispatch_gate.py` + `pdf_engine.py`.

---

## 7. Sacred floor verification

| Stage | Backend | Frontend |
|---|---|---|
| Pre-phase (G.4 close) | 255 passed, 19 skipped, 0 failed | 28/28 |
| Post-CP1 (`dd65940`) | ~262 passed, 19 skipped, 0 failed (+7 annotations CRUD + auto-pin extractor) | 28/28 |
| Post-CP2 (`cebb58b`) | ~262 passed, 19 skipped, 0 failed (frontend rewire — backend tests unchanged this CP) | 28/28 |
| Post-CP3 (`19783ca`) | ~262 passed, 19 skipped, 0 failed (frontend additions — backend tests unchanged this CP) | 28/28 |
| Post-CP4 (`e6a2ef5`) | ~270 passed, 19 skipped, 0 failed (+8: Protocol classmethods + auto-seed + grep-assert) | 28/28 |
| Post-CP4.1 (`d8def62`) | ~272 passed, 19 skipped, 0 failed (+2: cricket polygon + equipment curbs SF) | 28/28 |
| Post-CP4.2 (`364e6d0`) | 272 passed, 19 skipped, 0 failed (no test changes — race-condition fix verified by Daniel-driven empirical run) | 28/28 |
| **Post-canon (this report)** | **273 passed, 19 skipped, 0 failed** | **28/28** |

Backend +18 net tests; frontend held (mutation tests still authoritative — viewer rewire validated by Daniel-driven empirical run on Taco Bell, not new automated tests). No regressions at any boundary.

---

## 8. Receipts index

- **Plan file:** `~/.claude/plans/a-but-i-want-valiant-moler.md` (the CP4 Protocol-vocabulary unfreeze plan, approved by Daniel mid-phase)
- **Predecessor gate report:** `backend/G_4_GATE_REPORT.md`
- **Code commits:** `dd65940` (CP1), `cebb58b` (CP2), `19783ca` (CP3), `e6a2ef5` (CP4), `d8def62` (CP4.1), `364e6d0` (CP4.2) + canon commit at end of this sign-out
- **Live verification:** Daniel-driven empirical run on Taco Bell Weeki Wachee through CP4.1 + CP4.2 iteration; final receipt verbatim "all clean good to go"
- **Architectural correction lineage:** chat-Claude's draft of CP4 proposed `from core.roofing_vocabulary import SYSTEMS, ITEMS` in `job_storage.py`; Daniel forbade ("hardcoding roofing verbiage and systems outside of module is forbidden"); plan rewritten to TradeModule Protocol vocabulary methods with vault unfreeze authorization ("roofing module unlock vault is my command to make"); unfreeze contract specified ("1 then test if we have to change anything when test clears this gate vault rule goes back into effect"); vault re-locks at new SHA-1s per this report §6.

---

**End of Phase G.5a soft gate report.** Daniel reviews this, the canon updates ship in a single commit, branch awaits Daniel's explicit push approval.
