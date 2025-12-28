from transformers import pipeline

_sentiment_pipeline = None

def predict_sentiment(text: str) -> str:
    global _sentiment_pipeline

    if not text.strip():
        return "Neutral"

    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1  # force CPU
        )

    result = _sentiment_pipeline(text[:512])[0]
    return "Positive" if result["label"] == "POSITIVE" else "Negative"
