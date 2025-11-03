"""Entry point: Launches the Tkinter GUI and initializes the orchestrator."""

import tkinter as tk
from gui.main_window import MainWindow
from controller.orchestrator import AppOrchestrator
from utils.logger import setup_logging


def main():
    setup_logging()
    root = tk.Tk()
    root.title("JobTailor — AI Job Search & Resume Tailoring")
    # Initialize orchestrator (controller => agents)
    orchestrator = AppOrchestrator()
    app = MainWindow(root, orchestrator)
    root.protocol("WM_DELETE_WINDOW", lambda: app.on_close())
    root.mainloop()


if __name__ == "__main__":
    main()
