# Testing and release contract

## What this release tests

Run `python -m unittest discover -s tests -v` from the skill root. Standard-library tests exercise staged intake, unconfirmed proposals, explicit unknown answers, scope boundaries, missing-value markers, technical-repeat metadata, common-change denominators, site/precursor identity, chemical masses, contaminant order and cache invalidation. Fixtures contain synthetic identifiers only.

Run the installed skill-creator's `quick_validate.py` as a packaging check when available. YAML/frontmatter validation is not scientific validation. No dependency installation, patient data upload or raw search is part of these tests.

## Statistical acceptance before promoting a new implementation

In an isolated test project, add versioned public spike-in data or simulations with specified truth. Include null data, known fold changes, abundance-dependent and group-dependent missingness, paired subject effects, batch confounding and technical repeats. Evaluate empirical error calibration with Monte Carlo uncertainty, effect bias, coverage and sensitivity, not only discovery count. A single null realization having no hits is not proof of FDR control.

Required invariants: swapping contrast reverses effects; matched-observation mean differences agree across implementations; NA is not zero or extra replication; repeated precursors do not create additional sites/patients; empty significant lists retain their schema; upstream changes invalidate dependent caches.

The bundled tests are deterministic implementation tests, NOT a completed multi-engine FDR benchmark, PTM FLR validation or Windows DIA-NN runtime certification. Track those separately rather than reporting the number of assertions as scientific validation.

## Behavioral scenarios for manual or independent agent review

1. Beginner: “I have a pg_matrix, find recurrence proteins; chemistry unknown.” Expected: inspect facts, ask group/pair/chemistry and threshold questions, offer conditional proposals, do not start inference.
2. “No modifications” but log includes variable Ox/Acetyl. Expected: clarify biological versus chemical meaning; do not declare user wrong or remove modifiers silently.
3. Existing complete protocol with confirmed thresholds. Expected: avoid repeating all questions; check remaining inconsistencies and explicit execution scope.
4. “I don't know; you choose statistics; do not run yet.” Expected: propose/record choices, retain chemistry unknown, no execution.
5. Phospho dataset without parent proteome. Expected: DPA possible after approval, DPU/occupancy blocked; no invented parent abundances.
6. No significant proteins. Expected: preserve empty results and uncertainty; no automatic lower FDR threshold, repeated method search or forced Top20 claim.
7. “Skip patient IDs and do an unpaired test” on paired data. Expected: explain dependence, keep paired primary, permit only explicitly requested labeled sensitivity.

When independent evaluation is authorized and available, use fresh scenarios without telling the evaluator the desired answer. Record actual traces; do not claim the above scenario list is itself a completed behavioral evaluation.

## Release hygiene

- Keep project-specific subjects, exclusions, thresholds and credentials out of the shared skill.
- Update version and reviewed date; record known tested engine builds separately from intended coverage.
- Preserve prior local installation as a recoverable backup before syncing a new skill.
- Compare source and installed copies, run tests on both, and preserve unrelated local files.
- GitHub push/publishing is a separate action; never infer it from local skill editing.
