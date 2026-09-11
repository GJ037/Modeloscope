import numpy as np


def analyze_edge(mesh):
    if mesh is None:
        raise ValueError("Mesh is None")

    edge_count = int(len(mesh.edges_unique))

    edge_length_min = float(np.min(mesh.edges_unique_length)) if len(mesh.edges_unique_length) else 0.0
    edge_length_max = float(np.max(mesh.edges_unique_length)) if len(mesh.edges_unique_length) else 0.0
    edge_length_mean = float(np.mean(mesh.edges_unique_length)) if len(mesh.edges_unique_length) else 0.0
    edge_length_variance = float(np.var(mesh.edges_unique_length)) if len(mesh.edges_unique_length) else 0.0

    degenerate_edges = int(np.sum(mesh.edges_unique_length < 1e-12))
    sharp_edges = int(np.sum(mesh.face_adjacency_angles > np.deg2rad(30)))

    degenerate_edge_ratio = float(degenerate_edges / len(mesh.edges_unique)) if len(mesh.edges_unique) else 0.0
    sharp_edge_ratio = float(sharp_edges / len(mesh.face_adjacency_angles)) if len(mesh.face_adjacency_angles) else 0.0

    features = {
        "edge_count": edge_count,

        "edge_length_min": edge_length_min,
        "edge_length_max": edge_length_max,
        "edge_length_mean": edge_length_mean,
        "edge_length_variance": edge_length_variance,

        "degenerate_edges": degenerate_edges,
        "sharp_edges": sharp_edges,

        "degenerate_edge_ratio": degenerate_edge_ratio,
        "sharp_edge_ratio": sharp_edge_ratio
    }

    return features