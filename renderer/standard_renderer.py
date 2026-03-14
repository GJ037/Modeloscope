from vispy import scene
from vispy.color import Color

class StandardRenderer:
    """
    Renders mesh using shaded triangles.
    """

    def render(self, engine, model):

        if model is None:
            print("[StandardRenderer ERROR] model is None")
            return None

        try:
            mesh = scene.visuals.Mesh(
                vertices=model.vertices,
                faces=model.faces,
                color=Color("#7da6ff"),
                shading="smooth"
            )

            engine.add_visual(mesh)
            return True

        except Exception as e:
            print(f"[StandardRenderer ERROR] {e}")
            return None