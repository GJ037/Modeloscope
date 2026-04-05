import numpy as np


class QualityAnalyzer:

    def analyze(self, model, context=None):
        if model is None:
            raise ValueError("Model is None")

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

        return {
            "area_uniformity": round(uniformity, 5),
            "degenerate_faces": degenerate_faces,
            "duplicate_vertices": duplicate_vertices,

            "winding_consistent": bool(model.is_winding_consistent),
            "watertight": bool(model.is_watertight)
        }