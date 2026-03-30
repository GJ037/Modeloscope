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

    def inspect(self, model):
        if model is None:
            raise ValueError("[FaceNormalsInspector] Model is None")

        try:
            vertices = model.vertices
            faces = model.faces

            centers = []
            normals = []

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

                centers.append(center)
                normals.append(normal)
            
            return {
                "status": "success",
                "type": "face_normals",
                "data": {
                    "centers": centers,
                    "normals": normals
                }
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}