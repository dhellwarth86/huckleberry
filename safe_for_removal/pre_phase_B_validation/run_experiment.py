"""run_experiment.py — Phase 2 v0.1 experiment driver.

Reads test_fixtures/bidsets.json, walks each PDF, runs Layer 1 / 2 / 3,
writes per-PDF JSON to test_fixtures/experiment_outputs/<id>.json.

Usage:
    cd backend
    .venv/Scripts/python.exe scripts/run_experiment.py
    .venv/Scripts/python.exe scripts/run_experiment.py --only chipotle-tarpon-springs-shell-tarpon-springs-strategic-construction
    .venv/Scripts/python.exe scripts/run_experiment.py --resume   # skip bidsets whose JSON already exists

The output JSON is exhaustive — captures every observed field for every
bidset.  Schema design (which fields graduate) happens AFTER all 15 are
processed, in a separate step using these JSONs as evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import pypdfium2 as pdfium

# Make `scripts.<...>` and `seeds.<...>` importable when run from backend/
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(BACKEND_DIR.parent / "shared"))

from scripts._pipeline.dispatch import (  # noqa: E402
    PageText,
    build_dispatch_layer,
)
from scripts._pipeline.scope import build_scope_layer  # noqa: E402
from scripts._pipeline.assembly import build_assembly_layer  # noqa: E402

MANIFEST_PATH = BACKEND_DIR / "test_fixtures" / "bidsets.json"
OUTPUT_DIR = BACKEND_DIR / "test_fixtures" / "experiment_outputs"


def extract_pages(pdf_path: Path) -> list[PageText]:
    """Extract per-page text using pypdfium2.

    pdfplumber.extract_text() is ~70x slower than pypdfium2 on STACK PDFs
    because it walks every path operator (46-92k per page on these
    bidsets) to derive text positions. v0.1 doesn't need spatial precision
    — substring matching against keyword lists is sufficient. pypdfium2
    uses the same pdfium engine Chrome ships, gets full text reliably,
    and processes 39 pages in ~2s vs pdfplumber's ~140s.

    Title-block approximation: bottom-right quadrant via get_text_bounded.
    """
    pages: list[PageText] = []
    doc = pdfium.PdfDocument(str(pdf_path))
    try:
        for idx in range(len(doc)):
            page = doc[idx]
            try:
                tp = page.get_textpage()
                full_text = tp.get_text_range() or ""
                width = float(page.get_width())
                height = float(page.get_height())

                # Title block = bottom-right quadrant. pypdfium2 uses
                # PDF coordinate space where origin is bottom-left and
                # y increases upward. Bottom-right = (left=0.55w, bottom=0,
                # right=w, top=0.35h).
                tb_left = width * 0.55
                tb_bottom = 0.0
                tb_right = width
                tb_top = height * 0.35
                try:
                    tb_text = tp.get_text_bounded(
                        left=tb_left, bottom=tb_bottom,
                        right=tb_right, top=tb_top,
                    ) or ""
                except Exception:
                    tb_text = (full_text or "")[-600:]

                tp.close()
            except Exception:
                full_text = ""
                tb_text = ""
                width = height = 0.0
            finally:
                page.close()

            text_blocks = [
                {"text": line.strip()}
                for line in (full_text or "").splitlines()
                if line.strip()
            ]

            pages.append(PageText(
                page_index=idx,
                full_text=full_text,
                title_block_text=tb_text or full_text[-600:],
                text_blocks=text_blocks,
                width=width,
                height=height,
            ))
    finally:
        doc.close()
    return pages


def process_bidset(entry: dict) -> dict:
    """Run all three layers against a bidset, return the per-PDF JSON dict.

    The dict shape is layer-aligned so future schema work can read it directly.
    """
    pdf_path = Path(entry["local_path"])
    started = time.time()

    try:
        pages = extract_pages(pdf_path)
    except Exception as e:
        return {
            "id": entry["id"],
            "schema_version": "0.1",
            "source_pdf_ref": entry,
            "extraction_error": f"{type(e).__name__}: {e}",
            "extraction_traceback": traceback.format_exc(),
            "extracted_at": datetime.now(timezone.utc).isoformat(),
        }

    # Layer 1
    dispatch_out = build_dispatch_layer(pages)
    classifications = dispatch_out["page_classifications"]

    # Layer 2
    scope_out = build_scope_layer(pages, classifications)

    # Layer 3
    assembly_out = build_assembly_layer(scope_out, pages, classifications)

    # Provenance — minimal field-level provenance for v0.1
    provenance = build_provenance(scope_out, assembly_out, classifications)

    # Per-bidset extraction metrics
    elapsed = time.time() - started
    metrics = {
        "elapsed_seconds": round(elapsed, 2),
        "pages_processed": len(pages),
        "page_type_histogram": dispatch_out.get("page_type_histogram", {}),
        "confidence_histogram": dispatch_out.get("confidence_histogram", {}),
        "roof_pages_found": len(dispatch_out.get("roof_page_indices", [])),
        "scope_systems_identified": len(scope_out.get("systems", [])),
        "scope_pages_inspected": len(scope_out.get("pages_inspected", [])),
        "scope_fallback_used": scope_out.get("fallback_used", False),
        "scope_pages_skipped_glazing": scope_out.get("pages_skipped_glazing", 0),
        "extracted_at": datetime.now(timezone.utc).isoformat(),
    }

    return {
        "id": entry["id"],
        "schema_version": "0.1",
        "source_pdf_ref": entry,
        "dispatch": dispatch_out,
        "scope": scope_out,
        "assembly": assembly_out,
        "provenance": provenance,
        "extraction_metrics": metrics,
    }


def build_provenance(scope_out: dict, assembly_out: dict, classifications: list[dict]) -> dict:
    """Build the field-level provenance trail.

    Each promoted scope/assembly field gets a provenance entry naming its
    extraction method, source page(s), and confidence. Phase 3 ML training
    depends on this audit trail being intact from v0.1.
    """
    prov: dict = {"fields": {}}
    for sys_idx, sys in enumerate(scope_out.get("systems", [])):
        path_root = f"scope.systems[{sys_idx}]"
        prov["fields"][f"{path_root}.system_type"] = {
            "extraction_method": "scope.find_spec_sections + scope.find_system_type_keywords",
            "source_pages": sys.get("source_pages", []),
            "confidence": sys.get("confidence"),
            "parser_value": sys.get("system_type"),
        }
        if sys.get("manufacturer"):
            prov["fields"][f"{path_root}.manufacturer"] = {
                "extraction_method": "scope.find_manufacturers (filtered by system_type)",
                "source_pages": sys.get("source_pages", []),
                "confidence": sys.get("confidence"),
                "parser_value": sys.get("manufacturer"),
            }
        if sys.get("attachment"):
            prov["fields"][f"{path_root}.attachment"] = {
                "extraction_method": "scope.find_attachments (most-common)",
                "confidence": sys.get("confidence"),
                "parser_value": sys.get("attachment"),
            }
        if sys.get("spec_sections"):
            prov["fields"][f"{path_root}.spec_sections"] = {
                "extraction_method": "scope.find_spec_sections",
                "source_pages": sys.get("source_pages", []),
                "parser_value": sys.get("spec_sections"),
            }
    for sys_idx, sys in enumerate(assembly_out.get("systems", [])):
        path_root = f"assembly.systems[{sys_idx}]"
        if sys.get("matched_assembly_key"):
            prov["fields"][f"{path_root}.matched_assembly_key"] = {
                "extraction_method": "assembly.pick_assembly_key",
                "parser_value": sys.get("matched_assembly_key"),
            }
    # Sheet map provenance
    prov["fields"]["dispatch.sheet_map"] = {
        "extraction_method": "dispatch.extract_sheet_number on title-block text",
    }
    prov["fields"]["dispatch.page_classifications"] = {
        "extraction_method": "dispatch.classify_page using PAGE_CLASSIFICATION_KEYWORDS",
        "rule_source": "seeds/dispatch_seed.py",
    }
    return prov


def write_output(entry_id: str, payload: dict) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{entry_id}.json"
    tmp = out_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(payload, indent=2, default=str))
    tmp.replace(out_path)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", help="Process only this bidset id (can repeat)")
    parser.add_argument("--resume", action="store_true", help="Skip bidsets whose output already exists")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N bidsets")
    args = parser.parse_args()

    if not MANIFEST_PATH.exists():
        print(f"ERROR: manifest not found: {MANIFEST_PATH}", file=sys.stderr)
        return 2

    manifest = json.loads(MANIFEST_PATH.read_text())
    bidsets = manifest.get("bidsets", [])

    if args.only:
        bidsets = [b for b in bidsets if b["id"] in args.only]
    if args.limit:
        bidsets = bidsets[: args.limit]

    print(f"Processing {len(bidsets)} bidset(s)\n")

    n_done = 0
    n_skipped = 0
    n_failed = 0
    for entry in bidsets:
        bid_id = entry["id"]
        out_path = OUTPUT_DIR / f"{bid_id}.json"
        if args.resume and out_path.exists():
            print(f"[skip] {bid_id} (output exists)")
            n_skipped += 1
            continue
        print(f"[run]  {bid_id}  ({entry['filename']}, {entry.get('page_count', '?')} pp)")
        try:
            payload = process_bidset(entry)
            written = write_output(bid_id, payload)
            n = payload.get("extraction_metrics", {})
            err = payload.get("extraction_error")
            if err:
                print(f"   FAILED: {err}")
                n_failed += 1
            else:
                print(
                    f"   OK  pages={n.get('pages_processed')}  "
                    f"roof_pages={n.get('roof_pages_found')}  "
                    f"systems={n.get('scope_systems_identified')}  "
                    f"elapsed={n.get('elapsed_seconds')}s -> {written.name}"
                )
                n_done += 1
        except Exception as e:
            print(f"   CRASHED: {type(e).__name__}: {e}")
            traceback.print_exc()
            n_failed += 1

    print(f"\nDone. ok={n_done} skipped={n_skipped} failed={n_failed}")
    return 0 if n_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
