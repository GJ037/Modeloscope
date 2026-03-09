from vispy import scene

class WireframeRenderer:
    """
    Renders mesh in wireframe mode.
    """

    def render(self, engine, model):

        if model is None:
            print("[WireframeRenderer ERROR] model is None")
            return None

        try:
            edges = model.edges_unique

            lines = scene.visuals.Line(
                pos=model.vertices[edges].reshape(-1, 3),
                color="white",
                connect="segments",
                width=1.0
            )

            engine.view.add(lines)
            return True

        except Exception as e:
            print(f"[WireframeRenderer ERROR] {e}")
            return None