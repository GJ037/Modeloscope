import os, json, tkinter as tk
from tkinter import ttk, filedialog, messagebox
from interfaces.screen import Screen
from analyzers.runner import analyze


class AnalyzeInterface(Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.current_file = None
        self.last_report = None

        self.has_report = False
        self.is_loading = False
        self.is_active = False
        self.request_id = 0

        self.build_content()

    def build_content(self):
        button_frame = ttk.Frame(self.top_frame)
        button_frame.grid(row=0, column=0, pady=10)

        self.browse_button = ttk.Button(button_frame, text="📁 Browse File", width=15, command=self.browse_file)
        self.browse_button.pack(side="left", padx=20)

        self.run_button = ttk.Button(button_frame, text="📄 Run Analysis", width=15, command=self.run_analysis)
        self.run_button.pack(side="left", padx=20)

        self.export_button = ttk.Button(button_frame, text="💾 Export Report", width=15, command=self.export_report)
        self.export_button.pack(side="left", padx=20)

        self.clear_button = ttk.Button(button_frame, text="🧹 Clear", width=15, command=self.clear)
        self.clear_button.pack(side="left", padx=20)

        report_frame = ttk.Frame(self.bottom_frame, borderwidth=2, relief="solid")
        report_frame.grid(row=0, column=0, sticky="nsew", padx=120, pady=10)

        report_frame.columnconfigure(0, weight=1)
        report_frame.rowconfigure(0, weight=1)

        self.console = tk.Text(report_frame, state="disabled", wrap="word", bg="#f7f7f7")
        self.console.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(report_frame, command=self.console.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.console.config(yscrollcommand=scrollbar.set)

        navigation_frame = ttk.Frame(self.bottom_frame)
        navigation_frame.grid(row=1, column=0, pady=10)

        ttk.Button(navigation_frame, text="🏠 Return to Home", width=30,
                   command=lambda: self.controller.show_frame("HomeInterface")).pack()

        self.apply_cursor(self)

    def on_enter(self):
        self.is_active = True
        self.update_states()

    def on_exit(self):
        self.request_id += 1
        self.is_active = False
        self.set_loading(False)

        self.reset_ui()
        self.update_states()

    def update_states(self):
        is_loading = self.is_loading
        has_file = self.current_file is not None and os.path.exists(self.current_file)

        has_report = self.has_report
        has_anything = has_file or has_report

        self.browse_button.config(state="normal" if not is_loading else "disabled")
        self.run_button.config(state="normal" if (has_file and not is_loading) else "disabled")
        self.export_button.config(state="normal" if has_report else "disabled")
        self.clear_button.config(state="normal" if has_anything else "disabled")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Supported Formats", "*.stl *.off *.ply *.obj *.gltf *.glb")]
        )
        if file_path:
            self.request_id += 1

            self.reset_ui()
            self.current_file = file_path

            file_name = os.path.basename(file_path)
            self.controller.set_title(file_name)
            self.update_states()

    def display_report(self, grouped_features):
        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)

        self.console.tag_configure("section", font=("Segoe UI", 12, "bold"))
        self.console.tag_configure("metric", font=("Consolas", 10))

        for section, data in grouped_features.items():
            self.console.insert(tk.END, f"{section.upper()}\n", "section")
            self.console.insert(tk.END, "=" * 64 + "\n\n", "section")

            if isinstance(data, dict):
                for key, value in data.items():
                    formatted_key = key.replace("_", " ").title()
                    line = f"{formatted_key:<32} : {value}\n"
                    self.console.insert(tk.END, line, "metric")

            self.console.insert(tk.END, "\n\n")

        self.console.config(state="disabled")

    def run_analysis(self):
        file_path = self.current_file
  
        self.is_loading = True
        self.set_loading(True)

        self.request_id += 1
        current_id = self.request_id

        self.update_states()

        self.controller.task_manager.submit(
            func=lambda: analyze(file_path),
            success=lambda result: self.analysis_ready(result, current_id),
            failure=lambda error: self.analysis_error(error, current_id)
        )

    def analysis_ready(self, grouped_features, current_id):
        if not self.is_active or current_id != self.request_id:
            return

        self.display_report(grouped_features)

        self.last_report = grouped_features
        self.has_report = True
        self.is_loading = False

        self.set_loading(False)
        self.update_states()

    def analysis_error(self, error, current_id):
        if not self.is_active or current_id != self.request_id:
            return

        messagebox.showerror("Analysis Error", str(error))
        self.clear()

    def export_report(self):
        file_path = filedialog.asksaveasfilename(
            filetypes=[("Text File", "*.txt"), ("JSON File", "*.json")]
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

                    if isinstance(data, dict):
                        for key, value in data.items():
                            f.write(f"{key}: {value}\n")

                    f.write("\n")

            messagebox.showinfo("Export Success", "Report exported successfully.")

    def clear(self):
        self.request_id += 1

        self.reset_ui()
        self.set_loading(False)
        self.update_states()

    def reset_ui(self):
        self.controller.set_title()

        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.config(state="disabled")

        self.current_file = None
        self.last_report = None
        self.has_report = False
        self.is_loading = False