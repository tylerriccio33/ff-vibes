"""Extract player names from text by matching against known NFL players."""

import csv
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


@lru_cache(maxsize=1)
def _load_known_players() -> set[str]:
    """Load player names from data/players.csv."""
    path = DATA_DIR / "players.csv"
    if not path.exists():
        return set()
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row["display_name"] for row in reader if row["display_name"]}


def extract_players(text: str) -> list[str]:
    """Extract known NFL player names found in the text.

    Args:
        text: Text to search for player names.

    Returns:
        List of matched player names.
    """
    known = _load_known_players()
    text_lower = text.lower()
    return sorted(name for name in known if name.lower() in text_lower)
