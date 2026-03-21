from vispy import app, scene

app.use_app("tkinter")


class RenderEngine:
    """
    Central controller for the rendering system.

    Responsibilities:
    - Initializes and manages the rendering canvas and view
    - Maintains the scene graph and visual lifecycle
    - Provides APIs to add and remove visuals
    - Controls camera behavior (fit, reset)
    - Manages axis visibility

    Acts as the core runtime controller that coordinates rendering
    without performing any actual drawing logic.
    """

    def __init__(self):
        self.canvas = None
        self.view = None
        self.axis = None
        self.visuals = []

    def initialize(self, parent):
        if parent is None:
            raise ValueError("Parent frame is required")

        self.canvas = scene.SceneCanvas(
            keys="interactive",
            bgcolor="gray",
            parent=parent
        )

        self.canvas.native.pack(fill="both", expand=True)

        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.cameras.TurntableCamera()

        self._init_axis()
        self.set_axis(True)
        
    def _init_axis(self):
        self.axis = scene.visuals.XYZAxis(parent=self.view.scene)
        self.axis.transform = scene.transforms.STTransform(scale=(0.25, 0.25, 0.25))

    def clear_scene(self):
        for visual in self.visuals:
            visual.parent = None

        self.visuals.clear()

    def add_visual(self, visual):
        visual.parent = self.view.scene
        self.visuals.append(visual)

    def fit_camera(self):
        if self.view:
            self.view.camera.set_range()

    def fit_axis(self):
        if self.view:
            self.view.camera.set_range(x=(-1,1), y=(-1,1), z=(-1,1))

    def reset_camera(self):
        if self.view:
            self.view.camera = scene.cameras.TurntableCamera()

    def set_axis(self, visible: bool):
        if self.axis:
            self.axis.visible = visible