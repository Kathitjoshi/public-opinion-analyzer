from transformers import pipeline

_summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

def summarize_text(text: str) -> str:
    """
    Abstractive summarization using pretrained transformer.
    """
    if len(text.split()) < 20:
        return text

    summary = _summarizer(
        text[:1024],
        max_length=15,
        min_length=8,
        do_sample=False
    )

    return summary[0]["summary_text"]
