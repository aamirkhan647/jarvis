"""Very light GUI test: import main window factory."""

from gui.main_window import MainWindow
from controller.orchestrator import AppOrchestrator
import tkinter as tk


def test_mainwindow_init():
    root = tk.Tk()
    orch = AppOrchestrator()
    win = MainWindow(root, orch)
    assert win is not None
    root.destroy()
