import argparse
from pathlib import Path

from ff_vibes.pipeline import run


def main() -> None:
    """CLI entrypoint for sentiment scoring pipeline."""
    parser = argparse.ArgumentParser(
        description="Score fantasy football commentary for sentiment"
    )
    parser.add_argument("--input", required=True, help="Path to input CSV or JSON file")
    parser.add_argument(
        "--text-column",
        required=True,
        help="Name of the column containing text to score",
    )
    parser.add_argument(
        "--output", required=True, help="Path to output CSV or JSON file"
    )

    args = parser.parse_args()
    run(Path(args.input), args.text_column, Path(args.output))
