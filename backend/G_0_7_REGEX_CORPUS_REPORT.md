# G.0.7 Regex Corpus Validation Report

**Date:** 2026-05-01
**Phase:** G.0.7 (read-only corpus regex experiment)
**Branch:** `phase2-v0.3-G0-7-regex-corpus` from `2514457` (G.0.6 head)
**Executed by:** Claude Code (Developer session)
**Deliverable shape:** Single markdown report, one corpus table + verdict. Zero code changes. Zero tracked files modified. Sacred floors held (230/19/0).

**What this report does:** Opens all 15 bidsets in `C:\huck stage 2\full bid sets\`, extracts text from pages 0-9 via PyMuPDF, and applies both the current `_SHEET_NUM_RE` regex and Alt C from G.0.6 using the parser's exact `.match()` + dash-normalization logic. Reports which page each regex would select as the drawing index (≥10-unique-token threshold). When divergent, designs and tests a hybrid that rejects Silverleaf's bogus index AND preserves all real indexes.

**What this report does NOT do:** No code changes. No fixes shipped. No dispatches run. The regex change still lives only on paper.

---

## §1 — Corpus Sweep Results

### 1.1 Methodology

For each of the 15 PDFs in `C:\huck stage 2\full bid sets\`:
1. Open with `fitz.open(path)`, read pages 0 through `min(page_count, 10)-1`
2. For each page: split into lines, normalize each line per `dispatch_gate.py:210` (`re.sub(r'([A-Z])\s*-\s*(\d)', r'\1-\2', line.strip())`), apply `regex.match(line_norm)`
3. Collect unique tokens per page; first page hitting ≥10 unique tokens is the parser's index pick (matches `_find_drawing_index_page()` exactly)

Three regexes evaluated:

| Name | Pattern |
|------|---------|
| Current | `\b([A-Z]{1,2})-?(\d+[\.\d]*[A-Za-z]?)\b` |
| Alt C (from G.0.6) | `\b([A-Z]{1,2})-?(\d{3,}[\.\d]*[A-Za-z]?)\b` |
| Hybrid (proposed below) | `\b([A-Z]{1,2})-?(\d{3,}[\.\d]*[A-Za-z]?\|\d+\.\d+[\.\d]*[A-Za-z]?)\b` |

### 1.2 Corpus Table

Notation: `pN/K` = page N, K unique tokens. `none/0` = no page hit threshold. `*` = differs from current.

| # | Bidset | Current | Alt C | Hybrid |
|---|--------|---------|-------|--------|
| 1 | Auto Zone #10891 - Jacksonville | p0/32 | **none/0*** | p0/22 |
| 2 | Auto Zone Vero Beach, FL | none/0 | none/0 | none/0 |
| 3 | B2607 AEA Silverleaf | **p5/10 (BOGUS)** | none/0* | none/0* |
| 4 | Bearss Ave Distribution Center | p0/47 | p0/47 | p0/47 |
| 5 | Chewy Vet Care - London Square | p0/89 | p0/89 | p0/89 |
| 6 | Chipotle - Tarpon Springs | p0/39 | p0/39 | p0/39 |
| 7 | Hampshire Self Storage | none/0 | none/0 | none/0 |
| 8 | Panda Express - Naples | p0/87 | p0/79 | p0/80 |
| 9 | Panda Express - San Antonio | p1/34 | p3/18* | **p3/18*** |
| 10 | Panda Express Bradenton | p0/79 | p0/73 | p0/74 |
| 11 | Panda Express Hialeah Gardens | p0/20 | **none/0*** | p0/19 |
| 12 | Shoppes at Avalon - Spring Hill | p0/31 | p0/30 | p0/30 |
| 13 | Taco Bell - Weeki Wachee | p0/92 | **p1/10*** | p0/83 |
| 14 | Vine Street Retail Center | p2/44 | **none/0*** | p2/42 |
| 15 | Wendy's - Fort Myers | p6/11 | p6/10 | p6/10 |

### 1.3 Divergence Summary

**Alt C divergence (vs. current):** 6 of 15 bidsets diverge.

- **1 intentional fix:** Silverleaf p5 → none (the bug fix from G.0.6)
- **4 false rejections:** Auto Zone #10891, Hialeah Gardens, Vine Street → none. Taco Bell → wrong page (p1 instead of p0).
- **1 latent improvement:** Panda San Antonio → p3 (cleaner index than current's p1)

**Hybrid divergence (vs. current):** 2 of 15 bidsets diverge.

- **1 intentional fix:** Silverleaf p5 → none (bug fix preserved)
- **1 latent improvement:** Panda San Antonio → p3 (skips current's noisy schedule page p1)

The other 13 bidsets: hybrid selects the same page as current.

---

## §2 — Why Alt C Broke

### 2.1 Failure mode — sub-3-digit decimal sheet numbers

Many smaller plan sets (residential, retail, restaurant) use the `A-N.N` numbering convention rather than NCS's `A-NNN`. Alt C's `\d{3,}` floor rejects these.

**Concrete examples from the corpus:**

| Bidset | Sample tokens (rejected by Alt C) | Format |
|--------|-----------------------------------|--------|
| Auto Zone #10891 | `A1.0`, `A2.0`, `A3.0`, `D1.0`, `T1.0`, `AS1.0` | Discipline + single-digit-dot-digit |
| Hialeah Gardens | `C01.0`, `C01.1`, `C03.0`, `C03.1`, ... `C06.1` | Discipline + 2-digit-dot-digit |
| Taco Bell | `A0.1`-`A0.3`, `A1.0`-`A1.5`, `A2.0`-`A2.1`, `A3.0`-`A3.1`, `A4.0`-`A4.4`, `A5.0`-`A5.1` | Architectural decimal series |
| Vine Street | `A-0.1`, `A-1.0`-`A-1.4`, `A-2.0`-`A-2.4`, `A-3.0`, `A-4.0`, `E-0.0`, `E-1.0`, `E-2.0` | Dashed sub-3-digit decimal |

All four bidsets contain real, well-formed drawing index pages with 20-92 entries. Alt C rejects them because the digit count before the decimal is 1 or 2.

### 2.2 The discriminator that survives

Looking at all rejected-by-Alt-C tokens: **every single one contains a decimal point**. Looking at all Silverleaf p5 false positives (`HD1`, `HD8`, `L1`, `L2`, `L3`, `MW-1`, `SW-3S`, `WD1`): **none of them contain a decimal point**, and all have 1-digit numbers.

The clean separator: a token is a real sheet number if it has **either** ≥3 digits **or** a decimal point. Component marks have neither.

---

## §3 — Hybrid Regex

### 3.1 Pattern

```python
HYBRID = re.compile(r'\b([A-Z]{1,2})-?(\d{3,}[\.\d]*[A-Za-z]?|\d+\.\d+[\.\d]*[A-Za-z]?)\b')
```

The number group is now an alternation: either ≥3 digits (covers `A-101`, `S502`, `GC-6100`) or a decimal pattern (covers `A-1.3`, `C01.0`, `E-2.1`).

### 3.2 Control points

| Test case | Required | Current | Alt C | Hybrid |
|-----------|----------|---------|-------|--------|
| Silverleaf p5 (must FAIL — bogus framing-plan index) | <10 unique | **10** | 2 | **2** |
| Bearss p0 (must PASS — real 47-sheet index) | ≥10 unique | 47 | 47 | **47** |

Hybrid yields exactly `{S101, S502}` on Silverleaf p5 — both real sheet numbers buried in the framing plan as cross-references, but only 2 of them, well below threshold.

### 3.3 Hybrid corpus performance

- **13 of 15 bidsets:** hybrid selects the same page as current (token count slightly lower because component marks no longer match — this is the goal)
- **Silverleaf:** hybrid correctly rejects the bogus p5 index (the fix)
- **Panda San Antonio:** hybrid picks p3 instead of current's p1. Examining the tokens:
  - Current p1 (34 entries): `A-101`, `A-403`, `A45`, `BC88L`, `C02`, `CO2`, `CS-4E`, `D278`, `D2B`, `E5`, `E7`, `F1D`, `GC-6100`, `LV340C`, `M1`, ... — equipment model numbers and product schedules, not sheet numbers
  - Hybrid p3 (18 entries): `A-103`, `A-200`, `A-201`, `A-401`, `A-402`, `A-403`, `A-404`, `A-500`-`A-503`, `P200C`, `T108`, `T111`, `T119`, `T125`, `T200`, `T402` — clean discipline-prefixed sheet numbers

  This is a latent **improvement**: current was misidentifying a SCHEDULE page (p1) as the drawing index for the same reason it misidentified Silverleaf p5 — short alphanumeric tokens passing the loose regex. The hybrid skips it and finds the real index.

### 3.4 No false negatives detected in corpus

For every bidset where current selects a page:
- Hybrid selects the same page (13 cases), or
- Hybrid selects a better page with cleaner tokens (1 case: Panda San Antonio), or
- Hybrid correctly rejects (1 case: Silverleaf — the intended bug fix)

For every bidset where current selects no page (Auto Zone Vero Beach, Hampshire Self Storage):
- Hybrid also selects no page

No bidset where current correctly identifies a real index gets rejected by the hybrid.

### 3.5 Edge cases retained by the hybrid

| Token | Source | Branch matched | Retained? |
|-------|--------|----------------|-----------|
| `A-101` (Bearss) | NCS standard | `\d{3,}` | ✓ |
| `S502` (Silverleaf p5 cross-ref) | 3-digit | `\d{3,}` | ✓ (only 2 such, doesn't hit threshold) |
| `A-1.3` (Vine Street) | sub-3-digit decimal | `\d+\.\d+` | ✓ |
| `C01.0` (Hialeah) | 2-digit + decimal | `\d+\.\d+` | ✓ |
| `E-0.0` (Vine Street) | zero-padded decimal | `\d+\.\d+` | ✓ |
| `AR96268` (Auto Zone) | 5-digit, 2-letter prefix | `\d{3,}` | ✓ |
| `FL21961.2` (Auto Zone) | 5-digit + decimal | `\d{3,}` (greedy) | ✓ |
| `HD1` (Silverleaf p5) | 1-digit, no decimal | neither | rejected ✓ |
| `MW-1`, `SW-3S`, `WD1` | 1-digit, no decimal | neither | rejected ✓ |
| `L1`, `L2`, `L3` | 1-digit, no decimal | neither | rejected ✓ |

---

## §4 — Verdict

> **Alt C breaks on 4 bidsets — Auto Zone #10891, Hialeah Gardens, Taco Bell, Vine Street — that use sub-3-digit `A-N.N` decimal sheet numbering. The hybrid `\b([A-Z]{1,2})-?(\d{3,}[\.\d]*[A-Za-z]?\|\d+\.\d+[\.\d]*[A-Za-z]?)\b` is the actual answer.**

The hybrid:
1. **Rejects Silverleaf's bogus p5 index** (control point: 10 → 2 unique, below threshold) — fixing G.0.5 Bug 1
2. **Preserves the index page selection on all 14 other corpus bidsets** that have a discoverable index
3. **Improves on current for Panda San Antonio** by skipping a noisy schedule page and finding the real index on p3

The fix is no longer one character (`\d+` → `\d{3,}`) but a small disjunction. It targets the exact failure mode of structural component marks (1-digit, no decimal) while accepting both NCS-standard `A-NNN` and the common sub-3-digit `A-N.N` convention.

### 4.1 Recommended implementation steps (for a future phase)

1. Apply the hybrid pattern as `_SHEET_NUM_RE` in `dispatch_gate.py:57` (single-line change)
2. Run full backend test suite — expect 230/19/0 to hold (no test exercises the regex directly with Silverleaf-style data)
3. Re-run `run_dispatch` on the 15 bidsets and compare `sheet_map_size` and `page_to_sheet` size against the v0.3 baseline — Silverleaf should jump from 4 mapped pages to ~32, with no other bidset's mapping shrinking
4. Spot-check Panda San Antonio's drawing index — confirm p3 is genuinely the index (not a regression)

### 4.2 Residual risk

- **Bidsets outside the corpus** may use formats not represented in these 15 (e.g., `A1` single-digit no-dot, used by some shop drawings). These would be rejected by the hybrid. Mitigation: a real index would still need ≥10 such entries on one page, which is unlikely.
- **The fallback path** (`run_filter_1` lines 388-411 in `dispatch_gate.py`) catches the case where `_find_drawing_index_page()` returns `None`. So a hybrid false-negative downgrades to per-page title-block scanning rather than total failure.

### 4.3 Bottom line

> **Hybrid `\b([A-Z]{1,2})-?(\d{3,}[\.\d]*[A-Za-z]?\|\d+\.\d+[\.\d]*[A-Za-z]?)\b` is corpus-clean. Ship it.**
