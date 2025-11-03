"""Load environment and configuration files."""

import os
from dotenv import load_dotenv


def load_env(path: str = None):
    if path and os.path.exists(path):
        load_dotenv(path)
    else:
        load_dotenv()
