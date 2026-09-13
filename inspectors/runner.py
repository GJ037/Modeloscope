from functions.loader import load_mesh
from inspectors.heatmap import render_heatmap
from inspectors.duplicate_vertices import inspect_duplicate_vertices
from inspectors.non_manifold_edges import inspect_non_manifold_edges
from inspectors.sharp_edges import inspect_sharp_edges
from inspectors.degenerate_faces import inspect_degenerate_faces
from inspectors.flipped_normals import inspect_flipped_normals


def load(file_path, mode):
    if not file_path:
        raise ValueError("Invalid file path")

    mesh = load_mesh(file_path)

    match mode:
        case "duplicate_vertices":
            inspector = inspect_duplicate_vertices
        case "non_manifold_edges":
            inspector = inspect_non_manifold_edges
        case "sharp_edges":
            inspector = inspect_sharp_edges
        case "degenerate_faces":
            inspector = inspect_degenerate_faces
        case "flipped_normals":
            inspector = inspect_flipped_normals
        case _:
            raise ValueError(f"Unknown mode: {mode}")
        
    return mesh, inspector

def inspect(engine, mesh, inspector):
    engine.clear_all()

    values = inspector(mesh)
    render_heatmap(engine, mesh, values)

    engine.reset_view()
    engine.set_axis(False)