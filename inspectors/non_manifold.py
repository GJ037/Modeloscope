from collections import defaultdict
from .base import BaseInspector


class NonManifoldInspector(BaseInspector):
    """
    Detects non-manifold edges in a mesh.

    Responsibilities:
    - Identifies edges shared by more than two faces
    - Highlights invalid topology configurations

    Used to detect mesh errors that can cause issues in simulation,
    rendering, or manufacturing pipelines.
    """

    def inspect(self, model, context=None):
        if model is None:
            return self.error("Model is None")

        try:
            edge_count = defaultdict(int)
            faces = model.faces

            for face in faces:
                v0, v1, v2 = face

                edges = [
                    tuple(sorted((v0, v1))),
                    tuple(sorted((v1, v2))),
                    tuple(sorted((v2, v0)))
                ]

                for edge in edges:
                    edge_count[edge] += 1

            non_manifold_edges = [
                edge for edge, count in edge_count.items() if count > 2
            ]
        
            data = {
                "type": "non_manifold_edges",
                "payload": {
                    "edges": non_manifold_edges
                }
            }

            return self.success(data)

        except Exception as e:
            return self.error(str(e))