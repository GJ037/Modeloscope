from cores.loader import load
from renderers.flat import render_flat
from renderers.shaded import render_shaded
from renderers.wireframe import render_wireframe
from renderers.pointcloud import render_pointcloud

RENDERERS = {
    "flat": render_flat,
    "shaded": render_shaded,
    "wireframe": render_wireframe,
    "pointcloud": render_pointcloud
}


class RenderRunner:
    
    def __init__(self, engine):
        self.engine = engine

    def load(self, file_path, mode):
        if not file_path:
            raise ValueError("Invalid file path")

        model, meta = load(file_path)
        renderer = RENDERERS.get(mode)
        
        if not renderer:
            raise ValueError(f"Unknown render mode: {mode}")
        
        return model, renderer
    
    def render(self, model, renderer):
        self.engine.clear_all()

        renderer(self.engine, model)

        self.engine.reset_view()
        self.engine.set_axis(False)