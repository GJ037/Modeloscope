import os, tkinter as tk
from tkinter import ttk, filedialog, messagebox
from cores.engine import RenderEngine
from interfaces.screen import BaseScreen
from renderers.runner import RenderRunner


class RenderInterface(BaseScreen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title=None)
        self.mode = tk.StringVar()
        self.current_file = None
        self.engine = None
        self.runner = None
        self.has_render = False
        self.build_content()

        if self.engine is None:
            self.engine = RenderEngine()
            self.engine.initialize(self.viewer_frame)
            self.runner = RenderRunner(self.engine)

    def build_content(self):
        self.content.columnconfigure(0, weight=1)
        self.content.rowconfigure(2, weight=1)

        button_frame = ttk.Frame(self.content)
        button_frame.grid(row=0, column=0, pady=15)

        ttk.Button(button_frame, text="📁 Browse File", width=15, command=self.browse_file)\
            .pack(side="left", padx=20)

        ttk.Button(button_frame, text="🎨 Draw Render", width=15, command=self.draw_render)\
            .pack(side="left", padx=20)

        ttk.Button(button_frame, text="🔄 Reset View", width=15, command=self.reset_view)\
            .pack(side="left", padx=20)

        ttk.Button(button_frame, text="🧹 Clear Scene", width=15, command=self.clear_scene)\
            .pack(side="left", padx=20)

        toggle_frame = ttk.LabelFrame(self.content, text="Select Render Mode")
        toggle_frame.grid(row=1, column=0, pady=10)

        ttk.Radiobutton(toggle_frame, text="Flat", variable=self.mode, value="flat").grid(row=0, column=0, padx=15)
        ttk.Radiobutton(toggle_frame, text="Shaded", variable=self.mode, value="shaded").grid(row=0, column=1, padx=15)
        ttk.Radiobutton(toggle_frame, text="Wireframe", variable=self.mode, value="wireframe").grid(row=0, column=2, padx=15)
        ttk.Radiobutton(toggle_frame, text="Point Cloud", variable=self.mode, value="pointcloud").grid(row=0, column=3, padx=15)

        self.viewer_frame = ttk.Frame(self.content, borderwidth=2, relief="solid")
        self.viewer_frame.grid(row=2, column=0, sticky="nsew", padx=120, pady=10)

        self.add_footer_button(
            "🏠 Return to Home",
            lambda: self.controller.show_frame("HomeInterface")
        )

    def on_enter(self):
        if self.engine:
            self.engine.set_axis(True)
            self.engine.reset_view()

    def on_exit(self):
        if self.engine:
            self.engine.clear_visuals()
            self.engine.set_axis(False)

        self.mode.set("")       
        self.controller.set_title()
        self.current_file = None
        self.has_render = False

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("3D Models", "*.stl *.obj *.ply")]
        )
        if file_path:
            self.current_file = file_path

            file_name = os.path.basename(file_path)
            self.controller.set_title(file_name)

    def draw_render(self):
        file_path = self.current_file

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Invalid File", "Please select a valid 3D model.")
            return

        if not self.mode.get():
            messagebox.showwarning("No Mode Selected", "Select a render mode.")
            return

        self.runner.run(file_path, self.mode.get())
        self.has_render = True

    def reset_view(self):
        if not self.engine:
            return

        if not self.has_render:
            messagebox.showwarning("No Model Rendered", "Render a model first.")
            return
        
        self.engine.reset_view()
        self.engine.set_axis(False)

    def clear_scene(self):
        if not self.has_render:
            messagebox.showwarning("Nothing to Clear", "No rendered model available.")
            return

        self.engine.clear_visuals()
        self.engine.reset_view()
        self.engine.set_axis(True)

        self.has_render = False