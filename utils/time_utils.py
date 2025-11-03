"""Time helpers."""

from datetime import datetime


def now_iso():
    return datetime.utcnow().isoformat() + "Z"


def human_seconds(sec: float) -> str:
    if sec < 60:
        return f"{sec:.1f}s"
    m = sec / 60.0
    return f"{m:.1f}m"
