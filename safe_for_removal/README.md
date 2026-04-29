# safe_for_removal/

This folder collects files that are no longer needed for active development as of 2026-04-29.

## What's in here

Each subdirectory contains files retired from active use, grouped by category. Each file in a subdirectory has a corresponding entry in `MANIFEST.md` describing:

- What the file was
- When it was active
- Why it's retired
- What replaced it (if anything)
- What to look at if you encounter related issues

## What this folder is for

Daniel reviews this folder at his pace to confirm nothing critical is in here. After review:

1. If something here turns out to still be needed, move it back out (this folder is not deleted yet)
2. Once Daniel confirms everything here is safe, the folder gets removed in a future session
3. The MANIFEST.md is preserved (copied out before deletion) and converted into a wiki — "what was retired and why, useful for debugging old issues"

## What this folder is NOT for

- Vault-ruled production modules (roofing_module, glazing_module, roofing_vocabulary, glazing_vocabulary, debug_module) — these stay in `backend/core/`
- Sacred files (frontend HTMLs, TracePoint reference sources, seed files) — these stay in their canonical locations
- Active march orders or canonical documentation (PROJECT_CLAUDE.md, VALIDATION_LEDGER.md, BLOCK_RUN.md, current march orders) — these stay in workspace root or `backend/`
- Active test fixtures actually used by the test suite (216 backend tests) — these stay where the test runner expects them

## Subdirectories

(populated as work proceeds; each subdirectory category named in MANIFEST.md)

---

This folder exists temporarily. Last reviewed: pending.
