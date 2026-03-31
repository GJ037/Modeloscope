from collections import defaultdict
from .base import BaseInspector


class BoundaryInspector(BaseInspector):
    """
    Detects boundary edges in a mesh.

    Responsibilities:
    - Identifies edges that belong to only one face
    - Highlights open boundaries or holes in the mesh

    Used to detect mesh incompleteness and topology issues related
    to missing faces or non-closed surfaces.
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

            boundary_edges = [
                edge for edge, count in edge_count.items() if count == 1
            ]

            data = {
                "type": "boundary_edges",
                "payload": {
                    "edges": boundary_edges
                }
            }

            return self.success(data)

        except Exception as e:
            return self.error(str(e))