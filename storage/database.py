"""Simple SQLite wrapper for storing metadata like jobs and embeddings."""

import sqlite3
import os
from config.settings import DB_PATH
from utils.logger import get_logger

logger = get_logger(__name__)


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS jobs (
        job_id TEXT PRIMARY KEY,
        title TEXT,
        company TEXT,
        location TEXT,
        posted_date TEXT,
        raw_json TEXT
    );
    """
    )
    conn.commit()
    conn.close()
    logger.info("Database initialized at %s", DB_PATH)


def store_job(job_id: str, job_json: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
    INSERT OR REPLACE INTO jobs (job_id, title, company, location, posted_date, raw_json)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            job_id,
            job_json.get("title"),
            job_json.get("company"),
            job_json.get("location"),
            job_json.get("posted_date"),
            str(job_json),
        ),
    )
    conn.commit()
    conn.close()
