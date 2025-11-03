"""Global settings for JobTailor."""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model / embedding config
EMBEDDING_MODEL = os.environ.get("JT_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
LLM_PROVIDER = os.environ.get("JT_LLM_PROVIDER", "openai")

# Database file
DB_PATH = os.environ.get("JT_DB_PATH", os.path.join(BASE_DIR, "data", "jobtailor.db"))

# Default thresholds
DEFAULT_MATCH_THRESHOLD = float(os.environ.get("JT_DEFAULT_THRESHOLD", "60.0"))

# Worker pool size
WORKER_POOL_MAX_WORKERS = int(os.environ.get("JT_WORKER_POOL", "6"))

# Logging
LOG_LEVEL = os.environ.get("JT_LOG_LEVEL", "INFO")
