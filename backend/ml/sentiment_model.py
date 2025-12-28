from transformers import pipeline

_sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def predict_sentiment(text: str) -> str:
    """
    Robust sentiment classification using pretrained transformer.
    """
    if not text or not text.strip():
        return "Neutral"

    result = _sentiment_pipeline(text[:512])[0]
    return "Positive" if result["label"] == "POSITIVE" else "Negative"
