"""Shared test fixtures."""

import csv
import json
from pathlib import Path

import pytest


@pytest.fixture
def positive_text() -> str:
    """Sample positive text."""
    return "I love this player! Amazing performance!"


@pytest.fixture
def negative_text() -> str:
    """Sample negative text."""
    return "This is terrible. The worst trade ever."


@pytest.fixture
def neutral_text() -> str:
    """Sample neutral text."""
    return "The player was drafted in the third round."


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Create a sample CSV file with comments."""
    csv_file = tmp_path / "sample.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "text"])
        writer.writeheader()
        writer.writerow({"id": "1", "text": "Great trade!"})
        writer.writerow({"id": "2", "text": "Awful decision."})
    return csv_file


@pytest.fixture
def sample_json(tmp_path: Path) -> Path:
    """Create a sample JSON file with comments."""
    json_file = tmp_path / "sample.json"
    data = [
        {"id": "1", "text": "Amazing play!"},
        {"id": "2", "text": "Disappointing performance."},
    ]
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return json_file
