"""Very small diff viewer (line-by-line) for original vs tailored resume."""

import tkinter as tk
from tkinter import ttk, scrolledtext
import difflib


class DiffViewer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.left = scrolledtext.ScrolledText(self, height=20, width=40)
        self.left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right = scrolledtext.ScrolledText(self, height=20, width=40)
        self.right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def show_diff(self, original: str, tailored: str):
        # naive diff
        orig_lines = original.splitlines()
        tail_lines = tailored.splitlines()
        diff = difflib.unified_diff(orig_lines, tail_lines, lineterm="")
        diff_text = "\n".join(diff)
        self.left.delete("1.0", tk.END)
        self.right.delete("1.0", tk.END)
        self.left.insert(tk.END, original)
        self.right.insert(tk.END, tailored)
