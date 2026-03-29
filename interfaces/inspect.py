import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from interfaces.screen import BaseScreen
from renderers.runner import RenderRunner
from inspectors.runner import InspectRunner
from renderers.highlight import HighlightRenderer


class InspectInterface(BaseScreen):
    """
    Inspection UI following same pattern as RenderInterface.
    Self-contained (no dependency on other interfaces).
    """

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title=None)

        self.selected_file = tk.StringVar()
        self.mode = tk.StringVar()

        self.runner = None
        self.inspect_runner = InspectRunner()
        self.highlight_renderer = HighlightRenderer()

        self.has_render = False

        self.build_content()

    # -----------------------------

    def build_content(self):
        try:
            self.content.columnconfigure(0, weight=1)
            self.content.rowconfigure(3, weight=1)

            # File selection
            file_frame = ttk.Frame(self.content)
            file_frame.grid(row=0, column=0, pady=10)

            ttk.Label(file_frame, text="Select Model:").pack(side="left", padx=5)
            ttk.Entry(file_frame, textvariable=self.selected_file, width=50).pack(side="left", padx=5)
            ttk.Button(file_frame, text="📁 Browse", width=10, command=self.browse_file).pack(side="left", padx=5)

            # Mode selection
            mode_frame = ttk.LabelFrame(self.content, text="Select Inspect Mode")
            mode_frame.grid(row=1, column=0, pady=10)

            ttk.Radiobutton(mode_frame, text="Boundary Edges", variable=self.mode, value="boundary").grid(row=0, column=0, padx=15)
            ttk.Radiobutton(mode_frame, text="Non-Manifold Edges", variable=self.mode, value="non_manifold").grid(row=0, column=1, padx=15)
            ttk.Radiobutton(mode_frame, text="Face Normals", variable=self.mode, value="face_normals").grid(row=0, column=2, padx=15)
            ttk.Radiobutton(mode_frame, text="Vertex Normals", variable=self.mode, value="vertex_normals").grid(row=0, column=3, padx=15)
            ttk.Radiobutton(mode_frame, text="Flipped Normals", variable=self.mode, value="flipped_normals").grid(row=0, column=4, padx=15)

            # Buttons
            button_frame = ttk.Frame(self.content)
            button_frame.grid(row=2, column=0, pady=15)

            ttk.Button(button_frame, text="🧪 Run Inspect", width=15, command=self.run_inspect)\
                .pack(side="left", padx=20)

            ttk.Button(button_frame, text="🧹 Clear View", width=15, command=self.clear_view)\
                .pack(side="left", padx=20)

            # Viewer (same as RenderInterface)
            self.viewer_frame = ttk.Frame(self.content, borderwidth=2, relief="solid")
            self.viewer_frame.grid(row=3, column=0, sticky="nsew", padx=120, pady=10)

            self.add_footer_button(
                "🏠 Return to Home",
                lambda: self.controller.show_frame("HomeInterface")
            )

        except Exception as e:
            messagebox.showerror("UI Error", str(e))

        # Initialize runner
        self.runner = RenderRunner(self.viewer_frame)

    # -----------------------------

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("3D Models", "*.stl *.obj *.ply")]
        )
        if file_path:
            self.selected_file.set(file_path)

    # -----------------------------

    def run_inspect(self):
        file_path = self.selected_file.get().strip()

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Invalid File", "Please select a valid 3D model.")
            return

        if not self.mode.get():
            messagebox.showwarning("No Mode Selected", "Select an inspect mode.")
            return

        try:
            # Step 1: render model
            result = self.runner.render(file_path, "standard")

            if result["status"] != "success":
                messagebox.showerror("Render Error", result["message"])
                return

            model = self.runner.model
            engine = self.runner.engine

            # Step 2: inspect
            inspect_data = self.inspect_runner.run(model, self.mode.get())

            # Step 3: overlay
            engine.clear_overlay()
            self.highlight_renderer.render(engine, model, inspect_data)

            self.has_render = True

        except Exception as e:
            messagebox.showerror("Inspect Error", str(e))

    # -----------------------------

    def clear_view(self):
        if not self.has_render:
            messagebox.showwarning("Nothing to Clear", "No inspection available.")
            return

        if self.runner:
            # 🔥 clear overlay FIRST
            self.runner.engine.clear_overlay()

            # then clear scene
            self.runner.reset_scene()

        self.has_render = False

    # -----------------------------

    def reset(self):
        if self.runner:
            # 🔥 ALWAYS clear overlay
            self.runner.engine.clear_overlay()

            if self.has_render:
                self.runner.reset_scene()
            else:
                self.runner.reset_view()

        self.selected_file.set("")
        self.mode.set("")
        self.has_render = False