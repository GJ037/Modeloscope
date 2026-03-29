from core.loader import ModelLoader
from core.engine import RenderEngine
from renderers.standard import StandardRenderer
from renderers.wireframe import WireframeRenderer
from renderers.pointcloud import PointCloudRenderer


RENDERERS = {
    "standard": StandardRenderer,
    "wireframe": WireframeRenderer,
    "pointcloud": PointCloudRenderer
}


class RenderRunner:
    """
    Orchestrates the rendering pipeline.

    Responsibilities:
    - Loads the model using ModelLoader
    - Selects the appropriate renderer based on mode
    - Controls the rendering sequence (clear → render → adjust camera)
    - Coordinates interaction between engine and renderers

    Acts as the execution layer that connects model data with
    rendering logic in a controlled and predictable flow.
    """

    def __init__(self, parent):
        self.engine = RenderEngine()
        self.engine.initialize(parent)

    def render(self, file_path, mode):
        if not file_path:
            return {"status": "error", "message": "Invalid file path"}

        loader = ModelLoader()
        result = loader.load(file_path)

        if result["status"] != "success":
            return result

        model = result["model"]
        self.model = model

        self.reset_scene()

        renderer_class = RENDERERS.get(mode)

        if not renderer_class:
            return {"status": "error", "message": f"Unknown mode: {mode}"}
        
        renderer = renderer_class()
        render_result = renderer.render(self.engine, model)

        if render_result["status"] != "success":
            return render_result

        self.engine.fit_camera()
        self.engine.set_axis(False)

        return {"status": "success"}
    
    def reset_scene(self):
        if self.engine:
            self.engine.clear_scene()
            self.engine.set_axis(True)

            self.engine.reset_camera()
            self.engine.fit_axis()

    def reset_view(self):
        if self.engine:
            self.engine.set_axis(True)

            self.engine.reset_camera()
            self.engine.fit_axis()