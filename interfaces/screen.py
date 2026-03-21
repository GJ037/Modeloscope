from tkinter import ttk


class BaseScreen(ttk.Frame):
    """
    Abstract base class for all UI screens.

    Responsibilities:
    - Provides a common layout structure (header, content, footer)
    - Standardizes screen initialization and styling
    - Offers reusable UI components such as footer buttons
    - Defines a reset() method for clearing screen state

    Ensures consistency, reusability, and maintainability across all
    interface screens.
    """

    def __init__(self, parent, controller, title=""):
        super().__init__(parent)

        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        if title:
            self.header = ttk.Frame(self)
            self.header.grid(row=0, column=0, sticky="ew")

            ttk.Label(
                self.header,
                text=title,
                font=("Segoe UI", 28, "bold")
            ).pack(pady=(50, 30))

        self.content = ttk.Frame(self)
        self.content.grid(row=1, column=0, sticky="nsew")

        self.footer = ttk.Frame(self)
        self.footer.grid(row=2, column=0, sticky="ew", pady=30)

    def add_footer_button(self, text, command):
        try:
            ttk.Button(
                self.footer,
                text=text,
                width=30,
                command=command
            ).pack(pady=5)
        except Exception as e:
            print(f"[BaseScreen ERROR] {e}")