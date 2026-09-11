import numpy as np


def analyze_node(mesh):
    if mesh is None:
        raise ValueError("Mesh is None")

    vertex_count = int(len(mesh.vertices))

    distance_to_centroid = np.linalg.norm(mesh.vertices - mesh.centroid, axis=1)
    distance_to_centroid_min = float(np.min(distance_to_centroid))
    distance_to_centroid_max = float(np.max(distance_to_centroid))
    distance_to_centroid_mean = float(np.mean(distance_to_centroid))
    distance_to_centroid_variance = float(np.var(distance_to_centroid))

    centroid = mesh.centroid.tolist()
    center_mass = mesh.center_mass.tolist()

    duplicate_vertices = int(len(mesh.vertices) - len(np.unique(mesh.vertices, axis=0)))
    duplicate_vertex_ratio = float(duplicate_vertices / len(mesh.vertices)) if len(mesh.vertices) else 0.0

    features = {
        "vertex_count": vertex_count,

        "distance_to_centroid_min": distance_to_centroid_min,
        "distance_to_centroid_max": distance_to_centroid_max,
        "distance_to_centroid_mean": distance_to_centroid_mean,
        "distance_to_centroid_variance": distance_to_centroid_variance,

        "centroid": centroid,
        "center_mass": center_mass,
        
        "duplicate_vertices": duplicate_vertices,
        "duplicate_vertex_ratio": duplicate_vertex_ratio
    }

    return features