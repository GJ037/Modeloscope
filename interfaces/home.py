from interfaces.screen import BaseScreen
from tkinter import ttk


class HomeInterface(BaseScreen):
    """
    Landing screen of the application.

    Responsibilities:
    - Serves as the main navigation hub for the user
    - Provides entry points to Analyze, Render, and future Inspect features
    - Displays primary actions in a clear and accessible layout
    - Allows exiting the application

    Acts as a simple, user-friendly dashboard guiding users to different
    functional modules of the system.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title="HOME")
        self.build_content()

    def build_content(self):
        try:
            self.content.columnconfigure(0, weight=1)

            ttk.Button(
                self.content,
                text="🔍 Analyze Model",
                width=30,
                command=lambda: self.controller.show_frame("AnalyzeInterface")
            ).pack(pady=15)

            ttk.Button(
                self.content,
                text="🎨 Render Model",
                width=30,
                command=lambda: self.controller.show_frame("RenderInterface")
            ).pack(pady=15)

            ttk.Button(
                self.content,
                text="🧪 Inspect Model",
                width=30,
                command=lambda: self.controller.show_frame("InspectInterface")
            ).pack(pady=15)

            self.add_footer_button(
                "❌ Exit Application",
                self.controller.exit_app
            )

        except Exception as e:
            print(f"[HomeInterface ERROR] {e}")