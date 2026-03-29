from collections import defaultdict
from .base import BaseInspector


class BoundaryInspector(BaseInspector):
    """
    Detects boundary edges (holes in mesh).
    """

    def inspect(self, model):
        if model is None:
            raise ValueError("[BoundaryInspector] Model is None")

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

        # Extract boundary edges
        boundary_edges = [
            edge for edge, count in edge_count.items() if count == 1
        ]

        return {
            "type": "boundary_edges",
            "edges": boundary_edges
        }