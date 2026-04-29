# CLAUDE.md — Huckleberry AI

**Single source of truth for Claude sessions working on Huckleberry AI.**
**Last updated:** 2026-04-26, end of architectural-realignment session
**Project owner:** Daniel. Non-developer. Speaks plainly. Demands brutal honesty, no sugar-coating, no flattery. Will say "Karpathy logic" when discipline is slipping and expect Claude to apply it.
**Read order before any work:** this document end-to-end, then the relevant phase's march-orders document if one exists, then the source artifacts the work touches. Karpathy procedure applies to discussions, not just code.

---

## SECTION 0 — Identity

### What Huckleberry is

Huckleberry AI is a **commercial-construction-takeoff platform**. It reads architectural PDF bid sets and produces structured, reviewable, auto-annotated takeoff data that an estimator approves and exports to Excel. The user is the general contractor (GC) who uploads bidsets and reviews the auto-annotations. The first trade module to ship is roofing. **The platform is multi-trade by design**, with glazing, siding, mechanical, plumbing, electrical, structural all consuming the same dispatch and geometry layers via a shared trade module interface.

### What Huckleberry is NOT

- Not "a roofing program." Roofing is the first trade module, not the platform.
- Not a frontend app with parsing in the browser. Frontend is review/edit/approve/export only.
- Not a one-shot extraction tool. The product is the auto-notation review loop where corrections become labeled training data.
- Not an LLM-driven extractor in Phase 2. Rule-based + reference-data-driven only. LLM is a Phase 3+ decision and currently deferred.
- Not a network-exposed multi-user service. Localhost-only during POC and v0.x. Auth, multi-user, public network exposure are Phase 3+.

### Sacred constraints

These do not change without explicit user re-decision:

1. **Phase 1 HTML must remain runnable standalone forever.** The v6.3.5 single-file offline-capable HTML is the manual-tools fallback. It survives every future architectural change. It does not consume the backend API.
2. **No AI API calls anywhere in Phase 2.** Rule-based logic and reference data only.
3. **Localhost-only during POC.** No public network exposure.
4. **Karpathy procedure is mandatory.** Read first → failing tests first → minimum implementation → 100% green floor → commit. The B-16/17/18 anti-pattern (speculation patches without diagnostic) is the named failure mode this discipline prevents.
5. **No fabricated validation.** A measurement requires a named evaluation set. Confidence numbers require a calibration procedure. "Validated against X" is only true if X was actually run through the pipeline.

---

## SECTION 1 — The Canonical Workflow (Locked)

This is the workflow Huckleberry implements. Every architectural decision must serve this flow. When something doesn't fit this flow, the something is wrong, not the flow.

```
GC uploads bidset PDF → backend (Python)
    ↓
backend ingests, dispatches, runs trade modules,
extracts scope, detects polygons, identifies scale,
produces auto-annotated structured data
    ↓
backend writes to database under job folder
    ↓
frontend pulls structured data from database
    ↓
user reviews on screen, edits, approves
    ↓
approved data → Excel takeoff workbook
    ↓
corrections → back to database as labeled training data
```

### Frontend's job (the only things frontend does)

1. Pull structured data for a job from the backend database
2. Display auto-annotations on screen (the three-state annotation: auto-proposed cyan, user-confirmed green, user-corrected green-with-delta-and-original-preserved)
3. Accept user edits, approvals, and rejections
4. Render the approved annotation set as Excel takeoff workbook
5. Send corrections back to the backend for storage as training data
6. Run the manual-tools workflow (calibrate, polygon, measure, pin, etc.) as the user's correction interface

### Backend's job (everything else)

1. PDF ingestion from GC upload
2. Dispatch gate processing — TracePoint Layer 3 / Filters 1–5 (**ported in v0.2**)
3. Filter pipeline — TracePoint Stages 2–5 (**not yet ported**)
4. Geometry engine — TracePoint Stages 6–9 (**not yet ported**)
5. Post-clustering scorers — TracePoint Stages 10–12 (**not yet ported**)
6. Trade modules — one per trade, all consume shared PlanSetContext + geometry (**not yet built**)
7. Per-trade scope extraction with position-based filtering inside the building polygon, per TracePoint paper §9 (**not yet built**)
8. Cross-trade relationships layer (e.g., RTU on roof connects mechanical and roofing scopes) (**not yet built**)
9. Auto-annotation proposal generation with provenance — what / where / how confident / why (**not yet built**)
10. Database write under job folder, GC as primary identity (**not yet built**)
11. Database read on frontend request
12. Storage of user corrections as labeled training data, paired with original auto-proposals (**not yet built**)

### Database structure (target)

- One folder per job
- GC is the primary identity / access key
- Folder contains: source PDFs (input), backend structured outputs (PlanSetContext, geometry, polygons, scale, per-trade scopes, auto-annotations, provenance), user corrections, approved final state, Excel exports
- Schema is PlanSetContext-shaped (TracePoint canonical) extended with job-level entities
- v0.1 BidsetRecord schema is retired during the realignment

---

## SECTION 2 — Current State (2026-04-26)

### Repository layout

```
huckleberry/
├── frontend/                  # Phase 1 — single-file HTML, manual tools, offline-capable
│   └── Huckleberry_AI_6.3.5_Scope.html  (138/138 mutation-tested)
├── backend/                   # Phase 2 — Python, FastAPI + SQLAlchemy + Postgres + Pydantic
│   ├── core/                  # Ported TracePoint code
│   │   ├── config.py          # v0.2 verbatim
│   │   ├── pdf_engine.py      # v0.2 verbatim
│   │   ├── zone_filter.py     # v0.2 verbatim
│   │   ├── context.py         # v0.2 verbatim
│   │   └── dispatch_gate.py   # v0.2 verbatim + 3 same-character import edits
│   ├── seeds/                 # Reference data
│   │   ├── roofing_materials.py        # Phase 2's 21-item ROOFING_SEED_ITEMS + ROOFING_CONSTANTS
│   │   ├── roofing_spec_database.py    # TracePoint port (data/roofing_materials.py renamed)
│   │   ├── roof_assemblies.py          # 40-component database, currently NO consumer
│   │   ├── glazing_assemblies.py       # parked, NO consumer
│   │   └── glazing_materials.py        # parked, NO consumer
│   ├── tests/
│   │   ├── test_pdf_engine.py    # 40/40 v0.2 ported
│   │   ├── test_dispatch.py      # 34 unit + 19 skipped integration
│   │   └── test_seeds_load.py    # v0.1 baseline, 5/5
│   ├── scripts/
│   │   ├── run_dispatch_on_15_bidsets.py         # STACK sweep
│   │   ├── run_dispatch_on_public_corpus.py      # 4 non-STACK bidsets
│   │   ├── intake_diagnostic.py                  # Pass 1 read-only
│   │   ├── intake_diagnostic_pass2.py            # Pass 2 context inspection
│   │   └── compare_v0.1_to_v0.2.py
│   ├── test_fixtures/
│   │   ├── v0.2_outputs/                         # 15 STACK PlanSetContext JSONs
│   │   ├── public_corpus_outputs/                # 4 non-STACK JSONs (gitignored)
│   │   ├── intake_diagnostic_outputs/            # 19 per-page CSVs (gitignored)
│   │   └── intake_diagnostic_summary.json
│   ├── V0_2_VALIDATION.md             # symptom validation against v0.1
│   ├── PUBLIC_CORPUS_OBSERVATIONS.md  # uncommitted
│   ├── INTAKE_DIAGNOSTIC.md           # Pass 1 — uncommitted
│   ├── INTAKE_DIAGNOSTIC_PASS2.md     # Pass 2 — uncommitted
│   └── DISCOVERED_ISSUES.md           # D-1 through D-5
├── shared/                    # Wrapper schema between frontend and backend
│   └── bidset_record.py       # v0.1 — to be retired in v0.2.1 schema migration
├── STEP_17_REVIEW_CHECKLIST.md
├── STEP_18_DECISION_BRIEF.md
├── MARCH_ORDERS_v0_2.md       # historical, sealed
└── CLAUDE.md                  # this file
```

### Phase 1 status

**Closed at v6.3.5.** 138/138 tests green, mutation-tested, browser-verified. Manual toolchain mature. Single-file HTML, offline-capable, runs in Chrome with no backend dependency. Contains in JavaScript: ROOF_VOCAB scope parser, ROOFING_SEED_ITEMS palette, dispatch gate filters (partial port of TracePoint Stage 1), four-gate filter pipeline (Stages 2–5), union-find clustering (Stage 6), five-tier scale determination (Stage 7), post-clustering scorers (Stages 10–12). The frontend explicitly documents that the architect-profile flywheel, symbol diagnostic, and hatching diagnostic are intentionally NOT in the browser — "the depth of plan-set intelligence is intentionally trimmed to fit a browser."

The Phase 1 HTML is the offline fallback per sacred constraint. It does not consume the backend API and will not. Bug fixes and UX polish are allowed; new architecture is not.

### Phase 2 status

**v0.2 shipped on branch, not pushed.**
- Branch: `phase2-v0.2-dispatch-port`, HEAD `441896a`
- 35 files, +7389 / −1
- 250 tests across all suites green (138 Phase 1 + 38 Phase 2 v0.1 + 40 ported test_pdf_engine + 34 ported test_dispatch unit), 19 skipped, 0 failed
- The verbatim port held end-to-end. Three §7 stops (D-1 ~ D-3) handled correctly; all resolved. Final dispatch_gate.py diff vs TracePoint: 3 lines, all same-character.
- Discipline observation: v0.2 ported only TracePoint Layer 3 (the dispatch gate / Filters 1–5). Stages 2–12 of the TracePoint pipeline are NOT in the backend. This is acknowledged in Section 4 below as the trigger for the architectural realignment.

**v0.2.1 — pre-scoped, NOT started.** Schema migration (BidsetRecord → PlanSetContext, consumer surface = 1 file), D-4 (`PlanSetContext.to_json()` does not serialize `project`), D-5 (Hampshire title-block fallback hardening). All scoped in `STEP_18_DECISION_BRIEF.md`.

### Diagnostic results from this session

**Public-corpus observation sweep** (4 non-STACK bidsets, uncommitted):
- 4/4 dispatch_complete, 0 crashes, 0/4 detected_system, all empty scope_pages
- The verbatim port is robust across PDF producers (Adobe Acrobat/AutoCAD plus three Bluebeam variants)
- Hampshire-style sheet propagation did NOT reproduce on non-STACK PDFs

**Intake Diagnostic Pass 1** (19 bidsets read-only against v0.2 outputs, uncommitted):
- 11 of 15 STACK bidsets had positive manufacturer evidence; only 1 (Taco Bell) had non-empty scope_pages
- Surfaced an asymmetry that LOOKED like the gate was leaving signal on the floor

**Intake Diagnostic Pass 2** (context inspection of 35 manufacturer hits, uncommitted):
- 29 of 35 hits were manufacturers in non-roofing contexts (sealants, drywall, ceiling insulation, electrical conduit) — the same name appears in the seed because the company makes roofing AND other products
- 0 of 35 hits had Division 7 spec-section reference within 200 chars
- 1 of 35 hits was in a negation context (Shoppes "Firestone NOT ACCEPTABLE")
- The asymmetry largely dissolves: the dispatch gate correctly rejected non-roofing-context mentions
- The remaining 5–6 explicit-roofing-context hits that did NOT detect scope are the next-level question

**Shoppes-at-Avalon page-by-page read** (in this session's conversation):
- 97 pages, STACK-produced, 3 outparcel buildings bundled in one PDF
- ~25–30 pages rasterized (zero text extraction)
- Real roofing scope: 60 mil TPO Carlisle (Firestone/Duro-Last NOT acceptable), R-30 polyiso, B22 metal deck (only on rasterized structural sheets), parapet with metal coping, scuppers and emergency overflow, multiple RTU penetrations, standing-seam awnings (distinct from main roof system)
- Surfaced 8 concrete extraction requirements (multi-building boundary detection, OCR on rasterized pages, negation context, spatial clustering of text into blocks, multi-evidence synthesis, per-trade vocab including cross-trade penetrations, primary vs secondary system distinction, title-block-region positional sheet extraction)
- Most of these are addressable by porting the rest of TracePoint plus building the trade module layer

---

## SECTION 3 — The 18 Ratified Phase 2 Architectural Decisions

These were ratified 2026-04-25 as the architectural foundation of Phase 2 and remain canon:

1. **Frontend stays single-file HTML, offline-capable, no AI API.** Sacred. The v6.3.5 standalone HTML is preserved as the manual-tools fallback forever.
2. **Backend is Python.** FastAPI + SQLAlchemy + Postgres + Pydantic. Heavy parsing, dispatch, geometry, scope extraction all happen here.
3. **No LLM in Phase 2.** Rule-based + reference-data-driven only. LLM is a Phase 3 decision.
4. **Localhost-only during POC.** No public network exposure during v0.x.
5. **Save-on-button-press, not real-time sync.** Frontend works in memory like Phase 1 (fast, instant, no network chatter during drawing). Explicit "Save" button POSTs the annotation set to the backend.
6. **Frontend wins, backend keeps provenance trail.** When the user edits a parser-extracted field, the user's value is canonical in the JSON. The backend records what the parser originally proposed alongside the user's correction. Every correction becomes labeled training data.
7. **Reference data lives in Python files.** Backend imports `seeds/*.py` as modules at startup. No separate JSON or YAML configuration. The Python file IS the source of truth.
8. **Four reference layers.** Dispatch (which page is what), materials (what products exist), assemblies (how they go together), and the eventual trade-module-specific overlays. This is the conceptual structure of the seeds folder.
9. **Backend imports the .py seed files as live consumers.** This closes the manual-mirroring drift documented as the v6.3.2 Duro-Last anti-pattern. The frontend's vocabulary CAN drift independently for now; the long-term path is a single source of truth in Python with the frontend deriving from backend output.
10. **Postgres for backend persistence.** Job folders, structured outputs, training data deltas.
11. **`BidsetRecord` includes provenance from day one.** Every populated field carries origin (which page, which region) and confidence. This is what makes the auto-notation product loop possible.
12. **Step 12 (manufacturer dropdown) abandoned.** Manufacturer detection is rule-based via the seeds, not user-selected.
13. **No frontend rebuild during Phase 2.** The v6.3.5 frontend stays. A new API-driven frontend gets built during the realignment Phase E, but that's separate from this list.
14. **Experiment success = Pydantic schema + findings report.** v0.1 experiment shipped exactly this.
15. **The vault rule.** From TracePoint paper §7.5: the debug module must not be modified in the same session that modifies core pipeline files. Adopted as Huckleberry-wide for any diagnostic instrumentation, including trade modules.

    **Trade-module application (2026-04-28).** Trade modules ship "rough" — best-effort first pass against the contract, with vocabulary and logic that's reasonable but not fine-tuned against real bidsets. They get vault-ruled at the end of their rough-ship phase. After vault-rule application, the module is frozen as a stable observer/extractor in the same status as TracePoint's debug module relative to its core pipeline. Future fine-tuning happens in separate sessions where the module is the editing target and the rest of the pipeline is frozen, OR in completely new module versions, not by silently editing the frozen one.

    **Reason.** Rough modules are diagnostic surfaces. We learn what they get right and what they get wrong by running them against real bidsets and observing outputs. If they are tuned in the same session that we learn their behavior, prior diagnostic findings become stale and the module loses its value as a stable observer of what the pipeline produces.

    **Vault-ruled retroactively (2026-04-28):**
    - `backend/core/roofing_module.py` (C.2 commit `74772b6`)
    - `backend/core/roofing_vocabulary.py` (C.2 commit `74772b6`)
    - `backend/core/glazing_vocabulary.py` (C.3b commit `14f4f53`)

    **Vault-ruled at sealing (2026-04-28):**
    - `backend/core/glazing_module.py` (C.3c-build sealing commit on branch `phase2-v0.3-C3c-glazing-module`) — first Huckleberry-original trade module; rough-ship per Daniel's 2026-04-28 spec (verbatim in `MARCH_ORDERS_C_3c_build.md` §1). Module docstring lists known limitations explicitly. Behavior validation deferred to the C.3c-run sweep (separate phase).
    - `backend/core/debug_module.py` (C.5 partial-port sealing commit on branch `phase2-v0.3-C5-debug-module-port`) — TracePoint debug-module port, the original vault-rule subject from TracePoint paper §7.5. Sections 1 (dispatch health), 3 (page intelligence), 6 (legend contents + quality flags) ported verbatim from TracePoint source SHA-1 `b5a4cf93ca7c02116fc00f6dc5a1514da1b18b60`. Sections 2 (scale comparison), 4 (cross-reference graph), 5 (geometry diagnostics) stubbed pending external state per `backend/DEBUG_MODULE_REPORT.md` (scale-engine route, networkx + sheet-index, geometry results respectively). C.5 partial port; vault rule applies to all six sections, stubbed and ported alike. Tuning of sections 1/3/6 happens in dedicated sessions with `core/` frozen. Unstubbing of sections 2/4/5 is a future phase decision (D/E).

    **Vault-ruled when sealed:** every future trade module.

    **Tuning sessions** are dedicated, separate from `core/` work, with the relevant module as the only editing target and `core/` files frozen. Tuning of a vault-ruled module in the same session that touches the core pipeline is the named anti-pattern this rule prevents.

    **Contract evolution.** The trade module Protocol and the `TradeFieldValue` / `TradeModuleInput` / `TradeModuleOutput` dataclasses CAN be extended additively (as `TradeModuleInput.tables` was extended in C.3b commit `7ea9abb`) when multi-trade reality requires it. The vault rule applies to module behavior, not to contract evolution.
16. **Karpathy procedure is mandatory.** Read first → failing tests first → minimum implementation → 100% green floor → commit. The B-16/17/18 anti-pattern is the named failure mode this discipline prevents.
17. **Sacred files held every gate.** Phase 1 HTML, Phase 2 v0.1 backend, ported TracePoint files, seed files. Modifying sacred files requires explicit user approval at a phase gate, not in-session.
18. **Diagnostic-first development.** TracePoint paper §3.1, §8.1: every major feature follows the same pattern — write a diagnostic script first, run it across the corpus, report findings, only then write production code. Adopted Huckleberry-wide.

---

## SECTION 4 — Architectural Realignment (2026-04-26)

This section captures the realignment Daniel triggered by re-reading the TracePoint paper.

### What was named

The current state has three architectural mistakes baked in that this realignment corrects:

**Mistake 1: Frontend was doing platform work it shouldn't.** The v6.3.x frontend HTML contains in JavaScript: dispatch gate filters, the four-gate filter pipeline, union-find clustering, five-tier scale determination, post-clustering scorers, ROOF_VOCAB scope extraction, polygon area calculation. This was Phase 1's offline-first POC architecture. It was correct AS A POC. It is NOT correct as the production architecture.

**Mistake 2: v0.2 ported only the dispatch gate, not the whole pipeline.** The TracePoint paper documents a 12-stage pipeline. v0.2 ported Stage 1 verbatim and explicitly stopped there per the original march orders. Stages 2–12 are NOT in the backend. Auto-notation product quality requires the full pipeline because TracePoint paper §9 describes scope extraction as requiring position-based filtering of text blocks INSIDE the building polygon — and the building polygon comes from Stages 6–12.

**Mistake 3: The platform has been treated as roofing-shaped.** Multiple recent Claude sessions framed Huckleberry as "roofing first, extend later." The TracePoint paper §2.1 is explicit: "Layers 1–3 are trade-agnostic. A roofing module, an electrical module, and a structural module all consume the same PlanSetContext and geometry results." The frontend already has disabled UI cards for glazing and siding. The seed files glazing_assemblies.py and glazing_materials.py exist with no consumer.

### What the realignment establishes

- The canonical workflow in Section 1 is locked.
- Multi-trade is foundational, not an extension.
- The phased recovery path (Section 5) governs how the backend gets back to TracePoint-faithful + multi-trade.
- The hard guardrails (Section 6) prevent backsliding.

---

## SECTION 5 — Phased Recovery Path

These phases are gated. Each is its own march-orders document with sacred files, DO-NOT sections, Karpathy procedure. None of these phases starts without Daniel's explicit approval. Each completes (with all sacred floors held and tests green) before the next begins.

### Phase A — Close v0.2 properly

**Status:** Pre-realignment cleanup. Does not depend on the realignment but unblocks it.

**Work:**
- Push v0.2 (commit `441896a` on branch `phase2-v0.2-dispatch-port`) to remote
- Ship v0.2.1 as already pre-scoped in `STEP_18_DECISION_BRIEF.md`:
  - D-4 (`PlanSetContext.to_json()` serialization gap)
  - D-5 (Hampshire title-block fallback hardening — keep scoped narrowly)
  - Schema migration: BidsetRecord → PlanSetContext as canonical
- Commit the public-corpus observation work and the intake diagnostic work to a separate observations branch (or fold into v0.2.1 paperwork)

**Output:** v0.2.1 shipped, v0.2 pushed, observation work archived.
**Sacred floors:** 250 / 19 / 0 maintained.

### Phase B — Port the rest of TracePoint to backend

**Status:** Largest phase. 4 sub-phases, each with its own march orders. **If Daniel chooses, he can place a copy of the TracePoint folder in the project tree so Claude Code reads dispatch and 12-stage pipeline source directly during ports — same pattern as the v0.2 march orders read from `C:/TracePoint/`.**

**B.1 — Port Stages 2–5 (filter pipeline) verbatim.** Zone mask, weight filter, length filter, dash filter. Source: TracePoint's filter gate code. Target: `backend/core/filter_pipeline.py` or split per-gate. Discipline: same as v0.2's verbatim port. Tests: per-gate unit tests verbatim from TracePoint.

**B.2 — Port Stages 6–9 (geometry engine) verbatim.** Union-find clustering at 0.5-inch proximity, 50 sq.in. minimum filter, five-tier scale determination, perimeter cleanup, confidence scoring. Source: `tracepoint_port/TracePoint/core/geometry_matrix.py`. Target: `backend/core/geometry_matrix.py` (source filename preserved). Discipline: verbatim. Adds backend dependencies: `opencv-python`, `numpy`, `shapely`, `Pillow`. The L-shape / T-shape user-polygon override that the frontend implements does NOT come over — that's a frontend UX concern.

**B.3 — Port Stages 10–12 (post-clustering scorers) verbatim.** Interior density (callout density 0.06, long-text ratio 0.5, noise-zone overlap), rectilinear, final selection. Empirical thresholds come over verbatim — they were calibrated on 113 candidate polygons across 15 bid sets. Target: `backend/core/scorers.py`.

**B.4 — Port architect-profile system and storage layer verbatim.** Activates the `storage` argument that v0.2 gated to None (architecturally — actual activation in `run_dispatch()` calls is deferred to a later phase). Cover-page parsing for architect firm detection, per TracePoint paper §8.6 ("real architect extraction needs cover-page parsing, not title-block keyword matching"). Source files (3): `tracepoint_port/TracePoint/core/architect_profile.py`, `core/storage.py`, `core/correction_store.py`. Targets: `backend/core/architect_profile.py`, `backend/core/storage.py`, `backend/core/correction_store.py`. Tests: `backend/tests/test_architect_profile.py`. All four files port verbatim — `diff = 0` against TracePoint source. SQLite cache path preserved at `~/.tracepoint/cache.db` per TracePoint convention. Postgres / multi-tenant database work is deferred to Phase D where it belongs architecturally.

**Phase B output:** backend can process a PDF end-to-end through the full TracePoint 12-stage pipeline, producing a complete `PlanSetContext` with geometry, polygons, scale, scoring, and (optionally) cached storage with architect profile.

### Phase C — Trade module foundation

**Status:** Multi-trade platform takes shape. TracePoint paper §9 explicitly names this as future work; we're building it.

**C.1 — Port the trade module Protocol verbatim, capture cross-trade integration cases.** TracePoint's `core/trade_module.py` is already the design Daniel's C.1 design pass would have produced — a Protocol (`TradeModule`) plus three dataclasses (`TradeFieldValue`, `TradeModuleInput`, `TradeModuleOutput`) defining the platform/trade boundary. C.1 ports that file verbatim (`diff = 0` against TracePoint source) into `backend/core/trade_module.py`, and adds `backend/CROSS_TRADE_INTEGRATION_NOTES.md` covering the four obvious cross-trade interactions TracePoint's single-trade contract does not address (RTU/roofing↔mechanical, storefront/glazing↔roofing, siding↔roofing transition, structural-deck↔roofing). The appendix names the interactions, the info each side needs, and which phase decides — it is not the C.4 architecture document. No tests in C.1 (TracePoint has no `test_trade_module.py`; the Protocol is exercised by concrete modules, starting in C.2). No registration mechanism, no `build_trade_input()` — those land in C.2 when the first concrete trade module (roofing) needs them.

**C.2 — First trade module: roofing.** Built against the C.1 contract. Reuses `seeds/roofing_spec_database.py` and `seeds/roof_assemblies.py`. Position-based filtering: text blocks are filtered to inside the building polygon before scope extraction, per TracePoint §9.

**C.3 — Second trade module: glazing.** Built against the same contract. Uses `glazing_assemblies.py` and `glazing_materials.py`. Validates the contract generalizes.

**C.4 — Cross-trade relationships layer.** Reads outputs of multiple trade modules. Surfaces dependencies (RTU on roof connects to mechanical and roofing scopes; storefront meeting parapet connects to glazing and roofing scopes). TracePoint paper does not cover this — it's a Huckleberry extension to support the auto-notation product.

**Phase C output:** backend takes a PDF and produces trade-aware structured scope per building, with cross-trade relationships, ready to feed auto-notation.

### Phase D — Database and job folder structure

**Status:** Possibly parallel with C.

**Work:** Job folders per project, GC as primary identity. Schema work: extend PlanSetContext to a job-level entity supporting multiple bidsets per job, multiple buildings per bidset (Shoppes-at-Avalon multi-parcel pattern), GC ownership. Database technology decision (SQLite per-job or PostgreSQL multi-tenant) at phase start.

### Phase E — Backend API for frontend consumption

**Status:** Wires Phases B/C/D to the user.

**Work:** Backend exposes API endpoints. Frontend stops doing parsing — ROOF_VOCAB, the geometry engine, the dispatch gate filters all stop running in the browser. Frontend pulls structured data from the API, surfaces it for review, accepts edits, sends corrections back. Manual tools (calibrate, polygon, measure, pin) remain in frontend — they're how the user CORRECTS auto-annotations. Excel export remains in frontend (it operates on approved annotation state). Phase 1 v6.3.5 standalone HTML remains as offline fallback per sacred constraint.

### Phase F — Auto-notation product

**Status:** Cannot start before A through E.

**Work:** Three-state annotations (auto-proposed cyan, user-confirmed green, user-corrected with original preserved). Provenance shown to user (what value, where on which page in which region, how confident, why this rule fired). Corrections captured as training data. Excel rendered from approved state, not from raw auto-proposals. Confidence model that estimators trust (corroborated > single-source > inferred > guessed).

---

## SECTION 6 — Hard Guardrails

These are not suggestions. They are hard constraints. Violating any of them is grounds for stopping and asking Daniel.

### Phase discipline

1. **No phase starts without Daniel's explicit approval.** The phases above are a recovery path, not an execution plan. Each is gated.
2. **Phases are sequential except where this document explicitly says they can parallelize.** Don't start B before A. Don't start C before B. Don't start F before A through E.
3. **Each phase produces its own march-orders document.** Same shape as `MARCH_ORDERS_v0_2.md`: numbered steps, DO-NOTs, sacred files, gated execution.
4. **Each phase has its own pre-flight gate.** Sacred floors verified, dependency surface understood, constraint list reviewed before any code lands.

### Verbatim-port discipline

5. **Phases B.1, B.2, B.3, B.4 are verbatim ports.** Not improvements, redesigns, or "tidying up." Same character as v0.2. `diff` against TracePoint source must show only required edits (typically import paths). The line 1233 `getattr(tb, "text", "") or getattr(tb, "content", "")` fallback in dispatch_gate.py is the template — preserved exactly because it solves a real problem the original researcher identified.
6. **If Daniel places a TracePoint folder copy in the project tree, that becomes the source of truth for verbatim ports.** Claude Code reads from it. No making up code. No "I think this is what TracePoint probably looks like."
7. **TracePoint's calibrated thresholds are NOT to be retuned.** Density 0.06, long-text ratio 0.5, proximity 0.5 inches, 50 sq.in. minimum, 1.0 pt heavy-line cutoff — calibrated empirically on 113 polygons across 15 bid sets. Retuning them on a new corpus is forbidden in the verbatim-port phases. If retuning is genuinely needed, it's a separate phase with its own march orders.

### Frontend discipline

8. **Frontend stops being a parsing engine.** No new ROOF_VOCAB extensions. No new dispatch logic in JavaScript. No geometry engine work in JavaScript. The frontend's existing pipeline section (HTML lines ~1681+) becomes documentation of what the backend now does, after Phase E.
9. **The Phase 1 v6.3.5 standalone HTML stays untouched as the offline fallback.** Sacred. The realignment is about the PRODUCTION frontend, not the POC fallback.
10. **No new manual mirroring of vocab from Python into HTML.** The v6.3.2 Duro-Last anti-pattern is closed by making the backend the only consumer of seed files going forward.

### Multi-trade discipline

11. **The trade module interface is designed before any trade module is built (Phase C.1 before C.2).** The interface is designed for multi-trade from day one, not retrofitted after roofing ships.
12. **Roofing is not the platform. Roofing is the first trade module.** Any framing that says otherwise is wrong and should be corrected.
13. **`glazing_assemblies.py` and `glazing_materials.py` are NOT abandoned.** They are queued for Phase C.3.

### Database discipline

14. **GC is the primary identity for job folders.** Not the bidset, not the project, not the architect.
15. **One job per folder.** A job is the unit of GC engagement. Multiple bidsets per job allowed. Multiple jobs per GC allowed.
16. **Source PDFs stay in the job folder.** Inputs, not derived data. Not committed to the code repository (gitignored). Backend reads from the job folder.

### Discovery and diagnostic discipline

17. **Read first applies to architectural conversations as much as code.** Every architectural conversation begins by reading the relevant authoritative documents (TracePoint paper, this CLAUDE.md, the prior phase's march orders) before proposing.
18. **Diagnostics before production code.** TracePoint paper §3.1.
19. **Calibrate from data, not intuition.** TracePoint paper §8.5.
20. **Honest non-conclusions.** Every diagnostic and observation document records what it cannot conclude as well as what it can. Sample size limits, ground-truth absence, corpus characteristics.

### Anti-patterns to refuse

21. **No "while we're in there" scope expansion.** Even if a fix is small, even if it's obvious, it goes in its own ticket if it's outside current phase scope.
22. **No fabricated validation.** "Validated against X" requires X actually run through the pipeline. Quality scores without an evaluation set are not measurements.
23. **No threshold tuning on STACK-only or public-archive-only corpora.** Tuning waits for the supplier-sourced non-STACK corpus that is incoming. Tuning is a separate phase even after that corpus arrives.
24. **No Pydantic schema "improvements" from outside sources.** Schema decisions are driven by TracePoint canonical structure (PlanSetContext) and Phase D's job-aware extensions. External proposals (e.g., the v3.5 BidsetRecord schema from a previous side conversation) are not imported.
25. **No silent pivots.** When a march orders document is ambiguous or incomplete, stop and ask. The §7 stop pattern from v0.2 is the model.

### Stop conditions

26. **If a phase's gate doesn't pass, the phase doesn't ship.** Floor is 100%, with deliberate skips allowed only for documented reasons.
27. **If sacred floors regress, work stops until the regression is understood.** Phase 1 138/138, Phase 2 v0.1 38/38, v0.2 ported tests 40+34, baseline 250 / 19 / 0. Each phase's gate restates the floor.
28. **If Daniel says "stop," stop.** Don't continue "to a clean stopping point." Don't finish "what's queued." Stop, summarize state, await direction.

---

## SECTION 7 — Discovered Issues Register

| ID | Status | Summary | Resolution |
|---|---|---|---|
| D-1 | RESOLVED Step 15 | test_dispatch.py module-level import blocks Step 13 unit-test gate | Dissolved when dispatch_gate.py landed in Step 15 |
| D-2 | RESOLVED Step 16 Pt 1 | Third `data.roofing_materials` import on line 1359 (not in march orders' edit list) | Same-character third edit applied |
| D-3 | RESOLVED Step 17 | `STEP_17_REVIEW_CHECKLIST.md` not on disk; lived in chat artifact | Daniel placed the file in repo tree |
| D-4 | DEFERRED to v0.2.1 | `PlanSetContext.to_json()` does not serialize `project` (verbatim-port consequence — TracePoint itself doesn't either) | Smallest fix: extend `to_json()` body in `core/context.py` |
| D-5 | DEFERRED to v0.2.1 | Hampshire title-block fallback propagates "N19A" to 7 pages | Title-block fallback hardening; scope narrowly per Daniel |

---

## SECTION 8 — Communication With Daniel

- **Brutal honesty, no sugar-coating, no flattery.** Daniel will say so when he wants something. Do not soften delivery.
- **Push back when you disagree.** The best moments in recent sessions were correct disagreements. Agreement-with-everything is the failure mode.
- **"Karpathy logic"** is Daniel's signal that discipline is slipping. When invoked, stop, re-read CLAUDE.md, re-read the relevant authoritative documents, restart the conversation from a measured position.
- **"Continue"** is Daniel's resume signal between sessions. It means: pick up from the last gate report's "AWAITING APPROVAL" line.
- **Reports follow the v0.2 gate-report format.** Files Changed / Files Not Changed / Tests / Discipline Checks / Sacred Floors / Karpathy Discipline / Next Step / Awaiting Approval.
- **If the conversation drifts toward fabricated validation, schema expansion from outside sources, or roofing-only framing, name the drift and correct it.** Daniel will reinforce the correction.
- **No bullet points or emojis in casual replies.** Match the conversational register.
- **End on what Daniel decides next, not on what Claude proposes.** "Standing by" is the right closing.

---

## SECTION 9 — Discipline Lessons Codified

These are session-derived lessons that have generalized into project doctrine:

**The B-16/17/18 anti-pattern.** Three consecutive speculation patches shipped without tests, attacking the wrong layer. Every patch assumed pdf.js was rendering imperfectly when the actual question — "is pdf.js rendering at all?" — would have surfaced the bug instantly. Diagnostic before production code; test before fix; architecture over incremental patches.

**Synthetic-passes ≠ real-PDF-passes.** TracePoint paper §4.1: 0% error on synthetic plans, catastrophic failure on real PDFs. The v0.2 STACK validation reproduced the same pattern at the dispatch-gate layer. Always validate against real data; synthetic is a unit-test surface only.

**Null signal misreading.** B-19's root cause was a null-canvas being misread as "synthetic plan" by a code path that should have detected real-PDF state via `_pdfPageRef` presence. Signals must be unambiguous.

**Single-eval scoping.** The Node.js test harness requires concatenating all script blocks into a single `eval()` call to avoid `const` re-declaration errors across separate evaluations.

**Scope precedence is load-bearing.** Re-scan must never overwrite user edits. seed < parsed < user ordering must be preserved at all composition points.

**The fork-stub-audit pattern.** TracePoint paper §8.7. When code moves, its prior location must be deleted in the same commit, not left as a placeholder. Foundation forks; tools rebuild; garbage gets documented and left behind.

**Two-gate fork.** When extracting code before stubbing during a fork, execute as two gates so extraction risk and stubbing risk are isolated. The one-variable-at-a-time rule applied at architectural level.

**Calibrate from data, not intuition.** TracePoint paper §8.5. Initial estimates of density 0.04 / long-text 0.3 were misaligned. Empirical calibration on 105 polygons gave 0.06 / 0.5. The data sets the threshold.

**Don't fabricate validation.** A measurement against an evaluation set is only a measurement if the evaluation set was actually run. Confidence numbers without a calibration procedure are confidence theater.

**Diagnostic before action.** Pass 1 of the intake diagnostic surfaced an asymmetry that LOOKED actionable. Pass 2 contextualized it and largely dissolved the action case. Without Pass 2, we'd have written march orders for the wrong thing. When data points toward action, run the cheap follow-up before committing to the action.

**Read the full primary sources.** The v0.2 → realignment trigger was Daniel re-reading the TracePoint paper and identifying the gap between what was ported (Layer 3) and what TracePoint described as the full pipeline (Layers 1–3 + Stages 6–12 + trade modules). I missed this until Daniel pointed it out. Future sessions: read the TracePoint paper end-to-end before scoping any architectural work that touches TracePoint-derived code.

**The Postgres-adaptation reversal (2026-04-27).** A bookkeeping pass on this date added language to §5 B.4 calling for `storage.py` to be ported with adaptation (SQLite → Postgres + Alembic migration) as a §7-style deviation. Daniel reversed that decision the same day before B.4 execution: SQLite stays verbatim. The reversal is recorded here because the conversation that produced the original adaptation was not wrong (Postgres IS Huckleberry's backend persistence per Decision 10), but the layering was wrong — backend cache for dispatch/profile is one concern (local SQLite, fine), multi-tenant job-folder Postgres is a different concern (Phase D). Decisions can be reversed cleanly when the layering analysis improves; this is the canonical example.

---

## SECTION 10 — How to Use This Document

**For future Claude sessions:**

1. Read Section 0 to understand identity.
2. Read Section 1 to understand the canonical workflow.
3. Read Section 2 to understand current state.
4. Read Section 3 to understand the architectural decisions you cannot override.
5. Read Section 4 to understand the realignment that's in progress.
6. Read Section 5 to understand the phased path forward.
7. Read Section 6 to understand the hard guardrails.
8. THEN read whatever march-orders document or source artifact the work touches.

**For future Claude Code execution:**

The phases in Section 5 are not march orders. Each phase requires its own march-orders document drafted by extended-thinking Claude with Daniel's review. Do not begin a phase from this document alone.

**For future architectural conversations:**

The canonical workflow in Section 1 is the spine. Any proposed change must serve it. Changes that don't serve it are wrong, not the workflow. The discipline is to refuse drift back toward "frontend does parsing" or "Huckleberry is roofing-only," even when the drift seems incremental and reasonable.

**On the TracePoint folder copy:**

Daniel can place a copy of the TracePoint project folder in the working tree if needed for Claude Code to read source during verbatim ports. If that happens:
- The folder is read-only reference (gitignored)
- Verbatim ports read FROM it; nothing in it is modified
- The folder is the authoritative source for Phase B verbatim work
- When the folder is removed, the verbatim work is sealed and remains in the Huckleberry backend

This is the same pattern v0.2 used with `C:/TracePoint/` as the read-only canonical source.

**On removing the prior CLAUDE.md files:**

This document supersedes:
- `CLAUDE.md` (Huckleberry, v6.2.3 era, dated 2026-04-23) in `/mnt/project/`
- `CLAUDE.md` (TracePoint upstream paper's project file) in `/mnt/user-data/uploads/`

Both can be removed. Their content is either superseded by this document or preserved in the TracePoint AI Research Paper and the v0.2 march orders / V0_2_VALIDATION.md / DISCOVERED_ISSUES.md artifacts.

---

**End of CLAUDE.md. Phase A may begin when Daniel approves.**
