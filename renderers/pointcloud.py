from vispy import scene


def render_pointcloud(engine, mesh):
    if mesh is None:
        raise ValueError("Mesh is None")

    points = scene.visuals.Markers()

    points.set_data(
        mesh.vertices, face_color="white",
        edge_color=None, size=2
    )

    points.antialias = 0

    engine.add_visual(points)