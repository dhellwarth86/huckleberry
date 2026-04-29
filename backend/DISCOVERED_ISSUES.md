# Discovered Issues — Phase 2 v0.2 port

Per `MARCH_ORDERS_PHASE_2_v0.2.md` §7 Karpathy Procedure Reminder, issues found
outside the current Step's scope are recorded here. Do NOT fix in the current
Step — Daniel decides whether each is blocking.

---

## D-1 — Step 13 gate ~30/30 is structurally unreachable until Step 15

**Discovered:** 2026-04-26 during Step 13.

**Context:** March orders §5 Step 13 gate expects:

> roughly 30 tests passing across the four classes (schema dataclass
> instantiation, confidence ordering, LLM iron-cage validation, leak detection).

**What I observed:** TracePoint's `tests/test_dispatch.py` (copied verbatim per
Step 11, byte-identical to upstream) has a **module-level** import on line 29:

```python
from core.dispatch_gate import run_dispatch
```

Pytest collects test files by importing the module first. With
`backend/core/dispatch_gate.py` not yet present (it lands in Step 15), pytest
fails the entire module import and skips collection for ALL classes in the
file:

```
ERROR tests/test_dispatch.py
ModuleNotFoundError: No module named 'core.dispatch_gate'
```

The four target unit-test classes (TestSchema, TestConfidence,
TestLLMValidation, TestLeakCheck) **do not call `run_dispatch` themselves**
(verified via grep: only TestSinglePageCFA, TestMultiPageVineStreet,
TestTacoBell, TestAEA invoke `run_dispatch`). They only need the import line
to succeed.

So the Step 13 gate is functionally blocked by Step 15.

**What is verifiably true after Step 13:**

- `backend/core/zone_filter.py` and `backend/core/context.py` are byte-identical
  to TracePoint (`diff` confirmed zero output)
- `from core.context import (...all 22 symbols test_dispatch.py imports...)`
  succeeds when run interactively — schema is loadable
- `from core.zone_filter import detect_detail_zones, detect_title_block,
  filter_paths_by_zone` succeeds
- All sacred floors still green: Phase 1 138/138, v0.1 38/38,
  test_pdf_engine.py 40/40

**What is NOT true after Step 13 (but expected by the gate):**

- The four unit-test classes (~30 tests) do NOT collect, do NOT run, do NOT pass

**Resolution options for Daniel to choose from:**

A. **Accept and continue.** The four unit-test classes will collect cleanly
   the moment Step 15 ports dispatch_gate.py. Step 13 gate is treated as
   "schema/zone_filter loadable, all sacred floors green, test_dispatch.py
   still erroring at collection — same posture as after Step 11, plus the
   schema is now loadable independently." The ~30 tests come green at Step
   15's gate as a side-effect.

B. **Approve a single-line edit to TracePoint's test file** (deviates from
   "verbatim copy"): wrap the import in a fixture or move it inside the
   integration test classes. This makes the four unit-test classes
   collectable now. Specific change is small and reversible (revert before
   pushing).

C. **Add a stub `backend/core/dispatch_gate.py`** with `def run_dispatch():
   raise NotImplementedError` just to satisfy the import. Removed/replaced
   in Step 15. This violates "do not reinvent" but might be the smallest
   deviation.

I did NOT take any of these actions. Recording for Daniel's decision.

**My read:** Option A is the cleanest. The march orders' Step 13 expected ~30
tests to pass; the actual count is 0 collected, but the four target classes are
proven correct (their dependencies all import) and will collect at Step 15.
Total tests passing remains 78 (38 v0.1 + 40 pdf_engine) which is the same
posture as after Step 12. Option B is a sanctioned deviation if Daniel wants
the green count to track the gate spec literally.

**RESOLUTION (Step 14 brief, 2026-04-26):** Daniel implicitly chose Option A
by approving Step 14 to begin without addressing D-1 separately. The ~30 unit
tests will be expected to come green at Step 15's gate as a side-effect of
porting `dispatch_gate.py` (which provides the `run_dispatch` symbol that
test_dispatch.py imports at module level). Step 13 gate posture stayed at
"all sacred floors green, schema/zone_filter loadable independently,
test_dispatch.py erroring at collection" until Step 15.

---

## D-2 — A third `data.roofing_materials` import exists at line 1359 of dispatch_gate.py; the orders prescribe only two edits

**Discovered:** 2026-04-26 during Step 15 (after end-to-end read of
`C:/TracePoint/core/dispatch_gate.py`, before applying edits).

**Context:** Step 15 brief states:

> apply EXACTLY two import edits and no others:
>
>   from data.roofing_materials import all_manufacturer_names
>     → from seeds.roofing_spec_database import all_manufacturer_names
>   from data.roofing_materials import spec_section_to_system, MANUFACTURERS,
>                                       MATERIAL_PROPERTIES
>     → same with seeds.roofing_spec_database

> After the import edits, diff against TracePoint source should show exactly
> those two changed lines and nothing else.

**What I observed:** TracePoint's `core/dispatch_gate.py` actually contains
**three** `from data.roofing_materials` import sites:

```
1170: from data.roofing_materials import all_manufacturer_names
1292: from data.roofing_materials import (
1294:     spec_section_to_system, MANUFACTURERS, MATERIAL_PROPERTIES,
1295: )
1359: from data.roofing_materials import SPEC_SECTIONS, MATERIAL_PROPERTIES
```

Lines 1170 and 1292 match the prescribed edits. Line 1359 is a third
function-local import inside `_determine_roof_shape()`. It is not listed
in the orders.

**What I did per orders (Step 15, 2026-04-26):**

- Applied the two prescribed edits exactly. `diff` against TracePoint shows
  only those two changed lines.
- Did NOT touch line 1359. It still reads
  `from data.roofing_materials import SPEC_SECTIONS, MATERIAL_PROPERTIES`.

**Behavioral consequence:**

- Step 15 unit-test gate is unaffected. The four target test classes
  (TestSchema, TestConfidence, TestLLMValidation, TestLeakCheck) do not
  invoke `run_dispatch`, so `_determine_roof_shape` never runs during the
  unit tests. They should collect cleanly now and pass at ~30/30.
- Step 16 (the 15-bidset sweep) WILL be impacted. `run_dispatch` calls
  `run_scope_scanner`, which calls `_determine_roof_shape`. The deferred
  function-local import on line 1359 will fail with
  `ModuleNotFoundError: No module named 'data.roofing_materials'`. The
  failure is wrapped by a try/except at line 1477:
  ```python
  try:
      run_scope_scanner(engine, doc, ctx)
  except Exception as e:
      ctx.dispatch_warnings.append(f"scope scanner failed: {e}")
  ```
  So Step 16 will run to completion but every bidset will surface a
  `scope scanner failed` warning. The `ctx.project_scope` will not be
  populated for any bidset. Roof-shape signal, scope_pages, detected_system
  — none of it lands. **This defeats the whole purpose of the v0.2 port**
  (resolving v0.1's four symptoms).

**Resolution options for Daniel to choose from:**

A. **Approve a third edit on line 1359** (same character of rewire as the
   other two: `data.roofing_materials` → `seeds.roofing_spec_database`,
   no other change). The orders' "EXACTLY two" was likely an undercount
   from missing this third site during drafting. This is the cleanest fix
   and preserves the spirit of "no production code changes; only path
   rewires." After this edit, total `diff` vs TracePoint = 3 changed
   lines, all of identical character.

B. **Leave line 1359 broken; Step 16 produces 15 bidsets with empty
   project_scope and "scope scanner failed" warnings.** This faithfully
   honors "EXACTLY two" but produces a non-functional v0.2 — equivalent
   to v0.1's behavior on the scope axis.

C. **Defer the third edit to a separate step (Step 15.5).** Treat this
   purely procedurally: Step 15 lands as written; an additional one-line
   step bumps the third import. Requires Daniel's explicit go-ahead; same
   end state as Option A, just with a checkpoint.

I did NOT take any of A/B/C. Recording for Daniel's decision before
Step 16 runs.

**My read:** Option A is the architecturally honest one. Step 15's exit
posture in this file should be "every `data.roofing_materials` import in
the file rewired to `seeds.roofing_spec_database`; nothing else changed."
The orders may have undercounted because the third import is a deferred
function-local that doesn't surface in a quick top-of-file grep. Option C
is fine if Daniel wants a cleaner audit trail.

**RESOLUTION (Step 16 brief, 2026-04-26):** Daniel chose Option A. Line
1359 was rewired to `from seeds.roofing_spec_database import SPEC_SECTIONS,
MATERIAL_PROPERTIES` as Step 16 Part 1, before the 15-bidset sweep. After
the edit, `diff backend/core/dispatch_gate.py` against
`C:/TracePoint/core/dispatch_gate.py` shows exactly 3 changed lines, all
of identical character (data.roofing_materials → seeds.roofing_spec_database).
Line 1233 (Step 77 fallback) preserved verbatim. Zero remaining
`data.roofing_materials` references in the file. Full backend suite still
112 passed / 19 skipped, Phase 1 138/138.

---

## D-3 — STEP_17_REVIEW_CHECKLIST.md is referenced as the rubric but not on disk

**Discovered:** 2026-04-26 at the start of Step 17.

**Context:** Step 17 brief states:

> Use STEP_17_REVIEW_CHECKLIST.md as the rubric. Validate the four v0.1
> symptoms per the checklist's binary pass questions. ... gate decision per
> the checklist's threshold (≥3 of 4 symptoms PASS on ≥80% of applicable
> bidsets).

**What I observed:** No file named `STEP_17_REVIEW_CHECKLIST.md` exists
anywhere on disk. Searched:

- `C:\huck stage 2\` (top level, recursive depth 6) — not present
- `C:\huck stage 2\huckleberry\` and all subdirectories — not present
- `C:\huck stage 2\.claude\` — only `settings.local.json` is there
- `C:\huck stage 2\huckleberry\backend\` — only DISCOVERED_ISSUES.md,
  EXPERIMENT_FINDINGS.md, EXPERIMENT_PROMPT.md, README.md
- The v0.2 march orders document (which I have in conversation context)
  defined Step 17's pass criteria inline; Daniel's Step 17 brief today
  references a separate "checklist" file that should refine those
  criteria into "binary pass questions"

The brief's Step 17 contract requires the checklist to define, at
minimum:
  - The exact binary question for each of the four symptoms
  - The "applicable bidsets" denominator for each symptom (some symptoms
    target specific bidsets like Taco Bell or AutoZone; others apply
    corpus-wide)
  - The gate threshold per symptom and the corpus-wide gate

Without the checklist I would have to either (a) invent the binary
questions from the original march orders' Step 17 prose, which violates
"do not reinvent" §4.3, or (b) silently use the original prose criteria,
which conflicts with the brief's explicit instruction to use the
checklist.

**What I did NOT do:**

- Did NOT write `backend/scripts/compare_v0.1_to_v0.2.py`
- Did NOT write `backend/V0_2_VALIDATION.md`
- Did NOT measure any v0.2 outputs against an invented rubric
- Did NOT modify any production code

**Resolution options for Daniel to choose from:**

A. **Paste the checklist content into the chat** so I can save it to
   `STEP_17_REVIEW_CHECKLIST.md` at the documented path and proceed
   with Step 17 against that rubric. Cleanest. Preserves the brief's
   discipline.

B. **Authorize using the four symptom criteria from the original v0.2
   march orders' Step 17 section** (the prose that defines pass
   criteria for each symptom). I have those criteria in conversation
   context. They map cleanly to four binary questions:
     - Sym 1: Is `field_sources["project_name"].confidence` populated
       for every bidset where `project_name` is non-null? (corpus-wide,
       binary)
     - Sym 2: For Taco Bell, is `detected_system` exactly one of
       {tpo,pvc,epdm,modified_bitumen,built_up,metal_panel} with
       conf ≥ 0.7? AND for both AutoZones, is `detected_system=None`
       AND `scope_pages=[]`? (3 specific bidsets, binary)
     - Sym 3: Does `pages["18"].page_type == roof_plan` co-exist with
       `18 in project_scope.scope_pages` (drawing-vs-scope separation
       observed)? AND is the corpus-wide ratio of title-block-confirmed
       roof_plans (conf ≥ 0.9) higher than v0.1's 17/95? (mixed scope,
       binary)
     - Sym 4: For Vine Street, is `sheet_map_source == "drawing_index"`
       AND does `sheet_map` not contain `TS9D` repeated? AND no bidset
       has `sheet_map` with > 2 occurrences of any single string?
       (1 specific + corpus-wide, binary)
   This is the lowest-risk substitute and matches the brief's "binary
   pass questions" framing. End state matches A in spirit; just sources
   the rubric from the prose Daniel already wrote.

C. **Defer Step 17 entirely** until Daniel writes the checklist. Status
   stays at "Step 16 outputs produced, Step 17 blocked on rubric."

I did NOT take any of A/B/C. Recording for Daniel's decision.

**My read:** Option B is the path of least new work and least invention.
Daniel's earlier prose is already the rubric in everything but name; the
"checklist" file may have been planned as a refinement but never written,
or may exist somewhere I can't see. If Daniel just confirms "use the
march-orders prose as the binary rubric," Step 17 proceeds without
writing new criteria. Option A is best if Daniel has a specific
refinement in mind that the prose doesn't capture (e.g. tighter
thresholds, additional binary questions, different "applicable" sets).

**RESOLUTION (2026-04-26):** Daniel placed
`huckleberry/STEP_17_REVIEW_CHECKLIST.md` at the repo root as Option A.
Step 17 proceeded against that rubric. See V0_2_VALIDATION.md for results.

---

## D-4 — `to_json()` does not serialize `PlanSetContext.project` (Symptom 1 unmeasurable from JSON)

**Discovered:** 2026-04-26 during Step 17 (rubric-vs-actual-schema audit
per checklist §10).
**Filed:** 2026-04-26 per Daniel's gate-decision direction.
**Deferred to:** v0.2.1.

**Context:** STEP_17_REVIEW_CHECKLIST.md Symptom 1 inspects:

- `project.project_name`
- `project.field_sources.project_name.source`
- `project.field_sources.project_name.confidence`

**What the actual JSONs contain:** No top-level `project` field. The `to_json()`
body in `core/context.py` writes `pdf_path`, `pdf_hash`, `total_pages`,
`sheet_map_source`, `sheet_map`, `page_to_sheet`, `pages`, `all_cross_refs`,
`resolved_count`, `unresolved_count`, `all_legends`, `filters_completed`,
`dispatch_complete`, `dispatch_timestamp`, `dispatch_warnings`,
`architect_profile`, and `project_scope`. The `project` field
(`ProjectMetadata` with field_sources) is populated in memory by
`_extract_project_metadata()` but is never serialized.

**Verbatim-port confirmation (Daniel, 2026-04-26):** Grep of TracePoint's
`core/context.py` `to_json()` body confirms the same omission upstream.
The behavior is a faithful port consequence, NOT a port miss. v0.2's
discipline ("DO NOT modify ported TracePoint files") prevents fixing it
inside this version.

**Gate impact at Step 17:** Symptom 1 marked N/A. Strict rubric reading
gave 2 of 4 measurable PASS; Daniel chose path (a) ship v0.2 with the
override rationale recorded in V0_2_VALIDATION.md.

**Smallest fix when v0.2.1 work begins:** Extend `to_json()` and
`from_json()` in `core/context.py` to include the `project` block:
- `project.project_name`, `project.project_address`,
  `project.project_number`, `project.total_building_sf`, etc. (the
  ProjectMetadata.deterministic fields)
- `project.field_sources` as a dict keyed by field name with `SourceTag`
  payloads (origin, confidence, evidence)

After the fix, re-run the 15-bidset sweep (~33 min wall-clock) to
produce v0.2.1 outputs, then re-run `compare_v0.1_to_v0.2.py` against
the refreshed JSONs. Symptom 1 then becomes measurable.

This deviates from "verbatim port" discipline. v0.2.1 should formalize
the deviation: add a clearly-labelled `# v0.2.1 — extended to_json()
to surface project metadata for Symptom 1 measurability` block, gated
by the v0.2.1 ticket. Do NOT change runtime extractor behavior — only
serialization.

**v0.3 alternative:** instead of extending `to_json()`, harden cover-page
parsing so `project_name` quality is high enough that the original
checklist criterion ("non-null + populated confidence") becomes a
weaker test than what's actually shipping. v0.3 territory; not v0.2.1.

---

## D-5 — Hampshire title-block fallback propagates a non-sheet-number string ("N19A") to 7 pages (Symptom 4 FAIL)

**Discovered:** 2026-04-26 during Step 17 (Symptom 4 corpus
duplicate-sheet check).
**Filed:** 2026-04-26 per Daniel's gate-decision direction.
**Deferred to:** v0.2.1.

**Context:** STEP_17_REVIEW_CHECKLIST.md Symptom 4 corpus question:

> For every bidset, is `max(Counter(page_to_sheet.values())) <= 2`,
> EXCEPT documented multi-building cases (Bearss campus)?

**What the data show:**

- Hampshire Self Storage's `sheet_map_source` is `title_blocks` — Filter 1
  did NOT find a qualifying drawing index, so it fell back to
  `_find_sheet_on_page()` for every page.
- Pages 64, 67, 68, 69, 70, 71, 72 (7 consecutive pages, 64-72 except
  65/66) all got `page_to_sheet[i] == "N19A"`.
- Pages 38, 39, 40 (3 consecutive pages) all got
  `page_to_sheet[i] == "S3.3"`.

**Failure mode:** identical character to v0.1's Vine Street "TS9D × 7"
symptom. When the drawing-index detector misses, `_find_sheet_on_page()`
falls back to scanning short title-block text and the last 10 lines of
page text against `_SHEET_NUM_RE`. On Hampshire's structural sheets,
that pattern matched a non-sheet token (likely an engineer license
stamp like "N19A" — Florida structural engineer registration prefix —
or a surveyor signature). The matched token then propagated to every
page where the same stamp appeared.

**Why v0.2 didn't catch this:** Vine Street, the bidset on which TracePoint
calibrated the drawing-index detector, has a strong index page that
the gate accepts. The detector works on Vine Street (Symptom 4
per-bidset check passes there). Hampshire's index page (if any) doesn't
satisfy the "10+ unique sheet numbers in early pages" gate, so Filter
1 silently falls back to title-block scanning — which has the same
weakness as v0.1 had on Vine Street.

**Aggregate corpus effect:** 1 of 15 bidsets fails the corpus check.
Hampshire is the only bidset with `max_dup > 2` outside the documented
Bearss multi-building case.

**Gate impact at Step 17:** Symptom 4 FAIL. Strict rubric reading
contributed to the 2-of-4 measurable PASS count; Daniel chose path (a)
ship v0.2 with the override rationale (single-bidset, STACK-corpus,
not fixable inside verbatim-port discipline).

**Smallest fix when v0.2.1 work begins:** harden Filter 1's title-block
fallback path in `_find_sheet_on_page()`. Two options:

A. **Reject fallback matches that propagate to >N pages.** Post-pass
   over `ctx.page_to_sheet`: if any single sheet number string appears
   on >2 pages and `sheet_map_source == "title_blocks"`, re-classify
   those pages as having no sheet number. This avoids the propagation
   without changing the matching logic.

B. **Tighten the title-block regex to reject license-stamp patterns.**
   FL-style structural license numbers like `"N19A"`, `"PE12345"`,
   `"S####"` look like legitimate sheet numbers to `_SHEET_NUM_RE`.
   Adding a deny-list (or a context check — must appear in same text
   block as other sheet-like tokens) would help.

Option A is more conservative (doesn't change matching, just rejects
propagation). Option B is more invasive (changes a regex pattern
TracePoint left alone). v0.2.1 should pick A unless evidence justifies B.

This deviates from "verbatim port" discipline regardless. v0.2.1 should
formalize the deviation per the same pattern as D-4: clearly-labelled
post-pass after Filter 1 returns, gated by the v0.2.1 ticket, runtime
extractor untouched.

**v0.3 alternative:** loosen the drawing-index gate (e.g., 5+ unique
sheet numbers instead of 10+) so Hampshire-class bidsets fall into the
strong path instead of the weak fallback. Risks more false-positive
index detection on bidsets that legitimately don't have one. v0.3
territory; not v0.2.1.

---

> **Note on D-6 / D-7 / D-8 numbering:** D-6 was never assigned in
> this register. D-7 and D-8 are project-level identifiers used in
> `VALIDATION_LEDGER.md` §B as informational rows (TracePoint roofing-
> test absence; C.3a inventory miscounts). They are not file-level
> Discovered Issues entries here. The next file-level entry is D-9,
> matching `MARCH_ORDERS_profile_and_housekeeping.md` §7.4.

---

## D-9 — `glazing_module.py` docstring "known limitations" list undersells the actual code in four places

**Discovered:** 2026-04-28 during extended-thinking review of the
C.3c-build ship (commit `6001042`).
**Filed:** 2026-04-29 per `MARCH_ORDERS_profile_and_housekeeping.md`
§7.4.
**Status:** observation only. NOT a fix list. NOT scheduled.
**Belongs to:** future glazing tuning session, with the vault rule
active per CLAUDE.md §3 Decision 15. The docstring update is itself a
tuning action and goes in a vault-respecting session (`backend/core/`
frozen except for the target module).

**Context.** `backend/core/glazing_module.py` ships with an explicit
"Known limitations (rough-ship, deliberately not addressed in this
phase)" list in its module docstring (lines ~49–80). The list serves
two purposes: it tells the future tuning session where to start, and
it is the rough-ship contract the vault rule freezes around. C.3c-build
discipline (orders §1) has the docstring matching code reality.
Extended-thinking review surfaced four places where the code does
something the docstring doesn't name.

**Drift items.** All line numbers refer to `glazing_module.py` at C.3c-
build sealing commit (`6001042`); they may shift in any later commit
that modifies the file (vault rule means that should not happen
in-session anyway).

1. **Lines 686–688: three fields collapse into one classifier.**
   `door_type`, `frame_type`, and `material` all derive from a single
   `_classify_door_type(joined)` call. Three nominally-distinct
   schedule columns, one heuristic. Docstring limitation #7 covers
   single-vs-pair classification only — does NOT name the
   type/frame/material collapse. A door schedule that distinguishes
   these three fields independently would not be captured by the
   current code, regardless of how complete the schedule is.

2. **Line 214: `_NUMERIC_DOOR_RE` hardcoded to 100–199.** The bare
   numeric door-mark regex matches "typical retail" door numbering
   (door 100, 101, …, 199). Multi-story bidsets that number doors
   200–299 (second floor), 300–399 (third floor), etc., will miss
   every numeric mark above 199. The pattern is not exposed in any
   docstring limitation — the limitation list mentions architect-
   specific naming schemes outside the W-/D-/SF- prefix family but
   does not name this specific numeric range.

3. **Line 280: `_match_system` half-token threshold.** System name
   matching uses
   `best_hits >= max(1, len(best_name.split("_")) // 2)`. For two-
   token system names ("storefront_captured", "curtain_wall_4side",
   etc.), the threshold is `max(1, 1)` = 1 — i.e., any single token in
   any candidate row matches. "captured" alone matches "storefront_
   captured"; "wall" alone matches "curtain_wall_4side". The docstring
   does not name the half-token threshold or its consequence on short
   system names.

4. **Line 207: `_MARK_RE` includes more prefixes than the docstring.**
   Docstring limitation #3 enumerates W-/D-/SF-/WIN-/DOOR- as the
   recognized mark prefixes. The actual `_MARK_RE` adds HW (hardware
   set), HM (hollow metal), FR (frame?), and a bare `D` followed by a
   number. The mismatch isn't a bug — the broader regex is probably
   right — but the docstring claims a narrower surface than the code
   delivers.

**Discipline note.** D-9 is a docstring-vs-code drift issue, not a
behavior bug, but the docstring is part of the rough-ship contract and
the vault rule freezes the rough-ship contract. Fixing the docstring
mid-session would itself be a vault-rule violation. The future tuning
session for the glazing module includes "reconcile docstring with
actual code" as part of its scope.

**No action this session.** D-9 is logged here so it does not get
re-discovered. The four items above are the inventory; the tuning
session decides whether to update the docstring (cheap), tighten the
code to match (more expensive), or extend the docstring AND tighten
the regex/classifier (most invasive). Sweep observation reports
2026-04-28 + profile diagnostic 2026-04-29 are the data inputs that
inform whether any of these matter on real bidsets.

---



