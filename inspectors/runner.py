from cores.loader import ModelLoader
from inspectors.overlay import HeatmapOverlay
from inspectors.boundary_edges import BoundaryEdgesInspector
from inspectors.non_manifold_edges import NonManifoldEdgesInspector
from inspectors.face_normals import FaceNormalsInspector
from inspectors.flipped_normals import FlippedNormalsInspector

INSPECTORS = {
    "boundary_edges": BoundaryEdgesInspector,
    "non_manifold_edges": NonManifoldEdgesInspector,
    "face_normals": FaceNormalsInspector,
    "flipped_normals": FlippedNormalsInspector
}


class InspectRunner:

    def __init__(self, engine):
        self.engine = engine

    def load(self, file_path, mode):
        if not file_path:
            raise ValueError("Invalid file path")

        model, meta = ModelLoader().load(file_path)

        inspector_class = INSPECTORS.get(mode)
        if not inspector_class:
            raise ValueError(f"Unknown inspect mode: {mode}")

        inspector = inspector_class()
        values = inspector.inspect(model)

        return model, values

    def inspect(self, model, values):
        self.engine.clear_all()

        overlay = HeatmapOverlay()
        overlay.heatmap(self.engine, model, values)

        self.engine.reset_view()
        self.engine.set_axis(False)