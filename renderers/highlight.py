from vispy import scene
from vispy.color import Color


class HighlightRenderer:
    """
    Renders inspection overlays on top of the base mesh.

    Responsibilities:
    - Visualizes inspection results using line primitives
    - Supports multiple inspection types (edges, normals, etc.)
    - Draws overlays without modifying the base mesh

    Acts as the visualization layer for inspection results,
    separating analysis logic from rendering logic.
    """

    def render(self, engine, model, inspect_data, context=None):
        if model is None:
            print("[HighlightRenderer ERROR] Model is None")
            return

        try:
            data = inspect_data.get("data", {})

            data_type = data.get("type")
            payload = data.get("payload", {})

            RENDER_MAP = {
                "boundary_edges": self.render_boundary_edges,
                "non_manifold_edges": self.render_non_manifold_edges,
                "face_normals": self.render_face_normals,
                "vertex_normals": self.render_vertex_normals,
                "flipped_normals": self.render_flipped_normals,
            }

            handler = RENDER_MAP.get(data_type)
            handler(engine, model, payload)

        except Exception as e:
            return self.error(str(e))

    def render_boundary_edges(self, engine, model, data):
        try:
            edges = data.get("edges", [])
            vertices = model.vertices
            lines = []

            for v1, v2 in edges:
                lines.append(vertices[v1])
                lines.append(vertices[v2])

            scene.visuals.Line(
                pos=lines,
                color=Color("red"),
                width=2,
                method='gl',
                parent=engine.overlay
            )

        except Exception as e:
            return self.error(str(e))

    def render_non_manifold_edges(self, engine, model, data):
        try:
            edges = data.get("edges", [])
            vertices = model.vertices
            lines = []

            for v1, v2 in edges:
                lines.append(vertices[v1])
                lines.append(vertices[v2])

            scene.visuals.Line(
                pos=lines,
                color=Color("yellow"),
                width=3,
                method='gl',
                parent=engine.overlay
            )

        except Exception as e:
            return self.error(str(e))

    def render_face_normals(self, engine, model, data):
        try:
            centers = data.get("centers", [])
            normals = data.get("normals", [])

            lines = []
            scale = 0.02

            for c, n in zip(centers, normals):
                lines.append(c)
                lines.append(c + n * scale)

            scene.visuals.Line(
                pos=lines,
                color="blue",
                width=1,
                method='gl',
                parent=engine.overlay
            )

        except Exception as e:
            return self.error(str(e))

    def render_vertex_normals(self, engine, model, data):
        try:
            vertices = data.get("vertices", [])
            normals = data.get("normals", [])

            lines = []
            scale = 0.02

            for v, n in zip(vertices, normals):
                lines.append(v)
                lines.append(v + n * scale)

            scene.visuals.Line(
                pos=lines,
                color="green",
                width=1,
                method='gl',
                parent=engine.overlay
            )

        except Exception as e:
            return self.error(str(e))

    def render_flipped_normals(self, engine, model, data):
        try:
            centers = data.get("centers", [])
            normals = data.get("normals", [])

            lines = []
            scale = 0.02

            for c, n in zip(centers, normals):
                lines.append(c)
                lines.append(c + n * scale)

            scene.visuals.Line(
                pos=lines,
                color="magenta",
                width=2,
                method='gl',
                parent=engine.overlay
            )
            
        except Exception as e:
            return self.error(str(e))