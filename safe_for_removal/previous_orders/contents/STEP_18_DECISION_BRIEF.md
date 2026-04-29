# Phase 2 v0.2 — Step 18 Schema Migration Decision Brief

**Purpose:** Pre-stage the A/B/C call from `MARCH_ORDERS_v0_2.md` §5 Step 18 so the decision happens cold, not on Step 17 fatigue.
**Status:** Reading material. The decision itself is a hard pause-for-confirm AFTER Step 17 validation lands. Do not commit to anything yet.

---

## TL;DR

**Recommendation: Option C (defer).** This matches the march orders' own §5 Step 18 recommendation. The work below stages WHY C, not whether C — and pre-scopes the v0.2.1 ticket that takes the eventual A migration the rest of the way.

The reasoning is short. v0.1 has essentially no live consumer surface. B builds an adapter to protect consumers that don't exist. A is the right destination but doing it mid-port violates the §4.2 DO-NOT-expand-scope discipline that has held for Steps 10–15. C ships v0.2 cleanly and lets a properly-scoped v0.2.1 ticket do A with discovery first.

---

## What's actually changing schema-wise

| Aspect | v0.1 | v0.2 |
|---|---|---|
| Schema definition | Pydantic in `shared/bidset_record.py` | TracePoint dataclasses in `core/context.py` |
| Top-level shape | Flat | Nested |
| Key types | BidsetRecord | PlanSetContext, PageContext, ProjectMetadata, ProjectScope, SheetEntry, ScaleInfo, SourceTag |
| Output path | (existing test fixtures) | `backend/test_fixtures/v0.2_outputs/` |
| Serialization | Pydantic `.model_dump()` | `to_json()` / `from_json()` round-trip |

**These are incompatible shapes.** Code reading v0.1 JSONs will crash on v0.2 JSONs and vice versa. Any decision here is about how to handle that incompatibility.

---

## Consumer surface — the thing A's cost scales with

A's cost is proportional to who actually reads `BidsetRecord` today. Best estimate from project context:

**Real consumers (probable):**
- `shared/bidset_record.py` itself — defines the schema
- v0.1 extraction pipeline at `backend/scripts/_pipeline/*` — produces JSONs
- Whatever test asserts on v0.1 schema validity (`backend/tests/`)
- Daniel's manual JSON audit that produced the four-symptoms finding

**Definitely NOT consumers:**
- Frontend (Phase 2 has no viewer yet — that's v0.5+ trade module work)
- FastAPI routes (v0.2 explicitly does NOT port routes)
- External systems (no integration surface exists)
- The Phase 1 HTML (offline, sacred, doesn't touch backend schemas)

**Honest unknown:** the exact set of files that import `BidsetRecord`. A `grep -r "BidsetRecord\|bidset_record" backend/ shared/ scripts/` would resolve this in 30 seconds. Worth doing during the Step 16 sweep wait — see "Open questions" at the bottom.

The takeaway: A's migration is internal-only and probably small. But "probably small" is exactly the kind of confidence that mid-port refactors burn through. Get a real number before committing.

---

## Per-option breakdown

### Option A — PlanSetContext as canon, do it in v0.2

**What it means:** Rebuild or retire `shared/bidset_record.py`. Update every consumer. Make PlanSetContext the only schema in the monorepo.

**Cost:** Proportional to consumer surface (unknown precisely). Plus running sacred suites again to confirm 138 + 38 still green.

**Why not now:**
- Mid-port refactor is exactly what §4.2 DO-NOT prohibits ("DO NOT add features 'while we're in there' — refactoring, error handling, generalizing, renaming.")
- The discipline that produced clean Steps 10–15 should not loosen at Step 18 just because the temptation to "tidy up" is strong
- Without consumer-surface discovery, A's scope is speculative
- Even if A is one hour of work, doing it inside v0.2 means v0.2 ships entangled — harder to revert if something goes wrong, harder to bisect

**Verdict:** Correct destination. Wrong timing.

### Option B — both schemas side-by-side, with adapter

**What it means:** Build a `PlanSetContext → BidsetRecord` translator. Maintain both schemas as the codebase evolves.

**Cost:** Substantial (per the orders' own language). Plus ongoing maintenance.

**Why not:**
- The adapter exists to protect v0.1 consumers. The actual consumer surface is small-to-empty.
- Adapters become load-bearing. Once shipped, "we can't change PlanSetContext because the adapter assumes X" becomes a real constraint. A gets indefinitely deferred.
- B is the worst of both worlds: pays cost of A (rebuilding consumer pathways) without the benefit (single source of truth)

**Verdict:** Solving a problem we don't have. Reject.

### Option C — defer

**What it means:** v0.2 outputs land in `backend/test_fixtures/v0.2_outputs/`. v0.1 outputs and `shared/bidset_record.py` untouched. Two schemas coexist by living in different directories.

**Cost:** Zero in v0.2. Future cost: a v0.2.1 ticket that does A properly.

**Why now:**
- Ships v0.2 with discipline intact — the same discipline that prevented B-16/17/18-style scope creep across the port
- v0.2 already uses Step 14's seeds-coexistence pattern (TracePoint's `seeds/roofing_spec_database.py` next to Phase 2's `seeds/roofing_materials.py`). C extends that "two-files-coexist" pattern to schemas.
- Forces consumer-surface discovery to happen as a discrete v0.2.1 step, with proper Karpathy treatment

**What's NOT solved by C:**
- Long-term schema clarity (still TBD until v0.2.1)
- Risk of v0.1 schema living on as zombie if v0.2.1 gets deprioritized
- Two JSON output directories on disk forever until A actually ships

**Verdict:** Take.

---

## v0.2.1 ticket — pre-scoped so C-now-A-later isn't vapor

The biggest risk of C is that v0.2.1 never happens and the schemas drift forever. Counter that by writing the ticket NOW, before Step 18 even lands.

**Ticket title:** v0.2.1 — Migrate Phase 2 backend to PlanSetContext as canonical schema

**Pre-conditions:**
- v0.2 has shipped (Phase 1 138 + Phase 2 backend ~250 tests green, 15 v0.2 JSONs produced and validated)
- No active v0.2 work outstanding

**Step 1 — Discovery (do FIRST, before any code change):**
- `grep -r "BidsetRecord\|bidset_record" backend/ shared/ scripts/`
- Catalog every consumer. This is the migration scope. Write it into the ticket.
- Estimate effort. If consumer surface is larger than expected (>5 files), reassess whether A is actually the right v0.2.1 scope or whether it should be split.

**Step 2 — Failing tests first (Karpathy):**
- For every consumer found, write a test against PlanSetContext shape that fails today
- Confirm tests fail before writing migration code

**Step 3 — Rewrite or retire `shared/bidset_record.py`:**
Two viable paths, decide based on Step 1 findings:
- **Path A1 — thin shim:** rewrite `BidsetRecord` to be a re-export of relevant PlanSetContext fields. Old imports keep working, schema is unified.
- **Path A2 — delete:** remove `bidset_record.py` entirely, update consumers to import from `core.context`. Cleaner but more invasive.

**Step 4 — Update consumers** per Step 1 catalog.

**Step 5 — Run full suite:** 138 + 38 + 70 + new tests = 250+ all green, zero regressions.

**Step 6 — Archive v0.1 JSONs:**
Move `backend/test_fixtures/v0.1_outputs/` (or wherever they live) to `backend/test_fixtures/v0.1_archive/` if retained for comparison, or delete if not. v0.2 outputs become the canonical fixtures.

**Out of scope for v0.2.1 (DO NOT):**
- Any field-level changes to PlanSetContext
- Any new fields beyond TracePoint
- v0.1 extraction pipeline cleanup (separate ticket)
- Any frontend or API work

**Done criteria:**
- `shared/bidset_record.py` is either a thin shim or gone
- No production code imports `BidsetRecord` as the primary schema
- 250+ tests green, 0 regressions
- CLAUDE.md updated to remove "v0.1 schema retained alongside" language

---

## What CLAUDE.md needs to record (per §5 Step 18 gate, Step 19 commit)

Add to the "v0.2 — Dispatch Gate Port" section in CLAUDE.md:

> **Schema migration decision:** Option C selected. v0.2 produces `PlanSetContext` JSONs in `backend/test_fixtures/v0.2_outputs/`. v0.1's flat `shared/bidset_record.py` schema retained alongside, untouched. v0.2 makes no claim to v0.1-schema compatibility — the two coexist via separate output directories. Migration to PlanSetContext as canonical (retire or shim BidsetRecord) deferred to v0.2.1 ticket pre-scoped in `STEP_18_DECISION_BRIEF.md`.

Add to the DO NOT list:
- Do NOT write a `PlanSetContext → BidsetRecord` adapter. That's rejected Option B.
- Do NOT modify `shared/bidset_record.py` until v0.2.1 ships.
- Do NOT mix v0.1 and v0.2 outputs in the same directory.

---

## When this decision happens

`MARCH_ORDERS_v0_2.md` §5 Step 18 is a hard pause-for-confirm. Sequencing:

```
Step 16 (sweep) → Step 17 (symptom validation per STEP_17_REVIEW_CHECKLIST.md) →
Step 18 (this decision) → Step 19 (CLAUDE.md + commit, no push)
```

The decision should be made AFTER Step 17 results, not preemptively. If Step 17 surfaces something unexpected — say, a symptom passes only because v0.2 silently inherited a v0.1-schema field that A's migration would lose — the option weighting could shift.

This brief stages the call. It does not pre-commit to it.

---

## Open questions worth answering during the Step 16 wait

Not blocking, but cheap and they sharpen Step 18:

1. **Consumer surface grep.** `grep -r "BidsetRecord\|bidset_record" backend/ shared/ scripts/`. The result determines how big A actually is. Could be 3 files. Could be 15. Affects v0.2.1 effort estimate but not the C-now decision.

2. **Test references to v0.1 schema.** Do any of the 38 v0.1 backend tests assert on `BidsetRecord` specifically? If yes, those tests are a consumer that v0.2.1 needs to handle — possibly by porting them to PlanSetContext or by deleting them as v0.1 archaeology.

3. **Comparison script architecture.** §5 Step 17 specifies `compare_v0.1_to_v0.2.py`. That script reads both schemas as static JSON files for symptom comparison — no Pydantic enforcement needed, no adapter required. C is fully compatible with the comparison script. Worth confirming once the script exists.

---

## What this brief deliberately does NOT do

- Does not pre-commit to C. The decision is Daniel's at the §5 Step 18 gate.
- Does not propose schema changes to PlanSetContext. v0.2 is a verbatim port; field-level work is out of scope.
- Does not estimate v0.2.1 effort precisely. Discovery in Step 1 of the v0.2.1 ticket does that.
- Does not address v0.3+ trajectory (storage layer, architect_profile, Filter 6, trade module port). Those are §10 of the march orders, separate trajectory.
