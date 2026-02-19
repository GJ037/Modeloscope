import numpy as np

class TopologyAnalyzer:

    def analyze(self, model):

        vertex_count = int(len(model.vertices))
        face_count = int(len(model.faces))
        edge_count = int(len(model.edges_unique))

        euler_number = int(model.euler_number)
        watertight = bool(model.is_watertight)

        components = int(len(model.split(only_watertight=False)))

        non_manifold_edges = int(np.sum(model.edges_unique_counts > 2))

        return {
            "vertex_count": vertex_count,
            "face_count": face_count,
            "edge_count": edge_count,
            "euler_number": euler_number,
            "watertight": watertight,
            "connected_components": components,
            "non_manifold_edges": non_manifold_edges
        }
