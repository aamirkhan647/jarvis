# gui/main_window.py
"""
Tkinter GUI for JARVIS (Job search, ranking, tailoring).
This is a compact GUI that uses core modules.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.simpledialog import askstring
from pathlib import Path
import threading
import logging
import os

from core.utils import load_config
from core.resume_parser import extract_text
from core.job_fetcher import RSSFetcher, SimpleScraper, AdzunaFetcher
from core.ranker import rank_jobs
from core.tailor import create_docx
from core.utils import ROOT

logger = logging.getLogger(__name__)


class JobFinderApp(tk.Tk):
    def __init__(self, config):
        super().__init__()
        self.title("JARVIS — Job Application & Resume Virtual Intelligence System")
        self.geometry("1000x700")
        self.config_data = config
        self.saved_root = Path(self.config_data.get("saved_folder"))
        self.saved_root.mkdir(parents=True, exist_ok=True)
        self.resume_text = ""
        self.jobs = []
        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)
        ttk.Button(top, text="Load Resume", command=self.load_resume).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Label(top, text="Query:").pack(side=tk.LEFT, padx=(12, 0))
        self.query_var = tk.StringVar(value=self.config_data.get("job_query", ""))
        ttk.Entry(top, textvariable=self.query_var, width=40).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Search Now", command=self.search_now).pack(
            side=tk.LEFT, padx=6
        )
        ttk.Button(top, text="Open Saved Folder", command=self.open_saved_folder).pack(
            side=tk.LEFT, padx=6
        )

        main = ttk.Frame(self)
        main.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        left = ttk.Frame(main)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree = ttk.Treeview(left, columns=("company", "score"), show="headings")
        self.tree.heading("company", text="Company")
        self.tree.heading("score", text="Score")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_job_select)

        right = ttk.Frame(main, width=420)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        ttk.Label(right, text="Job Details").pack(anchor=tk.W)
        self.details = ScrolledText(right, height=20)
        self.details.pack(fill=tk.BOTH, expand=True)
        ttk.Button(
            right,
            text="Generate Tailored Resume (DOCX)",
            command=self.generate_tailored,
        ).pack(fill=tk.X, pady=6)
        ttk.Button(
            right,
            text="Generate + Convert to PDF (requires Word)",
            command=lambda: self.generate_tailored(as_pdf=True),
        ).pack(fill=tk.X, pady=2)
        ttk.Button(
            right, text="Auto-apply (Disabled)", command=self.auto_apply_disabled
        ).pack(fill=tk.X, pady=2)

        self.status = tk.StringVar(value="Idle")
        ttk.Label(self, textvariable=self.status).pack(side=tk.BOTTOM, fill=tk.X)

    def load_resume(self):
        path = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[("PDF/DOCX", "*.pdf *.docx"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            text = extract_text(path)
            if not text.strip():
                messagebox.showwarning(
                    "Empty", "No text could be extracted from the resume."
                )
                return
            self.resume_text = text
            self.status.set(f"Loaded resume: {Path(path).name}")
            messagebox.showinfo("Loaded", f"Loaded resume ({Path(path).name})")
        except Exception as e:
            logger.exception("Failed to load resume: %s", e)
            messagebox.showerror("Error", str(e))

    def search_now(self):
        q = self.query_var.get().strip()
        if not q:
            messagebox.showwarning("No query", "Please enter a job query.")
            return
        threading.Thread(target=self._search_thread, args=(q,), daemon=True).start()

    def _search_thread(self, query):
        self.status.set("Searching...")
        jobs = []
        # RSS feeds
        for feed in self.config_data.get("rss_feeds", []):
            try:
                jobs.extend(RSSFetcher.fetch(feed, limit=40))
            except Exception:
                pass
        # Simple scrape remoteok
        try:
            jobs.extend(SimpleScraper.scrape_remoteok(query, limit=30))
        except Exception:
            pass
        # Adzuna if keys present
        if self.config_data.get("adzuna_app_id") and self.config_data.get(
            "adzuna_api_key"
        ):
            try:
                adz = AdzunaFetcher(
                    self.config_data["adzuna_app_id"],
                    self.config_data["adzuna_api_key"],
                    country="gb",
                )
                jobs.extend(
                    adz.search(
                        query, self.config_data.get("location", ""), results_per_page=20
                    )
                )
            except Exception:
                pass
        # dedupe
        seen = {}
        uniq = []
        for j in jobs:
            key = (
                j.get("id")
                or j.get("link")
                or (j.get("title") + (j.get("company") or ""))
            )
            if not key:
                continue
            if key in seen:
                continue
            seen[key] = True
            uniq.append(j)
        self.jobs = uniq
        # rank
        if self.resume_text:
            ranked = rank_jobs(self.jobs, self.resume_text, top_k=100)
        else:
            for j in self.jobs:
                j["score"] = 0.0
            ranked = self.jobs
        self.jobs = ranked
        # update UI
        self.tree.delete(*self.tree.get_children())
        for idx, j in enumerate(self.jobs):
            comp = j.get("company") or ""
            score = f"{j.get('score', 0):.3f}"
            self.tree.insert(
                "", "end", iid=str(idx), values=(comp, score), text=j.get("title")
            )
        self.status.set(f"Found {len(self.jobs)} jobs.")

    def on_job_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        j = self.jobs[idx]
        txt = f"{j.get('title')}\nCompany: {j.get('company')}\nLink: {j.get('link')}\nScore: {j.get('score')}\n\n{j.get('description')}"
        self.details.delete("1.0", "end")
        self.details.insert("1.0", txt)

    def generate_tailored(self, as_pdf=False):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No job", "Select a job first.")
            return
        if not self.resume_text:
            messagebox.showwarning("No resume", "Load your resume first.")
            return
        idx = int(sel[0])
        job = self.jobs[idx]
        job_id = (job.get("id") or job.get("link") or job.get("title"))[:120]
        safe_id = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in job_id)
        folder = self.saved_root / safe_id
        folder.mkdir(parents=True, exist_ok=True)
        from datetime import datetime

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        docx_path = folder / f"tailored_{ts}.docx"
        name = (
            askstring(
                "Name for resume",
                "Enter the full name to display on the tailored resume:",
                parent=self,
            )
            or "Your Name"
        )
        self.status.set("Generating tailored resume...")
        try:
            create_docx(
                self.resume_text,
                (job.get("description") or "") + " " + (job.get("title") or ""),
                str(docx_path),
                name=name,
            )
            if as_pdf:
                # attempt conversion using docx2pdf (requires Word on Windows)
                try:
                    from docx2pdf import convert

                    pdf_path = str(folder / f"tailored_{ts}.pdf")
                    convert(str(docx_path), pdf_path)
                    messagebox.showinfo("Saved", f"SAVED: {docx_path}\n{pdf_path}")
                except Exception as e:
                    messagebox.showinfo(
                        "Saved",
                        f"SAVED DOCX: {docx_path}\n(PDF conversion failed: {e})",
                    )
            else:
                messagebox.showinfo("Saved", f"SAVED DOCX: {docx_path}")
            self.status.set(f"Saved tailored resume to {folder}")
        except Exception as e:
            logger.exception("Tailoring failed: %s", e)
            messagebox.showerror("Error", str(e))
            self.status.set("Error generating tailored resume.")

    def auto_apply_disabled(self):
        messagebox.showinfo(
            "Auto-apply disabled",
            "Automatic application is disabled by default due to Terms of Service and security concerns. See core/auto_apply.py for a safe stub.",
        )

    def open_saved_folder(self):
        os.startfile(str(self.saved_root))
