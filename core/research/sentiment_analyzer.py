"""Minimal sentiment analyzer stub."""


def analyze_sentiment(text: str) -> dict:
    """Return neutral sentiment by default; replace with real model later."""
    if not text:
        return {"polarity": 0.0, "label": "neutral"}
    return {"polarity": 0.0, "label": "neutral"}
