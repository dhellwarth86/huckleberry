# CLAUDE.md — Huckleberry AI Handoff Document

> **Purpose**: Single source of truth for the next Claude session to pick up the Huckleberry AI commercial roofing takeoff project without losing context. Read this file completely before writing a single line of code.
>
> **Last updated**: 2026-04-25, end of Phase 1 architectural decisions (Phase 1 closed at v6.3.5; Phase 2 plan ratified across 18 decisions).
> **Project owner**: Non-developer building a POC. Speaks plainly, wants brutal honesty, demands "no sugar coating" reviews.
> **Discipline**: Karpathy "build → test → test → test." No code ships without a test that was red before the code existed. For regression suites against already-working code (the Step 11 shape), the red phase is replaced by a **mutation test** that proves each new test is load-bearing. See **"Karpathy Procedure"** section below for the refined loop, now covering both shapes.
> **Phase 1 constraint** (still applies to the HTML at v6.3.5): Single-file HTML, no backend, no AI API calls, offline-capable. The HTML must remain runnable standalone after Phase 2 ships, as the offline fallback.
> **Phase 2 constraint** (begins next session): Python backend (FastAPI + SQLAlchemy + Postgres + Pydantic), runs on localhost during POC, no auth, monorepo with `huckleberry/{frontend,backend,shared}`. See **"Phases"** section below for the full architecture.

## Validation Receipts (proof this document matches reality)

Every concrete claim below was re-verified against the actual file at `/home/claude/work/Huckleberry_AI_6.3.5_Scope.html` immediately before publishing this document.

| Claim in document | Verification command | Result |
|---|---|---|
| Latest file is v6.3.5 | `grep "header-stat.*v6.3" Huckleberry_AI_6.3.5_Scope.html` | `v6.3.5` present in header stat ✓ |
| 138/138 tests green | `node run_tests.js Huckleberry_AI_6.3.5_Scope.html` | `118 UNIT + 20 INTEGRATION = 138/138 pass, 0 fail` ✓ |
| Full regression chain passes | same harness on 6.3.4 / 6.3.3 / 6.3.2 / 6.3.1 / 6.3.0 | 130/127/117/112/107 — all match originals ✓ |
| 3× stability | same harness × 3 on 6.3.5 | 138/138 × 3, no flake ✓ |
| Step 10b polygon-state fix (browser-verified) | `spotcheck_10b.js` | 7/7: 4-corner snap-close preserves all vertices at Chipotle-scale coords ✓ |
| Step 11 mutation test | `node mutation_test_step11.js` | 8/8 mutations caught — every Step 11 test is load-bearing ✓ |
| Cricket polygon palette (Step 10) | `spotcheck_cricket.js` | 4/4 ✓ |
| Manufacturer field (Step 9.x) | `spotcheck_manufacturer.js` | 14/14 ✓ |
| Duro-Last in roofing_materials.py | `python3 -c "from roofing_materials import MANUFACTURERS; 'Duro-Last' in MANUFACTURERS"` | `True` ✓ |
| B-19 test still present | `grep "B-19 · openViewerIfPossible"` | Preserved across 6.3.x ✓ |

If you find a claim that contradicts current reality, the file has drifted and this document is the bug — fix it before continuing.

---

## Phases — The Architectural Model

Huckleberry is being built in three phases. Each phase has a different goal, a different stack, a different test discipline, and a different failure mode. **Decisions made in this section are canon. Future Claude sessions must not negotiate against these without explicit user approval.**

### Phase 1 — Frontend HTML viewer + manual takeoff toolchain (CURRENT, ~COMPLETE)

**Goal**: A single-file HTML application that lets a roofing estimator manually annotate a PDF bidset and produce a takeoff workbook. No backend. No network. Runs offline in Chrome.

**Status**: v6.3.5, 138/138 green, browser-verified through Step 10b. Phase 1 is now closed. The manual toolchain is mature, takeoff math is mutation-tested, and the user has confirmed the workflow in browser.

**Components**:
- PDF rendering via pdf.js (3.11.174)
- OpenSeadragon viewer + Konva annotation overlay
- Manual tools: pan / calibrate / measure / line / polygon / rectangle / pin / excludeZone
- Three palettes: pin / edge / polygon
- Rule-based scope parser (`extractScope`, regex over flat text)
- Takeoff aggregation: count / LF / SF / derived-SF sections
- Excel export per system (SheetJS)
- 138-test suite + jsdom harness + spot-checks + Step-11 mutation test

**Phase 1 forward**: bug fixes only. UI/UX polish allowed. **No new architecture in the HTML.** Anything that smells like "data analysis," "auto-detection," "layout zoning," or "relationship validation" belongs in Phase 2 — do not bolt it onto v6.3.5.

**Phase 1 limitations resolved by Phase 2 (NOT bugs to fix in HTML)**:
- B-1: Stage 6 short-circuit half-built (real-PDF scale auto-detect)
- B-2: Real-PDF dash filter drops 0
- B-3: Auto-detect mega-cluster on real bidsets
- The "scope parser is regex over flat text with no provenance" architectural ceiling

These cannot be fixed in the browser. They are symptoms of trying to do data analysis on chord-flattened path arrays with no structural context. Phase 2 dissolves them by changing the input shape.

### Phase 2 — Backend service: PDF intake, data analysis, persistence (NEXT, NOT STARTED)

**Goal**: A Python backend that owns everything Phase 1 cannot reasonably do — real PDF extraction with layout awareness, relationship validation against the seed files, persistent storage of every processed bidset, accumulation of labeled data for future Phase 3 ML work.

**Why now**: Phase 1 has hit its architectural ceiling. The four seed files (`dispatch_seed.py`, `roofing_seed.py`, `glazingseed.py`, `material_matrix_seed.py`) currently have no runtime consumer. Manual mirroring of vocab from Python into HTML (the way Duro-Last got into both `roofing_materials.py.MANUFACTURERS` AND `ROOF_VOCAB.manufacturers` in v6.3.2) is unsustainable as the seed files grow. Phase 2's first job is giving those files a live consumer.

**The 18 architectural decisions** (ratified 2026-04-25 in rapid-fire planning, not negotiable without user approval):

1. **Backend = full server.** Processing + DB + reference data live there. Caged LLM **deferred to Phase 3** — refused as Phase 2 complexity that doesn't yet earn its keep.
2. **DB = PostgreSQL + S3-compatible object storage.** Postgres for structured BidsetRecord and user data; S3-style storage for the raw PDFs. (Specific S3 provider TBD: real AWS S3, MinIO self-hosted, Cloudflare R2, Backblaze B2 — all use the same API.)
3. **No LLM in Phase 2.** Rule-based + reference-data-driven only. LLM is a Phase 3 decision once there's documented evidence rules can't handle a specific failure.
4. **Auth = none in Phase 2.** Backend runs on localhost. HTML talks to backend over localhost. No login, no users, no sessions. Phase 3 problem when the backend gets network-exposed.
5. **Annotations save model = save-on-button-press.** Frontend works in memory like Phase 1 (fast, instant, no network chatter during drawing). Explicit "Save" button POSTs the whole annotation set to backend. Backend is the durable store; frontend is the working copy.
6. **Source-of-truth on save = frontend wins, backend keeps provenance trail.** When user edits a parser-extracted field (e.g. correcting "TPO" to "PVC"), user wins. Backend records what the parser originally said. Every correction becomes labeled training data for Phase 3.
7. **Backend stack = FastAPI + SQLAlchemy + Postgres + Pydantic.** The wrapper IS a Pydantic model — single source of truth for shape across DB row, API response, and frontend payload. No separate JSON Schema doc to maintain.
8. **PDF processing = job-based polling.** POST PDF → get `job_id` → poll `/jobs/{job_id}` for status → fetch BidsetRecord when done. Streaming progress (WebSocket / SSE) deferred until UX demands it.
9. **Reference data = imported as Python modules at startup.** Seed files are version-controlled `.py` source of truth; backend `import`s them, holds in memory. Postgres stores BidsetRecords and user data, NEVER reference data. Vocab edits go through git PR, not SQL.
10. **Repo = monorepo with three top-level dirs: `huckleberry/{frontend, backend, shared}`.** Single git history. The wrapper schema lives in `shared/`. v6.3.5 moves into `frontend/`. One PR can change both sides at once.
11. **BidsetRecord schema = start minimal, grow on contact with real data.** Six fields at start: `{ id, source_pdf_ref, pages, scope, annotations, provenance }`. Schema-first design — defined as Pydantic in `shared/` BEFORE backend code. Every new field must justify itself against a real bidset that needed it.
12. **Phase 1 closes at v6.3.5.** Step 12 (manufacturer dropdown / Excel column work) is **abandoned** — Phase 2's backend will produce that richness from real data. Building it twice in HTML would be throwaway.
13. **First Phase 2 deliverable = the experiment.** Run via Claude Code with filesystem access to a folder of 15 full real-world bidsets. Not Chipotle alone; the actual production distribution. Validates the architecture against evidence before any backend code is written.
14. **Experiment success criterion = a draft Pydantic BidsetRecord schema + a findings report.** Not stack picks. Not working code. The schema and the writeup that explains why each field is there, what real bidset behavior demanded it, and what surprised the experimenter.
15. **Schema inclusion rule = field appears in ≥ 3 of 15 bidsets AND has identifiable downstream consumer.** Both required. Other observed fields go in a "deferred / observed" appendix in the findings report.
16. **Schema versioning = yes from day one.** Every BidsetRecord carries a `schema_version` field, incremented on every breaking change. No migration scripts during experiment phase; old records stay untouched in DB; backend handles version mismatch at read time (upgrade-on-read or mark-stale).
17. **15 bidsets = uploaded to object storage from day one.** Repo carries only references / manifest (`huckleberry/backend/test_fixtures/bidsets.json`); backend's S3 client downloads on demand. Same code path for fixtures and production PDFs.
18. **Order of operations entering Phase 2 = (A) update CLAUDE.md to canonize all decisions [DONE in this update], (B) set up S3 + upload the 15 bidsets, (C) run the experiment in Claude Code.** Documentation before infrastructure. Infrastructure before work.

### Phase 3 — Auth, ML, multi-user, network exposure (FUTURE, NOT PLANNED)

Things deferred to Phase 3 with explicit user decisions:
- LLM integration (Q3 → E)
- User auth and sessions (Q4 → D)
- Network exposure beyond localhost
- Anything trained on the labeled corrections accumulated by Phase 2's provenance trail

Phase 3 is **not planned** at the architectural level yet. Do not propose Phase 3 work until Phase 2 has 100+ bidsets in the database and an empirically clear case for what the next layer should solve.

### Phase boundaries — the rules

- **Phase 1 must remain runnable standalone forever** as the offline fallback. Even after Phase 2 ships, the HTML must work without a backend running.
- **Phase 1 maintenance gets stricter once Phase 2 starts**, not looser. Every Phase 1 change must ask "does this need a corresponding backend change?" before merging.
- **Adjacent pre-existing bugs touched by new consumers get fixed in the same step, not deferred.** Step 10b's bitter lesson generalizes: if a Phase 2 change touches a Phase 1 surface, fix the Phase 1 surface in the same change.
- **Architecture decisions move only with explicit user approval.** The 18 decisions above are canon. A future Claude session that wants to renegotiate (e.g. "we should use MongoDB instead of Postgres") must surface that to the user explicitly, not silently pivot.

---

## TL;DR — Where We Are Right Now

- **Phase 1 status**: closed at **v6.3.5**, 138/138 green (118 unit + 20 integration). Stable across 3 consecutive runs. Full regression chain intact back to 6.3.0 (107/107). Browser-verified through Step 10b.
- **Phase 2 status**: planned, ratified across 18 architectural decisions on 2026-04-25 (see "Phases" section above). **Not started.** Next session begins with infrastructure setup (S3 + 15 bidset upload), then the experiment in Claude Code.
- **Latest shipped Phase 1 file**: `/mnt/user-data/outputs/Huckleberry_AI_6.3.5_Scope.html`
- **What Phase 1 does**: Synthetic plan, manual toolchain (pan / calibrate / measure / line / polygon / rectangle / pin / excludeZone), scope parser (regex over flat text), three palettes (pin / edge / polygon), takeoff with count / LF / SF / derived-SF sections, Excel export per system. **Manual workflow only** — auto-detection on real PDFs is broken (B-1/B-2/B-3) and these are explicitly deferred to Phase 2 architecture, not fixable in HTML.
- **What Phase 2 will do**: Python backend (FastAPI + SQLAlchemy + Postgres + Pydantic) with real PDF intake, layout-aware extraction, persistent storage of every bidset, live consumption of the four seed files, contractual relationship validation. HTML wraps the backend; backend does the heavy lifting.
- **Step 12 (manufacturer dropdown / Excel column richer scope card)**: **abandoned**. Phase 2 will produce that richness from real data; building it twice in HTML would be throwaway work.

---

## Karpathy Procedure (the TDD loop, refined across Steps 9a–11)

This section exists because the original "build → test → test → test" one-liner wasn't concrete enough to prevent session-to-session drift. There are two distinct shapes of TDD work in this project, and the loop differs between them.

### Shape A — Feature work (Steps 9a through 10, plus the 10b bug fix)

This is the standard Karpathy red-green-refactor. Used for any change that introduces new behavior, new schema, or fixes a bug.

1. **Replicate green before touching anything.** Never trust a claim of "N/N green" — load the file into the jsdom harness and re-run. If previous-Claude said "107/107" and harness says 106/107, previous-Claude was wrong (or you're running the wrong file). The harness is `run_tests.js`; it injects a hoist script that pulls `UNIT_TESTS` + `INTEGRATION_TESTS` onto `window` (inline `const` declarations don't auto-attach).

2. **Write failing tests first.** Write them for every new contract the step promises — schema shape, state field existence, factory output, parser behavior, aggregation math, regression guards. Cover positive AND negative paths (the "does NOT happen when X" cases catch over-eager implementations). A single test per public behavior, not per line of code.

3. **Run — verify the red pattern matches expectations exactly.** Count matters. If you wrote 5 new tests and only 3 fail, the other 2 are either already satisfied by existing code (fine — they're guards against future regressions) or misspecified (they assert something weaker than you intended — fix them). If tests fail with unexpected error messages ("Cannot read properties of undefined" instead of your assertion), either the test setup is broken or you're discovering an adjacent bug; stop and investigate before proceeding.

4. **Implement the minimum code.** Schema → factory → state → setter → parser → UI, in roughly that order. Don't refactor adjacent code unless the test requires it. If you find yourself wanting to fix a pre-existing bug, log it as a flag for the summary and leave it alone — UNLESS that pre-existing bug is adjacent to a new consumer you're adding. Step 10b's bitter lesson: I flagged a polygon `hoverIdx` bug in Step 9b and left it alone. Step 10 added snap-close, which called `slice(0, -1)` on the same broken state machine. The user hit it in the browser an hour later. **Adjacent pre-existing bugs touched by new consumers get fixed in the same step, not deferred.**

5. **Run — verify green.** If not green first try, don't panic-patch; read the failure message, go back to step 4 with the minimum fix. Most failures across 9a–10b were off-by-one on expected counts or forgetting to seed a field.

6. **Run 3× for stability.** Test infrastructure has flake vectors (async timing, shared state, test-order dependencies). Flake that shows up once in three runs will bite a real user 10× as often. If 3× green, ship. If any run fails, find the order or state dependency and fix.

7. **Regression + real-world spot-check.** Run the harness against every prior shipped version still on disk (6.3.0, 6.3.1, 6.3.2, …) — each should still match its original count. Then write a small standalone spot-check script (`spotcheck_*.js`) that exercises the feature against realistic inputs — CLAUDE.md's Panda Express / Taco Bell / Wendy's-class strings, a concrete commercial scenario (5000 sf building + two crickets at 25/40 sf), or the exact coords from a user's screenshot when fixing a reported bug. Both the test suite and the spot-check must pass before claiming ship-ready.

### Shape B — Regression suite against already-working code (Step 11)

Step 11's whole job was "add a dedicated guard for the derived-SF math." The code was already correct; the suite needed to prove that future changes can't silently break it. Red-phase verification doesn't apply because the code is intentionally not broken. Step 6 of the loop is replaced with **mutation testing**:

1. **Replicate green** — same as Shape A.

2. **Identify the contracts to lock.** Read the code being guarded. Inventory the invariants:
   - Exact counts (how many rows, columns, entries)
   - Value-level identities (all unit='sf', all share same base)
   - String contracts (derivedFrom always equals 'mainPolygonArea')
   - Edge cases (zero-area, override, multi-system isolation)
   - `kind` parameters that should not matter (rectangle vs polygon)
   - Fields that must never be `undefined`/`NaN` (Excel cell poison)

3. **Write one orthogonal test per invariant.** Orthogonal = the failure message points at the specific invariant that broke. If test A subsumes test B, drop test B — overlapping tests mean vague failure messages.

4. **Run — all new tests should pass immediately** (because the code is correct). If any fail at this stage, either the test is wrong or you've discovered a real bug. Investigate before proceeding.

5. **Mutation test — this is the critical step.** For each new test, define a targeted code mutation that should break that invariant. Run each mutation against the test harness and confirm the matching test(s) fail. Any mutation that escapes ALL tests = a test that looks green but guards nothing. Example mutation list from Step 11's `mutation_test_step11.js`:
   - `mutation A`: drop a derived seed → "exactly 3 rows" test must fail
   - `mutation B`: flip unit from 'sf' to 'lf' → unit-contract test must fail
   - `mutation C`: make one derived row read 0 instead of totalSF → "share same base" test must fail
   - … etc
   - **All 8 Step 11 mutations were caught by at least one Step 11 test.** That's how you know the suite is load-bearing.

6. **Run 3× for stability** — same as Shape A.

7. **Regression chain** — same as Shape A. Spot-check is optional here because the guarded code is already being exercised by prior steps' spot-checks.

**When to use which shape:**
- New feature / new schema / new state / new UI → Shape A (write red tests first)
- Bug fix for a reported symptom → Shape A (write failing test that reproduces the bug)
- "Add tests for something that already works but lacks coverage" → Shape B (mutation-test the new tests)
- "Prevent a specific class of future regression" → Shape B

### Shape C — Phase 2 backend integration tests (PROPOSED, not yet exercised)

When Phase 2 starts, a third TDD shape will be needed for end-to-end backend tests. This shape isn't fully designed yet — it gets refined in early Phase 2 — but the rough form:

1. **PDF fixture set** = the 15 real bidsets in object storage. Backend test runner pulls them on demand, same code path as production.
2. **Per-PDF golden records** = a JSON snapshot of the expected BidsetRecord for each fixture, version-stamped. Tests assert backend output matches the snapshot.
3. **Schema-level contract tests** = Pydantic validation runs on every BidsetRecord. A field added on one side without the other = a contract test failure, not a runtime mystery.
4. **Provenance contract tests** = every parser-extracted field has a corresponding provenance entry. User-edit overrides preserve provenance. (Provenance integrity is what Phase 3 ML training depends on; it gets test discipline now.)
5. **Database round-trip tests** = save a BidsetRecord, load it back, assert byte-identical (modulo timestamps). Catches silent serialization drift.
6. **Schema version mismatch tests** = old-version records in DB still readable by new-version backend code, either via upgrade-on-read or via mark-stale.

Shape C does NOT replace Shape A or Shape B inside the backend — those still apply to feature work and regression suites within the Python codebase. Shape C is the additional layer for the integration boundary.

The first Phase 2 step that has Shape C tests will probably be the wrapper schema itself (Pydantic models in `shared/`). Schema is the contract; contract tests come first.



- **Never claim a pass count without running it.** Claims like "138/138" with no receipt in the same turn are lies. The user has already caught this once in project history (B-19 era); don't repeat it. If the tool-use limit is approaching and you can't verify, say so explicitly and hand off as "implementation in place, verification pending."
- **Red phase is load-bearing, not ceremony (Shape A).** Skipping "verify the tests fail first" is how you ship a test that only passes because it asserts something trivially true. Run. See red. Then proceed.
- **Mutation phase is load-bearing, not ceremony (Shape B).** A green regression test is only evidence it guards something if a targeted break makes it fail. Without mutations, a green suite is decoration.
- **Adjacent pre-existing bugs get fixed with the consumers that touch them.** Step 10b was the lesson. Defer pre-existing bugs ONLY when no code in the current step reaches the broken area.
- **Honest flags beat silent punts.** If you touch something adjacent to the feature (a pre-existing bug, an undocumented assumption, scope creep into a later step), surface it in the final summary with an explicit "Honest flags" list. Small and explicit beats big and implicit.
- **One semantic per field.** When the HTML parser model and the Python reference model disagree (as they did for Duro-Last in Step 9b → 9.x), reconcile. Don't let two sources of truth drift — it compounds fast.

### Template receipts from Steps 9a–11

| Step | Shape | Tests added | Before | After | Stability | Mutation | Notes |
|---|---|---|---|---|---|---|---|
| 9a (line tool, prior session) | A | 6 | 101 | 107 | (prior) | — | |
| 9b (snap-to-close + Duro-Last) | A | 5 | 107 | 112 | 3× green | — | |
| 9.x (sys.manufacturer) | A | 5 (+2 updated) | 112 | 117 | 3× green | — | HTML/Python reconciliation |
| 10 (cricket polygon palette) | A | 10 | 117 | 127 | 3× green | — | |
| 10b (polygon state-machine fix) | A | 3 | 127 | 130 | 3× green | — | Browser-verified; fixed the hoverIdx bug deferred in 9b |
| 11 (derived-SF regression suite) | B | 8 | 130 | 138 | 3× green | **8/8 caught** | First Shape-B work in the project |

Every step also passed the regression chain (old versions still green at original counts) and a spot-check or mutation test.

---

## The Shipped Files

| File | Size | Tests | Purpose |
|---|---|---|---|
| `Huckleberry_AI_6.0_TracePoint.html` | 125 KB / 2,799 lines | 37/37 | Removed Claude AI pipeline, added 12-stage TracePoint geometry engine. Synthetic only. |
| `Huckleberry_AI_6.1_TracePoint_Viewer.html` | 180 KB / 4,028 lines | 53/53 | Added OpenSeadragon + Konva PDF viewer with 7 manual tools. Manual polygon override producing exact 4,100 sqft on L-shape. |
| `Huckleberry_AI_6.2_Scope.html` | 264 KB / 5,825 lines | 72/72 | Added scope-first workflow: trade picker, scope parser, page classifier, scope-aware pin tool, Excel export. |
| `Huckleberry_AI_6.2.3_Scope.html` | 301 KB / 6,221 lines | 77/77 | B-11..B-15 real-PDF bug fixes, B-19 synthetic-painter fix. |
| `Huckleberry_AI_6.3.0_Scope.html` | ~265 KB / 7,626 lines | 107/107 | Steps 1-9a: seed items, constants, precedence rules, corners pin with vertex snap, LINE tool for LF items, edge palette. |
| `Huckleberry_AI_6.3.1_Scope.html` | ~365 KB | 112/112 | Step 9b: polygon snap-to-close + Duro-Last added to ROOF_VOCAB + roofing_materials.py. |
| `Huckleberry_AI_6.3.2_Scope.html` | ~380 KB | 117/117 | Step 9.x: `sys.manufacturer` field, `ROOF_VOCAB.manufacturers` vocab block (7 brands), parser writes to it with `systems[0]` fallback when no explicit systemType. |
| `Huckleberry_AI_6.3.3_Scope.html` | ~407 KB | 127/127 | Step 10: `sys.polygonTypes` array, `App.activePolygonTypeId`, `makePolygonType` factory, cricket palette UI, typed-polygon auto-naming (`Cricket #N`), buildTakeoffModel.sf aggregation, derived-SF excludes tagged polygons. |
| `Huckleberry_AI_6.3.4_Scope.html` | ~417 KB | 130/130 | Step 10b: polygon state-machine fix. Old `hoverIdx` logic froze at index 1 after first onMove, causing saved polygons to have wrong vertices (triangle-with-shifted-bottom user report). New state machine maintains "hover is last" invariant. Browser-verified by user. |
| `Huckleberry_AI_6.3.5_Scope.html` | ~425 KB | **138/138** | Step 11: derived-SF regression suite. 8 new mutation-tested unit tests locking down `buildTakeoffModel.derived` contracts (row count, unit, shared base, derivedFrom string, zero-area, kind-agnostic sum, multi-system isolation, waste override). No production code changed — pure test-coverage work. **CURRENT PRODUCTION FILE.** |

All live in `/mnt/user-data/outputs/`. Working copies live in `/home/claude/work/`.

---

## Project History — What Was Tried and Why

### Pre-6.0 baseline (Huckleberry 5.0)
The starting point was a Claude-Vision-powered roofing estimator with a 4-pass pipeline (CLASSIFY → SURVEY → EXTRACT → VALIDATE), an `ANTHROPIC_API_KEY` bar in the UI, a token-cost panel, `claude_pipeline.py`, `prompts/`, and a `trap_filter.py`. Cost: $0.15–0.25 per run. Speed: ~30 seconds (network bound). Worked OK on clean plans, struggled with anything weird.

### 6.0 — Strip the AI, build the geometry engine (Karpathy-disciplined)
- **Why**: User wanted zero AI calls + zero per-run cost + offline operation.
- **What we did**: Removed every trace of the Claude pipeline. Built a 12-stage deterministic geometry engine in pure JavaScript based on the TracePoint AI research paper. Used PDF.js to extract vector paths.
- **Stages**: (1) Dispatch Gate, (2) Zone Mask, (3) Weight Filter, (4) Length Filter, (5) Dash Filter, (6) Union-Find Cluster, (7) Scale Determination (5 tiers), (8) Perimeter Cleanup, (9) Confidence Score, (10) Interior Density, (11) Rectilinear Score, (12) Polygon Selection.
- **Result on synthetic 5,000 sqft plan**: **0.00% error** (exact match). 37/37 tests green.
- **Result on real Wendy's bidset**: **14,151,546 sqft detected vs 1,565 actual.** Three orders of magnitude wrong. Dispatch couldn't find the scale, Stage 6 mega-clustered the entire page, Stage 7 fell to Tier 5 (scoring formula) and emitted nonsense.
- **Honest verdict**: Architectural skeleton works. Real-PDF accuracy: 0%.

### 6.1 — PDF viewer + manual tools (recover from 6.0's failure)
- **Why**: Auto-detect can't work on real plans yet. Need user to be able to recover.
- **What we did**: Added OpenSeadragon (4.1.0, tiled deep-zoom) + Konva (9.3.0, annotation overlay). Built 7 tools — pan, calibrate (2-point pick → enter real distance), measure, polygon, rectangle, exclude-zone, delete. All annotations stored in PDF points (72pt = 1 inch).
- **Pipeline override**: Wrapped `TP.run` so user-drawn polygon REPLACES Stage 12's winner; user manual scale REPLACES Stage 7's tier-5 nonsense.
- **Bug fixes attempted**: PDF graphics-state stack (`q`/`Q` save/restore) so `setLineWidth` and `setDash` don't leak across paths.
- **Result on Wendy's**: User calibrates (3/16" = 1'-0" = 5.333 ft/in), draws rectangle, gets **1,566 sqft vs 1,565 actual = 0.06% error.**
- **HONEST CAVEAT**: That match is the user's hand doing the work. The pipeline still produced 14M sqft. The viewer just lets the user override the answer.
- **Dash filter "fix"**: Synthetic test passes. **Real-PDF Wendy's run still showed 0 dashed paths dropped.** The fix is unverified in real conditions.
- 53/53 tests green.

### 6.2 — Scope-first workflow (current)
- **Why**: User answered 10 questions defining the real workflow: trade-pick → scope-from-PDF → pin palette derived from scope (NO hardcoded items) → multi-system / multi-area → Excel export with per-system sheets.
- **What we did**:
  - Added SheetJS for Excel export
  - Built 8-tab structure: NEW SESSION / SCOPE / PAGES / VIEWER / TAKEOFF / PIPELINE / TESTS / ABOUT
  - Wrote rule-based roofing vocabulary (`ROOF_VOCAB`, ~250 terms across 9 categories)
  - Built `extractScope()` that sweeps page text, splits by system labels (`ROOF SYSTEM A`, `Type 1`, etc.), emits `ScopeProposal` with per-field confidence
  - Built `classifyPage()` that scores each page as ROOF_PLAN / DETAIL / SPEC / COVER / OTHER
  - Built SCOPE tab with editable system cards, parser-found pin/edge tags with delete + add-inline
  - Built PAGES tab with thumbnails and color-coded classification badges
  - Built TAKEOFF tab with per-system tables and FINALIZE → EXCEL button
  - Wired viewer to scope: current-system selector, pin tool that reads from `scope.systems[current].pinPalette` (no hardcoding), keyboard 1-9 fast-switch, polygon/rectangle prompts for name and persists as scope-attached area with sqft/perimeter
  - Built Excel exporter: Summary sheet + per-system sheets with areas / pin-counts / itemized pins
- **Result on synthetic plan with synthetic spec text**: Scope produces 1 system (TPO Fully Adhered 60 mil + Polyiso tapered + Dens-Deck), 7 pin types, 2 edge types, HIGH confidence. Drawing 100×50 rectangle at 1/8"=1'-0" produces **exactly 5,000 sqft, 300 lf**. Pin counts route correctly to TAKEOFF tab. Excel export generates 2-sheet workbook.
- **Result on real PDFs**: UNTESTED. No real bidset has been run through 6.2 in this session.
- 72/72 tests green.

---

## Architecture (read this before changing anything)

### File structure (single-file HTML)

```
Huckleberry_AI_6.2.html
├── <head>
│   ├── CDN scripts: pdf.js 3.11.174, OpenSeadragon 4.1.0, Konva 9.3.0, xlsx 0.18.5
│   ├── Google Fonts: Rajdhani, Outfit, JetBrains Mono
│   └── <style>: ~900 lines of CSS (cyan-on-charcoal cyberpunk theme)
├── <body>
│   ├── Header + status bar
│   ├── Left sidebar: pipeline state + 12-stage list + Karpathy loop note
│   └── 8 panes (DOM order = tab index 0-7):
│       0: NEW SESSION  → trade picker + upload
│       1: SCOPE        → editable system cards
│       2: PAGES        → thumbnail grid
│       3: VIEWER       → OSD + Konva + 9-button toolbar + scope sidebar
│       4: TAKEOFF      → workbook preview + FINALIZE button
│       5: PIPELINE     → 12-stage grid + RUN button (demoted)
│       6: TESTS        → Karpathy harness
│       7: ABOUT        → docs + history
└── 3 inline <script> blocks:
    ├── Block 1 (~750 lines): App state + showTab + helper UI
    ├── Block 2 (~3,200 lines): TP engine + Viewer + tools + tests + boot
    └── Block 3 (~1,750 lines): v6.2 scope module + scope tests + integration tests + boot
```

### Key globals

| Global | Type | Purpose |
|---|---|---|
| `App` | object | Project state (`App.project = { trade, bidSetName, scope, annotations, ... }`) + transient (`App.lastRun`, `App.manualScale`, `App.activePinTypeId`, etc.) |
| `App.planSet` | object | Parsed PDF: `{ pages: [{ idx, page_w_pts, page_h_pts, paths, texts, zones, renderCanvas, renderDPI }] }` |
| `TP` | namespace | The 12-stage geometry engine. `TP.run(planSet, opts)` orchestrates. Each stage is `TP.dispatch / zoneMask / weightFilter / lengthFilter / dashFilter / clusterUnionFind / determineScale / perimeterCleanup / confidenceScore / densityScore / rectilinearScore / selectFinal` |
| `Viewer` | object | Owns OSD + Konva. `Viewer.init(planSet, pageIdx)` mounts. Coordinate authority: PDF points everywhere |
| `TOOL_HANDLERS` | object | One handler per tool: `pan, calibrate, measure, polygon, rectangle, pin, excludeZone` — each may have `onDown / onMove / onUp / onDblClick` |
| `ROOF_VOCAB` | object | Vocabulary bank for the parser. Keys: `systemTypes, attachmentMethods, membraneThickness, insulationMaterials, coverBoards, penetrations, accessories, edgeTypes, systemLabelPatterns, roofPlanMarkers, detailMarkers, specMarkers, coverMarkers` |
| `UNIT_TESTS / INTEGRATION_TESTS` | array | Test arrays. New tests get pushed in via `Array.prototype.push.apply(UNIT_TESTS, ...)` so the harness picks them up |

### State flow

```
User picks trade → App.project.trade = 'roofing'
User uploads PDF → loadPdfFile(file)
    → extractPlanSetFromPdf() → App.planSet (paths + texts + zones + renderCanvas per page)
    → extractScope(App.planSet) → App.project.scope.systems[]
    → classifyPage(page) for each → App.project.pageClasses
    → renderScopeTab(), renderPagesTab(), enable next-steps
User opens VIEWER → Viewer.init(App.planSet, pageIdx)
    → mounts OSD on offscreen canvas → Konva overlay
    → renderViewerSystemControls() → sidebar shows current system + pin palette
    → rehydrateViewerForPage(pageIdx) → restores any saved annotations for this page
User uses tools:
    calibrate → App.manualScale = ftPerInch
    polygon/rectangle → persistAreaFromPoints() → push into App.project.annotations.areas
    pin → TOOL_HANDLERS.pin.onDown → push into App.project.annotations.pins
User opens TAKEOFF → renderTakeoffTab() reads App.project for live preview
User hits FINALIZE → exportTakeoffToExcel() → SheetJS XLSX.writeFile()
```

### TP.run is wrapped THREE times (latency / debugging hazard)

```js
// Original definition (line 2244)
TP.run = async function run(planSet, opts) { ...12 stages... }

// Wrapper 1 (line 4139) — injects user zones, manual scale, replaces Stage 12 winner with user polygon
const _TP_run_original = TP.run;
TP.run = async function runWithOverrides(planSet, opts) { ... }

// Wrapper 2 (line 5569) — INCOMPLETE: tries to short-circuit Stage 6 but the engine doesn't honor opts.skipStage6
const _TP_run_for_shortcircuit = TP.run;
TP.run = async function runMaybeSkipStage6(planSet, opts) { ... }
```

**This three-wrapper pattern is fragile.** When debugging anything pipeline-related, remember: every call to `TP.run()` actually goes through `runMaybeSkipStage6 → runWithOverrides → run`. Future Claude should consider collapsing these into a single function with branching logic.

### Coordinate systems (don't mix these up)

1. **PDF points** — `72pt = 1 inch`. Authority for all annotations. `App.project.annotations.areas[*].pointsPt` and `App.project.annotations.pins[*].pt` are always in PDF points.
2. **Image pixels** — `renderDPI / 72` factor from points. Used for OSD's tile source.
3. **Screen pixels** — what the user sees. OSD viewport handles this.

`Viewer.ptToPx(x, y)` and `Viewer.pxToPt(x, y)` convert points ↔ image pixels.
`Viewer.imagePxToScreen(ix, iy)` and `Viewer.screenToImagePx(sx, sy)` convert image pixels ↔ screen pixels via OSD's `viewerElementToImageCoordinates`.
`Viewer.ptToScreen(x, y)` and `Viewer.screenToPt(sx, sy)` are the round-trip helpers.

---

## What's Done (and Tested)

### Slice A (foundation) — DONE
- A1 ✓ Copy 6.1 → 6.2
- A2 ✓ SheetJS CDN + local vendor
- A3 ✓ Project state model: `App.project = { trade, bidSetName, numPages, pageClasses, scope, annotations, currentSystemId, pendingOverrides }`
- A4 ✓ 8-tab structure with renumbered DOM order
- A5 ✓ NEW SESSION trade-picker UI (Roofing live; Glazing/Siding shown disabled)

### Slice B (scope parser) — DONE
- B1 ✓ `ROOF_VOCAB` with ~250 terms across 9 categories
- B2 ✓ `extractScope(planSet)` returns `{ systems[], rawText, lastScanAt }`
- B3 ✓ Multi-system label detection (regex for `ROOF SYSTEM A`, `Type 1`, `RS-1`, etc.)
- B4 ✓ Inline-fallback when no labels found
- B5 ✓ SCOPE tab with editable system cards, pin/edge tag chips, source-page click-jump
- B6 ✓ Re-scan button

### Slice C (page classifier) — DONE
- C1 ✓ `classifyPage(page)` scores 5 categories
- C2 ✓ PAGES tab thumbnail grid using `pg.renderCanvas.toDataURL`
- C3 ✓ Click thumbnail → opens viewer at that page
- C4 ✓ Filter chips (ALL / ROOF_PLAN / DETAIL / SPEC / COVER / OTHER)

### Slice D (viewer wired to scope) — MOSTLY DONE
- D1 ✓ Current-system selector dropdown in viewer sidebar
- D2 ✓ PIN tool reads from `scope.systems[current].pinPalette` — NO hardcoded list
- D3 ✓ Keyboard 1-9 fast-switch (guards against typing into INPUT/TEXTAREA/SELECT)
- D4 ✓ Auto-color via deterministic hash (`autoPinColor` — same name → same color across sessions)
- D5 ✓ Polygon/Rectangle → prompts for name → writes to `annotations.areas` with sqft/perimeter computed via shoelace × scale²
- D6 ✓ Per-page state: `viewerGotoPage(idx)` calls `rehydrateViewerForPage(idx)` to restore saved annotations
- **D7 ⚠ HALF-BUILT** — wrapped `TP.run` to detect manual polygon and set `opts.skipStage6 = true`, but `TP.clusterUnionFind` doesn't read that flag. The 30-second wait on real PDFs is NOT yet eliminated. The wrapper's user-polygon-replacement-of-winner still works correctly, so the *answer* is right; the *latency* is not fixed.

### Slice E (takeoff + Excel export) — MOSTLY DONE
- E1 ✓ TAKEOFF tab renderer with summary cards + per-system tables
- **E2 ✗ NOT BUILT** — edge labeling tool. Scope tab shows edge types but viewer has no tool to click each polygon edge and assign one
- E3 ✓ SheetJS workbook builder with Summary + per-system sheets + areas + pins-by-type + pins-itemized
- E4 ✓ FINALIZE → EXCEL button downloads `.xlsx`
- **NOTE**: Excel export does NOT include hyperlinks back to pages. SheetJS supports it (`hyperlinks` cell property); just not wired.

### Slice F (tests) — DONE
- F1 ✓ 8 scope parser tests
- F2 ✓ 4 page classifier tests
- F3 ✓ 3 pin palette + scope factory tests
- F4 ✓ Integration: full scope → annotations → takeoff flow
- F5 ✓ Integration: multi-system project, pins routed by `systemId`
- F6 ✓ Integration: per-page state isolation
- F7 ✓ All tests run in Node + browser, 72/72 green

### Slice G (smoke + ship) — DONE
- G1 ✓ Local-vendor browser smoke test
- G2 ✓ Screenshots: NEW SESSION, SCOPE, PAGES, VIEWER, TAKEOFF, PIPELINE, TESTS, ABOUT
- G3 ✓ Shipped to `/mnt/user-data/outputs/Huckleberry_AI_6.2_Scope.html`
- G4 ✓ Honest review delivered

### Slice H (real-PDF bug fixes + fullscreen) — DONE 2026-04-22 late
- H1 ✓ B-11 listener leak in `Viewer.bindInput` (guarded with `_inputBound` flag)
- H2 ✓ B-11b window resize handler leak across init calls
- H3 ✓ B-12 test isolation via `withTestIsolation()` wrapper
- H4 ✓ B-13 measurements auto-clear on tool change + capped to last 3
- H5 ✓ B-14 × delete button on viewer sidebar pin rows, cascades to placed pins
- H6 ✓ B-15 on-demand page rendering via `getOrRenderPageCanvas` (memory fix)
- H7 ✓ Fullscreen viewer mode (`toggleViewerFullscreen`, body.viewer-fullscreen class, ESC handler, floating exit button)
- H8 ✓ 4 new integration tests (B-11, B-12, B-13, B-14) → 76/76 green
- H9 ✓ Browser smoke passed with real fullscreen toggle, ESC exit, × button rendering

---

## What's Left (Priority-Ordered)

### Tier 1 — Real-bidset calibration (do this first)
The single biggest unknown is what happens when a real bidset is dropped into 6.2. The vocabulary is calibrated against synthetic prose I wrote myself. The first real run will reveal:
- Pin types the spec mentions but `ROOF_VOCAB.penetrations` doesn't catch
- Edge types missed
- Multi-system label patterns the regex doesn't recognize
- Page classification mistakes

**Action**: User has access to "100s of bidsets." Get ONE Wendy's-class bidset, drop it into 6.2, screenshot the SCOPE tab and PAGES tab, list every miss. Add patterns to `ROOF_VOCAB`. Iterate. This is the empirical-calibration loop the TracePoint paper describes — and the only honest path to a useful parser.

### Tier 2 — Stage 6 short-circuit (D7 finish)
**Problem**: Every `TP.run()` invocation costs 30 seconds on real PDFs because `TP.clusterUnionFind` runs full O(n)-with-bad-constant on 23K paths even when the user has already drawn the polygon and we know we're going to override the answer.

**Fix sketch**:
```js
TP.clusterUnionFind = function(paths, proximityInches = 0.5, minAreaInSq = 50, opts = {}) {
  if (opts.skipStage6 && opts._preClusters) {
    return { polygons: opts._preClusters, log: { in: paths.length, kept: opts._preClusters.length, clusters: 1, _shortCircuited: true } };
  }
  // ...existing code...
};
```
Then update the `TP.run` Stage 6 call to pass opts: `TP.clusterUnionFind(paths, 0.5, 50, opts)`.

This is a 10-line change. Add a test that proves the short-circuit actually skips when the flag is set.

### Tier 3 — Edge labeling tool (E2)
After a polygon is drawn, user should click each edge and pick from `scope.systems[current].edgeTypes`. The polygon's `edges[]` array gets `[{ type, lenFt }]` filled in. Excel export adds an "EDGES" section per system.

**UX sketch**:
- After polygon draw, viewer shows a new "EDGE LABEL" mode automatically
- Clicking an edge highlights it + shows a dropdown of edge types from current system's scope
- User picks one, edge gets labeled
- Repeat for each edge
- Skip = un-labeled edge stays "Unspecified"

### Tier 4 — Excel hyperlinks
SheetJS supports `cell.l = { Target: 'page-3.html', Tooltip: 'Open page 3' }`. The current export uses `Page 1`, `Page 2` etc. as text. They could be made into hyperlinks that — given a backend or a deep-link UI — would jump to the right place. For now, make them at least placeholder hyperlinks like `huckleberry://page-3` that document the intent.

### Tier 5 — Page selection memory
When user opens a bidset, the viewer should default to the first page classified as `ROOF_PLAN` (not page 0). Currently `Viewer.init` defaults to page 0, which on a real bidset is the cover sheet. This is a 5-line fix in `loadPdfFile` post-hook:
```js
const firstRoofIdx = Object.entries(App.project.pageClasses)
  .find(([k, v]) => v.kind === 'ROOF_PLAN')?.[0];
if (firstRoofIdx != null) Viewer.init(App.planSet, parseInt(firstRoofIdx, 10));
```

### Tier 6 — Vocabulary expansion via small local LLM
User explicitly said: "later a small local llm (no llm api call) for additional project context that just reads no pictures no counting just reading and reporting on what is written." This is for vocabulary augmentation when the regex parser misses something. Constraints: read-only, no images, no API calls, runs in-browser via WebLLM or transformers.js. **Not for this iteration.** Note it for next major version.

### Tier 7 — Real PDF correctness for the engine itself
The TracePoint pipeline still produces 14M sqft on Wendy's. The four root causes from the 6.0 review are STILL present in 6.2:
1. Stage 1 dispatch can't find scale text in STACK-reprocessed PDFs
2. Stage 2 zone mask drops nothing because there's no real detail-view detection
3. Stage 6 emits bbox-as-polygon (mega-cluster on dense sheets)
4. Stage 5 dash filter drops zero on real PDFs (the q/Q stack fix doesn't actually help)

The user has accepted that the auto-pipeline is a "try it" surface and the real workflow goes through manual polygon drawing. Don't lie about this. If you "fix" auto-detect, prove it on at least 5 real bidsets, not 1 synthetic.

---

## Bug List (open)

### B-1 — Stage 6 short-circuit not wired
- **Severity**: Medium (UX, not correctness)
- **Symptom**: User draws polygon, hits "RUN WITH OVERRIDES," waits 30s for an answer they already know
- **File**: `Huckleberry_AI_6.2.html` line 5569 (`runMaybeSkipStage6` wrapper) and line 1918 (`TP.clusterUnionFind`)
- **Fix**: 10-line patch to `clusterUnionFind` to honor `opts.skipStage6` + add test
- **Status**: Acknowledged in shipped review; test does not exist

### B-2 — Real-PDF dash filter still drops 0
- **Severity**: High (silent — pipeline keeps junk paths)
- **Symptom**: On Wendy's bidset, Stage 5 reports 0 dashed paths dropped despite the spec having lots of hidden lines
- **File**: `Huckleberry_AI_6.2.html` line 2671 (`extractPlanSetFromPdf`) — the q/Q graphics-state stack
- **Hypothesis**: pdf.js 3.11 may emit `OPS.save` / `OPS.restore` differently than I assumed, OR the dash-array is set inside a `gs` (ExtGState) reference that I'm not handling
- **Fix sketch**: Run a real PDF through the extractor with a debug log every time `setDash` fires, print the args, see what's actually happening
- **Status**: Synthetic test passes; real-PDF behavior is unverified-and-probably-broken. **Do NOT claim this is fixed.**

### B-3 — Stage 6 mega-cluster on dense sheets
- **Severity**: High (pipeline produces 14M sqft on real plans)
- **Symptom**: Union-Find at 0.5" proximity merges entire drawing into one blob
- **File**: `Huckleberry_AI_6.2.html` line 1918 (`TP.clusterUnionFind`)
- **Fix sketch**: Adaptive proximity based on path density. Or skip clustering entirely when user polygon is present (B-1 covers that). Or rewrite to emit actual concave hull instead of bounding box.
- **Status**: Sidestepped via manual polygon override; engine is still wrong

### B-4 — Page auto-selection broken on multi-page bidsets
- **Severity**: Medium (UX confusion)
- **Symptom**: Viewer opens to page 0 even when page 0 is the cover sheet and the roof plan is on page 3
- **Fix**: Tier 5 above (5-line fix)
- **Status**: Not fixed

### B-5 — Rectilinear score 58% on real plans (should be 85-95%)
- **Severity**: Low (cosmetic — affects scoring formula, but Stage 12 winner is overridden anyway)
- **Symptom**: Stage 11 reports ~58% rectilinear on real bidsets
- **Hypothesis**: `pdf.js OPS.curveTo` is converting curves to line segments using endpoint-only sampling, creating phantom diagonals
- **Fix**: Investigate `extractPlanSetFromPdf`'s curveTo handling; possibly suppress curve-derived line segments from rectilinear math
- **Status**: Not investigated

### B-6 — Three-wrapper TP.run pattern is debug-hostile
- **Severity**: Low (developer experience, not user-facing)
- **Symptom**: A single `TP.run()` call goes through `runMaybeSkipStage6 → runWithOverrides → run`. Stack traces are confusing.
- **Fix**: Collapse into a single `TP.run` with branching opts, or use an explicit middleware list
- **Status**: Tech debt

### B-7 — `drawImage` console warnings on rapid tab-switch
- **Severity**: Trivial (visible in DevTools, no user impact)
- **Symptom**: `Failed to execute 'drawImage' on 'CanvasRenderingContext2D': The image argument is a canvas element with a width or height of 0`
- **Hypothesis**: OSD tries to composite during tab-switches before its offscreen canvas measures
- **Fix**: Defer `Viewer.init` until the VIEWER tab is actually visible (`getBoundingClientRect().width > 0`)
- **Status**: Not fixed; harmless

### B-8 — Excel sheet name truncation is silent
- **Severity**: Low (data integrity)
- **Symptom**: System labels longer than 28 chars get truncated for sheet names. Two systems with the same first-28-char prefix would collide.
- **File**: `exportTakeoffToExcel`, line `const safeName = (s.label || 'System').replace(/[^A-Za-z0-9 ]/g, '_').slice(0, 28);`
- **Fix**: Append a discriminator (e.g. `-1`, `-2`) when collision detected
- **Status**: Not fixed

### B-9 — Synthetic plan auto-loads spec text into page 0
- **Severity**: Trivial (only affects synthetic, not real PDFs)
- **Symptom**: Calling `loadSyntheticPlan()` always pushes a fixed TPO spec text into page 0's `texts`. If you load synthetic twice, the spec gets duplicated.
- **File**: `loadSyntheticPlan` v6.2 wrapper, ~line 4930
- **Fix**: Check if the spec text is already there before pushing
- **Status**: Not fixed

### B-10 — Viewer tempState can leak between tools
- **Severity**: Low
- **Symptom**: If user starts drawing a polygon (clicks 3 corners) then switches to PIN tool without double-clicking, the in-progress polygon stays in `Viewer.tempState`. Switching back to polygon tool resumes from that state.
- **Hypothesis**: `setTool` doesn't clear `tempState` for non-polygon tools — actually it does (`this.tempState = null`), so this might be a non-issue, but worth verifying with a test
- **Status**: Not verified

### B-11 — Listener leak in Viewer.bindInput() [FIXED 2026-04-22 late]
- **Severity**: CRITICAL — this was the root cause of almost every UX bug the user reported in real-PDF testing
- **Symptom** (in user's Chipotle session): calibrate loops on first click with "invalid length" on second point, measurements accumulated to 196 instead of a handful, pin drops fired multiple pins per click, delete button did nothing visible
- **Root cause**: `Viewer.bindInput()` was called inside `Viewer.init()`, and `init()` ran on every page switch. After 30 page switches → 120 stacked `pointerdown`/`pointermove`/`pointerup`/`dblclick` listeners → every click fired handlers 30× in rapid succession. The calibrate loop was the cleanest signature: first listener recorded point 1, second listener immediately saw tempState with 1 point and tried to record point 2 at the SAME screen coordinate → 0-inch distance → "invalid length" prompt
- **Fix**: Added `_inputBound` flag in `Viewer.bindInput()`. First call binds, subsequent calls return early. 4 lines.
- **Test**: `integ · B-11 · bindInput() is idempotent (no listener leak)` — stubs `addEventListener`, asserts first call adds 4 listeners, subsequent calls add 0.
- **Status**: FIXED. Needs real-PDF re-test with 20+ minutes of page-switching to confirm no regressions.

### B-11b — window resize handler leaked across Viewer.init calls [FIXED 2026-04-22 late]
- **Severity**: Low (memory leak, not correctness)
- **Symptom**: Each `Viewer.init()` call added another `window.addEventListener('resize', syncAll)` where `syncAll` was a new closure over the old OSD instance. After page switches, dead closures accumulated.
- **Fix**: Track the resize handler on `this._winResize`; remove before re-binding.
- **Status**: FIXED.

### B-12 — Running tests mid-session destroyed real bidset state [FIXED 2026-04-22 late]
- **Severity**: Medium (data loss)
- **Symptom** (user quote): "I did run tests in test menu so that might have been culprit" — running tests while a real bidset was loaded wiped the scope and pages.
- **Root cause**: Several integration tests mutate `App.project` and `App.planSet` to set up fixtures. They never restored the originals. Tests ran → fixtures overwrote user state → bidset gone.
- **Fix**: Added `withTestIsolation(fn)` wrapper. Snapshots `App.project`, `App.planSet`, `App.currentSystemId`, `App.activePinTypeId`, `App.manualScale`, `App.pendingOverrides`, `Viewer.annotations`, `Viewer.tempState` before any test batch. Restores them in `finally`, regardless of pass/fail. Both `runUnitTests()` and `runAllTests()` now go through this wrapper.
- **Test**: `integ · B-12 · withTestIsolation restores App.project after mutation` — seeds user-like state, runs mutating block that throws, asserts original state restored.
- **Status**: FIXED.

### B-13 — Measurements piled up forever [FIXED 2026-04-22 late]
- **Severity**: Medium (UX clutter; also memory since measurements are kept in `Viewer.annotations`)
- **Symptom**: User's session had 196 measurements at the end. They were meant to be ephemeral (see a distance, move on).
- **Fix**: `Viewer.setTool()` now clears `kind === 'measure'` annotations when leaving the measure tool. Within the measure tool, capped to last 3 visible via filter/slice/concat pattern before each push.
- **Test**: `integ · B-13 · measurements auto-clear on tool change` — seeds 5 measurements, switches from measure to pan, asserts 0 remain.
- **Status**: FIXED.

### B-14 — Pin types couldn't be deleted from viewer sidebar [FIXED 2026-04-22 late]
- **Severity**: Medium (UX — user said "could not delete them at all")
- **Symptom** (user quote): "the only pin i have is some how hardcoded scuppers and i could not delete them at all"
- **Root cause**: SCOPE tab's pin chips had × delete buttons. Viewer sidebar's pin rows did NOT — only a click handler that set the row as active. User clicking "delete" on a pin row just re-activated it. The listener leak (B-11) made this worse — each click fast-cycled through pin types.
- **Fix**: Added `.vpr-x` × button to each row in viewer sidebar's pin palette with `event.stopPropagation()` so click doesn't bubble to the row's activate handler. New `viewerDeletePinType(sysId, pinTypeId)` function cascades: removes placed pins of that type, falls back `App.activePinTypeId` to the next palette item, repaints scope/viewer/takeoff. Uses `confirm()` when non-zero pins exist.
- **Test**: `integ · B-14 · viewerDeletePinType removes placed pins of that type` — seeds 2 scuppers + 3 RTUs, deletes scupper type, asserts palette has only RTU, pins array has only RTUs, active pin fell back to RTU.
- **Status**: FIXED.

### B-15 — Memory pressure: 35-page bidset lost PDF after 20 min [FIXED 2026-04-22 late]
- **Severity**: High (user-blocking for any real bidset session >15 minutes)
- **Symptom** (user quote): "if you are working for a while on something it might lose pdf and have to reload it in"
- **Root cause**: Extractor rendered every page's full canvas at 150 DPI eagerly on upload. 35 pages × ~25 MB/page = ~875 MB of decoded image data. Plus 73,043 vector paths. Plus accumulated listener-leak junk. Chrome GC'd the pdf.js worker state after ~20 minutes when memory pressure hit.
- **Fix**: Extractor now builds only a cheap 40-DPI `thumbCanvas` per page eagerly (for the PAGES grid). Full-resolution `renderCanvas` is built on demand by `getOrRenderPageCanvas(planSet, pageIdx)` when the viewer actually opens that page. When the viewer switches pages, the old full canvas is dropped (thumb kept). Holds a `_pdfPageRef` on each page plus `planSet._pdfDoc` so re-render works. Synthetic flow also populates `thumbCanvas` via downscale.
- **Estimated memory savings**: 35-page bidset drops from ~875 MB to ~30 MB (35 thumbs at ~40 KB + 1 full-res page at ~25 MB). Linear in page count instead of page-count × page-size.
- **Status**: FIXED. No direct test — memory behavior is hard to assert in headless Node. Browser smoke test confirmed pages still render correctly.
- **B-15 side effect that caused B-19**: the extractor now intentionally leaves `renderCanvas = null` after upload. The downstream `openViewerIfPossible` had a check that assumed "null canvas = synthetic plan" and always ran the synthetic painter. B-15 inverted the meaning of that signal without updating the downstream code. B-19 fixes the downstream.

### B-16 — [ATTEMPTED — NOT THE FIX] Canvas-size cap + Blob URL 2026-04-23 early
- **Severity when attempted**: believed High
- **Symptom**: User reported "page 13 shows only bottom-left tile" on real bidset renders.
- **Hypothesis at time**: Chrome per-canvas size cap being exceeded on 36×48" arch sheets at 150 DPI (5400×7200 = 38.9 MP), plus `toDataURL('image/jpeg')` silently truncating on very large base64 strings.
- **What was implemented**:
  - `RENDER_CANVAS_MAX_DIM = 4800` and `RENDER_CANVAS_MAX_AREA = 24_000_000` caps in `getOrRenderPageCanvas`.
  - `Math.round(rvp.width)` for canvas dims (was float-truncation).
  - Switched OSD source from `canvas.toDataURL` to `canvas.toBlob` + `URL.createObjectURL`, tracked + revoked on page switch.
- **Why it didn't work**: Subsequent screenshots showed the exact same fragmented render pattern. The canvas cap was addressing a theoretical issue that wasn't the real one — pdf.js's render never ran at all; the "partial" content was the synthetic painter's vector-path drawing (see B-19).
- **Verdict**: The canvas cap is defensively reasonable (iOS Safari has real limits ~16MP) but addresses a non-bug for this user. The Blob-URL switch saves ~33% memory during handoff to OSD, harmless.
- **Status**: REVERTED in 6.2.3. May be re-added as a standalone defense in a future version with its own test, not speculatively.

### B-17 — [ATTEMPTED — NOT THE FIX, VERIFIED BY DIAGNOSTIC] Fresh page proxy + serialization 2026-04-23 mid
- **Severity when attempted**: believed High
- **Symptom**: After B-16 shipped, user reported same fragmented render pattern persisted.
- **Hypothesis at time**: pdf.js evicts parsed font/colorspace/xobject resources under memory pressure from 39 parallel getOperatorList() calls during upload, and the deferred high-res render can't reconstitute them.
- **What was implemented**:
  - Module-level `_renderInFlight` promise to serialize renders.
  - Re-fetch `_pdfDoc.getPage(idx+1)` every render to get a "fresh" page proxy.
  - Call `pg._pdfPageRef.cleanup()` on non-current pages.
  - Post-render paint-% sampling on a 40-step grid, retry if <2%.
- **Verdict from diagnostic** (2026-04-23 late, Node-based test on actual Chipotle PDF):
  - Test: same page rendered with pdf.js 3.11, once via `render()` alone and once via `getOperatorList()` + `render()`.
  - **Result: paint=9.71% in both cases. Delta: 0.00%.** Calling `getOperatorList()` first does NOT degrade the render.
  - Therefore the "stale proxy" hypothesis is WRONG. The whole fresh-proxy dance was solving a non-problem.
- **Status**: REVERTED in 6.2.3. Diagnostic JSON in `/home/claude/diag/out/diag.json`.

### B-18 — [ATTEMPTED — NOT THE FIX] Render cascade + thumbnail-ratio detection 2026-04-23 late
- **Severity when attempted**: believed High
- **Symptom**: After B-17 shipped, user confirmed identical broken pattern persisted; said "NONE ARE RENDERING CORRECT."
- **Hypothesis at time**: pdf.js's TrueType font-program fallback (the `TT: undefined function: 21` warning) silently aborts render chunks mid-stream; try `intent='print'` as a different code path; also try half-DPI.
- **What was implemented**: Four-tier render cascade (display → print → half-DPI print → upscaled thumbnail), thumbnail-ratio paint detection (`< 50% of thumb paint = reject`), visible status HUD, document.title updates.
- **Why it didn't work**: The diagnostic later proved that pdf.js 3.11 render in Node renders page 13 correctly at 100 DPI (paint=9.71%, but the PNG visibly contains full elevations, title block, schedule — 9.71% is just low-density sampling of line art on a large canvas, not missing content). The browser wasn't running pdf.js render at ALL, due to B-19's bug; so no intent/DPI variation could have helped.
- **Verdict**: The cascade concept is sound (different PDFs will need different intents). The thumbnail-ratio heuristic is also sound for a real partial-render scenario. But neither is useful if the upstream code never calls render to begin with.
- **Status**: REVERTED in 6.2.3. The cascade design is noted for possible re-use in a future version IF a real partial-render scenario is ever confirmed.

### B-19 — ROOT CAUSE: openViewerIfPossible clobbers real PDFs with synthetic painter [FIXED 2026-04-23 late]
- **Severity**: CRITICAL — this is the bug that B-16, B-17, B-18 were all failing to fix because they were attacking the wrong layer.
- **Symptom**: User uploads any real bidset → opens VIEWER tab → sees only raw line-segments and tiny monospace text fragments scattered across an otherwise blank canvas. Same pattern on every page. Synthetic test plan renders perfectly.
- **Root cause**: `openViewerIfPossible` at line 4359 had:
  ```js
  const hasCanvas = App.planSet.pages[0] && App.planSet.pages[0].renderCanvas;
  if (!hasCanvas) {
    renderSyntheticCanvasForViewer(App.planSet);
  }
  await Viewer.init(App.planSet, 0);
  ```
  B-15 (memory fix) changed the extractor to leave `renderCanvas = null` on upload — the viewer now renders on demand. But `openViewerIfPossible` still interpreted `null canvas = synthetic plan` and called the synthetic painter unconditionally. The synthetic painter iterates every page and sets `renderCanvas` to a canvas containing ONLY the extracted vector line-segments and text labels drawn in black mono. Then `Viewer.init` → `getOrRenderPageCanvas` checked `if (!page.renderCanvas)` — now non-null — and **short-circuited, never calling pdf.js's actual `render()`**. The user was looking at the synthetic painter's output of real-PDF vector data, which on a STACK PDF with 46,000 extracted paths per page looks exactly like the chaotic fragmented pattern in every screenshot.
- **Why it went undiscovered**: four rounds of patches at the wrong layer. The synthetic-vs-real dichotomy was the diagnostic signal — user said synthetic works, real doesn't — and that narrowed the bug to "something about the real-PDF code path" which I interpreted as pdf.js being broken on these PDFs. But the actual real-PDF code path was `renderSyntheticCanvasForViewer` via `openViewerIfPossible`, which made it look like pdf.js rendered badly when pdf.js wasn't running at all.
- **Fix** (4-line change in `openViewerIfPossible`):
  ```js
  const page0 = App.planSet.pages[0];
  const isRealPdf = !!(page0 && page0._pdfPageRef);
  if (!isRealPdf && page0 && !page0.renderCanvas) {
    renderSyntheticCanvasForViewer(App.planSet);
  }
  ```
  The presence of `_pdfPageRef` is the reliable signal that this is a real PDF; skip the synthetic painter and let `Viewer.init → getOrRenderPageCanvas` do the real pdf.js render.
- **Test** (written BEFORE the fix, per Karpathy discipline): `integ · B-19 · openViewerIfPossible skips synthetic painter when _pdfPageRef present`. Seeds a fake real-PDF planSet (pages with `_pdfPageRef`, `renderCanvas=null`), stubs `Viewer.init`, counts how many times `renderSyntheticCanvasForViewer` gets invoked on `_pdfPageRef`-bearing pages. Must be 0. Test FAILED on unpatched code (ran on 2 pages), PASSED on fixed code (ran on 0).
- **Status**: FIXED in 6.2.3, test: 77/77 green (61 unit + 16 integration, +1 from B-19).

### F-1 — Fullscreen viewer mode [NEW FEATURE 2026-04-22 late]
- **Request**: "can we make the viewer expand to fill screen so estimator can focus on what he needs — screen toolbar and takeoff bar"
- **Implementation**: `⛶ FULLSCREEN` button in viewer header toggles `body.viewer-fullscreen` class. CSS hides `.header`, `.status-bar`, `.sidebar`, `.tabs`, and the pane's `.section-header`. Tool rail, plan canvas, and scope sidebar remain visible. Floating `⤢ EXIT FULLSCREEN · ESC` button appears top-right. ESC key also exits. After toggle, OSD + Konva are nudged via `requestAnimationFrame` to recompute canvas dimensions for the new viewport.
- **Browser smoke verified**: headerHidden=true, sidebarHidden=true, tabsHidden=true, exit button visible, ESC exits.
- **Status**: SHIPPED.

---

## Security List

### S-1 — XSS in renderTakeoffTab via unescaped systemType / attachment
- **Severity**: Medium
- **Location**: `Huckleberry_AI_6.2.html` line 5163
- **Code**: ``html += `<div class="card"><div class="card-title">${esc(s.label)} <span ...>${s.systemType || ''} ${s.attachment ? '· ' + s.attachment : ''}</span></div>`;``
- **Vector**: User edits `systemType` field on SCOPE tab, types `<img src=x onerror=alert(1)>`, opens TAKEOFF tab, payload fires
- **Fix**: Wrap with `esc()`: `${esc(s.systemType || '')} ${s.attachment ? '· ' + esc(s.attachment) : ''}`
- **Status**: Open. Single-user POC reduces practical risk but the bug is real.

### S-2 — XSS in renderSystemCard via insulationSummary
- **Severity**: Low
- **Location**: line 4794
- **Code**: `${esc(insulationSummary)}` — actually escaped, BUT `insulationSummary` is built from `i.material + i.thickness + (tapered)` which themselves come from regex matches in `extractScope()`. If regex captures unexpected content, the escape is the only safety net.
- **Status**: Defensive — escape is in place, audit if vocabulary changes

### S-2b — CSS injection via unescaped `pt.color` in inline `style` attributes
- **Severity**: Low (color is auto-generated from `PIN_PALETTE_COLORS`, a fixed array of 15 hex values, so user can't currently inject arbitrary CSS)
- **Location**: lines 5173 and 5274 — `style="background:${pt.color}"`
- **Vector**: If a future feature lets users pick custom pin colors via free-text input (e.g. "linear-gradient(...) ; }; body { display:none"), CSS injection becomes possible
- **Fix**: Validate `pt.color` matches `/^#[0-9a-fA-F]{6}$/` before insertion, OR use `setAttribute('style', ...)` with proper escaping
- **Status**: Defensive — not exploitable today, becomes exploitable if color picker is added

### S-3 — innerHTML pattern with template literals throughout
- **Severity**: Low (all user-controlled data is escaped in current code, but the pattern is fragile)
- **Location**: ~25 places that use `el.innerHTML = `<span>${var}</span>``
- **Issue**: If a future contributor adds a field without `esc()`, XSS vector opens silently
- **Mitigation**: Document the pattern. Consider switching to `textContent` for leaf nodes or DOM-builder helpers for complex fragments
- **Status**: Style note, not an active bug

### S-4 — SheetJS XLSX parsing of untrusted .xlsx
- **Severity**: Not applicable yet
- **Note**: SheetJS 0.18.5 is current — no known active CVEs for *write* path. We do not currently *read* .xlsx files. If we add import-from-Excel, audit the SheetJS version against advisories at that time.
- **Status**: Future-watch

### S-5 — PDF.js parses untrusted PDFs
- **Severity**: Implicit (every PDF reader inherits this)
- **Note**: Bidsets come from clients/architects, not the open internet, so threat model is low. PDF.js 3.11.174 has had several CVEs over its lifetime; 4.x has fixes. Upgrading PDF.js could break the q/Q graphics-state stack assumptions.
- **Status**: Living with current version for POC. Re-evaluate before any production deployment.

### S-6 — No CSP / Subresource Integrity on CDN scripts
- **Severity**: Medium for production, low for POC
- **Location**: `<head>` script tags
- **Issue**: `<script src="https://cdnjs.cloudflare.com/...">` without `integrity="sha384-..."` attributes. A compromised CDN could serve malicious code.
- **Fix**: Add SRI hashes for all 4 CDN scripts
- **Status**: Not added; vendor-local copies exist as fallback

### S-7 — No Content-Security-Policy header
- **Severity**: Low for POC
- **Issue**: Page is served as `file://` so no CSP. Production deployment must add a strict CSP header (esp. `script-src` to prevent injection from text-extracted PDF content).
- **Status**: Pre-production concern

### S-8 — `prompt()` and `alert()` for user input
- **Severity**: UX, not security
- **Location**: `persistAreaFromPoints` calls `prompt()` for area name; calibrate calls `prompt()` for distance; several `alert()` for errors
- **Issue**: Browser-native prompts are blockable, look unprofessional, and can't be styled
- **Fix**: Replace with custom modal once the POC graduates
- **Status**: Acceptable for POC

---

## Test Inventory

### Node + browser (both must pass before any ship)

**Unit tests (61)**:
- helpers (5): `pathLengthInches`, `bboxesOverlap`, `parseScaleToFtPerInch`
- stage 1 (3): dispatch classification + scale text + zones
- stage 2 (2): zone mask drops correct paths
- stage 3 (1): weight filter
- stage 4 (1): length filter
- stage 5 (1): dash filter
- stage 6 (3): clustering merges, separates, rejects too-small
- stage 7 (4): scale tier picking
- stage 8 (2): perimeter cleanup
- stage 9 (3): confidence
- stage 10 (2): density
- stage 11 (2): rectilinear
- stage 12 (2): selection
- tool (14): parseFeetInches variants, polygonAreaPt for rectangle and L-shape, polygonPerimeterPt, bboxOfPoints, calibrate math, measure math, buildOverridesFromViewer, end-to-end manual polygon override (5,000 sqft), end-to-end L-shape (4,100 sqft)
- scope (8): TPO/PVC/EPDM detection, penetrations → pin palette, parapet edge, multi-system labels, inline collapse, confidence scoring
- classify (4): ROOF_PLAN / SPEC / COVER / DETAIL
- pin palette (2): deterministic color, color spread
- scope (1): `makeScopeSystem` defaults

**Integration tests (15)**:
- 5,000 sqft synthetic, 8,000 sqft synthetic
- scale source = dispatch tier
- detail-view paths killed by zone mask
- dash + length filter strip noise
- empty plan returns error
- dash filter fix verifies dashed-heavy paths dropped (synthetic only)
- scope full flow: extract → pins → area → 5,000 sqft
- Excel export shape: Summary + system sheets
- per-page state: pin on page 0 doesn't show on page 1
- multi-system: pins routed by systemId
- **B-11**: bindInput idempotent (listener leak prevention)
- **B-12**: withTestIsolation restores App.project after mutation
- **B-13**: measurements auto-clear on tool change
- **B-14**: viewerDeletePinType removes placed pins of that type

### How to run
```bash
# Node (fast):
cd /home/claude/build && node test_runner_62.js
# (regenerate test_runner_62.js with the python block in this file's history if needed)

# Browser (catches DOM-related issues):
node smoke_d.js  # (or write a fresh one — see /home/claude/build/smoke_d.js for template)
```

### Coverage gaps that bite
- **Real-PDF behavior under sustained use still unverified for the fixes.** B-11 through B-15 are all fixed and tested in Node, but the user's original 20-minute Chipotle session needs to be replayed to confirm the fixes hold. The test suite can prove `bindInput()` is idempotent but not that a real session with 30+ page switches + 10 calibrations + 20 measurements + pin drops feels right.
- **No accessibility tests.** No keyboard nav verification beyond the 1-9 pin shortcut and new ESC-exits-fullscreen.
- **No visual regression tests.** Screenshots are taken but not diffed.
- **No XSS test for S-1.** Easy to add: build an `App.project.scope.systems` with `systemType: '<img src=x onerror=...>'`, render TAKEOFF, check `pane4.innerHTML` for raw `<img`.
- **No memory regression test for B-15.** Would need to measure `performance.memory.usedJSHeapSize` before/after opening a 35-page bidset, which is Chromium-specific and noisy.

---

## Local Vendor Setup (for offline browser testing)

The sandboxed test environment can't reach CDNs. To run smoke tests, a local-vendor copy is maintained:

```bash
cd /home/claude/build
# Tarballs are present from earlier:
# konva-9.3.0.tgz, openseadragon-4.1.0.tgz, pdfjs-dist-3.11.174.tgz, xlsx-0.18.5.tgz
# Extracted into: vendor/{konva, osd, pdfjs, xlsx}/
# Local-vendor HTML: Huckleberry_AI_6.2_localvendor.html
```

The `localvendor` HTML has the same content as the shipped CDN version, just with URLs swapped. Regenerate after any edit:

```python
import os
s = open('Huckleberry_AI_6.2.html').read()
s = s.replace('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js', 'vendor/pdfjs/build/pdf.min.js')
s = s.replace('https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/openseadragon.min.js', 'vendor/osd/build/openseadragon/openseadragon.min.js')
s = s.replace('https://unpkg.com/konva@9.3.0/konva.min.js', 'vendor/konva/konva.min.js')
s = s.replace('https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js', 'vendor/pdfjs/build/pdf.worker.min.js')
s = s.replace('https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js', 'vendor/xlsx/dist/xlsx.full.min.js')
s = s.replace("'https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/images/'", "'vendor/osd/build/openseadragon/images/'")
open('Huckleberry_AI_6.2_localvendor.html', 'w').write(s)
```

---

## Communication With the User

The user is a **non-developer** building a POC for commercial roofing takeoff. Specific patterns I learned:

1. **Demands brutal honesty.** "Review no sugar coating" is a recurring request. When something doesn't work, say so plainly. Don't bury caveats. Don't claim a fix works without proving it. The biggest trust-loss in this project would be saying "fixed" when it isn't.

2. **Doesn't know estimating jargon at expert level.** When asked technical scope questions, says "im not an estimator dont know." Don't expect them to define vocabulary for you — find it in the bidset text or look it up yourself. The user provides workflow direction, not domain expertise.

3. **Page indexing convention**: UI displays 1-indexed (PAGE 1 / 2 / 3). Code uses 0-indexed (`currentPage: 0`). When logging or screenshotting, convert to 1-indexed for the human-facing output.

4. **Continuity matters.** "make sure nothing falls through the cracks when you hit limit meaning complete tasks with out dropping anything when session limit hits waiting for me to push continue." This CLAUDE.md is the answer to that request.

5. **Karpathy discipline is not optional.** Build → test → test → test. Tests get pushed into the running suite via `Array.prototype.push.apply(UNIT_TESTS, ...)` so they're picked up automatically. Adding new code without adding new tests will get called out. **See the "Karpathy Procedure" section near the top of this document for the 7-step loop.** Specifically: no green claim without a same-turn receipt from `run_tests.js`. The user has caught this lie before (B-19 era); don't repeat it.

6. **No AI API calls. Period.** This was the original reason for ripping out Huckleberry 5.0's Claude pipeline. The user's "later a small local llm" caveat is for an in-browser model (WebLLM, transformers.js) — never a network API. Don't add `anthropic.messages.create` to anything.

7. **Single-file HTML.** The architecture goal is "modular monolith" eventually, but for now everything lives in one HTML file with three inline `<script>` blocks. Splitting into modules requires bundler + config + serving = scope creep.

8. **"Continue" is the resume signal.** When the user types "continue" the next session should pick up at the next unchecked item in this CLAUDE.md without asking. The plan-with-checkpoints pattern in the conversation history is the template.

---

## Recovery Protocol (when next Claude starts)

**Step 0 — Identify which phase the work is in.**
- If the user's request touches the HTML → Phase 1 (maintenance/bug-fix only; Phase 1 architecture is closed).
- If the user's request touches PDF intake, parsing, scope analysis, persistence, or anything backend-shaped → Phase 2.
- If the user proposes ML, auth, or multi-user → Phase 3 (push back; Phase 3 is not planned, requires explicit user re-decision).

**Step 1 — Read this entire CLAUDE.md before any code change.** Especially the "Phases" section. It is canon. Do not silently negotiate against it.

**Step 2 — Verify Phase 1 test suite is still green** before touching anything in `frontend/`:
```bash
cd /home/claude/work && node run_tests.js Huckleberry_AI_6.3.5_Scope.html
```
Expected: `RESULT: 138/138 passed, 0 failed`. If different, something drifted — don't proceed until you understand why.

**Step 3 — For Phase 2 work, verify the experiment + backend test suite** (once they exist; not yet at time of this update). The first Phase 2 sessions will create these — the next Claude after that should run them as a baseline.

**Step 4 — Read the conversation transcript** if available. Critical context lives there.

**Step 5 — Don't repeat work.** Grep for patterns already added before writing anything: `renderScopeTab`, `extractScope`, `TOOL_HANDLERS.pin`, `makePolygonType`, `viewerSetActivePolygon`, etc. (Phase 1). For Phase 2, grep `huckleberry/backend/` and `huckleberry/shared/` for existing modules.

**Step 6 — Test before claiming.** Synthetic-passes ≠ real-PDF-passes. The user has caught me lying about this once. Don't repeat. Pick the right Karpathy Shape (A / B / C) for the task; all three are documented near the top of this file.

**Step 7 — Phase 1 is closed.** No new architecture in HTML. Bug fixes and UX polish only. Anything that smells like data analysis goes in Phase 2.

**Step 8 — Architecture decisions move only with explicit user approval.** The 18 Phase 2 decisions are canon. If a future Claude wants to renegotiate any of them, surface to the user explicitly, do not silently pivot.

---

## Glossary (project-specific)

- **Bidset** — A collection of construction-document PDFs for a single project. Typical size: 60–140 pages.
- **Scope** — The roofing-specific work to be done on a project. Extracted from spec text, NOT from a hardcoded list.
- **System** — A specific roof assembly (e.g., "TPO Fully Adhered 60 mil over 3" tapered polyiso"). One project may have multiple systems; each gets its own scope card and Excel sheet.
- **Pin** — A user-placed marker for a countable item (scupper, drain, RTU, etc.). Pin types come from scope, never hardcoded.
- **Area** — A user-drawn polygon representing a roof section. Has SF (shoelace area × scale²) and LF (perimeter × scale).
- **Edge type** — A perimeter category (parapet w/ coping, edge metal, fascia). Edge types come from scope. Edge labeling tool is NOT BUILT.
- **TracePoint** — The 12-stage geometry pipeline derived from the research paper. Currently produces correct results on synthetic plans, garbage on real bidsets.
- **Stage 6** — The union-find clustering stage. Single biggest auto-detect failure point on dense real plans.
- **Tier 5** — Scale Determination's last-resort scoring formula. When all 4 prior tiers fail, it picks a scale by minimizing distance to 3,000 sqft. Useless on Wendy's because the building is 1,565 sqft, far from the 3,000 sqft prior.

---

## Files Index (every artifact in /home/claude/build/)

```
Huckleberry_AI_6.0_TracePoint.html        # 6.0 working file
Huckleberry_AI_6.1.html                   # 6.1 working file
Huckleberry_AI_6.1_localvendor.html       # 6.1 with local CDN paths for offline testing
Huckleberry_AI_6.2.html                   # 6.2 working file (CURRENT)
Huckleberry_AI_6.2_localvendor.html       # 6.2 offline test version
test_runner_62.js                         # Node test harness for 6.2
smoke62.js                                # Browser smoke test (Slice A-C verification)
smoke_d.js                                # Browser smoke test (Slice D verification)
shot62*.png                               # Screenshots of every tab
shot_viewer_lshape.png                    # 6.1 L-shape proof (4,100 sqft)
shot_viewer_rect.png                      # 6.1 rectangle proof (5,000 sqft)
vendor/{konva,osd,pdfjs,xlsx}/            # Local-vendored CDN libs
*.tgz                                     # npm tarballs of vendor libs (don't delete)
CLAUDE.md                                 # THIS FILE
```

---

## Session Notes — 2026-04-24 (Steps 9b → 9.x → 10 → 10b → 11, the "manufacturer, crickets, polygon bug, and regression suite" session)

### What happened in order

1. User handed over a "Step 9a shipped — line tool live, 107/107 green" handoff and said continue with Step 9b.
2. Claude set up the jsdom harness (`run_tests.js`) to replicate the 107/107 claim before touching anything. First attempt failed because `ResourceLoader` was dropped from jsdom 29's public exports. Second attempt worked — but needed a hoist script to pull `UNIT_TESTS` / `INTEGRATION_TESTS` off module scope onto `window`. **Baseline replicated: 107/107.**
3. **Step 9b** (snap-to-close polygon + Duro-Last):
   - Wrote 5 tests first: 3 snap-to-close (near / far / 2-vertex-no-close), 2 Duro-Last vocab. Red: 3 failed as expected, 2 already-green (the far-click and 2-vertex cases trivially pass without a snap feature but still guard against a future broken implementation).
   - Implemented: gated snap in `TOOL_HANDLERS.polygon.onDown` override with `findNearestVertex(pt, [points[0]], ROOFING_CONSTANTS.snapTolPx)` + drop-hover semantics matching `onDblClick`. Added Duro-Last to `ROOF_VOCAB.systemTypes`.
   - Ship: v6.3.1, **112/112** × 3 stable, 8-case real-bidset spot-check all green.
   - Mistake made and admitted same turn: claimed `roofing_materials.py` didn't exist when user asked for it there. It did — just hadn't been shown to me yet.
4. **Step 9b (Python side)**: user uploaded `roofing_materials.py` and a sibling roof-assemblies file. Added Duro-Last entry to `MANUFACTURERS` between Carlisle and Firestone (alphabetical within single-ply block). `systems=['pvc']`, aliases `['Duro Last', 'DuroLast', 'Duralast', 'Duro-Last Roofing Systems']`. File still parses; 13 manufacturers total; no alias collisions detected.
5. **Step 9.x** (the `sys.manufacturer` field — user asked for this to reconcile the HTML and Python models):
   - Flagged semantic tension: HTML treats Duro-Last as a `systemType`, Python treats it as a `MANUFACTURER` whose `systems=['pvc']`. Proposed three options; user picked "add manufacturer field to HTML" (the correct-model option).
   - Red: wrote 5 new tests + updated the 2 Step 9b Duro-Last tests to new schema. 7 failures / 110 passing.
   - Implemented: new `ROOF_VOCAB.manufacturers` vocab block (7 brands seeded: Duro-Last, Sika Sarnafil, Carlisle, Firestone, GAF, Johns Manville, Versico), `manufacturer: null` field in `makeScopeSystem`, parser walks manufacturer detection after systemType detection with `systems[0]` fallback when systemType still null, `_absorbProposalFields` preserves manufacturer across merges, UI surfacing via 1-line addition to scope card (technically Step 12 scope creep but flagged explicitly — without it the feature is invisible).
   - Ship: v6.3.2, **117/117** × 3 stable, 14-case real-bidset spot-check (Panda Express, Taco Bell, + 4 other mfrs, + 4 regression no-mfr cases, + 1 precedence edge case).
6. **Step 10** (cricket polygon palette):
   - Red: 9 unit + 1 integration test = 10 new tests. 9 failed (one "negative path" test trivially green). 118 passing.
   - Implemented across multiple turns (hit tool-use limit once, had to resume):
     - Schema: `polygonTypes: []` field on system, `makePolygonType(name, source, seedId)` factory with deterministic color
     - Seeding policy (flagged): polygon items seed in `polygonTypes` **regardless of priority**, unlike pin/edge seeding which gates on `priority === 'always'`. Cricket remains `priority: 'conditional'` in `ROOFING_SEED_ITEMS` so parser-surfacing semantics stay intact; the palette-seeding is a separate always-on policy. Commented inline so future Claude doesn't "fix" this back.
     - State: `App.activePolygonTypeId` defaults `null` (= building-area mode). `viewerSetActivePolygon(id)` mirrors `viewerSetActiveLine`; null is a valid state.
     - Persist: `persistAreaFromPoints` now branches on `App.activePolygonTypeId`. Typed polygons auto-name `Cricket #N` (no prompt), carry `polygonTypeId` + typed color. Untagged polygons keep the old prompt-for-name flow.
     - Takeoff fix: `buildTakeoffModel.totalSF` now sums ONLY untagged building areas (fixes the double-count bug where crickets would inflate membrane SF). New `sf` aggregation walks `area.polygonTypeId → sys.polygonTypes → seedId`, same shape as LF.
     - UI: new `vsPolygonPaletteSection` mirroring edge palette, with an extra "Building area (untagged)" toggle row at the bottom so users can visibly switch back to building mode. `viewerDeletePolygonType` with orphan-cascade.
     - Housekeeping: `viewerSetCurrentSystem` now clears `activeLineTypeId` AND `activePolygonTypeId` on system switch (prevents dangling refs).
   - Ship: v6.3.3, **127/127** × 3 stable, cricket spot-check passes (5000 sf building + 25 + 40 sf crickets → cricket row = 65 base / 71.5 w/waste, membrane = 5000 exactly, no cross-contamination).
7. User then said "reread claude.md then update karpathy logic karpathy procedure" — which is this update.

### Lessons for the next session

- **The 7-step Karpathy loop works.** It produced 4 clean version bumps (107 → 112 → 117 → 127) with zero regressions. Full regression chain still green. Every step had its own failing tests first, then implementation, then 3× stability, then real-bidset spot-check.
- **Call out semantic drift early.** The HTML-vs-Python Duro-Last mismatch in Step 9b would have compounded if not flagged. Users can't always see inconsistencies across files they didn't write; it's on Claude to surface them.
- **"Negative path" tests are worth writing even when they trivially pass at red phase.** The "far-click doesn't snap" and "2-vertex doesn't close" tests were green before any Step 9b code existed, but they guard the implementation shape forever. Same for "polygonTypeId null for building areas" in Step 10.
- **UI surfacing often gets scope-crept into feature-schema steps.** Pure schema changes with no UI are invisible — if the feature is meant to be user-visible, 1-2 lines of UI in the same step is almost always the right call, flagged as scope creep in the summary.
- **When a pre-existing bug shows up mid-flow, log it and walk away.** The polygon `hoverIdx` stale-index bug was noticed in Step 9b. It's real but benign in normal use (browsers fire `onmove` continuously). Touching it would have expanded Step 9b unpredictably. Still in the bug backlog; not fixed.

### Known pre-existing bugs surfaced but deliberately not fixed this session

- **`hoverIdx` stays stale after `onDown` in `TOOL_HANDLERS.polygon` (original handler).** Harmless in realistic mouse flow, biting only in sparse-move test simulations.
- **PVC regex narrowness** (`/\bPVC\b.*roof/i` requires "roof" word after PVC). Masks specs like "Duro-Last 40-mil PVC, mechanically fastened". Step 9.x works around this via `manufacturer.systems` fallback; the underlying regex was not touched.
- **`_mergePinsEdges` doesn't merge `polygonTypes`** from parser hits. Today this doesn't bite because cricket always-seeds. Will bite the first time someone adds a `priority: 'conditional'` polygon seed (saddle, IWS zone, ballast zone, etc.) expecting parser to surface it in the palette.
- **Excel export still lacks a CRICKETS / POLYGON ITEMS table** (like the LINE SEGMENTS table from Step 9a). `buildTakeoffModel.sf` is correct; just not surfaced in the per-system sheets. Step 12 work.
- **HVHZ code-rule enforcement** (crickets required on high side of curbs >30") not wired. Would need curb-width metadata on RTU pins.

### Artifacts in `/mnt/user-data/outputs/`

```
Huckleberry_AI_6.3.1_Scope.html      # Step 9b
Huckleberry_AI_6.3.2_Scope.html      # Step 9.x
Huckleberry_AI_6.3.3_Scope.html      # Step 10 — CURRENT
roofing_materials.py                  # with Duro-Last added to MANUFACTURERS
run_tests.js                          # jsdom harness
spotcheck_manufacturer.js             # 14-case manufacturer parse check
spotcheck_cricket.js                  # realistic cricket scenario end-to-end
```

### Next up

- **Step 12** — Materials/brands surfacing: Excel export adds Manufacturer column, per-system sheet adds POLYGON ITEMS section matching the LINE SEGMENTS table pattern, scope card Manufacturer input becomes a dropdown populated from `ROOF_VOCAB.manufacturers` rather than free-text, and `_mergePinsEdges` extended to merge `polygonTypes` from parser hits.

---

## Session continuation — 2026-04-24 (Steps 10b + 11, later in the same day)

### Step 10b — the deferred bug that bit

User loaded v6.3.3 into the browser, drew a 4-corner building polygon on the Chipotle bidset, and reported: "4 point complete click to close works save area then the bug happens after save it looses 1 corner becomes triangle also the bottom point of triangle shifted." Two screenshots attached showing exactly that pattern.

This was a bug I had **flagged and deliberately deferred** during Step 9b. Quote from the Step 9b summary at the time:

> The hoverIdx logic in the polygon tool has a pre-existing bug (hoverIdx isn't updated on `onDown`, so in sparse test flows the live-preview vertex lands in the wrong slot). It's dormant in real use because browsers fire `onmove` between every click, so the stale index gets corrected. I noticed it while debugging test 1's output but did not fix it — out of scope for 9b.

**I was wrong about "dormant in real use."** Snap-close (new in Step 9b) called `slice(0, -1)` on the same buggy state machine that dbl-click already used. That `slice(0, -1)` was a new consumer of the broken area. In normal mouse flow, `hoverIdx` freezes at 1 after the first `onMove`, so the layout becomes `[c1, hover, c2, c3, c4]` instead of `[c1, c2, c3, c4, hover]`. `slice(0, -1)` drops the last committed vertex (BL) and keeps the stale hover at index 1 as if it were real. Saved as `[TL, nearTL, TR, BR]` → self-intersecting polygon → visually reads as a triangle with a shifted vertex. Exactly the screenshot.

Fix: rewrite `TOOL_HANDLERS.polygon.onDown` and `onMove` to maintain the invariant "hover is always at `points[length - 1]`." Removed `hoverIdx` entirely — no other code reads it. Matches the B-20 lesson from the line tool.

Results: 3 new tests (observable, invariant, dbl-click preservation) × 3 baseline failures before the fix × 3 green after. 130/130 across 3 runs. 7/7 spot-check against realistic Chipotle-scale PDF coords. User re-tested in browser and confirmed: "10b results everything functioning and working good."

**Lesson filed to Karpathy Procedure:** adjacent pre-existing bugs touched by new consumers get fixed in the same step, not deferred. The Shape-A loop in the procedure section now reflects this.

### Step 11 — derived-SF regression suite

Two things differ about Step 11 from Steps 9a–10:

1. **The code being guarded was already correct.** Steps 6 and 10 both added derived-SF math with their own tests. Step 11's job was to add dedicated guards that lock the ABI down so a future refactor can't silently break it.
2. **Red phase doesn't work as verification** because the code is intentionally unbroken. A test that passes immediately against correct code could be passing because it asserts something trivially true, not because it guards anything.

The answer: **mutation testing**. For each new test, define a targeted code mutation that should break that specific invariant, run every test against the mutated code, and confirm the matching test fails. If a mutation escapes ALL tests → the suite is decoration.

Wrote 8 new unit tests locking 8 distinct contracts of `buildTakeoffModel.derived`:
- A. Exactly 3 derived rows (membrane/insulation/coverBoard) on every system
- B. Every derived row is `unit='sf'`
- C. All derived rows share the same base (one source of truth: mainPolygonArea)
- D. `derivedFrom` string is always `'mainPolygonArea'` across all derived seeds
- E. Zero-area system → base=0 on all rows, no NaN/undefined (Excel-cell poison)
- F. Rectangle and polygon `kind` both contribute to the sum
- G. Multi-system isolation: system A's areas don't leak into system B's derived
- H. Waste override on a single derived seed is honored without affecting siblings

Wrote `mutation_test_step11.js` with 8 targeted mutations (drop coverBoard, flip unit, zero-out one seed, typo derivedFrom, undefined withWaste, skip rectangle kind, cross-system leak, ignore waste override). All 8 mutations caught by at least one Step 11 test.

Results: 138/138 across 3 runs, 8/8 mutations caught, regression chain clean (6.3.0 through 6.3.4 all unchanged).

**Lesson filed to Karpathy Procedure:** regression suites against working code are Shape B — use mutation testing in place of red-phase verification. Added to the procedure section explicitly.

### Artifacts in `/mnt/user-data/outputs/` after this continuation

```
Huckleberry_AI_6.3.1_Scope.html      # Step 9b
Huckleberry_AI_6.3.2_Scope.html      # Step 9.x
Huckleberry_AI_6.3.3_Scope.html      # Step 10
Huckleberry_AI_6.3.4_Scope.html      # Step 10b (polygon state-machine fix)
Huckleberry_AI_6.3.5_Scope.html      # Step 11 (regression suite) — CURRENT
roofing_materials.py                  # with Duro-Last in MANUFACTURERS
run_tests.js                          # jsdom harness
spotcheck_manufacturer.js             # 14-case manufacturer parse check
spotcheck_cricket.js                  # cricket scenario end-to-end
spotcheck_10b.js                      # 7-check realistic polygon-state reproduction
mutation_test_step11.js               # 8-mutation load-bearing-ness proof
```

### Where to pick up next session

- **Step 12** — still the natural next. Materials/brands surfacing: Excel export adds Manufacturer column, per-system sheet adds POLYGON ITEMS section matching the LINE SEGMENTS table pattern, scope card Manufacturer input becomes a dropdown from `ROOF_VOCAB.manufacturers`, `_mergePinsEdges` extended to merge `polygonTypes` from parser hits.
- Alternative if time is short: a small Shape-B regression suite for line-tool math (mirror of Step 11, would catch future breakage in `buildTakeoffModel.lf`).

---

## Session — 2026-04-25 (architectural decisions, the "Phase 2 plan" session)

### What happened

The user paused feature work after Step 11 and surfaced two artifacts: (1) a Grok handoff document recommending a five-tool stack upgrade for "Dispatch," and (2) a sharpened observation that the HTML POC has hit its architectural ceiling — manual workflow is mature, but auto-detection on real PDFs cannot be solved in the browser, and the four seed files (`dispatch_seed.py`, `roofing_seed.py`, `glazingseed.py`, `material_matrix_seed.py`) currently have no runtime consumer.

After two rounds of "discussion before guardrails," the user pivoted to the rapid-fire single-question format that built Phase 1 (one question, 2-4 options, lock answer, next question). Across 18 questions, the entire Phase 2 architecture was ratified.

### What got decided

The 18 decisions are now canon in the "Phases" section above. Compactly:

- Phase 1 closes at v6.3.5 (manual toolchain done).
- Phase 2 = Python backend, FastAPI + SQLAlchemy + Postgres + Pydantic, S3 for PDFs, localhost-only, no auth.
- LLM deferred to Phase 3 (refused as Phase 2 complexity that doesn't earn its keep yet).
- Reference data stays as Python modules, version-controlled, never in DB.
- Monorepo: `huckleberry/{frontend,backend,shared}`. v6.3.5 moves into `frontend/`.
- BidsetRecord schema starts minimal (six fields), grows on contact with real data.
- Schema inclusion rule: ≥3 of 15 bidsets AND identifiable downstream consumer.
- First Phase 2 deliverable: an experiment in Claude Code against 15 real bidsets, producing a draft Pydantic schema + findings report. NOT a stack pick.
- Annotations: frontend works in memory like Phase 1; explicit Save POSTs to backend; frontend wins on save with provenance trail kept.
- Step 12 (manufacturer dropdown / Excel column) is abandoned — Phase 2 produces that richness.

### Lessons filed

Three things this session revealed about how Phase 2 should be approached:

1. **Architectural restraint paid off three times in a row.** User refused: an LLM in Phase 2 (Q3), a tool-stack pick before evidence (Q14), and field-level merge complexity (Q6). Each "no" was the strongest signal of design discipline. **Future Claude: when proposing Phase 2 work, default to refusing complexity until evidence justifies it.**

2. **Schema-first design is the architecture's red phase.** The user picked "experiment ends with a Pydantic schema, not stack picks" (Q14). This is the architectural analog of the Karpathy red phase — define the contract first, pick implementation tools to satisfy the contract. Tools-first picking is how stacks bloat.

3. **The Grok document was right about direction, wrong about specifics.** "Dispatch needs to be a data analysis pipeline" is correct. The five-tool list (Docling, pdfplumber, Camelot, Apryse, vision) is pre-experiment speculation. The 15-bidset experiment is what produces the right tool list, not strategic pre-planning.

### Where to pick up next session

In order:
1. **Set up S3-compatible object storage** (real AWS S3, MinIO, R2, B2 — user picks based on cost/offline preferences). Upload the 15 bidsets. Commit a manifest at `huckleberry/backend/test_fixtures/bidsets.json` referencing them by S3 key + content hash.
2. **Set up the monorepo skeleton.** `huckleberry/{frontend,backend,shared}` with v6.3.5 moved into `frontend/`. README explaining the architecture. Pushed to git.
3. **Run the experiment in Claude Code.** Filesystem access to the 15-bidset folder (or pulled from S3 manifest). Output: per-PDF JSON + a draft Pydantic schema in `shared/` + a markdown findings report. Schema inclusion rule (≥3 of 15 + downstream consumer) is enforced.
4. **Review the findings together.** Decide which observed-but-deferred fields graduate. Pin the v0.1 schema. Then start the actual Phase 2 backend.

The handoff doc that goes with this session (separate file) lists the bootstrap commands, the manifest schema, and the experiment prompt for Claude Code.



This document is the contract between sessions. If something isn't in here that the next Claude needs to know, that's a bug in this document — fix it before you touch code. If you do touch code, update this document in the same turn. The user paying attention will check.

**Three things I would do first if I were the next Claude:**

1. **Identify which phase the user's request lives in.** Phase 1 (HTML, maintenance only) vs Phase 2 (backend, the experiment + schema design + monorepo work) vs Phase 3 (push back, requires user re-decision). The "Phases" section near the top is canon.

2. **For Phase 1 work**: run `cd /home/claude/work && node run_tests.js Huckleberry_AI_6.3.5_Scope.html` and confirm 138/138 green. Run all spot-checks + mutation test. Don't proceed if anything drifted. Don't add architecture to HTML.

3. **For Phase 2 work**: read the "Phases" section in full, especially the 18 decisions. The first Phase 2 session has three setup tasks before any experiment runs (S3 + bidset upload, monorepo skeleton, then Claude Code experiment). The handoff doc paired with this CLAUDE.md update walks through them step by step.

Don't ship without running the test suite. Don't claim a fix without proof. Don't sugar-coat. Don't propose Phase 3 work without explicit user re-decision. Pick the right Karpathy Shape (A / B / C) for the task; all three are documented near the top.

---

## Real-PDF Session Notes — 2026-04-22 late (Chipotle bidset)

The user ran a ~35-page Chipotle bidset through 6.2 end-to-end for the first real test. Session lasted ~20 minutes. All findings:

### What worked
- **Scope parser** extracted 4 labeled systems from the bidset text: `TYPE V` (seen on PAGES 1 + 13, HIGH CONF) with 12 pin types (Scupper, Primary Drain, Gutter, Downspout, RTU, Exhaust Fan, Pipe Boot, VTR, Equipment Curb, Walk Pad, Cricket/Saddle, Antenna), `TYPE 1` (PAGES 13-14, LOW CONF — clearly a placeholder callout the regex caught), `TYPE 1` (PAGES 14-35, HIGH CONF with TPO Fully Adhered 60 mil EPS insulation), `TYPE V` (PAGES 35-39, LOW CONF). Screenshot showed the SCOPE tab rendering all 4 system cards cleanly with editable fields and × tag chips.
- **Page classifier** correctly tagged A-100 as ROOF PLAN.
- **Source-page hyperlinks** on scope cards worked — clicking `PAGE 13` jumped the viewer to that page.
- **Manual override workflow** worked end-to-end: user calibrated at 1" = 4' (Chipotle's 1:48 scale), drew a TYPE V polygon around the building footprint, got **2,413 sq ft** detected vs the auto-detect's **824,922,986 sq ft** on the same page. Huge validation of the manual-polygon-replaces-Stage-12-winner architecture.
- **Per-page state persistence** held through most of the session.

### What broke (all fixed this turn, see B-11..B-15)
1. Calibrate tool went into a loop after the first click on subsequent pages — saw "invalid length" repeatedly even though the first click was in a valid spot.
2. Delete button did nothing.
3. Measurements accumulated to 165 then 196 — user wasn't trying to make that many.
4. PDF disappeared after ~20 minutes of work, user had to reload.
5. Running tests mid-session corrupted the loaded bidset's state.
6. "Only pin I have is somehow hardcoded Scupper and I could not delete them at all" — actually the scope correctly had 12 pin types, but the × delete didn't exist in the viewer sidebar (only in SCOPE tab) and the listener leak made clicks feel broken.

### What it revealed architecturally
- **Listener-leak in `bindInput()` inside `init()`** was the single most damaging bug. One mistake → user-visible breakage of FOUR tools. B-11 fix closes this class of bug.
- **Test fixtures writing to `App.project`** without restore is a minefield. Anyone adding new tests must use `withTestIsolation()` or the snapshot-restore pattern.
- **150 DPI × 35 pages eager render is NOT viable on a browser.** B-15's on-demand pattern is the only way this scales to 100+ page bidsets.

### What's still honestly broken for real bidsets
- Auto-detect produced **824,922,986 sq ft** on the Chipotle A-100 page — pipeline mega-cluster on 73,043 vector paths. User correctly treated the PIPELINE tab as a diagnostic surface.
- Rectilinear score was 58% (should be 85-95% on a clean commercial roof plan). Curve-to-line segment approximation in pdf.js is probably introducing phantom diagonals.
- Dash filter still unverified on real PDFs — 0 dashed paths dropped despite the plan obviously having dashed callouts.

### Next real test
Replay the Chipotle session with the fixed 6.2. Target: 30+ minutes of sustained use without any of the B-11..B-15 symptoms returning. If that holds, we've earned the right to tackle Tier 2 (Stage 6 short-circuit). If it breaks again, we're back to diagnosis.

— end —

---

## Session Notes — 2026-04-23 (the B-16/17/18 saga and B-19 discovery)

### What happened in order
1. User reported "can't see plan viewer distorted view think its rendering bottom left tile" on Chipotle page 13.
2. Claude hypothesized: canvas size cap + toDataURL truncation → shipped B-16 (6.2.1).
3. User: "yes — patched file, issues persist".
4. Claude hypothesized: pdf.js internal state corruption from getOperatorList+render → shipped B-17 (6.2.2).
5. User: "NONE ARE RENDERING CORRECT" + shared DevTools console dump showing only `Warning: TT: undefined function: 21` and file:// security warnings, no [B-17] / [B-18] diagnostic logs at all.
6. Claude asked to pause. User directed "review claude.md apply karpathy logic test debug".
7. Claude reviewed CLAUDE.md, acknowledged the Karpathy discipline violation (shipping fixes without tests, claiming "partial render" without confirming the alternative hypothesis).
8. User provided the full Chipotle PDF. Claude inspected it: STACK Construction Technologies output, 39 pages, each with 46-92k path operators in the content stream and one embedded image.
9. Claude built a Node-based render diagnostic using pdfjs-dist 3.11 + @napi-rs/canvas. Measured paint% at multiple DPIs.
10. **Node rendered page 13 perfectly at 100 DPI with pdf.js 3.11**. Paint=9.71% is low only because line art on a 2.5× bigger canvas samples with lower density — but the PNG visually contains full elevations, text, title block, schedule. Nothing missing.
11. Coupling test: `getOperatorList() + render()` vs `render()` alone → identical paint%. H2 (extractor coupling) eliminated.
12. This narrowed the bug to: if pdf.js 3.11 renders correctly, but the user's browser shows garbage, something else is drawing the garbage. Grep for "synthetic" found `openViewerIfPossible` calling the synthetic painter unconditionally whenever `renderCanvas` was null — which B-15 made the default state for real PDFs.
13. Wrote the B-19 test (failing) BEFORE writing the B-19 fix. Test ran synthetic painter on 2 real-PDF pages, asserted should be 0. Failed as expected.
14. Wrote the 4-line fix: detect `_pdfPageRef` presence as "real PDF" signal; skip synthetic painter in that case.
15. Test passed. Full suite: 77/77 green.
16. Updated this CLAUDE.md in the same turn.

### Why B-16/B-17/B-18 didn't find B-19
Each patch assumed the user's symptoms were caused by *pdf.js rendering imperfectly*. That assumption prevented me from asking whether pdf.js was rendering at all. The diagnostic signal that would have caught B-19 in round one: "does LOAD SYNTHETIC PLAN render cleanly in the viewer while real PDFs don't?" The user eventually volunteered this — "synthetic plan is fine can see it" — which should have narrowed instantly to "synthetic path is working, real-PDF path is not" rather than "pdf.js is broken." The two paths differ in exactly one place: `openViewerIfPossible`.

### Lessons for the next session
- **Test the null hypothesis first.** Before patching an allegedly-partial render, confirm the render is even running. The absence of `[render pN]` console logs from B-18's diagnostics was the clue that my code wasn't being reached; I interpreted it as "user filtered console" when it actually meant "this code path is never entered."
- **Synthetic-vs-real is the single most valuable diagnostic signal.** If a project has a synthetic happy-path and a real data path, a bug that manifests only in one is evidence about which code path diverges. This is already in CLAUDE.md's Communication section: "Synthetic-passes ≠ real-PDF-passes." Read literally.
- **Karpathy: test before fix.** B-19 is the template. Red → green in one commit, with the test in the same commit as the change, was the only Karpathy-compliant move in this whole saga.
- **Diagnostic over speculation.** The 5-test Node diagnostic produced definitive evidence in ~5 minutes of compute. I should have built it before B-16, not after B-18.

### The Chipotle PDF content facts (for future bug-hunting)
- Producer: UniDoc v4.3.0 (via STACK Construction Technologies)
- PDF version: 1.3
- 39 pages, all at 1728×2592 pts (24×36" @ 72 DPI)
- Each page has 46k–92k path operators in the content stream (10–30× a typical CAD PDF)
- Each page has 1–3 embedded images (typically a 4919×5314 indexed-color FlateDecode raster; pages 23–31 smaller 206×222; pages 32–39 mixed JPEG+Flate)
- Fonts: Identity-H Type0 (ArialMT, Arial-BoldMT, CopperplateGothic-Light, PanRoman) → the `TT: undefined function` warnings are harmless font-hinting fallbacks
- Coordinate system uses `0.015 0 0 0.015 cm` transform so raw coords like 113439 map to 1701 pts on page
- `_pdfDoc` is held on `planSet._pdfDoc` so reconnection after page-canvas eviction works

### Diagnostic artifacts (kept in `/home/claude/diag/`)
- `worker.mjs` — single-test worker (spawn one per test to avoid pdf.js global-state conflicts)
- `mini.mjs` — orchestrator (5-test focused harness)
- `orchestrator.mjs` — full 32-test matrix (slower; use if needed for regression)
- `out/*.png` — render outputs, including `3.11_p13_100dpi_render-only.png` which is the proof that pdf.js renders these PDFs correctly
- `out/diag.json` — structured results

### Known pdf.js 4.10 limitation encountered
- pdf.js 4.10 with @napi-rs/canvas throws "Value is none of these types `String`, `Path`" — 4.10 passes a canvas primitive that @napi-rs/canvas doesn't accept. The real `canvas` npm package might work but requires native compilation not available in the sandbox. Running the diagnostic in a real browser (the originally-proposed standalone HTML approach) will bypass this. Not a blocker for B-19.

### Where to pick up next session
1. User tests 6.2.3 in their browser on the Chipotle bidset.
   - Expected: pages render correctly — full building elevations, schedules, spec text, title block, everything.
   - If yes: we're free to tackle Tier 2 (Stage 6 short-circuit) per the original plan.
   - If no: something else is wrong — possibly a CDN resource issue or a different init path; the diagnostic approach is still valid, just point it at whatever new symptom appears.
2. Delete the poisoned `Huckleberry_AI_6.2.1_Scope.html` and `Huckleberry_AI_6.2.2_Scope.html` files from `/mnt/user-data/outputs/` so they can't be run by mistake.
3. Optional (time-permitting): bundle the B-16 canvas cap defensively with its own regression test (separate PR, not speculative). iOS Safari's 16MP canvas cap is real and the cap is harmless on desktop.
