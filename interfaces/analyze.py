import tkinter as tk, os
from tkinter import ttk, filedialog, messagebox
from interfaces.screen import BaseScreen
from analyzers.runner import AnalyzerRunner


class AnalyzeInterface(BaseScreen):
    """
    Screen for performing analysis on 3D models.

    Responsibilities:
    - Allows users to select a model file
    - Provides options to choose different analysis modes
    - Executes analysis through AnalyzerRunner
    - Displays formatted analysis results
    - Supports clearing and exporting analysis reports
    - Maintains UI state for report availability

    Acts as the interaction layer between the user and the analysis
    pipeline, ensuring clear input handling and readable output presentation.
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller, title=None)
        self.selected_file = tk.StringVar()
        self.build_content()

        self.last_report = None
        self.has_report = False

    def build_content(self):
        try:
            self.content.columnconfigure(0, weight=1)
            self.content.rowconfigure(3, weight=1)

            file_frame = ttk.Frame(self.content)
            file_frame.grid(row=0, column=0, pady=10)

            ttk.Label(file_frame, text="Select Model:").pack(side="left", padx=5)
            ttk.Entry(file_frame, textvariable=self.selected_file, width=50).pack(side="left", padx=5)
            ttk.Button(file_frame, text="📁 Browse", width=10, command=self.browse_file).pack(side="left", padx=5)

            toggle_frame = ttk.LabelFrame(self.content, text="Select Analysis Modes")
            toggle_frame.grid(row=1, column=0, pady=10)

            self.meta_var = tk.BooleanVar()
            self.geometry_var = tk.BooleanVar()
            self.topology_var = tk.BooleanVar()
            self.quality_var = tk.BooleanVar()
            self.performance_var = tk.BooleanVar()

            ttk.Checkbutton(toggle_frame, text="Meta", variable=self.meta_var).grid(row=0, column=0, padx=15)
            ttk.Checkbutton(toggle_frame, text="Topology", variable=self.topology_var).grid(row=0, column=1, padx=15)
            ttk.Checkbutton(toggle_frame, text="Geometry", variable=self.geometry_var).grid(row=0, column=2, padx=15)
            ttk.Checkbutton(toggle_frame, text="Quality", variable=self.quality_var).grid(row=0, column=3, padx=15)
            ttk.Checkbutton(toggle_frame, text="Performance", variable=self.performance_var).grid(row=0, column=4, padx=15)

            button_frame = ttk.Frame(self.content)
            button_frame.grid(row=2, column=0, pady=15)

            ttk.Button(button_frame, text="📄 Analyze Model", width=15, command=self.run_analysis)\
                .pack(side="left", padx=20)
            
            ttk.Button(button_frame, text="💾 Export Report", width=15, command=self.export_report)\
                .pack(side="left", padx=20)

            ttk.Button(button_frame, text="🧹 Clear Report", width=15, command=self.clear_output)\
                .pack(side="left", padx=20)

            output_frame = ttk.Frame(self.content, borderwidth=2, relief="solid")
            output_frame.grid(row=3, column=0, sticky="nsew", padx=120, pady=10)

            output_frame.columnconfigure(0, weight=1)
            output_frame.rowconfigure(0, weight=1)

            self.console = tk.Text(output_frame, state="disabled", wrap="word", bg="#f7f7f7")
            self.console.grid(row=0, column=0, sticky="nsew")

            scrollbar = ttk.Scrollbar(output_frame, command=self.console.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")

            self.console.config(yscrollcommand=scrollbar.set)

            self.add_footer_button(
                "🏠 Return to Home",
                lambda: self.controller.show_frame("HomeInterface")
            )

        except Exception as e:
            messagebox.showerror("UI Error", str(e))

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select 3D File",
            filetypes=[("3D Models", "*.stl *.obj *.ply")]
        )
        if file_path:
            self.selected_file.set(file_path)

    def run_analysis(self):
        file_path = self.selected_file.get().strip()

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Invalid File", "Please select a valid 3D model.")
            return

        modes = []
        if self.meta_var.get(): modes.append("meta")
        if self.topology_var.get(): modes.append("topology")
        if self.geometry_var.get(): modes.append("geometry")
        if self.quality_var.get(): modes.append("quality")
        if self.performance_var.get(): modes.append("performance")

        if not modes:
            messagebox.showwarning("No Mode Selected", "Select a analysis mode.")
            return

        try:
            runner = AnalyzerRunner()
            result = runner.analyze(file_path, modes)

            if result["status"] != "success":
                messagebox.showerror("Analysis Error", result["message"])
                return

            self.display_report(result["report"])
            self.last_report = result["report"]
            self.has_report = True

        except Exception as e:
            messagebox.showerror("Analysis Error", str(e))

    def display_report(self, report):
        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)

        self.console.tag_configure("section", font=("Segoe UI", 11, "bold"))
        self.console.tag_configure("metric", font=("Consolas", 10))

        for section, data in report.items():
            self.console.insert(tk.END, f"{section.upper()}\n", "section")
            self.console.insert(tk.END, "=" * 50 + "\n\n", "section")

            if isinstance(data, dict) and "data" in data:
                actual_data = data["data"]
            else:
                actual_data = data

            if isinstance(actual_data, dict):
                for key, value in actual_data.items():
                    formatted_key = key.replace("_", " ").title()
                    line = f"{formatted_key:<25} : {value}\n"
                    self.console.insert(tk.END, line, "metric")

            self.console.insert(tk.END, "\n\n")

        self.console.config(state="disabled")
    
    def export_report(self):
        if not self.last_report:
            messagebox.showwarning("Export Error", "No report available to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt")]
        )

        if not file_path:
            return

        try:
            with open(file_path, "w") as f:
                for section, data in self.last_report.items():

                    f.write(f"{section.upper()}\n")
                    f.write("=" * 50 + "\n")

                    if isinstance(data, dict) and "data" in data:
                        actual_data = data["data"]
                    else:
                        actual_data = data

                    if isinstance(actual_data, dict):
                        for key, value in actual_data.items():
                            f.write(f"{key}: {value}\n")

                    f.write("\n")

            messagebox.showinfo("Export Success", "Report exported successfully.")

        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def clear_output(self):
        if not self.has_report:
            messagebox.showwarning("Nothing to Clear", "No analysis report available.")
            return
        
        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.config(state="disabled")

        self.last_report = None
        self.has_report = False

    def reset(self):
        self.selected_file.set("")
        self.meta_var.set(False)
        self.topology_var.set(False)
        self.geometry_var.set(False)
        self.quality_var.set(False)
        self.performance_var.set(False)

        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.config(state="disabled")

        self.last_report = None
        self.has_report = False