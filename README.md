# 🧠 JobTailor — Agentic AI Job Search and Resume Tailoring System

**JobTailor** is an intelligent Python + Tkinter desktop application that:
- Searches jobs online based on user keywords and location  
- Scores postings vs. your resume  
- Performs company research  
- Tailors your resume automatically with an AI model  
- Simulates ATS (Applicant Tracking System) scoring

---

## 🏗️ Project Structure

jobtailor_project/
│
├── jobtailor/
│ ├── agents/ # Autonomous agent logic (search, tailor, memory)
│ ├── core/ # Core NLP, parsing, scoring, ATS, tailoring
│ ├── gui/ # Tkinter GUI and views
│ ├── controller/ # Orchestrator and state handling
│ ├── workers/ # Background jobs, queues
│ ├── storage/ # DB, file, and cache management
│ └── utils/ # Common utilities, logging, errors
│
├── requirements.txt
├── setup.py
├── Makefile
└── README.md

yaml
Copy code

---

## ⚙️ Setup

```bash
git clone <your_repo_url>
cd jobtailor_project
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
make install
Create a .env file with:

ini
Copy code
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
🚀 Run
bash
Copy code
make run
Launches the Tkinter GUI.
You can upload a resume, enter job search parameters, and start the AI workflow.

🧪 Testing
Run the unit tests:

bash
Copy code
make test
🧩 Components
Layer	Description
GUI	Tkinter interface for upload, job results, and tailored resume preview
Agents	Orchestrate job search, tailoring, ATS simulation
Core	NLP parsing, similarity scoring, embeddings
Workers	Handles background processing and caching
Storage	Manages user resumes, company data, encryption
Utils	Logging, config, decorators, and error management

🔍 Extension Points
Replace scraping tools in agents/tools/scraping_tools.py with real job site APIs.

Enhance tailoring_engine.py prompt templates for better LLM guidance.

Integrate a real database (SQLite, PostgreSQL).

Add a resume visualizer and PDF export using reportlab.

🧭 Architecture Diagram
lua
Copy code
+------------------------------+
|        Tkinter GUI           |
|   (resume upload, results)   |
+--------------+---------------+
               |
               v
+------------------------------+
|     Controller / Orchestrator |
| Handles events, invokes agents|
+--------------+---------------+
               |
               v
+------------------------------+
|        AI Agents             |
| JobSearchAgent | TailorAgent |
+--------------+---------------+
               |
               v
+------------------------------+
|     Core NLP + Embeddings    |
| Similarity, Tailoring, ATS   |
+--------------+---------------+
               |
               v
+------------------------------+
|  Workers / Storage / Memory  |
|   Background saves, cache    |
+------------------------------+
🧩 License
MIT License © 2025 — Your Name

yaml
Copy code

---

### 🧠 5. Optional: Text-Based Class Diagram

You can visualize main components with this quick ASCII diagram:

AppOrchestrator
├──> JobSearchAgent
│ ├──> scraping_tools
│ └──> similarity_scorer
├──> TailoringAgent
│ ├──> tailoring_engine
│ ├──> llm_tools
│ └──> ats_simulator
├──> MemoryManager
│ └──> cache_manager
└──> GUI (Tkinter)