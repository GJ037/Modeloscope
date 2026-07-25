from vispy import scene
from vispy.color import Color


def render_flat(engine, model):
    if model is None:
        raise ValueError("Model is None")

    mesh = scene.visuals.Mesh(
        vertices=model.vertices,
        faces=model.faces,
        color=Color("white")
    )

    engine.add_visual(mesh)