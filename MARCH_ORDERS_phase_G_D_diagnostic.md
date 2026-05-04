# MARCH ORDERS — Phase G.D: End-to-End Diagnostic with Helpers

**Date:** 2026-05-03
**Drafted by:** General (extended-thinking Claude in chat)
**Phase type:** Diagnostic with controlled unblocking. Three compounding test runs culminating in one human-driven user test.
**Branch:** `phase2-v0.3-GD-diagnostic`
**Wall-clock budget:** None. This phase runs as long as it needs to run.

---

## Why this phase exists

11 phases have shipped. Each one passed the gate it was given. The end-to-end behavior of the system — what a user sees when they open the frontend, upload a bidset, run dispatch, and look at the results — has not been verified since E.2.2 in late April. Trade modules return 0 entries on Chipotle in standalone dispatch. The frontend ↔ backend connection has not been exercised since the canon updates of G.2 and G.3.

This phase fires up the full system, runs three compounding diagnostic test cycles, and ends with Daniel performing one real user test. The output is the truth on the ground — what works, what's drifted, what's broken — captured with backend logs, DB state, network traces, and screenshots correlated to a live timeline. Daniel reads it and decides what's next. No follow-up phase gets drafted from this seat.

---

## Core rules

**Vault rule (absolute):** The five vault-ruled trade modules are READ-ONLY this entire phase. They may be read for context. They may NOT be edited under any circumstance, by any helper, for any reason:

- `backend/core/roofing_module.py`
- `backend/core/roofing_vocabulary.py`
- `backend/core/glazing_module.py`
- `backend/core/glazing_vocabulary.py`
- `backend/core/debug_module.py`

If trade-module behavior looks wrong during the test, that is a FINDING. Log it. Do not edit.

**Unblocking rule:** Claude Code IS allowed to make minor and moderate fixes to anything preventing the system from running end-to-end:

- Missing dependencies → install
- Wrong path or filename → correct
- Port conflicts → use a different port and document
- Missing config files → recreate from documented defaults
- CORS / middleware blockers in dev → adjust to permissive
- Missing static asset paths the frontend needs → fix
- `requirements.txt` / `pyproject.toml` mismatch with what's actually imported → reconcile
- Database schema mismatch (e.g., column missing from a query) → migrate or reconcile
- Endpoint returns a shape mismatch from what the frontend expects → align IF it's a small format mismatch (snake_case vs camelCase, missing wrapper field). NOT if the underlying data isn't there.

Claude Code is NOT allowed to make scope-level fixes:

- Trade modules return 0 entries → finding, not fix
- Filter 1 misses Silverleaf cover page → finding, not fix
- Dispatch wall-clock is too slow → finding, not fix
- Page classification looks wrong → finding, not fix
- Trade module output values look wrong → finding, not fix

The line is: "did this break the test rig" (fix) vs "is this what the diagnostic exists to surface" (finding).

Every unblocking fix gets logged in the report with: file changed, before/after diff, why it was needed. Daniel reads them and either ratifies or flags as scope-fix-in-disguise.

---

## Pre-flight reads (mandatory)

1. `PROJECT_CLAUDE.md`
2. `PROJECT_ETIQUETTE.md`
3. `ITINERARY.md`
4. `CHECKLIST.md` last 3 handoff entries
5. `backend/G_3_GATE_REPORT.md` — last ship
6. `backend/G_2_HARD_GATE_REPORT.md` — prior ship
7. `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` — read enough to understand:
   - `runDispatchFlow()` (~line 1975) — the upload→createJob→dispatchJob→getResults flow
   - `populateScopeFromResults` and `populatePagesFromResults` — what fields the UI reads
   - The 3-state status bar logic (CHECKING / CONNECTED / UNREACHABLE)
8. `backend/server/` directory — endpoints, routes, app startup
9. The dispatch pipeline entry points in `backend/core/dispatch_gate.py` (`run_dispatch`, `_run_trade_modules`)
10. `backend/core/storage.py` — to know what gets persisted in SQLite

---

## Step 0 — Pre-flight setup

### 0a — Pop the housekeeping stash and commit

Per Daniel's standing instruction:

```
git stash list                                   (confirm stash@{0} exists)
git checkout phase2-v0.3-G3-single-pass-extraction
git stash pop
git status                                       (~40 deletions + reorganized files in safe_for_removal/ and backend/archive/)
git add -A
git commit -m "housekeeping: relocate stale phase docs to safe_for_removal/ and backend/archive/"
git push
```

If `git stash pop` produces conflicts, STOP and report. The stash predates G.3; it shouldn't conflict.

### 0b — Branch from the new head

```
git checkout -b phase2-v0.3-GD-diagnostic
```

### 0c — Sacred floor verification

```
pytest backend/tests
```

Must show 242 passed, 19 skipped, 0 failed. If it doesn't, STOP — something regressed before this phase started.

### 0d — Capture starting vault SHA-1s

Document in the report. All five trade-module SHA-1s plus `dispatch_gate.py` and `pdf_engine.py` for reference. The five trade modules MUST be unchanged at every checkpoint and at end of phase.

---

## Architecture — Claude Code + 2 helpers

This phase uses parallel observation to capture data Claude Code can't gather alone.

### Claude Code (driver)
- Starts and stops the backend
- Coordinates the three test cycles
- Owns the report
- Hands off to Daniel for the user test
- Decides what's an unblocking fix vs a finding

### Helper 1 — Backend watcher
A separate terminal / background process that watches:
- **Uvicorn stdout/stderr** in real time, prefixed with timestamp
- **The SQLite database file** — every 30 seconds, dump row counts of `jobs`, `dispatch_results`, `trade_outputs` tables. When a row is created or updated, log it with the row's primary key
- **Debug module emissions** — search the codebase for where the debug module writes (logs, files, context) and watch those locations
- **Dispatch warnings** at the dispatch level (e.g., "Filter 4 quality gate: X of Y legends removed")
- **Process resource usage** — RAM and CPU of the uvicorn process every 30 seconds. Unbounded RAM growth across the three cycles = finding (cache invalidation issue from G.3)

Helper 1 writes a live log file: `backend/G_D_BACKEND_TIMELINE.log`. Claude Code reads this when correlating frontend events to backend state.

### Helper 2 — Frontend prober
A separate terminal / process — likely a Playwright or Selenium script Claude Code writes for this phase only. The script gets DELETED at phase end, NOT committed to the repo.

Helper 2:
- Opens the frontend HTML in a real browser instance (headless OK for cycles 1-2; headful for cycle 3 since Daniel's at the wheel)
- Captures browser console messages (errors, warnings, info)
- Captures the network tab — every API call, status code, response body, timing
- Takes actual rendered PNG screenshots at each checkpoint (NOT DOM dumps)
- Logs everything to `backend/G_D_FRONTEND_TIMELINE.log` and `backend/G_D_screenshots/`

Helper 2 is automated for cycles 1 and 2. For cycle 3, Helper 2 runs alongside Daniel — capturing his clicks and resulting state, but Daniel is the one driving the browser.

---

## The three compounding test cycles

Each cycle uses the prior cycle's findings as input. None of the cycles produces scope fixes — they produce data the report uses to describe what the system actually does.

### Cycle 1 — Backend in isolation, smallest bidset (Chipotle)

**Goal:** Establish that backend, database, API, and dispatch path work end-to-end on a known-clean bidset, separate from the frontend. If this cycle fails, the failure is in the backend stack, not in coupling.

**Steps:**
1. Start backend (`uvicorn server.app:app --host 127.0.0.1 --port 8000`). Helper 1 starts watching.
2. Hit `/health` from curl. Confirm 200.
3. POST `/jobs` with Chipotle path. Capture response.
4. POST `/jobs/{id}/dispatch`. Capture response and time.
5. GET `/jobs/{id}`. Capture state transitions.
6. GET `/jobs/{id}/results`. Capture full response. Save to `backend/G_D_chipotle_results.json`.
7. SQLite dump: rows for this job from `jobs`, `dispatch_results`, `trade_outputs`. Save to `backend/G_D_chipotle_db.json`.
8. Stop backend.

**Findings to capture per Cycle 1:**
- Wall-clock for each step (createJob, dispatch, getResults)
- Page count and classification distribution
- Trade-module output entries (count, which pages, which trade)
- Any backend warnings or errors during dispatch
- Memory growth during dispatch
- Shape of the results JSON — does it match what the frontend expects per `populateScopeFromResults` and `populatePagesFromResults`?
- Any unblocking fixes Claude Code had to make for this cycle to complete

### Cycle 2 — Backend + Helper 2 (automated frontend), Chipotle

**Goal:** Add the frontend layer. Confirm the UI can talk to the backend and render results from a clean dispatch run. No human in the loop.

**Steps:**
1. Start backend.
2. Helper 2 launches headless browser, loads the frontend HTML.
3. Helper 2 waits for `/health` poll → CONNECTED state. Screenshot.
4. Helper 2 simulates: enter bidset name "diagnostic_chipotle", paste Chipotle path, click Run Dispatch.
5. Helper 2 waits for "DISPATCH COMPLETE" state. Screenshot at each state transition (CREATING JOB → DISPATCHING → LOADING RESULTS → COMPLETE).
6. Helper 2 clicks Scope tab. Screenshot.
7. Helper 2 clicks Pages tab. Screenshot. For each tab, capture visible content (text, table contents, any error states) verbatim.
8. Helper 2 captures all browser console output.
9. Helper 2 captures all network calls (URL, method, status, response body).
10. Stop backend.

**Findings to capture per Cycle 2:**
- Did the UI reach CONNECTED?
- Did the dispatch flow complete from the UI side?
- What's actually rendered in the Scope and Pages tabs? (verbatim text from screenshots, not "looks populated")
- Any JS console errors?
- Any 4xx or 5xx responses in the network tab?
- Time delta between API completion (backend log) and UI render (frontend log) — if there's a noticeable lag, that's a coupling finding
- Did Helper 1 see anything in the backend during the UI flow that Helper 2 didn't see in the frontend?
- Compare Cycle 2's results JSON to Cycle 1's — they should be byte-identical. If not, the API path is non-deterministic. Major finding.

### Cycle 3 — Daniel-driven user test, Daniel picks the bidset

**Goal:** Real user test. Daniel uploads, clicks, and finds what humans find that automation doesn't.

**Steps:**
1. Claude Code starts backend.
2. Claude Code confirms Helper 1 is watching backend.
3. Claude Code launches Helper 2 in headful mode (visible browser window). Helper 2 captures network + console + screenshots in the background while Daniel drives.
4. Claude Code prints clearly to its own console: **"BACKEND READY. HELPERS RUNNING. DANIEL — your turn. Open the browser, drive the test. Tell me 'done' or 'I'm done' when finished."**
5. Claude Code holds. It does not start work, does not idle-process, does not anticipate. It waits for Daniel.
6. While Daniel drives:
   - Helper 1 keeps logging the backend timeline
   - Helper 2 captures every click, network call, and screenshot
   - When Daniel sees something wrong, he screenshots it (his own screenshot, not Helper 2's) and tells Claude Code: "screenshot saved at X, the [tab/feature] was [wrong how]"
   - Claude Code, on each Daniel report, immediately:
     - Notes the timestamp Daniel reported
     - Pulls the corresponding Helper 1 backend log entries from that timestamp window (±10 seconds)
     - Pulls the corresponding Helper 2 frontend log entries from that timestamp window
     - Writes a correlation entry: "Daniel reports: [issue]. Backend at that timestamp: [what was happening server-side]. Frontend at that timestamp: [what the network/console showed]."
   - Claude Code does NOT investigate further. Does NOT propose fixes. Just correlates and logs.
7. When Daniel says "done", Claude Code:
   - Stops Helper 2 (closes browser, dumps final logs)
   - Stops backend (graceful shutdown)
   - Stops Helper 1
   - Verifies SQLite final state for the job(s) Daniel ran
   - Confirms vault SHA-1s are still unchanged

**Findings to capture per Cycle 3:**
- Which bidset Daniel chose
- Daniel's reports — verbatim, in chronological order
- Each report correlated to backend state and frontend network/console state at the timestamp
- Daniel's own screenshots, referenced in the report
- Helper 2's full screenshot trail of the session
- Any backend warnings, errors, or memory growth Helper 1 caught
- Final SQLite state for any jobs Daniel ran

---

## Step N — Coupling map (after cycle 3)

After Daniel finishes his test, before writing the final report, Claude Code produces a one-page coupling reference (markdown table form, NOT boxes-and-arrows):

- Frontend HTML → which API endpoints it calls and where
- Each API endpoint → which `core/` and `server/` functions it invokes
- `core/dispatch_gate.py` filters → which `core/` files they read/write
- Trade modules → which `TradeModuleInput` fields they read (read-only, gathered from reading the modules — not from running them)
- Storage layer → what gets persisted, what's transient
- Cache layer (G.3) → what gets cached, where it's invalidated

Goal: future phases can see blast radius before editing. This is reference material, not analysis.

---

## Step N+1 — Final report

`backend/G_D_DIAGNOSTIC_REPORT.md` with these sections, in this order:

1. **Honest summary** — 3-5 paragraphs, no spin, written FIRST. What works, what doesn't, what's the gap between gate-report claims and reality. Daniel reads this section first.
2. **Cycle 1 findings** with CLEAN/DRIFT/BROKEN labels per discovery
3. **Cycle 2 findings** — same labeling
4. **Cycle 3 findings** — Daniel's reports + backend/frontend correlations
5. **Unblocking fixes log** — every fix Claude Code made during the phase, with diff, file, and reason. Daniel ratifies or flags.
6. **Coupling map**
7. **Vault SHA-1 verification** at start vs. end (the five trade modules MUST be unchanged)
8. **Sacred floor verification** at start vs. end (242/19/0 MUST hold)
9. **Helper logs index** — pointers to `G_D_BACKEND_TIMELINE.log`, `G_D_FRONTEND_TIMELINE.log`, `G_D_screenshots/`, `G_D_chipotle_results.json`, etc.

---

## Hard guardrails

1. **Vault: five trade-module files unchanged at every checkpoint.** Any change to any of them = STOP, revert, restart. No exceptions.
2. **Sacred floor 242/19/0 at start and end.** New tests are NOT in scope. If a test fails, that's a finding. Don't fix tests.
3. **Helpers are temporary.** Helper 1's log files stay in `backend/` (the report references them). Helper 2's Playwright/Selenium script gets deleted at phase end — does NOT get committed. Screenshots and JSON dumps stay.
4. **One commit on this branch.** Report + log files + screenshots + DB dumps + unblocking fixes all in the same commit, so Daniel reviewing the commit sees both the fixes and the report explaining them.
5. **No git imports in any test or helper code.** No subprocess shelling out to git from Python. Git operations are at the shell, by Claude Code, between cycles.
6. **No new pytest tests.** This phase doesn't add tests. The diagnostic report IS the deliverable.
7. **No canon updates.** CHECKLIST.md, ITINERARY.md, PROJECT_CLAUDE.md, BLOCK_RUN.md are NOT updated by Claude Code. Daniel updates them after reading the report.
8. **No follow-up phase drafts.** The report ends with the honest summary. Daniel decides next.
9. **Safe defaults for Helper 2.** If Helper 2 encounters a destructive UI element (delete buttons, irrecoverable actions), it does not click them. Cycle 3 = Daniel's call, not Helper 2's automation.

---

## STOP conditions

1. **Sacred floor regresses at start.** Don't proceed.
2. **A vault trade-module SHA-1 changes during the phase.** Revert immediately, log the incident, restart from the last known-clean checkpoint.
3. **Cycle 1 backend won't start after reasonable unblocking attempts** (define "reasonable" as: 30 minutes of unblocking work, with each fix logged). Ship the report with what was learned. Documenting what's needed for the backend to even come up has its own value.
4. **An unblocking fix lands in `core/` outside `dispatch_gate.py` or `pdf_engine.py`.** Even those two should NOT change in this diagnostic phase (this is not a tuning phase). If you find yourself editing them, STOP, log the urge, revert.
5. **Claude Code finds itself fixing trade-module behavior, classifier behavior, Filter behavior, or scoring behavior.** Those are findings. Revert any such edit immediately.
6. **Cycle 3 — Daniel reports something Claude Code wants to "quickly fix while we're here."** STOP that thought. Log it as a finding. Continue holding for Daniel.
7. **Memory growth across cycles 1, 2, 3 indicates a leak.** That's a finding. Don't try to fix mid-phase.
8. **Daniel says "stop" or "pause" at any point.** Honor it immediately. Backend off, helpers off, current state captured to report, sign-out.

---

## Done when

- [ ] Stash popped, housekeeping committed and pushed
- [ ] Diagnostic branch created
- [ ] Cycle 1 ran (or BROKEN with reasons logged)
- [ ] Cycle 2 ran (or BROKEN with reasons logged)
- [ ] Cycle 3 ran with Daniel driving (or BROKEN with reasons logged)
- [ ] All Daniel reports during Cycle 3 correlated to backend + frontend timeline
- [ ] Coupling map produced
- [ ] `backend/G_D_DIAGNOSTIC_REPORT.md` written, honest summary at top
- [ ] Helper logs and screenshots present in `backend/`
- [ ] Helper 2's Playwright/Selenium script deleted (NOT committed)
- [ ] Sacred floor 242/19/0 verified at end
- [ ] Five trade-module SHA-1s verified unchanged
- [ ] One commit on the diagnostic branch
- [ ] Branch pushed
- [ ] Backend confirmed shut down
- [ ] Sign-out announcement: "Signed out as Developer. Diagnostic complete. Three cycles ran, [N] unblocking fixes applied, [N] findings logged. Daniel test session captured. Report at `backend/G_D_DIAGNOSTIC_REPORT.md`. Standing by."

---

## What this phase explicitly does NOT do

- Does NOT fix trade modules, classifier, filters, dispatch logic, or any scope-level behavior
- Does NOT update canon files (CHECKLIST, ITINERARY, PROJECT_CLAUDE, BLOCK_RUN)
- Does NOT propose next phases — Daniel decides after reading the report
- Does NOT measure trade-module accuracy, completeness, or correctness — just whether they fire and what they emit
- Does NOT touch any frontend file beyond what's needed for unblocking
- Does NOT add or modify any pytest tests
- Does NOT declare anything "ships clean" — verdicts per finding are CLEAN/DRIFT/BROKEN; the phase as a whole gets no verdict from Claude Code

---

**End of march orders. Three cycles, two helpers, one human-in-the-loop test, one honest report.**
