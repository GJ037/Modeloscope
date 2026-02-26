from tkinter import ttk


class BaseScreen(ttk.Frame):
    """
    BaseScreen

    Standard layout template for all UI screens.
    Provides:
        - Header
        - Expandable content area
        - Footer section
    """

    def __init__(self, parent, controller, title=""):
        super().__init__(parent)

        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Header
        self.header = ttk.Frame(self)
        self.header.grid(row=0, column=0, sticky="ew")

        ttk.Label(
            self.header,
            text=title,
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(50, 30))

        # Content
        self.content = ttk.Frame(self)
        self.content.grid(row=1, column=0, sticky="nsew")

        # Footer
        self.footer = ttk.Frame(self)
        self.footer.grid(row=2, column=0, sticky="ew", pady=30)

    def add_footer_button(self, text, command):
        """
        Add a button to footer section.
        """
        try:
            ttk.Button(
                self.footer,
                text=text,
                width=30,
                command=command
            ).pack(pady=5)
        except Exception as e:
            print(f"[BaseScreen ERROR] {e}")