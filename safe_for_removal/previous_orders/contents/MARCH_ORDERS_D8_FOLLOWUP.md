# D-8 Follow-Up + Trade-Module Vault Rule Extension

**Authored:** 2026-04-28 end-of-day
**Authority:** Daniel
**Predecessor:** C.3b (commits `7ea9abb` + `14f4f53` on branch `phase2-v0.3-C3b-glazing-vocabulary`). Sacred floor at session start: backend 214/19/0, frontend 107 + spotchecks + 8/8 mutations.
**Discipline:** read-only verification + minimal documentation patches. Same Karpathy discipline as the bookkeeping and C.3a/debug-spec sessions. No production code modified. No port executed. No new tests. No new dependencies.
**Expected wall-clock:** ~30–45 minutes.

---

## 0. Context

This brief covers three small tasks that surfaced from the C.3b ship and Daniel's subsequent direction:

1. **D-8 documentation patch.** The C.3a inventory miscounted parked-seed component count (60 vs actual 64) and system count (21 vs actual 23). The seeds did not move (SHA-1 unchanged). The C.3a verdict and gap list don't depend on exact counts, but the inventory table needs correction so future reads of the document don't carry the error forward.

2. **Gap-list re-verification.** Before C.3c builds GlazingModule on top of C.3a evidence, confirm the 4 components, 4 systems, 1 hardware set, and 5 manufacturers C.3b added are genuinely missing from the parked seeds (not duplicates under different names). Read-only check.

3. **Trade-module vault-rule extension.** Daniel's directive 2026-04-28: trade modules ship rough, then get vault-ruled when sealed. The vault rule (currently scoped to TracePoint's debug module per CLAUDE.md §3 Decision 15) extends to cover trade modules. Apply retroactively to RoofingModule (C.2) and glazing_vocabulary (C.3b). Apply forward to GlazingModule when C.3c ships.

All three tasks are documentation work. No production code changes. Sacred floor must hold.

---

## 1. The Vault-Rule Extension Principle (For Documentation)

This is the principle Daniel articulated 2026-04-28; it gets written into CLAUDE.md §3 Decision 15 as the extension:

> Trade modules ship "rough" — best-effort first pass against the contract, with vocabulary and logic that's reasonable but not fine-tuned against real bidsets. They get vault-ruled at the end of their rough-ship phase. After vault-rule application, the module is frozen as a stable observer/extractor in the same status as TracePoint's debug module relative to its core pipeline. Future fine-tuning happens in separate sessions where the module is the editing target and the rest of the pipeline is frozen, OR in completely new module versions, not by silently editing the frozen one.
>
> The reason: rough modules are diagnostic surfaces. We learn what they get right and what they get wrong by running them against real bidsets and observing outputs. If they are tuned in the same session that we learn their behavior, prior diagnostic findings become stale and the module loses its value as a stable observer of what the pipeline produces.
>
> Application:
> - **Vault-ruled retroactively (2026-04-28):** RoofingModule (C.2 commit `74772b6`), glazing_vocabulary.py (C.3b commit `14f4f53`)
> - **Vault-ruled when sealed:** GlazingModule (C.3c future), and every future trade module
> - **Tuning sessions:** dedicated, separate from core/ work, with the relevant module as the only editing target and core/ files frozen
> - **Contract evolution:** Protocol and Input/Output dataclasses CAN be extended additively (as `TradeModuleInput.tables` was in C.3b) when multi-trade reality requires; vault rule applies to module behavior, not to contract evolution

The wording above is what should land in CLAUDE.md.

---

## 2. Sacred Floor

| Suite | Count |
|---|---:|
| Frontend `run_tests.js` | 107/107 |
| Frontend spotchecks (4) | all pass |
| Frontend `mutation_test_step11.js` | 8/8 mutations caught |
| Backend full suite | 214 passed, 19 skipped, 0 failed |

Hold each line. Verify before, verify after. Same as every other session.

---

## 3. Constraints

### 3.1 — Authorized to modify

- `backend/C3_GLAZING_SEED_VALIDATION.md` — fix Section 1 inventory counts (60→64 components, 21→23 systems) and any per-section enumeration cell that miscounted. Do NOT change the verdict (Section 5) or the gap list (which lives within Section 5).
- `CLAUDE.md` — extend Section 3 Decision 15 to cover trade modules per §1 above. Single targeted edit; do NOT touch any other section.
- `PROJECT_CLAUDE.md` — minor consistency edits only if §6 ("Things that are NOT what someone might think") references the parked-glazing-seed counts. If it does, correct them. If it doesn't reference counts, leave it untouched.

### 3.2 — Sacred (do not modify)

- All TracePoint sources at `tracepoint_port/TracePoint/`
- Phase 1 frontend HTML and all frontend tests
- All v0.2 / B.1 / B.2 / B.3 / B.4 / C.1 / C.2 / C.3b ported and built files (including `backend/core/trade_module.py`, `roofing_module.py`, `roofing_vocabulary.py`, `trade_input_builder.py`, `glazing_vocabulary.py`)
- `backend/seeds/glazing_assemblies.py` and `glazing_materials.py` — PARKED, read-only this session (we're verifying counts, not editing)
- All other seed files
- `shared/bidset_record.py`
- All other `MARCH_ORDERS_*.md`, `STEP_*.md`, `DISCOVERED_ISSUES.md` (already sacred per C.3b §4.1), `V0_2_VALIDATION.md`, `VALIDATION_LEDGER.md`, `HANDOFF_*.md`, observation/diagnostic docs (other than C3_GLAZING_SEED_VALIDATION.md which is authorized to fix)
- `backend/core/__init__.py` (empty)
- `dispatch_gate.py` activation gates

### 3.3 — Do not expand scope

- DO NOT modify any production code in `backend/core/` or `backend/tests/`
- DO NOT modify any seed file
- DO NOT modify any C.3b commit
- DO NOT add new manufacturers/systems/components/relationships beyond what C.3b already shipped
- DO NOT propose tuning of RoofingModule or glazing_vocabulary in this session — that's the explicit OPPOSITE of what the vault-rule extension says
- DO NOT activate any trade module in dispatch_gate
- DO NOT touch frontend code
- DO NOT add new dependencies

### 3.4 — Karpathy procedure

- Read first: existing C.3a document, parked seeds (re-read), CLAUDE.md §3 Decision 15 current text
- Verify: count comparisons are mechanical, do them mechanically (Python `len()` calls, not eyeball)
- Sacred floor held at every checkpoint
- §7 stops: surface; do not silently resolve

### 3.5 — Autonomous execution

Single session, three sequential tasks. Substantive gates only. ONE final gate report.

---

## 4. Tasks

### Task 1 — Re-verify parked-seed counts mechanically

**Read:** `backend/seeds/glazing_assemblies.py` (1,311 lines) and `backend/seeds/glazing_materials.py` (264 lines).

**Verify mechanically (no writes):**

```python
from seeds.glazing_assemblies import (
    GLAZING_COMPONENTS, GLAZING_SYSTEMS, HARDWARE_SETS,
    ASSEMBLY_RELATIONSHIPS, FBC_CONSTRAINTS,
)
from seeds.glazing_materials import (
    SPEC_SECTIONS, MANUFACTURERS, MATERIAL_PROPERTIES, GLAZING_PIN_TYPES,
)

print("PARKED SEED COUNTS (mechanical):")
print(f"  GLAZING_COMPONENTS:        {len(GLAZING_COMPONENTS)}")
print(f"  GLAZING_SYSTEMS:           {len(GLAZING_SYSTEMS)}")
print(f"  HARDWARE_SETS:             {len(HARDWARE_SETS)}")
print(f"  ASSEMBLY_RELATIONSHIPS:    {len(ASSEMBLY_RELATIONSHIPS)}")
print(f"  FBC_CONSTRAINTS:           {len(FBC_CONSTRAINTS)}")
print(f"  SPEC_SECTIONS:             {len(SPEC_SECTIONS)}")
print(f"  MANUFACTURERS:             {len(MANUFACTURERS)}")
print(f"  MATERIAL_PROPERTIES (top): {len(MATERIAL_PROPERTIES)}")
print(f"  GLAZING_PIN_TYPES:         {len(GLAZING_PIN_TYPES)}")
```

**Record the actual counts.** These become the corrected Section 1 inventory in C.3a.

**Internal gate:** Counts recorded mechanically (not eyeballed). Discrepancies vs C.3a's claimed counts noted.

### Task 2 — Re-verify the C.3b gap list against parked seeds

For each of the 14 entries C.3b added, confirm it's genuinely missing from the parked seeds (not a duplicate under a different name).

**Components C.3b added:** `hw_deadbolt`, `hw_latch_guard`, `hw_door_viewer`, `flashing_drip_cap`

For each: search the parked `GLAZING_COMPONENTS` keys for any entry whose key OR description text matches the same physical item. Examples to check:
- "deadbolt" — any entry with "deadbolt", "dead bolt", or auxiliary lock?
- "latch guard" — any "latch_guard", "latch_protector", "strike_protector"?
- "door viewer" — any "viewer", "peephole", "peep_hole", "door_eye"?
- "drip cap" — any "drip_cap", "drip_edge", "head_flashing" (note: parked seed has `head_flashing` per C.3a §4.4 hardware set comparison — confirm whether `flashing_drip_cap` is genuinely distinct or duplicates `head_flashing`)

**Systems C.3b added:** `entrance_medium_stile_single`, `entrance_narrow_stile_single`, `entrance_wide_stile_single`, `window_storefront_panel`

For each: search parked `GLAZING_SYSTEMS` keys for any entry that's the single-leaf variant under a different name. Pair variants (`entrance_*_pair`) confirmed present per C.3a; confirm singles are genuinely absent. For `window_storefront_panel`, confirm it's distinct from `window_aluminum_fixed` and not duplicating any existing `storefront_*` entry.

**Hardware set C.3b added:** `hw_entrance_single_medium_stile_egress`

Search parked `HARDWARE_SETS` for any entry that combines single-leaf + storefront-style + panic. Per C.3a §4.4, the closest existing entry was `hw_exterior_single_egress` which is HM-flavored, not aluminum-storefront-flavored. Confirm.

**Manufacturers C.3b added:** `Cal Royal`, `Yale Security`, `Sargent`, `Schlage`, `Von Duprin`

For each: search parked `MANUFACTURERS` keys, alias lists, and product lists for any mention of these brand names. Per C.3a, the parked seed had no hardware OEM entries; confirm.

**For each entry, record one of:**
- ✓ confirmed missing (genuine addition)
- ⚠ duplicate of existing parked entry under different name (specify which) — would be a §7 stop
- ? ambiguous: similar concept but not exactly the same — specify the existing entry it's near

**Internal gate:** All 14 entries classified. Any ⚠ findings are §7 stops.

**§7 stop only if:** any C.3b addition turns out to be a duplicate of an existing parked entry. Surface for Daniel — the C.3b commit `14f4f53` may need amendment, OR the parked entry may need renaming, OR both. Stop and ask before any code change.

### Task 3 — Patch C3_GLAZING_SEED_VALIDATION.md

Apply Section 1 count corrections per Task 1 results.

Specifically, the Section 1 table currently shows:
- `GLAZING_COMPONENTS | 60`
- `GLAZING_SYSTEMS | 21`

Update to actual values from Task 1 (likely 64 and 23, but verify).

If Section 1's per-row description text references "60 components" or "21 systems" anywhere in narrative form, correct those references too.

**Do NOT change:**
- Section 2 (bidset chosen) — unaffected
- Section 3 (glazing pages identified) — unaffected
- Section 4 (term-by-term comparison) — unaffected
- Section 5 (verdict) — verdict doesn't depend on exact counts; explicitly preserve
- Section 5's gap list — preserved unless Task 2 surfaces a duplicate, in which case STOP per §7
- Section 6 (non-conclusions) — unaffected

Add a single editor's note to the bottom of Section 1:

> *Editor's note (2026-04-28): the original C.3a draft inventoried `GLAZING_COMPONENTS` and `GLAZING_SYSTEMS` counts incorrectly (60 / 21 instead of actual 64 / 23). Counts above corrected after mechanical re-verification during the D-8 follow-up session. The verdict (Section 5) and gap list do not depend on exact counts and are preserved as originally drafted. SHA-1 of both seed files is unchanged from the original C.3a inventory.*

### Task 4 — Extend CLAUDE.md §3 Decision 15 to cover trade modules

Locate Decision 15 in CLAUDE.md §3. Current text (paraphrased from PROJECT_CLAUDE.md §6 reference):

> "The vault rule. From TracePoint paper §7.5: the debug module must not be modified in the same session that modifies core pipeline files. Adopted as Huckleberry-wide for any diagnostic instrumentation."

Extend with the trade-module application per §1 of this brief. The full extended decision should read approximately:

> **15. The vault rule.** From TracePoint paper §7.5: the debug module must not be modified in the same session that modifies core pipeline files. Adopted as Huckleberry-wide for any diagnostic instrumentation, including trade modules.
>
> **Trade-module application (2026-04-28).** Trade modules ship "rough" — best-effort first pass against the contract, with vocabulary and logic that's reasonable but not fine-tuned against real bidsets. They get vault-ruled at the end of their rough-ship phase. After vault-rule application, the module is frozen as a stable observer/extractor in the same status as TracePoint's debug module relative to its core pipeline. Future fine-tuning happens in separate sessions where the module is the editing target and the rest of the pipeline is frozen, OR in completely new module versions, not by silently editing the frozen one.
>
> **Reason.** Rough modules are diagnostic surfaces. We learn what they get right and what they get wrong by running them against real bidsets and observing outputs. If they are tuned in the same session that we learn their behavior, prior diagnostic findings become stale and the module loses its value as a stable observer of what the pipeline produces.
>
> **Vault-ruled retroactively (2026-04-28):**
> - `backend/core/roofing_module.py` (C.2 commit `74772b6`)
> - `backend/core/roofing_vocabulary.py` (C.2)
> - `backend/core/glazing_vocabulary.py` (C.3b commit `14f4f53`)
>
> **Vault-ruled when sealed:** GlazingModule (C.3c future) and every future trade module.
>
> **Tuning sessions** are dedicated, separate from core/ work, with the relevant module as the only editing target and core/ files frozen.
>
> **Contract evolution** (Protocol, Input/Output dataclasses) CAN happen additively (as `TradeModuleInput.tables` was extended in C.3b) when multi-trade reality requires it. Vault rule applies to module behavior, not to contract evolution.

The exact wording can adapt to CLAUDE.md's voice. The substance is what's authoritative.

### Task 5 — Optional: PROJECT_CLAUDE.md alignment check

Read PROJECT_CLAUDE.md §6 ("Things that are NOT what someone might think"). The "parked glazing seeds" entry (added 2026-04-28) may reference specific counts. If it does, correct them. If it references the seeds in general without counts, leave it untouched.

If updates are warranted: small, factual, no expansion.

### Task 6 — Final regression sweep + commit + gate report

**Run:**
```
cd backend && pytest -q
node run_tests.js
node spotcheck_10b.js
node spotcheck_cricket.js
node spotcheck_durolast.js
node spotcheck_manufacturer.js
node mutation_test_step11.js
```

Expected: 214/19/0 backend, 107/107 + spotchecks + mutations on frontend.

**Commit:**
```
git add backend/C3_GLAZING_SEED_VALIDATION.md CLAUDE.md PROJECT_CLAUDE.md
git commit -m "D-8 follow-up: correct C.3a inventory counts, extend vault rule to cover trade modules

D-8 patch (documentation only):
- C3_GLAZING_SEED_VALIDATION.md §1 component count corrected 60→<actual>
- C3_GLAZING_SEED_VALIDATION.md §1 system count corrected 21→<actual>
- Editor's note added documenting the correction
- Gap list and verdict preserved (do not depend on counts)

Vault rule extension (CLAUDE.md §3 Decision 15):
- Trade modules now covered by vault rule
- Retroactive application: RoofingModule, roofing_vocabulary, glazing_vocabulary
- Forward application: GlazingModule (C.3c) and all future trade modules
- Tuning of vault-ruled modules requires dedicated session with core/ frozen
- Contract evolution (Protocol, Input/Output dataclasses) remains additive-permitted

Per Daniel's directive 2026-04-28: rough modules ship, then vault-rule
applies. Modules become stable observers; tuning is gated to separate
sessions to preserve diagnostic value."
```

If task 5 made no PROJECT_CLAUDE.md changes, drop that file from `git add`. Otherwise include.

**Final gate report** in the standard format. Single report covers all tasks.

---

## 5. §7 Stop Conditions

1. **Any C.3b addition turns out to be a duplicate** of an existing parked seed entry under a different name (Task 2 §7). Surface for Daniel; do not silently edit the C.3b commit.
2. **Sacred floor regresses** at any verification point.
3. **Parked seed counts differ from each other across reads** within this session (would mean something is unstable, very unlikely but worth catching).
4. **The CLAUDE.md §3 Decision 15 current text is structurally different** from what this brief assumes (the brief paraphrased it; if the actual text is meaningfully different, surface and verify the right edit shape).
5. **Production file outside the 3 authorized targets gets modified.**

§7 stops are documentation actions. Surface and ask Daniel.

---

## 6. Done Definition

- [ ] Parked seed counts re-verified mechanically; C.3a inventory corrected
- [ ] All 14 C.3b additions confirmed genuinely missing from parked seeds (or §7 stop fired)
- [ ] CLAUDE.md §3 Decision 15 extended to cover trade modules
- [ ] PROJECT_CLAUDE.md aligned if needed
- [ ] Sacred floor held throughout
- [ ] No production code modified
- [ ] No seed files modified
- [ ] No new dependencies
- [ ] Single commit on branch `phase2-v0.3-C3b-glazing-vocabulary` (continues C.3b's branch — this is bookkeeping for C.3b, not a separate phase)
- [ ] Stash workflow handled cleanly if uncommitted docs in working tree
- [ ] Final gate report produced

When done: D-8 closed. Trade-module vault rule canonical. C.3c planning may begin — and C.3c's march orders will explicitly include "vault-rule application as the final step" in its done definition.

---

**End of brief. Awaiting Daniel's review and Claude Code execution.**
