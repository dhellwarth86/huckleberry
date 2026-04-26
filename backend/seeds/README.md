# Reference Data — The Four-Layer Architecture

This directory contains five Python files that together form Huckleberry's reference-data spine. They are **read-only data**. No business logic lives here — these are vocabularies, taxonomies, patterns, and rule sets that the Phase 2 backend consumes at runtime.

## The four layers

```
┌───────────────────────────────────────────────────────────────────┐
│  Layer 1 — DISPATCH (plan-document structure)                     │
│  ─────────────────────────────────────────────                    │
│  dispatch_seed.py                                                 │
│                                                                   │
│  Answers: "what is this PDF made of, structurally?"               │
│  Contents: page-type vocabulary, sheet-number patterns,           │
│            cross-reference patterns, legend detection,            │
│            title-block extraction rules, LLM cage rules.          │
│  Used by:  the dispatch filters, before any trade vocab applies.  │
└───────────────────────────────────────────────────────────────────┘
                            │
                            ▼ produces classified plan-set
┌───────────────────────────────────────────────────────────────────┐
│  Layer 2 — MATERIALS (per-trade vocabulary)                       │
│  ─────────────────────────────────────────────                    │
│  roofing_materials.py        glazing_materials.py  (SKELETON)     │
│                                                                   │
│  Answers: "what trade vocabulary does this document use?"         │
│  Contents per file: CSI MasterFormat spec sections, manufacturer  │
│            registry, material properties (thickness markers,      │
│            insulation types, drawing conventions).                │
│  Used by:  the scope parser, on text from pages classified by     │
│            Layer 1 as roof_plan / spec_sheet / etc.               │
└───────────────────────────────────────────────────────────────────┘
                            │
                            ▼ given a system identified
┌───────────────────────────────────────────────────────────────────┐
│  Layer 3 — ASSEMBLIES (system → takeoff)                          │
│  ─────────────────────────────────────────────                    │
│  roof_assemblies.py          glazing_assemblies.py                │
│                                                                   │
│  Answers: "given a system identified by Layer 2, what's the       │
│            takeoff?"                                              │
│  Contents per file: COMPONENTS (universal vocab), SYSTEMS         │
│            (chemistry → component list), HARDWARE_SETS (glazing), │
│            ASSEMBLY_RELATIONSHIPS (cross-component rules), and    │
│            FBC_CONSTRAINTS (Florida code).                        │
│  Used by:  the takeoff generator, AFTER scope is identified by    │
│            Layer 2.                                               │
└───────────────────────────────────────────────────────────────────┘
```

There is no Layer 4 in code — Layer 4 is the runtime engine that consumes Layers 1–3 in order. That engine IS the Phase 2 backend.

## File-by-file

### `dispatch_seed.py` — 297 lines, ACTIVE
Plan-document structure. Page classification keywords, sheet number regex, cross-reference patterns, legend detection rules, project metadata extraction (deterministic vs LLM-only split), and the LLM cage rules for Phase 3.

The author notes that the diagnostic baseline against 15 real bidsets had **52 of 60 roof pages falling back to universal items** because the keyword lists are too narrow. Phase 2 v0.1's experiment is the place to either improve on or accept this baseline.

### `roofing_materials.py` — 243 lines, ACTIVE
Roofing trade vocabulary. CSI 07-series spec sections, 12 manufacturer entries with products and aliases, thickness markers, insulation types, drawing conventions. The most-used reference file in the entire stack.

### `roof_assemblies.py` — 1077 lines, ACTIVE
Roofing assembly map. ROOF_COMPONENTS (universal parts), ROOF_SYSTEMS (each membrane type → required + conditional components), ASSEMBLY_RELATIONSHIPS (12 cross-component rules: drain pairs with overflow, RTU drives curb count, curb >30" needs cricket, etc.), FBC_CONSTRAINTS (HVHZ, wind zones, positive drainage, secondary drainage, edge securement, reroof rules, energy code, fire rating, impact rating).

### `glazing_materials.py` — 264 lines, **SKELETON / OUT OF V0.1 SCOPE**
Glazing trade vocabulary. CSI 08-series spec sections plus a partial manufacturer list. The author explicitly marks this as "needs glazing-estimator review, don't treat as authoritative." Phase 2 v0.1 experiment scopes to roofing only; glazing review is for v0.2+.

### `glazing_assemblies.py` — 1311 lines, **OUT OF V0.1 SCOPE**
Glazing assembly map. Parallel structure to `roof_assemblies.py` for windows / doors / storefronts / curtain walls / entrances / louvers / spandrels. Schedule-driven approach (count from window/door schedules, not symbol-hunt on plans). Same v0.1 scope exclusion — review by a glazing estimator before we run an experiment against it.

## How the backend will consume these

(Speculative until the experiment runs; described here so future Claude doesn't have to reinvent.)

```python
# Notional Phase 2 v0.2+ consumption pattern
from seeds import dispatch_seed, roofing_materials, roof_assemblies

# Layer 1: classify pages
for page in pdf_pages:
    page.classification = classify_page(page, dispatch_seed.PAGE_CLASSIFICATION_KEYWORDS)
    page.cross_refs = extract_cross_refs(page, dispatch_seed.CROSS_REFERENCE_PATTERNS)
    page.legends = find_legends(page, dispatch_seed.LEGEND_HEADER_KEYWORDS)

# Layer 2: identify systems on classified pages
for page in pdf_pages:
    if page.classification.kind in ("roof_plan", "spec_sheet", "schedule_sheet"):
        page.scope = parse_scope(page.text, roofing_materials.MANUFACTURERS, roofing_materials.SPEC_SECTIONS)

# Layer 3: produce takeoff from identified systems
for system in identified_systems:
    assembly = roof_assemblies.ROOF_SYSTEMS[system.system_type]
    takeoff_items = build_takeoff(assembly, annotations)
    warnings = check_relationships(takeoff_items, roof_assemblies.ASSEMBLY_RELATIONSHIPS)
```

This is the architectural shape. The actual code is what Phase 2 v0.1 → v0.2 will produce.

## Edit policy

- **Reference data edits go through git PRs.** No SQL mutations. No runtime changes.
- **Adding a manufacturer** = edit the appropriate `*_materials.py`, run tests, commit.
- **Adding a system type** = edit `roof_assemblies.py` (or glazing equivalent), run tests, commit.
- **Tightening a regex** = edit `dispatch_seed.py`, regression-test against existing classifications, commit.
- **Backend hot reload** is not supported. Restart the backend after seed changes.

This intentional friction is the point. The seeds are project canon. Lossy as data, they're load-bearing as architecture.
