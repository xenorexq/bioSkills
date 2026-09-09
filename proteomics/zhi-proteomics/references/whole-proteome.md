# DIA whole-proteome workflow

Use this reference for DIA-NN protein-group matrices and whole-proteome differential analysis.

## Input contract

Prefer the DIA-NN protein-group matrix for routine downstream analysis and retain the main parquet report for quality, q-value, precursor, and protein-group evidence.

Keep immutable copies of:

- `report.parquet`, `report-lib.parquet`, log, manifest and stats;
- `report.pg_matrix.tsv`, `report.pr_matrix.tsv`, and description/annotation tables;
- the FASTA and exact contaminant tag;
- sample metadata with original run name, biological sample, subject, condition, batch, and exclusion status.

Never replace raw run names without retaining a reversible mapping table.

## Cleaning

1. Verify that all expected runs appear exactly once and no sample name is duplicated.
2. Remove decoys if present; classify protein groups by all-contaminant, mixed or noncontaminant membership using the configured FASTA tag. Exclude all-contaminant groups under the recorded policy and review mixed groups; do not change classification when member order changes.
3. Retain `Protein.Group`, matched accessions, gene annotation, sequence counts, and proteotypic-sequence counts.
4. Convert explicit zero/unquantified values to missing before log transformation. Do not convert missing values to biological zero.
5. Use log2 for distributional QC and linear modeling.
6. Do not add median, quantile, VSN, or batch normalization by default to an already normalized DIA-NN MaxLFQ/QuantUMS matrix. Diagnose a residual need first and record it as a separate sensitivity analysis.

## Protein inclusion

Choose a filter from the design, not a universal percentage.

- Paired design: require a pre-specified minimum number of complete pairs for the primary abundance test. Report the number of contributing pairs per protein.
- Independent groups: require sufficient observations in each group to estimate the declared contrast.
- Group-specific detection: preserve proteins strongly detected in one condition and missing in another for a separate detection analysis rather than manufacturing intensities.
- Single-peptide/proteotypic evidence: do not use a universal two-peptide deletion rule. Flag evidence strength and require stronger peptide concordance for final biomarker claims.

Freeze the filter before inspecting differential significance. Report how many proteins pass.

## QC sequence

QC has three linked levels:

1. Acquisition/run: scan counts, cycle time, FWHM, mass accuracy, RT prediction, signal, injection/acquisition metadata and DIA-NN warnings.
2. Identification/quantification: precursors and protein groups identified, q-value context, contaminants, missed cleavages, charge/length distribution, QuantUMS quality.
3. Matrix/study: missingness, intensity distributions, pair/replicate correlation, PCA/MDS, run-order drift, subject effects, batch-condition confounding and sample influence.

Use project/instrument baselines when available. Generic thresholds are screening aids, not pass/fail laws. A sample exclusion must have multiple supporting metrics, a documented cause or reproducible influence, and an analysis with/without the sample when borderline.

For paired clinical cohorts:

- put paired samples adjacent in heatmaps;
- draw arrows/segments between paired samples in PCA/MDS;
- inspect within-subject correlations and within-subject log2 differences;
- run leave-one-subject-out influence analyses for final candidates;
- do not use the same subject in both training and validation folds.

## Differential analysis

Read [statistics.md](statistics.md). The usual protein-level primary analysis is limma on the log2 normalized matrix with subject/patient and condition in the same design. Use DEqMS as a sensitivity or primary method only when the feature-count definition is defensible for DIA.

Do not feed visualization-imputed values into the primary model. For proteins with condition-dependent detection, run a separate paired binary analysis and report them as detection differences unless a censored-intensity model is justified.

## Biological interpretation

- Rank the full tested set by the signed moderated statistic for GSEA.
- For over-representation analysis, use the tested proteins as background, not the entire genome.
- Resolve one-to-many protein-group-to-gene mappings explicitly. Do not silently duplicate one group into several independent gene observations.
- Interpret pathway concordance before isolated protein hits.
- Validate final candidates at precursor level: multiple proteotypic precursors should support the direction, and oxidized/acetylated variants should not be the sole driver.

## Recommended figures

1. Cohort/sample flow and exclusion diagram.
2. Run-order panels for identifications, missingness, mass accuracy/FWHM, and signal/quality.
3. Raw and DIA-NN-normalized log2 distributions shown separately when raw quantities are available.
4. Pair-aware PCA/MDS and sample correlation heatmap with metadata bars.
5. Missingness versus abundance and group-specific detection plots.
6. MA plot and volcano/treat plot with FDR and effect uncertainty.
7. Paired slope plots for selected proteins.
8. Within-subject delta heatmap or waterfall plot.
9. GSEA summary plus leading-edge heatmaps.
10. Candidate precursor-concordance panels.

## References

- DIA-NN: https://doi.org/10.1038/s41592-019-0638-x
- QuantUMS: https://doi.org/10.1038/s41587-026-03131-2
- DIA workflow benchmarking: https://doi.org/10.1038/s41467-024-47899-w
- limma: https://doi.org/10.1093/nar/gkv007
- DEqMS: https://doi.org/10.1074/mcp.TIR119.001646
- DEqMS DIA protocol: https://doi.org/10.1038/s41596-026-01349-7
- Missing-value mechanisms: https://doi.org/10.1021/acs.jproteome.5b00981
