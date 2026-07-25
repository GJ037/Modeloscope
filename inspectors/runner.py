from cores.loader import load
from inspectors.overlay import heatmap
from inspectors.boundary_edges import inspect_boundary_edges
from inspectors.non_manifold_edges import inspect_non_manifold_edges
from inspectors.face_normals import inspect_face_normals
from inspectors.flipped_normals import inspect_flipped_normals

INSPECTORS = {
    "boundary_edges": inspect_boundary_edges,
    "non_manifold_edges": inspect_non_manifold_edges,
    "face_normals": inspect_face_normals,
    "flipped_normals": inspect_flipped_normals
}


class InspectRunner:

    def __init__(self, engine):
        self.engine = engine

    def load(self, file_path, mode):
        if not file_path:
            raise ValueError("Invalid file path")

        model, meta = load(file_path)
        inspector = INSPECTORS.get(mode)

        if not inspector:
            raise ValueError(f"Unknown inspect mode: {mode}")

        return model, inspector

    def inspect(self, model, inspector):
        values = inspector(model)
        self.engine.clear_all()

        heatmap(self.engine, model, values)

        self.engine.reset_view()
        self.engine.set_axis(False)