import numpy as np
from vispy import scene
from vispy.color import Colormap


def heatmap(engine, model, values):
    if values is None or len(values) == 0:
        return

    values = np.array(values)
    vmin = values.min()
    vmax = values.max()

    if vmax - vmin == 0:
        normalized = np.zeros_like(values)
    else:
        normalized = (values - vmin) / (vmax - vmin)

    colormap = Colormap(
        ["navy", "blue", "cyan", "lime", "yellow", "red"])
    
    colors = colormap.map(normalized)

    mesh = scene.visuals.Mesh(
        vertices=model.vertices,
        faces=model.faces,
        vertex_colors=colors
    )

    engine.add_visual(mesh)