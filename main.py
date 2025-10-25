# main.py
"""
Entry point for JARVIS (TechJobTailor).
Initializes logging/config and runs the GUI app.
"""
import sys
from pathlib import Path

from core.utils import setup_logging, load_config
from gui.main_window import JobFinderApp

def main():
    setup_logging()
    cfg = load_config()
    app = JobFinderApp(cfg)
    app.mainloop()

if __name__ == "__main__":
    main()
