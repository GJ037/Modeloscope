from vispy import scene
from vispy.color import Color


def render_flat(engine, mesh):
    if mesh is None:
        raise ValueError("Mesh is None")

    mesh = scene.visuals.Mesh(
        vertices=mesh.vertices, faces=mesh.faces,
        color=Color("white")
    )

    engine.add_visual(mesh)