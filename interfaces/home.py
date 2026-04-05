from interfaces.screen import BaseScreen
from tkinter import ttk


class HomeInterface(BaseScreen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title="HOME")
        self.build_content()


    def build_content(self):
        self.content.columnconfigure(0, weight=1)

        container = ttk.Frame(self.content)
        container.pack(expand=True)

        ttk.Button(container, text="🔍 Analyze Model", width=30,
            command=lambda: self.controller.show_frame("AnalyzeInterface")
        ).pack(pady=15)

        ttk.Button(container, text="🎨 Render Model", width=30,
            command=lambda: self.controller.show_frame("RenderInterface")
        ).pack(pady=15)

        ttk.Button(container, text="🧪 Inspect Model", width=30,
            command=lambda: self.controller.show_frame("InspectInterface")
        ).pack(pady=15)

        self.add_footer_button(
            "❌ Exit Application",
            self.controller.exit_app
        )