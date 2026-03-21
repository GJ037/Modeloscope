from vispy import scene
from vispy.color import Color
from renderers.base import BaseRenderer


class StandardRenderer(BaseRenderer):
    """
    Renders the mesh using shaded triangle surfaces.

    Responsibilities:
    - Creates a mesh visual from model vertices and faces
    - Applies basic shading for surface visualization
    - Submits the visual to the engine for rendering

    Provides a standard solid view of the model highlighting its
    surface geometry.
    """
    
    def render(self, engine, model):
        if model is None:
            return {"status": "error", "message": "Model is None"}

        try:
            mesh = scene.visuals.Mesh(
                vertices=model.vertices,
                faces=model.faces,
                color=Color("white"),
                shading="flat"
            )

            engine.add_visual(mesh)

            return {"status": "success"}

        except Exception as e:
            return {"status": "error", "message": str(e)}