"""Constants used across the application."""

ATS_SCORE_MAX = 100
JOB_MATCH_SCORE_MAX = 100

# Default weights for composite scoring (sum must be 1.0)
DEFAULT_SCORING_WEIGHTS = {
    "skills": 0.40,
    "experience": 0.25,
    "title": 0.10,
    "education": 0.10,
    "culture": 0.05,
    "location": 0.10,
}
