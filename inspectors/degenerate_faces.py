import numpy as np


def inspect_degenerate_faces(model):
    if model is None:
        raise ValueError("Model is None")

    faces = model.faces
    vertices = model.vertices
    
    values = np.zeros(len(vertices))

    for v0, v1, v2 in faces:
        p0, p1, p2 = vertices[v0], vertices[v1], vertices[v2]

        normal = np.cross(p1 - p0, p2 - p0)
        normalize = np.linalg.norm(normal)
        area = normalize / 2.0

        if area < 1e-12:
            values[v0] += 1
            values[v1] += 1
            values[v2] += 1

    return values