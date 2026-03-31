from vispy import scene
from renderers.base import BaseRenderer


class HighlightRenderer(BaseRenderer):
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
            return self.error("Model is None")

        try:
            data = inspect_data.get("data", {})
            data_type = data.get("type")
            payload = data.get("payload", {})
            
            RENDER_MAP = {
                "boundary_edges": self.render_edges,
                "non_manifold_edges": self.render_edges,
                "face_normals": self.render_normals,
                "vertex_normals": self.render_normals,
                "flipped_normals": self.render_normals,
            }

            handler = RENDER_MAP.get(data_type)

            if not handler:
                return self.error(f"Unknown type: {data_type}")
            
            handler(engine, model, payload)

        except Exception as e:
            return self.error(str(e))

    def render_edges(self, engine, model, data):
        try:
            edges = data.get("edges", [])

            if not edges:
                return None
            
            vertices = model.vertices
            lines = []

            for v1, v2 in edges:
                lines.append(vertices[v1])
                lines.append(vertices[v2])
            
            if len(lines) < 2:
                return None

            scene.visuals.Line(
                pos=lines,
                color="red",
                width=1,
                method='gl',
                parent=engine.overlay
            )

            return self.success()

        except Exception as e:
            return self.error(str(e))

    def render_normals(self, engine, model, data):
        try:
            points = data.get("centers") or data.get("vertices", [])
            normals = data.get("normals", [])

            if not points or not normals:
                return None
            
            lines = []

            scale = 0.02

            for p, n in zip(points, normals):
                lines.append(p)
                lines.append(p + n * scale)

            if len(lines) < 2:
                return None

            scene.visuals.Line(
                pos=lines,
                color="red",
                width=1,
                method='gl',
                parent=engine.overlay
            )

            return self.success()

        except Exception as e:
            return self.error(str(e))