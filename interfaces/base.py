import tkinter as tk
from tkinter import ttk


class BaseInterface(tk.Tk):
    """
    Main application controller responsible for managing all UI screens.

    Responsibilities:
    - Initializes the root application window
    - Registers and stores all interface screens (frames)
    - Handles navigation between screens
    - Ensures proper lifecycle handling (reset before display)
    - Acts as the central coordinator for UI flow

    Provides a unified structure for screen management and navigation
    across the entire application.
    """

    def __init__(self, title="Modeloscope_v2.2", size="1024x768"):
        super().__init__()

        self.title(title)
        self.geometry(size)
        self.resizable(True, True)
        self.minsize(1024, 768)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self.style.configure("TLabel", font=("Segoe UI", 10))

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}
        self.container = container

    def add_frame(self, name, frame_class):
        try:
            frame = frame_class(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        except Exception as e:
            print(f"[BaseInterface ERROR] Failed to add frame '{name}': {e}")

    def show_frame(self, name):
        try:
            frame = self.frames[name]
            if hasattr(frame, "reset"):
                frame.reset()
            frame.tkraise()
            self.update_idletasks()
            
        except Exception as e:
            print(f"[BaseInterface ERROR] {e}")

    def exit_app(self):
        try:
            self.destroy()
        except Exception as e:
            print(f"[BaseInterface ERROR] {e}")