# Statistical design and differential analysis

Use this reference for whole-proteome and PTM differential testing. The design, experimental unit, and missingness contract take precedence over the software package.

## Define the hypothesis family

Before fitting models, state:

- experimental unit: independent patient/subject, animal, culture, or technical injection;
- response unit: protein group, precursor, peptidoform, localized site, or PTM usage;
- contrast and direction;
- covariates and random/fixed effects;
- protein/site inclusion rule;
- primary multiple-testing family;
- minimum effect, if the claim requires one;
- primary and sensitivity analyses.

Technical injections do not increase biological sample size. Repeated samples from one subject must stay together in validation folds.

## Metadata and design checks

Reject or pause a design when:

- subject/sample identifiers are duplicated or missing;
- paired conditions are absent or mislabeled;
- condition is fully confounded with batch, acquisition date, enrichment plate, or instrument;
- the model matrix is rank deficient;
- the proposed covariate count is excessive for the number of independent subjects;
- treatment between longitudinal samples changes the scientific meaning of the contrast and is undocumented.

Prefer modeling known batch effects in the same inferential model. Use batch-removal functions only to create explicitly labeled visualization matrices, never as automatic preprocessing for the test.

## Whole-proteome model

For a paired protein-level matrix, a typical limma design is:

```r
design <- model.matrix(~ patient + condition, data = metadata)
fit <- limma::lmFit(log2_matrix, design)
fit <- limma::eBayes(fit, trend = use_trend, robust = TRUE)
result <- limma::topTable(fit, coef = "conditionRecurrent",
                          number = Inf, adjust.method = "BH")
```

Verify the actual coefficient name and sign. `trend=TRUE` is often useful for label-free intensity data when the mean-variance trend remains after summarization; inspect the trend rather than declaring it mandatory.

For an explicit minimum effect, apply `limma::treat` to the fitted contrast and use `topTreat`. Do not present an arbitrary post-hoc fold-change cutoff as if it were part of the FDR-controlled test.

DEqMS is appropriate when the count used by its variance model reflects the number of quantified mass-spectrometry features supporting each protein. For DIA, derive and document the precursor/peptide-count definition; do not substitute a convenient annotation count without checking it. Current DIA support is described in https://doi.org/10.1038/s41596-026-01349-7.

## Missingness

DIA missingness can contain several mechanisms: low-abundance censoring, interference/quality filtering, library/search effects, sample failure, and approximately random gaps. Diagnose rather than label the entire dataset MCAR or MNAR.

Primary options:

1. Test observed log2 values after a design-aware completeness rule and report the number of informative subjects per feature.
2. Use a feature-level model that handles missingness and repeated structure when its assumptions and converter are compatible with the data.
3. Analyze paired detection status separately for features with strong condition-dependent presence/absence.

Do not use imputation to create evidence for the primary p-value. Median/KNN/minimum/downshifted imputation may be used for a labeled visualization or pre-specified sensitivity analysis. Compare effect direction, ranking, and influential subjects across analyses.

For paired binary detection, use an exact McNemar-type test when counts permit and BH-correct the declared family. Do not assign an artificial fold change to a feature never quantified in one condition.

## PTM abundance and usage

Report two distinct endpoints when the matched whole proteome is available:

- differential PTM abundance (DPA): change in the modified peptide/site signal;
- differential PTM usage (DPU): change relative to the parent-protein abundance.

Both can be biologically meaningful. DPU is closer to a modification-usage or occupancy proxy but is not absolute stoichiometry.

For complex, paired, or missing PTM datasets, prefer a transparent peptidoform/site model such as msqrob2PTM and inspect observation counts and fit failures. MSstatsPTM is an alternative when its current DIA-NN converter and matched protein/PTM inputs are compatible; inspect which model was used for every significant feature because missingness can trigger simpler models.

Relevant methods:

- MSstatsPTM: https://doi.org/10.1016/j.mcpro.2022.100477
- msqrob2PTM: https://doi.org/10.1016/j.mcpro.2023.100708

## Multiplicity and reporting

- Use BH FDR within the predeclared feature family. If whole, phospho, and K-GG analyses are separate biological screens, report their FDR families separately.
- Report effect estimate, standard error or confidence interval, raw p-value, adjusted p-value, observation count, informative-subject count, localization threshold, and parent-protein availability.
- Plot the p-value distribution, mean-variance relation, residuals for representative features, and significance versus observation count.
- Use leave-one-subject-out influence analysis for clinical paired cohorts and flag results driven by one subject.
- Distinguish confirmatory from exploratory contrasts. Do not choose the primary model after inspecting which version gives more discoveries significant hits.

## Biomarker and machine-learning boundary

Do not build a clinical prediction claim from a small discovery cohort. If modeling is authorized and sample size is adequate:

- split and cross-validate by patient/subject;
- perform all filtering, imputation, scaling, and feature selection inside training folds;
- use nested cross-validation for tuning;
- report calibration and uncertainty, not AUROC alone;
- require an independent external cohort before a biomarker claim.

## Core references

- limma: https://doi.org/10.1093/nar/gkv007
- DEqMS: https://doi.org/10.1074/mcp.TIR119.001646
- DIA workflow benchmarking: https://doi.org/10.1038/s41467-024-47899-w
- Missing-value mechanisms: https://doi.org/10.1021/acs.jproteome.5b00981
- Nonignorable missingness: https://doi.org/10.1214/18-AOAS1144
