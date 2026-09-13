import numpy as np


def inspect_sharp_edges(model):
    if model is None:
        raise ValueError("Model is None")

    faces = model.faces
    vertices = model.vertices

    threshold = np.deg2rad(60.0)
    values = np.zeros(len(vertices))

    edge_faces = {}
    for index, (v0, v1, v2) in enumerate(faces):
        edges = [
            tuple(sorted((v0, v1))),
            tuple(sorted((v1, v2))),
            tuple(sorted((v2, v0)))
        ]
        
        for edge in edges:
            edge_faces.setdefault(edge, []).append(index)

    for (v0, v1), adjacent_faces in edge_faces.items():
        if len(adjacent_faces) == 2:
            f1, f2 = adjacent_faces

            n1 = np.cross(vertices[faces[f1][1]] - vertices[faces[f1][0]],
                          vertices[faces[f1][2]] - vertices[faces[f1][0]])
            n2 = np.cross(vertices[faces[f2][1]] - vertices[faces[f2][0]],
                          vertices[faces[f2][2]] - vertices[faces[f2][0]])

            if np.linalg.norm(n1) == 0 or np.linalg.norm(n2) == 0:
                continue

            n1 /= np.linalg.norm(n1)
            n2 /= np.linalg.norm(n2)

            angle = np.arccos(np.clip(np.dot(n1, n2), -1.0, 1.0))
            if angle > threshold:
                values[v0] += 1
                values[v1] += 1

    return values