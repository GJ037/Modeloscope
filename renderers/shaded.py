from vispy import scene
from vispy.color import Color


def render_shaded(engine, mesh):
    if mesh is None:
        raise ValueError("Mesh is None")

    mesh = scene.visuals.Mesh(
        vertices=mesh.vertices, faces=mesh.faces,
        color=Color("white"), shading="flat"
    )

    engine.add_visual(mesh)