import numpy as np
from analyzers.base import BaseAnalyzer


class GeometryAnalyzer(BaseAnalyzer):
    """
    Computes geometric properties of a 3D mesh.

    Responsibilities:
    - Calculates surface area and volume
    - Extracts bounding box dimensions (oriented when possible)
    - Determines spatial centers (center of mass and centroid)
    - Analyzes edge length distribution (min, max, mean)
    - Computes face density relative to area and volume

    Purely concerned with shape, size, and spatial characteristics
    of the mesh.
    """

    def analyze(self, model, context=None):

        if model is None:
            return self.error("Model is None")

        try:
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

            data = {
                "surface_area": round(surface_area, 5),
                "volume": round(volume, 5),

                "bbox_x": round(float(bbox[0]), 5),
                "bbox_y": round(float(bbox[1]), 5),
                "bbox_z": round(float(bbox[2]), 5),

                "center_mass": [round(float(x), 5) for x in center_mass],
                "centroid": [round(float(x), 5) for x in centroid],

                "edge_min": round(edge_min, 5),
                "edge_max": round(edge_max, 5),
                "edge_mean": round(edge_mean, 5),

                "face_density_area": round(face_density_area, 5),
                "face_density_volume": round(face_density_volume, 5)
            }

            return self.success(data)

        except Exception as e:
            return self.error(str(e))