import numpy as np

class QualityAnalyzer:
    """
    Evaluates mesh quality and structural integrity.

    Calculates:
        - Face area uniformity (standard deviation ratio)
        - Number of degenerate faces
        - Duplicate vertex count
        - Winding consistency
        - Watertight status
    """

    def analyze(self, model):

        if model is None:
            print("[QualityAnalyzer ERROR] model is None")
            return None

        try:
            face_areas = model.area_faces
            mean_area = np.mean(face_areas) if len(face_areas) else 0.0

            uniformity = float(np.std(face_areas) / mean_area) if mean_area > 0 else 0.0
            degenerate_faces = int(np.sum(face_areas < 1e-12))

            vertices = model.vertices
            duplicate_vertices = int(len(vertices) - len(np.unique(vertices.round(6), axis=0)))

            winding_consistent = bool(model.is_winding_consistent)
            watertight = bool(model.is_watertight)

            return {
                "area_uniformity": round(uniformity, 5),
                "degenerate_faces": degenerate_faces,
                "duplicate_vertices": duplicate_vertices,
                "winding_consistent": winding_consistent,
                "watertight": watertight
            }

        except Exception as e:
            print(f"[QualityAnalyzer ERROR] {e}")
            return None
        