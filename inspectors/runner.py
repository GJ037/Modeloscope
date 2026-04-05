from cores.loader import ModelLoader
from overlays.heatmap import HeatmapOverlay
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

    def __init__(self, engine):
        self.engine = engine

    def run(self, file_path, mode):
        if not file_path:
            raise ValueError("Invalid file path")

        inspector_class = INSPECTORS.get(mode)
        if not inspector_class:
            raise ValueError(f"Unknown inspect mode: {mode}")

        model, meta = ModelLoader().load(file_path)

        self.engine.clear_all()

        inspector = inspector_class()
        values = inspector.inspect(model)

        overlay = HeatmapOverlay()
        overlay.heatmap(self.engine, model, values)

        self.engine.reset_view()
        self.engine.set_axis(False)