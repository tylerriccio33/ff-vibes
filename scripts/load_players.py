"""Load NFL player names from nflverse and save to data/players.csv."""

from pathlib import Path

import nflreadpy


def main() -> None:
    df = nflreadpy.load_players()
    # Keep only display_name, deduplicate
    names = df.select("display_name").unique().sort("display_name")
    out = Path(__file__).resolve().parent.parent / "data" / "players.csv"
    names.write_csv(out)
    print(f"Wrote {len(names)} players to {out}")


if __name__ == "__main__":
    main()
