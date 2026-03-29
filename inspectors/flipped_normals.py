import numpy as np
from .base import BaseInspector


class FlippedNormalsInspector(BaseInspector):
    """
    Detects faces with flipped normals using mesh center heuristic.
    """

    def inspect(self, model):
        if model is None:
            raise ValueError("[FlippedNormalsInspector] Model is None")

        vertices = model.vertices
        faces = model.faces

        # Compute mesh center
        mesh_center = np.mean(vertices, axis=0)

        flipped_centers = []
        flipped_normals = []

        for face in faces:
            v0, v1, v2 = face

            p0 = vertices[v0]
            p1 = vertices[v1]
            p2 = vertices[v2]

            # edges
            e1 = p1 - p0
            e2 = p2 - p0

            normal = np.cross(e1, e2)

            norm = np.linalg.norm(normal)
            if norm == 0:
                continue

            normal = normal / norm

            # face center
            center = (p0 + p1 + p2) / 3

            # direction from mesh center
            direction = center - mesh_center

            # dot product test
            if np.dot(normal, direction) < 0:
                flipped_centers.append(center)
                flipped_normals.append(normal)

        print(f"[FlippedNormalsInspector] Faces: {len(faces)}")
        print(f"[FlippedNormalsInspector] Flipped: {len(flipped_centers)}")

        return {
            "type": "flipped_normals",
            "centers": flipped_centers,
            "normals": flipped_normals
        }