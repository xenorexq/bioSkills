# Cross-ome integration and reporting

Use this reference when matched whole proteome, phosphoproteome, and/or K-GG ubiquitinome data are analyzed together.

## Integration unit

Keep the measurement hierarchy explicit:

`run -> precursor -> peptidoform -> localized site -> protein group/accession -> gene -> pathway`

Do not duplicate one ambiguous protein group into several independent genes or treat several peptidoforms from one site as independent biological replicates. Preserve mapping multiplicity and the number of observations contributing to each summary.

Match datasets by biological sample/aliquot, subject, condition, time, and batch. Never join only on shortened sample names without a validated mapping table.

## Whole protein versus PTM

For every matched site and parent protein, keep both unadjusted abundance and protein-adjusted usage results.

| Parent protein | PTM site | Interpretation |
| --- | --- | --- |
| unchanged | changed | PTM-specific regulation/usage hypothesis |
| same direction, similar magnitude | changed | likely protein-abundance-driven PTM abundance |
| changed | stronger/opposite site change | combined abundance and PTM-usage effect |
| missing parent protein | changed site | DPA only; DPU unavailable |

These are interpretations, not mechanistic proof. Protein-adjusted values are relative usage proxies, not absolute occupancy.

For K-GG, a contemporaneous site increase plus protein decrease does not prove degradation. Time-resolved K-GG increase preceding protein loss, together with perturbation and E3/DUB evidence, is stronger.

## Pathways and regulators

- Use whole-proteome signed moderated statistics for protein GSEA.
- Use localized phosphosite statistics for PTM-SEA/KSEA.
- Use K-GG site statistics for ubiquitin-system enrichment and curated E3/DUB/substrate hypotheses.
- Compare pathway directions across layers using matched, versioned gene/site sets.
- Use the tested universe appropriate to each layer. Do not use the whole proteome as the phosphosite-site background.
- Correct multiple testing separately for clearly distinct hypothesis families, then label the family in every result.

Declare whether the gene-set test is preranked/gene-resampling, sample/subject-resampling, competitive or self-contained. Preserve patient structure in any sample-label permutation and choose the appropriate null; do not shuffle paired samples independently. Assess inter-gene correlation with a design-compatible method such as CAMERA/ROAST or an explicitly justified sensitivity. A fixed cameraPR correlation of 0.01 is an assumption, not a measured solution to all correlation.

Report leading-edge membership, set overlap/redundancy, contributing patient coverage and leave-one-subject-out stability for central pathway claims. Distinguish statistical enrichment from enzyme activity or a mechanism. Single-protein nonsignificance and pathway enrichment can coexist, but pathways are not a rescue strategy to claim success after a negative primary analysis. References: https://doi.org/10.1093/nar/gks461 and `methods-evidence.md`.

## Patient/subject heterogeneity

For paired or longitudinal cohorts, calculate subject-level deltas for each layer. Use pathway-level deltas before high-dimensional sample clustering when the cohort is small.

Relate heterogeneity to pre-specified clinical variables such as treatment, recurrence interval, disease etiology, tumor purity, and clonality. Do not infer a stable molecular subtype from a small cohort without resampling stability and external validation.

## Candidate evidence table

Build one row per candidate protein/site with:

- identifier and mapping ambiguity;
- whole-proteome effect, standard error, FDR, observation count and influence flag;
- phosphosite DPA and DPU, localization confidence and supporting peptidoforms;
- K-GG DPA and DPU, localization confidence, chain-linkage or UBL ambiguity flags;
- QuantUMS/site quantity quality where available;
- pathway/regulator evidence with database version;
- external-cohort direction;
- manual XIC/spectrum review and targeted validation status;
- final interpretation and explicit limitation.

Use evidence tiers, not a single opaque score. A candidate should not become "high confidence" solely because several correlated analyses reuse the same measurements.

## Visualization set

Use a compact figure system:

1. Sample and aliquot flow across the three omes.
2. Shared run-order QC with separate enrichment-specific panels.
3. Pair-aware PCA/MDS for each layer.
4. Protein effect versus phosphosite/K-GG DPA and DPU quadrant plots.
5. Subject-level pathway-delta heatmap across layers.
6. Kinase and E3/DUB hypotheses with substrate counts and evidence type.
7. Candidate panels combining protein, site, peptidoform and patient-level trajectories.

Avoid dense PPI hairballs, unlabeled Venn diagrams, and heatmaps selected only by the smallest p-values. Every figure must state the analysis unit, transformation, number of independent subjects, missing-value handling, and FDR family.

## Reproducibility

Record software/package versions, database releases, exact filters, random seeds, excluded samples, tested universes and mapping tables. Save complete results, not only significant rows. Keep a machine-readable manifest that links each figure/table to its input and command/script.

For biomarker prediction, use subject-grouped nested cross-validation and an external cohort. Small discovery cohorts support hypothesis generation, not a clinical performance claim.
