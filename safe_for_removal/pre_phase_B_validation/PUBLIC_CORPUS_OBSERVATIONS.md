# Public-Corpus Observation Sweep

**Date:** 2026-04-26
**Inputs:** 4 non-STACK bidsets at `C:\huck stage 2\not_stack-bidsets\` (outside the working tree)
**Pipeline:** v0.2 dispatch gate, ported verbatim from TracePoint, unmodified for this sweep
**Sweep script:** `backend/scripts/run_dispatch_on_public_corpus.py`
**Outputs:** `backend/test_fixtures/public_corpus_outputs/<bidset_id>.json` (4 files; gitignored)

This document is observation only. It records what v0.2 did on this sample.
It does NOT establish correct behavior, propose fixes, or recalibrate any
threshold. The STACK validation that shipped v0.2 is in
`backend/V0_2_VALIDATION.md` and is not affected by anything in this file.

---

## Source

The 4 PDFs were downloaded by Daniel from public web archives. They were
selected to introduce non-STACK PDF producers into a v0.2 observation
corpus. None of them came through STACK Construction Technologies — the
producer-stamp shifts that to Bluebeam (3 of 4) or Adobe Acrobat / AutoCAD
Architecture (1 of 4).

The PDFs themselves are NOT in the repository working tree (verified:
`git ls-files | grep .pdf` returns nothing). They live on Daniel's machine
at `C:\huck stage 2\not_stack-bidsets\`. The sweep reads them from that
fixed path.

Producer/architect/owner attribution beyond the PDF metadata was not
attempted. Each bidset's identity is inferred from filename only.

---

## Per-bidset measurements

| bidset_id | pages | runtime (s) | dispatch_complete | filters_completed match | sheet_map_source | sheet_map count | detected_system | system_confidence | scope_pages count | warning count | concerning warnings |
|---|---:|---:|:-:|:-:|---|---:|---|---:|---:|---:|---|
| suwannee-county-school-board-suwannee-high-school-courtyard-renovation | 31 | 11.7 | ✓ | ✓ | title_blocks | 20 | None | n/a | 0 | 1 | none |
| holabird-academy-elementary-middle-school | 96 | 221.3 | ✓ | ✓ | drawing_index | 295 | None | n/a | 0 | 2 | "LOW RESOLUTION: 8% cross-references resolved" (informational) |
| sanibel-fire-and-rescue-station-172 | 90 | 186.9 | ✓ | ✓ | drawing_index | 172 | None | n/a | 0 | 1 | none |
| uccs-cybersecurity-and-space-ecosystem-expansion | 133 | 147.9 | ✓ | ✓ | drawing_index | 129 | None | n/a | 0 | 1 | none |

Notes on the column "filters_completed match": all 4 had exactly
`["filter_1", "filter_2", "filter_4", "filter_3", "filter_5"]` — the
TracePoint-design ordering (Filter 4 before Filter 3) was preserved.

Notes on the column "concerning warnings": no bidset surfaced
`scope scanner failed` or any traceback-shaped warning. The
`Filter 4 quality gate` warning fired on every bidset (same as STACK)
and is informational, not error. Holabird's `LOW RESOLUTION` warning is
a documented Filter 3 leak-check signal and is informational; it does
not indicate dispatch failure.

### Producer / file metadata captured pre-sweep

| bidset_id | size (MB) | producer (PDF metadata) | creator (PDF metadata) |
|---|---:|---|---|
| suwannee-county-school-board-suwannee-high-school-courtyard-renovation | 9.0 | Adobe Acrobat 9.4.1 | AutoCAD Architecture 2012 (LMS Tech) |
| holabird-academy-elementary-middle-school | 56.3 | Bluebeam Brewery 5.0 | Bluebeam Stapler 2016.5.2 |
| sanibel-fire-and-rescue-station-172 | 55.2 | Bluebeam Brewery 5.0 | Bluebeam Stapler 21.0.50.11 |
| uccs-cybersecurity-and-space-ecosystem-expansion | 43.0 | Bluebeam PDF Library 20 | Bluebeam Revu x64 |

---

## Aggregate observations

### Detection rate

- Bidsets with non-null `project_scope.detected_system`: **0 / 4**
- Bidsets with empty `project_scope.scope_pages`: **4 / 4**
- Bidsets with `dispatch_complete: true`: **4 / 4**
- Bidsets that crashed during dispatch: **0 / 4**

### `sheet_map_source` distribution

- `drawing_index`: 3 / 4 (all 3 Bluebeam bidsets)
- `title_blocks`: 1 / 4 (the Adobe Acrobat / AutoCAD Architecture bidset)

### Max-duplicate-sheet check (the v0.2 Symptom-4 concern)

| bidset_id | `max(Counter(page_to_sheet.values()))` | most-common (count) |
|---|---:|---|
| suwannee-county-school-board-suwannee-high-school-courtyard-renovation | 1 | P-1.0 (1) |
| holabird-academy-elementary-middle-school | 1 | TS-2H (1) |
| sanibel-fire-and-rescue-station-172 | 1 | G000 (1) |
| uccs-cybersecurity-and-space-ecosystem-expansion | 1 | NV5 (1) |

All 4 bidsets had max-duplicate-sheet count of 1 — no page-to-sheet
propagation occurred on any of them. The Hampshire-style "N19A × 7"
pattern (STACK corpus, v0.2 Symptom 4 FAIL) did not reproduce here.

### Cross-reference resolution rate

| bidset_id | cross-refs total | resolved | rate |
|---|---:|---:|---:|
| suwannee-county-school-board-suwannee-high-school-courtyard-renovation | 13 | 0 | 0% |
| holabird-academy-elementary-middle-school | 13 | 1 | 8% |
| sanibel-fire-and-rescue-station-172 | 24 | 16 | 67% |
| uccs-cybersecurity-and-space-ecosystem-expansion | 51 | 26 | 51% |

Range across the 4: 0% to 67%. The 8% Holabird rate triggered the
`LOW RESOLUTION` informational warning. The 0% Suwannee rate did not
trigger that warning because the Filter 3 leak-check requires both
`resolved_count` and `unresolved_count` to be non-zero before evaluating
the rate.

### Page-type histograms (per bidset, top 6)

| bidset_id | top page_types |
|---|---|
| suwannee-county-school-board-suwannee-high-school-courtyard-renovation | unknown=11, detail_sheet=9, floor_plan=4, symbol_legend=3, elevation=2, framing_plan=1 |
| holabird-academy-elementary-middle-school | elevation=26, detail_sheet=16, section=15, floor_plan=10, schedule_sheet=10, ceiling_plan=7 |
| sanibel-fire-and-rescue-station-172 | detail_sheet=26, elevation=12, unknown=11, section=11, floor_plan=9, roof_plan=5 |
| uccs-cybersecurity-and-space-ecosystem-expansion | detail_sheet=22, schedule_sheet=22, floor_plan=21, ceiling_plan=19, elevation=14, mep_plan=11 |

### `roof_plan` count (informational)

| bidset_id | roof_plan total | roof_plan with conf ≥ 0.9 |
|---|---:|---:|
| suwannee-county-school-board-suwannee-high-school-courtyard-renovation | 0 | 0 |
| holabird-academy-elementary-middle-school | 0 | 0 |
| sanibel-fire-and-rescue-station-172 | 5 | 0 |
| uccs-cybersecurity-and-space-ecosystem-expansion | 0 | 0 |

Across the 4: 5 roof_plan pages total, 0 with explicit (title-block)
confidence. The single Sanibel cluster matched the keyword `ROOF PLAN`
in body text, not in title blocks.

### New failure modes (i.e., not seen on STACK)

None observed. The 3 documented STACK-corpus failure modes
(scope-scanner empty-result, Hampshire `N19A` propagation, Wendy's
runtime outlier) either reproduced (empty scope, on all 4) or did not
manifest (no propagation, no abnormal runtimes). No previously-unseen
crash, traceback, or warning shape arose.

### New Discovered Issues filed

None. No D-ticket from this sweep. Per Daniel's brief: D-tickets fire
only on gate crashes or behavior contradicting the verbatim-port
assumption. Both criteria came back clean.

---

## Side-by-side with STACK (no judgment about which is correct)

The STACK aggregates below come from `backend/V0_2_VALIDATION.md` and
`backend/test_fixtures/v0_2_validation_summary.json`. They are recorded
here for comparison only. Neither side is being declared "correct."

| Aggregate | STACK (15 bidsets) | Public corpus (4 bidsets) |
|---|---|---|
| Bidsets with `detected_system` non-null | 1 / 15 (Taco Bell, "tpo", conf 0.95) | 0 / 4 |
| Bidsets with empty `scope_pages` | 14 / 15 | 4 / 4 |
| `sheet_map_source = drawing_index` | 13 / 15 | 3 / 4 |
| `sheet_map_source = title_blocks` | 2 / 15 (auto-zone-vero, hampshire) | 1 / 4 (suwannee) |
| Bidsets with `max_dup > 2` outside Bearss | 1 / 15 (Hampshire, "N19A" × 7) | 0 / 4 |
| `dispatch_complete: true` | 15 / 15 | 4 / 4 |
| Crashes during dispatch | 0 / 15 | 0 / 4 |
| Filter-order match `[1, 2, 4, 3, 5]` | 15 / 15 | 4 / 4 |
| Runtime outlier (≥ 5× median per page) | 1 / 15 (Wendy's, 9 min for 64p) | 0 / 4 |

Per Daniel's brief: this side-by-side is a comparison, not a calibration
input. Sample sizes and ground-truth status are not equivalent on the
two sides.

---

## Explicit non-conclusions

These observations describe v0.2's behavior on a 4-bidset non-STACK
sample. They do not establish what correct behavior should be — that
requires ground-truth review of each plan set, which has not happened.
No tuning decisions, threshold adjustments, or fix paths are proposed
based on this data. Conclusions about gate calibration require both
(a) ground-truth validation and (b) a corpus large enough to distinguish
gate behavior from sample artifacts. This 4-bidset sweep meets neither
criterion.
