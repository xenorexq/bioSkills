---
name: zhi-proteomics
description: Audit and analyze DIA-NN 2.6+ bottom-up DIA whole-proteome, phosphoproteome, and K-GG ubiquitinome projects, including search/output validation, mode-aware QC, paired or complex differential analysis, PTM localization, parent-protein adjustment, cross-ome integration, and publication-ready evidence tables and figures. Use for DIA-NN report.parquet, report-lib.parquet, matrix TSVs, site reports, or matched whole-proteome/PTM studies. Do not use for generic DDA/TMT/SILAC, top-down proteomics, metabolomics, or instrument acquisition design unless the user explicitly expands scope.
metadata:
  owner: Zhi
  version: "0.1.0"
  reviewed_at: "2026-09-08"
---

# Zhi Proteomics

Analyze DIA whole proteome, phosphoproteome, and K-GG ubiquitinome as related but distinct evidence layers. Preserve raw outputs, document every filter, and make the biological unit, confidence level, and comparison design explicit.

The user's instructions and study protocol take precedence over this skill. Do not infer permission to rerun searches, install software, alter source files, or publish data.

## Start Here

1. Identify the requested mode: search audit, whole proteome, phosphoproteome, K-GG ubiquitinome, or cross-ome integration.
2. Inventory the exact DIA-NN version, command/pipeline, FASTA, modifications, quantification mode, output files, and sample metadata before interpreting counts.
3. Preserve original outputs. Write derived matrices and reports to new paths with a manifest of transformations.
4. Lock the biological design before testing: sample identity, subject/patient, condition, pairing, batch, acquisition order, treatment history, and exclusions.
5. State the analysis unit in every result: precursor, peptidoform, localized site, protein group, gene group, or pathway.

For a DIA-NN run or output question, read [references/diann-2.6.md](references/diann-2.6.md).

For whole-proteome analysis, read [references/whole-proteome.md](references/whole-proteome.md) and [references/statistics.md](references/statistics.md).

For phosphoproteomics, read [references/phosphoproteome.md](references/phosphoproteome.md) and [references/statistics.md](references/statistics.md).

For K-GG ubiquitinomics, read [references/ubiquitinome.md](references/ubiquitinome.md) and [references/statistics.md](references/statistics.md).

For matched multi-ome interpretation or final figures, read [references/integration-reporting.md](references/integration-reporting.md).

For the source audit that produced this skill, read [references/upstream-audit.md](references/upstream-audit.md).

## Non-Negotiable Evidence Contracts

- Do not equate precursor FDR, peptidoform FDR, protein-group FDR, and site-localization confidence. Name each level and context.
- Do not assume DIA missingness is MCAR. Diagnose intensity dependence and group dependence; retain missingness as evidence.
- Do not add a second normalization merely because a matrix is log transformed. DIA-NN `.Normalised` and `.MaxLFQ` quantities are already normalization-dependent outputs.
- Do not treat imputed values as observations in the primary statistical analysis. If imputation is used for a visualization or sensitivity analysis, label it and keep the primary inference separate.
- Do not call a phosphosite or K-GG site "differential usage/occupancy" unless parent-protein abundance was incorporated. Without it, call the result differential modified-peptide/site abundance.
- Do not treat K-GG as uniquely ubiquitin-derived: NEDD8 and ISG15 can leave the same remnant, and alkylation chemistry must be checked.
- Do not infer a kinase, E3 ligase, DUB, substrate relationship, or degradation mechanism from enrichment alone. Report these as hypotheses unless supported by curated interaction, temporal, perturbation, and parent-protein evidence.
- Do not use random train/test splitting when samples from the same patient or subject can cross folds.

## Default Analysis Choices

- Use protein groups for DIA-NN whole-proteome reporting; retain group membership and proteotypic evidence.
- Use a subject/patient term for paired or repeated designs. Add batch as a model covariate only when it is estimable and not fully confounded with biology.
- Use limma for a protein-level log2 matrix; use DEqMS when a defensible per-protein quantified-feature count is available; use feature-level mixed models when the experiment requires them.
- For PTMs, distinguish differential abundance from differential usage. Prefer transparent site/peptidoform models that expose observation counts and model failures.
- Correct multiplicity with BH FDR for the declared family of hypotheses. Use `limma::treat` when a minimum effect is part of the scientific claim.
- Rank the full tested universe for GSEA; use the actually tested proteins/sites as the background for over-representation analysis.

## Quality Gates

Stop and report rather than silently continuing when:

- sample identity, condition, or pairing is ambiguous;
- a condition is fully confounded with acquisition batch;
- a DIA-NN warning affects the selected workflow;
- the requested PTM analysis lacks localization fields or the modification cannot be identified in the report schema;
- too few independent biological subjects remain for the proposed model;
- parent-protein adjustment is requested but no matched whole-proteome evidence exists;
- a claimed site cannot be mapped unambiguously to a protein residue;
- a significant result is supported by too few observations or one influential subject.

## Reusable Checks

- Run `scripts/inspect_diann_project.py <project-or-output-dir>` to inventory DIA-NN outputs, commands, warnings, matrix dimensions, contaminants, q-value fields, and decoy presence.
- Run `scripts/validate_paired_design.py metadata.csv --sample sample --subject patient --condition condition` before paired testing.

These scripts are diagnostic. They do not modify source data.

## Deliverables

For a completed analysis, return:

- an immutable input manifest and software/parameter record;
- validated sample metadata and documented exclusions;
- filtered whole-proteome and/or localized PTM matrices with transformation logs;
- QC tables and figures before and after any authorized normalization;
- complete differential tables with effect, uncertainty, FDR, observation count, and evidence flags;
- pathway and regulator results with tested universe and database versions;
- candidate-level peptide/site/protein concordance plots;
- a concise limitations section separating measured evidence from mechanistic inference.
