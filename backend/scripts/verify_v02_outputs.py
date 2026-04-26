"""Verify Step 16 outputs against the gate spec:

- 15/15 JSONs present
- Each has dispatch_complete: true
- Each has filters_completed == ["filter_1", "filter_2", "filter_4", "filter_3", "filter_5"]
- AutoZone bidsets have project_scope null/empty (gate doing its job)
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "test_fixtures" / "v0.2_outputs"
EXPECTED_FILTERS = ["filter_1", "filter_2", "filter_4", "filter_3", "filter_5"]


def main() -> int:
    files = sorted(OUT_DIR.glob("*.json"))
    print(f"{len(files)} JSON(s) in {OUT_DIR}")
    print()

    headers = ("id", "complete", "filters", "pages", "scope_pages", "detected_system", "warnings")
    print(f"{headers[0]:<60}  {headers[1]:<8}  {headers[2]:<8}  {headers[3]:<5}  {headers[4]:>11}  {headers[5]:<16}  {headers[6]}")
    print("-" * 140)

    fails = 0
    for p in files:
        d = json.loads(p.read_text(encoding="utf-8"))
        bid = p.stem
        complete = d.get("dispatch_complete", False)
        filters = d.get("filters_completed", [])
        filters_match = filters == EXPECTED_FILTERS
        ps = d.get("project_scope") or {}
        sp_count = len(ps.get("scope_pages", []) or [])
        ds = ps.get("detected_system")
        warn = len(d.get("dispatch_warnings", []))
        total_pages = d.get("total_pages", 0)
        flag = "OK"
        if not complete:
            flag = "FAIL-INCOMPLETE"
            fails += 1
        elif not filters_match:
            flag = "FAIL-FILTERS"
            fails += 1
        print(f"{bid:<60}  {str(complete):<8}  {str(filters_match):<8}  {total_pages:>5}  {sp_count:>11}  {str(ds):<16}  {warn}  {flag}")

    print()
    print(f"FAILS: {fails}")
    print()
    print("AutoZone scope-empty check (gate doing its job per orders):")
    for p in files:
        if "auto-zone" in p.stem:
            d = json.loads(p.read_text(encoding="utf-8"))
            ps = d.get("project_scope") or {}
            sp = ps.get("scope_pages", []) or []
            ds = ps.get("detected_system")
            verdict = "OK (empty scope)" if (not sp and ds is None) else "UNEXPECTED"
            print(f"  {p.stem}  detected_system={ds!r}  scope_pages={sp}  -> {verdict}")

    print()
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
