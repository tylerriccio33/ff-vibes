"""Tests for the Flask sentiment scoring API."""

from flask.testing import FlaskClient


def test_score_positive(flask_client: FlaskClient) -> None:
    """Test scoring positive sentiment."""
    response = flask_client.post("/score", json={"text": "Amazing player!"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["label"] == "positive"
    assert data["score"] > 0.05


def test_score_negative(flask_client: FlaskClient) -> None:
    """Test scoring negative sentiment."""
    response = flask_client.post("/score", json={"text": "This is terrible!"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["label"] == "negative"
    assert data["score"] < -0.05


def test_score_neutral(flask_client: FlaskClient) -> None:
    """Test scoring neutral sentiment."""
    response = flask_client.post("/score", json={"text": "The player was drafted."})
    assert response.status_code == 200
    data = response.get_json()
    assert data["label"] == "neutral"
