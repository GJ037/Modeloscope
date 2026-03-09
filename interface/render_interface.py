import tkinter as tk, os
from tkinter import ttk, filedialog, messagebox
from interface.base_screen import BaseScreen
from render import RenderRunner

class RenderInterface(BaseScreen):
    """
    RenderInterface

    Screen responsible for:
        - Selecting a 3D model
        - Choosing render mode
        - Displaying rendered model
    """

    def __init__(self, parent, controller):
        super().__init__(parent, controller, title="Renderer")
        self.selected_file = tk.StringVar()
        self.build_content()

    def build_content(self):
        try:
            self.content.columnconfigure(0, weight=1)
            self.content.rowconfigure(3, weight=1)

            file_frame = ttk.Frame(self.content)
            file_frame.grid(row=0, column=0, pady=10)

            ttk.Label(file_frame, text="Select Model:").grid(row=0, column=0, padx=5)

            ttk.Entry(
                file_frame,
                textvariable=self.selected_file,
                width=45
            ).grid(row=0, column=1, padx=5)

            ttk.Button(
                file_frame,
                text="Browse",
                width=12,
                command=self.browse_file
            ).grid(row=0, column=2, padx=5)

            toggle_frame = ttk.LabelFrame(self.content, text="Select Render Mode")
            toggle_frame.grid(row=1, column=0, pady=10)

            self.standard_var = tk.BooleanVar(value=False)
            self.wireframe_var = tk.BooleanVar(value=False)

            ttk.Checkbutton(
                toggle_frame,
                text="Standard",
                variable=self.standard_var
            ).grid(row=0, column=0, padx=15, pady=5)

            ttk.Checkbutton(
                toggle_frame,
                text="Wireframe",
                variable=self.wireframe_var
            ).grid(row=0, column=1, padx=15, pady=5)

            ttk.Button(
                self.content,
                text="Render Model",
                width=20,
                command=self.render_model
            ).grid(row=2, column=0, padx=15)

            self.viewer_frame = ttk.Frame(self.content)
            self.viewer_frame.grid(row=3, column=0, sticky="nsew", padx=60, pady=10)

            # Placeholder label
            ttk.Label(
                self.viewer_frame,
                text="Render Viewport",
                font=("Segoe UI", 12)
            ).pack(expand=True)

            # Footer
            self.add_footer_button(
                "Return to Home",
                lambda: self.controller.show_frame("HomeInterface")
            )

        except Exception as e:
            print(f"[RenderInterface ERROR] {e}")

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

    def render_model(self):
        file_path = self.selected_file.get().strip()

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror(
                "Invalid File",
                "Please select a valid 3D model."
            )
            return

        if not any([
            self.standard_var.get(),
            self.wireframe_var.get()
        ]):
            messagebox.showwarning(
                "No Render Mode Selected",
                "Please select at least one render mode."
            )
            return
            
        try:
            for widget in self.viewer_frame.winfo_children():
                widget.destroy()

            runner = RenderRunner(
                file_path,
                render_standard=self.standard_var.get(),
                render_wireframe=self.wireframe_var.get()
            )
            
            runner.run(self.viewer_frame)

        except Exception as e:
            messagebox.showerror("Render Error", str(e))