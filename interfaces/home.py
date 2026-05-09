from interfaces.screen import BaseScreen
from tkinter import ttk


class HomeInterface(BaseScreen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.build_content()

    def build_content(self):
        button_frame = ttk.Frame(self.bottom_frame)
        button_frame.grid(row=0, column=0)

        ttk.Button(button_frame, text="🔍 Analyze Model", width=30,
            command=lambda: self.controller.show_frame("AnalyzeInterface")
        ).pack(pady=15)

        ttk.Button(button_frame, text="🎨 Render Model", width=30,
            command=lambda: self.controller.show_frame("RenderInterface")
        ).pack(pady=15)

        ttk.Button(button_frame, text="🧪 Inspect Model", width=30,
            command=lambda: self.controller.show_frame("InspectInterface")
        ).pack(pady=15)

        navigation_frame = ttk.Frame(self.bottom_frame)
        navigation_frame.grid(row=1, column=0, pady=10)

        ttk.Button(navigation_frame, text="❌ Exit Application", width=30,
                   command=self.controller.exit_app).pack()

        self.apply_cursor(self)