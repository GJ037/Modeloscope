from vispy import scene


def render_pointcloud(engine, model):
    if model is None:
        raise ValueError("Model is None")

    points = scene.visuals.Markers()

    points.set_data(
        model.vertices,
        face_color="white",
        edge_color=None,
        size=2
    )

    points.antialias = 0

    engine.add_visual(points)