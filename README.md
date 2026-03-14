
# Project Overview

This project takes commentary on fantasy football players and makes them accessible in a web UI for users.

## MVP 1: Sentiment Scoring Pipeline

**Flow:**
1. User provides CSV/JSON with a text column via CLI
2. `scorer.py` scores each text with VADER (returns float in [-1, 1] + label: positive/negative/neutral)
3. `pipeline.py` reads input, scores each row, writes output with `sentiment_score` and `sentiment_label` columns

**Usage:**
```bash
make score  # or: uv run ff-vibes --input data/raw.csv --text-column text --output out.csv
```

# For Agents :)

#### Project Conventions

- Use uv religiously; `uv add` should be a majority of things.
- MPV > finished product.
- 99% of all terminal commands should be a `make` command.

#### Testing Conventions

- Use pytest
- Don't group by class, just functions
- Fixtures should be leveraged heavily, and they all live in conftest
- xfail if something isn't implemented

#### Coding Conventions

- Run `make lint` which runs the linter and type checker for everything
- Mini-comments are smell, do a long form comment on a section if it's complicated.
- Fail fast. No `get`, `except Exception: ...` or anything like that.
- No premature optimizations, ever.