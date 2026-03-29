from inspectors.boundary import BoundaryInspector
from inspectors.non_manifold import NonManifoldInspector
from inspectors.face_normals import FaceNormalsInspector
from inspectors.vertex_normals import VertexNormalsInspector
from inspectors.flipped_normals import FlippedNormalsInspector


class InspectRunner:
    """
    Runs selected inspector and returns inspection result.
    """

    def __init__(self):
        self.inspectors = {
            "boundary": BoundaryInspector(),
            "non_manifold": NonManifoldInspector(),
            "face_normals": FaceNormalsInspector(),
            "vertex_normals": VertexNormalsInspector(),
            "flipped_normals": FlippedNormalsInspector()

        }

    def run(self, model, mode):
        if model is None:
            raise ValueError("[InspectRunner] Model is None")

        if mode not in self.inspectors:
            raise ValueError(f"[InspectRunner] Unknown mode: {mode}")

        inspector = self.inspectors[mode]

        result = inspector.inspect(model)

        return result
    
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