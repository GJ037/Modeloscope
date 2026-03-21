import numpy as np
from analyzers.base import BaseAnalyzer


class QualityAnalyzer(BaseAnalyzer):
    """
    Evaluates mesh integrity and structural quality.

    Responsibilities:
    - Measures face area uniformity
    - Detects degenerate faces
    - Identifies duplicate vertices
    - Checks winding consistency and watertightness
    - Evaluates convexity and volume validity

    Identifies structural issues and numerical inconsistencies
    within the mesh.
    """

    def analyze(self, model, context=None):

        if model is None:
            return self.error("Model is None")

        try:
            face_areas = model.area_faces
            mean_area = np.mean(face_areas) if len(face_areas) else 0.0

            uniformity = (
                float(np.std(face_areas) / mean_area) if mean_area > 0 else 0.0
            )

            degenerate_faces = int(np.sum(face_areas < 1e-12))

            vertices = model.vertices
            duplicate_vertices = int(
                len(vertices) - len(np.unique(vertices.round(6), axis=0))
            )

            data = {
                "area_uniformity": round(uniformity, 5),
                "degenerate_faces": degenerate_faces,
                "duplicate_vertices": duplicate_vertices,

                "winding_consistent": bool(model.is_winding_consistent),
                "watertight": bool(model.is_watertight),

                "is_convex": bool(model.is_convex),
                "is_volume": bool(model.is_volume),
            }

            return self.success(data)

        except Exception as e:
            return self.error(str(e))