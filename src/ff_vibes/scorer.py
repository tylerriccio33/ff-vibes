"""Sentiment scoring using VADER with spaCy sentence segmentation."""

import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nlp = spacy.load("en_core_web_sm")
analyzer = SentimentIntensityAnalyzer()


def score_text(text: str) -> tuple[float, str]:
    """Score full text for sentiment.

    Returns:
        A tuple of (score, label) where score is a float in [-1, 1]
        and label is "positive", "negative", or "neutral".
    """
    compound = analyzer.polarity_scores(text)["compound"]
    return compound, _label(compound)


def score_player_sentences(text: str, player: str) -> tuple[float, str]:
    """Score only the sentences that mention a player.

    Uses spaCy to segment text into sentences, finds the ones containing
    the player name, and scores their combined text with VADER.

    If no sentence match is found (shouldn't happen if the player was
    extracted from this text), falls back to scoring the full text.
    """
    doc = nlp(text)
    player_lower = player.lower()
    relevant = [sent.text for sent in doc.sents if player_lower in sent.text.lower()]

    target = " ".join(relevant) if relevant else text
    compound = analyzer.polarity_scores(target)["compound"]
    return compound, _label(compound)


def _label(compound: float) -> str:
    if compound >= 0.05:
        return "positive"
    elif compound <= -0.05:
        return "negative"
    return "neutral"
