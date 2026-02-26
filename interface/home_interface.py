from interface.base_screen import BaseScreen
from tkinter import ttk

class HomeInterface(BaseScreen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title="Home")
        self.build_content()

    def build_content(self):

        self.content.columnconfigure(0, weight=1)

        ttk.Button(
            self.content,
            text="Analyze Model",
            width=30,
            command=lambda: self.controller.show_frame("AnalyzeInterface")
        ).pack(pady=12)

        self.add_footer_button(
            "Exit Application",
            self.controller.exit_app
        )