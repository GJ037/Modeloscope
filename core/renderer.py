from vispy import app, scene

app.use_app("tkinter")

class ModelRenderer:
    """
    Core rendering engine.

    Manages:
    - SceneCanvas
    - View
    - Camera
    - Visual objects
    """

    def __init__(self):
        self.canvas = None
        self.view = None
        self.axis = None
        self.visuals = []

    def initialize(self, parent):

        if parent is None:
            print("[ModelRenderer ERROR] Parent frame required.")
            return False

        try:
            self.canvas = scene.SceneCanvas(
                keys="interactive",
                bgcolor="black",
                parent=parent
            )

            self.canvas.native.pack(fill="both", expand=True)

            self.view = self.canvas.central_widget.add_view()
            self.view.camera = scene.cameras.TurntableCamera()

            self.set_axis(visible=True)

            return True

        except Exception as e:
            print(f"[ModelRenderer ERROR] {e}")
            return False
    
    def fit_camera(self):
        if self.view:
            self.view.camera.set_range()
    
    def set_axis(self, visible=True):
        if not self.view:
            return

        try:
            if self.axis is None:
                self.axis = scene.visuals.XYZAxis(parent=self.view.scene)
                self.axis.transform = scene.transforms.STTransform(scale=(0.5, 0.5, 0.5))

            self.axis.visible = visible

        except Exception as e:
            print(f"[ModelRenderer AXIS ERROR] {e}")

    def add_visual(self, visual):
        visual.parent = self.view.scene
        self.visuals.append(visual)

    def clear(self):
        for visual in self.visuals:
            visual.parent = None

        self.visuals.clear()
        self.set_axis(True)

        if self.view:
            self.view.camera = scene.cameras.TurntableCamera()
            self.view.camera.set_range(x=(-1, 1), y=(-1, 1), z=(-1, 1))