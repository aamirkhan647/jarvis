# JARVIS — Job Application & Resume Virtual Intelligence System

A Windows-focused desktop assistant to find tech jobs, rank them vs. your resume, and produce tailored resumes.

## Features
- Load resume (PDF/DOCX), extract text
- Search job postings (RSS, optional Adzuna, lightweight scraping)
- Rank jobs by relevance using TF-IDF
- Generate a tailored DOCX resume (optionally convert to PDF on Windows with Word)
- Safe-by-default: auto-apply is disabled (stubbed)

## Quickstart
1. `python -m venv venv && venv\\Scripts\\activate`
2. `pip install -r requirements.txt`
3. Edit `config/defaults.json` or let the app create `config/config.json`.
4. `python main.py`

## Packaging
Use PyInstaller:
