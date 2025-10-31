import tkinter as tk
from gui.app_view import JobTailorApp


def main():
    """Initializes the Tkinter root and starts the main application loop."""
    root = tk.Tk()
    root.title("Agentic Job Tailor")
    root.geometry("1200x800")

    app = JobTailorApp(master=root)

    # Run the application
    app.mainloop()


if __name__ == "__main__":
    main()
