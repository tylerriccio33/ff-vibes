"""Shared test fixtures."""

import csv
from collections.abc import Generator
from pathlib import Path

import pytest
from flask.testing import FlaskClient


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
        writer.writerow({"id": "1", "text": "Patrick Mahomes is amazing and fantastic this season!"})
        writer.writerow({"id": "2", "text": "Josh Allen has been terrible lately."})
    return csv_file


@pytest.fixture
def flask_client() -> Generator[FlaskClient, None, None]:
    """Flask test client."""
    from ff_vibes.app import app

    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
