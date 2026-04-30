# MARCH ORDERS — Long-Run Chain: D.2 Build → Soft Gate → Three-Bidset Hard Gate

**Date issued:** 2026-04-29
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** **THREE PHASES STACKED in one continuous run.** Auto-continue between phases unless a soft gate fails. Single final master gate report.
**Read first:** PROJECT_CLAUDE.md, BLOCK_RUN.md, VALIDATION_LEDGER.md, then this document

---

## §0 — The chain at a glance

```
START
  ↓
Phase A: D.2 build
   - Job entity + persistent storage write path
   - User-fills-in metadata at upload (or download)
   - GC + sortable attributes (no GC hierarchy — flat)
   - Schema designed; SQLite for now (Postgres deferred to post-user-testing)
   - Single Silverleaf reference run to populate one job
  ↓
[CHECKPOINT 1: D.2 build complete; auto-continue if backend tests + vault SHA-1s + frontend SHA-1s held]
  ↓
Phase B: D.2 soft gate — auto-tested persistence round-trip
   - Run Silverleaf through D.2's wired path → job created + stored
   - Simulate session end (close + reopen storage handle)
   - Verify job + all per-page TradeModuleOutput round-trip from disk
   - 10 round-trip assertions
  ↓
[SOFT GATE: if all 10 round-trip assertions pass → continue. If any fail → STOP + report.]
  ↓
Phase C: three-bidset hard gate
   - Run Bearss + Shoppes + Vine Street through D.2's wired path
   - Each bidset becomes a persistent job
   - All three hard-gate criteria must pass per bidset
   - Compare module output against D.1 hard gate baseline (Silverleaf) + sweep baseline (Bearss/Shoppes/Vine)
  ↓
[HARD GATE: if any bidset fails any criterion → STOP + report. If all 3 pass → continue.]
  ↓
PROJECT_CLAUDE.md update + BLOCK_RUN.md update + commit + push
  ↓
END
```

**STOP CONDITIONS** (from any phase): sacred floor regression, vault-ruled SHA-1 change, frontend SHA-1 change, dispatch raises, persistence round-trip fails, hard gate criterion fails. Any of these stops the chain immediately and surfaces to Daniel.

**OUT OF SCOPE for this run:**
- Phase E (backend API) — separate run after this
- F.0 prep — separate run
- Wiki / Project Memory Vault — separate run, much later (Daniel directive)
- Postgres migration — deferred to post-user-testing
- Frontend changes — vault-treated throughout
- Module tuning — vault rule active throughout

---

## §1 — Pre-flight reads (Karpathy step 1)

Full reads, in this order, ONCE at the start of the chain:

1. **PROJECT_CLAUDE.md** — entry point. Note §3's D.1 paragraph; §7 phase table; §8 Phase E vs D.2 decision. The chain runs D.2.
2. **BLOCK_RUN.md** — Phase 1 (calibration), Phase 2 (D.1), Phase 2.5 (housekeeping). You extend with Phase 3 (D.2 build), Phase 3.5 (D.2 soft gate), Phase 4 (three-bidset hard gate).
3. **VALIDATION_LEDGER.md** — sacred floors. §A active production files. §G vault-ruled list. §H decisions including SQLite-stays.
4. **`backend/CALIBRATION_GATE_REPORT_silverleaf.md`** — calibration baseline.
5. **`backend/D_HARD_GATE_silverleaf.md`** — D.1 hard gate baseline. The numerical anchors for this chain's persistence comparisons.
6. **`backend/SWEEP_OBSERVATION_bearss-ave.md`**, **`backend/SWEEP_OBSERVATION_shoppes-at-avalon.md`**, **`backend/SWEEP_OBSERVATION_vine-street.md`** — three-bidset sweep baselines.
7. **`backend/HOUSEKEEPING_GATE_REPORT.md`** — what got moved into safe_for_removal/.
8. **`backend/core/dispatch_gate.py`** — current state with D.1 wiring.
9. **`backend/core/storage.py`** — full read. This file becomes load-bearing in D.2.
10. **`backend/core/context.py`** — current state with `trade_module_outputs` field from D.1.
11. **`backend/core/trade_module.py`** — `TradeModuleInput` + `TradeModuleOutput` shapes.
12. **`backend/core/trade_input_builder.py`** — current state.
13. **`backend/scripts/d1_silverleaf_hardgate.py`** — D.1 hard gate harness; D.2 hard gate harness will follow this pattern.
14. **`backend/scripts/sweep_three_bidsets.py`** — sweep harness pattern; the three-bidset hard gate is a sweep variant with persistence.

**Do NOT open:** the five vault-ruled modules, any frontend HTML, anything in `safe_for_removal/`, CLAUDE.md (retired).

---

## §2 — Step Chain.0: Pre-flight verification (chain start)

Before Phase A starts:

- Run the full backend suite. Floor: **216 passed, 19 skipped, 0 failed**. Hard stop if not met.
- Capture pre-chain SHA-1s for all five vault-ruled modules.
- Capture pre-chain SHA-1s for all five frontend HTML files.
- Verify branch state: `phase2-v0.3-housekeeping-safe-for-removal` head matches `870d555` per BLOCK_RUN.md.
- Locate all four bidsets:
  - **B2607 AEA Silverleaf** (D.2 reference + soft gate input)
  - **Bearss Ave Distribution Center** (hard gate bidset 1)
  - **Shoppes-at-Avalon** (hard gate bidset 2)
  - **Vine Street** (hard gate bidset 3)
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git`.

If any pre-flight check fails: chain doesn't start.

---

## §3 — Phase A: D.2 build

### §3.1 — Branch

```
phase2-v0.3-D2-job-folder-and-persistence  (NEW; from housekeeping head 870d555)
```

This is the chain's only branch. All three phases (build, soft gate, hard gate) commit to it. Two commits expected on this branch:

- **Commit 1:** D.2 build code + soft gate harness + hard gate harness + Phase A run results
- **Commit 2:** Soft gate output + hard gate output + PROJECT_CLAUDE.md update + BLOCK_RUN.md update

### §3.2 — Schema design

Design the job entity and its persistent layer. **No Postgres in this chain — SQLite stays per Daniel directive (post-user-testing migration).**

The schema lives in `backend/core/storage.py` (or a new sibling file `backend/core/job_storage.py` if `storage.py`'s current shape doesn't fit cleanly — Claude Code's call based on the read of storage.py). Adding a new file is preferred over modifying storage.py heavily, since storage.py is a B.4 verbatim port and minimal touches preserve the port relationship.

**Table: `jobs`** (or whatever SQLAlchemy/sqlite3 idiom storage.py uses)

| Column | Type | Constraint | Notes |
|---|---|---|---|
| `id` | TEXT | PRIMARY KEY | UUID4 generated at job creation |
| `name` | TEXT | NOT NULL | User-provided at upload (e.g. "B2607 AEA Silverleaf") |
| `gc` | TEXT | NULL allowed | General contractor name. Free-text for now; dropdown later. **Sortable.** |
| `location_city` | TEXT | NULL allowed | E.g. "St Augustine". **Sortable.** |
| `location_state` | TEXT | NULL allowed | E.g. "FL". **Sortable.** |
| `trade_scope` | TEXT | NOT NULL | Comma-separated tags: `"roofing,glazing"` etc. **Sortable.** |
| `bid_due_date` | TEXT | NULL allowed | ISO 8601 date. **Sortable.** |
| `notes` | TEXT | NULL allowed | Free-text. |
| `status` | TEXT | NOT NULL | One of: `draft`, `dispatched`, `in_review`, `exported`, `archived`. **Sortable.** |
| `created_at` | TEXT | NOT NULL | ISO 8601 timestamp. **Sortable.** |
| `updated_at` | TEXT | NOT NULL | ISO 8601 timestamp. **Sortable.** |
| `pdf_path` | TEXT | NOT NULL | Original PDF location |
| `pdf_sha1` | TEXT | NOT NULL | PDF content hash for identity verification |
| `dispatch_complete` | INTEGER | NOT NULL DEFAULT 0 | Boolean — has run_dispatch finished? |

**Table: `dispatch_results`** — one row per (job_id, page_idx)

| Column | Type | Constraint | Notes |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | |
| `job_id` | TEXT | FOREIGN KEY → jobs(id) | |
| `page_idx` | INTEGER | NOT NULL | |
| `page_type` | TEXT | NULL allowed | E.g. "schedule_sheet" |
| `sheet_num` | TEXT | NULL allowed | |
| `sheet_title` | TEXT | NULL allowed | |
| `legends_count` | INTEGER | NOT NULL DEFAULT 0 | |
| `has_legend` | INTEGER | NOT NULL DEFAULT 0 | |
| `has_schedule` | INTEGER | NOT NULL DEFAULT 0 | |
| `raw_tables_json` | TEXT | NULL allowed | JSON-serialized raw_tables for schedule pages |

**Table: `trade_outputs`** — one row per (job_id, page_idx, trade_name)

| Column | Type | Constraint | Notes |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | |
| `job_id` | TEXT | FOREIGN KEY → jobs(id) | |
| `page_idx` | INTEGER | NOT NULL | |
| `trade_name` | TEXT | NOT NULL | "roofing" or "glazing" |
| `output_json` | TEXT | NOT NULL | JSON-serialized `TradeModuleOutput` |

Indexes: `(jobs.gc)`, `(jobs.location_state, jobs.location_city)`, `(jobs.status)`, `(jobs.bid_due_date)`, `(jobs.created_at)` for fast sorts.

### §3.3 — Job lifecycle API (Python)

In the new file (`backend/core/job_storage.py` or wherever storage.py shape allows), expose these functions:

```python
def create_job(
    name: str,
    pdf_path: str,
    *,
    gc: str | None = None,
    location_city: str | None = None,
    location_state: str | None = None,
    trade_scope: str = "roofing",
    bid_due_date: str | None = None,
    notes: str | None = None,
    status: str = "draft",
) -> str:
    """Returns job_id. Computes pdf_sha1, persists job row."""

def get_job(job_id: str) -> dict | None:
    """Returns full job row or None."""

def list_jobs(
    *,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    filter_gc: str | None = None,
    filter_status: str | None = None,
    filter_state: str | None = None,
) -> list[dict]:
    """Returns list of job rows. sort_by must be one of the indexed columns."""

def update_job_status(job_id: str, status: str) -> None:
    """status must be one of the enum values; updates updated_at."""

def persist_dispatch_result(job_id: str, ctx: PlanSetContext) -> None:
    """Walks ctx.pages and writes one dispatch_results row per page."""

def persist_trade_outputs(job_id: str, ctx: PlanSetContext) -> None:
    """Walks ctx.trade_module_outputs and writes one trade_outputs row per (page_idx, trade_name)."""

def load_dispatch_results(job_id: str) -> dict[int, dict]:
    """Reverse of persist_dispatch_result. Reconstructs per-page dispatch state."""

def load_trade_outputs(job_id: str) -> dict[int, dict[str, dict]]:
    """Reverse of persist_trade_outputs. Maps page_idx → trade_name → output dict."""
```

Each function gets a single docstring describing its behavior. Each gets line comments tagged `# D.2:` for traceability.

### §3.4 — Dispatch integration

Modify `dispatch_gate.run_dispatch` minimally to accept an optional `job_id: str | None = None` parameter. When provided:
- After Stage 13 trade module execution, call `persist_dispatch_result(job_id, ctx)` and `persist_trade_outputs(job_id, ctx)`.
- If `job_id is None`, behavior is unchanged from D.1 (in-memory only).

Tag each modification line with `# D.2:`. Budget: ≤20 lines of dispatch_gate.py changes.

### §3.5 — Reference run on Silverleaf

Build a small reference script `backend/scripts/d2_silverleaf_reference.py` (tracked) that:

1. Calls `create_job(name="B2607 AEA Silverleaf", pdf_path=<silverleaf_path>, gc="Accelerated Construction Services", location_city="St Augustine", location_state="FL", trade_scope="roofing,glazing", status="draft")`.
2. Calls `run_dispatch(silverleaf_path, storage="auto", job_id=<returned_id>)`.
3. Updates job status to `"dispatched"`.
4. Prints job_id to stdout and writes a brief reference report to `backend/D2_REFERENCE_silverleaf.md`.

This produces one persistent job in the SQLite database. The soft gate (Phase B) verifies this job round-trips correctly.

### §3.6 — Backend tests stay sacred

D.2 adds NO new tests. Floor: 216/19/0 throughout. If a wiring change breaks an existing test, that's a §7 stop.

### §3.7 — Checkpoint 1 — automatic continue criteria

After Phase A completes, the chain auto-continues to Phase B IF:

1. Backend tests still 216/19/0
2. Vault-ruled module SHA-1s match pre-chain
3. Frontend HTML SHA-1s match pre-chain
4. `dispatch_gate.run_dispatch(silverleaf_path, storage="auto", job_id=<id>)` ran without raising
5. Silverleaf produced module output equivalent to D.1 hard gate (338 roofing fields, 20/81/6 glazing — within rounding)
6. SQLite database file exists and is readable
7. `get_job(<silverleaf_job_id>)` returns the full row

If any criterion fails: **stop the chain**. Phase B does not start.

If all pass: **commit** Phase A's work to the branch (commit 1 of 2) and continue.

---

## §4 — Phase B: D.2 soft gate — auto-tested persistence round-trip

### §4.1 — The soft gate harness

Build `backend/scripts/d2_persistence_soft_gate.py` (tracked).

The harness:

1. Reads the Silverleaf job_id from `backend/D2_REFERENCE_silverleaf.md` (Phase A wrote it).
2. Closes the storage handle (simulates session end).
3. Re-opens a fresh storage handle (simulates session start in a new process).
4. Runs the **10 round-trip assertions** below.
5. Writes the result to `backend/D2_SOFT_GATE_silverleaf.md`.

### §4.2 — The 10 round-trip assertions

Each is a single PASS/FAIL line in the soft gate report:

1. `get_job(silverleaf_job_id)` returns a non-None dict.
2. The dict's `name` equals "B2607 AEA Silverleaf".
3. The dict's `gc` equals "Accelerated Construction Services".
4. The dict's `trade_scope` contains both "roofing" and "glazing".
5. `load_dispatch_results(silverleaf_job_id)` returns a dict with 40 page entries (Silverleaf is 40 pages).
6. Of those 40 pages, exactly 18 have `page_type == "schedule_sheet"` (matches D.1 hard gate).
7. At least 18 pages have non-empty `raw_tables_json` (the schedule pages with cached tables — D.1 baseline was 18/18).
8. `load_trade_outputs(silverleaf_job_id)` returns a dict with 40 page keys.
9. Aggregating roofing fields across all pages yields 338 (matches D.1 hard gate).
10. Aggregating glazing items across all pages yields 20 glazing + 81 door + 6 storefront = 107 total (matches D.1 hard gate).

### §4.3 — Soft gate report

```markdown
# D.2 Soft Gate — Silverleaf Persistence Round-Trip

**Date:** 2026-04-29
**Branch:** `phase2-v0.3-D2-job-folder-and-persistence`
**Job ID:** <UUID from Phase A>
**Database:** ~/.tracepoint/cache.db (or wherever D.2 writes)
**Overall:** PASS / FAIL

## Round-trip assertions

| # | Assertion | Result | Evidence |
|---|---|---|---|
| 1 | get_job returns non-None | PASS / FAIL | <returned dict id> |
| 2 | name == "B2607 AEA Silverleaf" | PASS / FAIL | <actual name> |
| 3 | gc == "Accelerated Construction Services" | PASS / FAIL | <actual gc> |
| 4 | trade_scope contains both trades | PASS / FAIL | <actual trade_scope> |
| 5 | dispatch_results has 40 page entries | PASS / FAIL | <actual count> |
| 6 | 18 pages classified schedule_sheet | PASS / FAIL | <actual count> |
| 7 | ≥ 18 pages with raw_tables_json | PASS / FAIL | <actual count> |
| 8 | trade_outputs has 40 page keys | PASS / FAIL | <actual count> |
| 9 | Roofing fields aggregate == 338 | PASS / FAIL | <actual count> |
| 10 | Glazing items aggregate == 107 | PASS / FAIL | <breakdown> |

**Overall:** PASS only if all 10 assertions PASS. Any FAIL = overall FAIL.
```

### §4.4 — Soft gate decision logic

- **All 10 PASS** → Phase C auto-continues. Persistence works.
- **Any FAIL** → **STOP THE CHAIN.** Do not proceed to Phase C. Surface to Daniel with the failing assertion(s) and any traceback.

This is the chain's single hard pause point that's not a sacred-floor regression. The whole chain depends on D.2 actually persisting correctly.

---

## §5 — Phase C: three-bidset hard gate

### §5.1 — The hard gate harness

Build `backend/scripts/d2_three_bidset_hardgate.py` (tracked).

The harness:

1. For each of three bidsets (Bearss, Shoppes, Vine Street):
   - Calls `create_job(...)` with bidset-specific metadata.
   - Calls `run_dispatch(<pdf>, storage="auto", job_id=<id>)`.
   - Updates job status to `"dispatched"`.
   - Writes per-bidset hard gate report.
2. Writes master hard gate report `backend/D2_HARD_GATE_three_bidset.md`.

### §5.2 — Per-bidset metadata

| Bidset | name | gc | location_city | location_state | trade_scope |
|---|---|---|---|---|---|
| Bearss | "Bearss Ave Distribution Center" | "Marcobay Construction" | "Tampa" | "FL" | "roofing,glazing" |
| Shoppes | "Shoppes at Avalon" | (extract from sweep observation report if present, else null) | (extract) | (extract) | "roofing,glazing" |
| Vine Street | "Vine Street" | (extract from sweep) | (extract) | (extract) | "roofing,glazing" |

If sweep observation reports don't carry GC info for Shoppes / Vine Street, leave those fields as null. The schema allows it. Don't fabricate.

### §5.3 — Per-bidset hard gate criteria

Each bidset must pass all 7 criteria:

1. **`run_dispatch` completes without raising.**
2. **Module output equivalent to or better than sweep baseline:**
   - Bearss: roofing fields ≥ 700 (sweep produced 769); glazing items ≥ 200 (sweep: 232); door items ≥ 28 (sweep: 31); storefront items ≥ 22 (sweep: 24)
   - Shoppes: roofing ≥ 750 (sweep: 830); glazing ≥ 38 (sweep: 43); door ≥ 20 (sweep: 22); storefront ≥ 20 (sweep: 22)
   - Vine Street: roofing ≥ 1080 (sweep: 1201); glazing ≥ 90 (sweep: 100); door ≥ 11 (sweep: 12); storefront ≥ 21 (sweep: 23)
   - Each threshold is 90% of sweep baseline rounded down (matches D.1's "≥ 90% of baseline" rule).
3. **Per-page module error rate < 25%** (matches D.1 §11 #6).
4. **Tables populated on schedule_sheet pages** (any non-zero count is acceptable; matches D.1 spirit).
5. **Persistence round-trip:** after dispatch completes, close storage handle, reopen, call `load_trade_outputs(<job_id>)`, verify aggregate roofing fields and glazing items round-trip exactly.
6. **Vault-ruled module SHA-1 still matches pre-chain.**
7. **Frontend HTML SHA-1 still matches pre-chain.**

### §5.4 — Hard gate decision logic

- **All 3 bidsets PASS all 7 criteria** → chain proceeds to PROJECT_CLAUDE.md update.
- **Any bidset fails any criterion** → **STOP THE CHAIN.** Surface to Daniel with the failing bidset/criterion and traceback if any.

### §5.5 — Hard gate master report

`backend/D2_HARD_GATE_three_bidset.md`:

```markdown
# D.2 Three-Bidset Hard Gate

**Date:** 2026-04-29
**Branch:** `phase2-v0.3-D2-job-folder-and-persistence`
**Bidsets:** Bearss Ave / Shoppes at Avalon / Vine Street
**Overall:** PASS / FAIL

## Per-bidset summary

| Bidset | Pages | Dispatch wall-clock | Roofing fields | Glazing items | Total errors | Round-trip | Result |
|---|---:|---:|---:|---:|---:|---|---|
| Bearss | 91 | <s> | <N> | <N>/<N>/<N> | <N> | PASS/FAIL | PASS/FAIL |
| Shoppes | 97 | <s> | <N> | <N>/<N>/<N> | <N> | PASS/FAIL | PASS/FAIL |
| Vine Street | 138 | <s> | <N> | <N>/<N>/<N> | <N> | PASS/FAIL | PASS/FAIL |

## Per-bidset criterion table

(One per bidset; same shape as D.1 hard gate's §5.)

## Sacred floor verification

(Backend 216/19/0, vault SHA-1s, frontend SHA-1s.)

## Persistence round-trip details

(For each bidset: aggregate roofing fields pre- vs post- storage handle reopen.)

## Overall: PASS / FAIL
```

---

## §6 — Step Chain.End: PROJECT_CLAUDE.md + BLOCK_RUN.md update + commit + push

After Phase C ships PASS:

### §6.1 — PROJECT_CLAUDE.md surgical edits

- **§3** — Append Phase D.2 paragraph: storage write path activated; jobs table + dispatch_results + trade_outputs schema; user-fills-in metadata at upload; GC + 4 other sortable attributes; Silverleaf reference job persisted; soft gate PASS; three-bidset hard gate PASS (Bearss + Shoppes + Vine Street). Reference all gate reports by filename.
- **§7** — Phase table: D.2 → COMPLETE; E → NEXT; F → not started.
- **§8** — Rewrite next-planning-conversation: Phase E (backend API + frontend strip-and-connect) is the next phase. Phase F (auto-notation product) follows.

Sections §1, §2, §4, §5, §6, §9, §10 untouched.

### §6.2 — VALIDATION_LEDGER.md additive rows

- §A row for D.2 dispatch_gate.py + storage modifications
- §A row for new `job_storage.py` (or storage.py extensions)
- §A row for context.py changes (if any)
- §D rows: D.2 reference run on Silverleaf, D.2 soft gate, D.2 three-bidset hard gate
- §H row: schema design decisions (what fields, sortability, SQLite-stays-pending-migration)

### §6.3 — BLOCK_RUN.md update

Append Phase 3 (D.2 build), Phase 3.5 (D.2 soft gate), Phase 4 (three-bidset hard gate) sections.

### §6.4 — Commit 2 of 2

Files in commit 2:
- `backend/D2_SOFT_GATE_silverleaf.md` (NEW)
- `backend/D2_HARD_GATE_three_bidset.md` (NEW)
- `backend/D2_HARD_GATE_bearss-ave.md` (NEW — per-bidset detail)
- `backend/D2_HARD_GATE_shoppes-at-avalon.md` (NEW)
- `backend/D2_HARD_GATE_vine-street.md` (NEW)
- `backend/scripts/d2_persistence_soft_gate.py` (NEW)
- `backend/scripts/d2_three_bidset_hardgate.py` (NEW)
- `PROJECT_CLAUDE.md` (MODIFIED — §3, §7, §8 only)
- `VALIDATION_LEDGER.md` (MODIFIED — additive rows)
- `backend/BLOCK_RUN.md` (MODIFIED — Phase 3 / 3.5 / 4 sections)
- `backend/D2_MASTER_GATE_REPORT.md` (NEW — chain master report)

### §6.5 — Push

```
git push origin phase2-v0.3-D2-job-folder-and-persistence
```

If push fails: hard stop, report to Daniel.

---

## §7 — Stop conditions (chain-wide)

Any of these stops the chain immediately:

1. **Sacred floor regresses.** Backend below 216/19/0 at any checkpoint.
2. **Vault-ruled module SHA-1 changes.** All five modules.
3. **Frontend HTML SHA-1 changes.** All five HTMLs.
4. **`run_dispatch` raises** on any bidset.
5. **Phase B soft gate fails any of 10 round-trip assertions.**
6. **Phase C hard gate fails any of 7 criteria on any of 3 bidsets.**
7. **CLAUDE.md gets opened or edited.** Retired by Daniel directive 2026-04-29.
8. **PROJECT_CLAUDE.md edits exceed §6.1 surgical scope.**
9. **A new dependency is needed.** SQLite stays. No SQLAlchemy, no ORM. Use stdlib `sqlite3` directly per B.4 storage.py port.
10. **Push to origin fails.**
11. **Schema design diverges from §3.2 specs in a way that breaks the soft gate's 10 assertions.**

When a stop fires: write a partial gate report to `backend/D2_PARTIAL_<phase>.md` documenting where the chain stopped and why; commit what's safe to commit; push if appropriate; surface to Daniel.

---

## §8 — Discipline reminders (Karpathy)

1. **Read first.** Pre-flight reads in §1 done ONCE at chain start. Each phase doesn't re-read; it acts on what was read.
2. **Sacred floor first.** 216/19/0 verified before each phase, after each phase, after each commit, after push.
3. **Minimum implementation per phase.** Phase A builds the schema + lifecycle + integration + reference run. Not 5 phases of features. Not "while we're in here also wire X." If it's not in §3, it's not in Phase A.
4. **Vault rule held.** Five trade modules untouched and not opened. Frontend untouched. CLAUDE.md not opened.
5. **Auto-continue is structural.** No human-in-the-loop between Phase A → B → C unless a stop fires. Trust the gate criteria; don't pause for "are you sure?"
6. **Schema design is conservative.** SQLite stays. No new deps. Plain stdlib `sqlite3`. Postgres comes later, after user testing. Don't pre-optimize for migration.
7. **Soft gate is the persistence test.** It's the chain's load-bearing checkpoint. If round-trip fails, persistence is broken; the chain stops there even if everything else worked.
8. **Hard gate is empirical.** Three real bidsets, three real comparisons against published sweep baselines. Numbers come from the bidsets, not from speculation.

---

## §9 — Done definition (master gate report checklist)

The final master gate report `backend/D2_MASTER_GATE_REPORT.md` confirms:

- [ ] Pre-flight: 216/19/0 backend; vault SHA-1s captured; frontend SHA-1s captured; all four bidsets located
- [ ] Branch `phase2-v0.3-D2-job-folder-and-persistence` from housekeeping head `870d555`
- [ ] **Phase A:** schema designed and implemented; jobs/dispatch_results/trade_outputs tables created; lifecycle API exposed; dispatch integration ≤20 lines; Silverleaf reference job persisted; commit 1 landed
- [ ] **Phase B:** all 10 soft gate round-trip assertions PASS
- [ ] **Phase C:** all 3 bidsets PASS all 7 hard gate criteria; per-bidset reports saved
- [ ] No vault-ruled module modification (5 SHA-1s match)
- [ ] No frontend SHA-1 change (5 SHA-1s match)
- [ ] CLAUDE.md not opened, not edited
- [ ] No new dependencies (`pyproject.toml` unchanged)
- [ ] No new tests added (216/19/0 unchanged)
- [ ] PROJECT_CLAUDE.md updated per §6.1 (sections §3, §7, §8 only; others untouched)
- [ ] VALIDATION_LEDGER.md additive rows per §6.2
- [ ] BLOCK_RUN.md Phase 3 / 3.5 / 4 sections populated per §6.3
- [ ] Commit 1 (Phase A + harnesses) landed
- [ ] Commit 2 (gate reports + canon updates) landed
- [ ] Push to origin succeeded
- [ ] §7 stops: status of each enumerated explicitly (none expected to fire)
- [ ] Master gate report produced

---

## §10 — Closing

After this long-run chain ships:

1. **Daniel reviews** the master gate report (`backend/D2_MASTER_GATE_REPORT.md`), then per-bidset hard gate reports, then BLOCK_RUN.md.
2. **Daniel confirms** the schema design (or flags edits — schema can iterate before E).
3. **Phase E march orders drafted** by extended-thinking Claude — backend API + frontend strip-and-connect. Now unblocked by D.2.
4. **Phase F.0 prep** drafted next, separately.
5. **Wiki / Project Memory Vault** drafted much later (Daniel directive — not in this run, not in next run, drafted when Daniel signals).

Standing by for execution.

**End of MARCH_ORDERS_D2_long_run.md.**
