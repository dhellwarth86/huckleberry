# Phase C.3b — March Orders

**Target:** Two related but distinct deliverables in one autonomous session:
1. Extend `TradeModuleInput` (the C.1-ported contract) to add a `tables` field, additive-only, non-breaking. Documented as a §7-style deliberate adaptation.
2. Build `backend/core/glazing_vocabulary.py` by extending Huckleberry's parked seed files (`glazing_assemblies.py` + `glazing_materials.py`) with the documented gaps from the C.3a diagnostic.

**Authored:** 2026-04-28
**Authority:** Daniel (POC owner)
**Predecessor:** C.2 (commit `74772b6` on branch `phase2-v0.3-C2-roofing-module`). C.3a diagnostic complete (uncommitted output: `backend/C3_GLAZING_SEED_VALIDATION.md`).
**Source authority:** Huckleberry's parked `backend/seeds/glazing_assemblies.py` (1,311 lines) and `backend/seeds/glazing_materials.py` (264 lines), augmented by the C.3a Shoppes-at-Avalon evidence. **NOT a TracePoint port** — TracePoint has no glazing module per C.3 discovery (`/tmp/c3_discovery.md`).
**Discipline:** First Huckleberry-original implementation since v0.2 began. Discipline shifts from "verbatim port (don't touch TracePoint's calibrated decisions)" to "extension + diagnostic-first build (every addition is named, justified, and bounded by C.3a evidence)."
**Expected wall-clock:** ~75–105 minutes.

---

## 0. Why C.3b Is Different From Every Prior Phase

Every phase from v0.2 through C.2 has been verbatim port discipline. `diff = 0` against TracePoint source. No thresholds touched, no calibrations changed, no fields added or removed.

C.3b breaks that pattern in two specific places:

1. **Contract extension.** The C.1-ported `TradeModuleInput` dataclass gets a new optional field. This is the first modification to a Phase-C ported file. It is permitted because the C.1 port was the starting point of Huckleberry's contract, NOT the final state — TracePoint scoped trade modules; we extend the contract as multi-trade reality requires. The discipline: extension is documented explicitly in this march orders, additive-only (default value preserves existing behavior), and the modification is its own commit so the diff is reviewable.

2. **Vocabulary build (not port).** `glazing_vocabulary.py` is Huckleberry-original. There is no TracePoint source to `diff` against. The verification standard shifts from "byte-identical to source" to "every addition is named, every gap is documented, every threshold is justified." Same Karpathy procedure, applied to building rather than porting.

Both deliverables are bounded:
- The contract extension is **one field**. No other changes to `TradeModuleInput` or the `TradeModule` Protocol.
- The vocabulary build is **the C.3a documented gaps**. No additions beyond what C.3a evidence supports. No new system types, no new manufacturers, no new code constraints — only the entries C.3a explicitly named as missing.

If this discipline isn't held, the work expands into "redesign the glazing seeds" which is a different phase entirely.

---

## 1. C.3a Documented Gaps (Authoritative Scope for C.3b)

Per `backend/C3_GLAZING_SEED_VALIDATION.md` §5, the documented gaps surfaced by the Shoppes diagnostic are:

| Gap | C.3b action |
|---|---|
| No `entrance_*_single` variants in `GLAZING_SYSTEMS` (only pairs) | Add `entrance_medium_stile_single`, `entrance_narrow_stile_single`, `entrance_wide_stile_single` |
| No hardware set for "single aluminum storefront entrance + panic" (SET-1A pattern) | Add `hw_entrance_single_medium_stile_egress` |
| No discrete component slots for deadbolt, drip cap, latch guard, peep-hole | Add to `GLAZING_COMPONENTS`: `hw_deadbolt`, `hw_latch_guard`, `hw_door_viewer`, `flashing_drip_cap` |
| Hardware-OEM manufacturer table empty (Cal Royal, Yale, Sargent, Schlage, Von Duprin, etc.) | Extend `MANUFACTURERS` with hardware-OEM entries: Cal Royal, Yale Security, Sargent, Schlage, Von Duprin (5 entries; bounded list per C.3a evidence) |
| "Window types A–G" on A-602 are storefront framing wall panels, not punched windows — naming-boundary issue | Add `window_storefront_panel` to `GLAZING_SYSTEMS` (distinct from `window_aluminum_fixed`) |
| Standing-seam metal awning + flat aluminum canopy — trade-boundary question | DEFER to C.4 (cross-trade relationships layer). Add a note to `backend/CROSS_TRADE_INTEGRATION_NOTES.md` flagging the awning/canopy boundary; do NOT add awning/canopy entries to glazing vocabulary in C.3b. |

**Total additions to vocabulary:**
- 4 new components (deadbolt, latch guard, door viewer, drip cap)
- 4 new systems (3 entrance singles + 1 storefront window panel)
- 1 new hardware set (single medium-stile entrance with egress)
- 5 new manufacturers (hardware OEMs)

**Total additions to existing files:** none. C.3b creates `backend/core/glazing_vocabulary.py` as a NEW file. The parked `backend/seeds/glazing_assemblies.py` and `backend/seeds/glazing_materials.py` remain UNTOUCHED — they stay as the parked Huckleberry-side reference, exactly as they were.

This is a deliberate decision. C.3b's vocabulary file consumes the parked seeds (imports from them) and adds the C.3a-documented gaps as overlay. The parked seeds remain authoritative for their content; the vocabulary file extends them.

---

## 2. Goal Statement

**C.3b ships when:**

1. `backend/core/trade_module.py` is modified to add a single optional field to `TradeModuleInput`: `tables: list[Any] | None = None` (or equivalent based on what types are available — see §5 step C.3b.2 for type decision). The Protocol `TradeModule.run()` signature is UNCHANGED. Roofing module (C.2) continues to work unchanged because the new field defaults to `None` and roofing doesn't read it. Own commit.
2. `backend/core/glazing_vocabulary.py` exists, importing from the parked seeds and adding the C.3a-documented gaps as overlay. Public surface: `SYSTEMS`, `ITEMS`, `UNIVERSAL_ITEMS`, `RULES`, `MANUFACTURERS`, `GLAZING_VOCABULARY` (analogous to roofing_vocabulary's surface). Own commit.
3. `backend/CROSS_TRADE_INTEGRATION_NOTES.md` is updated to note the awning/canopy trade-boundary question (deferred to C.4). Own commit OR folded into the vocabulary commit, Daniel's preference.
4. Sacred floor preserved at every verification point.
5. No new dependencies added.
6. Roofing module (C.2) still passes the same import-resolution / public-surface smoke test it passed at C.2 ship. New tests for the contract extension are NOT required (the field is optional, default None, and C.2's RoofingModule doesn't reference it).
7. Smoke test for glazing_vocabulary: imports resolve, public surface is reachable, the C.3a-documented additions are present and named.

**C.3b explicitly does NOT ship:**

- `GlazingModule` class (that's C.3c)
- Behavior diagnostic against Shoppes (that's C.3c)
- Tests for either RoofingModule or GlazingModule against real bidsets (later phase)
- Modification to the parked `backend/seeds/glazing_assemblies.py` or `glazing_materials.py` (they stay parked)
- Activation of any trade module in `dispatch_gate.py` (Phase D/E)
- Anything from the cross-trade integration notes beyond the awning/canopy addition
- v0.2.1 work (D-4, D-5, schema migration)
- Debug module port (proposed C.5)
- New manufacturer entries beyond the 5 named in §1
- New system entries beyond the 4 named in §1
- New component entries beyond the 4 named in §1

If a "while we're in there" addition surfaces during execution, it gets noted as a future ticket and NOT added in this session. The §1 scope list is authoritative.

---

## 3. Sacred Floor

**Start-of-session baseline (C.2's end-state, unchanged through C.3a):**

| Suite | Count |
|---|---:|
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
| Backend `test_architect_profile.py` (B.4) | 23/23 |
| Backend v0.1 baseline | 38/38 |
| Backend full suite | **214 passed, 19 skipped, 0 failed** |

**Expected end-of-session:** 214 passed, 19 skipped, 0 failed (no test count change — C.3b adds no test files; the C.2 import-resolution smoke test for RoofingModule continues to pass because the contract extension is additive). Frontend unchanged.

If anything regresses, that's a §7 stop.

---

## 4. Constraints

### 4.1 — Sacred files (authorized modifications explicit)

**AUTHORIZED to modify in C.3b:**
- `backend/core/trade_module.py` — add ONE optional field to `TradeModuleInput`. No other changes. Documented in this march orders as a deliberate adaptation. Own commit.
- `backend/CROSS_TRADE_INTEGRATION_NOTES.md` — add ONE entry for the awning/canopy trade-boundary question. No other changes.

**AUTHORIZED to create in C.3b:**
- `backend/core/glazing_vocabulary.py` — NEW file. Public surface bounded by §1.

**SACRED (do NOT modify):**
- All TracePoint sources at `tracepoint_port/TracePoint/` (read-only)
- Phase 1 frontend HTML and all test files
- All v0.2 ported files (`config.py`, `pdf_engine.py`, `zone_filter.py`, `context.py`, `dispatch_gate.py`, `roofing_spec_database.py`, `test_pdf_engine.py`, `test_dispatch.py`)
- All B.1/B.2/B.3/B.4 ported files
- C.1's appendix (`CROSS_TRADE_INTEGRATION_NOTES.md`) — see authorized exception above for the single awning/canopy addition
- C.2 ported files (`roofing_vocabulary.py`, `roofing_module.py`, `trade_input_builder.py`)
- `backend/core/__init__.py` (kept empty)
- **`backend/seeds/glazing_assemblies.py` and `backend/seeds/glazing_materials.py`** — parked, NOT modified by C.3b. The vocabulary file imports from them; doesn't change them.
- All other seed files
- `shared/bidset_record.py`
- `CLAUDE.md`, `PROJECT_CLAUDE.md`, all `MARCH_ORDERS_*.md`, `STEP_*.md`, `DISCOVERED_ISSUES.md`, `V0_2_VALIDATION.md`, all observation/diagnostic docs, `VALIDATION_LEDGER.md`, `HANDOFF_*.md`

### 4.2 — Do not expand scope

- DO NOT build `GlazingModule` (C.3c)
- DO NOT add fields to `TradeModuleInput` beyond the single `tables` field
- DO NOT modify `TradeModule.run()` Protocol signature
- DO NOT modify the parked seed files
- DO NOT add manufacturers, systems, or components beyond §1's bounded list
- DO NOT add new dependencies
- DO NOT migrate `BidsetRecord`
- DO NOT fix D-4, D-5, D-6, or D-7
- DO NOT activate roofing or glazing modules anywhere
- DO NOT add features "while we're in there"
- DO NOT touch frontend code

### 4.3 — Do not reinvent the parked seeds

- The parked `glazing_assemblies.py` and `glazing_materials.py` stay authoritative for what's already in them. C.3b does not "improve" the existing 60 components, 21 systems, 7 hardware sets, 15 relationships, 9 FBC constraints. C.3a verified those are usable as a starting vocabulary. Improvements to the parked seeds — if any are warranted — are a separate phase requiring estimator review (see C.3a non-conclusion #6).
- The vocabulary file (`backend/core/glazing_vocabulary.py`) imports `GLAZING_COMPONENTS`, `GLAZING_SYSTEMS`, `HARDWARE_SETS`, `ASSEMBLY_RELATIONSHIPS`, `FBC_CONSTRAINTS` from the parked seeds, and overlays the C.3a-documented additions. The exact merge mechanism (dict union, list extend, separate keys) is decided in §5 step C.3b.4 based on what the parked file's structure makes natural.

### 4.4 — Karpathy procedure

- Read first: `glazing_assemblies.py` (1,311 lines), `glazing_materials.py` (264 lines), `backend/core/trade_module.py` (90 lines), `backend/core/roofing_vocabulary.py` (575 lines, for shape reference). Full reads.
- Failing test floor: NOT applicable — C.3b ships no new tests. The verification floor is sacred-floor regression + smoke test on the new vocabulary file's import resolution and public surface. Documented as the intentional verification floor for this phase.
- Minimum implementation: contract extension is ONE field with default None; vocabulary file is ONLY the C.3a-documented additions overlaid on the parked seeds. No more.
- 100% green floor: 214/19/0 holds at every verification point.
- §7 stops: surface Discovered Issues; do not silently resolve.

### 4.5 — Autonomous execution

Same pattern as C.2 / B.4 / B.2+B.3. Steps C.3b.0 through C.3b.6 run in one session. Substantive gates only. Two commits expected (contract extension + vocabulary file; cross-trade-notes addition can fold into vocabulary commit). ONE final gate report at the end.

---

## 5. Step List

### Step C.3b.0 — Pre-flight

**Read:** This march orders document end-to-end. `CLAUDE.md` §6 (hard guardrails refresh). `PROJECT_CLAUDE.md` for current state. `backend/C3_GLAZING_SEED_VALIDATION.md` end-to-end (this is the evidence base for what C.3b adds).

**Verify (no writes):**
- All §1 source files exist and readable
- Sacred floor matches §3 baseline exactly (`pytest backend/tests/ -q`)
- Working tree clean (or known-stash-pattern). Stash if needed: `git stash push -u -m "C.3b pre-flight: stash docs"`
- Branch state: branch fresh as `phase2-v0.3-C3b-glazing-vocabulary` from `74772b6` (C.2 HEAD). C.3b is conceptually distinct from C.2 (extension + build vs port).

**Internal gate:** Pre-conditions green. Branch + stash in place. C.3a diagnostic readable as evidence input.

**§7 stop only if:** baseline mismatch, working tree won't clean, C.3a output not present (shouldn't happen — it's been confirmed in chat), parked seeds missing.

### Step C.3b.1 — Read all source files end-to-end

**Read in full:**
- `backend/seeds/glazing_assemblies.py` (1,311 lines) — to confirm structure of GLAZING_COMPONENTS, GLAZING_SYSTEMS, HARDWARE_SETS, ASSEMBLY_RELATIONSHIPS, FBC_CONSTRAINTS exactly as C.3a inventoried them. Record the exact data structure (dict-of-dicts, list-of-dataclasses, etc.) so the vocabulary file's overlay matches.
- `backend/seeds/glazing_materials.py` (264 lines) — confirm SPEC_SECTIONS, MANUFACTURERS, MATERIAL_PROPERTIES, GLAZING_PIN_TYPES structure.
- `backend/core/trade_module.py` (90 lines) — confirm TradeModuleInput dataclass current shape, decide what type the new `tables` field should be (likely `list[Any] | None = None` if no Table dataclass exists in `core.context` already, OR `list[Table] | None = None` if one does).
- `backend/core/roofing_vocabulary.py` (575 lines) — for shape reference. The glazing vocabulary file should follow the same shape: a top-level dict containing SYSTEMS / ITEMS / UNIVERSAL_ITEMS / RULES, plus exported constants. C.3b's vocabulary file should mirror that structure for consistency with C.2.
- `backend/CROSS_TRADE_INTEGRATION_NOTES.md` — to find the right place to add the awning/canopy entry.

**Decisions to record at this step:**
1. Type for the new `tables` field on `TradeModuleInput`. If `core.context` has a `Table` dataclass (or a tabular-data type from pdfplumber's parse), use that. If not, use `list[Any] | None = None` — the type is intentionally loose because table representation is up to whatever produces them; consumers cast.
2. Vocabulary file structure: does it import-and-overlay from the parked seeds, or does it copy the parked content and add the new entries? Recommend import-and-overlay — preserves the "parked seeds are authoritative for what's already in them" discipline.
3. Where the awning/canopy note goes in `CROSS_TRADE_INTEGRATION_NOTES.md`: as a new entry under glazing↔roofing, or as a new section. Recommend: extend the existing storefront/glazing↔roofing entry with a sub-bullet noting awnings and canopies as adjacent boundary cases.

**Internal gate:** All structures recorded. Type decision made. Overlay mechanism decided. Awning/canopy note placement decided.

**§7 stop only if:** parked seed structure differs significantly from what C.3a documented (would mean either C.3a got it wrong or the seeds changed), `core.context` lacks a Table type AND has something else nearby that would suggest an existing convention.

### Step C.3b.2 — Extend TradeModuleInput contract

**Write:** Modify `backend/core/trade_module.py` to add ONE field to `TradeModuleInput`:

```python
@dataclass
class TradeModuleInput:
    # ... all existing fields unchanged ...
    
    # Tabular data (e.g., schedule pages) — added in C.3b for schedule-driven
    # trade modules (glazing, plumbing, electrical, mechanical). Optional;
    # default None preserves C.1/C.2 behavior. Roofing module ignores this
    # field.
    tables: list[Any] | None = None  # OR list[Table] | None = None per §5 C.3b.1 decision
```

The exact type and the comment are based on Step C.3b.1 decisions. The field MUST be optional with a default value, MUST come after all existing fields (dataclass ordering — required-then-optional), and MUST NOT change any existing field's name, type, or default.

**Verify (no writes beyond the edit):**
- `diff backend/core/trade_module.py` against the pre-edit version shows ONLY the new field addition, no other changes
- Module imports cleanly: `python -c "from core.trade_module import TradeModuleInput; print(TradeModuleInput.__annotations__)"`
- `RoofingModule` from C.2 still imports cleanly: `python -c "from core.roofing_module import RoofingModule; print('ok')"`

**Run sacred floor:**
```
cd backend && pytest -q
```

Expected: 214/19/0 unchanged. The contract extension is additive; no test depends on the absence of the field.

**Internal gate:** Field added, no other changes, all imports resolve, sacred floor unchanged.

**§7 stop only if:** any test regresses (would mean a test depended on the exact field set of TradeModuleInput, which itself would be a problem worth surfacing).

### Step C.3b.3 — Commit contract extension

**Write (commit only):**
```
git add backend/core/trade_module.py
git commit -m "Phase C.3b (1/2): Extend TradeModuleInput with optional tables field for schedule-driven trade modules

Additive-only change to the C.1-ported contract. Adds:
- tables: list[Any] | None = None

Default value preserves C.1/C.2 behavior. RoofingModule (C.2) ignores
the new field; GlazingModule (C.3c) will read it. The TradeModule
Protocol signature is unchanged.

Documented as a §7-style deliberate adaptation in MARCH_ORDERS_C_3b.md §0.
The C.1 port was the starting point of Huckleberry's contract, not the
final state — extensions are permitted as multi-trade reality requires."
```

**Internal gate:** Commit landed. Working tree clean (modulo stash from pre-flight).

### Step C.3b.4 — Build glazing_vocabulary.py

**Write:** Create `backend/core/glazing_vocabulary.py`. Structure follows `roofing_vocabulary.py`'s shape (top-level dict with SYSTEMS / ITEMS / UNIVERSAL_ITEMS / RULES + exported constants for backward consumption).

The file's logical structure:

```python
"""
Glazing vocabulary for the GlazingModule (Phase C.3c).

Imports the parked seed content from backend/seeds/glazing_{assemblies,materials}.py
verbatim and overlays the C.3a-documented gaps. The parked seeds remain
authoritative for what's already in them; this file extends them.

Source of truth for additions:
  backend/C3_GLAZING_SEED_VALIDATION.md (2026-04-28, C.3a diagnostic, Shoppes-at-Avalon)

Bounded additions per MARCH_ORDERS_C_3b.md §1:
  - 4 components: hw_deadbolt, hw_latch_guard, hw_door_viewer, flashing_drip_cap
  - 4 systems: entrance_medium_stile_single, entrance_narrow_stile_single,
              entrance_wide_stile_single, window_storefront_panel
  - 1 hardware set: hw_entrance_single_medium_stile_egress
  - 5 manufacturers: Cal Royal, Yale Security, Sargent, Schlage, Von Duprin
"""
from __future__ import annotations
from typing import Any

from seeds.glazing_assemblies import (
    GLAZING_COMPONENTS as _SEED_COMPONENTS,
    GLAZING_SYSTEMS as _SEED_SYSTEMS,
    HARDWARE_SETS as _SEED_HARDWARE_SETS,
    ASSEMBLY_RELATIONSHIPS as _SEED_RELATIONSHIPS,
    FBC_CONSTRAINTS as _SEED_FBC,
)
from seeds.glazing_materials import (
    SPEC_SECTIONS as _SEED_SPEC_SECTIONS,
    MANUFACTURERS as _SEED_MANUFACTURERS,
    MATERIAL_PROPERTIES as _SEED_MATERIAL_PROPS,
    GLAZING_PIN_TYPES as _SEED_PIN_TYPES,
)

# C.3a-documented additions
_C3A_COMPONENT_ADDITIONS: dict[str, Any] = {
    "hw_deadbolt": {
        # ... entry per the parked seed's component shape ...
    },
    "hw_latch_guard": {
        # ...
    },
    "hw_door_viewer": {
        # ...
    },
    "flashing_drip_cap": {
        # ...
    },
}

_C3A_SYSTEM_ADDITIONS: dict[str, Any] = {
    "entrance_medium_stile_single": {
        # ... entry per the parked seed's system shape, mirroring
        # entrance_medium_stile_pair but with single-leaf component count ...
    },
    "entrance_narrow_stile_single": {
        # ...
    },
    "entrance_wide_stile_single": {
        # ...
    },
    "window_storefront_panel": {
        # Distinct from window_aluminum_fixed; this is a storefront-framing
        # wall panel as named on A-602 of the Shoppes bidset.
    },
}

_C3A_HARDWARE_SET_ADDITIONS: dict[str, Any] = {
    "hw_entrance_single_medium_stile_egress": {
        # SET-1A pattern from Shoppes: single aluminum entrance + panic
    },
}

_C3A_MANUFACTURER_ADDITIONS: dict[str, dict[str, Any]] = {
    "Cal Royal": {
        # ... entry per parked seed's manufacturer shape ...
    },
    "Yale Security": {
        # ...
    },
    "Sargent": {
        # ...
    },
    "Schlage": {
        # ...
    },
    "Von Duprin": {
        # ...
    },
}

# Public surface — overlay the additions on the parked content
COMPONENTS: dict[str, Any] = {**_SEED_COMPONENTS, **_C3A_COMPONENT_ADDITIONS}
SYSTEMS: dict[str, Any] = {**_SEED_SYSTEMS, **_C3A_SYSTEM_ADDITIONS}
HARDWARE_SETS: dict[str, Any] = {**_SEED_HARDWARE_SETS, **_C3A_HARDWARE_SET_ADDITIONS}
RELATIONSHIPS: list[Any] = list(_SEED_RELATIONSHIPS)
FBC_CONSTRAINTS: dict[str, Any] = dict(_SEED_FBC)

SPEC_SECTIONS: dict[str, Any] = dict(_SEED_SPEC_SECTIONS)
MANUFACTURERS: dict[str, dict[str, Any]] = {**_SEED_MANUFACTURERS, **_C3A_MANUFACTURER_ADDITIONS}
MATERIAL_PROPERTIES: dict[str, Any] = dict(_SEED_MATERIAL_PROPS)
GLAZING_PIN_TYPES: dict[str, Any] = dict(_SEED_PIN_TYPES)

# Module-level vocabulary aggregate (matches roofing_vocabulary.py public surface convention)
GLAZING_VOCABULARY: dict[str, Any] = {
    "components": COMPONENTS,
    "systems": SYSTEMS,
    "hardware_sets": HARDWARE_SETS,
    "relationships": RELATIONSHIPS,
    "fbc_constraints": FBC_CONSTRAINTS,
    "spec_sections": SPEC_SECTIONS,
    "manufacturers": MANUFACTURERS,
    "material_properties": MATERIAL_PROPERTIES,
    "pin_types": GLAZING_PIN_TYPES,
}
```

The exact entry contents for each addition follow the shape of the parked seeds — Step C.3b.1 records that shape. The entries should NOT invent new dictionary keys beyond what the parked seeds use; same-shape additions only.

**Specific entry guidance per addition:**

- **hw_deadbolt, hw_latch_guard, hw_door_viewer, flashing_drip_cap:** mirror the shape of existing `GLAZING_COMPONENTS` entries (probably `{"category": str, "uom": str, "description": str, ...}` — exact keys per Step C.3b.1's read).
- **entrance_*_single (3 entries):** mirror `entrance_medium_stile_pair` etc., with `frame_count: 1` and `door_count: 1` (vs pair's 2/2), and `required_components` list adjusted (single pivot set, single closer, single threshold, etc.).
- **window_storefront_panel:** mirror `window_aluminum_fixed` shape but indicate "storefront framing wall panel" in description; the unit of measure is likely SF (panel area) rather than each.
- **hw_entrance_single_medium_stile_egress:** mirror `hw_entrance_pair_medium_stile` for component categories, with single-leaf counts and an added `panic_device` requirement.
- **Manufacturer entries:** mirror existing seeds' manufacturer shape (probably `{"aliases": list[str], "products": list[str], "category": str}` — exact keys per read). Hardware-OEM category should be distinct from storefront/glass categories; if the parked seeds don't have a hardware-OEM category enum, add one (named in this file's docstring as a structural addition).

**Verify (no writes beyond the file creation):**
- `python -c "from core.glazing_vocabulary import GLAZING_VOCABULARY; print(len(GLAZING_VOCABULARY['components']), len(GLAZING_VOCABULARY['systems']), len(GLAZING_VOCABULARY['manufacturers']))"`
- Expected output: `64 25 17` (60+4 components, 21+4 systems, 12+5 manufacturers). If the numbers differ, that's a §7 stop — the additions didn't land cleanly.
- Imports resolve cleanly: no circular imports, no missing seeds attributes
- All 5 new manufacturer entries have `aliases` populated
- All 4 new system entries have the same key set as their pair-variant counterparts (or window_aluminum_fixed for the storefront panel)
- All 4 new component entries have the same key set as existing components

**Run sacred floor:**
```
cd backend && pytest -q
```

Expected: 214/19/0 unchanged. New file adds no tests; existing tests don't import glazing_vocabulary.

**Internal gate:** File created with bounded additions, public surface accessible, count check passes, sacred floor unchanged.

**§7 stop only if:**
- Count check fails (additions didn't land or extra additions slipped in)
- Imports fail
- Sacred floor regresses
- Discovery during writing reveals the parked seeds use an unexpected structure that makes overlay non-trivial (would warrant a planning conversation, not silent invention)

### Step C.3b.5 — Update CROSS_TRADE_INTEGRATION_NOTES.md

**Write:** Add ONE entry to `backend/CROSS_TRADE_INTEGRATION_NOTES.md` noting the awning/canopy trade-boundary question, deferred to C.4.

Locate the existing storefront/glazing↔roofing entry. Add a sub-bullet (or extend the entry) with text approximately:

> **Awnings and canopies (added 2026-04-28 from C.3a Shoppes evidence).** Pre-fabricated standing-seam metal awnings (e.g., PAC-CLAD M-2) and pre-fabricated flat aluminum canopies (e.g., MAPES M-4) sit at the glazing↔roofing↔specialty-metal trade boundary. On small commercial bid sets they often appear in the storefront/glazing scope (visible in elevations adjacent to storefront callouts); on larger bidsets they bid with metal-panel scope. C.3b deliberately did NOT add awning/canopy entries to the glazing vocabulary — the boundary decision is a C.4 (cross-trade relationships layer) task. C.3b's scope was limited to the additions C.3a explicitly documented.

The exact wording can match the document's existing voice. The key point: future readers know awnings/canopies were considered, deliberately deferred, and the reasoning.

**Verify:** Document still readable, no other entries changed.

**Internal gate:** Single addition, no other edits.

**§7 stop only if:** the existing structure of CROSS_TRADE_INTEGRATION_NOTES.md doesn't have a glazing↔roofing section to extend (would mean re-reading the document carefully — not a blocker, just adjust placement).

### Step C.3b.6 — Final regression sweep + commit + gate report

**Run (in order):**
```
cd backend && pytest -v
node run_tests.js
node spotcheck_10b.js
node spotcheck_cricket.js
node spotcheck_durolast.js
node spotcheck_manufacturer.js
node mutation_test_step11.js
```

Expected: 214/19/0 backend, 107/107 + spotchecks + mutation tests on frontend.

**Write (commit):**
```
git add backend/core/glazing_vocabulary.py backend/CROSS_TRADE_INTEGRATION_NOTES.md
git commit -m "Phase C.3b (2/2): Build glazing_vocabulary.py extending parked seeds with C.3a-documented gaps

Additions (bounded by C.3a Shoppes-at-Avalon evidence):
- 4 components: hw_deadbolt, hw_latch_guard, hw_door_viewer, flashing_drip_cap
- 4 systems: entrance_*_single (3 stile variants), window_storefront_panel
- 1 hardware set: hw_entrance_single_medium_stile_egress
- 5 manufacturers: Cal Royal, Yale Security, Sargent, Schlage, Von Duprin

Additions overlaid on parked seeds (backend/seeds/glazing_{assemblies,materials}.py
remain unmodified). Vocabulary file's structure mirrors roofing_vocabulary.py
(C.2) for consistency.

CROSS_TRADE_INTEGRATION_NOTES.md updated to flag awning/canopy boundary
question (PAC-CLAD M-2, MAPES M-4 from Shoppes), deferred to C.4.

Source of truth: backend/C3_GLAZING_SEED_VALIDATION.md (C.3a, 2026-04-28)."
```

**Then:** `git stash pop` to restore documentation files.

Verify post-pop: `pytest backend/tests/ -q` still 214/19/0.

**Produce final gate report** in standard format. Single report covers contract extension + vocabulary build + cross-trade-notes update.

```
=== Phase C.3b Session Report — <date> ===

STEPS COMPLETED: C.3b — TradeModuleInput contract extension (1 field, additive) +
                 glazing_vocabulary.py build (overlay on parked seeds, bounded by
                 C.3a documented gaps) + CROSS_TRADE_INTEGRATION_NOTES.md awning/
                 canopy boundary entry.

FILES CHANGED:
  backend/core/trade_module.py                MODIFIED (+1 field on TradeModuleInput)
                                               Field: tables: <type> | None = None
                                               Documented as §0 deliberate adaptation.
  backend/core/glazing_vocabulary.py          NEW (<N> lines, sha1 <hash>)
                                               Imports from seeds/glazing_{assemblies,materials}.py
                                               Adds: 4 components, 4 systems, 1 hardware set,
                                                     5 manufacturers (per §1 bounded list)
                                               Public surface: GLAZING_VOCABULARY dict +
                                                     individual constants
                                               Count verification: components=64 systems=25 manufacturers=17
  backend/CROSS_TRADE_INTEGRATION_NOTES.md    MODIFIED (+1 entry: awning/canopy boundary)

DEPENDENCIES: pyproject.toml unchanged. No new deps.

FILES NOT CHANGED (sacred):
  All TracePoint sources (read-only)
  Phase 1 frontend
  v0.2 / B.1 / B.2 / B.3 / B.4 ported files (none touched)
  C.1 ported files (trade_module.py: ONE additive field, but verbatim shape preserved
    elsewhere — see PATH-EDIT LOG)
  C.2 ported files (roofing_vocabulary.py, roofing_module.py, trade_input_builder.py — none touched)
  backend/core/__init__.py (still empty)
  backend/seeds/glazing_assemblies.py (PARKED, not modified)
  backend/seeds/glazing_materials.py (PARKED, not modified)
  All other seed files
  shared/bidset_record.py
  CLAUDE.md, PROJECT_CLAUDE.md, all MARCH_ORDERS_*.md, STEP_*.md, DISCOVERED_ISSUES.md,
    V0_2_VALIDATION.md, observation/diagnostic docs, VALIDATION_LEDGER.md, HANDOFF_*.md
  dispatch_gate.py — neither RoofingModule nor (future) GlazingModule wired

PATH-EDIT LOG:
  trade_module.py — single field addition. Diff vs C.1-ported source shows ONLY the
    new field plus its docstring/comment. No other lines changed. This is the first
    deliberate adaptation of a Phase-C ported file; documented in MARCH_ORDERS_C_3b.md §0.
  glazing_vocabulary.py — NEW file. No port; no diff target.
  CROSS_TRADE_INTEGRATION_NOTES.md — single entry addition under existing storefront/
    glazing↔roofing section.

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
| Backend test_architect_profile.py    | 23/23   | 23/23   | sacred |
| Backend v0.1 baseline                | 38/38   | 38/38   | sacred |
| Backend full suite                   | 214     | 214     | unchanged (C.3b adds no test files) |

REGRESSIONS: none

KARPATHY DISCIPLINE:
  Read first: 5 source files read end-to-end (trade_module 90 lines + roofing_vocabulary 575
    + glazing_assemblies 1311 + glazing_materials 264 + CROSS_TRADE_INTEGRATION_NOTES — sum).
  Failing test floor: SKIPPED — C.3b ships no new test files; the verification floor is
    sacred-floor regression + smoke-test on the new vocabulary file's import resolution
    and bounded-addition counts. Documented as the intentional verification floor for
    a build-against-extension phase (vs the verbatim-port phases).
  Minimum implementation:
    - trade_module.py: ONE additive field with default None. No other changes.
    - glazing_vocabulary.py: ONLY the C.3a-documented additions, overlaid on parked seeds.
      Count verification confirms bounded list (60+4=64 components, 21+4=25 systems,
      12+5=17 manufacturers).
  100% green floor: all sacred suites unchanged at every checkpoint.
  No "while we're in there" additions surfaced — the C.3a-documented gap list was
    authoritative.

DISCOVERED ISSUES: <none, OR D-N+ if any surfaced>

EXECUTION DETAIL:
  Branch: phase2-v0.3-C3b-glazing-vocabulary (NEW; created from 74772b6 per §5 C.3b.0)
  Pre-flight stash: stash@{0} "C.3b pre-flight: stash docs" (popped at end)
  C.3b commit 1/2 (contract extension): <SHA> "Phase C.3b (1/2): Extend TradeModuleInput..."
  C.3b commit 2/2 (vocabulary): <SHA> "Phase C.3b (2/2): Build glazing_vocabulary.py..."
  Stash list at end: empty

git log (current branch):
  <C.3b 2/2 SHA>  Phase C.3b (2/2): Build glazing_vocabulary.py...
  <C.3b 1/2 SHA>  Phase C.3b (1/2): Extend TradeModuleInput...
  74772b6         Phase C.2: Port TracePoint roofing module verbatim...
  23a459c         Phase C.1: Port TracePoint trade_module.py Protocol verbatim...
  a8ee936         Phase B.4: ...
  ...

PHASE C.3b COMPLETE: TradeModuleInput contract extended (additive, non-breaking).
glazing_vocabulary.py built as overlay on parked seeds with bounded C.3a-documented
additions. Cross-trade integration notes updated for awning/canopy boundary deferred
to C.4. C.3c (build GlazingModule against contract + behavior diagnostic on Shoppes)
is now unblocked.

NEXT STEP: Phase C.3c — build GlazingModule class implementing the C.1 Protocol,
running against the C.3b vocabulary, with one-bidset behavior diagnostic on Shoppes.
First module to use the new TradeModuleInput.tables field. C.3c is design + build,
larger than C.3b — needs its own march-orders document and likely a planning
conversation about behavior validation strategy (no ground truth, single-bidset
evidence floor).

AWAITING APPROVAL: yes — Daniel approves both C.3b commits and confirms C.3c
planning may begin.
```

---

## 6. §7 Stop Conditions

Stop and surface as Discovered Issue:

1. **Sacred floor regresses** at any verification point
2. **Vocabulary count check fails** (additions didn't land or extras slipped in)
3. **`TradeModuleInput` contract extension breaks RoofingModule import** (would mean the field addition wasn't truly additive)
4. **Parked seeds' structure differs significantly** from what C.3a documented
5. **Awning/canopy boundary reasoning leads toward "actually we should add these"** — STOP. C.3b's scope is bounded. Add to a future ticket; do not expand in-session.
6. **Hardware-OEM category needs to be added to the parked seeds** to make the new manufacturer entries fit cleanly — surface, since modifying parked seeds is out of scope per §4.1
7. **Production file outside the 3 authorized targets gets modified**
8. **More than one field addition to TradeModuleInput surfaces as needed**
9. **Any new dependency would be required** to make imports resolve

§7 stops are documentation actions. Document in `backend/DISCOVERED_ISSUES.md` as next available D-number.

---

## 7. Done Definition

C.3b is done when:

- [ ] `backend/core/trade_module.py` has ONE new optional field on `TradeModuleInput`, no other changes
- [ ] `backend/core/glazing_vocabulary.py` exists, overlays parked seeds, count check passes (64 / 25 / 17)
- [ ] `backend/CROSS_TRADE_INTEGRATION_NOTES.md` has awning/canopy boundary entry
- [ ] All sacred floors held at every verification point (214/19/0)
- [ ] No new dependencies
- [ ] Two commits on the new branch
- [ ] Stash popped cleanly
- [ ] Final gate report produced

When done, **C.3b is sealed.** Next: C.3c — build `GlazingModule` against the contract using the C.3b vocabulary, with a one-bidset behavior diagnostic on Shoppes. Different shape of work; needs its own march-orders document.

---

**End of MARCH_ORDERS_C_3b.md. Awaiting Daniel's review and Claude Code execution brief.**
