import tkinter as tk
from tkinter import ttk


class BaseInterface(tk.Tk):
    """Main App window that manages navigation."""

    def __init__(self, title="Modeloscope", size="800x768"):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self.style.configure("TLabel", font=("Segoe UI", 10))

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

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