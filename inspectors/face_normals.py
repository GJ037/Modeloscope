import numpy as np
from .base import BaseInspector


class FaceNormalsInspector(BaseInspector):
    """
    Computes face normals for visualization.

    Responsibilities:
    - Calculates normal vectors for each face
    - Computes face centers for visualization

    Used to visualize surface orientation and detect shading or
    geometric inconsistencies.
    """

    def inspect(self, model, context=None):
        if model is None:
            return self.error("Model is None")

        try:
            vertices = model.vertices
            faces = model.faces

            face_centers = []
            face_normals = []

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

                center = (p0 + p1 + p2) / 3

                face_centers.append(center)
                face_normals.append(normal)

            data = {
                "type": "face_normals",
                "payload": {
                    "centers": face_centers,
                    "normals": face_normals
                }
            }

            return self.success(data)

        except Exception as e:
            return self.error(str(e))