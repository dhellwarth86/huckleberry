# Phase 2 v0.1 Experiment — Verbatim Prompt for Claude Code

> This file is the permanent record of the experiment's instructions. The same prompt is in `PHASE_2_HANDOFF.md` Section 5 at the repo root. Both copies must stay synchronized; if you edit one, edit the other.
>
> **DO NOT MODIFY this prompt during the experiment.** It locks in scope. If you find yourself wanting to expand scope, document the expansion in `EXPERIMENT_FINDINGS.md` → "Recommended next experiments" instead.

---

You are running the Phase 2 v0.1 experiment for Huckleberry AI. Read `CLAUDE.md` and `PHASE_2_HANDOFF.md` in full before doing anything else. Then read `backend/seeds/README.md` and skim each of the five seed files to understand the four-layer reference architecture (dispatch / materials / assemblies). The "Phases" section in CLAUDE.md is canon — do not negotiate against the 18 architectural decisions documented there.

**Your goal**: produce three deliverables from running 15 real-world commercial roofing bidsets through a layered extraction pipeline that uses the seed files in `backend/seeds/`. The output is evidence-driven schema design, not a backend.

**You are NOT building**:
- A FastAPI backend (no routes, no DB models, no migrations)
- A tool stack recommendation (don't pick libraries beyond what's already in `backend/pyproject.toml`)
- LLM / ML / vision-model integration (Phase 3, refused for Phase 2)
- A glazing pipeline (glazing seeds are skeletons per their author; glazing is out of v0.1 scope — only roofing-relevant pages of the 15 bidsets are in scope)

**You ARE building**: an evidence-driven draft of the BidsetRecord wrapper schema, plus the findings that justify its shape.

## Deliverables (all three required, none optional)

### 1. Per-PDF JSON output

One file per bidset, written to `backend/test_fixtures/experiment_outputs/<bidset_id>.json`. Each file contains everything you observed about that bidset, organized by:

- `dispatch` — Layer 1 output: page classifications, sheet map, cross-references, legend regions, project metadata (DETERMINISTIC fields only — leave the LLM-only fields as null per `dispatch_seed.PROJECT_METADATA_LLM_ONLY`)
- `scope` — Layer 2 output: identified roofing systems with manufacturer / attachment / spec section, source page(s), confidence (using `dispatch_seed.CONFIDENCE` levels)
- `assembly` — Layer 3 output: per identified system, the components-list and any triggered relationship warnings
- `provenance` — for every populated field, what extraction method produced it and where in the PDF it came from (page index, text-block coords, regex pattern, etc.)
- `extraction_metrics` — pages processed, classification confidence histogram, fields that were null because the data wasn't present, fields that were null because the extractor failed

Use whatever per-bidset shape feels natural inside each section; the goal is observation, not yet schema. The schema design comes after, from looking at the 15 outputs together.

### 2. Draft Pydantic schema

Replaces the stub at `shared/bidset_record.py`. Built from observation, not guess. Apply the inclusion rule strictly:

- A field is in the schema if and only if it appears in **>= 3 of 15 bidsets** AND has an **identifiable downstream consumer** (a real or near-future user-facing capability that consumes it). Both conditions required.
- Fields that fail one or both conditions go in the deferred/observed appendix in the findings report, NOT in the schema.
- Every field in the schema must have a docstring justifying its inclusion: which bidsets had it, what consumes it.
- Top-level shape is layer-aligned: `id`, `schema_version`, `source_pdf_ref`, `dispatch`, `scope`, `assembly`, `annotations`, `provenance`. The stub already shows this — your job is to replace each layer's `dict[str, Any]` with concrete nested Pydantic models.

### 3. Findings report — `backend/EXPERIMENT_FINDINGS.md`

Markdown. Required sections:

- **Coverage matrix**: table with 15 rows (one per bidset) and N columns (one per observed field), marking which bidsets had which fields. The audit trail for the inclusion rule.

- **Dispatch layer accuracy**: how the four-layer pipeline performed against `dispatch_seed.py`'s patterns. Specifically measure against the **52 of 60 roof pages → universal fallback** baseline mentioned in `dispatch_seed.py`'s docstring — did the keyword lists in `PAGE_CLASSIFICATION_KEYWORDS` correctly classify roof pages on these 15 bidsets, or did they fall back? Report the new ratio (e.g., "44 of 53 roof pages classified correctly; 9 fell back"). If accuracy is worse than baseline, document why; if better, document what improved.

- **Scope layer accuracy**: for each bidset, how many systems were identified, with what confidence, and what manufacturer/spec-section data was attached. Note bidsets where scope was identified at the wrong level (e.g., "saw 'TPO' generically but missed the specific Carlisle product spec'd in the schedule").

- **Assembly layer accuracy**: for the systems that were identified, how many components from the matching `roof_assemblies.ROOF_SYSTEMS[*].required_components` could be supported by extracted text vs flagged as "expected but not found"? How many `ASSEMBLY_RELATIONSHIPS` warnings would have triggered if the user had drawn pins matching what's visible on the plans?

- **Promoted fields**: list of fields that made it into the schema. For each: count of bidsets in which it appeared, identified downstream consumer, short rationale.

- **Deferred / observed appendix**: fields that were observed but didn't meet the inclusion rule. For each: count, missing condition (frequency or consumer or both), notes on why it might still matter someday.

- **Surprises**: bullet list of things the experiment revealed that weren't predicted before looking at the data. This section is important — it's the signal that says "the experiment was actually useful." Examples of what counts as a surprise: "the title block was on the first page in 5 PDFs but on every page in 8" or "STACK-produced PDFs strip scale labels but preserve them in a hidden text layer." Examples of what doesn't count: "PDFs are sometimes large." Be specific.

- **Tooling notes**: which tools you used (start with pdfplumber per `pyproject.toml`; add others ONLY as specific failures justify, and document each addition with the failure that motivated it). Per-bidset success/failure record for each tool.

- **Recommended next experiments**: things you couldn't answer in v0.1 but that v0.2 should look into. Examples: "the dispatch keyword list misses architect-specific notation X — recommend expanding patterns" or "Sika Sarnafil's specs format differs enough from Carlisle that scope parser needs a per-manufacturer hook."

## The discipline

- **The four-layer architecture is canon.** Use the seeds. Don't reinvent classification or vocab — `dispatch_seed.py`'s patterns ARE the classification system, `roofing_materials.py`'s `MANUFACTURERS` and `SPEC_SECTIONS` ARE the vocab, `roof_assemblies.py`'s `ROOF_SYSTEMS` ARE the takeoff drivers. If a pattern fails, document the failure in tooling notes and recommended next experiments — DO NOT silently rewrite the seed file. Seed edits are a separate, explicit decision that goes through user review.

- **Glazing is out of scope.** Pages classified as glazing-relevant get noted but not deeply parsed. The glazing seed files are skeletons per their authors and need an estimator's review before they're trustworthy. v0.1 produces no glazing observations beyond "this page references glazing."

- **Don't pick a tool stack.** The experiment's output is a schema, not a stack recommendation. Tool picks happen after the schema is reviewed and the next milestone is planned. If pdfplumber fails on certain bidsets, document the failure mode in the findings report; do not pivot to Docling or Camelot mid-experiment unless pdfplumber is so broken that no useful output is being produced. If you do pivot, document why explicitly in tooling notes.

- **Don't write a backend.** No FastAPI app. No SQLAlchemy models. No HTTP endpoints. The backend is v0.2, planned after the schema is reviewed. Your work is in `backend/scripts/` (extraction), `shared/bidset_record.py` (schema replacement), and `backend/EXPERIMENT_FINDINGS.md` (the report). Stay there.

- **Use the inclusion rule honestly.** If only 2 bidsets have a field, it's deferred, not promoted. If a field is in 12 bidsets but you can't articulate a downstream consumer, it's deferred. Both criteria, every field, no shortcuts.

- **Provenance is not optional, even at v0.1.** Every promoted field should have a provenance shape — what extraction step produced it, what page, what confidence. Phase 2's whole reason for capturing provenance is Phase 3 training data (Decision #6). Drop provenance now and you've corrupted the dataset for Phase 3.

## Process

1. Read `CLAUDE.md` (especially "Phases" section), `PHASE_2_HANDOFF.md`, `shared/bidset_record.py` (the stub you're replacing), `backend/seeds/README.md`, and skim each of the five seed files.

2. Verify bootstrap: `cd backend && pytest tests/test_seeds_load.py` (expected: 7 passed). Then `python scripts/verify_fixtures.py` (expected: 15/15 reachable). Don't proceed if either fails.

3. Read the bidset manifest at `backend/test_fixtures/bidsets.json`. For each bidset:
   - Download from S3
   - Apply Layer 1 (dispatch filters) using `dispatch_seed.py` patterns
   - On classified pages, apply Layer 2 (scope parsing) using `roofing_materials.py`
   - For identified systems, apply Layer 3 (assembly mapping) using `roof_assemblies.py`
   - Record everything in the per-PDF JSON, including failures and confidence
   - Build the per-PDF JSON incrementally so partial progress survives session interruption

4. After all 15 are processed, build the coverage matrix from the 15 JSONs.

5. Apply the inclusion rule (≥3 of 15 AND downstream consumer). Promote fields. Defer fields.

6. Write the draft Pydantic schema in `shared/bidset_record.py`. Every promoted field must have a docstring justifying inclusion (which bidsets, what consumer). Replace the stub's `dict[str, Any]` placeholders with concrete nested models.

7. Write the findings report `backend/EXPERIMENT_FINDINGS.md`. All eight required sections.

8. Commit your work in `huckleberry/` with a descriptive message. Do not push (the user will review first).

9. Stop. Do not write a backend. Do not propose v0.2 architecture beyond the "recommended next experiments" section. Do not pick tool stacks. The next step after the experiment is the user's review checkpoint, not your code.

## What "done" looks like

- 15 JSON files in `backend/test_fixtures/experiment_outputs/`
- `shared/bidset_record.py` updated from stub to draft schema
- `backend/EXPERIMENT_FINDINGS.md` exists with all eight required sections
- Coverage matrix has 15 rows
- Dispatch layer accuracy is reported as a ratio against the 52/60 baseline
- Every promoted field has a docstring with bidset count + downstream consumer
- Deferred appendix has every observed-but-not-promoted field
- Surprises section is non-empty and specific
- You have not added a single FastAPI route, SQLAlchemy model, or HTTP endpoint
- Glazing pages are noted but not deeply parsed

Begin.
