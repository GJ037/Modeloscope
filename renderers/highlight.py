from vispy import scene
from vispy.color import Color


class HighlightRenderer:
    """
    Renders inspection overlays on top of existing scene.
    """

    def render(self, engine, model, inspect_data):
        if model is None:
            raise ValueError("[HighlightRenderer] Model is None")

        if inspect_data is None:
            return

        data_type = inspect_data.get("type")

        if not data_type:
            print("[HighlightRenderer ERROR] Missing type in inspect_data")
            return

        if data_type == "boundary_edges":
            self._render_boundary_edges(engine, model, inspect_data)
        
        elif data_type == "non_manifold_edges":
            self._render_non_manifold_edges(engine, model, inspect_data)

        elif data_type == "face_normals":
            self._render_face_normals(engine, model, inspect_data)

        elif data_type == "vertex_normals":
            self._render_vertex_normals(engine, model, inspect_data)

        elif data_type == "flipped_normals":
            self._render_flipped_normals(engine, model, inspect_data)

    # -----------------------------

    def _render_boundary_edges(self, engine, model, inspect_data):
        edges = inspect_data.get("edges", [])

        if not edges:
            print("[HighlightRenderer] No boundary edges found")
            return

        vertices = model.vertices

        lines = []

        for v1, v2 in edges:
            lines.append(vertices[v1])
            lines.append(vertices[v2])

        line_visual = scene.visuals.Line(
            pos=lines,
            color=Color("red"),
            width=2,
            method='gl',
            parent=engine.overlay
        )

    def _render_non_manifold_edges(self, engine, model, inspect_data):
        edges = inspect_data.get("edges", [])

        if not edges:
            print("[HighlightRenderer] No non-manifold edges found")
            return

        vertices = model.vertices
        lines = []

        for v1, v2 in edges:
            lines.append(vertices[v1])
            lines.append(vertices[v2])

        scene.visuals.Line(
            pos=lines,
            color=Color("yellow"),   # 🔥 different color
            width=3,
            method='gl',
            parent=engine.overlay
        )

    def _render_face_normals(self, engine, model, inspect_data):
        centers = inspect_data.get("centers", [])
        normals = inspect_data.get("normals", [])

        if not centers:
            print("[HighlightRenderer] No face normals found")
            return

        lines = []

        scale = 0.05  # 🔥 adjust based on model size

        for c, n in zip(centers, normals):
            start = c
            end = c + n * scale

            lines.append(start)
            lines.append(end)

        scene.visuals.Line(
            pos=lines,
            color="blue",   # 🔵 normals color
            width=1,
            method='gl',
            parent=engine.overlay
        )
        print(f"[HighlightRenderer] Rendering {len(centers)} normals")

    def _render_vertex_normals(self, engine, model, inspect_data):
        vertices = inspect_data.get("vertices", [])
        normals = inspect_data.get("normals", [])

        if not vertices:
            print("[HighlightRenderer] No vertex normals found")
            return

        print(f"[HighlightRenderer] Rendering {len(vertices)} vertex normals")

        lines = []

        scale = 0.05  # adjust if needed

        for v, n in zip(vertices, normals):
            start = v
            end = v + n * scale

            lines.append(start)
            lines.append(end)

        scene.visuals.Line(
            pos=lines,
            color="green",   # 🟢 vertex normals
            width=1,
            method='gl',
            parent=engine.overlay
        )

    def _render_flipped_normals(self, engine, model, inspect_data):
        centers = inspect_data.get("centers", [])
        normals = inspect_data.get("normals", [])

        if not centers:
            print("[HighlightRenderer] No flipped normals found")
            return

        print(f"[HighlightRenderer] Rendering {len(centers)} flipped normals")

        lines = []

        scale = 0.1  # slightly larger for visibility

        for c, n in zip(centers, normals):
            start = c
            end = c + n * scale

            lines.append(start)
            lines.append(end)

        scene.visuals.Line(
            pos=lines,
            color="magenta",   # 🔥 flipped = magenta
            width=2,
            method='gl',
            parent=engine.overlay
        )