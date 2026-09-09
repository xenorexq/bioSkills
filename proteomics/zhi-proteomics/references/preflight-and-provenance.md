# Preflight, evidence and provenance

## Before inferential execution

Ask and reconcile three separate layers: (1) actual sample-preparation SOP/user confirmation; (2) exact search command/build/library settings; (3) report sequences, masses, q-value fields and quantitative outputs. Contradictions are findings, not permission to silently change either layer. A lab's nominal SOP may also need confirmation if individual samples were treated differently.

Chemistry review covers species/mixture, preservation, reduction/alkylation and reagent, protease/P-blocking, enrichment/PTM, inhibitors, and matching database modifications. Missing fixed C in a command is a prompt for review, not proof of no alkylation. Inspect actual modified sequences; compare precursor m/z where available. `evidence_contracts.py` supports a small explicit mass dictionary and rejects unrecognized syntax/modifications rather than guessing.

Whole-proteome “not a PTM study” is not “no chemical modifications”. Oxidation/acetylation search options are not always beneficial; choose based on purpose and current documentation rather than assuming every standard variable modification is mandatory.

## Issue levels and affected endpoints

| Level | Typical issue | Permitted next action |
| --- | --- | --- |
| Block affected inference | unresolved sample identity/direction; rank-deficient comparison; missing localization for a site claim | resolve or omit affected endpoint; authorized inventory/QC can continue |
| Pilot review | uncertain chemistry/search consistency; warning whose current-version impact is unvalidated; unknown treatment/batch | explain limitations, ask whether restricted pilot should proceed; never bypass hard blocks |
| Record | known informational message or warning unrelated to requested endpoint | record the version/evidence and why it does not alter the requested task |

Known chemistry incompatible with a proposed search blocks that proposed search until corrected/confirmed. Existing results may be explored only as an explicitly compromised pilot, not certified as valid identification/quantification. Missing parent proteome blocks DPU, not necessarily DPA. A site ambiguity blocks site-specific claims but may permit peptidoform-level reporting.

For every issue, record: `code`, `severity`, `source`, `software_build`, `affected_endpoint`, `decision`, `resolution_condition`, and `user_authorization_if_needed`. Unknown is not a green QC status.

## Software, metadata and cache

Keep `subject_id`, `biosample_id`, `aliquot_id`, `run_id`, `condition`, `timepoint`, `fraction`, `technical_replicate_type`, `prep_batch`, `enrichment_batch`, and `acquisition_batch` distinct when applicable. A reinjection does not add a subject. File number is not verified acquisition order; a specimen accession is not an exact date.

The pair validator can recognize reinjections with explicit biosample/run columns. It validates identities/counts only, never merges intensities or chooses a model. More than one biological sample in one subject/condition requires an explicitly modeled nested/longitudinal design. Unknown batch cells remain unknown; run a design-matrix rank/estimability check in the actual modeling environment.

Cache fingerprints include raw-file hashes, FASTA/library hashes, software/build, exact search/quantification/normalization parameters and relevant prediction model versions. Distinguish cached per-run search from cross-run normalization/library learning; changing cohort membership may require rerunning downstream cross-run stages. `--use-quant` is only evidence that reuse was requested, not proof every file was reused compatibly.

Never pick an arbitrary result when multiple `report.parquet`/logs exist. Require an exact output directory or manifest. Keep original files and use new outputs for reruns. Do not call a first-pass empirical library the original whole-FASTA predicted library. Task-level two stages and MBR's internal two passes are distinct.

## Confidence profiles and quantitative QC

Store exact column expressions for the engine/build/mode. In DIA-NN Peptidoforms + MBR, review applicable `Lib.Peptidoform.Q.Value` in addition to precursor/protein context. Missing required fields are unsupported, not zero or silently ignored filters. A main report containing Decoy=0 only is not evidence that target-decoy calibration was absent.

Contaminants: classify all-contaminant, noncontaminant and mixed groups independently of accession order. Remove explicitly all-contaminant groups under the chosen policy; flag mixed mappings and document the inference/quantification policy. A leading-prefix-only legacy policy may be retained for a frozen reproduction, but label it rather than calling it universally correct.

Inspect distributions/missingness of `Quantity.Quality`, `PG.MaxLFQ.Quality` and other available quantification-quality columns with definitions from the matching software. Do not turn arbitrary quality scores into linear-model precision weights without a supported mapping and calibration. A q-value is not an abundance uncertainty estimate.

Distinguish implementation assertions from statistical validation. Checksums and row counts cannot establish false-discovery calibration, adequate power, or scientific truth.

## References

- DIA-NN current manual and version history: https://github.com/vdemichev/DiaNN
- Version-specific historical combined-run fix: https://github.com/vdemichev/DiaNN/releases/tag/1.9.2
- Maintainer explanation of combined settings: https://github.com/vdemichev/DiaNN/discussions/1558
- QuantUMS methods: https://doi.org/10.1038/s41587-026-03131-2
- quantms design/provenance: https://doi.org/10.1038/s41592-024-02343-1
