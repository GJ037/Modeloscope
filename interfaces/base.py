import tkinter as tk
from tkinter import ttk


class BaseInterface(tk.Tk):

    def __init__(self, title="Modeloscope_v3.2", size="1024x768"):
        super().__init__()

        self.current_frame = None

        self.base_title = title
        self.title(self.base_title)

        self.geometry(size)
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

        self.container = container
        self.frames = {}

    def set_title(self, model_name=None):
        if model_name:
            self.title(f"{self.base_title} | {model_name}")

        else:
            self.title(self.base_title)

    def add_frame(self, name, frame_class):
        frame = frame_class(self.container, self)
        self.frames[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        new_frame = self.frames.get(name)

        if not new_frame:
            raise ValueError(f"Frame '{name}' not found")

        if self.current_frame and hasattr(self.current_frame, "on_exit"):
            self.current_frame.on_exit()

        if hasattr(new_frame, "on_enter"):
            new_frame.on_enter()

        new_frame.tkraise()
        self.update_idletasks()
        self.current_frame = new_frame

    def exit_app(self):
        self.destroy()