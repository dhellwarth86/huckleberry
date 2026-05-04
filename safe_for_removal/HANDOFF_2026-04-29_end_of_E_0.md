# HANDOFF — 2026-04-29 End of E.0

**Purpose:** Single document to bring any next session up to speed without re-reading every gate report. Read after PROJECT_CLAUDE.md and BLOCK_RUN.md.

---

## 1. Where the project is, in two sentences

Phase D (storage activation + module wiring + persistence) is complete. Phase E.0 (API design + frontend audit + v6.3.x housekeeping) is complete. Phase E.1 (FastAPI scaffold + first endpoints) march orders are drafted; ready to execute.

---

## 2. What shipped this week

- **Calibration session on Silverleaf** — Bug 1 (page-type ordering) and Bug 3 (tables plumbing) both fixed. Vault rule active throughout.
- **Phase D.1** — storage activated, RoofingModule + GlazingModule wired into `run_dispatch`, Silverleaf hard gate PASS.
- **Housekeeping safe_for_removal** — 53 retired files moved with manifest; recoverable.
- **Phase D.2 long-run chain** — job persistence layer, soft gate (10/10 round-trip assertions PASS), three-bidset hard gate (Bearss + Shoppes + Vine Street, 21/21 criteria PASS), byte-exact module output reproducibility vs sweep baseline.
- **Phase E.0** — frontend audit revealing ~1,320 lines of business logic in v6.3.5 duplicating backend functions; FastAPI design doc; v6.3.1-6.3.4 frontend HTMLs moved to safe_for_removal.

---

## 3. Where things stand right now

**Branch state:**
- All branches pushed to `https://github.com/dhellwarth86/huckleberry.git`
- Most-recent: `phase2-v0.3-E0-api-design-and-frontend-audit` head = E.0 commit per BLOCK_RUN.md Phase 5
- E.1 branch: `phase2-v0.3-E1-fastapi-scaffold` (NEW; created at execution time from E.0 head)

**Sacred floors at end of E.0:**
- Backend: 216 passed, 19 skipped, 0 failed
- Frontend: 138/138 against v6.3.5
- Five vault-ruled module SHA-1s captured and unchanged
- v6.3.5 SHA-1 captured and unchanged (audit was read-only)
- Four other frontend HTMLs (v6.3.1-6.3.4) moved to safe_for_removal/frontend_versions/

**Database state:**
- SQLite at `~/.tracepoint/cache.db`
- One Silverleaf reference job persisted from D.2 run; three more jobs persisted from D.2 hard gate (Bearss, Shoppes, Vine Street); E.0 added zero new jobs
- D.2 hard gate proved: persistence round-trips correctly; same job re-loaded after handle close/reopen produces byte-exact module output

**Vault rule active on:**
- `backend/core/roofing_module.py`
- `backend/core/glazing_module.py`
- `backend/core/roofing_vocabulary.py`
- `backend/core/glazing_vocabulary.py`
- `backend/core/debug_module.py`

**Frontend treatment:**
- `Huckleberry_AI_6.3.5_Scope.html` is canonical going forward
- v6.3.1-6.3.4 in `safe_for_removal/frontend_versions/` pending Daniel's eventual emptying of safe_for_removal/
- v6.3.5 vault-treated through Phase E.1 (E.2 strips it; E.0/E.1 leave it alone)

---

## 4. What's coming next

### Immediate (E.1)

**Phase E.1 — FastAPI scaffold + first endpoints.** Single session, autonomous, soft gates only.

Builds:
- FastAPI server scaffold under `backend/api/`
- POST /jobs (create) endpoint
- GET /jobs/{job_id} (load) endpoint  
- GET /health (exempt liveness probe)
- 6 new tests bringing backend 216 → 222
- Silverleaf single-bidset hard gate (3-bidset deferred to post-Phase-G)
- Three new deps: fastapi, uvicorn[standard], pydantic

Doesn't build:
- Authentication (deferred to Postgres/security phase)
- CORS lockdown (permissive in dev; locked at Postgres phase)
- File upload (deferred — string path for now; upload at Postgres migration; cloud when data volume requires)
- Other endpoints (E.2 / E.3 territory)
- Frontend changes (vault-treated through E.1)

**Soft gate after E.1.** Chain pauses for Daniel review.

### After E.1 (in order)

**E.2 — Frontend strip + connect.** Re-architecture, not refactor. Per E.0 audit, ~3,800-4,100 lines (~45% of v6.3.5) deletable. Likely sub-phased:
- E.2.0 — line-by-line strip plan
- E.2.1 — actual deletion + connect to API
- E.2.hard-gate — real bidset through full upload → display flow

**E.3 — Trade module output rendering + edit surface.** User can edit/correct annotations (groundwork for Phase F's three-state annotations).

### After E (parallel track before any future multi-bidset testing)

**Phase G — Quadrant smart scan.** PyMuPDF + Pandas + tiling at 200-300 DPI to reduce compute and improve drawing detection. Required before any future 3-bidset hard gate, sweep, or compute-heavy testing.

### After G

**Phase F — Auto-notation product.** Three-state annotations (gold / user-edited gold + correction logged / user-deleted with negative signal). Provenance. Training data loop via correction store.

### Post-user-testing security cluster (multi-phase)

- Authentication implementation (USERS table, JWT or session)
- CORS lockdown
- OpenAPI docs hide
- Postgres migration from SQLite
- File upload + local disk save → cloud when data volume requires
- Settings/Developer tables
- PROJECT_SCOPE_BY_TRADE rollup table

---

## 5. Six locked decisions from E.0 review

These came from rapid-fire Q&A after E.0 ship. Locked into E.1 march orders.

| # | Decision | E.1 dev | Postgres/security phase |
|---|---|---|---|
| 1 | PDF input | string path | upload to local disk → cloud later |
| 2 | CORS | permissive | locked down |
| 3 | /health | exempt from budget | (stays exempt) |
| 4-5 | Test count | 222 floor (6 new tests) | grows organically |
| 4-5 | Data leak test | option 1+2 combined | (stays) |
| 5 | status validation | strict via Literal | (stays) |
| 6 | OpenAPI docs | exposed at /docs and /redoc | hidden |
| (extra) | DB location | ~/.tracepoint/cache.db | move to backend/ |
| (extra) | E phases | soft gate between sub-phases | — |
| (extra) | Multi-bidset testing | single-bidset only until Phase G | — |

---

## 6. Discipline rules in effect

These apply to every session for the foreseeable future:

1. **Vault rule.** Five trade modules + the v6.3.5 frontend HTML have SHA-1s captured at session start, verified at session end. Any change is a §7 stop.
2. **Sacred floors.** Backend 216/19/0 (will be 222/19/0 after E.1 ships). Frontend 138/138 against v6.3.5. Hard stop on regression.
3. **CLAUDE.md retired.** Do not open. Do not edit. Do not reference. PROJECT_CLAUDE.md is the canonical entry point.
4. **PROJECT_CLAUDE.md surgical edits only.** Each phase touches §3 (state paragraph append) and §7 (phase table) typically. Other sections require explicit authorization.
5. **No new tests outside scope.** Each phase specifies test count delta. Adding more is scope creep.
6. **Soft-gate-with-Daniel-review between every E sub-phase.** No auto-continuing across re-architecture work.
7. **No multi-bidset hard gates until Phase G ships.** Single-bidset Silverleaf is the only hard gate anywhere in E.

---

## 7. Open items / debt to track

- v6.3.5 status bar copy reads "AI BACKEND: REMOVED / 100% OFFLINE · CLIENT-SIDE" — load-bearing-incorrect after E.2 strips the JS pipeline. Schedule update in E.2 or E.3.
- `npm run test:spotchecks` will fail because spotcheck scripts reference moved HTMLs. The 138/138 floor (`npm test`) is unaffected. Cleanup deferred to next frontend-touching session.
- Three intake-diagnostic JSONs in `backend/test_fixtures/` are technically gitignored-on-paper but not in `.gitignore`. Won't break anything; cleanup folds into next housekeeping pass.
- E.0 audit revealed v6.3.5's TP namespace is a complete JS port of the backend pipeline (~830 lines). E.2 needs to handle this carefully — full deletion may break manual annotation tools that still depend on parts of TP.

---

## 8. Files to read in any next session

**Always read first (every session):**
1. `PROJECT_CLAUDE.md`
2. `backend/BLOCK_RUN.md`

**For E.1 execution specifically:**
3. `MARCH_ORDERS_E_1_fastapi_scaffold.md` (the active phase orders)
4. `backend/E0_API_DESIGN.md` (the design contract E.1 builds against)
5. `backend/E0_FRONTEND_AUDIT.md` (E.2 context, helpful for understanding what's coming)

**For deep state recall:**
6. `backend/D2_MASTER_GATE_REPORT.md`
7. `backend/D_HARD_GATE_silverleaf.md`
8. `backend/CALIBRATION_GATE_REPORT_silverleaf.md`
9. `VALIDATION_LEDGER.md` (sacred floors, vault list, decisions)

---

## 9. Standing by

E.1 march orders ready. Daniel green-lights → Claude Code executes. Single session. Soft gate to E.2 after.

**End of HANDOFF_2026-04-29_end_of_E_0.md.**
