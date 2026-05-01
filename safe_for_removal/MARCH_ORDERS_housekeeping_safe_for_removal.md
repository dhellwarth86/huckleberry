# MARCH ORDERS — Housekeeping: safe_for_removal Sweep

**Date issued:** 2026-04-29
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** Single session, autonomous, soft-gates-only, single final gate report
**Phase scope:** Move retired / no-longer-needed files into a `safe_for_removal/` folder. Generate a manifest documenting what was moved, why, and what each file's purpose was. No production-code touches. No vault-ruled file touches. No frontend touches.
**Read first:** PROJECT_CLAUDE.md, BLOCK_RUN.md, then this document

---

## §0 — What this phase is

**A pure organizational sweep.** Workspace has accumulated retired / orphaned / no-longer-needed files across multiple phases. Before D.2 starts, we collect them into one folder so they:

1. Stop cluttering the workspace
2. Don't get accidentally referenced by future sessions
3. Stay recoverable if something turns out to still be needed
4. Can be reviewed by Daniel at his pace
5. After review and deletion, the folder's manifest becomes a wiki for "what was retired, why, and what to look at if I'm debugging something old"

**The discipline:** files MOVE to `safe_for_removal/`. Files do not get DELETED in this session. Daniel reviews the folder after this session ships, confirms no critical content lives in it, and then the folder gets removed in a later session. The manifest survives the deletion as the wiki source.

**This is NOT:**
- A code refactor
- A test cleanup
- A vault-ruled module touch
- A frontend touch
- A canonical doc edit (PROJECT_CLAUDE.md gets one tiny note about safe_for_removal/'s creation; that's it)

---

## §1 — Pre-flight reads (Karpathy step 1)

Full reads, in this order:

1. **PROJECT_CLAUDE.md** — entry point. §3 names every artifact created across phases; §4 names sacred and vault-ruled files. The retire-decisions in this session must be cross-checked against §3 and §4.
2. **BLOCK_RUN.md** — Phase 1 + Phase 2 entries list every file created in the last two sessions. Cross-check before retiring anything.
3. **VALIDATION_LEDGER.md** — §A files (sacred), §G vault-ruled list, §H decisions list. These three sections name what cannot be moved.

That's enough. Do not open `dispatch_gate.py`, `trade_module.py`, or any other production code in `backend/core/` — this session does not touch production code.

---

## §2 — Step HK.0: Pre-flight verification

- Run the full backend test suite. Floor: **216 passed, 19 skipped, 0 failed**. Hard stop if not met.
- Capture pre-session SHA-1s for all five vault-ruled modules:
  - `backend/core/roofing_module.py`
  - `backend/core/glazing_module.py`
  - `backend/core/roofing_vocabulary.py`
  - `backend/core/glazing_vocabulary.py`
  - `backend/core/debug_module.py`
- Capture pre-session SHA-1s for every frontend HTML in the workspace tree (`Huckleberry_AI_6.3.1_Scope.html` through `6.3.5_Scope.html` per BLOCK_RUN.md Phase 2 entries). All five SHA-1s captured for end-of-session verification.
- Verify branch state:
  - `phase2-v0.3-D1-storage-and-module-wiring` head matches the pushed remote SHA per BLOCK_RUN.md.
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git`.

If any pre-flight check fails, **§7 stop**.

---

## §3 — Step HK.1: Branch + create folder

Branch from D.1 head:

```
phase2-v0.3-housekeeping-safe-for-removal  (NEW; from D.1 head)
```

Create the directory `safe_for_removal/` at workspace root. Add a `safe_for_removal/README.md` with this content (verbatim):

```markdown
# safe_for_removal/

This folder collects files that are no longer needed for active development as of 2026-04-29.

## What's in here

Each subdirectory contains files retired from active use, grouped by category. Each file in a subdirectory has a corresponding entry in `MANIFEST.md` describing:

- What the file was
- When it was active
- Why it's retired
- What replaced it (if anything)
- What to look at if you encounter related issues

## What this folder is for

Daniel reviews this folder at his pace to confirm nothing critical is in here. After review:

1. If something here turns out to still be needed, move it back out (this folder is not deleted yet)
2. Once Daniel confirms everything here is safe, the folder gets removed in a future session
3. The MANIFEST.md is preserved (copied out before deletion) and converted into a wiki — "what was retired and why, useful for debugging old issues"

## What this folder is NOT for

- Vault-ruled production modules (roofing_module, glazing_module, roofing_vocabulary, glazing_vocabulary, debug_module) — these stay in `backend/core/`
- Sacred files (frontend HTMLs, TracePoint reference sources, seed files) — these stay in their canonical locations
- Active march orders or canonical documentation (PROJECT_CLAUDE.md, VALIDATION_LEDGER.md, BLOCK_RUN.md, current march orders) — these stay in workspace root or `backend/`
- Active test fixtures actually used by the test suite (216 backend tests) — these stay where the test runner expects them

## Subdirectories

(populated as work proceeds; each subdirectory category named in MANIFEST.md)

---

This folder exists temporarily. Last reviewed: pending.
```

---

## §4 — Step HK.2: Inventory and categorize

Walk the workspace tree (excluding `.git`, `node_modules`, `tracepoint_port/TracePoint/`, `backend/seeds/`, and `backend/core/`) and produce an inventory. For each file or directory, decide one of three statuses:

- **KEEP** — actively needed for development, testing, or as canonical reference
- **MOVE TO safe_for_removal/** — retired, orphaned, or accumulated dirt
- **AMBIGUOUS** — could be either; surface to Daniel before moving

**Files that ALWAYS keep (do not move under any circumstance):**

| Category | Files | Why |
|---|---|---|
| Vault-ruled production modules | `backend/core/roofing_module.py`, `backend/core/glazing_module.py`, `backend/core/roofing_vocabulary.py`, `backend/core/glazing_vocabulary.py`, `backend/core/debug_module.py` | Vault rule (Decision 15 retired CLAUDE.md, but the vault rule itself is permanent — see §G of VALIDATION_LEDGER.md) |
| Active production code | All other `backend/core/*.py` (`dispatch_gate.py`, `trade_module.py`, `trade_input_builder.py`, `context.py`, `storage.py`, `pdf_engine.py`, `architect_profile.py`, `correction_store.py`, etc.) | Production |
| TracePoint reference | All of `tracepoint_port/TracePoint/` | Sacred read-only reference |
| Seeds | All of `backend/seeds/` | Sacred |
| Active tests | `backend/tests/` (the 216 test suite) | Sacred — never move test files |
| Frontend HTMLs | `Huckleberry_AI_6.3.1_Scope.html` through `6.3.5_Scope.html` | Vault-treated for Phase D per Daniel directive |
| Canonical docs | `PROJECT_CLAUDE.md`, `VALIDATION_LEDGER.md`, `BLOCK_RUN.md` | Active canon |
| Latest handoff | `HANDOFF_FINAL_2026-04-28.md` (or whatever the current latest is) | Active state record |
| Active scripts | `backend/scripts/calibrate_silverleaf.py`, `backend/scripts/d1_silverleaf_hardgate.py`, `backend/scripts/profile_diagnostic.py`, `backend/scripts/page_type_verification.py` | Tracked, reusable diagnostic harnesses |
| Active reports | All `backend/CALIBRATION_*.md`, `backend/D_HARD_GATE_*.md`, `backend/PROFILE_DIAGNOSTIC_*.md`, `backend/PAGE_TYPE_VERIFICATION_*.md`, `backend/SWEEP_OBSERVATION_*.md`, `backend/C5_DEBUG_RUN_THROUGH_*.md`, `backend/C3_GLAZING_SEED_VALIDATION.md`, `backend/DEBUG_MODULE_REPORT.md`, `backend/CROSS_TRADE_INTEGRATION_NOTES.md`, `backend/DISCOVERED_ISSUES.md` | Active receipts |
| Current march orders | `MARCH_ORDERS_phase_D1.md`, this housekeeping orders file | Active |
| pyproject.toml + requirements | All dependency manifests | Active |

**Files that ARE candidates for safe_for_removal/:**

Categories to walk through with a critical eye:

1. **Old march orders that have completed.** ALL `MARCH_ORDERS_*.md` files for completed phases EXCEPT the most-recent two (D.1 and this housekeeping doc). C.1, C.2, C.3a, C.3b, C.3c-build, C.5, sweep, profile, page-type-verification, calibration. These march orders have shipped; their gate reports persist; the orders themselves are historical. Move to `safe_for_removal/march_orders/`.

2. **Old handoff documents.** Any `HANDOFF_*.md` other than the most recent. Move to `safe_for_removal/handoffs/`.

3. **`previous handoff/` directory at workspace root.** This is where Daniel moved CLAUDE.md and other archive material. The directory itself is retired-by-intent. Move to `safe_for_removal/previous_handoff/`.

4. **`previous orders/` directory at workspace root.** Same shape. Move to `safe_for_removal/previous_orders/`.

5. **The anomalous nested `huckleberry/` git repo at workspace root** (the soft-observation flagged in profile-and-housekeeping session). It has its own `.git/` and empty working tree. Move the whole directory to `safe_for_removal/anomalous_nested_repo_huckleberry/`. **Document in MANIFEST.md that it has its own `.git` directory** so Daniel knows what he's looking at when reviewing.

6. **Old intake-diagnostic outputs** in `backend/test_fixtures/intake_diagnostic_outputs/` plus the two summary JSONs (`intake_diagnostic_summary.json`, `intake_diagnostic_pass2_summary.json`). VALIDATION_LEDGER.md §H documents them as "gitignored on Daniel's machine" — but they're not actually gitignored, they sit untracked. They're one-shot diagnostic dumps from sessions that have shipped. Move to `safe_for_removal/intake_diagnostic_outputs/`.

7. **Step-by-step orders files (STEP_*.md)** if any survive. These were the older B.1/B.2/B.3/B.4 sub-phase guidance docs. Move to `safe_for_removal/step_by_step_orders/`.

8. **Any one-shot validation file from before B.4 ship.** `V0_2_VALIDATION.md` and similar pre-Phase-B reports. Move to `safe_for_removal/pre_phase_B_validation/`.

9. **Old terminal logs** (`*_terminal.log` or `terminal.log` files older than the page-type verification one). Move to `safe_for_removal/old_terminal_logs/`.

10. **One-shot scripts that have been superseded by tracked harnesses.** Specifically: any `c5_run_through.py`, any `sweep_three_bidsets.py` (these were intentionally untracked one-shots; if they exist in the working tree, move to `safe_for_removal/superseded_scripts/`).

**Ambiguous categories — DO NOT MOVE without surfacing as a soft observation in the gate report:**

- Any file in `backend/` whose purpose isn't obvious from name or directory location
- Any file referenced by name in PROJECT_CLAUDE.md or VALIDATION_LEDGER.md (a name-reference means it's still considered active)
- Any `.gitignore` file or `.gitattributes` file (config; leave alone)
- Any markdown file in `backend/` that describes architecture that may still be referenced (e.g., `CROSS_TRADE_INTEGRATION_NOTES.md` is active per the keep-list)

If you're unsure: **leave it where it is** and add a row to the gate report's "Ambiguous — left in place, surfacing for Daniel review" section.

---

## §5 — Step HK.3: Move and document

For each file or directory marked "MOVE":

1. `git mv` the file (preserves history) to its target subdirectory under `safe_for_removal/`.
2. Append an entry to `safe_for_removal/MANIFEST.md` (created if not yet existing) using this format:

```markdown
## <filename>

**Original path:** `<full path before move>`
**New path:** `safe_for_removal/<subdir>/<filename>`
**Category:** <one of: completed_march_orders, completed_handoffs, archived_canon, anomalous_nested_repo, intake_diagnostic_outputs, step_by_step_orders, pre_phase_B_validation, old_terminal_logs, superseded_scripts, other>
**When active:** <date range or "before <date>" if unknown>
**Purpose when active:** <one-sentence description>
**Why retired:** <one-sentence reason>
**What replaced it (if anything):** <name of replacement file or "nothing — pre-Phase-B artifact" or "shipped, no replacement needed">
**What to look at if related issues surface:** <name of current canonical doc or report that covers the same territory>

---
```

The MANIFEST.md is the artifact that survives the eventual deletion of `safe_for_removal/`. After Daniel removes the folder, the MANIFEST.md gets copied out and converted to a wiki. So write entries with that future use in mind: **someone debugging in 2027 should be able to read an entry and understand what they need to know.**

---

## §6 — Step HK.4: Update PROJECT_CLAUDE.md (one tiny note)

Single surgical edit to PROJECT_CLAUDE.md §3:

Append one new paragraph at the end of §3 (before the "For full state detail" closer):

```
**Workspace housekeeping complete (2026-04-29):** Retired / no-longer-needed files moved to `safe_for_removal/` folder per `MARCH_ORDERS_housekeeping_safe_for_removal.md`. Manifest at `safe_for_removal/MANIFEST.md` documents what was moved, why, and what to look at if related issues surface. The folder will be removed in a future session after Daniel reviews; the MANIFEST.md is preserved as a wiki source. Tracked branch: `phase2-v0.3-housekeeping-safe-for-removal` from D.1 head.
```

Do NOT modify §1, §2, §4, §5, §6, §7, §8, §9, §10. Single-paragraph append to §3 only.

---

## §7 — Step HK.5: Update BLOCK_RUN.md

In `BLOCK_RUN.md`, append a new section between Phase 2 and Phase 3:

```markdown
## Phase 2.5: Housekeeping — safe_for_removal sweep (2026-04-29)

**Branch:** `phase2-v0.3-housekeeping-safe-for-removal` (from D.1 head)
**Trigger:** Daniel directive 2026-04-29 — clear retired files into safe_for_removal/ folder before D.2 starts; manifest preserves recovery info; folder reviewed and deleted in future session, manifest preserved as wiki source.
**Scope discipline:** No production-code touches; no vault-ruled module touches; no frontend touches; no test suite touches; no canonical doc edits beyond a single PROJECT_CLAUDE.md §3 paragraph.

### Files created
- `safe_for_removal/` (new directory at workspace root)
- `safe_for_removal/README.md`
- `safe_for_removal/MANIFEST.md`
- (subdirectories per category — populate at session end)

### Files moved
(populate at session end with full git mv list)

### Files modified
- `PROJECT_CLAUDE.md` — single new paragraph appended to §3 (housekeeping complete note)

### Files deleted
None this session. (Files in safe_for_removal/ pending Daniel review before deletion.)

### Commits
(populate at session end)

### Pushes
(populate at session end)

### Vault-ruled files touched
None. SHA-1 verification at session end (matches pre-session captured at HK.0).

### Frontend touched
None. SHA-1 verification at session end.

### Sacred floor at session end
Backend 216/19/0 (verified pre-flight; not re-run if no test files moved). Frontend at baseline (SHA-1 verified).
```

Populate the "Files moved" and "Commits" / "Pushes" sections at session end.

---

## §8 — Step HK.6: Sacred floor verification

Before commit:
- Run backend test suite. **216/19/0 must hold.** If it doesn't, something got moved that shouldn't have. **§7 stop, investigate, restore.**
- Verify all five vault-ruled module SHA-1s match pre-session.
- Verify all frontend HTML SHA-1s match pre-session.

If any verification fails, **§7 stop** — do not commit a regressed state.

---

## §9 — §7 Stop Conditions

Stop, report, wait for Daniel if any fire:

1. **Sacred floor regresses.** Backend below 216/19/0. Hard stop. Restore moved files until tests pass again.
2. **Vault-ruled module SHA-1 changes.** Hard stop. (Should be impossible since this session does not open them, but verifying.)
3. **Frontend HTML SHA-1 changes.** Hard stop.
4. **A move turns out to break something** (an import, a test, a build). Hard stop; restore the moved file.
5. **Inventory surfaces a file whose category is genuinely unclear** AND the file is meaningfully large or load-bearing-looking. Hard stop, list, ask. (Small ambiguous files just get left in place per §4 instruction.)
6. **PROJECT_CLAUDE.md edit exceeds the single-paragraph append** to §3. Hard stop.
7. **Total file count moved exceeds 100.** This is not by itself wrong, but is high enough that Daniel should be aware before commit. Soft observation in gate report at >50; hard stop at >100.
8. **A canonical doc reference points to a file in the move list.** I.e., PROJECT_CLAUDE.md says "see X.md" and X.md is being moved. Hard stop. Either the canonical reference needs updating (which is out of scope this session) or the file shouldn't be moved.

---

## §10 — Discipline reminders

1. **Read first.** PROJECT_CLAUDE.md, BLOCK_RUN.md, VALIDATION_LEDGER.md before any moves.
2. **Sacred floor first.** 216/19/0 before, after, before commit, before push.
3. **Minimum implementation.** This is a sweep, not a refactor. Move files. Document them. Stop.
4. **Vault rule held.** Five trade modules + five frontend HTMLs untouched and not opened.
5. **No production-code edits.** Not even comments. The only file modified is `PROJECT_CLAUDE.md` (one paragraph) and `BLOCK_RUN.md` (one section).
6. **`git mv` not `git rm` + create.** History preservation matters for the eventual wiki conversion.
7. **MANIFEST.md is the load-bearing artifact.** Write entries for future-you. The folder gets deleted; the manifest survives. If an entry would be useless without the file alongside it, rewrite the entry.

---

## §11 — Done definition (gate report checklist)

The final gate report (`backend/HOUSEKEEPING_GATE_REPORT.md`) must confirm:

- [ ] Pre-flight: 216/19/0 backend; vault SHA-1s captured; frontend SHA-1s captured; branch correct
- [ ] Branch `phase2-v0.3-housekeeping-safe-for-removal` from D.1 head
- [ ] `safe_for_removal/` directory created at workspace root
- [ ] `safe_for_removal/README.md` created with the verbatim text from §3
- [ ] `safe_for_removal/MANIFEST.md` created with one entry per moved file
- [ ] N files moved via `git mv` (list with categories)
- [ ] No production code modified (verified by `git diff --stat backend/core/`)
- [ ] No test files moved (216/19/0 still passes)
- [ ] No vault-ruled module SHA-1 change
- [ ] No frontend SHA-1 change
- [ ] PROJECT_CLAUDE.md updated with single §3 paragraph append (no other edits)
- [ ] BLOCK_RUN.md Phase 2.5 section populated
- [ ] Single commit on `phase2-v0.3-housekeeping-safe-for-removal`; pushed to origin
- [ ] §7 stops: status of each enumerated explicitly
- [ ] Final gate report produced
- [ ] List of "Ambiguous — left in place, surfacing for Daniel review" files (if any)

---

## §12 — Commit shape

**Single commit** on `phase2-v0.3-housekeeping-safe-for-removal`:

- `safe_for_removal/README.md` (NEW)
- `safe_for_removal/MANIFEST.md` (NEW)
- `safe_for_removal/<category>/*` (multiple — git mv from original locations)
- `PROJECT_CLAUDE.md` (MODIFIED — §3 single paragraph append)
- `BLOCK_RUN.md` (MODIFIED — Phase 2.5 section added)
- `backend/HOUSEKEEPING_GATE_REPORT.md` (NEW — gate report)

Commit message body:
- "Housekeeping: move retired files to safe_for_removal/ before D.2"
- File count moved
- Categories of moves (one line each)
- "No production code modified; no vault-ruled / frontend / sacred files touched; backend 216/19/0 held"
- "Manifest preserved for future wiki conversion"

Push at end of session. Authorized.

---

## §13 — Execution mode

**Single chunk, autonomous, soft gates only.** Run HK.0 through HK.6 without per-step confirmation. Single final gate report at end.

§7 stops are the only hard pauses.

Total wall-clock estimate: ~30 minutes. Pre-flight reads, inventory walk, git mv operations, MANIFEST.md drafting (the longest part), surgical doc updates, commit, push.

---

## §14 — Closing

After this phase ships, **Daniel reviews `safe_for_removal/` at his pace.** He confirms nothing critical lives in it (or pulls items back out if needed). When he's confirmed, a future short session removes the folder. Before deletion, the MANIFEST.md is copied out (probably to `backend/RETIRED_FILES_WIKI.md` or similar) and becomes the wiki artifact.

The next phase after this is **D.2 — job folder + sortable-by-GC identity + schema migration.** D.2's march orders get drafted by extended-thinking Claude after this housekeeping session ships.

Standing by for execution.

**End of MARCH_ORDERS_housekeeping_safe_for_removal.md.**
