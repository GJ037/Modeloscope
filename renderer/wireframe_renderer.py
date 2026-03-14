from vispy import scene

class WireframeRenderer:
    """
    Renders mesh edges.
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
                width=0.5
            )

            engine.add_visual(lines)
            return True

        except Exception as e:
            print(f"[WireframeRenderer ERROR] {e}")
            return None