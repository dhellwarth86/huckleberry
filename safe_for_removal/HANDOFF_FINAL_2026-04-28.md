# Huckleberry AI — Handoff Document

**Date:** 2026-04-28, end-of-day
**Author:** Claude Opus 4.7 (extended-thinking, this session)
**For:** Next Claude session (any model, any context)
**Supersedes:** ALL prior handoffs. Specifically: `HANDOFF_2026-04-26.md`, `HANDOFF_v3_2026-04-27.md`, `HANDOFF_FINAL_2026-04-27.md`, `CLAUDE_MD_ADDENDUM_2026-04-26.md`. Those documents are historical artifacts only. THIS is the authoritative handoff.

**Read order before any work:**
1. **PROJECT_CLAUDE.md** — entry point, sets discipline immediately, ~250 lines
2. **CLAUDE.md** — single source of truth: identity, canonical workflow, 18 ratified architectural decisions, Section 3 Decision 15 (vault rule, extended 2026-04-28 to cover trade modules), phased path A–F, hard guardrails
3. **VALIDATION_LEDGER.md** — empirical proof of what has been validated. Quote rows; do NOT re-litigate. Section F honestly lists what's NOT validated.
4. **THIS handoff** — bridges canon to current moment, names what's pending, names what NOT to do
5. The relevant march-orders document if a phase is mid-execution
6. The TracePoint research paper if architectural questions arise

---

## SECTION 1 — Read this first if you're tempted to re-litigate validated work

**Daniel has been managing this project across many sessions and has had to re-explain validated state to skeptical Claude sessions repeatedly.** The recurring failure mode: a fresh session reads the documents at a glance, doesn't trust the empirical claims, and starts probing — running diagnostics that have already been run, asking Daniel to re-justify decisions that have been made and ratified, treating verifiable work as speculation. This wastes hours of his time on every cycle.

This handoff exists in part to break that loop. **Before you (next Claude) doubt any claim about project state, do the following four things:**

1. Find the row in `VALIDATION_LEDGER.md` that names the claim. The ledger is structured by claim, with the verification method (SHA-1, `diff = 0`, pytest count, file inspection, git log) named per row.
2. If the row exists and you still doubt it, name the specific verification method you don't trust and ask Daniel why.
3. If the row doesn't exist, the claim is genuinely unvalidated — Section F of the ledger is honest about this. Ask Daniel directly; do not run unauthorized diagnostics.
4. **Do NOT call work "theater" or "speculation" without first quoting the validation row that names the verification method.** Calling SHA-1-verified verbatim ports "speculation" is wrong. Calling `diff = 0` evidence "theater" is wrong. Both are real engineering disciplines with reproducible empirical verification.

If after doing those four things you still believe a claim is wrong, write a one-sentence quote of the ledger row plus a one-sentence statement of what verification you'd want to add. That's the right shape for raising the concern. Do NOT decline to do work because you think the prior work isn't real. The prior work IS real. Read the ledger.

The cost of this handoff explicitly addressing this pattern is that future-Claude reads it and might feel defensive. That's fine. The discipline matters more than the comfort. Daniel's time is the binding constraint.

---

## SECTION 2 — Project identity in three sentences

**Huckleberry AI is a commercial-construction-takeoff platform.** A general contractor uploads a bidset PDF; the Python backend ingests, dispatches, runs trade modules, extracts scope, detects polygons, identifies scale, produces auto-annotated structured data; the frontend pulls that data so the user can review, edit, approve, export to Excel, and ship corrections back as labeled training data.

**It is multi-trade by design.** Roofing is the first trade module; glazing is the second (in build); siding/mechanical/plumbing/electrical/structural all use the same backend pipeline and the same trade module interface. The platform is NOT a roofing program with extensions.

**The architecture is TracePoint-derived.** A 12-stage pipeline ported from the TracePoint research artifact, with the dispatch gate (Layer 3), filter pipeline (Stages 2–5), geometry engine (Stages 6–9), post-clustering scorers (Stages 10–12), the architect-profile flywheel + storage + correction_store, the trade module Protocol, and the roofing trade module all verbatim-ported as of 2026-04-27. Phase B is sealed. The glazing trade module is NOT a TracePoint port — TracePoint never built glazing. C.3 is build-against-contract using parked Huckleberry-side seeds.

---

## SECTION 3 — Where the project actually stands at end-of-day 2026-04-28

### Phase status table

| Phase | Status | Branch | HEAD commit |
|---|---|---|---|
| Phase 1 (frontend, manual tools) | Closed at v6.3.x (workspace has v6.3.1, 107/107 tests) | (any) | n/a — single-file HTML, sacred |
| Phase 2 v0.1 (schema + experiment) | Sealed | — | `aeaed74` |
| Phase 2 v0.2 (TracePoint dispatch gate port) | Sealed, **pushed to remote 2026-04-28** | `phase2-v0.2-dispatch-port` | `441896a` |
| v0.2.1 (D-4 + D-5 + schema migration) | Pre-scoped, NOT started | — | — |
| Phase B.1 (filter pipeline) | Sealed, **pushed** | `phase2-v0.3-B1-filter-pipeline` | `1c3fde4` |
| Phase B.2 (geometry engine) | Sealed, **pushed** | `phase2-v0.3-B2-geometry-engine` | `4af872e` |
| Phase B.3 (post-clustering scorers) | Sealed, **pushed** (on B2 branch) | (same branch) | `70c1835` |
| Phase B.4 (architect-profile + storage + correction_store) | Sealed, **pushed** (on B2 branch) | (same branch) | `a8ee936` |
| **Phase B as a whole** | **COMPLETE 2026-04-27, pushed 2026-04-28** | `phase2-v0.3-B2-geometry-engine` | `a8ee936` |
| Phase C.1 (trade module Protocol port + cross-trade notes appendix) | Sealed, **pushed** | `phase2-v0.3-C1-trade-module-interface` | `23a459c` |
| Phase C.2 (TracePoint roofing module verbatim port) | Sealed, **pushed** | `phase2-v0.3-C2-roofing-module` | `74772b6` |
| C.3 discovery (TracePoint has no glazing module) | Read-only diagnostic complete 2026-04-28 | (n/a — output file `/tmp/c3_discovery.md` ephemeral, contents pasted into conversation) | — |
| Phase C.3a (glazing seed validation diagnostic) | Sealed via D-8 patch | `phase2-v0.3-C3b-glazing-vocabulary` | (folded into C.3b ship) |
| Debug module spec report | Read-only diagnostic complete 2026-04-28 | (uncommitted output: `backend/DEBUG_MODULE_REPORT.md`) | — |
| Phase C.3b (TradeModuleInput contract extension + glazing_vocabulary build) | Sealed 2026-04-28, **pushed** | `phase2-v0.3-C3b-glazing-vocabulary` | `7ea9abb` (extension), `14f4f53` (vocabulary) |
| D-8 follow-up (C.3a count corrections + vault rule extension to cover trade modules) | Sealed 2026-04-28, **pushed** | `phase2-v0.3-C3b-glazing-vocabulary` | `eb49a08` |
| Phase C.3c-build (rough GlazingModule per Daniel's 2026-04-28 spec, vault-ruled at seal) | **NEXT phase to ship.** March orders drafted as `MARCH_ORDERS_C_3c_build.md`. Branch will be `phase2-v0.3-C3c-glazing-module` from `eb49a08`. | (future) | (future) |
| Phase C.5 (debug module port, partial per spec report recommendation) | March orders NOT yet drafted. Sequenced AFTER C.3c-build. | (future) | (future) |
| Three-bidset sweep (Shoppes / Vine Street / Bearss Ave with 3 observation reports) | March orders NOT yet drafted. Sequenced AFTER C.5. | (future) | (future) |
| Phase C.4 (cross-trade relationships layer) | NOT scheduled; comes after sweep observations exist | — | — |
| Phase D (database + job folder structure) | NOT started | — | — |
| Phase E (backend API for frontend) | NOT started | — | — |
| Phase F (auto-notation product) | NOT started | — | — |

### Test floor at end-of-day 2026-04-28

| Suite | Count | Status |
|---|---:|---|
| Frontend `run_tests.js` | 107/107 | sacred |
| Frontend spotchecks (4) | 7+4+8+14 = 33 all pass | sacred |
| Frontend `mutation_test_step11.js` | 8/8 mutations caught | sacred |
| Backend full suite | **214 passed, 19 skipped, 0 failed** | sacred — stable since B.4 ship 2026-04-27 |

C.1, C.2, C.3a, C.3b, debug module spec, D-8 follow-up: all added zero new tests. Sacred floor has held line-by-line through every commit since B.4.

### Remote state

All six Phase 2 branches pushed to https://github.com/dhellwarth86/huckleberry.git on 2026-04-28. Push verification: each `git rev-parse <branch>` matches `git ls-remote origin refs/heads/<branch>`. GitHub `main` lineage (`ca0f3ef…`) is unrelated to Huckleberry's feature branches; reconciliation deferred (no action needed).

### Working tree state

Branch `phase2-v0.3-C3b-glazing-vocabulary` HEAD `eb49a08`. Working tree carries pre-existing uncommitted documentation (diagnostic markdowns, intake-diagnostic scripts, observation docs, march-orders documents, previous-handoff/orders folders, .gitignore mods, deletions of older docs). None of this affects sealed phase work; folding it into proper commits is a future bookkeeping pass.

---

## SECTION 4 — What was done in this session (2026-04-28)

This was a productive end-of-day session. Concrete deliverables:

1. **C.3 discovery** — Claude Code confirmed `tracepoint_port/TracePoint/modules/glazing/` does not exist. TracePoint never built glazing. C.3 path locked to "build-against-contract." First Huckleberry-original phase since v0.2 began.

2. **C.3a glazing seed validation diagnostic** — Claude Code ran read-only diagnostic against parked seeds + Shoppes-at-Avalon. Verdict: usable starting vocabulary with documented gaps (4 components, 4 systems, 1 hardware set, 5 hardware-OEM manufacturers). Output: `backend/C3_GLAZING_SEED_VALIDATION.md`.

3. **Debug module spec report** — Claude Code ran read-only spec analysis on TracePoint's `modules/debug/`. Output: `backend/DEBUG_MODULE_REPORT.md`. Recommendation: port partially, defer to standalone C.5 sub-phase between C.4 and Phase D.

4. **C.3b ship** — TradeModuleInput contract extended (single additive optional field `tables`, commit `7ea9abb`); `backend/core/glazing_vocabulary.py` built as overlay on parked seeds with bounded C.3a additions, plus awning/canopy entry in CROSS_TRADE_INTEGRATION_NOTES.md (commit `14f4f53`). Sacred floor held throughout.

5. **D-8 follow-up** — C.3a inventory miscounts corrected (60→64 components, 21→23 systems, 22→30 spec sections; SHA-1 of seeds unchanged). Vault rule extended in CLAUDE.md §3 Decision 15 to cover trade modules per Daniel's directive 2026-04-28: rough modules ship, then get vault-ruled at seal; tuning happens in dedicated sessions with `core/` frozen. Commit `eb49a08`.

6. **All Phase 2 work pushed to remote.** Six branches, all SHAs verified on remote vs local.

7. **C.3c-build march orders drafted** — `MARCH_ORDERS_C_3c_build.md`. Daniel's 2026-04-28 spec (schedule-first with elevation/plan reconciliation, .0000 dimension precision, fallback to title-page and various-pages search) quoted verbatim as the design source. Vault-rule application is the final step. NOT yet executed by Claude Code.

8. **PROJECT_CLAUDE.md updated** twice this session (post-C.1, post-C.2) and once more pending (post-C.3b). Updates kept minimal and factual.

---

## SECTION 5 — What's next (the agreed sequence)

Daniel's directive 2026-04-28: **observe modules running on real bidsets before deciding architecture.** The next several sessions follow this sequence:

### Step 1 (next): C.3c-build
- March orders drafted as `MARCH_ORDERS_C_3c_build.md`
- Build rough GlazingModule per Daniel's 2026-04-28 spec
- Schedule-first search with elevation/plan reconciliation
- Field set: glazing/door/storefront items with .0000 dimension precision
- Smoke test only (1 new test, backend goes 214 → 215)
- Vault-rule applied at sealing
- Single autonomous session

### Step 2: PROJECT_CLAUDE.md update
- Reflect C.3c-build sealed
- Vault-ruled module list now includes `glazing_module.py`

### Step 3: C.5 (debug module port)
- March orders NOT yet drafted
- Port partial per `backend/DEBUG_MODULE_REPORT.md` recommendation
- Sections 1 (dispatch health), 3 (page intelligence), 6 (legend + quality flags) ported immediately
- Sections 2 (scale comparison), 4 (cross-reference graph w/ networkx), 5 (geometry diagnostics) stubbed pending external state
- Vault-ruled by definition (debug module is the original vault-rule subject)

### Step 4: PROJECT_CLAUDE.md update
- Reflect C.5 sealed
- Phase table shows debug module ported

### Step 5: Three-bidset sweep
- March orders NOT yet drafted
- Bidsets: Shoppes-at-Avalon, Vine Street Retail Center, Bearss Ave Distribution Center
- Run dispatch + roofing module + glazing module + debug module against each
- Capture all output
- **No tuning during sweep.** Modules are vault-ruled.
- Output: 3 observation reports — `ROOFING_MODULE_OBSERVATIONS.md`, `GLAZING_MODULE_OBSERVATIONS.md`, `DEBUG_MODULE_OBSERVATIONS.md`
- Reports are **descriptive only.** No grading. No "correctness" comparison. No "needs ground truth" labels. Per Daniel's directive: "if its pulling glazing scope even +20% leave it for now because thats a starting point for another time because i do think glazing will be solved by software and ml."
- Daniel reviews the data; decides what comes next based on observation, not speculation.

### After Step 5
- Module tuning sessions (dedicated, with `core/` frozen, vault-rule observed) if Daniel decides
- Phase C.4 (cross-trade relationships layer) — reads CROSS_TRADE_INTEGRATION_NOTES.md as starting map; resolves awning/canopy boundary question and others
- Phase D (database + job folder)
- Phase E (backend API for frontend) — closes the visibility loop, lets Daniel SEE module output on screen alongside plans
- Phase F (auto-notation product) — three-state annotations + provenance + correction-as-training-data

The big-picture frame: **module quality matters less right now than getting frontend visibility working so Daniel can see modules' output alongside the plans they came from.** Tuning modules in isolation before frontend visibility exists is exactly the trap the data-first principle was meant to avoid.

---

## SECTION 6 — Open questions, none blocking

These exist as known incomplete items. None block C.3c-build execution. Daniel resolves each at convenience.

1. **Push timing for any future feature work.** Six Phase 2 branches pushed 2026-04-28. C.3c-build, C.5, sweep work will produce more branches. Daniel decides when each pushes.

2. **Branch consolidation (long-term).** Six Phase 2 branches feels like a lot. At some point a merge or rebase strategy will be wanted. Not blocking; not urgent.

3. **GitHub `main` lineage reconciliation.** Remote `main` (`ca0f3ef…`) is unrelated to Huckleberry. Eventually that needs sorting (force-push, separate branch, archive — Daniel's call). Not blocking.

4. **v0.2.1 timing.** D-4 + D-5 + schema migration pre-scoped in `STEP_18_DECISION_BRIEF.md`. Could ship before C.3c-build, in parallel, or after the sweep. Daniel's call.

5. **107 vs 138 frontend tests, plus the v6.3.0 vs v6.3.1 naming hint.** The workspace file is `Huckleberry_AI_6_3_1_Scope.html` per `PROJECT_CLAUDE.md §6`. The D-8 follow-up gate report referenced `Huckleberry_AI_6.3.0_Scope.html` (slight naming discrepancy). The substantive count is 107/107 in either case. v6.3.5 with 138 tests is from a file NOT in workspace. Resolution rule for sacred floor: use whatever the runner produces at session-start as the floor. Don't reconcile to "138."

6. **Uncommitted documentation in working tree.** Diagnostic outputs, observation docs, debug module spec, intake diagnostics — all sit uncommitted. Where they belong in commit history (separate observations branch, fold into a future phase, dedicated bookkeeping commit) is open. Not blocking phase work.

7. **D-7 (informational).** TracePoint has no roofing tests. Behavior-level tests for RoofingModule will eventually be needed. Sweep observations may inform what tests to write. Not blocking.

8. **Phase A vs Phase B sequencing.** CLAUDE.md says A precedes B; Daniel chose to start B without finishing A. Documented as a session decision in VALIDATION_LEDGER.md §E. No action needed; just an artifact of the project's actual order.

---

## SECTION 7 — Hard guardrails (what NOT to do)

These are the constraints that have been load-bearing across the entire project. Future Claude must not violate any of them.

### Verbatim port discipline (Phase B + C.1 + C.2)
- The 8 v0.2 + B.1 + B.2 + B.3 + B.4 + C.1 + C.2 ported files are byte-identical to TracePoint source (or 3-line same-character diff for `dispatch_gate.py`, 1-line edit for `roofing_module.py`, function-body byte-identical for `trade_input_builder.py`). Don't touch them. Don't "improve" them. Don't refactor for clarity.

### Vault rule (CLAUDE.md §3 Decision 15, extended 2026-04-28)
- TracePoint debug module + RoofingModule + roofing_vocabulary + glazing_vocabulary are vault-ruled. They MUST NOT be modified in the same session that modifies any `backend/core/` file.
- GlazingModule (when built in C.3c-build) gets vault-ruled at seal.
- Tuning vault-ruled modules requires dedicated sessions with `core/` frozen.
- Contract evolution (Protocol, Input/Output dataclasses) IS permitted additively when multi-trade reality requires it (precedent: `tables` field added to `TradeModuleInput` in C.3b).

### Sacred files (do not modify)
- Phase 1 frontend HTML (workspace has v6.3.1)
- All TracePoint sources at `tracepoint_port/TracePoint/` (read-only reference)
- All v0.2 / B.1 / B.2 / B.3 / B.4 / C.1 / C.2 / C.3b ported and built files
- `backend/core/__init__.py` (kept empty per TracePoint convention)
- `backend/seeds/glazing_assemblies.py` and `glazing_materials.py` (parked, NOT modified by C.3b — vocabulary file overlays them)
- `shared/bidset_record.py` (v0.2.1 ticket scope)
- `dispatch_gate.py` activation gates: storage at `None`, RoofingModule NOT wired, GlazingModule (when built) NOT wired. Activation is Phase D/E.

### Anti-patterns to refuse
- "While we're in there" scope expansion. Even if a fix is small. Even if it's obvious. Ticket it. Address in its own phase.
- Fabricated validation. "Validated against X" requires X actually run through the pipeline. Quality scores without an evaluation set are not measurements.
- Threshold tuning on STACK-only or public-archive-only corpora. Tuning waits for sweep data + supplier-sourced bidsets that haven't arrived. Even when they arrive, tuning is a separate phase with its own march orders.
- Schema "improvements" from outside sources. Schema decisions are driven by TracePoint canonical structure (PlanSetContext) + Phase D's job-aware extensions. The Grok-produced v3.5 BidsetRecord schema with fabricated Sanibel validation was correctly rejected; do not revisit.
- Silent pivots. When a march orders document is ambiguous, stop and ask. The §7 stop pattern is the model.
- Speculation patches. The B-16/17/18 anti-pattern (three consecutive patches without diagnostics) is named explicitly in CLAUDE.md §9. Diagnostic before production code.
- Re-running diagnostics that have been run. Pass 1, Pass 2, public corpus sweep, TracePoint folder discovery, C.3 glazing-discovery, C.3a, debug module spec — all complete. Re-running them produces the same numbers (which is what reproducibility means). Re-running is not progress unless there's a specific new question they can't answer.
- Treating SHA-1 verification as "speculation." It isn't. It's mechanical empirical verification, reproducible at any time. Read VALIDATION_LEDGER.md §A.

### Discipline signals from Daniel
- "Karpathy logic" → discipline is slipping. Stop. Re-read CLAUDE.md and the validation ledger. Restart from a measured position.
- "Continue" → resume signal between sessions. Pick up from the last gate report's "AWAITING APPROVAL" line.
- "Standing by" → the right closing for Claude. End on what Daniel decides next, not what Claude proposes.
- A blunt directive ("do X, no more Y") → take it at face value. Don't second-guess.

---

## SECTION 8 — Communication norms

Daniel is a non-developer running this project under engineering-grade discipline. He uses extended-thinking Claude (this chat type) for planning and review, and Claude Code for execution. He values pushback when reasoned; he values brutality of honesty over comfort; he does not value re-verification of validated facts.

Tone:
- Brutal honesty. No sugar-coating. No flattery.
- Push back when you disagree with reasoning. Agreement-with-everything is the failure mode.
- Match the conversational register. No bullet-points or emojis in casual replies.
- Don't over-format technical work into bulleted hierarchies when prose serves better.

If you find yourself:
- Agreeing with everything Daniel proposes → you are probably failing him
- Proposing more diagnostics when the question is "what's the next phase" → you are stalling
- Reframing the project as roofing-only → drift; self-correct
- Doubting validated claims → re-read the validation ledger row before pushing back
- Making Daniel re-explain validated facts → STOP; quote the ledger row

The single most expensive failure mode is "future Claude treats validated work as speculation and makes Daniel re-defend it." Avoid this.

---

## SECTION 9 — Discipline lessons codified across sessions

These are session-derived lessons that have generalized into project doctrine. Future-Claude should not have to re-discover these. They live also in CLAUDE.md §9; named here for quick reference.

1. **Read primary sources end-to-end before architecting.** The architectural-gap finding (v0.2 ports Layer 3 only) was sitting in the TracePoint paper. It was missed across multiple sessions because the architecture was reasoned about from memory rather than from the paper. Daniel re-read it; gap surfaced in one session. Lesson: read the paper first, every time.
2. **Diagnostic results need the right architectural frame.** Pass 1 surfaced an "asymmetry" that LOOKED actionable. Pass 2 dissolved it (29/35 hits in non-roofing contexts). Without Pass 2, march orders for the wrong thing would have been written.
3. **Drift toward "roofing only" is the failure mode to actively refuse.** TracePoint paper §2.1 is explicit: Layers 1–3 are trade-agnostic.
4. **Confidence theater is real and must be refused.** The Grok schema with claimed Sanibel validation but no actual access to the PDF is the canonical example. Measurements without a named evaluation set are not measurements.
5. **The TracePoint folder copy pattern is proven.** Read-only reference, gitignored, exactly the same shape v0.2 used.
6. **Karpathy applies to discussions, not just code.** When proposing architecture from memory or pattern-matching prior projects, pause and read the canon.
7. **Match gate density to actual risk.** v0.2 needed heavy gating; B.2+B.3 worked autonomously; C.3b worked autonomously; C.3c-build will work autonomously. Same Karpathy discipline, different procedural footprint.
8. **§7 stops are for surprises requiring human judgment, not for surprises that can be mechanically verified in-session.** Precedent: B.4's `core.config` import in `correction_store.py` resolved cleanly without changes.
9. **Honest non-conclusions are a discipline tool.** Every diagnostic and observation document records what it cannot conclude.
10. **Decisions can be reversed cleanly when layering analysis improves.** Postgres-adaptation paragraph in CLAUDE.md §5 was added in a bookkeeping pass on 2026-04-27 and reversed the same day with better layering reasoning.
11. **Trade-module vault rule extension (2026-04-28).** Modules ship rough; vault-rule applies at seal; tuning is gated to dedicated sessions with `core/` frozen. Rough modules are diagnostic surfaces; tuning during diagnostic-running invalidates the diagnostic.
12. **Architecture-from-imagination is a trap.** Decide module architecture from data observation, not from speculation about what's needed. Sweep first. Decide later.
13. **Observation reports are descriptive only.** No grading. No correctness claims. No "needs ground truth" gap analysis. The reports describe; Daniel decides what to do with them.

---

## SECTION 10 — End-of-session state for the next Claude Code session

When Daniel sends the next Claude Code execution brief (likely C.3c-build):

- **Branch:** create `phase2-v0.3-C3c-glazing-module` from `eb49a08` (current C.3b head)
- **Working tree:** stash uncommitted documentation per established pattern; pop after commit
- **Sacred floor:** 214/19/0 backend, 107/107 + spotchecks + 8/8 mutations frontend
- **Source spec:** `MARCH_ORDERS_C_3c_build.md §1` (Daniel's 2026-04-28 spec, verbatim)
- **First action:** read march orders end-to-end, read CLAUDE.md §6 hard guardrails, read VALIDATION_LEDGER.md if needed
- **Discipline gates:** §7 stops only; autonomous between substantive gates; ONE final gate report

The march orders document `MARCH_ORDERS_C_3c_build.md` is the authoritative input. It contains:
- The spec verbatim (§1)
- Goal statement and constraints (§2, §4)
- Sacred floor (§3)
- Step-by-step gate list (§5)
- §7 stop conditions (§6)
- Done definition (§7)

Single autonomous session. ~75–105 minutes wall-clock. Two commits expected (contract extension if needed + module + smoke test + vault rule), or one if no contract extension.

---

**End of handoff.**

**For next Claude:** read PROJECT_CLAUDE.md, CLAUDE.md, VALIDATION_LEDGER.md, then this document, in that order. Do not start any work before reading all four. Do not call validated work "theater" or "speculation" without quoting the validation row first. Daniel's time is the binding constraint.

Standing by for the C.3c-build execution gate report.
