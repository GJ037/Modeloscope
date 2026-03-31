from core.loader import ModelLoader
from core.engine import RenderEngine
from renderers.standard import StandardRenderer
from renderers.highlight import HighlightRenderer
from inspectors.boundary import BoundaryInspector
from inspectors.non_manifold import NonManifoldInspector
from inspectors.face_normals import FaceNormalsInspector
from inspectors.vertex_normals import VertexNormalsInspector
from inspectors.flipped_normals import FlippedNormalsInspector


INSPECTORS = {
    "boundary": BoundaryInspector,
    "non_manifold": NonManifoldInspector,
    "face_normals": FaceNormalsInspector,
    "vertex_normals": VertexNormalsInspector,
    "flipped_normals": FlippedNormalsInspector
}


class InspectRunner:
    """
    Orchestrates the inspection pipeline.

    Responsibilities:
    - Loads the model using ModelLoader
    - Renders base mesh using StandardRenderer
    - Runs selected inspector
    - Renders overlay using HighlightRenderer

    Acts as the execution layer that connects model data with
    inspection logic and visualization in a controlled flow.
    """

    def __init__(self, parent):
        self.engine = RenderEngine()
        self.engine.initialize(parent)

        self.model = None

    def inspect(self, file_path, mode, context=None):

        if not file_path:
            return {"status": "error", "message": "Invalid file path"}

        loader = ModelLoader()
        result = loader.load(file_path)

        if result["status"] != "success":
            return result

        data = result["data"]
        model = data["model"]
        meta = data["meta"]
        context = {}

        self.model = model

        self.reset_scene()

        renderer = StandardRenderer()
        render_result = renderer.render(self.engine, model)

        if render_result["status"] != "success":
            return render_result

        inspector_class = INSPECTORS.get(mode)

        if not inspector_class:
            return {"status": "error", "message": f"Unknown mode: {mode}"}

        inspector = inspector_class()
        inspect_result = inspector.inspect(model, context)

        if inspect_result["status"] != "success":
            return inspect_result

        highlight_renderer = HighlightRenderer()
        highlight_renderer.render(self.engine, model, inspect_result)

        self.engine.fit_camera()
        self.engine.set_axis(False)

        return {
            "status": "success",
            "data": inspect_result["data"]
        }

    def reset_scene(self):
        if self.engine:
            self.engine.clear_scene()
            self.engine.clear_overlay()

            self.engine.set_axis(True)
            self.engine.reset_camera()
            self.engine.fit_axis()

    def reset_view(self):
        if self.engine:
            self.engine.set_axis(True)

            self.engine.reset_camera()
            self.engine.fit_axis()