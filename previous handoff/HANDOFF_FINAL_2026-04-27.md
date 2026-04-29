# Huckleberry AI — Handoff Document

**Date:** 2026-04-27, end-of-day
**Author:** Claude Opus 4.7 (extended-thinking, this session)
**For:** Next Claude session
**Supersedes:** all prior handoffs (`HANDOFF_2026-04-26.md`, `HANDOFF_v3_2026-04-27.md`, `CLAUDE_MD_ADDENDUM_2026-04-26.md`). This is the only handoff that matters going forward.

**Read order before any work:**
1. This handoff (you are here)
2. `CLAUDE.md` — single source of truth, ratified canon
3. `VALIDATION_LEDGER.md` — empirical proof of what's been validated; quote it instead of re-litigating
4. The relevant march-orders document if a phase is mid-execution
5. The TracePoint research paper if architectural questions arise
6. Source artifacts the work touches

---

## SECTION 1 — What you are walking into

You are picking up a project that just finished Phase B. The backend now contains a full TracePoint port: dispatch gate (Layer 3), filter pipeline (Stages 2–5), geometry engine (Stages 6–9), post-clustering scorers (Stages 10–12), and the architect-profile flywheel + storage + correction_store. 2,354 lines of verbatim port across four sub-phases (B.1 through B.4) plus the v0.2 dispatch-gate port. All sealed. All sacred floors held line-by-line throughout. No D-tickets opened from Phase B work other than D-6 (informational discovery import-analysis discrepancy, fully resolved).

You are NOT walking into a fragile or speculative state. You are walking into a state where every claim in `VALIDATION_LEDGER.md` is paired with empirical verification (SHA-1, `diff = 0`, pytest counts, file inspection, git log). If you find yourself doubting any of those claims, read the ledger before re-litigating. The verification is named.

You are walking into a project owner (Daniel) who has invested two-plus weekends into this work, with engineering-grade discipline, and who is tired of having to re-explain validated facts to skeptical Claude sessions. He values pushback when reasoned; he does not value re-verification of things already verified. Read the ledger.

---

## SECTION 2 — Where the project stands at end-of-day 2026-04-27

### Phase status

| Phase | Status | Branch | HEAD commit |
|---|---|---|---|
| Phase 1 (frontend, manual tools, offline-capable) | Closed at v6.3.x | (any) | n/a — single-file HTML, sacred |
| Phase 2 v0.1 (schema + experiment) | Sealed | — | `aeaed74` |
| Phase 2 v0.2 (TracePoint dispatch gate port) | Sealed | `phase2-v0.2-dispatch-port` | `441896a` |
| v0.2.1 (D-4 + D-5 + schema migration) | Pre-scoped, NOT started | — | — |
| Phase B.1 (filter pipeline) | Sealed | `phase2-v0.3-B1-filter-pipeline` | `1c3fde4` |
| Phase B.2 (geometry engine) | Sealed | `phase2-v0.3-B2-geometry-engine` | `4af872e` |
| Phase B.3 (post-clustering scorers) | Sealed | (same branch) | `70c1835` |
| Phase B.4 (architect-profile + storage + correction_store) | Sealed | (same branch) | `a8ee936` |
| **Phase B as a whole** | **COMPLETE — sealed end of 2026-04-27** | `phase2-v0.3-B2-geometry-engine` | `a8ee936` |
| Phase C (trade module foundation) | NOT started; design phase | — | — |
| Phase D (database + job folder structure) | NOT started | — | — |
| Phase E (backend API for frontend) | NOT started | — | — |
| Phase F (auto-notation product) | NOT started | — | — |

**Push status:** No phase has been pushed to remote. Daniel's call. Not a blocker for further work.

### Test floor at end-of-day 2026-04-27

| Suite | Count |
|---|---:|
| Frontend `run_tests.js` | 107/107 |
| Frontend `spotcheck_10b.js` | 7/7 |
| Frontend `spotcheck_cricket.js` | 4/4 |
| Frontend `spotcheck_durolast.js` | 8/8 |
| Frontend `spotcheck_manufacturer.js` | 14/14 |
| Frontend `mutation_test_step11.js` | 8/8 mutations caught |
| Backend full suite | **214 passed, 19 skipped, 0 failed** |

The frontend file in workspace is `Huckleberry_AI_6_3_1_Scope.html` (v6.3.1, 107 tests). Earlier conversation notes referenced "v6.3.5 / 138 tests"; that file is NOT in this workspace. The empirical truth is 107/107. Future Claude: do NOT try to reconcile to 138. The floor is what the runner produces.

### Backend file inventory (Phase B end-state)

```
backend/
├── core/
│   ├── __init__.py              (empty, per TracePoint convention)
│   ├── config.py                v0.2 ported, sacred
│   ├── pdf_engine.py            v0.2 ported, sacred
│   ├── zone_filter.py           v0.2 ported, sacred
│   ├── context.py               v0.2 ported, sacred
│   ├── dispatch_gate.py         v0.2 ported, sacred (storage activation gate at None)
│   ├── filter_pipeline.py       B.1 ported, sacred
│   ├── geometry_matrix.py       B.2 ported, sacred (uses cv2/numpy/shapely/PIL)
│   ├── polygon_scorers.py       B.3 ported, sacred
│   ├── architect_profile.py     B.4 ported, sacred (NOT activated in dispatch_gate yet)
│   ├── storage.py               B.4 ported, sacred (SQLite at ~/.tracepoint/cache.db; Postgres deferred to Phase D)
│   └── correction_store.py      B.4 ported, sacred (JSONL append per doc_id)
├── seeds/
│   ├── roofing_materials.py     v0.1 — ROOFING_SEED_ITEMS (21 items), no current consumer
│   ├── roofing_spec_database.py v0.2 ported (renamed from data/roofing_materials.py), sacred
│   ├── roof_assemblies.py       40-component DB, no current consumer (Phase C target)
│   ├── glazing_assemblies.py    parked, no current consumer (Phase C.3 target)
│   └── glazing_materials.py     parked, no current consumer (Phase C.3 target)
├── tests/
│   ├── test_pdf_engine.py       v0.2 ported, 40/40
│   ├── test_dispatch.py         v0.2 ported, 34 + 19 skipped
│   ├── test_filter_pipeline.py  B.1 ported, 27/27
│   ├── test_geometry_matrix.py  B.2 ported, 36/36
│   ├── test_polygon_scorers.py  B.3 ported, 16/16
│   ├── test_architect_profile.py B.4 ported, 23/23
│   ├── test_pipeline_dispatch.py v0.1, 14/14
│   ├── test_pipeline_scope.py   v0.1, 12/12
│   ├── test_schema_round_trip.py v0.1, 5/5
│   └── test_seeds_load.py       v0.1, 7/7
├── scripts/                     diagnostic scripts (uncommitted)
├── test_fixtures/
│   ├── v0.2_outputs/            15 STACK PlanSetContext JSONs (committed)
│   ├── public_corpus_outputs/   4 non-STACK JSONs (gitignored)
│   ├── intake_diagnostic_outputs/  19 per-page CSVs (gitignored)
│   └── *.json                   diagnostic summaries (gitignored)
├── pyproject.toml               adds opencv-python, numpy, shapely, Pillow at B.2
├── V0_2_VALIDATION.md           sealed (4-symptom STACK validation)
├── PUBLIC_CORPUS_OBSERVATIONS.md uncommitted
├── INTAKE_DIAGNOSTIC.md         uncommitted (Pass 1)
├── INTAKE_DIAGNOSTIC_PASS2.md   uncommitted (Pass 2)
├── TRACEPOINT_DISCOVERY.md      uncommitted (discovery output)
└── DISCOVERED_ISSUES.md         D-1 through D-5 (D-1/2/3 resolved; D-4/5 deferred to v0.2.1)
```

### Working tree state at end-of-day 2026-04-27

`phase2-v0.3-B2-geometry-engine` branch (carries B.2 + B.3 + B.4 commits on top of v0.2's `441896a`).

Uncommitted in working tree (pre-existing, not from B.4 work):
- `MARCH_ORDERS_B_4.md`, `MARCH_ORDERS_B_2_AND_B_3.md`, `MARCH_ORDERS_B_1.md`
- `backend/PUBLIC_CORPUS_OBSERVATIONS.md`
- `backend/INTAKE_DIAGNOSTIC.md`, `backend/INTAKE_DIAGNOSTIC_PASS2.md`
- `backend/TRACEPOINT_DISCOVERY.md`
- `backend/scripts/run_dispatch_on_public_corpus.py`
- `backend/scripts/intake_diagnostic.py`
- `backend/scripts/intake_diagnostic_pass2.py`
- `.gitignore` (modifications from prior sessions)

These are documentation and observation artifacts. They have not been committed because the right home for them is unclear (separate observations branch? fold into a future phase?). Daniel's call when convenient.

---

## SECTION 3 — What just happened in this session (2026-04-27)

This was a long, productive session. Six concrete things shipped:

### 3.1 — Architectural realignment

Daniel re-read the TracePoint research paper end-to-end and identified that v0.2 ported only Layer 3 (the dispatch gate / Filters 1–5). Stages 2–12 of TracePoint's 12-stage pipeline were not in the backend. The frontend had Layer-1/2/2.5 work in JavaScript with a user-polygon override. The platform had been treated as roofing-shaped when TracePoint paper §2.1 explicitly designs Layers 1–3 as trade-agnostic.

The realignment locked the **canonical workflow** (GC uploads → backend ingests/dispatches/runs trade modules/extracts scope/detects polygons → database under job folder → frontend pulls/reviews/edits/approves → Excel export → corrections back as training data) into `CLAUDE.md` Section 1 as non-negotiable. Frontend = review/edit/approve/export only. Backend = everything else.

### 3.2 — New consolidated CLAUDE.md

Replaced both the older Huckleberry v6.2.3-era CLAUDE.md and the upstream TracePoint CLAUDE.md. Single source of truth going forward. 10 sections including: identity, canonical workflow, current state, the 18 ratified Phase 2 architectural decisions, the realignment, the phased recovery path A through F, hard guardrails (28 specific constraints), discovered issues register, communication norms, and instructions for future sessions.

### 3.3 — TracePoint folder placement and discovery

Daniel placed `C:/TracePoint/` as `C:/huck stage 2/huckleberry/tracepoint_port/TracePoint/` (1.6 GB, full project tree). Read-only reference for Phase B verbatim ports. Same pattern as v0.2 used with the network-drive `C:/TracePoint/`.

Claude Code ran a discovery pass producing `backend/TRACEPOINT_DISCOVERY.md`. Established Phase B port surface = 2,854 lines source, splittable into 4 clean sub-phases (B.1: 500, B.2: 1,212, B.3: 442, B.4: 700), with B.2 adding 4 new dependencies (opencv-python, numpy, shapely, Pillow) and B.4 originally requiring Postgres adaptation (later reversed — see 3.6 below).

### 3.4 — Bookkeeping pass (CLAUDE.md edits + folder cleanup)

Deleted the redundant flat snapshot `C:/huck stage 2/tracepoint_port/`. Preserved tree at `huckleberry/tracepoint_port/TracePoint/`. Updated CLAUDE.md §5 with corrections: B.2 keeps `geometry_matrix.py` source filename; B.4 originally got a Postgres-adaptation paragraph (later reversed).

### 3.5 — Phase B.1 through B.4 shipped

Four sub-phases of verbatim port executed against the TracePoint folder, all sealed by end-of-day 2026-04-27:

- **B.1** (filter_pipeline.py + tests, stdlib-only, 500 lines) — gated 6 ways, single session, single commit `1c3fde4`. Sacred floor preserved. SHA-1 verified.
- **B.2** (geometry_matrix.py + tests, adds 4 deps, 1,212 lines) and **B.3** (polygon_scorers.py + tests, stdlib-only, 442 lines) — combined autonomous big-run session per Daniel's "stop the procedural pauses" directive. Two commits `4af872e`, `70c1835`. opencv-python wheel installed cleanly on Windows. SHA-1 verified for all 4 files.
- **B.4** (architect_profile.py + storage.py + correction_store.py + tests, 700 lines) — autonomous big-run, single commit `a8ee936`. SHA-1 verified for all 4 files. Stash workflow handled the CLAUDE.md realignment substrate cleanly. D-6 (informational) opened: discovery's import analysis missed `from core.config import CORRECTION_DIR` in correction_store.py, but the import resolved cleanly because v0.2 already ported config.py with that symbol — no code changes needed.

Total Phase B: 2,354 lines verbatim port, no regressions, no D-tickets blocking, all sacred floors held line-by-line.

### 3.6 — Postgres-adaptation reversal

Daniel reversed the Postgres-adaptation decision before B.4 execution: SQLite stays verbatim. Postgres deferred to Phase D where multi-tenant job-folder data lives architecturally — backend cache for dispatch/profile is a different concern. The reversal is documented in CLAUDE.md §9 as a discipline lesson ("decisions can be reversed cleanly when the layering analysis improves").

### 3.7 — Two diagnostic passes from the prior weekend

Carried forward into this session: Pass 1 (intake diagnostic, 19 bidsets, surfaced asymmetry) and Pass 2 (context inspection of 35 manufacturer hits, dissolved most of the asymmetry — 29 of 35 hits were sealants/drywall/etc., not roofing). Both still uncommitted as observation artifacts. Their conclusions remain valid: dispatch gate is doing approximately what it was designed to do; the 1/15 STACK detection rate may be approximately correct given input data; auto-notation product quality requires the layer that comes after Phase B (trade modules with position-based filtering inside building polygons, per TracePoint paper §9).

---

## SECTION 4 — Commit graph

```
phase2-v0.3-B2-geometry-engine
  a8ee936  Phase B.4: Port architect_profile / storage / correction_store verbatim, reverse Postgres note
  70c1835  Phase B.3: Port polygon_scorers.py verbatim
  4af872e  Phase B.2: Port geometry_matrix.py verbatim, add cv2/numpy/shapely/Pillow deps
phase2-v0.3-B1-filter-pipeline
  1c3fde4  Phase B.1: Port filter_pipeline.py verbatim
phase2-v0.2-dispatch-port
  441896a  Phase 2 v0.2: Port TracePoint dispatch gate
main / earlier
  aeaed74  Phase 2 v0.1 experiment complete: schema draft + findings
```

To get the full Phase B work into a single push when Daniel is ready: push `phase2-v0.3-B2-geometry-engine` (which carries B.2/B.3/B.4 on top of B.1's branch root, but note B.1's commit lives on its own branch — a merge or rebase decision is open).

---

## SECTION 5 — Open questions, none blocking

These exist as known incomplete items. None block Phase C planning. Daniel resolves at convenience.

1. **Push timing for Phase B work.** Daniel hasn't pushed any Phase B work to remote. Could push all four commits at once (`phase2-v0.3-B2-geometry-engine` branch + `phase2-v0.3-B1-filter-pipeline` branch) or hold. Not a blocker.

2. **Branch consolidation.** B.1 lives on its own branch; B.2/B.3/B.4 share another. If a single Phase B branch is wanted, merge or rebase decision needed.

3. **v0.2.1 timing.** Pre-scoped in `STEP_18_DECISION_BRIEF.md`. Could ship before Phase C, in parallel with C, or after C. Daniel's call.

4. **107 vs 138 frontend tests.** Documented environmental fact (workspace has v6.3.1, not v6.3.5). Resolution rule for sacred floor: use whatever the runner produces at session-start as the floor. No reconciliation needed.

5. **Uncommitted documentation.** Diagnostic outputs, observation docs, march-orders documents all sit uncommitted. Where they belong (separate branch? fold into Phase C work?) is open.

6. **D-6 follow-up.** Informational ticket from B.4 — discovery's import analysis missed `from core.config import CORRECTION_DIR` in correction_store.py. Doesn't block anything; worth logging in `backend/DISCOVERED_ISSUES.md` in a future bookkeeping pass.

---

## SECTION 6 — What comes next

### The next planning conversation is Phase C.1

Phase C.1 = define the trade module interface (TradeModuleInput contract per TracePoint paper §9). This is **design work**, not porting. Different shape of session from B.1/B.2/B.3/B.4.

The questions C.1 needs to answer:
- What data structure does a trade module receive? (TracePoint paper §9 names "TradeModuleInput" but doesn't detail the schema.)
- What does it produce? (Per-trade scope + per-trade evidence + per-trade confidence — but in what shape?)
- How does it register with the platform?
- How does it report uncertainty?
- What's the contract for cross-trade dependencies (e.g., RTU on roof = roofing scope's responsibility for flashing, mechanical scope's responsibility for the unit itself)?

Output of C.1 is a design document, NOT code. Reviewed before C.2 begins.

After C.1: C.2 builds the first trade module (roofing) against the contract. C.3 builds the second (glazing). C.4 builds the cross-trade relationships layer.

After Phase C: Phase D database structure, Phase E backend API, Phase F auto-notation product.

### Questions for Daniel before Phase C.1 starts

These do NOT need answers right now; they will be the topics of the C.1 planning conversation:

- Should C.1 design from scratch or take TracePoint's `core/trade_module.py` (90 lines, per discovery) as the starting point and evolve from it?
- Is there an existing TracePoint trade module example (`modules/roofing/`) to look at for shape, even if we won't port it directly?
- Does the trade module interface need to support cross-trade synthesis from day one, or is C.4 a separate layer the modules don't know about?
- Where does position-based filtering (text blocks inside polygon, per paper §9) live — inside each trade module, or in a shared layer all modules use?

### What NOT to do in the next session

- DO NOT propose tuning the dispatch gate or any other ported file. Phase B is sealed; the verbatim port discipline holds. Tuning is a separate phase with its own march orders.
- DO NOT start any port work that wasn't authorized by march orders. Phase C.1 is design, not port.
- DO NOT re-run the intake diagnostics. They've been run twice. Their conclusions are in the validation ledger.
- DO NOT propose new schemas from outside sources (no Grok-style "improvements"). Schema decisions are Phase D.
- DO NOT activate the storage gate in `dispatch_gate.py`. That's a Phase D/E decision.
- DO NOT re-litigate the 18 Phase 2 architectural decisions. They are ratified.
- DO NOT speculate about ground truth that doesn't exist. Auto-notation feasibility cannot be measured without supplier-sourced bidsets that haven't arrived yet.

---

## SECTION 7 — How to communicate with Daniel

Daniel is a non-developer building this project under engineering-grade discipline. He runs sessions with extended-thinking Claude (this chat type) for planning and review, and with Claude Code for execution against the actual repo.

**Discipline signals:**
- "Karpathy logic" → discipline is slipping. Stop. Re-read CLAUDE.md and authoritative documents. Restart from a measured position.
- "Continue" → resume signal between sessions. Pick up from the last gate report's "AWAITING APPROVAL" line.
- "Standing by" → the right closing for Claude. End on what Daniel decides next, not what Claude proposes.
- A blunt directive ("do X, no more Y") → real, take it at face value, don't second-guess.

**Style:**
- Brutal honesty, no sugar-coating, no flattery. He says so explicitly.
- Push back when you disagree. The best moments in recent sessions were correct disagreements. Agreement-with-everything is the failure mode.
- No bullet points or emojis in casual replies. Match the conversational register.
- If you find yourself agreeing with everything Daniel proposes, you are probably failing him.

**On validation:**
- Read `VALIDATION_LEDGER.md` BEFORE doubting any project claim.
- If a claim is in the ledger, the verification is named. Re-litigating it is wasted time and Daniel will say so.
- If a claim is NOT in the ledger, ask Daniel before assuming. Don't speculate.
- Daniel has been managing this project's state across many sessions. He has explained the project state more times than he should have to. Reduce that load.

**Anti-patterns to refuse:**
- Speculating about what's in PDFs without reading them
- Drafting architecture based on outputs that contain confidence labels but no measurements (the Grok schema incident is the canonical example)
- Proposing tuning changes against single-corpus datasets
- Building new schemas while v0.2.1 schema migration is queued
- Writing or accepting "production-grade" / "0.97 quality" / "validated" language without a named evaluation set
- Conflating "extraction works" with "auto-notation works"
- Re-deriving facts that the TracePoint paper already documents

---

## SECTION 8 — Discipline lessons earned this session

These are session-derived lessons that have generalized into project doctrine. Future-Claude should not have to re-discover these.

**1. Read primary sources end-to-end before architecting.** The architectural-gap finding (v0.2 ports Layer 3 only) was sitting in the TracePoint paper the entire time. It was missed across multiple sessions because the architecture was reasoned about from memory rather than from the paper. Daniel re-read the paper and found the gap in one session. Lesson: when working with TracePoint-derived code or architecture, read the paper first, every time.

**2. Diagnostic results need the right architectural frame.** Pass 1 surfaced an "asymmetry" that LOOKED actionable. Pass 2 contextualized it (29/35 hits in non-roofing contexts) and largely dissolved the action case. Without Pass 2, march orders for the wrong thing would have been written. Lesson: when data points toward action, run the cheap follow-up before committing.

**3. Drift toward "roofing only" is the failure mode to actively refuse.** TracePoint paper §2.1 is explicit that Layers 1–3 are trade-agnostic. The disabled UI cards say so. The seed files say so. Daniel says so. Refusing the drift requires active discipline.

**4. Confidence theater is real and must be refused.** The Grok-produced schema with claimed Sanibel validation but no actual access to the PDF is the canonical example. A measurement without a named evaluation set is not a measurement. If you encounter similar inputs, refuse them.

**5. The TracePoint folder copy pattern is proven.** v0.2 read from `C:/TracePoint/`. Phase B reads from `tracepoint_port/TracePoint/` placed in the project tree. Both treat the folder as read-only authoritative source. Don't second-guess it.

**6. Karpathy applies to discussions, not just code.** When you find yourself proposing architecture from memory or pattern-matching prior projects, pause and read the canon.

**7. Match gate density to actual risk.** v0.2 needed heavy gating because the work was novel. Phase B sub-phases needed mechanical verification because the work was repetitive. Same Karpathy discipline, different procedural footprint. Six pause-for-confirm gates on B.1 was theater; autonomous big-runs on B.2+B.3 and B.4 with §7 stops only was right-sized.

**8. §7 stops are for surprises requiring human judgment, not for surprises that can be mechanically verified in-session.** Precedent set during B.4 with the `core.config` import in correction_store.py. The strict reading of the rule said stop; the spirit said continue with verification. Continue was right.

**9. Honest non-conclusions are a discipline tool.** Every diagnostic and observation document records what it cannot conclude as well as what it can. Sample size limits, ground-truth absence, corpus characteristics. The discipline of explicit non-conclusions is what kept the v0.2 validation honest. Carry it forward.

**10. Decisions can be reversed cleanly when layering analysis improves.** The Postgres-adaptation paragraph was added to CLAUDE.md in good faith. Daniel reversed it the same day with better layering reasoning (backend cache vs multi-tenant job-folder data are different concerns). Documented as a §9 lesson. Reversibility is fine; theatrical resistance to changing one's mind is not.

---

## SECTION 9 — How this handoff differs from prior handoffs

Prior handoffs (`HANDOFF_2026-04-26.md`, `HANDOFF_v3_2026-04-27.md`) were written mid-session with Phase B not yet complete. They captured snapshots of partial state. This handoff is end-of-day with Phase B sealed and the validation ledger written. It is the canonical handoff going forward.

The validation ledger (`VALIDATION_LEDGER.md`) is new this session. Its purpose is to prevent future Claude sessions from re-litigating validated facts. If you (future Claude) feel the urge to re-verify something, read the ledger first. Most things are already verified with named methods.

This handoff and the validation ledger should be read together. The handoff is the narrative; the ledger is the receipts.

---

## SECTION 10 — Final state, plain

Phase B sealed. Backend has a full TracePoint port plus the architect-profile flywheel + storage + correction_store. 214 backend tests passing, 19 skipped, 0 failed. Frontend unchanged at the v6.3.1 baseline (107/107 + spotchecks + mutation tests). All sacred files held line-by-line throughout. Dispatch gate's storage activation gate is at None deliberately — the layer is ported, the wiring is a Phase D/E call.

The platform is now positioned for Phase C: trade module foundation. C.1 is design work, not porting. The discipline going forward is: read the canon, pay attention to layering, refuse confidence theater, hold sacred files, match gate density to actual risk, document reversibility.

If you (future Claude) read this and find anything unclear, ask Daniel. Don't speculate. Don't probe. Don't run unauthorized diagnostics. Quote the validation ledger. The work that's been done is real. The next work is Phase C.1.

**End of handoff. Standing by for Phase C.1 planning conversation when Daniel is ready.**
