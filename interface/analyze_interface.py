import tkinter as tk, os
from tkinter import ttk, filedialog, messagebox
from interface.base_screen import BaseScreen
from analyze import AnalyzerRunner

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
            self.content.rowconfigure(4, weight=1)

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
            
            toggle_frame = ttk.LabelFrame(self.content, text="Select Analyzers")
            toggle_frame.grid(row=1, column=0, pady=10)

            self.meta_var = tk.BooleanVar(value=True)
            self.geometry_var = tk.BooleanVar(value=True)
            self.topology_var = tk.BooleanVar(value=True)
            self.quality_var = tk.BooleanVar(value=True)
            self.performance_var = tk.BooleanVar(value=True)

            ttk.Checkbutton(
                toggle_frame,
                text="Meta",
                variable=self.meta_var
            ).grid(row=0, column=0, padx=15, pady=5)

            ttk.Checkbutton(
                toggle_frame,
                text="Topology",
                variable=self.topology_var
            ).grid(row=0, column=1, padx=15, pady=5)

            ttk.Checkbutton(
                toggle_frame,
                text="Geometry",
                variable=self.geometry_var
            ).grid(row=0, column=2, padx=15, pady=5)

            ttk.Checkbutton(
                toggle_frame,
                text="Quality",
                variable=self.quality_var
            ).grid(row=0, column=3, padx=15, pady=5)

            ttk.Checkbutton(
                toggle_frame,
                text="Performance",
                variable=self.performance_var
            ).grid(row=0, column=4, padx=15, pady=5)

            ttk.Button(
                self.content,
                text="Run Analysis",
                width=30,
                command=self.run_analysis
            ).grid(row=2, column=0, pady=15)

            ttk.Label(
                self.content,
                text="Output",
                font=("Segoe UI", 10, "bold")
            ).grid(row=3, column=0, pady=(10, 5))

            output_frame = ttk.Frame(self.content)
            output_frame.grid(row=4, column=0, sticky="nsew", padx=120)

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

            if not file_path.lower().endswith((".stl", ".obj", ".ply")):
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

        if not any([
            self.meta_var.get(),
            self.geometry_var.get(),
            self.topology_var.get(),
            self.quality_var.get(),
            self.performance_var.get()
        ]):
            messagebox.showwarning(
                "No Analyzer Selected",
                "Please select at least one analyzer."
            )
            return

        try:
            runner = AnalyzerRunner(
                file_path,
                run_meta=self.meta_var.get(),
                run_geometry=self.geometry_var.get(),
                run_topology=self.topology_var.get(),
                run_quality=self.quality_var.get(),
                run_performance=self.performance_var.get()
            )

            report = runner.run()

            if report is None:
                messagebox.showerror(
                    "Analysis Failed",
                    "Model analysis could not be completed."
                )
                return

            self.display_report(report)

        except Exception as e:
            messagebox.showerror("Analysis Error", str(e))

    def display_report(self, report):
        try:
            self.console.config(state="normal")
            self.console.delete("1.0", tk.END)

            self.console.tag_configure("section", font=("Segoe UI", 11, "bold"))
            self.console.tag_configure("metric", font=("Consolas", 10))

            for section, data in report.items():

                self.console.insert(tk.END, f"{section.upper()}\n", "section")
                self.console.insert(tk.END, "=" * 50 + "\n\n", "section")

                if isinstance(data, dict):
                    for key, value in data.items():
                        formatted_key = key.replace("_", " ").title()
                        line = f"{formatted_key:<25} : {value}\n"
                        self.console.insert(tk.END, line, "metric")

                self.console.insert(tk.END, "\n\n")

            self.console.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Display Error", str(e))