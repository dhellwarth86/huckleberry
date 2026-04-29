# Page-Type Verification — Gate Report

**Date:** 2026-04-29
**Phase:** phase2-v0.3-page-type-verification
**Branch:** phase2-v0.3-page-type-verification (commit `963f0c5` at session start, single-commit branch ships at session end)
**Bidsets:** Shoppes-at-Avalon, Vine Street, Bearss Ave

---

## §1 — What was verified

Three coupled bugs hypothesized by extended-thinking Claude on 2026-04-29 in dispatch's table-extraction path:

- **Bug 1 — page-type ordering.** `dispatch_gate._PAGE_TYPE_RULES` has ELEVATION (line 110) and DETAIL (line 111) before SCHEDULE (line 112). First-match-wins. Combined-content sheet titles like 'DOOR & WINDOW SCHEDULES, FRAMES & DETAILS' match DETAIL first.
- **Bug 2 — Filter 4 narrow gate.** Line 839 only runs `extract_tables` on `page_type == SCHEDULE_SHEET`. Coupled to Bug 1.
- **Bug 3 — `trade_input_builder` contract drift.** C.3b extended `TradeModuleInput` with `tables: Optional[list[Any]] = None`, but the C.2 verbatim port of `trade_input_builder.py` was never extended to populate it.

## §2 — Hypothesis status across the three bidsets

| Bidset | Schedule-bearing pages | Classified `schedule_sheet` today | Would under simulation | Tables extracted on changed pages |
|---|---:|---:|---:|---:|
| shoppes-at-avalon | 1 | 0 | 1 | 558 tables / 2236 rows |
| vine-street | 0 | 0 | 0 | 172 tables / 980 rows |
| bearss-ave | 3 | 1 | 2 | 832 tables / 4685 rows |
| **Total** | **4** | **1** | **3** | **1562 / 7901** |

**Bug 1 is PARTIALLY CONFIRMED by this data.** Threshold applied: misclassification rate of schedule-bearing pages under current dispatch ordering = 3 / 4 = 75.00%; >=80% = CONFIRMED, <=20% = REFUTED, in between = PARTIALLY CONFIRMED.

## §3 — Filter 4 cache status (Bug 3 audit)

**Bug 3 is CONFIRMED — no raw tables cached on PlanSetContext or PageContext.**

Implication string (from Block 3 payload):

> raw tables not cached anywhere on PlanSetContext or PageContext; the eventual fix needs either (a) cache add to PlanSetContext or PageContext (touches dispatch's data contract), (b) per-page re-extraction in trade_input_builder (the harness pattern the sweep + profile already use; pays extract_tables cost twice if Filter 4 also runs on the same page), or (c) extension of _parse_tables_on_page in dispatch_gate.py to optionally cache raw tables alongside the Legend objects (one-touch, dispatch-side).

Evidence (from `dispatch_gate.py` lines 733–878 + `context.py` PlanSetContext + PageContext field lists):

- dispatch_gate.py line 744: tables = page.extract_tables() — local-scope
- dispatch_gate.py line 768-776: legends.append(Legend(...)) — wraps each table into a Legend object
- dispatch_gate.py line 777: return legends — returns Legend objects, not raw tables
- dispatch_gate.py line 840-841: legends.extend(table_legends) — only Legend objects propagated
- dispatch_gate.py line 855: ctx.all_legends = clean_legends — only filtered Legend objects stored
- context.py PlanSetContext + PageContext — no 'tables' or 'raw_tables' field; field lists enumerated above

## §4 — Coupling diagnostic — what the simulation+extraction proved

### shoppes-at-avalon

- Total pages: 97; pages that would change classification: 13
- Schedule-bearing not currently classified: 1; would flip under simulation: 1
- Block 5 validated 13 of 13 flipped pages (cap applied: False, hard cap abort: False); 13 produced ≥1 table; 558 tables / 2236 rows total in 61.55s (median per-page ~4734ms).

### vine-street

- Total pages: 138; pages that would change classification: 32
- Schedule-bearing not currently classified: 0; would flip under simulation: 0
- Block 5 validated 20 of 30 flipped pages (cap applied: True, hard cap abort: False); 20 produced ≥1 table; 172 tables / 980 rows total in 126.69s (median per-page ~6334ms).

### bearss-ave

- Total pages: 91; pages that would change classification: 18
- Schedule-bearing not currently classified: 2; would flip under simulation: 2
- Block 5 validated 17 of 17 flipped pages (cap applied: False, hard cap abort: False); 17 produced ≥1 table; 832 tables / 4685 rows total in 102.66s (median per-page ~6039ms).

Production-cost estimate for fixing Bug 1 alone: a one-line ordering change in `_PAGE_TYPE_RULES` plus the empirical table-extraction cost of 50 validated changed pages ≈ 290.9s across the three bidsets (extrapolating from validated subset to full changed-page set is a future-phase decision, not made here).

## §5 — Soft observations

- New misclassifications under simulation: 57 pages across the three bidsets would classify as `schedule_sheet` under SCHEDULE-first ordering despite NOT containing 'SCHEDULE' in their sheet title. Per-bidset breakdown in each report's Block 4 payload (`new_misclassifications_sample`). This is the §7 stop #9 surface — soft observation, not §7 stop. The future fix-orders conversation decides whether this is acceptable collateral damage of fixing Bug 1, or whether a more targeted approach (e.g., keyword precedence or whole-word matching) is needed.
- Block 5 wall-clock soft-cap (120s) exceeded on: ['vine-street']. Hard cap (360s) not reached on any bidset.

## §6 — Discipline check

- Vault rule: held (5 modules untouched — `roofing_module.py`, `glazing_module.py`, `roofing_vocabulary.py`, `glazing_vocabulary.py`, `debug_module.py`).
- §0 fix-prohibition: held. `dispatch_gate.py` and `trade_input_builder.py` byte-identical to pre-session state (SHA-1 verification recorded in commit message).
- Sacred floor: 216/19/0 backend; frontend at baselines (verified at session start and end).
- §7 stops: status of each enumerated below.

## §7 — Implications for next planning conversation

With Bug 1 PARTIALLY CONFIRMED and Bug 3 CONFIRMED — no raw tables cached on PlanSetContext or PageContext, the next planning conversation has data to choose:

- **Bug 1 partially confirmed.** Some schedule-bearing pages misclassify, some don't. Whether the partial rate justifies the ordering fix depends on what kind of partial — Daniel and extended-thinking Claude discuss before committing to fix-orders.

Either way, this phase shipped verification, not fix.

## §8 — Done definition

Per `MARCH_ORDERS_page_type_verification.md` §10 — full checklist confirmed in the gate report message at end of session.

## §9 — Standing by
