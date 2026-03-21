from vispy import scene
from renderers.base import BaseRenderer


class WireframeRenderer(BaseRenderer):
    """
    Renders the mesh as a wireframe representation.

    Responsibilities:
    - Extracts unique edges from the mesh
    - Constructs line segments representing mesh edges
    - Submits the wireframe visual to the engine

    Highlights the structural connectivity and topology of the mesh.
    """
    
    def render(self, engine, model):
        if model is None:
            return {"status": "error", "message": "Model is None"}

        try:
            edges = model.edges_unique

            lines = scene.visuals.Line(
                pos=model.vertices[edges].reshape(-1, 3),
                color="white",
                connect="segments",
                width=0.5
            )

            engine.add_visual(lines)

            return {"status": "success"}

        except Exception as e:
            return {"status": "error", "message": str(e)}