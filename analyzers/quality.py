import numpy as np


def analyze_quality(model, context=None):
    if model is None:
        raise ValueError("Model is None")

    vertices = model.vertices
    face_areas = model.area_faces

    duplicate_vertices = int(len(vertices) - len(np.unique(vertices.round(6), axis=0)))

    mean_area = np.mean(face_areas) if len(face_areas) else 0.0
    area_uniformity = float(np.std(face_areas) / mean_area) if mean_area > 0 else 0.0
    degenerate_faces = int(np.sum(face_areas < 1e-12))

    return {
        "duplicate_vertices": duplicate_vertices,

        "area_uniformity": round(area_uniformity, 5),
        "degenerate_faces": degenerate_faces,

        "winding_consistent": bool(model.is_winding_consistent),
        "watertight": bool(model.is_watertight)
    }