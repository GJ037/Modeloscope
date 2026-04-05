import numpy as np
from collections import defaultdict


class NonManifoldInspector:

    def inspect(self, model):
        if model is None:
            raise ValueError("Model is None")

        faces = model.faces
        vertex_count = len(model.vertices)

        edge_count = defaultdict(int)

        for v0, v1, v2 in faces:
            edges = [
                tuple(sorted((v0, v1))),
                tuple(sorted((v1, v2))),
                tuple(sorted((v2, v0)))
            ]
            for e in edges:
                edge_count[e] += 1

        values = np.zeros(vertex_count)

        for (v0, v1), count in edge_count.items():
            if count > 2:
                values[v0] += count
                values[v1] += count

        return values