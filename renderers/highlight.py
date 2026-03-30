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

    def render(self, engine, model, inspect_data):
        if model is None:
            raise ValueError("[HighlightRenderer] Model is None")

        if not inspect_data or inspect_data.get("status") != "success":
            return

        data_type = inspect_data.get("type")
        data = inspect_data.get("data", {})

        if not data_type:
            print("[HighlightRenderer ERROR] Missing type in inspect_data")
            return

        if data_type == "boundary_edges":
            self.render_boundary_edges(engine, model, data)

        elif data_type == "non_manifold_edges":
            self.render_non_manifold_edges(engine, model, data)

        elif data_type == "face_normals":
            self.render_face_normals(engine, model, data)

        elif data_type == "vertex_normals":
            self.render_vertex_normals(engine, model, data)

        elif data_type == "flipped_normals":
            self.render_flipped_normals(engine, model, data)

    def render_boundary_edges(self, engine, model, data):
        edges = data.get("edges", [])

        if not edges:
            return

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

    def render_non_manifold_edges(self, engine, model, data):
        edges = data.get("edges", [])

        if not edges:
            return

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

    def render_face_normals(self, engine, model, data):
        centers = data.get("centers", [])
        normals = data.get("normals", [])

        if not centers:
            return

        lines = []
        scale = 0.025

        for c, n in zip(centers, normals):
            start = c
            end = c + n * scale
            lines.append(start)
            lines.append(end)

        scene.visuals.Line(
            pos=lines,
            color="blue",
            width=1,
            method='gl',
            parent=engine.overlay
        )

    def render_vertex_normals(self, engine, model, data):
        vertices = data.get("vertices", [])
        normals = data.get("normals", [])

        if not vertices:
            return

        lines = []
        scale = 0.025

        for v, n in zip(vertices, normals):
            start = v
            end = v + n * scale
            lines.append(start)
            lines.append(end)

        scene.visuals.Line(
            pos=lines,
            color="green",
            width=1,
            method='gl',
            parent=engine.overlay
        )

    def render_flipped_normals(self, engine, model, data):
        centers = data.get("centers", [])
        normals = data.get("normals", [])

        if not centers:
            return

        lines = []
        scale = 0.025

        for c, n in zip(centers, normals):
            start = c
            end = c + n * scale
            lines.append(start)
            lines.append(end)

        scene.visuals.Line(
            pos=lines,
            color="magenta",
            width=2,
            method='gl',
            parent=engine.overlay
        )