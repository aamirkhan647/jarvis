"""Simple status bar for the GUI."""

import tkinter as tk
from tkinter import ttk


class StatusBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.var = tk.StringVar(value="Ready")
        self.label = ttk.Label(self, textvariable=self.var, anchor=tk.W)
        self.label.pack(fill=tk.X)

    def set(self, text: str):
        self.var.set(text)
