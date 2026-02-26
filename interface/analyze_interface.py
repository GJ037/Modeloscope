import tkinter as tk, os
from tkinter import ttk, filedialog, messagebox

from analyze import AnalyzerRunner


class AnalyzeInterface(ttk.Frame):
    """Interface for running model analysis."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_file = tk.StringVar()
        self.build_ui()

    def build_ui(self):

        ttk.Label(
            self,
            text="Analyzer",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(40, 20))

        # File Section (Centered)
        file_frame = ttk.Frame(self)
        file_frame.pack(pady=20)

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
            self,
            text="Run Analysis",
            width=30,
            command=self.run_analysis
        ).pack(pady=15)

        # Output Label
        ttk.Label(
            self,
            text="Output",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(20, 5))

        # Console Area
        self.console = tk.Text(
            self,
            height=15,
            state="disabled",
            wrap="word",
            bg="#f7f7f7"
        )
        self.console.pack(fill="both", expand=True, padx=60, pady=10)

        ttk.Button(
            self,
            text="Return to Home",
            width=30,
            command=lambda: self.controller.show_frame("HomeInterface")
        ).pack(pady=20)
        
    def log(self, text):
        self.console.configure(state="normal")
        self.console.insert(tk.END, text + "\n")
        self.console.configure(state="disabled")
        self.console.see(tk.END)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select STL File",
            filetypes=[("All files", "*.*")]
        )
        if file_path:
            self.selected_file.set(file_path)

    def run_analysis(self):
        file_path = self.selected_file.get().strip()

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Invalid File", "Please select a valid 3D model.")
            return

        file_name = os.path.basename(file_path)
        self.log(f"Running analysis on: {file_name} ...")

        try:
            runner = AnalyzerRunner(file_path)
            runner.run()
            self.log("Analysis completed successfully.")
            messagebox.showinfo("Success", "Model analysis finished successfully.")
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", f"An error occurred:\n{e}")