-- Basic schema for jobtailor app
CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    posted_date TEXT,
    raw_json TEXT
);

CREATE TABLE IF NOT EXISTS resumes (
    resume_id TEXT PRIMARY KEY,
    filename TEXT,
    uploaded_at TEXT,
    metadata TEXT
);
