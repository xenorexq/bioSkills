# Zhi Proteomics

## 中文简介

`Zhi Proteomics` 是一套面向 DIA-NN 2.6+ 的个人 Codex skill，专门处理相互匹配的 DIA 全蛋白组、磷酸化蛋白组和 K-GG/diGly 泛素组。它覆盖搜库与输出审计、分层质控、配对/复杂设计差异分析、PTM 位点定位、母蛋白校正、跨组学整合和论文级结果呈现。

## English overview

`Zhi Proteomics` is a personal Codex skill for matched DIA-NN 2.6+ whole-proteome, phosphoproteome, and K-GG/diGly ubiquitinome projects. It covers search/output auditing, layered QC, paired and complex differential designs, PTM localization, parent-protein adjustment, cross-ome integration, and publication-oriented reporting.

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
├── references/
│   ├── diann-2.6.md
│   ├── whole-proteome.md
│   ├── phosphoproteome.md
│   ├── ubiquitinome.md
│   ├── statistics.md
│   ├── integration-reporting.md
│   └── upstream-audit.md
└── scripts/
    ├── inspect_diann_project.py
    └── validate_paired_design.py
```

## 安装 / Installation

将仓库克隆到 Codex personal skills 目录：

Clone the repository into the Codex personal skills directory:

```bash
git clone https://github.com/xenorexq/bioSkills.git
cp -R bioSkills/proteomics/zhi-proteomics ~/.codex/skills/zhi-proteomics
```

也可以直接将本目录复制到 `~/.codex/skills/zhi-proteomics`。重新打开任务后，Codex 会从 `SKILL.md` 的名称和描述发现它。

Alternatively copy this directory directly to `~/.codex/skills/zhi-proteomics`. Codex discovers it from the name and description in `SKILL.md` when a new task loads skills.

## 使用示例 / Example prompts

```text
$zhi-proteomics 审查这个 DIA-NN 2.6 项目，并解释所有 warning、q-value 和矩阵。
$zhi-proteomics 为配对原发-复发队列建立全蛋白组差异分析流程。
$zhi-proteomics 分析 DIA 磷酸化组，分别输出 phosphosite DPA 和母蛋白校正后的 DPU。
$zhi-proteomics 分析 K-GG 泛素组，并检查 NEDD8/ISG15、IAA artifact 和母蛋白变化。
$zhi-proteomics 整合 whole proteome、phosphoproteome 和 ubiquitinome，生成候选证据表。
```

```text
$zhi-proteomics audit this DIA-NN 2.6 project and explain its warnings, q-values, and matrices.
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

两个脚本均为只读诊断，不会修改原始数据。

Both scripts are read-only diagnostics and do not modify source data.

## 依赖 / Dependencies

脚本主要使用 Python 标准库。若要读取 DIA-NN Parquet 内容，需要 `pyarrow`。实际统计分析根据任务使用 R/Bioconductor 中的 limma、DEqMS、msqrob2/msqrob2PTM 或 MSstatsPTM。

The scripts primarily use the Python standard library. `pyarrow` is required for DIA-NN Parquet content inspection. Statistical analyses use task-appropriate R/Bioconductor packages such as limma, DEqMS, msqrob2/msqrob2PTM, or MSstatsPTM.

## 版本与依据 / Version and evidence

- Skill version: `0.1.0`
- Audit date: `2026-09-08`
- DIA-NN guidance: https://github.com/vdemichev/diann
- QuantUMS: https://doi.org/10.1038/s41587-026-03131-2
- DEqMS DIA protocol: https://doi.org/10.1038/s41596-026-01349-7
- msqrob2PTM: https://doi.org/10.1016/j.mcpro.2023.100708
- DIA ubiquitinomics: https://doi.org/10.1038/s41467-021-25454-1

## 许可 / License

本 skill 的上游审计来源和 MIT 许可见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。

See [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for upstream provenance and the MIT notice.
