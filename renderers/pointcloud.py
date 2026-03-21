from vispy import scene
from renderers.base import BaseRenderer


class PointCloudRenderer(BaseRenderer):
    """
    Renders the mesh as a point cloud.

    Responsibilities:
    - Uses mesh vertices as point positions
    - Creates marker visuals for each vertex
    - Submits the point cloud to the engine

    Provides a lightweight visualization of the mesh geometry
    without surface or edge connectivity.
    """

    def render(self, engine, model):
        if model is None:
            return {"status": "error", "message": "Model is None"}

        try:
            points = scene.visuals.Markers()

            points.set_data(
                model.vertices,
                face_color="white",
                edge_color=None,
                size=2
            )

            points.antialias = 0

            engine.add_visual(points)

            return {"status": "success"}

        except Exception as e:
            return {"status": "error", "message": str(e)}