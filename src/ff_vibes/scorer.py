"""Sentiment scoring using zero-shot NLI with spaCy sentence segmentation."""

import spacy
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")
_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
)

_LABELS = ["positive", "negative"]


def score_text(text: str) -> tuple[float, str]:
    """Score full text for sentiment (no player context).

    Returns:
        A tuple of (score, label) where score is a float in [-1, 1]
        and label is "positive", "negative", or "neutral".
    """
    if not text.strip():
        return 0.0, "neutral"

    result = _classifier(
        text,
        candidate_labels=_LABELS,
        hypothesis_template="The sentiment of this text is {}.",
    )
    return _extract_score(result)


def score_player_sentences(text: str, player: str) -> tuple[float, str]:
    """Score sentiment toward a specific player using zero-shot NLI.

    Uses spaCy to extract sentences mentioning the player, then asks
    the NLI model whether the outlook for that player is positive or negative.
    """
    doc = nlp(text)
    name_parts = [t.lower() for t in player.split() if len(t) > 2]
    relevant = [
        sent.text
        for sent in doc.sents
        if any(part in sent.text.lower() for part in name_parts)
    ]

    target = " ".join(relevant) if relevant else text

    if not target.strip():
        return 0.0, "neutral"

    result = _classifier(
        target,
        candidate_labels=_LABELS,
        hypothesis_template=f"The fantasy football outlook for {player} is {{}}.",
    )
    return _extract_score(result)


def _extract_score(result: dict) -> tuple[float, str]:
    """Convert zero-shot classification result to (score, label)."""
    scores = dict(zip(result["labels"], result["scores"]))
    pos = scores["positive"]
    neg = scores["negative"]
    # Map to [-1, 1]: positive confidence pushes toward +1, negative toward -1
    score = pos - neg
    return score, _label(score)


def _label(score: float) -> str:
    if score >= 0.3:
        return "positive"
    elif score <= -0.3:
        return "negative"
    return "neutral"
