from vispy import scene


def render_wireframe(engine, model):
    if model is None:
        raise ValueError("Model is None")

    edges = model.edges_unique

    lines = scene.visuals.Line(
        pos=model.vertices[edges].reshape(-1, 3),
        color="white",
        connect="segments",
        width=0.5
    )

    engine.add_visual(lines)