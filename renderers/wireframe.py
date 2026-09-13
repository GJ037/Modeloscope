from vispy import scene


def render_wireframe(engine, mesh):
    if mesh is None:
        raise ValueError("Mesh is None")

    edges = mesh.edges_unique

    lines = scene.visuals.Line(
        pos=mesh.vertices[edges].reshape(-1, 3),
        color="white", connect="segments", width=0.5
    )

    engine.add_visual(lines)