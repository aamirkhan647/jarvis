# tests/test_resume_parser.py
import unittest
from main import main


def test_main():
    res = main()
    assert res is None
