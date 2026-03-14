"""Sentiment scoring pipeline for CSV/JSON files."""

import csv
import json
from pathlib import Path

from ff_vibes.scorer import score_text


def run(input_path: Path, text_column: str, output_path: Path) -> None:
    """Score sentiment for text in a CSV or JSON file.

    Args:
        input_path: Path to input CSV or JSON file.
        text_column: Name of the column containing text to score.
        output_path: Path to write output file.

    Raises:
        ValueError: If file extension is unknown or text_column is missing.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    if input_path.suffix.lower() == ".csv":
        _process_csv(input_path, text_column, output_path)
    elif input_path.suffix.lower() == ".json":
        _process_json(input_path, text_column, output_path)
    else:
        raise ValueError(
            f"Unknown file extension: {input_path.suffix}. Supported: .csv, .json"
        )


def _process_csv(input_path: Path, text_column: str, output_path: Path) -> None:
    """Process CSV file and write scored output."""
    rows = []

    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or has no headers")
        if text_column not in reader.fieldnames:
            raise ValueError(
                f"Column '{text_column}' not found. Available: {reader.fieldnames}"
            )
        for row in reader:
            text = row[text_column]
            score, label = score_text(text)
            row["sentiment_score"] = score
            row["sentiment_label"] = label
            rows.append(row)

    fieldnames = list(rows[0].keys()) if rows else [text_column]
    if "sentiment_score" not in fieldnames:
        fieldnames.append("sentiment_score")
    if "sentiment_label" not in fieldnames:
        fieldnames.append("sentiment_label")

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _process_json(input_path: Path, text_column: str, output_path: Path) -> None:
    """Process JSON file and write scored output."""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON file must contain a list of objects")

    if not data:
        # Empty list, write it back
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return

    # Check that text_column exists in first row
    if text_column not in data[0]:
        raise ValueError(
            f"Column '{text_column}' not found. Available: {data[0].keys()}"
        )

    for row in data:
        text = row[text_column]
        score, label = score_text(text)
        row["sentiment_score"] = score
        row["sentiment_label"] = label

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
