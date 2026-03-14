"""Tests for sentiment scoring pipeline."""

import csv
import json
from pathlib import Path

import pytest

from ff_vibes.pipeline import run


def test_csv_roundtrip(sample_csv: Path, tmp_path: Path) -> None:
    """Test CSV file scoring roundtrip."""
    output_csv = tmp_path / "output.csv"
    run(sample_csv, "text", output_csv)

    # Verify output file exists and has sentiment columns
    assert output_csv.exists()

    with open(output_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 2
    assert "sentiment_score" in rows[0]
    assert "sentiment_label" in rows[0]

    # First row should be positive
    assert rows[0]["sentiment_label"] == "positive"
    assert float(rows[0]["sentiment_score"]) > 0.05

    # Second row should be negative
    assert rows[1]["sentiment_label"] == "negative"
    assert float(rows[1]["sentiment_score"]) < -0.05


def test_json_roundtrip(sample_json: Path, tmp_path: Path) -> None:
    """Test JSON file scoring roundtrip."""
    output_json = tmp_path / "output.json"
    run(sample_json, "text", output_json)

    # Verify output file exists and has sentiment columns
    assert output_json.exists()

    with open(output_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    assert "sentiment_score" in data[0]
    assert "sentiment_label" in data[0]

    # First row should be positive
    assert data[0]["sentiment_label"] == "positive"
    assert data[0]["sentiment_score"] > 0.05

    # Second row should be negative
    assert data[1]["sentiment_label"] == "negative"
    assert data[1]["sentiment_score"] < -0.05


def test_missing_column_csv(tmp_path: Path) -> None:
    """Test that missing text column raises error for CSV."""
    csv_file = tmp_path / "missing_col.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "comment"])
        writer.writeheader()
        writer.writerow({"id": "1", "comment": "Some text"})

    output_file = tmp_path / "output.csv"
    with pytest.raises(ValueError, match="Column 'text' not found"):
        run(csv_file, "text", output_file)


def test_missing_column_json(tmp_path: Path) -> None:
    """Test that missing text column raises error for JSON."""
    json_file = tmp_path / "missing_col.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump([{"id": "1", "comment": "Some text"}], f)

    output_file = tmp_path / "output.json"
    with pytest.raises(ValueError, match="Column 'text' not found"):
        run(json_file, "text", output_file)


def test_unknown_file_extension(tmp_path: Path) -> None:
    """Test that unknown file extension raises error."""
    unknown_file = tmp_path / "data.txt"
    unknown_file.write_text("some data")

    output_file = tmp_path / "output.txt"
    with pytest.raises(ValueError, match="Unknown file extension"):
        run(unknown_file, "text", output_file)
