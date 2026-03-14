"""Tests for sentiment scorer."""

from ff_vibes.scorer import score_text


def test_positive_text(positive_text: str) -> None:
    """Test scoring of positive text."""
    score, label = score_text(positive_text)
    assert label == "positive"
    assert score > 0.05


def test_negative_text(negative_text: str) -> None:
    """Test scoring of negative text."""
    score, label = score_text(negative_text)
    assert label == "negative"
    assert score < -0.05


def test_neutral_text(neutral_text: str) -> None:
    """Test scoring of neutral text."""
    score, label = score_text(neutral_text)
    assert label == "neutral"
    assert -0.05 <= score <= 0.05


def test_empty_string() -> None:
    """Test scoring of empty string."""
    score, label = score_text("")
    assert label == "neutral"
    assert score == 0.0
