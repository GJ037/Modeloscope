import numpy as np

class GeometryAnalyzer:

    def analyze(self, mesh):

        surface_area = float(mesh.area)
        volume = float(mesh.volume) if mesh.is_watertight else 0.0

        bbox = mesh.bounding_box.extents
        center = mesh.center_mass

        edge_lengths = mesh.edges_unique_length
        edge_min = float(np.min(edge_lengths)) if len(edge_lengths) else 0.0
        edge_max = float(np.max(edge_lengths)) if len(edge_lengths) else 0.0
        edge_mean = float(np.mean(edge_lengths)) if len(edge_lengths) else 0.0

        area = surface_area if surface_area > 0 else 1.0
        face_density_area = float(len(mesh.faces) / area)

        volume_safe = volume if volume > 0 else 1.0
        face_density_volume = float(len(mesh.faces) / volume_safe)

        return {
            "surface_area": round(surface_area, 5),
            "volume": round(volume, 5),
            "bbox_x": round(float(bbox[0]), 5),
            "bbox_y": round(float(bbox[1]), 5),
            "bbox_z": round(float(bbox[2]), 5),
            "center_x": round(float(center[0]), 5),
            "center_y": round(float(center[1]), 5),
            "center_z": round(float(center[2]), 5),
            "edge_min": round(edge_min, 5),
            "edge_max": round(edge_max, 5),
            "edge_mean": round(edge_mean, 5),
            "face_density_area": round(face_density_area, 5),
            "face_density_volume": round(face_density_volume, 5)
        }
