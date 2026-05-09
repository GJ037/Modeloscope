from tkinter import ttk


class BaseScreen(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._init_top_frame()
        self._init_bottom_frame()

    def _init_top_frame(self):
        self.top_frame = ttk.Frame(self)
        self.top_frame.grid(row=0, column=0, sticky="ew")

        self.top_frame.columnconfigure(0, weight=1)

    def _init_bottom_frame(self):
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")

        self.bottom_frame.columnconfigure(0, weight=1)
        self.bottom_frame.rowconfigure(0, weight=1)

    def set_loading(self, active: bool):
        self.controller.config(cursor="watch" if active else "")

    def apply_cursor(self, parent):
        stack = [parent]

        while stack:
            widget = stack.pop()

            cls = widget.winfo_class()
            if cls in (
                "TButton", "Button", "Checkbutton", "TCheckbutton", 
                "Radiobutton", "TRadiobutton", "Scrollbar", "Text"
                ):
                widget.config(cursor="arrow")

            stack.extend(widget.winfo_children())