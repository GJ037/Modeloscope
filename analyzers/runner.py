from functions.loader import load_mesh
from functions.grouper import group_features
from analyzers.node import analyze_node
from analyzers.edge import analyze_edge
from analyzers.mesh import analyze_mesh


def analyze(file_path: str):
    if not file_path:
        raise ValueError("Invalid file path")

    mesh = load_mesh(file_path)

    node_features = analyze_node(mesh)
    edge_features = analyze_edge(mesh)
    mesh_features = analyze_mesh(mesh)

    grouped_features = group_features(node_features, edge_features, mesh_features)

    return grouped_features