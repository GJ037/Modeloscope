import os, json, tkinter as tk
from tkinter import ttk, filedialog, messagebox
from interfaces.screen import BaseScreen
from analyzers.runner import AnalyzerRunner


class AnalyzeInterface(BaseScreen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title=None)

        self.current_file = None
        self.last_report = None

        self.has_report = False
        self.is_loading = False
        self.is_active = False

        self.request_id = 0
        self.build_content()

    def build_content(self):
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(2, weight=1)

        button_frame = ttk.Frame(self.content)
        button_frame.grid(row=0, column=0, pady=15)

        self.browse_button = ttk.Button(button_frame, text="📁 Browse File", width=15, command=self.browse_file)
        self.browse_button.pack(side="left", padx=20)

        self.run_button = ttk.Button(button_frame, text="📄 Run Analysis", width=15, command=self.run_analysis)
        self.run_button.pack(side="left", padx=20)

        self.export_button = ttk.Button(button_frame, text="💾 Export Result", width=15, command=self.export_result)
        self.export_button.pack(side="left", padx=20)

        self.clear_button = ttk.Button(button_frame, text="🧹 Clear", width=15, command=self.clear)
        self.clear_button.pack(side="left", padx=20)

        toggle_frame = ttk.LabelFrame(self.content, text="Analysis Modes")
        toggle_frame.grid(row=1, column=0, pady=10)

        self.toggle_var = tk.BooleanVar()
        self.meta_var = tk.BooleanVar()
        self.geometry_var = tk.BooleanVar()
        self.topology_var = tk.BooleanVar()
        self.quality_var = tk.BooleanVar()
        self.performance_var = tk.BooleanVar()

        self.toggle_button = ttk.Checkbutton(toggle_frame, text="All/None", variable=self.toggle_var, 
                        command=lambda: [self.handle_toggle(), self.update_states()])
        self.toggle_button.grid(row=0, column=0, padx=15)

        self.meta_button = ttk.Checkbutton(toggle_frame, text="Meta", variable=self.meta_var, 
                        command=lambda: [self.update_toggle(), self.update_states()])
        self.meta_button.grid(row=0, column=1, padx=15)

        self.topology_button = ttk.Checkbutton(toggle_frame, text="Topology", variable=self.topology_var, 
                        command=lambda: [self.update_toggle(), self.update_states()])
        self.topology_button.grid(row=0, column=2, padx=15)

        self.geometry_button = ttk.Checkbutton(toggle_frame, text="Geometry", variable=self.geometry_var, 
                        command=lambda: [self.update_toggle(), self.update_states()])
        self.geometry_button.grid(row=0, column=3, padx=15)

        self.quality_button = ttk.Checkbutton(toggle_frame, text="Quality", variable=self.quality_var, 
                        command=lambda: [self.update_toggle(), self.update_states()])
        self.quality_button.grid(row=0, column=4, padx=15)

        self.performance_button = ttk.Checkbutton(toggle_frame, text="Performance", variable=self.performance_var, 
                        command=lambda: [self.update_toggle(), self.update_states()])
        self.performance_button.grid(row=0, column=5, padx=15)

        output_frame = ttk.Frame(self.content, borderwidth=2, relief="solid")
        output_frame.grid(row=2, column=0, sticky="nsew", padx=120, pady=10)

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

    def on_enter(self):
        self.is_active = True
        self.update_states()

    def on_exit(self):
        self.request_id += 1
        self.is_active = False

        self.reset_ui()
        self.update_states()

    def handle_toggle(self):
        state = self.toggle_var.get()

        self.meta_var.set(state)
        self.topology_var.set(state)
        self.geometry_var.set(state)
        self.quality_var.set(state)
        self.performance_var.set(state)

    def update_toggle(self):
        all_modes = (
            self.meta_var.get() and
            self.topology_var.get() and
            self.geometry_var.get() and
            self.quality_var.get() and
            self.performance_var.get()
        )

        self.toggle_var.set(all_modes)

    def update_states(self):
        has_file = self.current_file is not None and os.path.exists(self.current_file)

        has_modes = (
            self.meta_var.get() or
            self.topology_var.get() or
            self.geometry_var.get() or
            self.quality_var.get() or
            self.performance_var.get()
        )

        is_loading = self.is_loading

        has_report = self.has_report
        has_anything = has_file or has_modes or has_report

        self.toggle_button.config(state="normal" if (has_file and not is_loading) else "disabled")
        self.meta_button.config(state="normal" if (has_file and not is_loading) else "disabled")
        self.geometry_button.config(state="normal" if (has_file and not is_loading) else "disabled")
        self.topology_button.config(state="normal" if (has_file and not is_loading) else "disabled")
        self.quality_button.config(state="normal" if (has_file and not is_loading) else "disabled")
        self.performance_button.config(state="normal" if (has_file and not is_loading) else "disabled")

        self.browse_button.config(state="normal" if not is_loading else "disabled")
        self.run_button.config(
            state="normal" if (has_file and has_modes and not is_loading) else "disabled"
        )
        self.export_button.config(state="normal" if has_report else "disabled")
        self.clear_button.config(state="normal" if has_anything else "disabled")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select 3D File",
            filetypes=[("3D Models", "*.stl *.obj *.ply")]
        )
        if file_path:
            self.request_id += 1

            self.reset_ui()
            self.current_file = file_path

            file_name = os.path.basename(file_path)
            self.controller.set_title(file_name)
            self.update_states()

    def display_report(self, report):
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

    def run_analysis(self):
        file_path = self.current_file

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
            messagebox.showwarning("No Mode Selected", "Select an analysis mode.")
            return

        self.is_loading = True
        self.request_id += 1
        current_id = self.request_id
        self.update_states()

        runner = AnalyzerRunner()

        self.controller.task_manager.submit(
            func=lambda: runner.analyze(file_path, modes),
            on_success=lambda result: self.analysis_ready(result, current_id),
            on_error=lambda error: self.analysis_error(error, current_id)
        )

    def analysis_ready(self, report, current_id):
        if not self.is_active or current_id != self.request_id:
            return

        self.display_report(report)
        self.last_report = report
        self.has_report = True

        self.is_loading = False
        self.update_states()

    def analysis_error(self, error, current_id):
        if not self.is_active or current_id != self.request_id:
            return

        messagebox.showerror("Analysis Error", str(error))

        self.is_loading = False
        self.update_states()

    def export_result(self):
        if not self.last_report:
            messagebox.showwarning("Export Error", "No report available to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text File", "*.txt"),
                ("JSON File", "*.json")
           ]
        )

        if not file_path:
            return

        if file_path.endswith(".json"):
            with open(file_path, "w") as f:
                json.dump(self.last_report, f, indent=4)
            
            messagebox.showinfo("Export Success", "Report exported as JSON.")

        else:
            with open(file_path, "w") as f:
                for section, data in self.last_report.items():

                    f.write(f"{section.upper()}\n")
                    f.write("=" * 50 + "\n")

                    if isinstance(data, dict):
                        for key, value in data.items():
                            f.write(f"{key}: {value}\n")

                    f.write("\n")

            messagebox.showinfo("Export Success", "Report exported successfully.")

    def clear(self):
        self.request_id += 1

        self.reset_ui()
        self.update_states()

    def reset_ui(self):
        self.controller.set_title()

        self.toggle_var.set(False)
        self.meta_var.set(False)
        self.topology_var.set(False)
        self.geometry_var.set(False)
        self.quality_var.set(False)
        self.performance_var.set(False)

        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.config(state="disabled")

        self.current_file = None
        self.last_report = None
        self.has_report = False
        self.is_loading = False