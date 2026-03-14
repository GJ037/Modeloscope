from vispy import scene

class PointCloudRenderer:
    """
    Renders vertices as a point cloud.
    """

    def render(self, engine, model):

        if model is None:
            print("[PointCloudRenderer ERROR] model is None")
            return None

        try:
            points = scene.visuals.Markers()

            points.set_data(
                model.vertices,
                face_color="white",
                symbol="disc",
                size=3
            )

            engine.add_visual(points)
            return True

        except Exception as e:
            print(f"[PointCloudRenderer ERROR] {e}")
            return None