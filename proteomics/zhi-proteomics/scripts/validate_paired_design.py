#!/usr/bin/env python3
"""Validate sample metadata for paired or repeated-measures proteomics.

Prints a JSON report and never changes the metadata file.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from evidence_contracts import missing


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    text = path.read_text(encoding="utf-8-sig")
    try:
        dialect = csv.Sniffer().sniff(text[:8192], delimiters=",\t")
    except csv.Error:
        dialect = csv.excel_tab if path.suffix.lower() in {".tsv", ".txt"} else csv.excel
    reader = csv.DictReader(text.splitlines(), dialect=dialect)
    return list(reader.fieldnames or []), list(reader)


def normalized(value: Any) -> str:
    return "" if missing(value) else str(value).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("--sample", required=True, help="Sample identifier column")
    parser.add_argument("--subject", required=True, help="Patient/subject column")
    parser.add_argument("--condition", required=True, help="Condition/time column")
    parser.add_argument("--batch", help="Optional acquisition/enrichment batch column")
    parser.add_argument('--biosample',help='Optional biological specimen ID to distinguish repeat injections; requires --run')
    parser.add_argument('--run',help='Unique acquisition/injection ID when --biosample is supplied')
    parser.add_argument(
        "--expected-conditions",
        help="Comma-separated condition labels expected once per subject, e.g. Primary,Recurrent",
    )
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()

    path = args.metadata.expanduser().resolve()
    if not path.is_file():
        parser.error(f"Metadata file does not exist: {path}")

    fields, rows = read_rows(path)
    required = [args.sample, args.subject, args.condition]
    if args.batch:
        required.append(args.batch)
    if bool(args.biosample)!=bool(args.run):parser.error('--biosample and --run must be supplied together')
    if args.biosample:required += [args.biosample,args.run]
    missing_columns_nf = [column for column in required if column not in fields]
    if missing_columns_nf:
        parser.error(f"Missing columns: {', '.join(missing_columns_nf)}")

    errors: list[str] = []
    warnings: list[str] = []
    if not rows:errors.append('No sample rows supplied')
    missing_cells = defaultdict(list)
    technical_repeats = []
    original_rows = len(rows)
    if args.biosample:
        seen_runs=set();specimens={};collapsed=[]
        for row in rows:
            run=normalized(row.get(args.run));bio=normalized(row.get(args.biosample))
            if not run or not bio:
                errors.append('Missing run/biosample ID');continue
            if run in seen_runs:errors.append(f'Duplicate run identifier: {run}')
            seen_runs.add(run)
            identity=(normalized(row.get(args.subject)),normalized(row.get(args.condition)))
            if bio in specimens:
                if specimens[bio]!=identity:errors.append(f'Conflicting identity for biosample: {bio}')
                technical_repeats.append({'run':run,'biosample':bio})
            else:
                specimens[bio]=identity;copy=dict(row);copy[args.sample]=bio;collapsed.append(copy)
        rows_for_batch=rows
        rows=collapsed
        if technical_repeats:warnings.append('Technical repeats identified; counts below use biological specimens. No intensities merged. Confirm aggregation or repeated-measures model before testing.')
    else:rows_for_batch=rows
    samples = []
    subject_conditions: dict[str, list[str]] = defaultdict(list)
    condition_counts = Counter()

    for index, row in enumerate(rows, start=2):
        sample = normalized(row.get(args.sample))
        subject = normalized(row.get(args.subject))
        condition = normalized(row.get(args.condition))
        for column, value in (
            (args.sample, sample),
            (args.subject, subject),
            (args.condition, condition),
        ):
            if not value:
                missing_cells[column].append(index)
        if sample:
            samples.append(sample)
        if subject and condition:
            subject_conditions[subject].append(condition)
            condition_counts[condition] += 1

    duplicates = sorted(sample for sample, count in Counter(samples).items() if count > 1)
    if duplicates:
        errors.append(f"Duplicate sample identifiers: {duplicates}")
    for column, line_numbers in missing_cells.items():
        errors.append(f"Missing {column} at rows {line_numbers}")

    expected = (
        [item.strip() for item in args.expected_conditions.split(",") if item.strip()]
        if args.expected_conditions
        else sorted(condition_counts)
    )
    expected_counter = Counter(expected)
    if len(expected_counter)<2:errors.append('A paired comparison requires at least two conditions; specify the expected condition set')
    complete_subjects = []
    incomplete_subjects = {}
    duplicate_within_subject = {}
    for subject, conditions in sorted(subject_conditions.items()):
        observed = Counter(conditions)
        if any(count > 1 for count in observed.values()):
            duplicate_within_subject[subject] = dict(observed)
        if observed == expected_counter:
            complete_subjects.append(subject)
        else:
            incomplete_subjects[subject] = {
                "observed": dict(observed),
                "expected": dict(expected_counter),
            }
    if incomplete_subjects:
        errors.append(f"{len(incomplete_subjects)} subjects do not have the expected condition set")
    if duplicate_within_subject:
        errors.append(f"{len(duplicate_within_subject)} subjects repeat a condition")

    batch_table = None
    fully_confounded = False
    if args.batch:
        table: dict[str, Counter[str]] = defaultdict(Counter)
        for row in rows_for_batch:
            batch = normalized(row.get(args.batch))
            condition = normalized(row.get(args.condition))
            if batch and condition:
                table[batch][condition] += 1
            elif not batch:warnings.append('Unknown batch values present; cannot conclude absence of batch confounding')
        batch_table = {batch: dict(counts) for batch, counts in sorted(table.items())}
        if len(table) > 1 and all(len(counts) == 1 for counts in table.values()):
            fully_confounded = True
            errors.append("Each batch contains only one condition; batch and condition are fully confounded")
        elif any(len(counts) == 1 for counts in table.values()):
            warnings.append("At least one batch contains a single condition; inspect estimability and imbalance")

    report = {
        "metadata": str(path),
        "rows": original_rows,
        "biological_specimen_rows": len(rows),
        "technical_repeats": technical_repeats,
        "scope_note": "Validates complete pair metadata only, not arbitrary longitudinal model rank, chemistry or analysis authorization",
        "columns": fields,
        "unique_samples": len(set(samples)),
        "subjects": len(subject_conditions),
        "condition_counts": dict(condition_counts),
        "expected_conditions_per_subject": expected,
        "complete_subjects": len(complete_subjects),
        "incomplete_subjects": incomplete_subjects,
        "duplicate_conditions_within_subject": duplicate_within_subject,
        "batch_condition_table": batch_table,
        "fully_confounded": fully_confounded,
        "errors": errors,
        "warnings": warnings,
        "valid": not errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=args.indent))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
