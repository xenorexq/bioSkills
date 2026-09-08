# DIA K-GG ubiquitinome workflow

Use this reference for anti-K-ε-GG/diGly-enriched DIA data. The direct measurement is a K-GG-modified peptide/site, not a ubiquitin linkage mechanism or protein degradation event.

## Chemistry contract

Confirm before analysis:

- enrichment reagent/lot and whether the protocol targets K-GG remnants;
- alkylation reagent: iodoacetamide can create a +114.0429-Da lysine artifact; chloroacetamide is preferred for avoiding this confound;
- input amount, enrichment batch, digestion protocol, protease inhibitor/proteasome inhibitor exposure, and whether samples were pooled or fractionated;
- matched unenriched whole-proteome material from the same biological samples/aliquots;
- disease or perturbation contexts that alter ISG15 or NEDD8.

Anti-K-GG enrichment is not absolutely ubiquitin-specific. Ubiquitin, NEDD8, and ISG15 can leave the same lysine diglycine remnant after tryptic digestion. Report the measurement as K-GG/diGly unless orthogonal evidence supports ubiquitin specificity.

K-GG profiling detects lysine-linked remnants and ubiquitin-chain linkage peptides at K6, K11, K27, K29, K33, K48, and K63 when observed. It does not by itself quantify M1/linear ubiquitination.

## DIA-NN search contract

Use a dedicated K-GG search/library and the two-stage DIA-NN workflow in [diann-2.6.md](diann-2.6.md).

- Add UniMod:121 (+114.042927 Da) on K as the biological variable modification.
- Account for the modified lysine's blocked tryptic cleavage and document the missed-cleavage/search-space choice.
- Limit unrelated variable modifications.
- Use peptidoform/proteoform scoring and preserve precursor, peptidoform, protein-group, and localization confidence fields.
- Retain `Protein.Sites`, localization probabilities, modified sequence, charge, and all protein mappings.

Do not transfer whole-proteome protein-group filtering rules directly to K-GG sites. The central units are modified peptidoforms and localized lysine sites.

## Site table

A stable K-GG site key should contain:

`leading accession | gene | K position | UniMod:121 | peptidoform`

Retain ambiguous mappings and isoform-specific coordinates rather than collapsing them silently. Separate:

- localized single-site peptidoforms;
- multiply modified peptidoforms;
- ubiquitin-chain linkage peptides;
- sites mapping to NEDD8/ISG15 or ambiguous paralogs;
- K-GG sites without matched parent-protein quantification.

## QC

Report:

- enrichment yield and percentage of quantified precursors carrying K-GG;
- localized K-GG site counts at exploratory and stringent thresholds;
- input/enrichment-batch effects, K-GG completeness and missingness versus abundance;
- replicate/pair correlations and run-order behavior;
- charge, length, missed-cleavage and localization distributions;
- K-GG sites per protein and chain-linkage peptide signals;
- overlap/mapping rate to the matched whole proteome;
- ISG15/NEDD8 markers and known pathway context when relevant.

Do not interpret a low K-GG/total-protein overlap as automatic failure: enriched modified peptides and global protein digests have different detectability. Investigate systematic sample/batch differences and mapping errors.

## Differential endpoints

Read [statistics.md](statistics.md). Produce distinct results:

1. K-GG DPA: change in localized K-GG peptide/site abundance.
2. K-GG DPU: change relative to matched parent-protein abundance.
3. Protein abundance: whole-proteome change.
4. Detection shift: paired presence/absence evidence when quantitative modeling is unsupported.

Both DPA and DPU can be biologically meaningful. Label them accurately. DPU is an occupancy/usage proxy, not absolute stoichiometry.

Prefer msqrob2PTM for transparent abundance/usage and peptidoform-level modeling in complex or missing datasets. MSstatsPTM is an alternative when its DIA-NN converter and model are compatible; audit observation counts and the model used for each feature.

## Mechanistic integration

Use time and direction carefully:

- early K-GG increase followed by later parent-protein decrease can support a degradation hypothesis;
- simultaneous K-GG and protein changes in a cross-sectional cohort cannot establish degradation;
- K-GG decrease does not prove deubiquitinase activation;
- E3/DUB enrichment or interaction supports a hypothesis but does not prove a direct enzyme-substrate pair.

For E3/DUB/substrate prioritization, combine K-GG DPA/DPU, whole-proteome change, curated physical interactions, perturbation/temporal evidence, subcellular localization, and known degrons. Report which evidence types are direct versus inferred.

## Recommended figures

1. K-GG enrichment/localization yield funnel.
2. Run-order and enrichment-batch QC.
3. Pair-aware PCA and missingness plots.
4. K-GG DPA versus DPU scatter with parent-protein change.
5. Chain-linkage peptide profile.
6. Site-level paired slope plots with parent-protein panel.
7. E3/DUB–substrate network limited to evidence-backed candidates.
8. Protein–K-GG quadrant plot; add time ordering when available.
9. Peptidoform and XIC/spectrum evidence for final sites.

## References

- DIA ubiquitinome/circadian workflow: https://doi.org/10.1038/s41467-020-20509-1
- DIA-NN K-GG and USP7 workflow: https://doi.org/10.1038/s41467-021-25454-1
- K-GG enrichment: https://doi.org/10.1038/nbt.1654
- Iodoacetamide artifact: https://doi.org/10.1038/nmeth.1208
- UbiSite specificity: https://doi.org/10.1038/s41594-018-0084-y
- MSstatsPTM: https://doi.org/10.1016/j.mcpro.2022.100477
- msqrob2PTM: https://doi.org/10.1016/j.mcpro.2023.100708
