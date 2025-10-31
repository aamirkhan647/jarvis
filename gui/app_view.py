import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
from core.orchestrator import Orchestrator
from tools.resume_parser import (
    parse_resume,
)  # Note: Need to adjust this tool for file path handling
from models.job_data import JobPost, Scorecard


class JobTailorApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.orchestrator = Orchestrator()
        self.base_resume_text = ""
        self.jobs_found = []  # List of (JobPost, Scorecard) tuples
        self.current_tailoring_job: JobPost | None = None
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_widgets()

    def create_widgets(self):
        # Configure layout using PanedWindow for flexible resizing
        self.paned_window = tk.PanedWindow(
            self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED
        )
        self.paned_window.pack(fill="both", expand=True)

        # --- Left Frame: Controls (Search and Resume) ---
        self.control_frame = ttk.Frame(self.paned_window, padding="10")
        self.paned_window.add(self.control_frame, width=350)
        self.create_control_widgets(self.control_frame)

        # --- Right Frame: Results (Job List) ---
        self.results_frame = ttk.Frame(self.paned_window, padding="10")
        self.paned_window.add(self.results_frame)
        self.create_results_widgets(self.results_frame)

        # Initialize the Job Results area (Treeview)
        self.job_treeview.bind("<<TreeviewSelect>>", self.on_job_select)

    def create_control_widgets(self, parent):
        # Resume Input Section
        ttk.Label(parent, text="1. Base Resume").pack(pady=(5, 0), anchor="w")
        self.resume_path_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.resume_path_var, state="readonly").pack(
            fill="x", pady=5
        )
        ttk.Button(parent, text="Upload Resume File", command=self.upload_resume).pack(
            fill="x", pady=5
        )

        # Resume Text Display (Hidden/Minimized)
        ttk.Label(parent, text="Resume Text Preview:").pack(pady=(10, 0), anchor="w")
        self.resume_text_preview = scrolledtext.ScrolledText(
            parent, height=6, wrap=tk.WORD, state=tk.DISABLED
        )
        self.resume_text_preview.pack(fill="x", pady=5)

        # Search Criteria Section
        ttk.Label(parent, text="2. Search Criteria").pack(pady=(20, 0), anchor="w")

        ttk.Label(parent, text="Keywords:").pack(pady=(5, 0), anchor="w")
        self.keywords_var = tk.StringVar(value="Agentic AI Engineer")
        ttk.Entry(parent, textvariable=self.keywords_var).pack(fill="x", pady=5)

        ttk.Label(parent, text="Location:").pack(pady=(5, 0), anchor="w")
        self.location_var = tk.StringVar(value="Remote")
        ttk.Entry(parent, textvariable=self.location_var).pack(fill="x", pady=5)

        self.search_button = ttk.Button(
            parent, text="Start Job Search & Scoring", command=self.run_search_thread
        )
        self.search_button.pack(fill="x", pady=15)

        # Status Bar
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(
            parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor="w"
        ).pack(side="bottom", fill="x", pady=(10, 0))

    def create_results_widgets(self, parent):
        # Job Listing Treeview
        ttk.Label(parent, text="3. Scored Job Results (Click to View/Tailor)").pack(
            pady=(5, 10), anchor="w"
        )

        columns = ("Score", "Title", "Company", "Location", "Rationale")
        self.job_treeview = ttk.Treeview(parent, columns=columns, show="headings")

        for col in columns:
            self.job_treeview.heading(
                col, text=col, command=lambda c=col: self.sort_treeview(c)
            )
            self.job_treeview.column(col, width=100)  # Default width

        self.job_treeview.column("Score", width=50, anchor="center")
        self.job_treeview.column("Rationale", width=200)

        self.job_treeview.pack(fill="both", expand=True)

        # Separator
        ttk.Separator(parent, orient="horizontal").pack(fill="x", pady=10)

        # Tailoring Section (Detailed View)
        self.tailor_title = ttk.Label(parent, text="Selected Job Details:")
        self.tailor_title.pack(pady=(5, 0), anchor="w")

        self.tailoring_notebook = ttk.Notebook(parent)
        self.tailoring_notebook.pack(fill="both", expand=True)

        # Tab 1: Tailoring Controls
        self.tab_controls = ttk.Frame(self.tailoring_notebook)
        self.tailoring_notebook.add(self.tab_controls, text="Tailor & Validate")
        self.create_tailor_controls(self.tab_controls)

        # Tab 2: Tailored Resume Output
        self.tab_output = ttk.Frame(self.tailoring_notebook)
        self.tailoring_notebook.add(self.tab_output, text="Tailored Output")
        self.create_output_widgets(self.tab_output)

    def create_tailor_controls(self, parent):
        self.job_details_text = scrolledtext.ScrolledText(
            parent, height=10, wrap=tk.WORD, state=tk.DISABLED
        )
        self.job_details_text.pack(fill="x", pady=5)

        self.tailor_button = ttk.Button(
            parent,
            text="Generate Tailored Resume",
            command=self.run_tailor_thread,
            state=tk.DISABLED,
        )
        self.tailor_button.pack(pady=10)

        self.ats_confidence_var = tk.StringVar(value="ATS Confidence: N/A")
        ttk.Label(
            parent, textvariable=self.ats_confidence_var, font=("Arial", 12, "bold")
        ).pack(pady=5)

        ttk.Label(parent, text="Validation Feedback:").pack(pady=(10, 0), anchor="w")
        self.ats_feedback_text = scrolledtext.ScrolledText(
            parent, height=5, wrap=tk.WORD, state=tk.DISABLED
        )
        self.ats_feedback_text.pack(fill="x", pady=5)

        self.save_button = ttk.Button(
            parent,
            text="Save Tailored Resume",
            command=self.save_tailored_resume,
            state=tk.DISABLED,
        )
        self.save_button.pack(pady=10)

    def create_output_widgets(self, parent):
        self.tailored_resume_text = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, state=tk.DISABLED
        )
        self.tailored_resume_text.pack(fill="both", expand=True)

    # --- Action Handlers ---

    def upload_resume(self):
        """Opens a file dialog for resume upload."""
        filepath = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("PDF files", "*.pdf"),
                ("Word documents", "*.docx"),
                ("All files", "*.*"),
            ],
        )
        if filepath:
            # --- Change is here ---
            parsed_result = parse_resume(filepath)

            if parsed_result is None:
                messagebox.showerror("File Error", "File path is invalid or empty.")
                self.status_var.set("Error loading resume.")
                return

            if parsed_result.startswith("Error:"):
                messagebox.showerror("Parsing Error", parsed_result)
                self.status_var.set(f"Error: {parsed_result}")
                return

            # If we reach here, parsing was successful
            self.resume_path_var.set(filepath)
            self.base_resume_text = parsed_result

            # Update preview text
            self.resume_text_preview.config(state=tk.NORMAL)
            self.resume_text_preview.delete("1.0", tk.END)
            self.resume_text_preview.insert(
                tk.END,
                self.base_resume_text[:500]
                + ("..." if len(self.base_resume_text) > 500 else ""),
            )
            self.resume_text_preview.config(state=tk.DISABLED)

            self.status_var.set("Resume loaded and parsed successfully.")

    def run_search_thread(self):
        """Runs the search and scoring in a separate thread to keep the GUI responsive."""
        if not self.base_resume_text:
            messagebox.showerror(
                "Input Required", "Please upload or provide resume text first."
            )
            return

        self.search_button.config(state=tk.DISABLED)
        self.status_var.set("Searching and analyzing jobs... (Please wait)")

        keywords = self.keywords_var.get()
        location = self.location_var.get()

        thread = threading.Thread(
            target=self._execute_search, args=(keywords, location)
        )
        thread.start()

    def _execute_search(self, keywords, location):
        """Executed in the background thread."""
        try:
            self.jobs_found = self.orchestrator.run_initial_search(
                keywords, location, self.base_resume_text
            )
            self.master.after(0, self.update_job_treeview)
        except Exception as e:
            self.master.after(
                0,
                lambda: messagebox.showerror(
                    "Search Error", f"An error occurred during search: {e}"
                ),
            )
        finally:
            self.master.after(0, lambda: self.search_button.config(state=tk.NORMAL))
            self.master.after(
                0,
                lambda: self.status_var.set(
                    f"Search complete. Found {len(self.jobs_found)} jobs."
                ),
            )

    def update_job_treeview(self):
        """Updates the Treeview widget on the main thread."""
        self.job_treeview.delete(*self.job_treeview.get_children())

        # Sort by score descending
        sorted_jobs = sorted(
            self.jobs_found, key=lambda x: x[1].relevance_score, reverse=True
        )

        for job, score in sorted_jobs:
            self.job_treeview.insert(
                "",
                tk.END,
                iid=job.link,
                values=(
                    score.relevance_score,
                    job.title,
                    job.company,
                    job.location,
                    score.rationale[:50] + "...",
                ),
            )

    def on_job_select(self, event):
        """Called when a job is selected in the treeview."""
        selected_item = self.job_treeview.selection()
        if not selected_item:
            return

        job_link = selected_item[0]
        # Find the selected job and its score
        job_tuple = next(
            ((j, s) for j, s in self.jobs_found if j.link == job_link), None
        )

        if job_tuple:
            self.current_tailoring_job, score = job_tuple

            # Display job details
            self.tailor_title.config(
                text=f"Selected Job: {self.current_tailoring_job.title} ({self.current_tailoring_job.company})"
            )
            self.job_details_text.config(state=tk.NORMAL)
            self.job_details_text.delete("1.0", tk.END)
            self.job_details_text.insert(
                tk.END,
                f"Score: {score.relevance_score}/100\n\n{self.current_tailoring_job.raw_description}",
            )
            self.job_details_text.config(state=tk.DISABLED)

            self.tailor_button.config(state=tk.NORMAL)
            self.ats_confidence_var.set("ATS Confidence: N/A")
            self.ats_feedback_text.config(state=tk.NORMAL)
            self.ats_feedback_text.delete("1.0", tk.END)
            self.ats_feedback_text.config(state=tk.DISABLED)
            self.save_button.config(state=tk.DISABLED)
            self.tailoring_notebook.select(self.tab_controls)

    def run_tailor_thread(self):
        """Runs the tailoring and validation in a separate thread."""
        self.tailor_button.config(state=tk.DISABLED)
        self.status_var.set(
            f"Generating tailored resume for {self.current_tailoring_job.company}..."
        )
        self.save_button.config(state=tk.DISABLED)

        thread = threading.Thread(target=self._execute_tailoring)
        thread.start()

    def _execute_tailoring(self):
        """Executed in the background thread."""
        try:
            tailored_resume, ats_score = self.orchestrator.process_tailoring(
                self.current_tailoring_job, self.base_resume_text
            )

            # Update GUI on the main thread
            self.master.after(
                0, lambda: self.display_tailoring_results(tailored_resume, ats_score)
            )
        except Exception as e:
            self.master.after(
                0,
                lambda: messagebox.showerror(
                    "Tailoring Error", f"An error occurred: {e}"
                ),
            )
        finally:
            self.master.after(0, lambda: self.tailor_button.config(state=tk.NORMAL))
            self.master.after(
                0, lambda: self.status_var.set("Tailoring and validation complete.")
            )
            self.master.after(
                0, lambda: self.tailoring_notebook.select(self.tab_output)
            )

    def display_tailoring_results(self, tailored_resume, ats_score):
        # Update Tailored Resume Tab
        self.tailored_resume_text.config(state=tk.NORMAL)
        self.tailored_resume_text.delete("1.0", tk.END)
        self.tailored_resume_text.insert(tk.END, tailored_resume)
        self.tailored_resume_text.config(state=tk.DISABLED)

        # Update Validation Tab
        self.ats_confidence_var.set(f"ATS Confidence: {ats_score.ats_pass_confidence}%")
        self.ats_feedback_text.config(state=tk.NORMAL)
        self.ats_feedback_text.delete("1.0", tk.END)
        self.ats_feedback_text.insert(
            tk.END,
            f"Keyword Match: {ats_score.keyword_match_score}%\n"
            f"Formatting Hygiene: {ats_score.formatting_hygiene}%\n\n"
            f"Recommendations: {', '.join(ats_score.recommendations_for_fix)}",
        )
        self.ats_feedback_text.config(state=tk.DISABLED)

        self.save_button.config(state=tk.NORMAL)

    def save_tailored_resume(self):
        """Saves the displayed tailored resume to a file."""
        if not self.tailored_resume_text.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "No tailored resume generated yet.")
            return

        default_name = f"resume_tailored_for_{self.current_tailoring_job.company.replace(' ', '_')}.txt"

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text files", "*.txt"), ("Markdown files", "*.md")],
        )

        if filepath:
            try:
                content = self.tailored_resume_text.get("1.0", tk.END)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                self.status_var.set(f"Resume successfully saved to {filepath}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file: {e}")

    # Helper function for sorting treeview columns
    def sort_treeview(self, col):
        # Simplistic sort implementation (can be complex depending on data type)
        l = [
            (self.job_treeview.set(k, col), k)
            for k in self.job_treeview.get_children("")
        ]
        # Try to convert score column to integer for correct sorting
        try:
            l.sort(key=lambda t: int(t[0]), reverse=True)
        except ValueError:
            l.sort(reverse=True)  # Fallback to alphabetical sort

        for index, (val, k) in enumerate(l):
            self.job_treeview.move(k, "", index)
