# MARCH ORDERS — Phase G.D2: Baseline Inventory + Live-Fire Diagnostic

**Date:** 2026-05-04
**Drafted by:** General (extended-thinking Claude in chat)
**Phase type:** Two-stage diagnostic. Stage 1: read-only code inventory. Stage 2: live-fire end-to-end with full-spectrum observation helpers + Daniel-driven session.
**Branch:** `phase2-v0.3-GD2-baseline-inventory`
**Wall-clock budget:** None. Runs as long as it needs to run.
**Predecessor phase:** G.D shipped at `e51c785` + canon at `726d767` + housekeeping commit. G.D2 starts from current head of `phase2-v0.3-GD-diagnostic` after that branch's final commit.

---

## Why this phase exists

G.D proved the system runs end-to-end and surfaced specific findings. What G.D did NOT do is map the **actual implementation status** of every baseline-required capability against the code that ships today. The E.2.2 gate report describes what was *supposed* to be wired. G.D found out the Scope tab doesn't populate, the polygon/rect/line/measure tools silently discard their work, the takeoff tab status is unverified, and Excel export status is unverified. We don't yet know which of those is "stubbed and waiting for wiring", which is "implemented but unwired", and which is "doesn't exist at all."

This phase produces two artifacts:

1. **An updated `PROJECT_CLAUDE.md`** with a new top-priority section defining baseline + the architectural truth: **backend is the database; viewer is the application window to edit, review, finalize document, and export.**
2. **A fact-inventory report** (`backend/G_D2_INVENTORY_REPORT.md`) that maps every baseline capability against the actual codebase, then verifies each label against a live-fire session.

Daniel reads both. Daniel decides what G.4 fixes first.

---

## Core rules

**Vault rule (absolute):** The five vault-ruled trade modules are READ-ONLY this entire phase:

- `backend/core/roofing_module.py`
- `backend/core/roofing_vocabulary.py`
- `backend/core/glazing_module.py`
- `backend/core/glazing_vocabulary.py`
- `backend/core/debug_module.py`

**Unblocking rule (same as G.D):** Minor/moderate fixes allowed if they're preventing the system from running end-to-end. NOT allowed for any scope-level behavior. Every unblocking fix gets logged.

**No new pytest tests this phase.** No edits to existing tests.

**No canon updates EXCEPT the explicitly-defined PROJECT_CLAUDE.md update in Step 1.** Claude Code does NOT touch CHECKLIST.md, ITINERARY.md, or BLOCK_RUN.md in this phase. Those are Daniel's call after he reads the report.

**No follow-up phase drafts.** The report ends. Daniel decides next.

---

## Pre-flight reads (mandatory)

1. `PROJECT_CLAUDE.md`
2. `PROJECT_ETIQUETTE.md`
3. `ITINERARY.md`
4. `CHECKLIST.md` last 3 handoff entries
5. `backend/G_D_DIAGNOSTIC_REPORT.md` — the predecessor diagnostic
6. `backend/E2_2_GATE_REPORT.md` — the supposed-to-be-wired baseline
7. `backend/E0_FRONTEND_AUDIT.md`
8. `backend/E2_0_NEW_FILE_DESIGN.md`
9. `backend/E2_0_API_CLIENT_SPEC.md`
10. `MARCH_ORDERS_E_2_1_strip.md`
11. `MARCH_ORDERS_E_2_2_frontend_connect_and_hard_gate.md`
12. `frontend/src/Huckleberry_AI_phase2.v1.0.0.html` — full read this time, not just the dispatch flow
13. `backend/api/` directory tree — every route file
14. `backend/core/job_storage.py` — what gets persisted, in which tables
15. `backend/core/dispatch_gate.py` (`run_dispatch`, `_run_trade_modules`)
16. `backend/core/storage.py`
17. Any existing Excel export code anywhere in the repo — search for `xlsx`, `openpyxl`, `to_excel`, `xlsxwriter`, `Excel`, `export`

---

## Step 0 — Pre-flight setup

### 0a — Branch from current G.D head

Identify the head commit of `phase2-v0.3-GD-diagnostic` (likely the diagnostic-report commit on top of the housekeeping push). Branch from it:

```
git status                                   (must be clean)
git log -1                                   (capture head SHA)
git checkout -b phase2-v0.3-GD2-baseline-inventory
```

### 0b — Sacred floor verification

```
pytest backend/tests
```

Must show 242 passed, 19 skipped, 0 failed.

### 0c — Vault SHA-1 capture

Document starting SHA-1s for all 5 trade modules + dispatch_gate.py + pdf_engine.py.

---

## Step 1 — Update PROJECT_CLAUDE.md (FIRST, before any other work)

**This is the priority deliverable. Do this BEFORE Stage 1 inventory. Daniel's directive: get the architectural truth and baseline definition into PROJECT_CLAUDE.md so neither chat-Claude nor next-session-Claude-Code drifts from it.**

Add a NEW TOP-LEVEL SECTION at the very top of `PROJECT_CLAUDE.md`, immediately after the title line (before "What Huckleberry is"). Title:

```markdown
## Baseline definition + architectural truth (G chain target)
```

Content (write it close to this — adapt phrasing to match the rest of PROJECT_CLAUDE.md's voice but DO NOT change the substance):

```markdown
**Architectural truth:** Backend is the database. Viewer (frontend) is the application window to edit, review, finalize document, and export. The viewer does not own state. Every edit a user makes is a database mutation. Every save is a database commit. Every export reads from the database. Refresh the browser, everything is still there because it lives in the database.

This has been the design intent since Huckleberry v5. It is the contract every G-chain phase ships against.

**Baseline (the engineering target that unlocks Phase F user testing):**

1. Single upload point. The user uploads a bidset file to the backend in one place. The backend stores the file. There is no separate client-side dropzone for thumbnails — thumbnails come from the backend's stored copy.
2. Dispatch fires on the backend's stored copy at the user's discretion (RUN DISPATCH button).
3. Scope tab populates from the database after dispatch. User can pick a system. A retry control re-fetches scope when the tab is empty.
4. Pages tab shows classified pages from the database. User can manually re-classify; the change writes back to the database.
5. Viewer opens a page. All tools — calibrate, measure, line, polygon, rectangle, pin, exclude — save their edits to the database. No silent discards.
6. Takeoff tab reads from the database (scope + user edits accumulated in the viewer) and shows the in-progress takeoff.
7. Excel export reads from the database. Output: one folder per trade, one page per trade per file.
8. Browser refresh persists everything. The user's session resumes from the database.

When all eight items work end-to-end on a real bidset, baseline is met. Phase F (user testing + trade-module tuning) unlocks. No G-phase ships against any other definition of "done" until baseline is met.
```

After writing the new section, do a single targeted scan of the rest of `PROJECT_CLAUDE.md` for any sentence that contradicts the architectural truth or baseline. If found, do NOT delete or rewrite — flag in the gate report under a "PROJECT_CLAUDE.md contradictions to resolve" subsection. Daniel decides what to do with each.

Commit this change as the FIRST commit on the branch:

```
git add PROJECT_CLAUDE.md
git commit -m "PROJECT_CLAUDE: add baseline definition + architectural truth (G chain target)"
```

Do NOT push yet. The push happens at the end of the phase with all commits batched.

---

## Step 2 — Stage 1: Read-only code inventory

Read-only against the working tree. NO edits. The deliverable is sections of the report.

For each baseline capability below, Claude Code reads the relevant code and produces a fact-inventory entry with one of these labels:

- **IMPLEMENTED + WIRED** — code exists, end-to-end path is connected, expected to work
- **IMPLEMENTED + UNWIRED** — code exists but isn't connected to the rest of the path
- **STUBBED** — placeholder exists with explicit "not implemented" or empty return
- **PARTIAL** — some of the path exists, some doesn't (specify which parts)
- **MISSING** — no code exists for this capability anywhere in the repo

Each entry includes: file paths involved, function/component names, line numbers where the relevant code lives (or doesn't), and a one-sentence factual statement of what's there vs not.

### 2.1 — Single upload point

The current frontend has TWO upload mechanisms:
- Step 2 dropzone (`#dropZone`, drag-drop) — renders pages client-side via PDF.js
- Step 1.5 server-path text input — passes a string path to backend

Inventory:
- Backend: is there an endpoint that accepts a file upload (multipart/form-data)? Search `api/routes/` for `UploadFile`, `File(...)`, `multipart`. If yes, what does it do with the bytes?
- Backend: where does the dispatched PDF currently come from? `pdf_path` string in the job record points to where? File on disk pre-existing? Bytes blob in SQLite?
- Frontend: what code paths drive each of the two upload mechanisms? What database state does each produce?
- Database: is there a `pdf_blob` column anywhere? Is the PDF file stored in the database, on disk, or only referenced by path?

Verdict per: "single upload point that stores file in backend database."

### 2.2 — Dispatch fires on backend-stored copy

Inventory:
- The current `POST /jobs/{id}/dispatch` endpoint reads the PDF from `job.pdf_path`. If `pdf_path` is a server-side string path to a file on the dev machine, that's NOT "backend stores the file" — it's "backend reads a file the user put on the same machine." Confirm or refute.
- For baseline to be met, dispatch must fire on a file the user uploaded into the database (or backend-managed storage area). What's the gap between current and required?

Verdict per: "dispatch fires on backend-stored copy at user discretion."

### 2.3 — Scope tab populates + system pickable + retry

G.D found the shape mismatch (frontend reads `output.systems`, API has no `systems` key). Inventory:
- Frontend: `populateScopeFromResults()` — what does it expect? Read it line by line.
- Backend: `GET /jobs/{id}/results` — what does it return? Schema in `api/schemas/jobs.py`.
- Backend: trade modules' actual output shape — read the TradeModuleOutput dataclass / dict structure.
- Frontend: where would a "system pick" persist? `App.project.scope.selectedSystem`? Does it write to the database via API call, or only in-memory?
- Frontend: is there a retry button on the Scope tab? Search HTML for "retry", "refresh", "reload" near the scope rendering.

Verdict per each: scope-populate, system-pick-persists, retry-control.

### 2.4 — Pages tab + manual re-classify writes to database

G.D confirmed Pages tab renders correctly when both client-side PDF AND backend classifications are present. Inventory:
- Frontend: is there UI for manually changing a page's classification? Search HTML for "reclassify", "change type", or any chip click handler that mutates `page_type`.
- Backend: is there an endpoint like `PATCH /jobs/{id}/pages/{page_idx}` that accepts a page_type override? Search `api/routes/`.
- Database: is there a column/table to store user-overridden classifications, distinct from the dispatch-generated ones?

Verdict per: "user can manually re-classify, change writes to database."

### 2.5 — Viewer tools save to database

The seven tools per E.2.2 audit: calibrate, measure, line, polygon, rectangle, pin, exclude. For EACH tool:

- Frontend: where does the tool's "complete" handler live? What does it do with the result?
- Frontend: does the result land in `App.project.<something>` (in-memory only)?
- Frontend: does the result get sent to an API endpoint? Search for `apiClient.<anything>` calls inside tool handlers.
- Backend: is there an endpoint that accepts annotations / measurements / pins for a job/page? Search `api/routes/` for anything matching annotation, pin, polygon, measurement, calibration, exclusion.
- Database: are there tables for any of these? Search `core/job_storage.py` and `core/storage.py` for table definitions.

Verdict per tool: IMPLEMENTED+WIRED / IMPLEMENTED+UNWIRED / STUBBED / MISSING.

Plus an overall verdict: "tool edits survive a browser refresh."

### 2.6 — Takeoff tab populates from scope + user edits

Inventory:
- Frontend: what code reads from scope + user edits and produces takeoff line items? Search HTML for `renderTakeoff`, `populateTakeoff`, `takeoffItems`, `takeoffData`.
- Frontend: is the takeoff populated from `App.currentResults` (backend), `App.project.takeoff` (local), or some combination?
- Backend: is there a `/jobs/{id}/takeoff` endpoint? Or are takeoff items derived purely on the frontend from results + edits?
- Data shape: is there a defined structure for "a takeoff line item" anywhere — backend schema, frontend constant, or implicit?

Verdict per: "takeoff tab populates from database + edits."

### 2.7 — Excel export

Inventory (search broadly — this code may be legacy from v6.3.5):
- Search the repo for `xlsx`, `openpyxl`, `xlsxwriter`, `to_excel`, `export`, `download`. Note every hit and what it does.
- Frontend: is there an "export" button? Where? What does it call?
- Backend: is there a `/jobs/{id}/export` endpoint?
- Output contract: anywhere in the codebase or docs, is there a spec for "one folder per trade, one page per trade per file"? Or is that contract net-new for G.4?

Verdict per: "Excel export with one-folder-per-trade output."

### 2.8 — Refresh persistence

Inventory:
- After dispatch, the job + dispatch_results + trade_outputs rows exist in SQLite (G.D verified this).
- Does the frontend, on page load, check for an in-progress job? Search for any boot-time call to `getJob` or `getResults` other than triggered by user action.
- Does any localStorage / sessionStorage persist `currentJobId`? G.3 march orders prohibited storage APIs in artifacts but the actual frontend isn't an artifact — does it use them?
- If the user refreshes mid-edit, what happens to their viewer annotations? In-memory only? Lost?

Verdict per: "browser refresh persists current job + all edits."

### 2.9 — PROJECT_CLAUDE.md contradictions

Subsection in the report: any sentence in the rest of `PROJECT_CLAUDE.md` (after Step 1's new section is added) that contradicts the new baseline / architectural truth section. List with line numbers and proposed resolution. Daniel decides.

---

## Step 3 — Stage 2: Live-fire diagnostic with full-spectrum helpers

Stage 1 produced a paper inventory. Stage 2 verifies each label against a running system. Same architecture as G.D Cycle 3 — Claude Code drives, Daniel performs the user actions, helpers capture everything observable.

### 3.1 — Helper roster (expanded from G.D)

#### Helper 1 — Backend watcher (same as G.D)
- Uvicorn stdout/stderr with timestamps
- SQLite tables polled every 30s for row count + recent updates: `jobs`, `dispatch_results`, `trade_outputs`, plus any tables Stage 1 inventory finds for annotations/pins/measurements/exclusions/calibrations
- Debug module emissions
- Process RAM/CPU every 30s
- Output: `backend/G_D2_BACKEND_TIMELINE.log`

#### Helper 2 — Frontend HTTP server (same as G.D)
- Static file server on port 8080 serving the frontend HTML
- Output: `backend/G_D2_FRONTEND_TIMELINE.log`

#### Helper 3 — API call interceptor (NEW for x-ray vision)
- A reverse-proxy or middleware that logs every API request and response between frontend and backend with full request body, response body, timing, and status. Two implementation options:
  - (a) Add a FastAPI middleware that logs request + response to a separate log file. Minimum-invasive. Removed at end of phase.
  - (b) Use mitmproxy or similar between the browser and backend.
- Output: `backend/G_D2_API_INTERCEPT.log` — every API call with full body in/out, plus timing
- Why this matters: G.D could see "POST /jobs/{id}/dispatch returned 200" but couldn't see the response body. Helper 3 captures everything.

#### Helper 4 — SQLite mutation watcher (NEW for x-ray vision)
- Polls SQLite every 2 seconds during active testing (not 30) and diffs row state to detect any change
- For every detected mutation, log: which table, which row PK, before-state vs after-state of changed columns
- Output: `backend/G_D2_DB_MUTATIONS.log`
- Why this matters: when Daniel clicks a viewer tool and "nothing happens," Helper 4 confirms whether ANYTHING wrote to the database

#### Helper 5 — Browser instrumentation (NEW for x-ray vision)
- Inject a small JavaScript snippet into the served HTML (NOT a permanent edit to the source file — Helper 5 serves a wrapped version):
  - Console-log every click on a `<button>`, every tab switch, every tool selection, every keyboard shortcut
  - Capture every `App.project.*` mutation via Proxy (if performance allows; if not, snapshot every 2s and diff)
  - Capture every `apiClient.*` call argument and return
  - Stream all of this to `localStorage` AND a tiny POST to a side-channel telemetry endpoint that Helper 5 also serves
- Output: `backend/G_D2_BROWSER_TELEMETRY.log`
- Why this matters: G.D had zero visibility into client-side actions. Helper 5 closes that gap. The instrumented HTML is served from a Helper 5-controlled path; the original `Huckleberry_AI_phase2.v1.0.0.html` is NOT modified on disk.
- **Helper 5 must be deleted at end of phase.** Same rule as Helper 2's Playwright script in G.D — instrumentation is temporary.

#### Helper 6 — File system watcher (NEW for x-ray vision)
- Watches `~/.tracepoint/` (or wherever the SQLite + any uploaded files live) for any file create/modify/delete during the session
- Output: `backend/G_D2_FILESYSTEM.log`
- Why this matters: if "single upload point that stores file in backend" is supposed to work, we should see the file land somewhere. Helper 6 says where (or confirms nowhere).

### 3.2 — Live fire procedure

1. Claude Code starts backend with Helper 3 (API intercept) middleware enabled
2. Claude Code starts Helper 2 (frontend HTTP server) serving the HTML wrapped by Helper 5 (browser instrumentation)
3. Claude Code starts Helper 1 (backend watcher), Helper 4 (DB mutation watcher), Helper 6 (filesystem watcher)
4. Claude Code prints: **"x-ray helpers running. Backend at 8000. Frontend at 8080. Daniel — drive the test. Tell me 'done' when finished."**
5. Claude Code holds.
6. Daniel drives. Per his earlier message: "I'll put in the file in the preview bar of Claude Code and have it dispatch." Claude Code uses its preview/screenshot tool to load the frontend in a Claude-Code-controlled browser context that Daniel can interact with. When Daniel says he's putting a file in, Claude Code captures the upload event via Helper 5 and the resulting backend state via Helpers 1/3/4/6.
7. For each baseline item from Step 2's inventory, Daniel exercises it in the UI. Claude Code does NOT prompt him through a checklist — Daniel drives in his own order. As each item gets exercised, Claude Code annotates Stage 1's inventory entry with: "Stage 2 verification — [matched / contradicted / partial — details]."
8. When Daniel says "done":
   - Stop browser context
   - Stop backend
   - Stop all helpers
   - Verify vault SHA-1s held
   - Verify sacred floor 242/19/0 still passes
   - Delete Helper 5's instrumented-HTML wrapper script
   - Helper 3's API-intercept middleware: if added as a code edit to `api/main.py` or a new middleware file, REVERT that edit. Middleware should be a development-only insertion that doesn't ship in the commit.

### 3.3 — Stage 2 deliverable

Each Stage 1 inventory entry gets a Stage 2 annotation:

- **Stage 2 verified IMPLEMENTED+WIRED** — observed working in live fire
- **Stage 2 verified BROKEN** — code claims to be wired but observation contradicts
- **Stage 2 verified MISSING** — Daniel attempted to use the capability and there was nothing to use
- **Stage 2 NOT EXERCISED** — Daniel didn't test this; verification deferred

The combination of Stage 1 (code) + Stage 2 (observation) gives a confidence-graded fact map.

---

## Step 4 — Final report

`backend/G_D2_INVENTORY_REPORT.md` with these sections, in this order:

1. **Baseline status summary** — for each of the 8 baseline items, one-line status: "MET / NOT MET — reason"
2. **PROJECT_CLAUDE.md update confirmation** — show the new section that was added (verbatim)
3. **Stage 1 inventory** — eight subsections (2.1 through 2.8) plus 2.9 contradictions
4. **Stage 2 live-fire annotations** — each Stage 1 item annotated with what was observed
5. **The gap between current state and baseline** — short narrative, no spin: what specifically needs to be built/wired/fixed for baseline to be met
6. **Unblocking fixes log** — every fix Claude Code applied during the phase
7. **Helper logs index** — pointers to all five log files
8. **Vault SHA-1 verification** — start vs end (must be identical for all 5)
9. **Sacred floor verification** — 242/19/0 at start, 242/19/0 at end
10. **What this phase does NOT do** — explicit list (no fixes to scope-level findings, no new tests, no canon updates beyond Step 1's PROJECT_CLAUDE update, no follow-up phase drafts)

---

## Step 5 — Commits + push

Branch carries TWO commits maximum:

1. **Step 1 commit** — `PROJECT_CLAUDE: add baseline definition + architectural truth (G chain target)` — already done at end of Step 1
2. **Final commit** — `Phase G.D2: baseline inventory + live-fire diagnostic` — includes the report, all helper log files, any unblocking fixes, the deleted Helper 5 wrapper script (i.e., NOT committed because deleted before commit), Helper 3 middleware revert (also not committed)

Push:
```
git push -u origin phase2-v0.3-GD2-baseline-inventory
```

---

## Hard guardrails

1. **Vault: 5 trade modules unchanged at every checkpoint.** Any change = STOP, revert, restart.
2. **Sacred floor 242/19/0 at start and end.**
3. **No edits to dispatch_gate.py or pdf_engine.py.** Both integration-frozen this phase.
4. **No new pytest tests. No edits to existing tests.**
5. **Helper 3 middleware and Helper 5 instrumented HTML are TEMPORARY.** Both removed before final commit. Logs they produced ARE committed.
6. **Step 1's PROJECT_CLAUDE.md update is the ONLY canon update.** No CHECKLIST, ITINERARY, or BLOCK_RUN edits.
7. **No git imports in any helper code. No subprocess shelling out to git from Python.**
8. **Two commits maximum on this branch.**
9. **No follow-up phase drafts.**

---

## STOP conditions

1. Sacred floor regresses at start. Don't proceed.
2. Vault SHA-1 changes during the phase. Revert immediately, log, restart.
3. Stage 1 inventory tries to "verify" by running anything more than reading code. Stage 1 is read-only. If you find yourself wanting to import a module to introspect it, that's Stage 2 territory — defer.
4. An unblocking fix lands in `core/` outside what's already explicitly allowed. STOP, log the urge, revert.
5. Claude Code finds itself fixing scope-level behavior. Findings, not fixes.
6. Daniel says "stop" or "pause" at any point. Honor immediately.
7. The PROJECT_CLAUDE.md update at Step 1 turns into a multi-section rewrite. STOP. The directive is one new top section + a flag list of contradictions. Anything more is scope creep.
8. You start drafting a follow-up phase. Don't.

---

## Done when

- [ ] Branch `phase2-v0.3-GD2-baseline-inventory` exists
- [ ] PROJECT_CLAUDE.md updated with new top section, committed
- [ ] Stage 1 inventory complete for all 8 baseline items + contradictions subsection
- [ ] Stage 2 live-fire run with Daniel driving, all 6 helpers captured logs
- [ ] Each Stage 1 inventory entry has a Stage 2 annotation (or "NOT EXERCISED")
- [ ] `backend/G_D2_INVENTORY_REPORT.md` written
- [ ] All 6 helper log files present in `backend/`
- [ ] Helper 5 instrumentation wrapper script DELETED (not committed)
- [ ] Helper 3 API-intercept middleware REVERTED (not committed)
- [ ] Sacred floor 242/19/0 verified at end
- [ ] Five trade-module SHA-1s verified unchanged
- [ ] Two commits on branch
- [ ] Branch pushed
- [ ] Backend confirmed shut down
- [ ] Sign-out announcement: "Signed out as Developer. G.D2 inventory complete. PROJECT_CLAUDE.md updated. [N] of 8 baseline items MET. Report at `backend/G_D2_INVENTORY_REPORT.md`. Standing by."

---

## What this phase explicitly does NOT do

- Does NOT fix any scope-level finding
- Does NOT update CHECKLIST.md, ITINERARY.md, or BLOCK_RUN.md
- Does NOT add or modify any pytest tests
- Does NOT touch trade modules
- Does NOT touch dispatch_gate.py or pdf_engine.py
- Does NOT propose G.4 scope or any follow-up phase
- Does NOT declare anything "ships clean" — verdicts are factual labels (IMPLEMENTED+WIRED / IMPLEMENTED+UNWIRED / STUBBED / PARTIAL / MISSING) plus Stage 2 observation matches

---

**End of march orders. Update PROJECT_CLAUDE.md first. Then inventory. Then live-fire. Then report.**
