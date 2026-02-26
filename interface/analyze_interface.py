import tkinter as tk
import os
from tkinter import ttk, filedialog, messagebox
from analyze import AnalyzerRunner
from interface.base_screen import BaseScreen


class AnalyzeInterface(BaseScreen):
    """
    AnalyzeInterface

    Screen responsible for:
        - Selecting a 3D model file
        - Running analysis
        - Displaying structured output
    """

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title="Analyzer")
        self.selected_file = tk.StringVar()
        self.build_content()

    def build_content(self):
        try:
            self.content.columnconfigure(0, weight=1)
            self.content.rowconfigure(3, weight=1)

            # File selection
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

            # Run button
            ttk.Button(
                self.content,
                text="Run Analysis",
                width=30,
                command=self.run_analysis
            ).grid(row=1, column=0, pady=15)

            # Output label
            ttk.Label(
                self.content,
                text="Output",
                font=("Segoe UI", 10, "bold")
            ).grid(row=2, column=0, pady=(10, 5))

            # Console area
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

        except Exception as e:
            print(f"[AnalyzeInterface ERROR] {e}")

    def browse_file(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select 3D File",
                filetypes=[
                    ("3D Models", "*.stl *.obj *.ply"),
                    ("STL Files", "*.stl"),
                    ("OBJ Files", "*.obj"),
                    ("PLY Files", "*.ply")
                ]
            )

            if not file_path:
                return

            valid_ext = (".stl", ".obj", ".ply")
            if not file_path.lower().endswith(valid_ext):
                messagebox.showerror(
                    "Invalid File",
                    "Only STL, OBJ, and PLY files are supported."
                )
                return

            self.selected_file.set(file_path)

        except Exception as e:
            messagebox.showerror("Browse Error", str(e))

    def run_analysis(self):
        file_path = self.selected_file.get().strip()

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror(
                "Invalid File",
                "Please select a valid 3D model."
            )
            return

        try:
            runner = AnalyzerRunner(file_path)
            report = runner.run()

            if report is None:
                messagebox.showerror(
                    "Analysis Failed",
                    "Model analysis could not be completed."
                )
                return

        except Exception as e:
            messagebox.showerror("Analysis Error", str(e))

    def display_report(self, report):
        try:
            self.console.config(state="normal")
            self.console.delete("1.0", tk.END)

            for section, data in report.items():
                self.console.insert(tk.END, f"{section}\n")
                self.console.insert(tk.END, "-" * 40 + "\n")

                if isinstance(data, dict):
                    for key, value in data.items():
                        self.console.insert(tk.END, f"{key}: {value}\n")

                self.console.insert(tk.END, "\n")

            self.console.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Display Error", str(e))