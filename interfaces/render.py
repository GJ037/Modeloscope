import tkinter as tk, os
from tkinter import ttk, filedialog, messagebox
from interfaces.screen import BaseScreen
from renderers.render import RenderRunner


class RenderInterface(BaseScreen):
    """
    Screen for visualizing 3D models.

    Responsibilities:
    - Allows users to select a model file
    - Provides options to choose rendering modes (standard, wireframe, point cloud)
    - Executes rendering through RenderRunner
    - Displays rendered models in an interactive viewport
    - Supports clearing the viewport and resetting the scene
    - Maintains UI state for render availability

    Acts as the interaction layer between the user and the rendering
    pipeline, providing real-time visual feedback and control.
    """
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller, title=None)
        self.selected_file = tk.StringVar()
        self.render_mode = tk.StringVar()
        self.runner = None
        self.build_content()
        self.has_render = False

    def build_content(self):
        try:
            self.content.columnconfigure(0, weight=1)
            self.content.rowconfigure(3, weight=1)

            file_frame = ttk.Frame(self.content)
            file_frame.grid(row=0, column=0, pady=10)

            ttk.Label(file_frame, text="Select Model:").pack(side="left", padx=5)
            ttk.Entry(file_frame, textvariable=self.selected_file, width=50).pack(side="left", padx=5)
            ttk.Button(file_frame, text="📁 Browse", width=10, command=self.browse_file).pack(side="left", padx=5)

            toggle_frame = ttk.LabelFrame(self.content, text="Select Render Mode")
            toggle_frame.grid(row=1, column=0, pady=10)

            ttk.Radiobutton(toggle_frame, text="Standard", variable=self.render_mode, value="standard").grid(row=0, column=0, padx=15)
            ttk.Radiobutton(toggle_frame, text="Wireframe", variable=self.render_mode, value="wireframe").grid(row=0, column=1, padx=15)
            ttk.Radiobutton(toggle_frame, text="Point Cloud", variable=self.render_mode, value="pointcloud").grid(row=0, column=2, padx=15)

            button_frame = ttk.Frame(self.content)
            button_frame.grid(row=2, column=0, pady=15)

            ttk.Button(button_frame, text="🎨 Render Model", width=15, command=self.render_model)\
                .pack(side="left", padx=20)

            ttk.Button(button_frame, text="🧹 Clear Render", width=15, command=self.clear_view)\
                .pack(side="left", padx=20)

            self.viewer_frame = ttk.Frame(self.content, borderwidth=2, relief="solid")
            self.viewer_frame.grid(row=3, column=0, sticky="nsew", padx=120, pady=10)

            self.add_footer_button(
                "🏠 Return to Home",
                lambda: self.controller.show_frame("HomeInterface")
            )
            
        except Exception as e:
            messagebox.showerror("UI Error", str(e))

        self.runner = RenderRunner(self.viewer_frame)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("3D Models", "*.stl *.obj *.ply")]
        )
        if file_path:
            self.selected_file.set(file_path)

    def render_model(self):
        file_path = self.selected_file.get().strip()

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Invalid File", "Please select a valid 3D model.")
            return

        if not self.render_mode.get():
            messagebox.showwarning("No Mode Selected", "Select a render mode.")
            return

        try:
            if not self.runner:
                self.runner = RenderRunner(self.viewer_frame)

            result = self.runner.render(file_path, self.render_mode.get())

            if result["status"] != "success":
                messagebox.showerror("Render Error", result["message"])
            
            self.has_render = True

        except Exception as e:
            messagebox.showerror("Render Error", str(e))

    def clear_view(self):
        if not self.has_render:
            messagebox.showwarning("Nothing to Clear", "No rendered model available.")
            return
        
        if self.runner:
            self.runner.reset_scene()

        self.has_render = False

    def reset(self):
        if self.has_render:
            self.runner.reset_scene()
            self.has_render = False

        else:
            self.runner.reset_view()
        
        self.selected_file.set("")
        self.render_mode.set("")