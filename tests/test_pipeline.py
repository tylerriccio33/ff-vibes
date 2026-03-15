"""Tests for sentiment scoring pipeline."""

import csv
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
    assert "player" in rows[0]
    assert "sentiment_score" in rows[0]
    assert "sentiment_label" in rows[0]

    # Patrick Mahomes row should be positive
    assert rows[0]["player"] == "Patrick Mahomes"
    assert rows[0]["sentiment_label"] == "positive"
    assert float(rows[0]["sentiment_score"]) > 0.05

    # Josh Allen row should be negative
    assert rows[1]["player"] == "Josh Allen"
    assert rows[1]["sentiment_label"] == "negative"
    assert float(rows[1]["sentiment_score"]) < -0.05


def test_missing_column(tmp_path: Path) -> None:
    """Test that missing text column raises error."""
    csv_file = tmp_path / "missing_col.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "comment"])
        writer.writeheader()
        writer.writerow({"id": "1", "comment": "Some text"})

    output_file = tmp_path / "output.csv"
    with pytest.raises(ValueError, match="Column 'text' not found"):
        run(csv_file, "text", output_file)
