---
name: zhi-proteomics
description: Guide beginners through questions about samples, chemistry, DIA-NN settings and study design before auditing or analyzing DIA whole-proteome, phosphoproteome and K-GG ubiquitinome data. Use for DIA-NN logs, parquet/site reports, quantitative matrices, paired studies and matched PTM/protein integration. Preserve unknowns and ask for key decisions rather than silently choosing settings. Not a general DDA/TMT or metabolomics pipeline.
metadata:
  owner: Zhi
  version: "0.2.0"
  reviewed_at: "2026-09-09"
---

# Zhi Proteomics

Analyze DIA whole proteome, phosphoproteome, and K-GG ubiquitinome as related but distinct evidence layers. Preserve raw outputs, document every filter, and make the biological unit, confidence level, and comparison design explicit.

The user's instructions and study protocol take precedence over this skill. Do not infer permission to rerun searches, install software, alter source files, or publish data.

## Start Here

1. Identify the requested scope: explanation, read-only audit, planning, pilot, confirmed analysis, or raw-data rerun; and omics mode. A request to explain is not execution approval.
2. For any new study or changed sample/search/design context, read [intake-and-confirmation.md](references/intake-and-confirmation.md). Use its staged question bank. For a narrow conceptual question, answer directly and ask only what is necessary.
3. Read available files/logs first. Keep measured/documented facts, user confirmations, proposals, conflicts and unknowns separate. A search log describes search settings, not proof of sample chemistry.
4. Ask the relevant unanswered questions, with a short reason and conditional recommendation. Do not silently select study direction, chemistry, pairing, exclusions, FDR, effect size, missingness policy or normalization. A suggested/preselected answer is not consent. Stop before the affected computation until confirmed or explicitly authorized as a limited pilot.
5. Audit chemistry/search consistency before differential testing, using [preflight-and-provenance.md](references/preflight-and-provenance.md). Preserve original outputs; freeze the confirmed analysis plan with its unresolved items and permitted endpoints.
6. State the evidence unit: precursor, peptidoform, localized site, protein group, gene group, or pathway. Record software/build/schema versions; version 2.6.x guidance is not a guarantee of compatibility with every later release.

## Ask, Explain, Then Confirm

- Be proactive and comprehensive with beginners. Cover relevant sample preparation, digestion/alkylation, enrichment/PTMs, DIA-NN setup, grouping/repeats, QC and statistical choices across several short rounds (normally 3–5 related questions per message).
- Let users answer “unknown / 不知道”, supply a company SOP/log/screenshot instead, or ask for advice. Do not convert unknown into “no”, default, or confirmed. Do not repeatedly ask a question already answered without new contradictory evidence.
- Offer a reasoned proposal when the user does not know a statistical choice; label it proposed, not a scientific fact or universal requirement. Explain identification q-value versus differential BH FDR versus localization confidence.
- Before inferential execution or a rerun, present a plain-language plan summary and request explicit confirmation. An explicit instruction to use your proposed choices may approve choices, never invent sample facts or override an earlier “do not run”.
- Unknown clinical covariates need not block every descriptive pilot. Block only the affected endpoint; see the gate rules below. Never claim unknown batch is “no batch effect”.
- Persist intake answers and their sources in the authorized project output, not inside this shared skill. Use pseudonymous subjects; no patient data, tokens or project-specific sample IDs in the skill repository.

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

Classify each issue with evidence, version, affected endpoint, and resolution. See [preflight-and-provenance.md](references/preflight-and-provenance.md).

- **Block affected inference:** unresolved identity/direction conflict, non-estimable design, inadequate independent replication, missing PTM localization for site claims, or missing parent protein for DPU. Unaffected inventory/QC may continue if authorized.
- **Pilot only after explicit consent:** unresolved search warnings, chemistry uncertainty or unknown clinical/batch factors where limited observed-data exploration remains meaningful. Retain limitations; no causal, validated-biomarker or final search-validity claim.
- **Record and continue:** informational or out-of-scope messages with a documented explanation. WARNING text alone is not proof of a software bug; inspect the exact version and official resolution history.
- **Candidate downgrade:** sparse support or single-subject dependence limits that candidate, not automatically the whole study. Zero significant proteins is a valid output; never loosen thresholds to populate a list.

## Reusable Checks

- Run `scripts/inspect_diann_project.py <project-or-output-dir>` to inventory DIA-NN outputs, commands, warnings, matrix dimensions, contaminants, q-value fields, and decoy presence.
- Run `scripts/validate_paired_design.py metadata.csv --sample sample --subject patient --condition condition` before paired testing.
- Run `scripts/intake_questions.py --mode whole --stage analysis --state intake_state.json` to identify unresolved decisions and propose the next question round. It is a question selector, not an auto-approval engine.
- Use `scripts/evidence_contracts.py` for chemistry mass checks, cache fingerprints, distinct site/peptidoform/precursor keys and missing-aware common-change counts.
- Run `python -m unittest discover -s tests -v` after changing scripts. See [testing-and-release.md](references/testing-and-release.md) for statistical benchmark and behavioral evaluation boundaries.

These scripts are diagnostic. They do not modify source data.

For evidence supporting method choices and restrictions, read [methods-evidence.md](references/methods-evidence.md). Templates in `configs/` deliberately start unconfirmed; never treat them as an executable approved plan.

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
