# MARCH ORDERS — Page-Type Verification + Coupling Diagnostic

**Date issued:** 2026-04-29
**Issued by:** Daniel (via extended-thinking Claude planning session)
**Executed by:** Claude Code
**Phase shape:** Single session, autonomous, soft-gates-only, single final gate report
**Read first:** PROJECT_CLAUDE.md, CLAUDE.md, VALIDATION_LEDGER.md, then this document

---

## §0 — What this phase is and is not

**Is:** read-only diagnostic that tests an extended-thinking hypothesis about three coupled bugs in dispatch's table-extraction path:

- **Bug 1 (page-type ordering):** `dispatch_gate.py` `_PAGE_TYPE_RULES` (lines 105–119) evaluates ELEVATION (line 110) and DETAIL (line 111) BEFORE SCHEDULE (line 112). First match wins. Combined-content sheet titles like "DOOR & WINDOW SCHEDULES, FRAMES & DETAILS" match ELEVATION or DETAIL first and never reach SCHEDULE.
- **Bug 2 (Filter 4 conditional gate skips most schedule pages):** `dispatch_gate.py` line 839 only runs `extract_tables` on `page_type == PageType.SCHEDULE_SHEET`. If Bug 1 misclassifies most schedule-bearing pages, Filter 4 effectively never extracts tables on them.
- **Bug 3 (trade_input_builder.py contract drift):** C.3b extended `TradeModuleInput` with `tables: Optional[list[Any]] = None`, but `trade_input_builder.py` (the C.2 verbatim port) was never extended to populate it. Sweep + profile harnesses bypass the official builder and call `extract_tables` per page themselves, which is the 824s cost driver on Bearss.

**Is NOT:** a fix for any of these bugs. No code changes to `dispatch_gate.py`. No code changes to `trade_input_builder.py`. No tuning. No simulation runs that mutate state. Vault rule active throughout — five vault-ruled modules read-only.

**The three diagnostic outputs this phase produces:**

1. **Page-type histogram** for each of the three sweep bidsets — what `page_type` does Filter 2 actually produce for each page, and how many "schedule-bearing" sheets (sheet title contains "SCHEDULE") classify as something OTHER than SCHEDULE_SHEET? This is the empirical test of Bug 1.

2. **Filter 4 cache audit (static read)** — does dispatch's `_parse_tables_on_page` cache the raw tables anywhere on `PlanSetContext`, or only the derived `Legend` objects? This determines what Bug 3's eventual fix has to look like (if raw tables aren't cached, the eventual fix needs a small dispatch-side extension; if they are, `trade_input_builder.py` just reads from there).

3. **Page-type ordering simulation + table-extraction validation** — re-classify each page under a simulated `_PAGE_TYPE_RULES` ordering with SCHEDULE moved to position 1. For pages that change classification, run `extract_tables` and measure the empirical "what would Filter 4 have done if Bug 1 weren't blocking it." This is the coupling diagnostic — Bug 1's effect on Bug 2's gate, measured per page.

**End state:** three structured reports + one terminal log + one gate report. Daniel reviews. If hypothesis confirmed, fix-orders drafted in a separate session. If hypothesis rejected or partially supported, the data in hand reframes the next planning conversation.

This phase ships **the verification, not the fix.** No fix code lands in this session under any circumstances.

---

## §1 — Pre-flight reads (Karpathy step 1)

Full reads, in this order:

1. **PROJECT_CLAUDE.md** — entry point. Note §3's coverage of the open Path (a)/(b)/(c) decision; this verification informs that decision.
2. **CLAUDE.md** — §3 Decision 15 (vault rule, current 5-module list). §6 hard guardrails. §9 anti-patterns.
3. **VALIDATION_LEDGER.md** — sacred floors (216/19/0 backend); §D existing rows for sweep + profile diagnostic.
4. **`backend/core/dispatch_gate.py`** lines 100–135 (`_PAGE_TYPE_RULES` and discipline mapping), lines 421–470 (`_classify_page_type` + `run_filter_2`), lines 733–855 (`_parse_tables_on_page` + `_quality_check_legends` + `run_filter_4`), lines 1440–1505 (`run_dispatch`). Read-only inspection — vault rule does not apply to dispatch_gate.py (NOT vault-ruled), but no modifications this session per §0.
5. **`backend/core/trade_input_builder.py`** entire file (~150 lines). Confirm the absence of any `extract_tables` call and any `tables=` keyword on the `TradeModuleInput` constructor.
6. **`backend/core/context.py`** — read PlanSetContext + PageContext dataclass definitions. The Filter 4 cache audit needs to enumerate every field on these dataclasses to confirm whether raw tables are stored.
7. **`backend/core/trade_module.py`** — confirm the `tables` field added to `TradeModuleInput` in C.3b. Note its type annotation.
8. **`backend/SWEEP_OBSERVATION_shoppes-at-avalon.md`**, **`backend/SWEEP_OBSERVATION_vine-street.md`**, **`backend/SWEEP_OBSERVATION_bearss-ave.md`** — each report's section 3 (`page_intelligence`) is the cross-reference data for the simulation step. Skim, don't deep-read.
9. **`backend/scripts/profile_diagnostic.py`** — the harness shape this verification harness reuses (timing helper, page selection input, output structure).

Read-only inspection of `roofing_module.py`, `glazing_module.py`, `roofing_vocabulary.py`, `glazing_vocabulary.py`, `debug_module.py` is NOT needed for this phase. Don't open them.

---

## §2 — Step Verify.0: Pre-flight verification

- Run the full backend suite. Floor: **216 passed, 19 skipped, 0 failed**. Hard stop if not met.
- Run the four frontend test suites at sacred floors: `run_tests.js` 107/107, spotchecks 7/4/8/14, mutations 8/8 caught.
- Verify branches:
  - `phase2-v0.3-profile-and-housekeeping` head = `963f0c5` (current; pushed)
- All three bidset PDFs locatable at `C:/huck stage 2/full bid sets/` (or workspace equivalent):
  - Shoppes-at-Avalon
  - Vine Street
  - Bearss Ave
- Confirm `git remote -v` shows `https://github.com/dhellwarth86/huckleberry.git`.

---

## §3 — Step Verify.1: Branch

Branch from current housekeeping head:

```
phase2-v0.3-page-type-verification  (NEW; from 963f0c5)
```

Single commit at end of session — three reports + one terminal log + harness. Branch pushed at end. No second commit, no incremental commits.

---

## §4 — Step Verify.2: Build the verification harness

Create `backend/scripts/page_type_verification.py` (tracked — reusable diagnostic, like `profile_diagnostic.py`).

The harness has **four diagnostic blocks**, each clearly delimited for grep extraction. The block format is mandatory and consistent:

```
##DIAG_START:<block_name>:<bidset_short>##
<JSON or structured payload, indented for human reading>
##DIAG_END:<block_name>:<bidset_short>##
```

Block names (exactly these, lowercase, snake_case):
- `page_type_histogram`
- `schedule_bearing_audit`
- `filter4_cache_audit` (one-shot, no bidset suffix — static read of dispatch_gate.py + context.py source)
- `reclassification_simulation`
- `table_extraction_validation`

These delimiters appear in BOTH the terminal output AND the per-bidset reports' raw-data sections. Cleanup for grep is mechanical:

```
sed -n '/##DIAG_START:page_type_histogram:bearss-ave##/,/##DIAG_END:page_type_histogram:bearss-ave##/p' terminal.log
```

### Diagnostic block contents

**Block 1: `page_type_histogram` (per bidset)**

For each bidset, run `run_dispatch`, then enumerate `ctx.pages`. For each page, capture:
- `page_idx`
- `sheet_num` (from `ctx.page_to_sheet`)
- `sheet_title` (from `ctx.sheet_map[sheet_num].title` if mapped, else `null`)
- `page_type` (the enum's `.value` — string)
- `confidence` (the float on `page_ctx`)
- `has_legend` (bool)
- `has_schedule` (bool — set by Filter 4 if any legend with type ending in `_schedule`)
- `legend_count` (int — `len(page_ctx.legends)`)

Then compute:
- Histogram: `Counter(page_type for page in ctx.pages.values())`. Print sorted by count descending.
- Total pages, total mapped pages, total pages with `has_legend=true`, total with `has_schedule=true`.

**Block 2: `schedule_bearing_audit` (per bidset)**

For each page, the harness computes a heuristic "schedule-bearing" flag:
- `is_schedule_bearing = "SCHEDULE" in (sheet_title or "").upper() if sheet_title else False`

This is the "ground truth" approximation for the histogram cross-check. It is not real ground truth — it just tests whether the sheet's title self-identifies as schedule-bearing.

For each schedule-bearing page, capture:
- `page_idx`, `sheet_num`, `sheet_title`
- Current `page_type` (what Filter 2 actually produced)

Then compute:
- Total schedule-bearing pages (per heuristic).
- Of those, how many classify as `SCHEDULE_SHEET` today.
- Of those, how many classify as something else (DETAIL_SHEET, ELEVATION, MEP_PLAN, UNKNOWN, etc.). For each "other" classification, list `(page_idx, sheet_num, sheet_title, current_type)`.

This block is the empirical test of Bug 1. If most schedule-bearing pages already classify as SCHEDULE_SHEET, Bug 1 is mostly false. If most classify as DETAIL_SHEET / ELEVATION, Bug 1 is confirmed.

**Block 3: `filter4_cache_audit` (one-shot, static read — no bidset)**

This block is produced ONCE per run, not per bidset. It's a static-read summary of:
- The full field list of `PlanSetContext` from `context.py` (or wherever it's defined).
- The full field list of `PageContext`.
- A specific search: does any field name contain "table", "raw_table", "extracted_table", or similar?
- The body of `_parse_tables_on_page` from `dispatch_gate.py` lines 733–779. Specifically: where does its return value go in `run_filter_4` (line 840)? It assigns to `table_legends`, then `legends.extend(table_legends)`. The raw `tables` list is NOT stored — only the derived Legend objects.
- The body of `run_filter_4` lines 829–878. Confirm: no caching of raw tables anywhere on the context.

The block payload is a structured dict:

```json
{
  "plan_set_context_fields": ["pdf_path", "pages", "sheet_map", "all_legends", "..."],
  "page_context_fields": ["page_idx", "page_type", "legends", "has_legend", "has_schedule", "..."],
  "table_field_search": {
    "fields_with_table_in_name": [],
    "any_raw_tables_cached": false,
    "evidence_lines": ["dispatch_gate.py:777 returns Legend list, not tables", "..."]
  },
  "implication_for_bug3_fix": "raw tables not cached anywhere; eventual fix needs either (a) cache add to PlanSetContext, or (b) per-page re-extraction in trade_input_builder, or (c) extension of _parse_tables_on_page to optionally cache raw tables."
}
```

Where the "implication" string is the harness's mechanical observation, not a recommendation. Daniel and extended-thinking Claude make the architectural call about which fix path to pursue.

**Block 4: `reclassification_simulation` (per bidset)**

The harness does NOT modify `dispatch_gate.py`. Instead, it reads `_PAGE_TYPE_RULES` directly from the imported module, makes a deep copy of the rules list, **moves the SCHEDULE rule to position 0**, and then reproduces the classification logic locally:

```python
# pseudocode, not literal
from core.dispatch_gate import _PAGE_TYPE_RULES, _classify_page_type
import copy

simulated_rules = copy.deepcopy(_PAGE_TYPE_RULES)
# find SCHEDULE rule index, pop it, insert at 0
# reproduce _classify_page_type's logic locally with simulated_rules

def _simulated_classify(title_text, full_text, rules):
    title_upper = title_text.upper()
    full_upper = full_text.upper()
    for keywords, ptype, title_conf, page_conf in rules:
        for kw in keywords:
            if kw in title_upper:
                return (ptype, title_conf)
    for keywords, ptype, title_conf, page_conf in rules:
        for kw in keywords:
            if kw in full_upper:
                return (ptype, page_conf)
    return (PageType.UNKNOWN, CONFIDENCE_UNKNOWN)
```

The simulation re-classifies each page using the same `title_text` and `full_text` Filter 2 used. (The harness does NOT re-extract; it pulls the already-extracted text from a re-run of Filter 1 + 2 done locally, OR — preferred — runs Filter 2's input-extraction code path once and caches per-page text.)

For each page, capture:
- `page_idx`, `sheet_num`, `sheet_title`
- `current_type` (what real dispatch produced — already in Block 1's data)
- `simulated_type` (what the SCHEDULE-first ordering would produce)
- `changed` (bool — did the type change?)

Then compute:
- Total pages where classification changed under simulation.
- For changed pages: histogram of `(current_type → simulated_type)` transitions.
- Cross-check: of the schedule-bearing pages from Block 2 that don't currently classify as SCHEDULE_SHEET, how many would under simulation? Report counts and a per-page list.

**This is the coupling test.** If Bug 1 is real, the simulation should re-classify most/all of Block 2's "schedule-bearing but not SCHEDULE_SHEET" pages as SCHEDULE_SHEET. If Bug 1 is false, very few pages would change.

**Block 5: `table_extraction_validation` (per bidset, capped)**

For each page in Block 4 that changed classification from non-SCHEDULE_SHEET to SCHEDULE_SHEET under simulation, run `pdfplumber.extract_tables` and capture:
- `page_idx`
- Number of tables extracted
- Total rows across all tables
- First 80 chars of each table's first row (header)
- Wall-clock time for `extract_tables` on this page (single run, `time.perf_counter`)

**Hard cap: 20 pages per bidset.** If more than 20 pages changed classification, sort by some signal (Block 1's `legend_count` or similar) and take the top 20. Document the cap in the report — "extracted on 20 of N changed pages, ranked by legend_count."

**Total wall-clock budget for this block: ~60s per bidset.** If it exceeds 120s, that's a soft observation in the gate report (records the empirical cost of bulk re-extraction; not a §7 stop).

This block is the empirical evidence of "what tables would Filter 4 have produced if Bug 1 weren't blocking it." If the changed pages have actual tables (door schedules, mechanical schedules, etc.), the cost of fixing Bug 1 was indeed buying real value. If they're empty, Bug 1's effect was overestimated.

---

## §5 — Step Verify.3: Per-bidset reports

After all four blocks run for a bidset, the harness writes `backend/PAGE_TYPE_VERIFICATION_<bidset_short_name>.md` with this skeleton:

```markdown
# Page-Type Verification — <Bidset Display Name>

**Date:** 2026-04-29
**Phase:** Page-type verification + coupling diagnostic
**Bidset file:** <full path>
**Page count:** <N>
**Dispatch wall-clock:** <s>

## §1 — Block 1: Page-Type Histogram

(Histogram table sorted descending. Total pages, mapped pages, has_legend pages, has_schedule pages.)

##DIAG_START:page_type_histogram:<bidset_short>##
{ ...full payload... }
##DIAG_END:page_type_histogram:<bidset_short>##

## §2 — Block 2: Schedule-Bearing Audit

(Total schedule-bearing pages. How many classify as SCHEDULE_SHEET today. How many don't, with per-page list of [page_idx, sheet_num, sheet_title, current_type].)

##DIAG_START:schedule_bearing_audit:<bidset_short>##
{ ...full payload... }
##DIAG_END:schedule_bearing_audit:<bidset_short>##

## §3 — Block 4: Reclassification Simulation

(Total pages where classification changed under SCHEDULE-first ordering. Transition histogram. Schedule-bearing-page coverage check.)

##DIAG_START:reclassification_simulation:<bidset_short>##
{ ...full payload... }
##DIAG_END:reclassification_simulation:<bidset_short>##

## §4 — Block 5: Table Extraction Validation

(Per-page detail: tables extracted, row count, headers, wall-clock. Total tables/rows/wall-clock across the changed pages. Cap noted if >20 pages.)

##DIAG_START:table_extraction_validation:<bidset_short>##
{ ...full payload... }
##DIAG_END:table_extraction_validation:<bidset_short>##

## §5 — Cross-Reference With Sweep Section 3

For each page in §4 that produced ≥2 tables under validation, look up its section 3 entry from `SWEEP_OBSERVATION_<bidset>.md`. Report:
- `page_idx`, current `page_type`, `has_legend`, `legend_count`
- Did sweep's section 3 already flag this page as legend-rich?

(Short table; one row per validated page with ≥2 tables.)

## §6 — Observations (no fixes, no recommendations)

(3–6 plain "Observed:" statements describing the histogram shape, the schedule-bearing-vs-classified delta, the simulation transition counts, and what the validated table extractions found. NEVER "should be:", "recommend:", "looks like a bug:". The gate-level observation about Bug 1's confirmation/refutation lives in the gate report, not here.)

## §7 — Closing

Diagnostic only. Three coupled bugs hypothesized by extended-thinking Claude 2026-04-29 are tested by this report's data. The gate report (separate file) summarizes hypothesis status across all three bidsets. No fixes were attempted. dispatch_gate.py and trade_input_builder.py NOT modified. Vault rule held — five vault-ruled modules untouched.
```

Three reports total: `PAGE_TYPE_VERIFICATION_shoppes-at-avalon.md`, `PAGE_TYPE_VERIFICATION_vine-street.md`, `PAGE_TYPE_VERIFICATION_bearss-ave.md`.

The Block 3 (`filter4_cache_audit`) one-shot output goes in a separate single-bidset-agnostic file: `backend/PAGE_TYPE_VERIFICATION_filter4_cache_audit.md`.

---

## §6 — Step Verify.4: Combined gate report

A separate markdown file: `backend/PAGE_TYPE_VERIFICATION_GATE_REPORT.md`.

This is the gate report for the phase, not a per-bidset report. Skeleton:

```markdown
# Page-Type Verification — Gate Report

**Date:** 2026-04-29
**Phase:** phase2-v0.3-page-type-verification
**Branch:** phase2-v0.3-page-type-verification (commit <sha>)

## §1 — What was verified

(One paragraph restating the three coupled bugs Hypothesis from extended-thinking Claude.)

## §2 — Hypothesis status across the three bidsets

| Bidset       | Schedule-bearing pages | Classified SCHEDULE_SHEET today | Would under simulation | Tables extracted on changed pages |
|--------------|------------------------|----------------------------------|------------------------|------------------------------------|
| Shoppes      | <N>                    | <N>                              | <N>                    | <N tables / <M rows>               |
| Vine Street  | <N>                    | <N>                              | <N>                    | <N tables / <M rows>               |
| Bearss Ave   | <N>                    | <N>                              | <N>                    | <N tables / <M rows>               |
| **Total**    | **<N>**                | **<N>**                          | **<N>**                | **<N> / <M>**                      |

(One sentence: "Bug 1 is CONFIRMED / PARTIALLY CONFIRMED / REFUTED by this data" with the evidence threshold named — e.g., "≥80% of schedule-bearing pages misclassify under current ordering" = confirmed, "<20%" = refuted, between = partial.)

## §3 — Filter 4 cache status (Bug 3 audit)

(Quote the implication string from Block 3. Confirm no raw tables cached. List the dispatch_gate.py + context.py line numbers that document the absence.)

## §4 — Coupling diagnostic — what the simulation+extraction proved

(Per-bidset summary of: pages that would change classification, how many produced ≥2 tables under validation, total table count vs sweep's Filter 4 quality-gate output. Estimate of "production cost of fixing Bug 1 alone" based on changed-page count × measured per-page extract_tables time.)

## §5 — Soft observations

(Anything Block 5's wall-clock surfaced. Anything the simulation produced that was unexpected — e.g., schedule-first ordering causing NEW misclassifications elsewhere. Run-to-run variance noted.)

## §6 — Discipline check

- Vault rule: held (5 modules untouched).
- §0 fix-prohibition: held (dispatch_gate.py + trade_input_builder.py untouched).
- Sacred floor: 216/19/0 backend; frontend baselines.
- §7 stops: status of each.

## §7 — Implications for next planning conversation

(One paragraph: "If Bug 1 is confirmed, fix-orders for the page-type ordering change are the next phase. If refuted, the 824s cost driver is somewhere else and the next planning conversation needs different data. Either way, this phase shipped verification, not fix.")

## §8 — Done definition (full checklist below in §10 of march orders)

(Tick each box, point to receipts.)

## §9 — Standing by
```

This gate report is what Daniel reads first after the run lands.

---

## §7 — Step Verify.5: Terminal log capture

The harness writes a complete terminal log to `backend/PAGE_TYPE_VERIFICATION_terminal.log`.

The harness should:
- Use a `Tee` class that writes to BOTH stdout and the log file simultaneously (so Daniel sees it live AND has a captured artifact).
- Print every diagnostic block in full to both surfaces, with the `##DIAG_START:...##` / `##DIAG_END:...##` delimiters intact.
- Print a clear opening banner (date, branch, commit SHA, bidset list) and closing banner (wall-clock totals, status).
- Print per-bidset section banners (e.g., `=== BIDSET 1 of 3: shoppes-at-avalon ===`).
- Print warning lines for any soft observation (e.g., "WARN: bidset X took 180s for Block 5, exceeded 120s soft cap").

**The log is committed to the branch.** It is the verbatim record of the run. Future debugging or independent reproduction can replay against this log.

The harness's verbose-print surface should be cleanly bounded for future cleanup. Recommended structure:

```python
# ============================================================
# DIAGNOSTIC OUTPUT (delete this section to run silently)
# All ##DIAG_START / ##DIAG_END print sites are gathered in
# diag_block(). Set DIAGNOSTIC_MODE=False at top to disable.
# ============================================================
DIAGNOSTIC_MODE = True

class Tee:
    def __init__(self, *streams): self.streams = streams
    def write(self, s):
        for s_ in self.streams: s_.write(s); s_.flush()
    def flush(self):
        for s_ in self.streams: s_.flush()

def diag_block(name: str, payload, bidset: str | None = None):
    if not DIAGNOSTIC_MODE: return
    suffix = f":{bidset}" if bidset else ""
    print(f"##DIAG_START:{name}{suffix}##")
    print(json.dumps(payload, indent=2, default=str))
    print(f"##DIAG_END:{name}{suffix}##")
# ============================================================
# END DIAGNOSTIC SECTION
# ============================================================
```

Future cleanup: delete the bounded section, set DIAGNOSTIC_MODE=False, or replace `diag_block` calls with logging at a lower level. All three are mechanical edits.

---

## §8 — §7 Stop Conditions

Stop, report, wait for Daniel if any fire:

1. **Sacred floor regresses.** 216/19/0 backend or frontend baselines. Hard stop.
2. **Any bidset cannot be located.** Stop and ask. Do not substitute.
3. **Dispatch raises** on any bidset. (Did not raise during sweep 2026-04-28; did not raise during profile 2026-04-29; if it raises now, something changed.)
4. **`extract_tables` raises** on any page during Block 5 validation. Capture traceback; soft-skip that page; record in report. Hard stop only if it raises on >50% of attempted pages (signals an extractor-side issue, not edge-case noise).
5. **Need to modify any `backend/core/` file** for any reason. Hard stop. Vault rule active. dispatch_gate.py + trade_input_builder.py also forbidden under §0 — even though neither is vault-ruled, this phase's discipline forbids touching them.
6. **Need to add a dependency.** Hard stop. `pdfplumber`, `time`, `json`, `copy`, `statistics` — all already present.
7. **Block 5 wall-clock exceeds 5 minutes per bidset.** Soft observation, not stop, but cap individual bidset Block 5 at 6 minutes hard — if reached, abort the rest of that bidset's Block 5 with a partial-data note in the report. Move on.
8. **Hypothesis comes back REFUTED** (i.e., schedule-bearing pages mostly already classify as SCHEDULE_SHEET, or simulation barely changes any classifications, or changed pages produce no tables). NOT a §7 stop. The verification's job is to find this out. Document in the gate report and continue. Refutation is a perfectly good outcome.
9. **Block 4 simulation produces NEW misclassifications** (e.g., a non-schedule sheet that currently classifies as ELEVATION starts classifying as SCHEDULE_SHEET because its title accidentally contains "SCHEDULE" somewhere). Soft observation in §5 of gate report — quantify the new misclassification rate. NOT a stop.

---

## §9 — Discipline reminders (Karpathy)

1. **Read first.** All §1 docs in full. Especially `dispatch_gate.py` lines 100–135 + 421–470 + 733–878 — the architectural anchor for the whole hypothesis.
2. **Sacred floor first.** 216/19/0 before, after diagnostic, after commit, after push.
3. **Minimum implementation.** Five diagnostic blocks. Not six. Not "let me also profile X while I'm here." If you find another interesting question during the run, write it down for next planning conversation; do NOT add a Block 6.
4. **Vault rule held.** Five vault-ruled modules read-only. dispatch_gate.py + trade_input_builder.py also read-only this phase.
5. **No fix this session.** §0 is non-negotiable. If the data screams "obvious 1-line fix here," resist. Future Daniel + extended-thinking Claude will read this data and decide. The diagnostic-fix separation is the discipline.
6. **Observation discipline.** Per-bidset reports' §6 sections use "Observed:" prefix only. Same load-bearing rule as sweep + profile. No "should be:", "recommend:", "looks like a bug:" anywhere in any report. The gate report is allowed ONE evaluative sentence: "Bug 1 is CONFIRMED / PARTIALLY CONFIRMED / REFUTED by this data." That's it. No further evaluation.
7. **Hypothesis humility.** Extended-thinking Claude built this hypothesis from code-reading. The data may show I was wrong. That's a feature, not a failure. The gate report says what the data says.

---

## §10 — Done definition (gate report checklist)

The final gate report must confirm:

- [ ] Pre-flight: 216/19/0 backend; frontend at baselines; branches correct; all three bidsets located
- [ ] `backend/scripts/page_type_verification.py` written and runs cleanly (tracked, reusable)
- [ ] Block 1 (page_type_histogram) produced for all three bidsets
- [ ] Block 2 (schedule_bearing_audit) produced for all three bidsets
- [ ] Block 3 (filter4_cache_audit) produced once (not per bidset)
- [ ] Block 4 (reclassification_simulation) produced for all three bidsets
- [ ] Block 5 (table_extraction_validation) produced for all three bidsets, with cap-noted (≤20 pages) per bidset
- [ ] All diagnostic blocks use the `##DIAG_START:<name>:<bidset>##` / `##DIAG_END:<name>:<bidset>##` delimiter format consistently
- [ ] `backend/PAGE_TYPE_VERIFICATION_shoppes-at-avalon.md`, `_vine-street.md`, `_bearss-ave.md` saved per §5 skeleton
- [ ] `backend/PAGE_TYPE_VERIFICATION_filter4_cache_audit.md` saved (Block 3 standalone)
- [ ] `backend/PAGE_TYPE_VERIFICATION_GATE_REPORT.md` saved per §6 skeleton with hypothesis status sentence
- [ ] `backend/PAGE_TYPE_VERIFICATION_terminal.log` captured (Tee output to stdout + file)
- [ ] All per-bidset reports' §6 sections use "Observed:" prefix only (zero forbidden-language hits)
- [ ] No `backend/core/` modification (verified by `git diff --stat`)
- [ ] No `pyproject.toml` change
- [ ] dispatch_gate.py and trade_input_builder.py byte-identical to pre-session state (verified by SHA-1)
- [ ] Backend suite still 216/19/0 (zero new tests)
- [ ] Frontend at baseline
- [ ] Single commit on `phase2-v0.3-page-type-verification`; pushed to origin
- [ ] §7 stops: status of each enumerated explicitly (likely none; #8 / #9 may surface as soft observations)
- [ ] All three §1 PDFs accessible at expected path (no fallback substitution)
- [ ] Final gate report produced

---

## §11 — Commit shape

**Single commit** on `phase2-v0.3-page-type-verification`:

- `backend/scripts/page_type_verification.py` (NEW — tracked harness)
- `backend/PAGE_TYPE_VERIFICATION_shoppes-at-avalon.md` (NEW)
- `backend/PAGE_TYPE_VERIFICATION_vine-street.md` (NEW)
- `backend/PAGE_TYPE_VERIFICATION_bearss-ave.md` (NEW)
- `backend/PAGE_TYPE_VERIFICATION_filter4_cache_audit.md` (NEW)
- `backend/PAGE_TYPE_VERIFICATION_GATE_REPORT.md` (NEW)
- `backend/PAGE_TYPE_VERIFICATION_terminal.log` (NEW — verbatim run log)

Commit message body: hypothesis status (CONFIRMED/PARTIAL/REFUTED) on one line, total schedule-bearing pages across 3 bidsets, total pages that would re-classify under simulation, total tables empirically extracted on changed pages. List any §7 stops fired (none expected) and any §7 #8 / #9 soft observations.

Push at end of session. Authorized. If push fails, §7 stop.

---

## §12 — Execution mode

**Single chunk, autonomous, soft gates only.** If pre-flight reads complete cleanly and no §7 stop fires, execute Verify.0 through Verify.5 without pausing for confirmation. Single final gate report.

Soft observations (per-bidset Block 5 cap reached, surprising simulation transitions, run-to-run dispatch variance) go in the gate report. Do not pause for those.

Total wall-clock estimate: 3 bidsets × (~80s dispatch + ~60s Blocks 1–4 each + ~120s Block 5 budget) ≈ 13 minutes plus harness write/test/commit. Allow 30 minutes total session.

---

## §13 — Closing

After the gate report lands, Daniel reviews:

1. **Hypothesis status** (the one evaluative sentence in §2 of the gate report).
2. **The Block 2 / Block 4 numbers** (how many schedule-bearing pages misclassify, how many would re-classify under simulation).
3. **The Block 5 numbers** (how many tables would actually be extracted under correct classification — this is the empirical "what's at stake").

The next planning conversation chooses, with data in hand:

- **If CONFIRMED:** Bug 1 fix-orders next (small dispatch_gate.py change). Bug 3 fix-orders after that (trade_input_builder.py extension), informed by Block 3's `filter4_cache_audit` output about which architectural fix path is cleanest.
- **If REFUTED:** the 824s cost driver lives somewhere extended-thinking Claude didn't anticipate. Next conversation needs different data — possibly a profile of `extract_tables` cost on already-SCHEDULE_SHEET pages, or instrumenting `pdfplumber` itself.
- **If PARTIAL:** depends on what kind of partial. We'd discuss before committing to fix-orders.

Either way, this phase ships verification, not fix. Standing by for execution.

**End of MARCH_ORDERS_page_type_verification.md.**
