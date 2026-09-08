# GPTomics proteomics skill audit

Audit date: 2026-09-08

Upstream: https://github.com/GPTomics/bioSkills/tree/main/proteomics

Commit: `d91ed3d563019e649dc854c56ccd62551359488a`

Repository state: archived read-only by the owner on 2026-08-15.

The audit covered every `SKILL.md`, usage guide, and example file in all nine directories. Python examples compile, the shell example passes `bash -n`, and the R example parses. Syntax success does not validate scientific assumptions or current software flags.

## Verdict summary

| Upstream skill | Verdict | Retain | Rewrite or remove |
| --- | --- | --- | --- |
| `dia-analysis` | Strong foundation, major update required | q-value level/context, output inventory, acquisition-aware reasoning | Its one-command predicted-library example conflicts with DIA-NN 2.6 guidance to separate prediction from raw analysis; MBR/Lib and peptidoform filters are incomplete; `smart-profiling`, output naming, and matrix-filter claims must be verified per installed version; do not call raw directDIA the default for this workflow. |
| `data-import` | Partial retain | format detection, immutable inputs, contaminant/decoy removal, zero-to-missing conversion | The statement "DIA is closer to MCAR" is too broad; DIA missingness remains abundance- and scoring-dependent. DIA-NN filtering ignores Global/Lib contexts, peptidoform localization, and the ready-to-use matrix contract. MaxQuant dominates a skill intended for DIA. |
| `protein-inference` | Reference only | protein groups are inferred; retain group membership and proteotypic evidence | DIA-NN already performs inference and q-value calculation. Re-inferring with a toy parsimony algorithm is unsafe. "Two-peptide rule is wrong" and "quantify only unique peptides" are overgeneralized; peptide-count requirements belong to candidate confidence/sensitivity analyses, not universal filtering. |
| `peptide-identification` | Archive from default workflow | q-value versus PEP; separate ID levels; entrapment awareness | Mostly DDA database-search content. Hand-rolled FDR examples omit conservative corrections and engine-specific competition details. It should not route routine DIA-NN whole/PTM analysis. |
| `proteomics-qc` | Strong retain, substantial rewrite | three-layer QC, inspect acquisition/search/matrix together, use project baselines, document exclusions | Universal correlation/CV/ID thresholds are not portable. Automatic ComBat advice is unsafe under confounding. Summed MaxLFQ intensity and contaminant fractions are not absolute composition measurements. Add DIA-NN stats, QuantUMS quality, localization, enrichment yield, pair-aware QC, and influence analysis. |
| `quantification` | Split and narrow | distinguish raw/normalized/MaxLFQ; report summarization; preserve NA | TMT/SILAC material is out of scope. Do not median-center an already normalized DIA-NN matrix by default. "Always compare two summarizers" and "summarizer changes the answer more than the test" are not universal requirements. Add QuantUMS quality fields and separate whole-proteome from modified-peptide/site quantification. |
| `differential-abundance` | Strong retain, redesign around study design | limma/DEqMS, BH, `treat`, batch in model, no inferential use of visualization imputation | Its Python fallback only supports independent groups and would silently mishandle paired data. `trend=TRUE` is useful but not universally mandatory. Missingness is not uniformly MNAR. PTM analyses need differential abundance versus differential usage and parent-protein matching. |
| `spectral-libraries` | Optional niche reference | library provenance, modification compatibility, external-library QC | Manual iRT/CCS calibration is not a universal prerequisite for DIA-NN's built-in predicted-library workflow; DIA-NN performs run calibration. External Koina/Prosit/NCE tuning adds complexity not needed by default. Retain only for third-party, empirical, GPF, or conversion workflows. |
| `ptm-analysis` | Strong concepts, split into two modes | localization distinct from ID; K-GG ambiguity; matched background; parent-protein context; regulator priors | MaxQuant-specific multiplicity code is not a DIA-NN site pipeline. Current MSstatsPTM arguments differ from the example. "Only adjusted hits are regulated" conflates differential PTM abundance with differential usage; both are valid but answer different questions. Add msqrob2PTM, DIA-NN 2.6 site outputs, observation-count gates, and separate phospho versus K-GG contracts. |

## Cross-cutting problems

1. The skills repeat long generic explanations and thresholds, increasing context cost and conflict risk.
2. Several claims are written as absolutes even when they depend on instrument, software version, enrichment chemistry, cohort design, or biological question.
3. Many references are useful, but exact software calls are not pinned to a reproducible environment.
4. Whole proteome, phosphoproteome, and ubiquitinome are treated as variants of one matrix instead of distinct evidence layers with different localization and chemistry contracts.
5. There is no end-to-end matched-sample contract for parent-protein adjustment and cross-ome interpretation.
6. There is no strict patient/subject leakage guard for paired clinical cohorts or biomarker models.

## Evidence used for modernization

- DIA-NN current documentation: https://github.com/vdemichev/diann
- QuantUMS: https://doi.org/10.1038/s41587-026-03131-2
- DIA differential workflow benchmarking: https://doi.org/10.1038/s41467-024-47899-w
- DEqMS DIA protocol: https://doi.org/10.1038/s41596-026-01349-7
- MSstatsPTM: https://doi.org/10.1016/j.mcpro.2022.100477
- msqrob2PTM: https://doi.org/10.1016/j.mcpro.2023.100708
- DIA phosphoproteomics: https://doi.org/10.1038/s41467-020-14609-1
- DIA ubiquitinomics: https://doi.org/10.1038/s41467-021-25454-1 and https://doi.org/10.1038/s41467-020-20509-1
- K-GG alkylation artifact: https://doi.org/10.1038/nmeth.1208

## Resulting architecture

One discoverable `zhi-proteomics` skill routes to focused references for DIA-NN, whole proteome, phosphoproteome, ubiquitinome, statistics, and integration. This consolidates shared invariants while loading mode-specific detail only when needed. DDA/TMT/SILAC, generic protein inference, and external-library engineering are intentionally outside the default scope.
