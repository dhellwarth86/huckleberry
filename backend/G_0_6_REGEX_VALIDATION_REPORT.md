# G.0.6 Regex Theory Validation Report

**Date:** 2026-05-01
**Phase:** G.0.6 (read-only regex experiment)
**Branch:** `phase2-v0.3-G0-6-regex-validation` from `9cdcec5` (G.0.5 head)
**Executed by:** Claude Code (Developer session)
**Deliverable shape:** Single markdown report, 3 sections + 1 verdict. Zero code changes. Zero tracked files modified. Sacred floors held (230/19/0).

**What this report does:** Extracts raw text from three PDF pages via PyMuPDF, applies the current `_SHEET_NUM_RE` regex and three proposed tighter alternatives using the parser's exact matching logic (line-start `.match()` with dash-normalization), classifies every matched token, and determines whether a regex-only fix can separate the false-positive (Silverleaf page 5) from the true-positive (Bearss Ave page 0).

**What this report does NOT do:** No code changes. No fixes proposed. No dispatches run.

---

## §1 — Scout 1: The Bogus Index (Silverleaf)

### 1.1 Methodology

Text extracted from Silverleaf PDF (`B2607 AEA Silverleaf - St Augustine - Accelerated Construction Services (6).pdf`) pages 0 and 5 using `fitz.open(path)[page_idx].get_text("text")`. Each line normalized per `dispatch_gate.py:210` (`re.sub(r'([A-Z])\s*-\s*(\d)', r'\1-\2', line.strip())`), then matched at line start per `dispatch_gate.py:213` (`_SHEET_NUM_RE.match(line_norm)`).

### 1.2 Silverleaf Page 0 — The Real Cover (Parser Skipped It)

| Metric | Value |
|--------|-------|
| Total text lines | 685 |
| Lines matching `_SHEET_NUM_RE` at start | 6 |
| Unique tokens | **4** |

**Token inventory:**

| Token | Prefix | Number | Count | Classification |
|-------|--------|--------|-------|----------------|
| `A101` | A | 101 | 2 | **Real sheet number** — architectural plan reference |
| `S000` | S | 000 | 2 | **Real sheet number** — structural cover sheet |
| `S001` | S | 001 | 1 | **Real sheet number** — structural sheet |
| `S1` | S | 1 | 1 | **Not a sheet number** — extracted from line "S1 = 0.052" (a structural calculation value) |

**Assessment:** 4 unique tokens, well below the ≥10 threshold. Page 0 is correctly rejected by the parser. Three of four tokens are legitimate sheet references appearing in footer cross-references, but the page has no tabular index structure. The `S1` match is noise from an engineering formula.

### 1.3 Silverleaf Page 5 — The False Positive (Parser Chose It)

| Metric | Value |
|--------|-------|
| Total text lines | 195 |
| Lines matching `_SHEET_NUM_RE` at start | 46 |
| Unique tokens | **10** (exactly at threshold) |

**Token inventory:**

| Token | Prefix | Number | Count | Classification |
|-------|--------|--------|-------|----------------|
| `HD1` | HD | 1 | 1 | **Component mark** — structural hold-down connector |
| `HD8` | HD | 8 | 4 | **Component mark** — structural hold-down connector |
| `L1` | L | 1 | 3 | **Level/line marker** — structural grid line or level reference |
| `L2` | L | 2 | 18 | **Level/line marker** — structural grid line or level reference |
| `L3` | L | 3 | 2 | **Level/line marker** — structural grid line or level reference |
| `MW-1` | MW | 1 | 5 | **Component mark** — moment wall or metal wall identifier |
| `S101` | S | 101 | 1 | **Real sheet number** — this page's own title-block sheet ID |
| `S502` | S | 502 | 7 | **Real sheet number** — cross-reference to a detail sheet |
| `SW-3S` | SW | 3S | 2 | **Component mark** — shear wall identifier |
| `WD1` | WD | 1 | 2 | **Component mark** — window detail or wood component mark |

**Classification summary:**

| Category | Count | Tokens |
|----------|-------|--------|
| Real sheet numbers | 2 | `S101`, `S502` |
| Component marks (structural hardware) | 5 | `HD1`, `HD8`, `MW-1`, `SW-3S`, `WD1` |
| Level/line markers | 3 | `L1`, `L2`, `L3` |
| **Total** | **10** | |

**Assessment:** 8 of 10 unique tokens (80%) are structural annotation markers, not sheet numbers. The page is sheet `S101 ROOF FRAMING PLAN` — a dense structural drawing where component callouts (`HD` = hold-down, `MW` = moment wall, `SW` = shear wall, `WD` = window detail) and grid-line labels (`L1`–`L3`) each start their own text line in the PyMuPDF extraction. The token count lands at exactly 10 — the minimum threshold — with zero margin. All 8 false tokens have **single-digit numbers** (1, 2, 3, 8) or **non-numeric suffixes** (3S), and 5 of 8 have **two-letter prefixes** not found in any discipline standard (HD, MW, SW, WD).

---

## §2 — Scout 2: The Working Case (Bearss Ave)

### 2.1 Bearss Ave Page 0 — The Real Drawing Index

| Metric | Value |
|--------|-------|
| Total text lines | 659 |
| Lines matching `_SHEET_NUM_RE` at start | 48 |
| Unique tokens | **47** |

**Token inventory (all 47, sorted by discipline):**

| Discipline | Tokens | Count |
|------------|--------|-------|
| A (Architectural) | `A-001`, `A-002`, `A-003`, `A-101`, `A-121`, `A-201`, `A-202`, `A-401`, `A-402`, `A-501`, `A-601` | 11 |
| S (Structural) | `S-000`, `S-100`, `S-101`, `S-102`, `S-103`, `S-200`, `S-210`, `S-300`, `S-301`, `S-310`, `S-311`, `S-312`, `S-313`, `S-320`, `S-321`, `S-322`, `S-323`, `S-400`, `S-500`, `S-501`, `S-510`, `S-520`, `S-530` | 23 |
| M (Mechanical) | `M-001`, `M-002`, `M-100` | 3 |
| P (Plumbing) | `P-001`, `P-002`, `P-100` | 3 |
| E (Electrical) | `E-001`, `E-002`, `E-101`, `E-201`, `E-301`, `E-401` | 6 |
| C (Civil) | `C123` | 1 |

**Classification summary:**

| Category | Count | Notes |
|----------|-------|-------|
| Real sheet numbers | **47** | All tokens follow NCS convention: single-letter discipline prefix + 3-digit number |
| Component marks | 0 | — |
| Noise | 0 | — |

**Assessment:** 47 of 47 tokens (100%) are legitimate sheet numbers. Every token has a single-letter NCS discipline prefix (A, S, M, P, E, C) and a 3-digit number. Noise ratio is zero. The one format variant is `C123` (no dash), compared to the dash-separated format used by all other entries — this is a common real-world variation. All remainders are empty because the Bearss index uses split-line format (sheet number on one line, title on the next).

---

## §3 — Scout 3: Regex Alternatives

### 3.1 Current Regex

```python
_SHEET_NUM_RE = re.compile(r'\b([A-Z]{1,2})-?(\d+[\.\d]*[A-Za-z]?)\b')
```

**What it accepts:** 1–2 uppercase letters, optional dash, one or more digits with optional decimal and trailing letter. This is intentionally broad — it catches `A-1.3`, `FP-100`, `A101`, and `S502` alike. The problem: it also catches `HD1`, `L2`, `MW-1`, `WD1`, and `SW-3S`.

### 3.2 Alternative A — Discipline Prefix Allowlist

```python
ALT_A = re.compile(r'\b([ASMEPGCL]|FP)-?(\d+[\.\d]*[A-Za-z]?)\b')
```

**Rationale:** Restrict the prefix group to known NCS discipline designators used in the codebase's `_DISCIPLINE_MAP`: A (Architectural), S (Structural), M (Mechanical), E (Electrical), P (Plumbing), G (General), C (Civil), L (Landscape), FP (Fire Protection). Rejects prefixes not in any discipline standard: HD, MW, SW, WD.

**Trade-off:** L (Landscape) is a valid discipline, so `L1`, `L2`, `L3` still match. This is correct behavior for a Landscape sheet like `L-1.0`, but produces false positives on structural level/line markers that happen to start with L.

### 3.3 Alternative B — Single-Letter Prefix + Minimum 3 Digits

```python
ALT_B = re.compile(r'\b([A-Z])-?(\d{3,}[\.\d]*[A-Za-z]?)\b')
```

**Rationale:** Two filters stacked: (1) single-letter prefix only, rejecting all 2-letter prefixes (HD, MW, SW, WD, and also FP); (2) minimum 3 digits, rejecting single/double-digit numbers (1, 2, 3, 8, 3S). Real NCS sheet numbers use 3-digit numbering (A-101, S-200, E-301).

**Trade-off:** Rejects `FP-100` (Fire Protection) because `FP` is 2 letters. Any bidset with Fire Protection sheets would lose those entries. Also rejects legitimate short-numbered sheets if they exist (e.g., `A-1.3` format with sub-decimal notation).

### 3.4 Alternative C — Any Prefix + Minimum 3 Digits

```python
ALT_C = re.compile(r'\b([A-Z]{1,2})-?(\d{3,}[\.\d]*[A-Za-z]?)\b')
```

**Rationale:** Same as current regex but with one change: minimum 3 digits instead of 1. Keeps 2-letter prefix support (FP-100 passes), but rejects all single/double-digit numbers. This targets the specific failure mode: structural component marks universally use 1–2 digit identifiers (HD1, L2, MW-1), while real sheet numbers universally use 3+ digit identifiers (A-101, S-502, FP-100).

**Trade-off:** Would reject sheets using sub-3-digit numbering, such as `A-1.3` or `S-1.0` (common in smaller residential plan sets). However, the threshold is "≥10 unique tokens on an index page" — small plan sets with <10 sheets wouldn't hit the threshold anyway, so this is unlikely to cause false negatives in practice.

### 3.5 Decision Matrix

Results from applying each regex to all three pages using the parser's exact `.match()` + normalization logic:

| Page | Current | Alt A | Alt B | Alt C | Desired |
|------|---------|-------|-------|-------|---------|
| Silverleaf p0 | 4 (FAIL) | 4 (FAIL) | 3 (FAIL) | 3 (FAIL) | FAIL (not an index) |
| **Silverleaf p5** | **10 (PASS)** | **5 (FAIL)** | **2 (FAIL)** | **2 (FAIL)** | **FAIL (not an index)** |
| Bearss p0 | 47 (PASS) | 47 (PASS) | 47 (PASS) | 47 (PASS) | PASS (real index) |

All three alternatives correctly reject Silverleaf page 5 and correctly accept Bearss page 0.

### 3.6 Surviving Tokens Under Each Alternative

**Silverleaf page 5:**

| Token | Current | Alt A | Alt B | Alt C | Reality |
|-------|---------|-------|-------|-------|---------|
| `HD1` | match | — | — | — | component mark |
| `HD8` | match | — | — | — | component mark |
| `L1` | match | match | — | — | level marker |
| `L2` | match | match | — | — | level marker |
| `L3` | match | match | — | — | level marker |
| `MW-1` | match | — | — | — | component mark |
| `S101` | match | match | match | match | real sheet |
| `S502` | match | match | match | match | real sheet |
| `SW-3S` | match | — | — | — | component mark |
| `WD1` | match | — | — | — | component mark |
| **Unique** | **10** | **5** | **2** | **2** | — |

**Bearss page 0:** All 47 tokens pass under all four regexes. No entries lost.

---

## §4 — Verdict

### 4.1 Finding

**All three proposed alternatives cleanly reject Silverleaf's bogus index AND accept Bearss's real index.** The fix is regex-amenable.

### 4.2 Recommendation

**Alternative C** (`\b([A-Z]{1,2})-?(\d{3,}[\.\d]*[A-Za-z]?)\b`) is the recommended candidate:

1. **Minimal change:** differs from the current regex by exactly one character (`\d+` → `\d{3,}`).
2. **Preserves 2-letter prefix support:** FP (Fire Protection) sheets pass, unlike Alt B.
3. **Targets the exact failure mode:** every false-positive token on Silverleaf p5 has a 1-digit number. Every true-positive token on Bearss p0 has a 3-digit number. The digit-count floor is the cleanest discriminator.
4. **Zero collateral damage on the tested data:** Bearss p0 retains all 47 entries.

### 4.3 Risk assessment for Alt C

| Risk | Severity | Mitigation |
|------|----------|------------|
| Rejects `A-1.3` format (sub-3-digit with decimal) | Medium | These appear in smaller residential sets. However, such sets typically have <10 sheets, so they wouldn't trigger the ≥10 threshold anyway. Verify against the full 20-bidset corpus before implementing. |
| Rejects `G-0.0` format (zero-padded single digit) | Low | `G-0.0` has 1 digit before the decimal. Would need `\d{1,}` to match. But `G-0.0` is uncommon as a standalone format in drawing indexes. |
| Component marks with 3+ digits (e.g., `HD100`) | Low | Uncommon. Structural hardware marks rarely exceed 2 digits. If they do, the 2-letter prefix filter (Alt A) would catch them, suggesting a combined A+C approach as a fallback. |

### 4.4 Open question for implementation phase

The `A-1.3` / `G-0.0` format (discipline + single digit + decimal) is used in some of the 20-bidset test corpus. Before changing the regex, the implementation phase should run Alt C against all 20 bidsets' first-10-page scans to verify no real drawing index is lost. The threshold interaction (≥10 unique tokens) may make this a non-issue — a plan set using `A-1.3` numbering that has 10+ sheets would have tokens like `A-1.0` through `A-1.9` then `A-2.0`, which all have single-digit leading numbers and would be rejected by Alt C's `\d{3,}` floor.

**If the 20-bidset sweep reveals losses:** a hybrid approach combining Alt A's prefix allowlist with Alt C's digit floor would provide defense in depth. Alternatively, the digit floor could be lowered to `\d{2,}` (≥2 digits), which still kills 7 of 8 Silverleaf false positives (all except `HD8` which has 1 digit) while accepting `A-1.3` tokens (since `1.3` starts with digit `1` — wait, `\d{2,}` requires the leading digit run to be ≥2, so `1.3` would match `1` as `\d{1}` and fail). The correct hybrid would need regex design work in the implementation phase.

### 4.5 Bottom line

> **Alternative C cleanly rejects Silverleaf's bogus index AND accepts Bearss's real index.** The minimum-3-digit floor is the single most effective discriminator between structural component marks and real NCS sheet numbers. Implementation should validate against the full 20-bidset corpus before committing the regex change.
