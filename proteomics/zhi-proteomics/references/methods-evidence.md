# Methods evidence and transfer boundaries

Reviewed 2026-09-09. This is a methods adaptation register, not a claim that a highly cited paper validates every configuration in this skill. Store any later adopted implementation's exact version and benchmark evidence. Do not copy article prose or original data into the skill.

| Source | Methods detail checked | Adopt as a principle | Do not generalize |
| --- | --- | --- | --- |
| Peng et al., Nature Communications 2024, https://doi.org/10.1038/s41467-024-47899-w | varied matrix construction, normalization, imputation and testing; DIA-NN 1.8.1 | assess the whole pipeline; compare a small prespecified set of defensible workflows | a benchmark-winning imputation/summarizer is not a proven optimum for DIA-NN 2.6.x paired clinical tissue; do not chase the largest discovery count |
| Grossmann et al., Nature Biotechnology 2026, https://doi.org/10.1038/s41587-026-03131-2 | feature signal quality informs bias/uncertainty; data-dependent QuantUMS training | retain quality information and exact training/quantification provenance | quality scores are not automatically calibrated limma weights; paper publication year is not search-engine version |
| Bekker-Jensen et al., Nature Communications 2020, https://doi.org/10.1038/s41467-020-14609-1 | mode-specific localization; dedicated phospho/nonphospho/protein stoichiometry modeling | separate site localization, abundance and occupancy evidence; benchmark mapping/localization | Spectronaut-era localization and imputation thresholds are not universal DIA-NN defaults |
| Steger et al., Nature Communications 2021, https://doi.org/10.1038/s41467-021-25454-1 | CAA chemistry, K-GG enrichment, peptide/site mapping, time-resolved proteome and ubiquitinome | chemistry before search; separate biological time and matched protein evidence | simultaneous protein/site changes do not prove degradation; do not transplant old re-inference or normalization code |
| Dai et al., Nature Methods 2024, https://doi.org/10.1038/s41592-024-02343-1 | SDRF-driven design, separate predicted/empirical library stages, MSstats outputs | explicit sample hierarchy, pipeline provenance and reusable stage boundaries | cloud/HPC infrastructure is not required for every personal-PC project |
| Wu and Smyth, NAR 2012, https://doi.org/10.1093/nar/gks461 | CAMERA accounts for inter-gene correlation | assess gene-set dependence and declare the null being tested | a fixed cameraPR correlation sensitivity is not an empirical estimate of all within-set correlations |

## Public skills and engineering references

- GPTomics/bioSkills: https://github.com/GPTomics/bioSkills/tree/main/proteomics — topic routing and examples; archived 2026-08-15, retained as historical reference, not an updating dependency.
- ClawBio proteomics-de: https://github.com/ClawBio/ClawBio/tree/main/skills/proteomics-de — runnable demo and report/provenance packaging; default downshift imputation/two-group assumptions are not adopted for clinical paired DIA.
- K-Dense proteomics-scientist: https://github.com/K-Dense-AI/scientific-agents/tree/main/scientific-agents/proteomics-scientist — acquisition/evidence-layer reasoning; agent instructions are not method validation.
- quantmsdiann: https://github.com/bigbio/quantmsdiann — version-specific stages, SDRF, blocked flags and test profiles. A workflow repository is not an AI skill; borrow engineering contracts deliberately.

## Required evidence record for future method additions

Record DOI/URL, publication date, exact Methods section, acquisition and enrichment type, engine/version, matrix unit, biological design, missingness approach, tested null/FDR family, validation dataset, limits on transfer, and local implementation test status. Distinguish author recommendation, method benchmark and this project's adopted decision.

Missingness alternatives must use their current official API and accommodate the study design. proDA documentation: https://bioconductor.org/packages/release/bioc/html/proDA.html . MSstats, msqrob2 and PTM-specific methods remain alternatives, not automatic substitutions when a first analysis has no discoveries.
