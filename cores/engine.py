from vispy import app, scene

app.use_app("tkinter")


class RenderEngine:
    
    def __init__(self):
        self.canvas = None
        self.view = None
        self.axis = None
        self.overlay = None
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
        self.view.camera = scene.cameras.ArcballCamera()

        self.axis = scene.visuals.XYZAxis(parent=self.view.scene)
        self.axis.transform = scene.transforms.STTransform(scale=(0.25, 0.25, 0.25))

        self.overlay = scene.Node(parent=self.view.scene)

        self.center_camera()

    def add_visual(self, visual):
        visual.parent = self.view.scene
        self.visuals.append(visual)

    def clear_visuals(self):
        for visual in self.visuals:
            if visual.parent is not None:
                visual.parent = None

        self.visuals.clear()

    def clear_overlay(self):
        if not self.overlay:
            return

        for child in list(self.overlay.children):
            child.parent = None

    def clear_all(self):
        self.clear_visuals()
        self.clear_overlay()

    def center_camera(self):
        if self.view and self.view.camera:
            self.view.camera.set_range(x=(-1, 1),y=(-1, 1),z=(-1, 1))

    def fit_camera(self):
        if self.view and self.view.camera:
            self.view.camera.set_range()

    def reset_camera(self):
        if self.view and self.view.camera:
            self.view.camera = scene.cameras.ArcballCamera()

    def reset_view(self):
        self.reset_camera()

        if self.visuals:
            self.fit_camera()
        else:
            self.center_camera()

    def set_axis(self, visible: bool):
        if self.axis:
            self.axis.visible = visible