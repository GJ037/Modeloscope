import tkinter as tk
from tkinter import ttk


class BaseInterface(tk.Tk):
    """Main App window that manages navigation."""

    def __init__(self, title="Modeloscope", size="1024x768"):
        super().__init__()
        self.title(title)
        self.geometry(size)

        # Make resizable
        self.resizable(True, True)
        self.minsize(1024, 768)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self.style.configure("TLabel", font=("Segoe UI", 10))

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")

        # Make window expand properly
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}
        self.container = container

    def add_frame(self, name, frame_class):
        frame = frame_class(self.container, self)
        self.frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()

    def exit_app(self):
        self.destroy()