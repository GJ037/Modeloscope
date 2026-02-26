import tkinter as tk, os
from tkinter import ttk, filedialog, messagebox
from analyze import AnalyzerRunner
from interface.base_screen import BaseScreen


class AnalyzeInterface(BaseScreen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title="Analyzer")
        self.selected_file = tk.StringVar()
        self.build_content()

    def build_content(self):

        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(3, weight=1)

        # File Section
        file_frame = ttk.Frame(self.content)
        file_frame.grid(row=0, column=0, pady=10)

        ttk.Label(file_frame, text="Select Model:").pack(side="left", padx=5)

        ttk.Entry(
            file_frame,
            textvariable=self.selected_file,
            width=45
        ).pack(side="left", padx=5)

        ttk.Button(
            file_frame,
            text="Browse",
            width=12,
            command=self.browse_file
        ).pack(side="left", padx=5)

        # Run Button
        ttk.Button(
            self.content,
            text="Run Analysis",
            width=30,
            command=self.run_analysis
        ).grid(row=1, column=0, pady=15)

        # Output Label
        ttk.Label(
            self.content,
            text="Output",
            font=("Segoe UI", 10, "bold")
        ).grid(row=2, column=0, pady=(10, 5))

        # Expandable Output
        output_frame = ttk.Frame(self.content)
        output_frame.grid(row=3, column=0, sticky="nsew", padx=120)

        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.console = tk.Text(
            output_frame,
            state="disabled",
            wrap="word",
            bg="#f7f7f7"
        )
        self.console.grid(row=0, column=0, sticky="nsew")

        self.add_footer_button(
            "Return to Home",
            lambda: self.controller.show_frame("HomeInterface")
        )

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select 3D File",
            filetypes=[
                ("3D Models", "*.stl *.obj *.ply"),
                ("STL Files", "*.stl"),
                ("OBJ Files", "*.obj"),
                ("PLY Files", "*.ply")
            ]
        )
        if file_path:
            self.selected_file.set(file_path)

        valid_ext = (".stl", ".obj", ".ply")
        if not file_path.lower().endswith(valid_ext):
            messagebox.showerror("Invalid File", "Only STL, OBJ, and PLY files are supported.")
            return

    def run_analysis(self):
        file_path = self.selected_file.get().strip()

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Invalid File", "Please select a valid 3D model.")
            return

        try:
            runner = AnalyzerRunner(file_path)
            runner.run()
            messagebox.showinfo("Success", "Model analysis finished successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")