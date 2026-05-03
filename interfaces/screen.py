from tkinter import ttk


class BaseScreen(ttk.Frame):

    def __init__(self, parent, controller, title=""):
        super().__init__(parent)

        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._init_header(title)
        self._init_content()
        self._init_footer()

    def _init_header(self, title):
        if not title:
            self.header = None
            return

        self.header = ttk.Frame(self)
        self.header.grid(row=0, column=0, sticky="ew")

        ttk.Label(self.header,text=title,
            font=("Segoe UI", 28, "bold")).pack(pady=(50, 30))

    def _init_content(self):
        self.content = ttk.Frame(self)
        self.content.grid(row=1, column=0, sticky="nsew")

    def set_loading(self, active: bool):
        if active:
            self.controller.config(cursor="watch")
        else:
            self.controller.config(cursor="")

    def _init_footer(self):
        self.footer = ttk.Frame(self)
        self.footer.grid(row=3, column=0, sticky="ew",padx=120, pady=10)

    def set_footer(self, text, command):
        ttk.Button(self.footer, text=text, width=30, command=command)\
            .pack(pady=10)

    def apply_cursor(self, parent):
        stack = [parent]

        while stack:
            widget = stack.pop()

            cls = widget.winfo_class()
            if cls in ("TButton", "Button", "Checkbutton", "TCheckbutton",
                    "Radiobutton", "TRadiobutton", "Scrollbar", "Text"):
                widget.config(cursor="arrow")

            stack.extend(widget.winfo_children())