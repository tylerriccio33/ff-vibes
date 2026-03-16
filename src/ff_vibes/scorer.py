"""Sentiment scoring using DistilBERT with spaCy sentence segmentation."""

import spacy
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")
_classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)


def score_text(text: str) -> tuple[float, str]:
    """Score full text for sentiment.

    Returns:
        A tuple of (score, label) where score is a float in [-1, 1]
        and label is "positive", "negative", or "neutral".
    """
    if not text.strip():
        return 0.0, "neutral"

    result = _classifier(text, truncation=True)[0]
    # Map model confidence [0.5, 1.0] to magnitude [0, 1], with sign from label
    confidence = result["score"]
    magnitude = 2 * (confidence - 0.5)  # 0.5 -> 0, 1.0 -> 1.0
    score = magnitude if result["label"] == "POSITIVE" else -magnitude
    return score, _label(score)


def score_player_sentences(text: str, player: str) -> tuple[float, str]:
    """Score only the sentences that mention a player.

    Uses spaCy to segment text into sentences, finds the ones containing
    the player name, and scores their combined text with DistilBERT.

    If no sentence match is found, falls back to scoring the full text.
    """
    doc = nlp(text)
    player_lower = player.lower()
    relevant = [sent.text for sent in doc.sents if player_lower in sent.text.lower()]

    target = " ".join(relevant) if relevant else text
    return score_text(target)


def _label(score: float) -> str:
    if score >= 0.6:
        return "positive"
    elif score <= -0.6:
        return "negative"
    return "neutral"
