"""Encapsulated list view widget for job results."""

import tkinter as tk
from tkinter import ttk


class JobListView(ttk.Frame):
    def __init__(self, parent, select_callback=None):
        super().__init__(parent)
        self.select_callback = select_callback
        self.listbox = tk.Listbox(self, height=12)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.listbox.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.bind("<Double-Button-1>", self._on_double_click)
        self._items = []

    def set_items(self, jobs):
        self._items = jobs or []
        self.listbox.delete(0, tk.END)
        for j in self._items:
            title = j.get("title", "No Title")
            company = j.get("company", "Unknown")
            score = j.get("score", 0)
            display = f"{title} — {company} (score: {score})"
            self.listbox.insert(tk.END, display)

    def _on_double_click(self, event):
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if self.select_callback:
            self.select_callback(idx, self._items[idx])
