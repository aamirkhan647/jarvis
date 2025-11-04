"""Test simple tools."""

from tools.nlp_tools import extract_keywords


def test_extract_keywords():
    txt = "Python, machine learning, data analysis and SQL are required."
    kws = extract_keywords(txt)
    assert "python" in [k.lower() for k in kws]
