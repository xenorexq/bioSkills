#!/usr/bin/env python3
"""Read-only inventory of a DIA-NN output directory.

The script prints JSON to stdout and never modifies source files. PyArrow is
optional; without it, text reports and matrices are still inspected.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


TEXT_FILES = {
    "log": "report.log.txt",
    "manifest": "report.manifest.txt",
    "stats": "report.stats.tsv",
    "pg_matrix": "report.pg_matrix.tsv",
    "pr_matrix": "report.pr_matrix.tsv",
    "gg_matrix": "report.gg_matrix.tsv",
    "unique_genes_matrix": "report.unique_genes_matrix.tsv",
}


def find_file(root: Path, name: str) -> Path | None:
    direct = root / name
    if direct.is_file():
        return direct
    matches = sorted(root.rglob(name), key=lambda p: (len(p.parts), str(p)))
    return matches[0] if matches else None


def count_tsv(path: Path, contaminant_tag: str) -> dict[str, Any]:
    rows = 0
    malformed = 0
    contaminants = 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)
        width = len(header)
        for row in reader:
            rows += 1
            if len(row) != width:
                malformed += 1
            if row and row[0].startswith(contaminant_tag):
                contaminants += 1

    if path.name.endswith("pg_matrix.tsv"):
        metadata_columns = 6
    elif path.name.endswith("pr_matrix.tsv"):
        metadata_columns = 10
    elif path.name.endswith(("gg_matrix.tsv", "unique_genes_matrix.tsv")):
        metadata_columns = 3
    else:
        metadata_columns = 0

    samples = header[metadata_columns:] if metadata_columns else []
    return {
        "rows": rows,
        "columns": width,
        "metadata_columns_assumed": metadata_columns,
        "sample_columns": len(samples),
        "sample_headers": samples,
        "malformed_rows": malformed,
        "leading_contaminant_rows": contaminants,
    }


def inspect_log(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    version = None
    match = re.search(r"DIA-NN\s+([^\s]+)", text)
    if match:
        version = match.group(1)
    command = next(
        (line.strip() for line in text.splitlines() if "diann" in line.lower() and " --" in line),
        None,
    )
    warnings = [line.strip() for line in text.splitlines() if "WARNING" in line.upper()]
    errors = [line.strip() for line in text.splitlines() if re.search(r"\bERROR\b", line, re.I)]
    processed = None
    match = re.search(r"(\d+) files will be processed", text)
    if match:
        processed = int(match.group(1))
    return {
        "version": version,
        "files_announced": processed,
        "command": command,
        "warnings": warnings,
        "errors": errors,
    }


def inspect_stats(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))

    def numeric_summary(column: str) -> dict[str, float] | None:
        values = []
        for row in rows:
            try:
                values.append(float(row[column]))
            except (KeyError, TypeError, ValueError):
                pass
        if not values:
            return None
        return {"min": min(values), "max": max(values), "mean": sum(values) / len(values)}

    return {
        "runs": len(rows),
        "precursors_identified": numeric_summary("Precursors.Identified"),
        "proteins_identified": numeric_summary("Proteins.Identified"),
        "total_quantity": numeric_summary("Total.Quantity"),
        "ms1_signal": numeric_summary("MS1.Signal"),
        "ms2_signal": numeric_summary("MS2.Signal"),
    }


def inspect_parquet(path: Path, contaminant_tag: str) -> dict[str, Any]:
    try:
        import pyarrow.compute as pc
        import pyarrow.parquet as pq
    except ImportError:
        return {"available": False, "reason": "Install pyarrow to inspect parquet content."}

    parquet = pq.ParquetFile(path)
    names = parquet.schema_arrow.names
    selected = [
        name
        for name in (
            "Decoy",
            "Protein.Group",
            "Q.Value",
            "Global.Q.Value",
            "Lib.Q.Value",
            "Peptidoform.Q.Value",
            "Global.Peptidoform.Q.Value",
            "Lib.Peptidoform.Q.Value",
            "PTM.Site.Confidence",
            "Lib.PTM.Site.Confidence",
            "PG.Q.Value",
            "Global.PG.Q.Value",
            "Lib.PG.Q.Value",
            "Quantity.Quality",
            "PG.MaxLFQ.Quality",
        )
        if name in names
    ]
    table = pq.read_table(path, columns=selected) if selected else None
    result: dict[str, Any] = {
        "available": True,
        "rows": parquet.metadata.num_rows,
        "row_groups": parquet.num_row_groups,
        "columns": names,
    }
    if table is None:
        return result

    if "Decoy" in selected:
        result["decoy_counts"] = {
            str(item["values"]): item["counts"]
            for item in pc.value_counts(table["Decoy"]).to_pylist()
        }
    if "Protein.Group" in selected:
        mask = pc.starts_with(table["Protein.Group"], contaminant_tag)
        result["leading_contaminant_rows"] = pc.sum(pc.cast(mask, "int64")).as_py()
    qvalue_summary = {}
    for name in selected:
        if name.endswith("Q.Value") or name.endswith("Site.Confidence") or name.endswith("Quality"):
            column = table[name]
            summary = pc.min_max(column).as_py()
            if name.endswith("Q.Value"):
                summary["le_0.01"] = pc.sum(
                    pc.cast(pc.less_equal(column, 0.01), "int64")
                ).as_py()
                summary["le_0.05"] = pc.sum(
                    pc.cast(pc.less_equal(column, 0.05), "int64")
                ).as_py()
            summary["null"] = column.null_count
            qvalue_summary[name] = summary
    result["score_summaries"] = qvalue_summary
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="DIA-NN output directory or project root")
    parser.add_argument("--contaminant-tag", default="CONTAMINANT_")
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()

    root = args.path.expanduser().resolve()
    if not root.exists():
        parser.error(f"Path does not exist: {root}")

    found = {key: find_file(root, name) for key, name in TEXT_FILES.items()}
    report_parquet = find_file(root, "report.parquet")
    report_library = find_file(root, "report-lib.parquet")

    output: dict[str, Any] = {
        "root": str(root),
        "files": {key: str(path) if path else None for key, path in found.items()},
    }
    if found["log"]:
        output["log"] = inspect_log(found["log"])
    if found["stats"]:
        output["stats"] = inspect_stats(found["stats"])
    output["matrices"] = {
        key: count_tsv(path, args.contaminant_tag)
        for key, path in found.items()
        if key.endswith("matrix") and path
    }
    if report_parquet:
        output["report_parquet"] = inspect_parquet(report_parquet, args.contaminant_tag)
    if report_library:
        output["report_library_parquet"] = inspect_parquet(report_library, args.contaminant_tag)

    print(json.dumps(output, ensure_ascii=False, indent=args.indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
