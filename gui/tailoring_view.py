"""View to display tailored resume and ATS score."""

import tkinter as tk
from tkinter import ttk, scrolledtext


class TailoringView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Tailored Resume Preview").pack(anchor=tk.W)
        self.text = scrolledtext.ScrolledText(self, height=20, width=80)
        self.text.pack(fill=tk.BOTH, expand=True)
        self.ats_label = ttk.Label(self, text="ATS Score: N/A")
        self.ats_label.pack(anchor=tk.W, pady=(6, 0))

    def show_tailored(self, tailored: dict, ats_score: int, notes: list = None):
        self.text.delete("1.0", tk.END)
        display_text = (
            tailored.get("text") if isinstance(tailored, dict) else str(tailored)
        )
        self.text.insert(tk.END, display_text)
        self.ats_label.config(text=f"ATS Score: {ats_score}")
        if notes:
            self.text.insert(tk.END, "\n\nATS Notes:\n" + "\n".join(notes))
