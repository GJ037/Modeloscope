import numpy as np


def inspect_flipped_normals(mesh):
    if mesh is None:
        raise ValueError("Mesh is None")

    faces = mesh.faces
    vertices = mesh.vertices

    mesh_center = np.mean(vertices, axis=0)
    values = np.zeros(len(vertices))

    for v0, v1, v2 in faces:
        p0, p1, p2 = vertices[v0], vertices[v1], vertices[v2]

        normal = np.cross(p1 - p0, p2 - p0)
        normalize = np.linalg.norm(normal)

        if normalize == 0:
            continue

        normal /= normalize

        center = (p0 + p1 + p2) / 3
        direction = center - mesh_center

        if np.dot(normal, direction) < 0:
            values[v0] += 1
            values[v1] += 1
            values[v2] += 1

    return values