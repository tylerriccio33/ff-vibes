"""Sentiment scoring using VADER."""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def score_text(text: str) -> tuple[float, str]:
    """Score text for sentiment.

    Args:
        text: The text to score.

    Returns:
        A tuple of (score, label) where score is a float in [-1, 1]
        and label is "positive", "negative", or "neutral".
    """
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return compound, label
