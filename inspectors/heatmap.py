import numpy as np
from vispy import scene
from vispy.color import get_colormap


def render_heatmap(engine, mesh, values):
    if values is None or len(values) == 0:
        return

    values = np.array(values)
    vmin, vmax = values.min(), values.max()

    if vmax - vmin == 0:
        normalized = np.zeros_like(values)
    else:
        normalized = (values - vmin) / (vmax - vmin)

    colormap = get_colormap("coolwarm")
    colors = colormap.map(normalized)

    mesh = scene.visuals.Mesh(
        vertices=mesh.vertices,faces=mesh.faces,
        vertex_colors=colors
    )

    engine.add_visual(mesh)