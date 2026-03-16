"""Flask API for sentiment scoring and dashboard."""

import csv
from flask import Flask, request, jsonify, render_template

from ff_vibes.scorer import score_text

app = Flask(__name__, template_folder="templates")


def _read_csv(path: str) -> list[dict]:
    """Read CSV file and return list of dictionaries."""
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        pass
    return rows


@app.route("/", methods=["GET"])
def index():
    """Serve the sentiment dashboard UI."""
    return render_template("index.html")


@app.route("/api/players", methods=["GET"])
def get_players():
    """Get list of all players with aggregate sentiment stats.

    Returns: [{"name": str, "avg_score": float, "count": int}]
    """
    rows = _read_csv("out.csv")
    if not rows:
        return jsonify([])

    player_stats = {}
    for row in rows:
        player = row.get("player", "").strip()
        if not player:
            continue
        score_str = row.get("sentiment_score", "0")
        try:
            score = float(score_str)
        except (ValueError, TypeError):
            score = 0.0

        if player not in player_stats:
            player_stats[player] = {"scores": [], "count": 0}
        player_stats[player]["scores"].append(score)
        player_stats[player]["count"] += 1

    result = [
        {
            "name": name,
            "avg_score": sum(stats["scores"]) / len(stats["scores"]),
            "count": stats["count"],
        }
        for name, stats in player_stats.items()
    ]
    return jsonify(sorted(result, key=lambda x: x["name"]))


@app.route("/api/players/<name>", methods=["GET"])
def get_player_comments(name: str):
    """Get all comments mentioning a specific player.

    Returns: [{"text": str, "score": float, "label": str}]
    """
    rows = _read_csv("out.csv")
    result = []
    for row in rows:
        if row.get("player", "").strip() == name:
            result.append(
                {
                    "text": row.get("text", ""),
                    "score": float(row.get("sentiment_score", "0")),
                    "label": row.get("sentiment_label", ""),
                }
            )
    return jsonify(result)


@app.route("/score", methods=["POST"])
def score():
    """Score sentiment for provided text.

    Expects JSON body: {"text": "..."}
    Returns: {"score": float, "label": str}
    """
    body = request.get_json(force=True)
    text = body["text"]
    score_val, label = score_text(text)
    return jsonify({"score": score_val, "label": label})
