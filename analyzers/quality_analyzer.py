import numpy as np

class QualityAnalyzer:

    def analyze(self, model):

        face_areas = model.area_faces
        mean_area = np.mean(face_areas) if len(face_areas) else 0.0

        uniformity = float(np.std(face_areas) / mean_area) if mean_area > 0 else 0.0

        degenerate_faces = int(np.sum(face_areas < 1e-12))

        vertices = model.vertices
        dup_vertices = int(len(vertices) - len(np.unique(vertices.round(6), axis=0)))

        winding_consistent = bool(model.is_winding_consistent)
        self_intersecting = bool(model.is_self_intersecting)

        return {
            "area_uniformity": round(uniformity, 5),
            "degenerate_faces": degenerate_faces,
            "duplicate_vertices": dup_vertices,
            "winding_consistent": winding_consistent,
            "self_intersecting": self_intersecting
        }
