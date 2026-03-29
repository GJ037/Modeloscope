from collections import defaultdict
from .base import BaseInspector


class NonManifoldInspector(BaseInspector):
    """
    Detects non-manifold edges (edges shared by more than 2 faces).
    """

    def inspect(self, model):
        if model is None:
            raise ValueError("[NonManifoldInspector] Model is None")

        edge_count = defaultdict(int)
        faces = model.faces

        # Count edges
        for face in faces:
            v0, v1, v2 = face

            edges = [
                tuple(sorted((v0, v1))),
                tuple(sorted((v1, v2))),
                tuple(sorted((v2, v0)))
            ]

            for edge in edges:
                edge_count[edge] += 1

        # Extract non-manifold edges (>2 faces)
        non_manifold_edges = [
            edge for edge, count in edge_count.items() if count > 2
        ]

        return {
            "type": "non_manifold_edges",
            "edges": non_manifold_edges
        }