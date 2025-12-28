from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
import random
from datetime import datetime

from ml.sentiment_model import predict_sentiment
from nlp.summarizer import summarize_text
from security.hash_utils import hash_text

app = Flask(__name__)
CORS(app)

# =========================
# CONFIGURATION
# =========================
CSV_PATH = "data/feedback.csv"

QUESTIONS = [
    "What do you think about global warming?",
    "How serious is air pollution in cities?",
    "Should plastic usage be banned?",
    "What is your opinion on digital surveillance?",
    "How effective are government policies?",
    "Is climate change exaggerated?",
    "Do you trust online news sources?",
    "Is remote work the future?",
    "How concerned are you about data privacy?",
    "Should renewable energy be prioritized?"
]

CSV_HEADERS = [
    "timestamp",
    "question",
    "feedback",
    "summary",
    "sentiment",
    "hash"
]

# =========================
# CSV SAFETY & VALIDATION
# =========================
def ensure_csv_is_valid():
    """
    Ensures feedback.csv exists and has correct headers.
    Repairs file if deleted or corrupted.
    """
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(CSV_HEADERS)
        return

    try:
        with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)

        if header != CSV_HEADERS:
            with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)
                writer.writerow(CSV_HEADERS)

    except Exception:
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(CSV_HEADERS)

# Run once at startup
ensure_csv_is_valid()

# =========================
# DUPLICATE DETECTION
# =========================
def is_duplicate_feedback(feedback_hash):
    """
    Checks if feedback hash already exists.
    """
    try:
        with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("hash") == feedback_hash:
                    return True
    except Exception:
        pass

    return False

# =========================
# ROUTES
# =========================

@app.route("/question", methods=["GET"])
def get_question():
    """Return a random question (sampling with replacement)."""
    return jsonify({
        "question": random.choice(QUESTIONS)
    })


@app.route("/submit", methods=["POST"])
def submit_feedback():
    """
    Accepts feedback, performs NLP processing,
    stores securely, and returns only success message.
    """
    data = request.get_json()

    feedback = data.get("feedback", "").strip()
    question = data.get("question", "").strip()

    if not feedback or not question:
        return jsonify({"error": "Invalid input"}), 400

    hashed = hash_text(feedback)

    # Duplicate check
    if is_duplicate_feedback(hashed):
        return jsonify({"status": "Duplicate feedback ignored"})

    # NLP processing (backend-only)
    sentiment = predict_sentiment(feedback)
    summary = summarize_text(feedback)

    # Safe CSV append
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow([
            datetime.utcnow().isoformat(),
            question,
            feedback,
            summary,
            sentiment,
            hashed
        ])

    return jsonify({"status": "Feedback saved successfully"})


@app.route("/admin/analytics", methods=["GET"])
def per_question_analytics():
    """
    Returns sentiment counts per question.
    Admin-only analytics endpoint.
    """
    analytics = {}

    try:
        with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                q = row["question"]
                s = row["sentiment"]

                if q not in analytics:
                    analytics[q] = {
                        "Positive": 0,
                        "Negative": 0,
                        "Neutral": 0
                    }

                analytics[q][s] += 1

    except Exception:
        pass

    return jsonify(analytics)

# =========================
# START APP
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

