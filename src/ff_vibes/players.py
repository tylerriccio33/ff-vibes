"""Extract player names from text using simple pattern matching."""

import re


def extract_players(text: str) -> list[str]:
    """Extract potential player names from text.

    Uses a simple heuristic: capitalized words that appear to be names.
    Common words (single letters, stop words) are filtered out.

    Args:
        text: Text to extract player names from.

    Returns:
        List of unique player names found in the text.
    """
    # Common words to exclude
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "of",
        "to",
        "for",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "must",
        "can",
        "great",
        "really",
        "good",
        "bad",
        "very",
        "well",
        "too",
        "so",
        "that",
        "this",
        "which",
        "who",
        "what",
        "when",
        "where",
        "why",
        "how",
        "all",
        "each",
        "every",
        "both",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "no",
        "nor",
        "not",
        "only",
        "own",
        "same",
        "so",
        "than",
        "too",
        "very",
    }

    # Find capitalized words (potential names)
    # Match words that start with uppercase, excluding sentence starts
    words = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", text)

    # Filter out common words and deduplicate
    players = []
    seen = set()
    for word in words:
        lower = word.lower()
        # Skip if it's a common word or already seen
        if lower not in stop_words and word not in seen:
            seen.add(word)
            players.append(word)

    return players
