import tkinter as tk, os
from tkinter import ttk, filedialog, messagebox
from interfaces.screen import BaseScreen
from inspectors.runner import InspectRunner


class InspectInterface(BaseScreen):
    """
    User interface for performing visual inspection on 3D models.

    Responsibilities:
    - Allows users to select a model file
    - Provides options to choose different inspection modes
    - Executes inspection through InspectRunner
    - Displays rendered model along with inspection overlays
    - Supports clearing overlay and resetting the viewport
    - Maintains UI state for rendered model and overlay availability

    Acts as the interaction layer between the user and the inspection
    pipeline, ensuring a clear separation between UI logic and
    inspection execution while providing real-time visual feedback.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title=None)
        self.selected_file = tk.StringVar()
        self.mode = tk.StringVar()
        self.inspect_runner = None
        self.has_render = False
        self.has_overlay = False
        self.build_content()

    def build_content(self):
        try:
            self.content.columnconfigure(0, weight=1)
            self.content.rowconfigure(3, weight=1)

            file_frame = ttk.Frame(self.content)
            file_frame.grid(row=0, column=0, pady=10)

            ttk.Label(file_frame, text="Select Model:").pack(side="left", padx=5)
            ttk.Entry(file_frame, textvariable=self.selected_file, width=50).pack(side="left", padx=5)
            ttk.Button(file_frame, text="📁 Browse", width=10, command=self.browse_file).pack(side="left", padx=5)

            mode_frame = ttk.LabelFrame(self.content, text="Select Inspect Mode")
            mode_frame.grid(row=1, column=0, pady=10)

            ttk.Radiobutton(mode_frame, text="Boundary Edges", variable=self.mode, value="boundary").grid(row=0, column=0, padx=15)
            ttk.Radiobutton(mode_frame, text="Non-Manifold Edges", variable=self.mode, value="non_manifold").grid(row=0, column=1, padx=15)
            ttk.Radiobutton(mode_frame, text="Face Normals", variable=self.mode, value="face_normals").grid(row=0, column=2, padx=15)
            ttk.Radiobutton(mode_frame, text="Vertex Normals", variable=self.mode, value="vertex_normals").grid(row=0, column=3, padx=15)
            ttk.Radiobutton(mode_frame, text="Flipped Normals", variable=self.mode, value="flipped_normals").grid(row=0, column=4, padx=15)

            button_frame = ttk.Frame(self.content)
            button_frame.grid(row=2, column=0, pady=15)

            ttk.Button(button_frame, text="🧪 Run Inspect", width=15, command=self.run_inspect)\
                .pack(side="left", padx=20)

            ttk.Button(button_frame, text="🧹 Clear View", width=15, command=self.clear_view)\
                .pack(side="left", padx=20)

            self.viewer_frame = ttk.Frame(self.content, borderwidth=2, relief="solid")
            self.viewer_frame.grid(row=3, column=0, sticky="nsew", padx=120, pady=10)

            self.add_footer_button(
                "🏠 Return to Home",
                lambda: self.controller.show_frame("HomeInterface")
            )

        except Exception as e:
            messagebox.showerror("UI Error", str(e))

        self.inspect_runner = InspectRunner(self.viewer_frame)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("3D Models", "*.stl *.obj *.ply")]
        )
        if file_path:
            self.selected_file.set(file_path)

    def run_inspect(self):
        file_path = self.selected_file.get().strip()

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Invalid File", "Please select a valid 3D model.")
            return

        if not self.mode.get():
            messagebox.showwarning("No Mode Selected", "Select an inspect mode.")
            return

        try:
            result = self.inspect_runner.inspect(file_path, self.mode.get())

            if result["status"] != "success":
                messagebox.showerror("Inspect Error", result["message"])
                return

            self.has_render = True
            self.has_overlay = True

        except Exception as e:
            messagebox.showerror("Inspect Error", str(e))

    def clear_view(self):
        if not self.has_render and self.has_overlay:
            messagebox.showwarning("Nothing to Clear", "No inspection available.")
            return
        
        if self.inspect_runner:
            self.inspect_runner.reset_scene()
            self.mode.set("")

            self.has_render = False
            self.has_overlay = False

    def reset(self):
        if self.has_overlay or self.has_render:
            self.inspect_runner.reset_scene()
            self.has_render = False
            self.has_overlay = False

        else:
            self.inspect_runner.reset_view()

        self.selected_file.set("")
        self.mode.set("")