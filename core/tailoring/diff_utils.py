"""Compute simple diffs for auditing changes."""

import difflib


def compute_diff(original: str, revised: str):
    """Return a unified diff string."""
    o = (original or "").splitlines()
    r = (revised or "").splitlines()
    diff = difflib.unified_diff(o, r, lineterm="")
    return "\n".join(diff)
