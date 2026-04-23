from cores.loader import ModelLoader
from renderers.flat import FlatRenderer
from renderers.shaded import ShadedRenderer
from renderers.wireframe import WireframeRenderer
from renderers.pointcloud import PointCloudRenderer

RENDERERS = {
    "flat": FlatRenderer,
    "shaded": ShadedRenderer,
    "wireframe": WireframeRenderer,
    "pointcloud": PointCloudRenderer
}


class RenderRunner:

    def __init__(self, engine):
        self.engine = engine

    def load(self, file_path, mode):
        if not file_path:
            raise ValueError("Invalid file path")

        model, meta = ModelLoader().load(file_path)

        renderer_class = RENDERERS.get(mode)
        if not renderer_class:
            raise ValueError(f"Unknown render mode: {mode}")
        
        return model, renderer_class
    
    def render(self, model, renderer_class):
        self.engine.clear_all()

        renderer = renderer_class()
        renderer.render(self.engine, model)

        self.engine.reset_view()
        self.engine.set_axis(False)