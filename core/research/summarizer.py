"""Tiny summarizer for research data."""


def simple_summarize(text: str, max_sentences: int = 2) -> str:
    if not text:
        return ""
    # naive: split by sentence punctuation
    import re

    sents = re.split(r"(?<=[.!?]) +", text)
    return " ".join(sents[:max_sentences])
