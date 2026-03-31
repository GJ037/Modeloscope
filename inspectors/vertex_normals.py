import numpy as np
from collections import defaultdict
from .base import BaseInspector


class VertexNormalsInspector(BaseInspector):
    """
    Detects faces with flipped normals.

    Responsibilities:
    - Identifies faces whose normals point inward
    - Uses mesh center as reference for orientation

    Used to detect incorrect normal orientation which can affect
    lighting, rendering, and simulation.
    """

    def inspect(self, model, context=None):
        if model is None:
            return self.error("Model is None")

        try:
            vertices = model.vertices
            faces = model.faces

            vertex_normals = defaultdict(lambda: np.zeros(3))

            final_normals = []
            final_vertices = []

            for face in faces:
                v0, v1, v2 = face

                p0 = vertices[v0]
                p1 = vertices[v1]
                p2 = vertices[v2]

                e1 = p1 - p0
                e2 = p2 - p0

                normal = np.cross(e1, e2)

                normalize = np.linalg.norm(normal)
                if normalize == 0:
                    continue

                normal = normal / normalize

                vertex_normals[v0] += normal
                vertex_normals[v1] += normal
                vertex_normals[v2] += normal


            for vid, normal in vertex_normals.items():
                normalize = np.linalg.norm(normal)
                if normalize == 0:
                    continue

                normal = normal / normalize

                final_vertices.append(vertices[vid])
                final_normals.append(normal)
        
            data = {
                "type": "vertex_normals",
                "payload": {
                    "vertices": final_vertices,
                    "normals": final_normals
                }
            }

            return self.success(data)

        except Exception as e:
            return self.error(str(e))