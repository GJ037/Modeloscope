from tkinter import ttk

class HomeInterface(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()

    def build_ui(self):

        ttk.Label(
            self,
            text="Home",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(40, 20))

        ttk.Button(
            self,
            text="Analyze Model",
            width=30,
            command=lambda: self.controller.show_frame("AnalyzeInterface")
        ).pack(pady=12)

        ttk.Button(
            self,
            text="Exit Application",
            width=30,
            command=self.controller.exit_app
        ).pack(pady=12)