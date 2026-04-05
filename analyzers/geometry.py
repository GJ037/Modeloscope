import numpy as np


class GeometryAnalyzer:

    def analyze(self, model, context=None):
        if model is None:
            raise ValueError("Model is None")

        surface_area = float(model.area)
        volume = float(model.volume) if model.is_watertight else 0.0

        bbox = model.bounding_box.extents
        center_mass = model.center_mass
        centroid = model.centroid

        edge_lengths = model.edges_unique_length
        edge_min = float(np.min(edge_lengths)) if len(edge_lengths) else 0.0
        edge_max = float(np.max(edge_lengths)) if len(edge_lengths) else 0.0
        edge_mean = float(np.mean(edge_lengths)) if len(edge_lengths) else 0.0

        face_density_area = (
            len(model.faces) / surface_area if surface_area > 0 else 0.0
        )

        face_density_volume = (
            len(model.faces) / volume if volume > 0 else 0.0
        )

        return {
            "surface_area": round(surface_area, 5),
            "volume": round(volume, 5),

            "bounding_box": [round(float(x), 5) for x in bbox],
            "center_mass": [round(float(x), 5) for x in center_mass],
            "centroid": [round(float(x), 5) for x in centroid],

            "edge_min": round(edge_min, 5),
            "edge_max": round(edge_max, 5),
            "edge_mean": round(edge_mean, 5),

            "face_density_area": round(face_density_area, 5),
            "face_density_volume": round(face_density_volume, 5)
        }