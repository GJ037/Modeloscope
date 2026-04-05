from vispy import scene
from vispy.color import Color


class FlatRenderer:

    def render(self, engine, model):
        if model is None:
            raise ValueError("Model is None")

        mesh = scene.visuals.Mesh(
            vertices=model.vertices,
            faces=model.faces,
            color=Color("white")
        )

        engine.add_visual(mesh)