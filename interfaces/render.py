import os, tkinter as tk
from tkinter import ttk, filedialog, messagebox
from cores.engine import RenderEngine
from interfaces.screen import BaseScreen
from renderers.runner import RenderRunner


class RenderInterface(BaseScreen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title=None)
        self.mode = tk.StringVar()

        self.engine = None
        self.runner = None
        self.current_file = None

        self.has_render = False
        self.is_loading = False
        self.is_active = False

        self.request_id = 0
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

        self.browse_button = ttk.Button(button_frame, text="📁 Browse File", width=15, command=self.browse_file)
        self.browse_button.pack(side="left", padx=20)

        self.render_button = ttk.Button(button_frame, text="🎨 Draw Render", width=15, command=self.draw_render)
        self.render_button.pack(side="left", padx=20)

        self.reset_button = ttk.Button(button_frame, text="🔄 Reset View", width=15, command=self.reset_view)
        self.reset_button.pack(side="left", padx=20)

        self.clear_button = ttk.Button(button_frame, text="🧹 Clear", width=15, command=self.clear)
        self.clear_button.pack(side="left", padx=20)

        toggle_frame = ttk.LabelFrame(self.content, text="Render Modes")
        toggle_frame.grid(row=1, column=0, pady=10)

        self.flat_button = ttk.Radiobutton(
            toggle_frame, text="Flat", variable=self.mode, value="flat", command=self.update_states
        )
        self.flat_button.grid(row=0, column=0, padx=15)

        self.shaded_button = ttk.Radiobutton(
            toggle_frame, text="Shaded", variable=self.mode, value="shaded", command=self.update_states
        )
        self.shaded_button.grid(row=0, column=1, padx=15)

        self.wireframe_button = ttk.Radiobutton(
            toggle_frame, text="Wireframe", variable=self.mode, value="wireframe", command=self.update_states
        )
        self.wireframe_button.grid(row=0, column=2, padx=15)

        self.pointcloud_button = ttk.Radiobutton(
            toggle_frame, text="Point Cloud", variable=self.mode, value="pointcloud", command=self.update_states
        )
        self.pointcloud_button.grid(row=0, column=3, padx=15)

        self.viewer_frame = ttk.Frame(self.content, borderwidth=2, relief="solid")
        self.viewer_frame.grid(row=2, column=0, sticky="nsew", padx=120, pady=10)

        self.add_footer_button(
            "🏠 Return to Home",
            lambda: self.controller.show_frame("HomeInterface")
        )

    def on_enter(self):
        self.is_active = True

        if self.engine:
            self.engine.set_axis(True)

        self.update_states()

    def on_exit(self):
        self.request_id += 1
        self.is_active = False

        self.reset_ui()

        if self.engine:
            self.engine.set_axis(False)

        self.update_states()

    def update_states(self):
        has_file = self.current_file is not None
        has_mode = bool(self.mode.get())
        is_loading = self.is_loading

        has_render = self.has_render
        has_anything = has_file or has_mode or has_render

        self.flat_button.config(state="normal" if (has_file and not is_loading) else "disabled")
        self.shaded_button.config(state="normal" if (has_file and not is_loading) else "disabled")
        self.wireframe_button.config(state="normal" if (has_file and not is_loading) else "disabled")
        self.pointcloud_button.config(state="normal" if (has_file and not is_loading) else "disabled")

        self.browse_button.config(state="normal" if not is_loading else "disabled")
        self.render_button.config(
            state="normal" if (has_file and has_mode and not is_loading) else "disabled"
        )
        self.reset_button.config(state="normal" if has_render else "disabled")
        self.clear_button.config(state="normal" if has_anything else "disabled")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("3D Models", "*.stl *.obj *.ply")]
        )
        if file_path:
            self.request_id += 1

            self.reset_ui()
            self.current_file = file_path

            file_name = os.path.basename(file_path)
            self.controller.set_title(file_name)
            self.update_states()

    def draw_render(self):
        file_path = self.current_file

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Invalid File", "Please select a valid 3D model.")
            return

        if not self.mode.get():
            messagebox.showwarning("No Mode Selected", "Select a render mode.")
            return

        self.is_loading = True
        self.request_id += 1
        current_id = self.request_id
        self.update_states()

        self.controller.task_manager.submit(
            func=lambda: self.runner.load(file_path, self.mode.get()),
            on_success=lambda result: self.render_ready(result, current_id),
            on_error=lambda error: self.render_error(error, current_id)
        )

    def render_ready(self, result, current_id):
        if not self.is_active or current_id != self.request_id:
            return
        
        self.runner.render(*result)

        self.has_render = True
        self.is_loading = False
        self.update_states()

    def render_error(self, error, current_id):
        if not self.is_active or current_id != self.request_id:
            return

        messagebox.showerror("Render Error", str(error))

        self.is_loading = False
        self.update_states()

    def reset_view(self):
        if not self.engine:
            return

        if not self.has_render:
            messagebox.showwarning("No Model Rendered", "Render a model first.")
            return
        
        self.engine.reset_view()
        self.engine.set_axis(False)

    def clear(self):
        self.request_id += 1

        self.reset_ui()
        self.update_states()
    
    def reset_ui(self):
        if self.engine:
            self.engine.clear_visuals()
            self.engine.reset_view()
            self.engine.set_axis(True)

        self.mode.set("")
        self.controller.set_title()

        self.current_file = None
        self.has_render = False
        self.is_loading = False