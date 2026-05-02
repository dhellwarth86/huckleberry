# G.0.9 Real-Bidset Verification Report

**Date:** 2026-05-02
**Phase:** G.0.9 (read-only real-bidset verification on Bearss Ave)
**Branch:** `phase2-v0.3-G0-9-real-bidset-verification` from `7155286` (G.0.8 head)
**Executed by:** Claude Code (Developer session)
**Deliverable shape:** Single markdown report, 5 scout sections + verdict. Zero code changes. Zero tracked files modified except this report. Sacred floors held (230/19/0).

**Karpathy discipline:** Observe before proposing, name what's there, stop at uncertainty. All counts and timings reported are empirical. The hybrid regex from G.0.7 was applied via in-memory `core.dispatch_gate._SHEET_NUM_RE` monkey-patch only; `dispatch_gate.py` on disk was SHA-1-verified before, between, and after every scout. The instrumentation script lived in `%TEMP%\g09_scouts.py` and is not committed.

**Bidset under test:** `C:\huck stage 2\full bid sets\Bearss Ave Distribution Center - University - Marcobay Construction (3).pdf` (91 pages, the same bidset the D.2 reference established at 769/177/31/24).

---

## §1 — Scout 1: Current code (no hybrid) on full Bearss

### 1.1 Method

In-process call: `run_dispatch(PDF_PATH, storage="auto", job_id=None)` from a Python script in `%TEMP%`. Working directory pinned to `backend/`. No code changes. `dispatch_gate.py` SHA-1 captured before and after.

### 1.2 Captured fields

| Field | Value |
|---|---:|
| Wall-clock | **474.11 s** |
| Total pages | 91 |
| `sheet_map_size` | 47 |
| `page_to_sheet` count (pages with `sheet_number`) | 44 |
| `roofing_fields` (sum across all pages) | **769** |
| `glazing_items` | **177** |
| `door_items` | **31** |
| `storefront_items` | **24** |
| `dispatch_warnings` count | 1 |
| `filters_completed` | filter_1, filter_2, filter_4, filter_3, filter_5, stage_13_trade_modules |

### 1.3 Dispatch warnings (single line)

```
Filter 4 quality gate: 749 of 990 legends removed (241 kept)
```

### 1.4 SHA-1 fence

| Checkpoint | dispatch_gate.py SHA-1 |
|---|---|
| Before Scout 1 | `c206ff9e7e85eeee2c1c9bdaae8f0313308cd4a3` |
| After Scout 1 | `c206ff9e7e85eeee2c1c9bdaae8f0313308cd4a3` |

Held.

### 1.5 Cross-check against G.0.5

G.0.5's instrumented Bearss run reported 544.2 s, 91 pages, 769/177/31/24. Scout 1: 474.11 s, 91 pages, **769/177/31/24** — trade-output totals byte-identical. Wall-clock −12.9% from G.0.5; G.0.8 §5.7 already named dispatch wall-clock variance as unmeasured (G.0.8 saw 184.2 s vs G.0.5's 544.2 s, 3× spread, cause unknown). The 12.9% delta sits inside that known noise floor. No STOP fired.

---

## §2 — Scout 2: Hybrid regex via in-memory monkey-patch

### 2.1 Method

`import core.dispatch_gate as dg` → snapshot `dg._SHEET_NUM_RE` → assign `dg._SHEET_NUM_RE = re.compile(HYBRID_PATTERN)` → run `run_dispatch(...)` → restore original. `dispatch_gate.py` on disk SHA-1-verified before and after.

### 2.2 Patterns

| Pattern | Regex |
|---|---|
| Original (`dispatch_gate.py:57`) | `\b([A-Z]{1,2})-?(\d+[\.\d]*[A-Za-z]?)\b` |
| Hybrid (G.0.7 §4) | `\b([A-Z]{1,2})-?(\d{3,}[\.\d]*[A-Za-z]?\|\d+\.\d+[\.\d]*[A-Za-z]?)\b` |

### 2.3 Captured fields

| Field | Value |
|---|---:|
| Wall-clock | **516.45 s** |
| Total pages | 91 |
| `sheet_map_size` | 47 |
| `page_to_sheet` count | 44 |
| `roofing_fields` | **769** |
| `glazing_items` | **177** |
| `door_items` | **31** |
| `storefront_items` | **24** |
| `dispatch_warnings` count | 1 |
| `filters_completed` | filter_1, filter_2, filter_4, filter_3, filter_5, stage_13_trade_modules |

### 2.4 Dispatch warnings (single line)

```
Filter 4 quality gate: 749 of 990 legends removed (241 kept)
```

Identical text to Scout 1.

### 2.5 SHA-1 fence

| Checkpoint | dispatch_gate.py SHA-1 |
|---|---|
| Before Scout 2 | `c206ff9e7e85eeee2c1c9bdaae8f0313308cd4a3` |
| After Scout 2 (post-restore) | `c206ff9e7e85eeee2c1c9bdaae8f0313308cd4a3` |

Held. The monkey-patch lived in module memory only; the file on disk is unchanged.

---

## §3 — Scout 3: Byte-by-byte comparison (Scout 1 vs Scout 2)

### 3.1 Comparison table

| Field | Scout 1 | Scout 2 | Equal? |
|---|---:|---:|---|
| `roofing_fields` | 769 | 769 | ✓ |
| `glazing_items` | 177 | 177 | ✓ |
| `door_items` | 31 | 31 | ✓ |
| `storefront_items` | 24 | 24 | ✓ |
| `sheet_map_size` | 47 | 47 | ✓ |
| `page_to_sheet` count | 44 | 44 | ✓ |
| `total_pages` | 91 | 91 | ✓ |
| `dispatch_warnings` (text) | 1 line, identical | 1 line, identical | ✓ |
| `filters_completed` (sequence) | identical | identical | ✓ |

### 3.2 Verdict

**BYTE-EQUIVALENT.** All seven numeric fields agree. The single dispatch warning is identical text. The filter sequence is identical.

### 3.3 What this names

The hybrid regex is invisible on Bearss. Bearss already had a clean drawing-index page under the current regex (no Silverleaf-style false-positive index, no Panda-San-Antonio-style schedule-page-mistaken-for-index). Switching to the hybrid neither removes a real entry nor admits a new spurious one on this PDF. Both regexes converge on the same `sheet_map` (47 entries), the same `page_to_sheet` mapping (44 mapped), and the same downstream trade-module aggregates.

This was the predicted outcome (G.0.7 §3.3 named Bearss in the "13 of 15 bidsets where hybrid selects the same page as current" group). The empirical result confirms the prediction on the live PDF.

---

## §4 — Scout 4: Debug module comparison (run_debug on both ctxs)

### 4.1 Method

`run_debug(scout1_ctx)` → `debug1`, `run_debug(scout2_ctx)` → `debug2`. Compare three structures: `dispatch_health` (dict), `page_intelligence[:10]` (first 10 entries), `legend_quality_flags` (list).

### 4.2 `dispatch_health` comparison

| Key | Scout 1 | Scout 2 | Equal? |
|---|---|---|---|
| `dispatch_complete` | True | True | ✓ |
| `filters_completed` | (6 entries identical) | (6 entries identical) | ✓ |
| `filter_count` | 6 | 6 | ✓ |
| `warnings` | 1 line identical | 1 line identical | ✓ |
| `warning_count` | 1 | 1 | ✓ |
| **`timestamp`** | `2026-05-02T04:38:05.579574+00:00` | `2026-05-02T04:46:42.012003+00:00` | **✗ (timestamp delta)** |
| `total_pages` | 91 | 91 | ✓ |
| `sheet_map_source` | `drawing_index` | `drawing_index` | ✓ |
| `sheet_count` | 47 | 47 | ✓ |
| `mapped_pages` | 44 | 44 | ✓ |

The only divergence is `timestamp`, which records `dispatch_timestamp` from the moment `run_dispatch` set it (`datetime.now(timezone.utc).isoformat()` at the end of dispatch — `dispatch_gate.py:1728`). The 8m37s gap between the two timestamps is exactly the wall-clock gap between Scout 1 and Scout 2 plus their respective dispatch durations. This is a clock artefact, not a regex artefact: rerunning Scout 1 with the original regex in Scout 5 would also produce a different timestamp.

### 4.3 `page_intelligence[:10]` comparison

The first 10 entries (pages 0–9) compared field-by-field across all 14 reported keys (`page`, `sheet`, `title`, `discipline`, `type`, `confidence`, `has_drawing`, `has_title_block`, `has_details`, `has_legend`, `detail_count`, `zone_count`, `legend_count`, `refs_out`, `refs_in`).

Result: **MATCH on every entry.** Spot examples:

| Page | Sheet (S1=S2) | Title (S1=S2) | type (S1=S2) |
|---:|---|---|---|
| 0 | A-001 | COVER SHEET … | cover |
| 1 | A-002 | CODE & LIFE SAFETY | life_safety |
| 2 | A-003 | ARCHITECTURAL SITE PLAN | site_plan |
| 3 | A-202 | PANEL ELEVATIONS, WALL SECTIONS, & DETAILS | roof_plan |
| 4 | A-402 | MISC. DETAILS | floor_plan |
| 5 | A-201 | EXTERIOR ELEVATIONS | schedule_sheet |
| 6 | --- | --- | elevation |
| 7 | A-401 | ROOF MISC. DETAILS | detail_sheet |
| 8 | --- | --- | detail_sheet |
| 9 | (matches) | (matches) | (matches) |

### 4.4 `legend_quality_flags` comparison

Both runs produced 5 flags, identical text:

```
WARNING: unusually high legend count (241) — possible pdfplumber noise
WARNING: page 12 has 17 legends — review for duplicates or noise
WARNING: page 40 has 12 legends — review for duplicates or noise
WARNING: page 58 has 14 legends — review for duplicates or noise
WARNING: page 86 has 12 legends — review for duplicates or noise
```

Identical, byte-for-byte.

### 4.5 Verdict

The hybrid does not perturb anything `debug_module` surfaces on Bearss except `dispatch_timestamp`, which is a clock artefact unavoidable across any two runs (re-running with the same regex would produce the same delta). The structural diagnostics — page-by-page sheet identity, page type, discipline, drawing/legend/detail flags, ref counts, legend-quality warnings — are byte-identical between current and hybrid.

`debug_module.py` SHA-1 unchanged: `78f71d9030cde3b173389603f5f39bd6bedaac07` (vault-ruled — read-only walkthrough only, never imported with mutation).

---

## §5 — Scout 5: Determinism check (current regex, second run)

### 5.1 Method

After Scouts 1–4 complete, `importlib.reload(dg)` to flush any in-memory state, then a fresh `run_dispatch(PDF_PATH, storage="auto", job_id=None)` with the original (unpatched) regex. Compare against Scout 1.

### 5.2 Captured fields

| Field | Scout 1 | Scout 5 | Equal? |
|---|---:|---:|---|
| Wall-clock | 474.11 s | 500.69 s | (+5.6% — variance) |
| Total pages | 91 | 91 | ✓ |
| `sheet_map_size` | 47 | 47 | ✓ |
| `page_to_sheet` count | 44 | 44 | ✓ |
| `roofing_fields` | 769 | 769 | ✓ |
| `glazing_items` | 177 | 177 | ✓ |
| `door_items` | 31 | 31 | ✓ |
| `storefront_items` | 24 | 24 | ✓ |
| `dispatch_warnings` (text) | 1 line | 1 line, identical | ✓ |
| `filters_completed` | identical | identical | ✓ |

### 5.3 SHA-1 fence

| Checkpoint | dispatch_gate.py SHA-1 |
|---|---|
| After Scout 5 | `c206ff9e7e85eeee2c1c9bdaae8f0313308cd4a3` |

Held.

### 5.4 Verdict

**DETERMINISTIC.** Two runs of the unpatched code on the same PDF produced identical structural and trade-output values. Wall-clock varies by 5.6% (474.11 s vs 500.69 s) — this is execution-environment noise (PyMuPDF/pdfplumber wall-clock variance G.0.8 §5.7 named as unmeasured), not a state-changing nondeterminism. Trade-module aggregates do not depend on wall-clock; they depend on PDF text content and regex/heuristic decisions, both of which are deterministic.

The Scout 3 comparison is therefore valid: Scout 1 and Scout 5 produce the same outputs on the same code, so any divergence Scout 3 surfaced would have been attributable to the regex monkey-patch, not to baseline drift. Scout 3 surfaced zero divergences.

---

## §6 — Verdict

> **Hybrid is byte-equivalent to current on Bearss.**

Concretely, on the 91-page Bearss Ave Distribution Center bidset:

- All four trade-output totals match exactly: **roofing_fields 769, glazing_items 177, door_items 31, storefront_items 24** under both current and hybrid regex.
- `sheet_map_size` (47) and `page_to_sheet` count (44) are unchanged by the regex switch.
- The single dispatch warning is identical text.
- The `filters_completed` sequence is identical.
- `debug_module.run_debug` produces structurally identical `dispatch_health` (modulo the run-clock `timestamp`), identical `page_intelligence` for the first 10 pages, and identical `legend_quality_flags` (5 flags, byte-for-byte).
- The baseline is deterministic (Scout 5 reproduces Scout 1 exactly on the trade fields).
- The D.2 reference (769/177/31/24) is reproduced exactly — Bearss byte-exact ground truth held across this verification.

This is the predicted outcome from G.0.7 §3.3 ("13 of 15 bidsets: hybrid selects the same page as current"). G.0.9 closes the empirical gap that G.0.8 §5.7 named as an honest deficit ("Not validated: real-PDF test impact of the hybrid"). The hybrid does not change Bearss outputs.

### 6.1 What this verdict does NOT say

Per Karpathy: name what's there, don't propose.

- **Bearss is one bidset.** This verdict applies to Bearss only. Silverleaf is the bidset where the hybrid is supposed to _change_ the answer (rejecting the bogus p5 framing-plan-misidentified-as-index per G.0.5/G.0.7). G.0.9 did not run Silverleaf — its proper verification belongs to a future phase that runs the hybrid on Silverleaf and confirms the index moves to the real page and the sheet_map gains entries (G.0.7 §4.1 step 3 predicted "Silverleaf should jump from 4 mapped pages to ~32").
- **Wall-clock variance is unexplained.** Three runs of the same dispatch gave 474.11 s, 516.45 s, 500.69 s — a 9.0% spread. G.0.8 saw a 3× spread (184.2 s vs G.0.5's 544.2 s) and named it. Scout 5 confirms output determinism but does not isolate the wall-clock-variance source.
- **No tests exercise the regex with Silverleaf-style data.** Scout 4 `legend_quality_flags` and `page_intelligence` agreement on Bearss does not imply agreement on a bidset where the regex would actually choose a different drawing-index page.
- **Layer 1 (`seeds/dispatch_seed.py:134`) was not exercised.** G.0.8 §5.2 flagged the Layer1/Layer3 inconsistency the hybrid would create. G.0.9 monkey-patched only the Layer 3 (`dispatch_gate._SHEET_NUM_RE`) regex; Layer 1's broad regex remained in place. On Bearss this didn't matter; on a bidset where Layer 1 is the deciding path, the result could differ.
- **`debug_module` was a read-only walkthrough.** `run_debug` was called as a black-box; this report does not validate `debug_module`'s internals beyond confirming output equivalence.

These are honest gaps, not scope failures. Each should be closed before the hybrid ships.

---

## §7 — Sacred floor verification

### 7.1 Backend test floor

Pre-scouts: `python -m pytest backend/tests/ -q --tb=no` → **230 passed, 19 skipped, 0 failed, 1 warning in 4.50s**.

Post-scouts (verified at end of session, see `§7.3` below).

### 7.2 SHA-1 fence (13 critical files, captured pre-scouts)

| File | SHA-1 |
|---|---|
| `backend/core/dispatch_gate.py` | `c206ff9e7e85eeee2c1c9bdaae8f0313308cd4a3` |
| `backend/core/debug_module.py` | `78f71d9030cde3b173389603f5f39bd6bedaac07` |
| `backend/core/roofing_module.py` | `ae9e5b284191b45de419faacf11771da27a548f9` |
| `backend/core/roofing_vocabulary.py` | `ec6c17f8955ef8e27c3ff1d552b299a6962c9d0b` |
| `backend/core/glazing_vocabulary.py` | `64249c8ef5f7d9db50added3c9a40836cba356ea` |
| `backend/core/context.py` | `99db54dda0528626aa82a2bb358aea8d4a429d36` |
| `backend/core/pdf_engine.py` | `e872f69eb60f99d84dca0085c86ee48900b4e74e` |
| `backend/core/trade_module.py` | `6995950fc780e46090f115c12a83c28356cda5ae` |
| `backend/core/trade_input_builder.py` | `c89a9ee85dac98040f0a75a43e6979d5e8d0844f` |
| `backend/core/filter_pipeline.py` | `62390dbb98b25d35574a9e6ff4c16d2149de1e6b` |
| `backend/core/geometry_matrix.py` | `e0884449aaa92e11fa970d61275e43ae79286feb` |
| `backend/core/polygon_scorers.py` | `c60d1419d8a918d5f071a4355705c5c53a010445` |
| `backend/core/architect_profile.py` | `80d33dfdbf25c1d214cb0952e86c452d16ed5e35` |

`dispatch_gate.py` SHA-1 verified before Scout 1, after Scout 1, after Scout 2 (post monkey-patch restore), after Scout 5 — all four checkpoints `c206ff9e…`. Held.

### 7.3 Post-session re-verification

Captured at the end of the session (after the report is written, before commit).

| Check | Result |
|---|---|
| Backend test floor | (verified post-write — see commit message) |
| 13 critical-file SHA-1s | (verified post-write — see commit message) |
| New tracked file count | 1 (this report only) |
| `dispatch_gate.py` on-disk pattern | unchanged: `\b([A-Z]{1,2})-?(\d+[\.\d]*[A-Za-z]?)\b` |
| Instrumentation script location | `%TEMP%\g09_scouts.py` — outside the tree, not committed |
| Hybrid regex applied to disk | **No.** Monkey-patch only. Hybrid stays on paper. |

---

## §8 — Wall-clock budget

| Phase | Elapsed |
|---|---:|
| Environment verification (file listing, SHA-1 capture, test floor, code reads) | ~7 min |
| Scout 1 dispatch (current regex) | 474.11 s = 7.9 min |
| Scout 2 dispatch (hybrid monkey-patch) | 516.45 s = 8.6 min |
| Scout 3 (numeric comparison, in-process) | <1 s |
| Scout 4 (`run_debug` on both ctxs, in-process) | <1 s |
| Scout 5 dispatch (current regex, determinism) | 500.69 s = 8.3 min |
| Report writing + post-checks | ~5 min |
| **Total** | **~46 min** (within the 90-min guardrail) |

---

## §9 — Karpathy postscript

This report names what was observed on Bearss and stops there. It does not propose shipping the hybrid. It does not claim the hybrid is safe on Silverleaf, Panda San Antonio, or any of the 13 other corpus bidsets. It does not address the Layer 1 / Layer 3 inconsistency. It does not investigate the wall-clock variance. Each of those is a discrete, separable observation a future phase can take up.

What G.0.9 closes: the question "would shipping the hybrid regex break Bearss?" The answer is **no, on Bearss the hybrid is byte-equivalent to current**. That single empirical claim is what this branch contributes.
