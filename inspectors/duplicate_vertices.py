import numpy as np


def inspect_duplicate_vertices(model):
    if model is None:
        raise ValueError("Model is None")

    vertices = model.vertices
    
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
