import numpy as np
from collections import defaultdict
from .base import BaseInspector


class VertexNormalsInspector(BaseInspector):
    """
    Computes vertex normals by averaging adjacent face normals.
    """

    def inspect(self, model):
        if model is None:
            raise ValueError("[VertexNormalsInspector] Model is None")

        vertices = model.vertices
        faces = model.faces

        vertex_normals = defaultdict(lambda: np.zeros(3))

        # Step 1: compute face normals and accumulate
        for face in faces:
            v0, v1, v2 = face

            p0 = vertices[v0]
            p1 = vertices[v1]
            p2 = vertices[v2]

            e1 = p1 - p0
            e2 = p2 - p0

            normal = np.cross(e1, e2)

            norm = np.linalg.norm(normal)
            if norm == 0:
                continue

            normal = normal / norm

            # accumulate to each vertex
            vertex_normals[v0] += normal
            vertex_normals[v1] += normal
            vertex_normals[v2] += normal

        # Step 2: normalize vertex normals
        final_normals = []
        final_vertices = []

        for vid, normal in vertex_normals.items():
            norm = np.linalg.norm(normal)
            if norm == 0:
                continue

            normal = normal / norm

            final_vertices.append(vertices[vid])
            final_normals.append(normal)

        print(f"[VertexNormalsInspector] Vertices: {len(vertices)}")
        print(f"[VertexNormalsInspector] Valid normals: {len(final_normals)}")

        return {
            "type": "vertex_normals",
            "vertices": final_vertices,
            "normals": final_normals
        }