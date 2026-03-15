"""Sentiment scoring pipeline for CSV files."""

import csv
from pathlib import Path

from ff_vibes.scorer import score_player_sentences
from ff_vibes.players import extract_players


def run(input_path: Path, text_column: str, output_path: Path) -> None:
    """Score per-player sentiment for text in a CSV file.

    Phases:
    1. Ingestion: Read and validate input CSV
    2. Staging: Extract players and score sentences mentioning each player
    3. Consumption: Write one row per (comment, player) pair

    Args:
        input_path: Path to input CSV file.
        text_column: Name of the column containing text to score.
        output_path: Path to write output CSV file.

    Raises:
        ValueError: If text_column is missing from CSV.
    """
    input_path = Path(input_path)
    output_path = Path(output_path)

    rows = _ingest(input_path, text_column)
    scored = _stage(rows, text_column)
    _consume(scored, output_path)


def _ingest(input_path: Path, text_column: str) -> list[dict]:
    """Ingest phase: Read CSV and validate schema.

    Args:
        input_path: Path to input CSV file.
        text_column: Name of the column containing text to score.

    Returns:
        List of row dictionaries from the CSV.

    Raises:
        ValueError: If CSV is empty or text_column is missing.
    """
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
            rows.append(row)

    return rows


def _stage(rows: list[dict], text_column: str) -> list[dict]:
    """Staging phase: Explode each row into one row per mentioned player.

    For each player found, scores only the sentences mentioning that player.
    Rows with no player mentions are dropped.

    Args:
        rows: List of row dictionaries to process.
        text_column: Name of the column containing text to score.

    Returns:
        List of scored row dicts, one per (comment, player) pair.
    """
    scored = []
    for row in rows:
        text = row[text_column]
        players = extract_players(text)
        for player in players:
            score, label = score_player_sentences(text, player)
            scored.append({**row, "player": player, "sentiment_score": score, "sentiment_label": label})
    return scored


def _consume(rows: list[dict], output_path: Path) -> None:
    """Consumption phase: Write scored rows to output CSV.

    Args:
        rows: List of scored row dictionaries.
        output_path: Path to write output CSV file.
    """
    fieldnames = list(rows[0].keys()) if rows else []

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
