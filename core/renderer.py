from vispy import app
from vispy import scene

app.use_app("tkinter")

class ModelRenderer:
    """
    Manages SceneCanvas and camera for rendering.
    """

    def __init__(self):
        self.canvas = None
        self.view = None

    def initialize(self, parent):

        if parent is None:
            print("[ModelRenderer ERROR] Parent frame is required.")
            return False

        try:
            self.canvas = scene.SceneCanvas(
                keys="interactive",
                bgcolor="black",
                parent=parent,
                show=True
            )

            self.canvas.native.pack(fill="both", expand=True)

            self.view = self.canvas.central_widget.add_view()
            self.view.camera = scene.cameras.TurntableCamera()

            return True

        except Exception as e:
            print(f"[ModelRenderer ERROR] {e}")
            return False

    def fit_camera(self):
        if self.view:
            self.view.camera.set_range()