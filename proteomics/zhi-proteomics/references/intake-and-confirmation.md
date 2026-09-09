# Guided intake and confirmation

## Purpose and scope

This skill deliberately favors asking over guessing for study-specific facts and material analysis decisions. Be beginner-friendly without turning a one-sentence explanation into a compulsory interview. Ask comprehensively over the life of a real analysis, not all questions in a single wall of text. Follow the user's explicit scope and platform confirmation rules.

Use `../configs/question_bank.json` as a routed checklist. Each item carries a reason, conditional suggestion, mode, stage and unresolved-state policy. Translate naturally into the user's language. The bank supports Chinese and English; do not send raw JSON to a beginner.

## Interaction sequence

1. **Understand the task.** Does the user want an explanation, audit, plan, execution, rerun or preparation for a company? Identify whole, phospho, K-GG, or multi-ome. If uncertain, ask rather than selecting whole proteome because the file says pg_matrix.
2. **Extract available evidence.** Inspect existing metadata and the exact current log, not an old analysis plan. State what was read and from where. Offer this as a short prefilled summary, not as inferred clinical truth.
3. **Ask in rounds.** Usually 3–5 related questions: study/groups first; chemistry and acquisition next; search/quantification next; QC and inferential choices next; PTM/integration and outputs only when relevant. Adapt to user's answers and tempo. Do not ask unrelated PTM details of a whole-only study.
4. **Track uncertainty.** For each item keep `value`, `status`, `source`, and `asked`. Valid statuses are `unknown`, `documented`, `user_confirmed`, `proposed`, `conflicting`, `not_applicable`. Documented means an identified source supports that specific fact. `asked: true` means “do not repeat absent new evidence”, not “resolved”.
5. **Resolve mismatches.** If SOP says CAA alkylation but search evidence lacks expected fixed C, describe the discrepancy and ask for verification. Do not overwrite either source or silently add a modification. A log flag cannot confirm the wet-lab procedure.
6. **Confirm the plan.** Summarize scope, biological unit, conditions/contrast, exclusions, eligible proteins/sites, model, FDR family, effect rule, normalization/missingness, upstream warnings, outputs and pilot limitations. Ask whether to execute this concrete plan. A later change affecting the interpretation reopens the affected choice.

If the user supplies an already complete protocol, review it and confirm the unresolved essentials once. Do not re-ask every field. If the user says “you choose”, document exactly which proposed choices that approves; retain unknown chemistry, dates and clinical facts as unknown.

## Question wording

Use: **question → why it matters → how to find the answer or conditional suggestion → unknown is allowed**.

Example chemistry question:

“公司是否做过还原和烷基化？如果做过，用的是 IAA、CAA 还是其他试剂？这决定搜库中 C 的固定修饰。可以发样本制备 SOP；不知道也没关系，我会标为待确认，不按‘通常做过’处理。”

Example statistical question:

“你希望筛选的是队列平均差异，还是大多数患者同方向变化，还是两者都要？这是不同的问题。若没有预先方案，我建议分开交付；是否接受？”

Example FDR question:

“DIA-NN 的鉴定 q-value 和差异分析的 FDR 不是同一个阈值。差异检验若无预先方案，可以建议 BH FDR<0.05，并同时报告效应和区间；这只是候选方案。你有课题组／公司指定标准吗？”

Example interpretation check:

“你说的‘无修饰’是只做全蛋白组、不研究生物学 PTM，还是样本制备中也没有化学修饰？这两种含义不同。”

Do not quiz beginners on package arguments when a biological choice is sufficient. The assistant remains responsible for choosing an appropriate estimable implementation and explaining tradeoffs.

## Three separate confidence layers

Ask and store separately:

- identification: precursor/protein/peptidoform, run/global/library q-value context;
- site localization: probability/FLR definition, engine and version;
- differential analysis: raw P versus BH FDR, hypothesis family and minimum effect.

Neither “FDR 1%” nor “use default” is enough to determine all three layers. Never auto-promote one threshold into the others.

## Persistence and permission

When project-file creation is authorized, write `intake_state.json` and an `analysis_plan.json` into the new project output. Use `../configs/intake_state.example.json` for record shape. Never store real subjects or answers in this reusable skill. Read-only Q&A can maintain the same ledger in the conversation without creating files.

`scripts/intake_questions.py` prints missing items and the next question batch. It does not write answers, infer chemistry, validate the full design or authorize execution. Its stage-ready flag is only completeness for the listed core items; all contextual gates remain required.

Unknown answers should lead to a missing-information checklist and a targeted request to the laboratory when needed. Do not contact a company, publish data, install tools or rerun searches just because intake is complete.

## Before execution checklist

- Have all context-relevant questions been considered, including those outside the bank?
- Are logged settings distinguished from actual sample preparation?
- Is the research direction confirmed, not deduced only from specimen years?
- Is the statistical plan explicitly approved, with no proposed key choices silently accepted?
- If proceeding as pilot, is its restricted scope approved, while hard blocks remain enforced?
- Have user-declared unknowns been retained and avoided as invented covariates?
- Does the summary explain what the analysis will not establish?
