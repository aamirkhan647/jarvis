"""Simple progress modal to show background work status."""

import tkinter as tk
from tkinter import ttk


class ProgressModal:
    def __init__(self, root, title="Working..."):
        self.top = tk.Toplevel(root)
        self.top.title(title)
        self.top.geometry("300x80")
        self.label = ttk.Label(self.top, text=title)
        self.label.pack(pady=10)
        self.pb = ttk.Progressbar(self.top, mode="indeterminate")
        self.pb.pack(fill=tk.X, padx=10, pady=6)
        self.top.transient(root)
        self.top.grab_set()
        self.pb.start(10)

    def close(self):
        try:
            self.pb.stop()
            self.top.destroy()
        except Exception:
            pass
