# Phase B.4 — March Orders

**Target:** Port TracePoint's architect-profile / storage / correction_store layer verbatim into the Huckleberry backend. Final sub-phase of Phase B. After B.4, the backend has TracePoint Stages 1–12 + the architect-profile flywheel.

**Authored:** 2026-04-27
**Authority:** Daniel (POC owner)
**Predecessor:** B.3 (commit `70c1835` on branch `phase2-v0.3-B2-geometry-engine`). Sacred floor at session start: backend 191 passing / 19 skipped / 0 failing, frontend 107 + spotchecks + mutation tests all unchanged.
**Source authority:** `tracepoint_port/TracePoint/` — read-only reference.
**Discipline:** Karpathy preserved on substance. Autonomous between substantive gates per the B.2+B.3 pattern that just shipped successfully. Daniel reviews ONE final report at the end.
**Expected wall-clock:** ~45–75 minutes. Smaller than B.2+B.3.

---

## 0. Decision Reversal — SQLite Stays Verbatim

**This is the substantive change from CLAUDE.md's current B.4 paragraph.** The bookkeeping pass on 2026-04-27 added a paragraph to CLAUDE.md §5 stating that `storage.py` would be ported as a "deliberate adaptation" replacing SQLite with Postgres, with corresponding Alembic migration. **Daniel has reversed that decision.** SQLite stays. Postgres migration is deferred to a later phase (likely Phase D database/job-folder work, where the multi-tenant Postgres question gets answered properly).

**Consequence for B.4:** all three production files (`architect_profile.py`, `storage.py`, `correction_store.py`) are now **pure verbatim ports**, identical in shape to B.1/B.2/B.3. The `diff = 0` and SHA-1 verification standard applies to all three. No SQLAlchemy model work. No Alembic migration. No "behavior parity" verification beyond what the verbatim test suite already covers.

**Consequence for CLAUDE.md:** the §5 B.4 paragraph requires correction. That correction is Step B.4.1 of this march orders, before any production code lands. The paragraph reverts to verbatim-port language consistent with B.1/B.2/B.3.

---

## 1. TracePoint Files Read in Full (Pre-Condition)

Before any code touches the backend, the following files are read end-to-end:

**B.4 port targets (read in full):**
- `tracepoint_port/TracePoint/core/architect_profile.py` (174 lines)
- `tracepoint_port/TracePoint/core/storage.py` (221 lines)
- `tracepoint_port/TracePoint/core/correction_store.py` (134 lines)
- `tracepoint_port/TracePoint/tests/test_architect_profile.py` (171 lines)

**Read for context, NOT ported:**
- `backend/core/dispatch_gate.py` — calls `architect_profile.detect_architect()` when storage is enabled (currently gated to `None` in v0.2; B.4 doesn't change that — the activation decision stays separate)
- TracePoint paper §8.6 — "real architect extraction needs cover-page parsing, not title-block keyword matching"

**Discovery already established:**
- `architect_profile.py` imports: stdlib only (`re`, `dataclasses`, `typing`) plus `from core.storage import StorageEngine` for runtime profile load/save. Zero `from data.*` imports.
- `storage.py` imports: stdlib (`hashlib`, `json`, `pathlib`, `sqlite3`, `dataclasses`, `typing`). Zero `from core.*` and zero `from data.*` imports.
- `correction_store.py` imports: stdlib only (`json`, `pathlib`, `dataclasses`, `typing`, `datetime`). Zero `from core.*` and zero `from data.*` imports.
- `test_architect_profile.py` is the only test file in scope. There is no separate test_storage.py or test_correction_store.py — TracePoint's storage and correction_store are exercised through architect_profile's tests plus the integration tests we already deferred to Phase E (per Q5).
- Expected diff vs source for all three production files: zero lines.
- No new backend dependencies (sqlite3 is stdlib).

If discovery's import analysis is wrong, that's a §7 stop at Step B.4.3 — surface as Discovered Issue, do not silently absorb.

---

## 2. Goal Statement

**B.4 ships when:**

1. CLAUDE.md §5 B.4 paragraph corrected to verbatim-port language (no Postgres adaptation references)
2. `backend/core/architect_profile.py` byte-identical to TracePoint source (`diff = 0`, SHA-1 match)
3. `backend/core/storage.py` byte-identical
4. `backend/core/correction_store.py` byte-identical
5. `backend/tests/test_architect_profile.py` byte-identical
6. All B.4 tests pass at 100% (count empirical, ~15–25 expected from 171-line test file)
7. Sacred floors held — see §3
8. Single commit at end of B.4.5
9. Two CLAUDE.md edits: the §5 B.4 paragraph correction (Step B.4.1) AND a one-line acknowledgment in §9 that the Postgres adaptation note from the 2026-04-27 bookkeeping pass was reversed

**B.4 explicitly does NOT ship:**
- Activation of `storage` argument in `run_dispatch()` — that gate stays at `None` per v0.2 discipline. B.4 ports the storage layer but does not wire it live. Activation is a Phase D or Phase E decision when database/job-folder structure is finalized.
- Activation of `architect_profile` detection — same reason
- Any Postgres-specific code, SQLAlchemy models, or Alembic migrations
- v0.2.1 schema migration / D-4 / D-5
- Any change to v0.2 ported files, B.1/B.2/B.3 ported files, or `dispatch_gate.py`'s gating logic
- Any new dependency

---

## 3. Sacred Floor — Hold Each Line Item

Same rule as B.1/B.2/B.3: each line independent, no reconciliation to a single total.

**Start-of-session baseline (B.3's end-state):**

| Suite | Count |
|---|---|
| Frontend `run_tests.js` | 107/107 |
| Frontend `spotcheck_10b.js` | 7/7 |
| Frontend `spotcheck_cricket.js` | 4/4 |
| Frontend `spotcheck_durolast.js` | 8/8 |
| Frontend `spotcheck_manufacturer.js` | 14/14 |
| Frontend `mutation_test_step11.js` | 8/8 mutations caught |
| Backend `test_pdf_engine.py` | 40/40 |
| Backend `test_dispatch.py` | 34 passed, 19 skipped |
| Backend `test_filter_pipeline.py` (B.1) | 27/27 |
| Backend `test_geometry_matrix.py` (B.2) | 36/36 |
| Backend `test_polygon_scorers.py` (B.3) | 16/16 |
| Backend v0.1 baseline | 38/38 |
| Backend full suite | 191 passed, 19 skipped, 0 failed |

**Expected end-of-session:** 191 + B.4 count, 19 skipped, 0 failed. Every other line unchanged.

If anything regresses below baseline at any verification point, that's a §7 stop.

---

## 4. Constraints

### 4.1 — Sacred files (do not modify except as explicitly authorized)

- **Authorized modification:** `CLAUDE.md` (Steps B.4.1 only — §5 B.4 paragraph + §9 reversal note)
- **Authorized creation:** the four B.4 target files
- **Sacred (do not touch):** all TracePoint sources at `tracepoint_port/TracePoint/`, Phase 1 frontend HTML, all v0.2 ported files (`config.py`, `pdf_engine.py`, `zone_filter.py`, `context.py`, `dispatch_gate.py`, `roofing_spec_database.py`, `test_pdf_engine.py`, `test_dispatch.py`), B.1/B.2/B.3 ported files, v0.1 schema (`shared/bidset_record.py`), seed files, `backend/core/__init__.py` (kept empty), all other docs (`MARCH_ORDERS_*.md`, `STEP_*.md`, `DISCOVERED_ISSUES.md`, `V0_2_VALIDATION.md`, observation/diagnostic docs)

### 4.2 — Do not expand scope

- DO NOT activate the `storage` argument in `run_dispatch()` calls
- DO NOT activate `architect_profile` detection in dispatch
- DO NOT add Postgres / SQLAlchemy / Alembic anything
- DO NOT add new dependencies
- DO NOT migrate `BidsetRecord` to `PlanSetContext`
- DO NOT fix D-4 or D-5
- DO NOT add features "while we're in there"
- DO NOT touch frontend code
- DO NOT add re-exports to `backend/core/__init__.py`

### 4.3 — Do not reinvent

- DO NOT change SQLite path defaults — TracePoint uses `~/.tracepoint/cache.db`. Verbatim port keeps that path. (This is intentional per Daniel's decision — separate concerns: backend cache for the dispatch/profile layer is local-machine SQLite; the Phase D Postgres work is multi-tenant job-folder data, which is a different layer.)
- DO NOT change the JSONL append schema in `correction_store.py`
- DO NOT change the regex patterns in `architect_profile.py` cover-page detection
- DO NOT replace `dataclasses` with anything else

### 4.4 — Karpathy procedure (held on substance)

- Read first (full reads). State which files were read in the final gate report.
- Verbatim copy. `diff = 0` for all three production files and the one test file.
- Sacred floors held at every verification point.
- §7 stops surface Discovered Issues; do not silently resolve.

### 4.5 — Autonomous execution

Same pattern as B.2+B.3. Steps B.4.0 through B.4.5 run in one session. Substantive gates only. ONE final gate report at the end.

---

## 5. Step List

### Step B.4.0 — Pre-flight

**Read:** This march orders document end-to-end. `CLAUDE.md` §5 (current B.4 paragraph that needs correcting) and §6 (hard guardrails refresh). `backend/TRACEPOINT_DISCOVERY.md` §3.10–3.12, §8.4 (B.4 spec).

**Verify (no writes):**
- All §1 source files exist and readable (record SHA-1s)
- All §3 baseline counts match exactly
- Working tree clean. Stash any in-flight docs per the B.1/B.2 pattern: `git stash push -u -m "B.4 pre-flight: stash docs"`
- Branch state: continue on `phase2-v0.3-B2-geometry-engine` (carries B.2 + B.3) and add B.4 to it as the third commit, OR branch fresh as `phase2-v0.3-B4-architect-profile` from `70c1835`. **Recommended: continue on `phase2-v0.3-B2-geometry-engine`** — B.4 is the natural extension of the B.2+B.3 work and a third commit on the same branch is simpler than a third branch. Same convention as B.2+B.3 sharing one branch.

**Internal gate:** Pre-conditions green. Baseline recorded. Branch and stash in place.

**§7 stop only if:** baseline mismatch, source file missing, working tree won't clean.

### Step B.4.1 — CLAUDE.md correction

**Write:** Two edits to `CLAUDE.md`:

**Edit A — §5 B.4 paragraph.** Find the paragraph that begins:

> **B.4 — Port architect-profile system and storage layer with Postgres adaptation.**

Replace its full text (including the deviation block immediately below it) with:

> **B.4 — Port architect-profile system and storage layer verbatim.** Activates the `storage` argument that v0.2 gated to None (architecturally — actual activation in `run_dispatch()` calls is deferred to a later phase). Cover-page parsing for architect firm detection, per TracePoint paper §8.6 ("real architect extraction needs cover-page parsing, not title-block keyword matching"). Source files (3): `tracepoint_port/TracePoint/core/architect_profile.py`, `core/storage.py`, `core/correction_store.py`. Targets: `backend/core/architect_profile.py`, `backend/core/storage.py`, `backend/core/correction_store.py`. Tests: `backend/tests/test_architect_profile.py`. All four files port verbatim — `diff = 0` against TracePoint source. SQLite cache path preserved at `~/.tracepoint/cache.db` per TracePoint convention. Postgres / multi-tenant database work is deferred to Phase D where it belongs architecturally.

**Edit B — §9 Discipline Lessons.** Append a new bullet to the Section 9 list:

> **The Postgres-adaptation reversal (2026-04-27).** A bookkeeping pass on this date added language to §5 B.4 calling for `storage.py` to be ported with adaptation (SQLite → Postgres + Alembic migration) as a §7-style deviation. Daniel reversed that decision the same day before B.4 execution: SQLite stays verbatim. The reversal is recorded here because the conversation that produced the original adaptation was not wrong (Postgres IS Huckleberry's backend persistence per Decision 10), but the layering was wrong — backend cache for dispatch/profile is one concern (local SQLite, fine), multi-tenant job-folder Postgres is a different concern (Phase D). Decisions can be reversed cleanly when the layering analysis improves; this is the canonical example.

**Run:** Sacred floor check (no test impact expected from doc edits, but verify):
```
pytest backend/tests/ -q
node run_tests.js
```

**Internal gate:** CLAUDE.md edits applied. Sacred floor unchanged.

**§7 stop only if:** any test regresses (would indicate something unexpected).

### Step B.4.2 — Read all four B.4 source files end-to-end

**Read:**
- `tracepoint_port/TracePoint/core/architect_profile.py` (174 lines, full)
- `tracepoint_port/TracePoint/core/storage.py` (221 lines, full)
- `tracepoint_port/TracePoint/core/correction_store.py` (134 lines, full)
- `tracepoint_port/TracePoint/tests/test_architect_profile.py` (171 lines, full)

**Verify (no writes):**
- `architect_profile.py` imports: stdlib + `from core.storage import StorageEngine`. Confirm exactly that — no surprises.
- `storage.py` imports: stdlib only (`hashlib`, `json`, `pathlib`, `sqlite3`, `dataclasses`, `typing`). Confirm zero `from core.*`, zero `from data.*`.
- `correction_store.py` imports: stdlib only. Confirm zero `from core.*`, zero `from data.*`.
- `test_architect_profile.py` imports `from core.architect_profile import ...` — public surface confirmed
- Test count rough estimate recorded for B.4.5 gate

**Internal gate:** All imports as discovery anticipated.

**§7 stop only if:** any unexpected import (e.g., a `from core.dispatch_gate` that discovery missed; a Postgres reference; a deferred-phase module import).

### Step B.4.3 — Failing test floor for B.4

**Write:** Copy `tracepoint_port/TracePoint/tests/test_architect_profile.py` → `backend/tests/test_architect_profile.py`. Pure copy, verbatim.

**Run:**
```
pytest backend/tests/test_architect_profile.py -v
pytest backend/tests/ --ignore=backend/tests/test_architect_profile.py -q
```

**Expected:** B.4 tests fail with ImportError (collection-time, reported as 1 error). Rest of suite holds at 191 passed, 19 skipped, 0 failed.

**Internal gate:** Test file in place. ImportError on missing production modules. Sacred floor + B.1/B.2/B.3 unchanged.

**§7 stop only if:** non-ImportError failure or any regression elsewhere.

### Step B.4.4 — Verbatim port of three production files

**Write (in this order — storage first because architect_profile imports it):**
1. Copy `tracepoint_port/TracePoint/core/storage.py` → `backend/core/storage.py`
2. Copy `tracepoint_port/TracePoint/core/correction_store.py` → `backend/core/correction_store.py`
3. Copy `tracepoint_port/TracePoint/core/architect_profile.py` → `backend/core/architect_profile.py`

All pure copies, verbatim, no edits.

**Verify (after each file):**
```
diff tracepoint_port/TracePoint/core/storage.py backend/core/storage.py
sha1sum tracepoint_port/TracePoint/core/storage.py backend/core/storage.py

diff tracepoint_port/TracePoint/core/correction_store.py backend/core/correction_store.py
sha1sum tracepoint_port/TracePoint/core/correction_store.py backend/core/correction_store.py

diff tracepoint_port/TracePoint/core/architect_profile.py backend/core/architect_profile.py
sha1sum tracepoint_port/TracePoint/core/architect_profile.py backend/core/architect_profile.py
```

**Expected:** All three `diff` commands produce zero output. All three SHA-1 pairs match.

**§7 stop only if:** any `diff` produces output. Surface as Discovered Issue.

**Run:**
```
pytest backend/tests/test_architect_profile.py -v
pytest backend/tests/ -q
```

**Expected:** B.4 tests now pass. Full backend suite: 191 + B.4 count, 19 skipped, 0 failed.

**Internal gate:** All three production files byte-identical. B.4 tests 100%. Full backend suite green.

**§7 stop only if:** any test failure or sacred regression.

### Step B.4.5 — Final regression sweep + commit + final gate report

**Run (in order):**
```
# Backend full suite
cd backend && pytest -v

# Frontend — every suite explicitly
node run_tests.js
node spotcheck_10b.js
node spotcheck_cricket.js
node spotcheck_durolast.js
node spotcheck_manufacturer.js
node mutation_test_step11.js
```

**Expected:** Backend at 191 + B.4 count passing. Frontend every suite at exact baseline.

**Write (commit):**
```
git add CLAUDE.md backend/core/architect_profile.py backend/core/storage.py backend/core/correction_store.py backend/tests/test_architect_profile.py
git commit -m "Phase B.4: Port TracePoint architect_profile / storage / correction_store verbatim, reverse Postgres-adaptation note in CLAUDE.md"
```

**Then:**
```
git stash pop
```

Verify post-pop: full backend pytest still at 191 + B.4 count / 19 / 0.

**Produce final gate report** in standard format, single report covering both the CLAUDE.md correction and the verbatim port.

```
=== Phase B.4 Session Report — <date> ===

STEPS COMPLETED: B.4 — verbatim port of architect_profile.py + storage.py + correction_store.py + test_architect_profile.py, with CLAUDE.md correction reversing the Postgres adaptation paragraph.

FILES CHANGED:
  CLAUDE.md                                     MODIFIED (§5 B.4 paragraph + §9 reversal note)
  backend/core/architect_profile.py             NEW (174 lines, byte-identical, sha1 <hash>)
  backend/core/storage.py                       NEW (221 lines, byte-identical, sha1 <hash>)
  backend/core/correction_store.py              NEW (134 lines, byte-identical, sha1 <hash>)
  backend/tests/test_architect_profile.py       NEW (171 lines, byte-identical, sha1 <hash>)
  Verbatim verification: diff against TracePoint source = zero output for all 4 ported files. SHA-1 sums match for all 4.

DEPENDENCIES: pyproject.toml unchanged. No new deps. (sqlite3 is stdlib.)

FILES NOT CHANGED (sacred):
  All TracePoint sources (read-only)
  Phase 1 frontend
  v0.2 ported files (none touched)
  B.1/B.2/B.3 ported files (none touched)
  backend/core/__init__.py (still empty)
  shared/bidset_record.py
  All other docs (MARCH_ORDERS_*, STEP_*, DISCOVERED_ISSUES, V0_2_VALIDATION, observations)
  dispatch_gate.py call sites — storage argument NOT activated; remains None per v0.2 discipline

TESTS:
| Suite                                | Before  | After   | Status |
|--------------------------------------|---------|---------|--------|
| Frontend run_tests.js                | 107/107 | 107/107 | sacred |
| Frontend spotchecks (4)              | all     | all     | sacred |
| Frontend mutation_test_step11.js     | 8/8     | 8/8     | sacred |
| Backend test_pdf_engine.py           | 40/40   | 40/40   | sacred |
| Backend test_dispatch.py             | 34+19sk | 34+19sk | sacred |
| Backend test_filter_pipeline.py      | 27/27   | 27/27   | sacred |
| Backend test_geometry_matrix.py      | 36/36   | 36/36   | sacred |
| Backend test_polygon_scorers.py      | 16/16   | 16/16   | sacred |
| Backend v0.1 baseline                | 38/38   | 38/38   | sacred |
| Backend test_architect_profile.py    | -       | <N>/<N> | B.4 NEW |
| Backend full suite                   | 191     | 191+N   | +N passing |

REGRESSIONS: none

KARPATHY DISCIPLINE:
  Read first: 4 source files read end-to-end before any writes (174 + 221 + 134 + 171 = 700 lines)
  Failing test floor: B.4.3 produced expected ModuleNotFoundError before production code landed
  Minimum implementation: pure verbatim copies, zero edits. diff = 0 for all 4 files.
  100% green floor: all sacred suites unchanged, B.4 tests fully green
  CLAUDE.md correction reverses an architectural decision cleanly with the §9 reversal note documenting the reasoning

DISCOVERED ISSUES: <none, OR D-6+ if any surfaced>

EXECUTION DETAIL:
  Branch: phase2-v0.3-B2-geometry-engine (continued; this is the third commit on the branch)
  Pre-flight stash: stash@{0}: B.4 pre-flight: stash docs (popped at end of session)
  B.4 commit: <SHA> "Phase B.4: Port TracePoint architect_profile / storage / correction_store verbatim, reverse Postgres-adaptation note in CLAUDE.md"
  Stash list at end: empty

git log (current branch):
  <B.4 SHA>  Phase B.4: ...
  70c1835    Phase B.3: Port TracePoint polygon_scorers.py verbatim
  4af872e    Phase B.2: Port TracePoint geometry_matrix.py verbatim, add cv2/numpy/shapely/Pillow deps
  1c3fde4    Phase B.1: Port TracePoint filter_pipeline.py verbatim
  441896a    Phase 2 v0.2: Port TracePoint dispatch gate

PHASE B COMPLETE: B.1 + B.2 + B.3 + B.4 all sealed. Backend now contains TracePoint Stages 1–12 plus the architect-profile flywheel + storage + correction_store. 1,654 + 700 = 2,354 lines of verbatim port across the four sub-phases. No regressions across any sacred suite. No D-tickets opened from Phase B work.

NEXT STEP: Phase C — trade module foundation. C.1 is design work (define the trade module interface / TradeModuleInput contract per TracePoint paper §9), no production code. Phase C is the first phase that requires architectural design work in addition to porting. C.1 march orders draft is the next planning task.

AWAITING APPROVAL: yes — Daniel approves B.4 commit and confirms Phase B is sealed before Phase C planning begins.
```

---

## 6. §7 Stop Conditions

Stop and surface as Discovered Issue, ask Daniel:

1. **`diff` produces non-zero output** at B.4.4 for any of the three production files
2. **SHA-1 mismatch** between source and ported file
3. **Any sacred floor count regresses** at any verification point
4. **Unexpected import** surfaces beyond what discovery documented (e.g., a `from core.dispatch_gate` import in storage.py that discovery missed)
5. **Test count significantly different** from rough expectation
6. **Production file outside the 4 B.4 targets gets modified** by accident (specifically: `dispatch_gate.py` must NOT be modified — the storage argument stays at `None` activation-wise; B.4 only ports the layer, doesn't wire it)
7. **CLAUDE.md edit at B.4.1 introduces a regression** (test files reading from CLAUDE.md? unlikely but possible if any meta-test exists)
8. **Stash pop produces conflicts** at end of B.4.5

§7 stops are documentation actions. Document in `backend/DISCOVERED_ISSUES.md` as next available D-number, pause, ask Daniel.

---

## 7. Done Definition

This session is done when:

- [ ] CLAUDE.md §5 B.4 paragraph corrected
- [ ] CLAUDE.md §9 reversal note added
- [ ] `backend/core/architect_profile.py` byte-identical to source
- [ ] `backend/core/storage.py` byte-identical
- [ ] `backend/core/correction_store.py` byte-identical
- [ ] `backend/tests/test_architect_profile.py` byte-identical
- [ ] All B.4 tests 100% green
- [ ] All sacred floors held at every verification point
- [ ] No new dependencies
- [ ] No changes to `dispatch_gate.py` activation logic
- [ ] No changes to any other sacred file
- [ ] No D-tickets opened, OR all open ones resolved/deferred
- [ ] Single commit on the branch
- [ ] Stash popped cleanly
- [ ] Final gate report produced

When done, **Phase B is complete.** The next planning conversation is Phase C.1 — defining the trade module interface. That's design work, not porting; it's a different kind of session.

---

**End of MARCH_ORDERS_B_4.md. Awaiting Daniel's review and Claude Code execution brief.**
