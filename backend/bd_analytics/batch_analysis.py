import csv
from collections import Counter
import os

CSV_PATH = "data/feedback.csv"

def sentiment_summary():
    if not os.path.exists(CSV_PATH):
        return {}

    sentiments = []

    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sentiments.append(row["sentiment"])

    return dict(Counter(sentiments))
