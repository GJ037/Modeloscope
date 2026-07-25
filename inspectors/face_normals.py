import numpy as np


def inspect_face_normals(model):
    if model is None:
        raise ValueError("Model is None")

    faces = model.faces
    vertices = model.vertices
    
    values = np.zeros(len(vertices))

    for v0, v1, v2 in faces:
        p0 = vertices[v0]
        p1 = vertices[v1]
        p2 = vertices[v2]

        normal = np.cross(p1 - p0, p2 - p0)
        normalize = np.linalg.norm(normal)

        if normalize == 0:
            continue

        values[v0] += normalize
        values[v1] += normalize
        values[v2] += normalize

    return values