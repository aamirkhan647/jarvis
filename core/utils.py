# core/utils.py
import json
import logging
from pathlib import Path
import os

ROOT = Path(__file__).parents[1].resolve()
CONFIG_DIR = ROOT / "config"
DEFAULTS_PATH = CONFIG_DIR / "defaults.json"
USER_CONFIG_PATH = CONFIG_DIR / "config.json"
DATA_DIR = ROOT / "data"
LOG_DIR = DATA_DIR / "logs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=str(LOG_DIR / "app.log"),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logging.getLogger().addHandler(logging.StreamHandler())  # also print to console
    logging.info("Logging initialized.")


def load_config():
    # Load defaults then merge with user config (if exists)
    defaults = {}
    if DEFAULTS_PATH.exists():
        with open(DEFAULTS_PATH, "r", encoding="utf-8") as f:
            defaults = json.load(f)
    else:
        # fallback default dict
        defaults = {
            "saved_folder": "%USERPROFILE%\\Documents\\JARVIS_TailoredResumes",
            "adzuna_app_id": "b68674e7",
            "adzuna_api_key": "942660a8437647763f41a0f2d5f907e5",
            "openai_api_key": "",
            "search_interval_minutes": 60,
            "job_query": "machine learning engineer, llm, python",
            "location": "Canada",
            "use_openai_embeddings": False,
            "auto_apply_enabled": False,
            "rss_feeds": [
                "https://remoteok.com/remote-jobs.rss",
                "https://stackoverflow.com/jobs/feed",
            ],
        }

    user_conf = {}
    if USER_CONFIG_PATH.exists():
        try:
            with open(USER_CONFIG_PATH, "r", encoding="utf-8") as f:
                user_conf = json.load(f)
        except Exception as e:
            logging.error(f"Error loading user config: {e}")
            user_conf = {}
    # merge: user values override defaults
    merged = defaults.copy()
    merged.update(user_conf)
    # Expand environment variables in saved_folder
    merged["saved_folder"] = os.path.expandvars(
        merged.get("saved_folder", defaults["saved_folder"])
    )
    return merged
