"""Minimal Tkinter GUI that integrates with AppOrchestrator."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from utils.logger import get_logger
from storage.database import init_db

logger = get_logger(__name__)


class MainWindow:
    def __init__(self, root, orchestrator):
        self.root = root
        self.orch = orchestrator
        self._build_ui()
        init_db()

    def _build_ui(self):
        # Top frame: upload resume
        top = ttk.Frame(self.root, padding=10)
        top.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(top, text="Resume file or raw text:").pack(anchor=tk.W)
        self.resume_path_var = tk.StringVar()
        entry = ttk.Entry(top, textvariable=self.resume_path_var, width=60)
        entry.pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(top, text="Browse", command=self.browse_resume).pack(side=tk.LEFT)

        # Search frame
        search_frame = ttk.Frame(self.root, padding=10)
        search_frame.pack(fill=tk.X)
        ttk.Label(search_frame, text="Keywords:").grid(row=0, column=0, sticky=tk.W)
        self.keywords_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.keywords_var, width=30).grid(
            row=0, column=1, padx=6
        )

        ttk.Label(search_frame, text="Location:").grid(row=0, column=2, sticky=tk.W)
        self.location_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.location_var, width=20).grid(
            row=0, column=3, padx=6
        )

        ttk.Button(search_frame, text="Search", command=self.on_search).grid(
            row=0, column=4, padx=10
        )

        # Results
        results_frame = ttk.Frame(self.root, padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        self.results_list = tk.Listbox(results_frame, height=12)
        self.results_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(
            results_frame, orient=tk.VERTICAL, command=self.results_list.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_list.config(yscrollcommand=scrollbar.set)
        self.results_list.bind("<Double-Button-1>", self.on_select_job)

    def browse_resume(self):
        filetypes = [
            ("Text files", "*.txt"),
            ("PDF", "*.pdf"),
            ("Word", "*.docx"),
            ("All files", "*.*"),
        ]
        path = filedialog.askopenfilename(
            title="Select resume file", filetypes=filetypes
        )
        if path:
            self.resume_path_var.set(path)

    def on_search(self):
        resume = self.resume_path_var.get().strip()
        keywords = self.keywords_var.get().strip() or "Data Scientist"
        location = self.location_var.get().strip() or "Remote"
        try:
            jobs = self.orch.search_jobs(
                resume=resume, keywords=keywords, location=location
            )
            self.results_list.delete(0, tk.END)
            for j in jobs:
                title = j.get("title", "No Title")
                company = j.get("company", "Unknown")
                score = j.get("score", 0)
                display = f"{title} — {company} (score: {score})"
                self.results_list.insert(tk.END, display)
            if not jobs:
                messagebox.showinfo("No results", "No jobs matched the threshold.")
        except Exception as e:
            logger.exception("Search failed")
            messagebox.showerror("Search error", str(e))

    def on_select_job(self, event):
        sel = self.results_list.curselection()
        if not sel:
            return
        idx = sel[0]
        # For simplicity, re-run search to get job object list (in a real app keep state)
        resume = self.resume_path_var.get().strip()
        keywords = self.keywords_var.get().strip() or "Data Scientist"
        location = self.location_var.get().strip() or "Remote"
        jobs = self.orch.search_jobs(
            resume=resume, keywords=keywords, location=location
        )
        job = jobs[idx] if idx < len(jobs) else None
        if job:
            tailored, score, notes = self.orch.tailor_resume_for_job(
                resume=resume, job=job
            )
            # Display a simple dialog
            msg = f"Predicted ATS score: {score}\n\nNotes:\n" + (
                "\n".join(notes) if notes else "None"
            )
            messagebox.showinfo("Tailored result", msg)

    def on_close(self):
        # perform cleanup if needed
        try:
            self.root.destroy()
        except Exception:
            pass
