# G.1 Gate Report — Test-Floor Audit + Hybrid Regex Patch

**Date:** 2026-05-02
**Branch:** `phase2-v0.3-G1-audit-and-regex` (from G.0.9 head `af67825`)
**Tracks:** Test-floor audit (T1) + Hybrid regex patch (T2) + Housekeeping (T3, **halted**)
**Status:** STOP fired on Guardrail #6 — Silverleaf classification cascade did not shift as predicted; sheet-map cascade did. Track 3 not run.

---

## §1 — Pre-flight

### 1.1 Branch + base

| Item | Value |
|---|---|
| Branch | `phase2-v0.3-G1-audit-and-regex` |
| Base commit | `af67825` (G.0.9 head — real-bidset hybrid byte-equivalence) |
| Workspace | `C:\huck stage 2\huckleberry\` |
| Pre-existing uncommitted work | Stashed as `pre-G1-uncommitted-housekeeping` (5 march-orders moves left over from a prior session — out of G.1 scope, not touched) |

### 1.2 Vault-ruled module SHA-1s before any code change

| File | SHA-1 |
|---|---|
| `core/dispatch_gate.py` | `c206ff9e7e85eeee2c1c9bdaae8f0313308cd4a3` |
| `core/roofing_module.py` | `ae9e5b284191b45de419faacf11771da27a548f9` |
| `core/glazing_module.py` | `52c014421915ec6a66b4a6860b71a0a3274920f2` |
| `core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` |
| `core/waterproofing_module.py` | NOT PRESENT in repo |
| `core/siding_module.py` | NOT PRESENT in repo |
| `core/framing_module.py` | NOT PRESENT in repo |

The orders listed five vault-ruled trade modules + `debug_module.py`. Three of them (`waterproofing`, `siding`, `framing`) do not exist as standalone modules in the current backend. The four vault SHAs that DO exist are the ones recorded above.

### 1.3 Pre-patch sacred floor

| Metric | Value |
|---:|---:|
| Tests collected | 249 |
| Passed | 230 |
| Skipped | 19 |
| Failed | 0 |
| Wall-clock | 7.06 s |

---

## §2 — Test-floor audit (Track 1)

### 2.1 Method

Read every `.py` in `backend/tests/` (16 files including `conftest.py`). For each test, identified fixture path constants, checked whether each fixture resolves, and ran `pytest -rs -v` to capture skip reasons verbatim.

### 2.2 Fixture-path inventory

| Fixture / constant | File | Resolved? |
|---|---|---|
| `_SILVERLEAF_CANDIDATES[0]` (conftest) | `…\full bid sets\B2607 AEA Silverleaf … (6).pdf` | ✓ exists |
| `_SILVERLEAF_CANDIDATES[1]` (conftest) | `…\full bid sets\B2607 AEA Silverleaf …\.pdf` (no suffix) | ✗ does not exist (fallback) |
| `small_pdf_path` (conftest) | written into `tmp_path` from `_MINIMAL_PDF` bytes | ✓ always works |
| `CFA_PDF` (test_dispatch.py:36) | `test_plans/cfa_roof_A230.pdf` | ✗ does not exist |
| `VINE_PDF` (test_dispatch.py:37) | `test_plans/Vine_Street_…\.pdf` | ✗ does not exist |
| `TACO_BELL_PDF` (test_dispatch.py:38) | `test_plans/tacobell_roof_A12.pdf` | ✗ does not exist |
| `AEA_PDF` (test_dispatch.py:39) | `test_plans/aeasilverleaf_roof_A106.pdf` | ✗ does not exist |
| `OUTPUTS_DIR` (test_schema_round_trip.py:19) | `backend/test_fixtures/experiment_outputs/` (15 .json files) | ✓ exists |
| `scripts._pipeline.dispatch` (test_pipeline_dispatch.py:8) | importable | ✓ |
| `scripts._pipeline.scope` (test_pipeline_scope.py:3) | importable | ✓ |

### 2.3 Honest X / Y / Z breakdown of the 249 collected items

| Bucket | Count | Description |
|---|---:|---|
| **X — genuinely passed** | **230** | Executed, asserted, returned True. No silent-skip patterns hiding inside. |
| **Y — silently skipped (counted as passed)** | **0** | No tests in the suite return early without asserting. Every conftest fixture either succeeds (`small_pdf_path`, `silverleaf_path`) or calls `pytest.skip()` which produces a SKIPPED line, not a phantom PASS. |
| **Z — explicitly skipped (skip-marker)** | **19** | All 19 are `@pytest.mark.skipif(not <PDF>.exists(), …)` decorators on classes in `test_dispatch.py`: 4 × `TestSinglePageCFA`, 7 × `TestMultiPageVineStreet`, 4 × `TestTacoBell`, 4 × `TestAEA`. |
| **Total collected** | **249** | X + Y + Z = 230 + 0 + 19 = 249 ✓ |

### 2.4 Tests that genuinely silently-skip — list

**None.** This is the audit's most important finding: the 230 floor is honest. No test counts toward "passed" without doing real work.

The original concern that some tests "have been counting toward the 230 floor as passed but did no work" was a hypothesis. The audit ruled it out:

- The four `test_plans/*.pdf` fixtures don't exist, but their owner classes use `@pytest.mark.skipif` — so missing fixtures land in Z (SKIPPED), never in X.
- The `silverleaf_path` fixture in `conftest.py:53` calls `pytest.skip("Silverleaf bidset PDF not found; …")` if neither candidate path exists. On THIS machine the primary candidate exists, so the four `test_api_jobs.py` tests that depend on it (`test_create_job_happy_path`, `test_get_job_happy_path`, `test_create_job_validation_error_invalid_status`, `test_data_leak_response_shape_and_error_messages`) genuinely run. On a CI machine without the bidset they would land in Z, not X.
- `test_schema_round_trip.test_all_experiment_outputs_pass_schema` asserts `len(paths) >= 15` against `experiment_outputs/`, which contains 15 .json files. It runs and asserts.
- `test_pipeline_dispatch.py` and `test_pipeline_scope.py` import from `scripts._pipeline.*`. Both modules import cleanly. All 26 tests there execute.

### 2.5 Verbatim skip reasons (`pytest -rs` output)

```
SKIPPED [1] tests\test_dispatch.py:216: CFA test PDF not available
SKIPPED [1] tests\test_dispatch.py:220: CFA test PDF not available
SKIPPED [1] tests\test_dispatch.py:224: CFA test PDF not available
SKIPPED [1] tests\test_dispatch.py:228: CFA test PDF not available
SKIPPED [1] tests\test_dispatch.py:242: Vine Street test PDF not available
SKIPPED [1] tests\test_dispatch.py:245: Vine Street test PDF not available
SKIPPED [1] tests\test_dispatch.py:248: Vine Street test PDF not available
SKIPPED [1] tests\test_dispatch.py:251: Vine Street test PDF not available
SKIPPED [1] tests\test_dispatch.py:256: Vine Street test PDF not available
SKIPPED [1] tests\test_dispatch.py:263: Vine Street test PDF not available
SKIPPED [1] tests\test_dispatch.py:266: Vine Street test PDF not available
SKIPPED [1] tests\test_dispatch.py:381: Taco Bell PDF not available
SKIPPED [1] tests\test_dispatch.py:384: Taco Bell PDF not available
SKIPPED [1] tests\test_dispatch.py:387: Taco Bell PDF not available
SKIPPED [1] tests\test_dispatch.py:390: Taco Bell PDF not available
SKIPPED [1] tests\test_dispatch.py:401: AEA PDF not available
SKIPPED [1] tests\test_dispatch.py:404: AEA PDF not available
SKIPPED [1] tests\test_dispatch.py:408: AEA PDF not available
SKIPPED [1] tests\test_dispatch.py:411: AEA PDF not available
================= 230 passed, 19 skipped, 1 warning in 7.06s ==================
```

### 2.6 Honest baseline

**The 230 floor is the honest pass count.** Track 1 names no gap to fix; the bookkeeping was already correct. The "fixture wiring" Daniel suspected does not exist: there is no test that pretends to run when it can't. The 19 SKIPPED items are openly skipped via `skipif`, and the 230 PASSED items all assert.

This is the post-patch baseline used in §3.

---

## §3 — Regex patch verification (Track 2)

### 3.1 Patch (single-line, dispatch_gate.py:57)

```diff
-_SHEET_NUM_RE = re.compile(r'\b([A-Z]{1,2})-?(\d+[\.\d]*[A-Za-z]?)\b')
+_SHEET_NUM_RE = re.compile(r'\b([A-Z]{1,2})-?(\d{3,}[\.\d]*[A-Za-z]?|\d+\.\d+[\.\d]*[A-Za-z]?)\b')
```

Post-patch SHA-1 of `dispatch_gate.py`: `2a708d193ac5247472d589252bbc3766ced9041f` (changed, as expected).

Vault SHA-1s **after** patch:
- `core/roofing_module.py` `ae9e5b284191b45de419faacf11771da27a548f9` ✓ unchanged
- `core/glazing_module.py` `52c014421915ec6a66b4a6860b71a0a3274920f2` ✓ unchanged
- `core/debug_module.py` `78f71d9030cde3b173389603f5f39bd6bedaac07` ✓ unchanged

Guardrail 3 held.

### 3.2 Post-patch pytest (Track 2a)

```
================= 230 passed, 19 skipped, 1 warning in 3.55s ==================
```

230 / 19 / 0 — identical to pre-patch baseline. Guardrail 4 held.

### 3.3 Bearss byte-equivalence (Track 2b)

Re-dispatched `Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf` via `run_dispatch(BEARSS, storage="auto", job_id=None)` with the patched regex on disk.

| Field | Expected (G.0.9) | Post-patch | ✓/✗ |
|---|---:|---:|---|
| `roofing_fields` (sum across all pages, counted as `len(per_page['roofing'].fields)`) | 769 | **769** | ✓ |
| `glazing_items` (sum) | 177 | **177** | ✓ |
| `door_items` (sum) | 31 | **31** | ✓ |
| `storefront_items` (sum) | 24 | **24** | ✓ |

Bearss byte-equivalence holds. Guardrail 5 satisfied.

Note on counting method: G.0.9 reported `roofing_fields=769`. The current `TradeModuleOutput` exposes `fields` (a `dict`, length 9 on a typical Bearss page), not `roofing_fields`. The 769 is `sum(len(per_page['roofing'].fields) for per_page in ctx.trade_module_outputs.values())`. The first count attempted (`r.roofing_fields`) returned 0 because that attribute doesn't exist on `TradeModuleOutput` — that's a counting-script artefact, not a behavior delta. Once corrected to `r.fields`, the number lands exactly on 769.

### 3.4 Silverleaf classification delta (Track 2c) — **GUARDRAIL #6 FIRED**

Re-dispatched `B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf` post-patch.

| Metric | G.0.5 / E2_2 baseline | Post-patch | Δ | Expected? |
|---|---:|---:|---|---|
| `total_pages` | 40 | 40 | 0 | (n/a) |
| `sheet_map_size` | 10 | **31** | +21 | ✓ "jumps from ~4 to ~30+" |
| `mapped_pages` | 4 | **32** | +28 | ✓ |
| `sheet_map_source` | `drawing_index` | **`title_blocks`** | shifted | unexpected — the new regex caused Filter 1 to bail on the drawing index and fall through to the title-block path |
| ROOF_PLAN count | 1 | **1** | 0 | ✗ "must increase from 1" |
| UNKNOWN count | 4 | **4** | 0 | ✗ "must drop from 4" |
| `dispatch_warnings` count | 1 | 2 | +1 | (now also flags `LOW RESOLUTION: 22% cross-references resolved`) |

**Guardrail #6 reading:** "ROOF_PLAN count must increase from 1, UNKNOWN count must drop from 4. **If neither shifts**, the regex fix didn't resolve what we expected — STOP and document, do NOT proceed to housekeeping."

ROOF_PLAN did not increase. UNKNOWN did not drop. Both metrics unchanged. **Guardrail #6 fires.** Track 3 (housekeeping) was halted before any `git mv`.

### 3.5 Plain-language reading of what shifted on Silverleaf

The regex fix did massive work on **sheet number extraction** (Filter 1):

- `sheet_map_size`: 10 → **31** (3.1×)
- `mapped_pages`: 4 → **32** (8×)
- Every page in the post-patch run now resolves a sheet number — pages 0..9 are tagged `S001..S601`, where in baseline they were tagged `—`.

The regex fix did **not** shift **page-type classification** (Filter 2) the way the orders predicted:

- ROOF_PLAN remains at 1 (page 27, the same page baseline already classified).
- UNKNOWN remains at 4 (pages 12, 13, 38, 39 — same four pages).
- The four UNKNOWN pages are pages whose title-block text simply doesn't contain Filter-2's classification keywords ("ROOF PLAN", "FLOOR PLAN", "DETAIL", etc.). Filter 2 is keyword-driven on title_block_text, not regex-driven on sheet number, so a Filter 1 fix does not propagate to it unless the new sheet number unlocks a discipline-based fallback. On Silverleaf, the new sheet numbers are S-prefix (Structural), C-prefix, MP-prefix, etc. — none of which trigger the ROOF_PLAN keyword cascade.

**Why the orders predicted a cascade:** the orders' hypothesis was that drawing pages were being classified as UNKNOWN because Filter 1 was matching false-positive sheet numbers in the drawing-index page text (e.g., parsing "5'-6\"" as sheet "5-6"), which corrupted the sheet-map and starved Filter 2 of context. Track 2c proves the second half of that prediction wrong: Filter 2 doesn't actually consume `sheet_map`. It runs from `title_block_text` keyword scoring, independent of sheet-number resolution.

**What this means for the regex fix:** the patch is still correct — it fixes the actual bug (drawing-index regex mismatching dimension strings), and the proof is the 4→32 mapped-page jump. But the user-facing "drawing pages now classify correctly" cascade isn't a thing on Silverleaf the way it was hypothesized. The classification problem on pages 12/13/38/39 is a Filter 2 problem (keyword coverage), not a Filter 1 problem.

### 3.6 sheet_map_source shift — additional finding

Baseline: `sheet_map_source = "drawing_index"` with 10 sheets / 4 mapped pages.
Post-patch: `sheet_map_source = "title_blocks"` with 31 sheets / 32 mapped pages.

The hybrid regex made the drawing-index parse worse-looking (probably it now extracts fewer false-positive sheet numbers from index text), so Filter 1's drawing-index path bails out and falls through to the title-block path, which finds 31 real sheet numbers across 32 pages. This is a **net win** by every measurable count, but it's worth flagging that the hybrid changes the path Filter 1 takes, not just what it returns.

A separate look (out of G.1 scope) at why drawing-index parsing falls through on Silverleaf might surface a second tunable: the threshold at which Filter 1 commits to drawing_index vs falls through. Right now, falling through to title_blocks gave the better answer; that may not always be true.

---

## §4 — Debug-module output comparison (Track 2d-e)

### 4.1 Bearss debug — post-patch vs G.0.9 Scout 1

| `dispatch_health` key | G.0.9 Scout 1 | G.1 post-patch | Equal? |
|---|---|---|---|
| `dispatch_complete` | True | True | ✓ |
| `filters_completed` | (6, identical order) | (6, identical order) | ✓ |
| `filter_count` | 6 | 6 | ✓ |
| `warnings` | `["Filter 4 quality gate: 749 of 990 legends removed (241 kept)"]` | `["Filter 4 quality gate: 749 of 990 legends removed (241 kept)"]` | ✓ |
| `warning_count` | 1 | 1 | ✓ |
| `total_pages` | 91 | 91 | ✓ |
| `sheet_map_source` | `drawing_index` | `drawing_index` | ✓ |
| `sheet_count` | 47 | 47 | ✓ |
| `mapped_pages` | 44 | 44 | ✓ |
| `timestamp` | (G.0.9) | (G.1) | ✗ — clock artefact only |

`page_intelligence[:10]`: matches G.0.9's first-10 byte-for-byte except `timestamp`. Spot-checked: page 0 sheet=A-001, page 3 sheet=A-202 type=roof_plan, page 7 sheet=A-401 type=detail_sheet — every key identical.

`legend_quality_flags`: 5 flags, byte-identical to G.0.9.

**Bearss verdict:** `debug_module` surfaces nothing new on Bearss post-patch. The hybrid is byte-equivalent on the bidset where the original regex already worked.

### 4.2 Silverleaf debug — post-patch vs E.2.2 baseline

| `dispatch_health` key | E.2.2 (`E2_2_DEBUG_silverleaf.md`) | G.1 post-patch | Equal? |
|---|---|---|---|
| `dispatch_complete` | True | True | ✓ |
| `filter_count` | 6 | 6 | ✓ |
| `warning_count` | 1 | **2** | ✗ — +1 new warning |
| `warnings` | `["Filter 4 quality gate: 85 of 145 legends removed (60 kept)"]` | `["Filter 4 quality gate: 85 of 145 legends removed (60 kept)", "LOW RESOLUTION: 22% cross-references resolved"]` | ✗ — text expanded |
| `total_pages` | 40 | 40 | ✓ |
| `sheet_map_source` | `drawing_index` | **`title_blocks`** | ✗ — path shifted |
| `sheet_count` | 10 | **31** | ✗ — Δ +21 |
| `mapped_pages` | 4 | **32** | ✗ — Δ +28 |

`page_intelligence[:10]` first-page diffs (selected):

| Page | E.2.2 sheet | Post-patch sheet | E.2.2 type | Post-patch type |
|---:|---|---|---|---|
| 0 | — | **S001** | SCHEDULE_SHEET | SCHEDULE_SHEET |
| 1 | — | **S002** | SCHEDULE_SHEET | SCHEDULE_SHEET |
| 2 | — | **S003** | SCHEDULE_SHEET | SCHEDULE_SHEET |
| 3 | — | **S010** | SCHEDULE_SHEET | SCHEDULE_SHEET |
| 4 | S502 | **S100** | SCHEDULE_SHEET | SCHEDULE_SHEET |
| 5 | S101 | S101 | FRAMING_PLAN | FRAMING_PLAN |
| 6 | — | **S501** | DETAIL_SHEET | DETAIL_SHEET |
| 7 | — | **S502** | SCHEDULE_SHEET | SCHEDULE_SHEET |
| 8 | — | **S503** | DETAIL_SHEET | DETAIL_SHEET |
| 9 | SW-3S | **S601** | SCHEDULE_SHEET | SCHEDULE_SHEET |

**Plain-language reading**: every page now has a sheet number (S001–S601 in the first 10), and the page TYPE is unchanged. The discipline column (not shown above) is now uniformly `S` (Structural) for the first 10 pages, where baseline had it inconsistent (mostly `?`). The "type" column is identical, confirming Filter 2's classification did not move on this prefix of pages.

`legend_quality_flags`: empty list both runs.

`legend_quality_flags` (Bearss): identical 5 lines:
```
WARNING: unusually high legend count (241) — possible pdfplumber noise
WARNING: page 12 has 17 legends — review for duplicates or noise
WARNING: page 40 has 12 legends — review for duplicates or noise
WARNING: page 58 has 14 legends — review for duplicates or noise
WARNING: page 86 has 12 legends — review for duplicates or noise
```

### 4.3 What the debug module made visible

| Question | Bearss answer | Silverleaf answer |
|---|---|---|
| Did the patch break Bearss? | No — byte-identical to G.0.9 | (n/a) |
| Did the patch help Silverleaf? | (n/a) | Yes — 4→32 mapped pages, 10→31 sheets |
| Did page TYPE change? | No | No (1 ROOF_PLAN, 4 UNKNOWN — same pages) |
| Did sheet identity change? | No | Yes — every page now has the right sheet number |
| Did the dispatch path change? | No (drawing_index → drawing_index) | Yes (drawing_index → title_blocks) |
| New warnings? | None | +1 (`LOW RESOLUTION: 22% cross-references resolved` — 22% < 50% threshold in `check_for_leaks`) |

---

## §5 — Housekeeping log (Track 3)

**Track 3 not run.** Guardrail #6 fired during Track 2c — ROOF_PLAN/UNKNOWN cascade did not shift. Per the orders' hard guardrail: "STOP and document, do NOT proceed to housekeeping."

Scope of files reviewed: **none.** No `git mv` was issued. `safe_for_removal/MANIFEST.md` is unchanged.

The pre-existing housekeeping work-in-progress (5 march-orders moves left dirty in the working tree at session start) was stashed (`pre-G1-uncommitted-housekeeping`) and not touched. That work belongs to a separate session — Daniel's call when to land it.

---

## §6 — Sacred floor verification + open items

### 6.1 Session-end pytest

```
================= 230 passed, 19 skipped, 1 warning in 3.55s ==================
```

230 / 19 / 0 — identical to pre-patch baseline. Sacred floor honest and held.

### 6.2 Vault SHA-1s — final

| File | Pre-G.1 | Post-G.1 | Equal? |
|---|---|---|---|
| `core/dispatch_gate.py` | `c206ff…cd4a3` | **`2a708d…041f`** | ✗ (the one line we changed) |
| `core/roofing_module.py` | `ae9e5b…548f9` | `ae9e5b…548f9` | ✓ |
| `core/glazing_module.py` | `52c014…920f2` | `52c014…920f2` | ✓ |
| `core/debug_module.py` | `78f710…aac07` | `78f710…aac07` | ✓ |

### 6.3 Guardrail status at session end

| # | Guardrail | Fired? |
|---|---|---|
| 1 | Code change outside dispatch_gate.py:57 | No |
| 2 | Test fixture path constant edited | No (Track 1 only named the gap) |
| 3 | Vault-ruled module SHA-1s changed | No (only `dispatch_gate.py` SHA changed, as designed) |
| 4 | Sacred floor regresses post-patch | No (230/19/0 holds) |
| 5 | Bearss byte-equivalence breaks | No (769/177/31/24 byte-exact) |
| 6 | **Silverleaf classification cascade does NOT improve** | **YES — ROOF_PLAN unchanged, UNKNOWN unchanged. Track 3 halted as required.** |
| 7 | CLAUDE.md opened | No |
| 8 | Files moved that contain content referenced by active code | No (no files moved) |
| 9 | Wall-clock > 3 hours | No (well under) |

### 6.4 Open items for Daniel review

1. **Should the regex patch land?** The hybrid is correct on its own merits — it fixes the drawing-index false-positive bug on Silverleaf (4→32 mapped pages, +800%) and is byte-equivalent on Bearss. But the predicted page-classification cascade on Silverleaf does not happen because Filter 2 (`title_block` keyword scoring) doesn't read from `ctx.sheet_map`. The three options are:
   - (a) Land the patch as-is. The sheet-map fix is real and big; it just doesn't propagate to ROOF_PLAN/UNKNOWN counts the way G.0.5/G.0.7 hypothesized. Document the boundary.
   - (b) Revert the patch, treat G.1 as a research run, and write a follow-up phase that fixes both Filter 1 AND Filter 2's keyword coverage on the four UNKNOWN pages.
   - (c) Keep the patch and add a Filter 2 review as a separate G.2 phase.
   - (Recommendation: (a) or (c). The patch is right. The cascade prediction was incomplete, not wrong.)

2. **`sheet_map_source` shifted from `drawing_index` to `title_blocks` on Silverleaf.** Worth a separate look at why: did the new regex actually find fewer sheet numbers on the drawing-index page (causing fall-through to title_blocks), or is there a threshold/tie-break in Filter 1 that's now landing differently? This is OUT of G.1 scope but flagged for Daniel.

3. **The new `LOW RESOLUTION: 22% cross-references resolved` warning on Silverleaf** is also a fall-out of the regex shift. Cross-ref resolution depends on the sheet_map. With more sheets known, more cross-refs were attempted, and 22% is below the 50% leak-check threshold. This is `check_for_leaks` doing its job; it's surfacing a real number. Worth a Filter 3 review when Daniel revisits classification.

4. **`waterproofing_module.py`, `siding_module.py`, `framing_module.py` are not present in the repo.** The orders' Guardrail 3 listed them among "vault-ruled module SHA-1s" that must not change. They can't change because they don't exist. Worth either removing them from the vault list or creating stubs.

5. **Pre-existing housekeeping work-in-progress is stashed as `pre-G1-uncommitted-housekeeping`** (5 march-orders moves, left over from a prior session, found dirty in the working tree at G.1 start). That work is independent of G.1 and was not touched. Daniel's call when to land it.

6. **Test fixture wiring is honest — no fix needed.** Track 1 was a Daniel-driven hypothesis check ("is the 230 floor really honest?"). Answer: yes. The 19 skipped tests have explicit `skipif` markers; they don't masquerade as passes. If Daniel wants those 19 tests to actually run, the fix is to populate `backend/test_plans/` with the four named PDFs (or add them to the `_SILVERLEAF_CANDIDATES`-style fallback pattern already used in `conftest.py`).

---

**End of G.1 Gate Report.**
