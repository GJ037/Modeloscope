import numpy as np
from collections import defaultdict


class VertexNormalsInspector:

    def inspect(self, model):
        if model is None:
            raise ValueError("Model is None")

        vertices = model.vertices
        faces = model.faces

        normals = defaultdict(lambda: np.zeros(3))

        for v0, v1, v2 in faces:
            p0 = vertices[v0]
            p1 = vertices[v1]
            p2 = vertices[v2]

            normal = np.cross(p1 - p0, p2 - p0)
            normalize = np.linalg.norm(normal)

            if normalize == 0:
                continue

            normal /= normalize

            normals[v0] += normal
            normals[v1] += normal
            normals[v2] += normal

        values = np.zeros(len(vertices))

        for vid, normal in normals.items():
            values[vid] = np.linalg.norm(normal)

        return values