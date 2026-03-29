import numpy as np
from .base import BaseInspector


class FaceNormalsInspector(BaseInspector):
    """
    Computes face normals for visualization.
    """

    def inspect(self, model):
        if model is None:
            raise ValueError("[FaceNormalsInspector] Model is None")

        vertices = model.vertices
        faces = model.faces

        centers = []
        normals = []

        for face in faces:
            v0, v1, v2 = face

            p0 = vertices[v0]
            p1 = vertices[v1]
            p2 = vertices[v2]

            # Compute edges
            e1 = p1 - p0
            e2 = p2 - p0

            # Cross product → normal
            normal = np.cross(e1, e2)

            # Normalize
            norm = np.linalg.norm(normal)
            if norm == 0:
                continue

            normal = normal / norm

            # Face center
            center = (p0 + p1 + p2) / 3

            centers.append(center)
            normals.append(normal)

        print(f"[FaceNormalsInspector] Faces: {len(faces)}")
        print(f"[FaceNormalsInspector] Valid normals: {len(normals)}")
        
        return {
            "type": "face_normals",
            "centers": centers,
            "normals": normals
        }