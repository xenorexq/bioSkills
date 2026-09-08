# DIA-NN 2.6+ workflow and output contract

Use this reference for DIA-NN setup, log review, q-value interpretation, output parsing, and PTM search audits. It is intentionally version-aware rather than a frozen command copied from an older release.

Primary source: https://github.com/vdemichev/diann (reviewed 2026-09-08).

## Before running or interpreting

Record:

- exact DIA-NN binary version and license tier;
- raw-file format, instrument, acquisition window scheme, gradient, and run order;
- FASTA release, isoform policy, contaminants, and accession tags;
- enzyme, missed cleavages, peptide length/charge range, fixed and variable modifications;
- scoring mode, MBR/reanalysis mode, quantification mode, mass accuracy and scan window;
- every warning and the full generated command or saved pipeline.

Do not copy command-line flags from a paper or skill without checking the installed binary/GUI Wizard and `--help`. Flag names, defaults, output formats, and recommended modes have changed across DIA-NN releases.

## Predicted-library workflow

DIA-NN 2.6 documentation describes a two-stage workflow:

1. Generate a predicted library from the FASTA as its own pipeline step. Save the predicted `.speclib` and the exact digest/modification settings.
2. Analyze the raw files against that saved library with FASTA annotation, MBR/reanalysis and matrix generation as appropriate. Do not activate FASTA digest again in the raw-analysis step.

A run that combines in-silico prediction and raw analysis may complete while printing an `incorrect settings` warning. Treat the outputs as provisional until the warning is resolved or a matched two-step run shows the result is stable.

An empirical library generated from the project's DIA data is a different artifact from the whole-FASTA predicted library. Name and preserve both; do not call fragment rows, precursors, and proteins by the same count.

## Mode-specific search space

Use separate searches/libraries for whole proteome, phosphoproteome, and K-GG ubiquitinome. Combining several large variable-modification spaces in one search weakens power and obscures the null model.

- Whole proteome: standard digest and sample-preparation modifications. Oxidation and protein N-terminal acetylation are common variable modifications but are not biological PTM endpoints here.
- Phosphoproteome: phosphorylation on S/T/Y is the biological variable modification. Use DIA-NN's peptidoform/proteoform scoring and localization outputs; limit unrelated variable modifications.
- K-GG ubiquitinome: add the diglycine lysine remnant (UniMod:121, +114.042927 Da on K) and account for the blocked tryptic cleavage/search-space consequences. Limit unrelated variable modifications.

The exact maximum modification count and missed-cleavage allowance must match sample chemistry and be checked against search-space size and identification yield; they are not universal constants.

## Main output fields

The main report is a long precursor-by-run table. Selected fields:

- `Decoy`: 0/1 only becomes operational when decoys are reported; many normal main reports contain only `0`.
- `Precursor.Id`, `Modified.Sequence`, `Stripped.Sequence`, `Precursor.Charge`: precursor identity.
- `Protein.Group`: inferred reporting group; retain its membership context.
- `Protein.Ids`: all database proteins matched by the precursor.
- `Proteotypic`: whether the precursor is specific under the selected database/inference policy.
- `Precursor.Quantity`: non-normalized precursor quantity.
- `Precursor.Normalised`: normalized precursor quantity.
- `PG.MaxLFQ`: normalized QuantUMS/MaxLFQ protein-group quantity.
- `Q.Value`, `PEP`: run-specific precursor confidence.
- `Global.Q.Value`: experiment-wide precursor confidence.
- `Lib.Q.Value`: confidence stored for the relevant library entry; in MBR this refers to the first-pass empirical library.
- `PG.Q.Value`, `PG.PEP`: run-specific protein-group confidence.
- `Global.PG.Q.Value`, `Lib.PG.Q.Value`: global/library protein-group confidence contexts.
- `Peptidoform.Q.Value`, `Global.Peptidoform.Q.Value`, `Lib.Peptidoform.Q.Value`: modification-aware peptidoform confidence.
- `PTM.Site.Confidence`, `Lib.PTM.Site.Confidence`, `Site.Occupancy.Probabilities`, `Protein.Sites`: localization evidence and site mapping.
- `Quantity.Quality`, `Empirical.Quality`, `PG.MaxLFQ.Quality`: QuantUMS quantity-quality evidence when produced.

Q-values are filters for a declared list, not probabilities that a particular result is correct. PEP and site confidence answer different local questions.

## Filtering contract

For the main report, first state the analysis goal and then select the confidence context. Current DIA-NN guidance commonly considers:

- run-specific precursor `Q.Value` in the 0.01–0.05 range;
- `Global.Q.Value <= 0.01`;
- `Global.PG.Q.Value <= 0.01`;
- run-specific `PG.Q.Value` in the 0.01–0.05 range;
- the relevant `Lib.*` and peptidoform fields when MBR, an empirical DIA library, or PTM/peptidoform scoring is involved.

Do not use one universal Boolean expression for every mode. Save the selected expression in the output manifest and report how many rows, unique precursors, protein groups, and sites remain after each clause.

The wide matrices are intended as ready-to-use normalized summaries, but still require metadata validation, contaminant handling, missing-value representation, and appropriate statistics. If rebuilding a matrix from the long report, demonstrate set/count reconciliation rather than assuming the report and matrix must match.

## Decoys and contaminants

- Decoys calibrate scores and may be absent from the normal main report. Do not search the wide protein matrix for reverse accessions as a substitute for reading `Decoy` and the run log.
- Contaminants are a database/annotation contract. When FASTA accessions are tagged, use the exact tag such as `CONTAMINANT_`. For a protein-group matrix, exclude groups led by a tagged contaminant and retain the decision log.
- A precursor can map to both a biological protein and a contaminant duplicate. Removing every row whose `Protein.Ids` merely contains the tag may discard valid shared evidence; distinguish contaminant-led groups from mixed mappings.

## Required audit outputs

At minimum report:

- parsed version, command, warnings, number of raw runs;
- FASTA entries and tagged contaminant entries when the FASTA is available;
- main-report rows, unique runs/precursors/protein groups, decoy values;
- q-value minima/maxima and counts passing each proposed filter;
- matrix dimensions and sample-column mapping;
- contaminant-led group counts;
- run-level identification, mass accuracy, RT/FWHM and signal metrics;
- QuantUMS quality distributions when present;
- PTM localization and peptidoform confidence distributions for PTM modes.

Use `../scripts/inspect_diann_project.py` for a non-mutating first pass, then inspect mode-specific evidence directly.

## Key references

- DIA-NN documentation and main output reference: https://github.com/vdemichev/diann
- Demichev et al. DIA-NN. https://doi.org/10.1038/s41592-019-0638-x
- Grossmann et al. QuantUMS. https://doi.org/10.1038/s41587-026-03131-2
- Bekker-Jensen et al. library-free DIA phosphoproteomics. https://doi.org/10.1038/s41467-020-14609-1
- Hansen et al. DIA ubiquitinomics. https://doi.org/10.1038/s41467-020-20509-1
- Steger et al. DIA-NN K-GG ubiquitinomics. https://doi.org/10.1038/s41467-021-25454-1
