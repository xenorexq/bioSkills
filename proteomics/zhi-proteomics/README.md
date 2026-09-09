# Zhi Proteomics

## 中文简介

`Zhi Proteomics` 是一套以**分轮问询、证据核对和执行前确认**为起点的个人 Codex skill，面向 DIA 全蛋白组、磷酸化组和 K-GG/diGly 泛素组。尤其适合首次接触蛋白组学的用户。当前参考规范聚焦 DIA-NN 2.6.x；后续版本必须重新核对字段和参数，不承诺自动向前兼容。

## English overview

`Zhi Proteomics` is a question-first personal Codex skill for DIA whole-proteome, phosphoproteome and K-GG/diGly ubiquitinome projects, including beginners. It asks staged, explained questions, checks the evidence and confirms the plan before execution. Current guidance targets reviewed DIA-NN 2.6.x behavior; later versions require renewed schema/parameter review.

## 新手问询 / Beginner-guided intake

先从文件和日志提取已知内容，再按研究设计、样本制备、搜库、统计和交付分轮提问，通常一轮3–5个相关问题。问题附“为什么要问”和有条件的建议，允许回答“不知道”或直接提供公司SOP。已回答的问题不反复问，但新证据冲突时重新核对。

Inspect files/logs first, then ask short rounds about design, preparation, search, statistics and outputs. Each question explains its purpose and offers a conditional suggestion. “Unknown” and a laboratory SOP are valid responses. Do not repeat resolved questions unless evidence conflicts.

重点覆盖：物种和组织、保存、还原/烷基化（IAA/CAA）、酶切、全蛋白/PTM目标、富集、样本量、临床配对/技术重复、批次、DIA-NN版本、FASTA、修饰与搜索空间、谱库和MBR、评分/定量、各层q-value、旧缓存、QC排除、缺失值、覆盖要求、差异FDR、最小效应、共同变化、母蛋白和定位、输出与隐私。

Coverage includes species/material, preservation, reduction/alkylation, digestion, PTM goals/enrichment, amounts, pairing/technical repeats, batches, engine/build, FASTA/search space, libraries/MBR, scoring/quantification, confidence levels, cache, exclusions, missingness, coverage, differential FDR/effect, common changes, parent protein/localization and output/privacy.

**建议不等于确认，未知不等于没有，日志设置不等于实验事实。** 执行前汇总方案并请求确认；用户说“你来定”可授权明确提出的分析选择，但不能据此编造化学处理或临床事实。用户说“先不执行”则保持计划状态。

**A proposal is not confirmation; unknown is not absent; a search setting is not a wet-lab fact.** Confirm the summarized plan before execution. Delegating statistical choices does not supply missing chemistry/clinical facts, and a hold instruction remains binding.

详细问询协议 / Full interaction protocol: [`references/intake-and-confirmation.md`](references/intake-and-confirmation.md)

## 为什么重新设计 / Why it was redesigned

本 skill 基于对 GPTomics/bioSkills 仓库中 9 个 proteomics skills 的逐文件审查重新编写。上游仓库已于 2026-08-15 归档。原内容中的 q-value 层级、蛋白组推断、QC、limma/DEqMS 和 PTM 定位思想值得保留，但 DIA-NN 2.6 两步流程、MBR/Lib q-value、DIA 缺失机制、QuantUMS、当前 MSstatsPTM 接口和磷酸化/泛素组区分需要更新。

This skill was rewritten after a file-by-file audit of the nine proteomics skills in GPTomics/bioSkills. The upstream repository was archived on 2026-08-15. Its core ideas on q-value levels, protein inference, QC, limma/DEqMS, and PTM localization remain useful, but the DIA-NN 2.6 two-stage workflow, MBR/Lib q-values, DIA missingness, QuantUMS, current MSstatsPTM interfaces, and phosphoproteome-versus-ubiquitinome boundaries required modernization.

完整审计见 / Full audit: [`references/upstream-audit.md`](references/upstream-audit.md)

## 核心原则 / Core principles

- 区分 precursor、peptidoform、localized site、protein group 和 pathway。  
  Distinguish precursor, peptidoform, localized site, protein group, and pathway evidence.
- 不把 DIA 缺失值默认当作 MCAR，也不把填补值用于主检验。  
  Do not assume DIA missingness is MCAR or use imputed values as primary inferential evidence.
- 不对 DIA-NN 已归一化的 QuantUMS/MaxLFQ 矩阵自动再次归一化。  
  Do not automatically renormalize an already normalized DIA-NN QuantUMS/MaxLFQ matrix.
- PTM abundance 与母蛋白校正后的 PTM usage 是不同问题。  
  PTM abundance and parent-protein-adjusted PTM usage are different endpoints.
- K-GG 是 diGly 信号，不自动等同于特异性 ubiquitination。  
  K-GG is a diGly measurement and is not automatically ubiquitin-specific.
- 配对患者必须在模型和交叉验证中保持为同一统计单元。  
  Paired samples from one patient must remain one statistical unit in models and validation folds.

## 目录 / Structure

```text
zhi-proteomics/
├── SKILL.md
├── README.md
├── THIRD_PARTY_NOTICES.md
├── agents/openai.yaml
├── configs/
│   ├── question_bank.json
│   ├── intake_state.example.json
│   └── analysis_plan.example.json
├── references/
│   ├── intake-and-confirmation.md
│   ├── preflight-and-provenance.md
│   ├── methods-evidence.md
│   ├── testing-and-release.md
│   ├── diann-2.6.md
│   ├── whole-proteome.md
│   ├── phosphoproteome.md
│   ├── ubiquitinome.md
│   ├── statistics.md
│   ├── integration-reporting.md
│   └── upstream-audit.md
├── scripts/
│   ├── inspect_diann_project.py
│   ├── validate_paired_design.py
│   ├── intake_questions.py
│   └── evidence_contracts.py
└── tests/test_contracts.py
```

## 安装 / Installation

将这一整个目录安装到 `~/.codex/skills/zhi-proteomics`，更新前备份已有版本并检查本地改动。不要用递归复制无检查地覆盖独立修改。GitHub同步是另一个操作；本地版本升级不代表远端也已更新。

Install this complete folder at `~/.codex/skills/zhi-proteomics`, backing up and reviewing local differences before an update. Do not overwrite independent edits blindly. GitHub synchronization is separate; a local update does not imply a remote release.

## 使用示例 / Example prompts

```text
$zhi-proteomics 审查这个 DIA-NN 2.6 项目，并解释所有 warning、q-value 和矩阵。
$zhi-proteomics 我第一次做蛋白组学，请先分轮询问样本制备、搜库和分析目标，解释建议，确认后再运行。
$zhi-proteomics 为配对原发-复发队列建立全蛋白组差异分析流程。
$zhi-proteomics 分析 DIA 磷酸化组，分别输出 phosphosite DPA 和母蛋白校正后的 DPU。
$zhi-proteomics 分析 K-GG 泛素组，并检查 NEDD8/ISG15、IAA artifact 和母蛋白变化。
$zhi-proteomics 整合 whole proteome、phosphoproteome 和 ubiquitinome，生成候选证据表。
```

```text
$zhi-proteomics audit this DIA-NN 2.6 project and explain its warnings, q-values, and matrices.
$zhi-proteomics I am new to proteomics. Ask staged questions about preparation, search and design, explain suggestions, and confirm the plan before running.
$zhi-proteomics build a paired whole-proteome differential workflow for primary versus recurrent tumors.
$zhi-proteomics analyze this DIA phosphoproteome and report phosphosite DPA and parent-protein-adjusted DPU separately.
$zhi-proteomics analyze this K-GG ubiquitinome and audit NEDD8/ISG15, IAA artifacts, and parent-protein changes.
$zhi-proteomics integrate matched whole proteome, phosphoproteome, and ubiquitinome into a candidate evidence table.
```

## 诊断脚本 / Diagnostic scripts

读取 DIA-NN 项目结构、日志、矩阵、decoy、污染物和 q-value 字段：

Inspect DIA-NN outputs, logs, matrices, decoys, contaminants, and q-value fields:

```bash
python scripts/inspect_diann_project.py /path/to/project
```

验证配对设计和 batch–condition 混杂：

Validate paired metadata and batch–condition confounding:

```bash
python scripts/validate_paired_design.py metadata.csv \
  --sample sample --subject patient --condition condition \
  --expected-conditions Primary,Recurrent
```

列出下一轮问询（例子中的建议尚未确认，脚本不会授权执行）：

List the next question round (example proposals are unconfirmed; the selector never authorizes execution):

```bash
python scripts/intake_questions.py --mode whole --stage analysis \
  --state configs/intake_state.example.json
```

若有补测／重复针，用明确的生物样本和run列检查，不自动合并强度：

When reinjections exist, explicitly identify biological specimens and runs; the validator does not aggregate intensities:

```bash
python scripts/validate_paired_design.py metadata.tsv \
  --sample sample_id --subject subject_id --condition condition \
  --biosample biosample_id --run run_id --expected-conditions Primary,Recurrent
```

所有诊断脚本均只读，不修改原始数据。问询和计划JSON模板必须填写/确认后才用于项目，不是可直接执行的默认方案。

All diagnostic scripts are read-only. Intake/plan JSON templates require completion and confirmation; they are not ready-to-execute default protocols.

## 测试和限制 / Tests and limitations

```bash
python -m unittest discover -s tests -v
```

测试覆盖：建议不能自动成为确认、未知不重复追问或补成默认值、pilot不能越过身份冲突、NA标记、技术重复、配对方向、共同变化分母、位点/前体身份、固定C质量、缓存参数变更和污染物成员顺序。

Tests cover unconfirmed proposals, retained unknowns, pilot/identity boundaries, missing markers, technical replicates, contrast direction, common-change denominators, site/precursor identity, fixed-C masses, cache changes and contaminant member ordering.

这些是确定性实现测试，不代表已完成统计FDR/位点FLR大规模benchmark、Windows实机搜库认证或新手用户行为评测。后续验证方案见 [`references/testing-and-release.md`](references/testing-and-release.md)。本skill提供问询、审查和分析规范及辅助脚本，不冒充一个覆盖所有模式的一键自动分析软件。

These deterministic tests do not constitute a statistical FDR/FLR benchmark, Windows search certification or completed novice-user behavioral evaluation. See the testing/release reference for the remaining validation plan. This skill provides guidance and tested helpers, not a certified one-click implementation of every supported analytical mode.

## 依赖 / Dependencies

脚本主要使用 Python 标准库。若要读取 DIA-NN Parquet 内容，需要 `pyarrow`。实际统计分析根据任务使用 R/Bioconductor 中的 limma、DEqMS、msqrob2/msqrob2PTM 或 MSstatsPTM。

The scripts primarily use the Python standard library. `pyarrow` is required for DIA-NN Parquet content inspection. Statistical analyses use task-appropriate R/Bioconductor packages such as limma, DEqMS, msqrob2/msqrob2PTM, or MSstatsPTM.

## 版本与依据 / Version and evidence

- Skill version: `0.2.0`
- Review date: `2026-09-09`
- 本版变化 / This release: staged intake; chemistry/search preflight; warning levels; separate site and evidence IDs; model/common-change/zero-result contracts; regression tests.
- Methods adaptation register: [`references/methods-evidence.md`](references/methods-evidence.md)
- DIA-NN guidance: https://github.com/vdemichev/diann
- QuantUMS: https://doi.org/10.1038/s41587-026-03131-2
- DEqMS DIA protocol: https://doi.org/10.1038/s41596-026-01349-7
- msqrob2PTM: https://doi.org/10.1016/j.mcpro.2023.100708
- DIA ubiquitinomics: https://doi.org/10.1038/s41467-021-25454-1

## 许可 / License

本 skill 的上游审计来源和 MIT 许可见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。

See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for upstream provenance and the MIT notice.
