import numpy as np

class TopologyAnalyzer:

    def analyze(self, mesh):

        vertex_count = int(len(mesh.vertices))
        face_count = int(len(mesh.faces))
        edge_count = int(len(mesh.edges_unique))

        euler_number = int(mesh.euler_number)
        watertight = bool(mesh.is_watertight)

        components = int(len(mesh.split(only_watertight=False)))

        non_manifold_edges = int(np.sum(mesh.edges_unique_counts > 2))

        return {
            "vertex_count": vertex_count,
            "face_count": face_count,
            "edge_count": edge_count,
            "euler_number": euler_number,
            "watertight": watertight,
            "connected_components": components,
            "non_manifold_edges": non_manifold_edges
        }
