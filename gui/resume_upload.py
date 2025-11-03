"""GUI helper for uploading and previewing resumes (Tkinter)."""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext


class ResumeUploadDialog:
    def __init__(self, parent):
        self.parent = parent
        self.path = None

    def show(self):
        filetypes = [("PDF", "*.pdf"), ("Word", "*.docx"), ("Text", "*.txt")]
        path = filedialog.askopenfilename(title="Select resume", filetypes=filetypes)
        if path:
            self.path = path
        return self.path

    @staticmethod
    def preview_text(path: str):
        # naive preview: read text file if possible
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return f"Preview not available for {path}"
