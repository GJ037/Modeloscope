import numpy as np


def inspect_duplicate_vertices(mesh):
    if mesh is None:
        raise ValueError("Mesh is None")

    vertices = mesh.vertices
    
    values = np.zeros(len(vertices))
    visited = {}

    for index, vertex in enumerate(vertices):
        key = tuple(np.round(vertex / 1e-12).astype(int))

        if key in visited:
            values[index] += 1
            values[visited[key]] += 1
            
        else:
            visited[key] = index

    return values
