# DIA phosphoproteome workflow

Use this reference for phosphopeptide-enriched DIA data. Treat enrichment, identification, localization, abundance, and usage as separate evidence layers.

## Required inputs

- phosphopeptide-enriched DIA-NN raw outputs and log;
- matched sample metadata and enrichment batch/plate information;
- FASTA and phosphorylation search configuration;
- ideally, a matched unenriched whole-proteome measurement from the same biological samples or aliquots;
- the DIA-NN main report and site report with modification-aware q-values and localization fields.

If no matched whole proteome exists, differential phosphosite abundance can still be analyzed, but protein-adjusted differential usage cannot be claimed.

## Search and identification contract

Use a dedicated phosphoproteome search/library. Include phosphorylation on S/T/Y and only justified companion variable modifications. The large modified search space makes peptidoform confidence and localization filters essential.

For DIA-NN 2.6+, follow the two-step predicted-library/raw-analysis workflow in [diann-2.6.md](diann-2.6.md). Use the current peptidoform/proteoform scoring recommended for PTM-focused data and preserve:

- precursor and protein-group q-values in the selected run/global/library context;
- `Peptidoform.Q.Value` and the applicable global/library peptidoform q-value;
- `PTM.Site.Confidence` and, with MBR, `Lib.PTM.Site.Confidence`;
- `Site.Occupancy.Probabilities` and `Protein.Sites`;
- the site report and all mappings from precursor to peptidoform to protein residue.

Do not borrow a MaxQuant class-I threshold without documenting that DIA-NN's localization probability has a different calibration. Use a predeclared exploratory and stringent localization threshold, report both yields, and use an empirical FLR/entrapment check when the claim is high-stakes.

## Site identity

A site key is distinct from its evidence key:

- `site_id = FASTA version/hash | accession/isoform | residue | position | modification`
- `peptidoform_id = fully modified peptide sequence` under a recorded modification convention
- `precursor_id = peptidoform_id | charge` (add channel when multiplexed)

Use a separate precursor-to-site mapping table. Gene names are annotation, not immutable identity. Different charges, missed-cleavage peptides or co-modified forms can support the same site without creating multiple unique sites. A row retaining all these fields is an evidence record, not a distinct site count. Do not sum overlapping evidence blindly.

Retain all candidate protein mappings. Do not collapse ambiguous isoform positions into one site. For multiply modified peptides, retain the peptidoform and the contribution of each localized site; a second modification can drive a peptidoform change attributed to the phosphosite.

## QC

Report:

- enrichment yield and fraction of modified precursors;
- localized-site counts at each localization threshold;
- S/T/Y proportions and singly versus multiply phosphorylated peptidoforms;
- precursor/peptidoform/site completeness and missingness versus abundance;
- replicate or pair correlations at precursor, peptidoform, and site level;
- enrichment-batch and run-order effects;
- distribution of localization confidence, quantity quality, charge, peptide length, and missed cleavages;
- overlap and mapping rate to the matched whole proteome.

Do not compare TiO2, Fe-IMAC, or other enrichment chemistries as if they sampled the same phosphoproteome. Chemistry differences are a technical factor unless deliberately part of the design.

## Differential analysis

Read [statistics.md](statistics.md).

Produce both endpoints when possible:

1. DPA: differential abundance of localized phosphopeptides/sites.
2. DPU: differential usage after accounting for parent-protein abundance.

Prefer peptidoform-aware models for multiply modified peptides and complex missingness. msqrob2PTM distinguishes abundance from usage and exposes observation/model structure. MSstatsPTM supports DIA-NN conversion, but always verify the installed function signatures; current documentation uses `DIANNtoMSstatsPTMFormat`, `dataSummarizationPTM`, and `groupComparisonPTM` with separate PTM and protein label-type arguments.

Never call an adjusted log-ratio absolute occupancy unless a stoichiometry-calibrated experiment supports that claim.

## Kinase and pathway inference

- Rank all adequately localized tested sites; do not use only significant sites.
- Use curated site-specific signatures such as PTMsigDB/PTM-SEA and a kinase-substrate method such as KSEA.
- Report the substrate database version, substrate count, coverage, enrichment statistic, and FDR.
- Use an experiment-matched phosphosite background for motif analysis, preserving central residue and identified-protein composition.
- A kinase score is an activity hypothesis. Cross-check kinase abundance, activation-loop sites, phosphatases, localization, and known perturbations.

## Candidate evidence

A strong phosphosite candidate has:

- high localization confidence under the predeclared threshold;
- adequate independent subjects/replicates and no single-subject dependence;
- consistent supporting peptidoforms/charge states;
- a clear DPA/DPU interpretation with matched parent protein where available;
- coherent pathway or kinase evidence;
- manual spectrum/XIC review or targeted PRM for final claims.

## Recommended figures

1. Localization-confidence and site-yield funnel.
2. Enrichment yield, missingness and run-order QC.
3. Pair-aware PCA at phosphosite or peptidoform level.
4. DPA versus DPU scatter, colored by parent-protein change.
5. Site-level paired slope plots with parent-protein panel.
6. Kinase activity heatmap/dot plot with substrate counts.
7. PTM-SEA enrichment curves and leading-edge site heatmap.
8. Sequence logos against a matched background.
9. Peptidoform decomposition for multiply modified candidates.

## References

- Library-free DIA phosphoproteomics: https://doi.org/10.1038/s41467-020-14609-1
- DIA-NN current PTM/output documentation: https://github.com/vdemichev/diann
- MSstatsPTM: https://doi.org/10.1016/j.mcpro.2022.100477
- msqrob2PTM: https://doi.org/10.1016/j.mcpro.2023.100708
- Functional phosphosite annotation: https://doi.org/10.1038/s41587-019-0344-3
