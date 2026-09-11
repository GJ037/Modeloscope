from functions.loader import load_mesh
from inspectors.overlay import heatmap
from inspectors.boundary_edges import inspect_boundary_edges
from inspectors.non_manifold_edges import inspect_non_manifold_edges
from inspectors.face_normals import inspect_face_normals
from inspectors.flipped_normals import inspect_flipped_normals


def load(file_path, mode):
    if not file_path:
        raise ValueError("Invalid file path")

    mesh = load_mesh(file_path)

    match mode:
        case "boundary_edges":
            inspector = inspect_boundary_edges
        case "non_manifold_edges":
            inspector = inspect_non_manifold_edges
        case "face_normals":
            inspector = inspect_face_normals
        case "flipped_normals":
            inspector = inspect_flipped_normals
        case _:
            raise ValueError(f"Unknown mode: {mode}")
        
    return mesh, inspector

def inspect(engine, mesh, inspector):
    engine.clear_all()

    values = inspector(mesh)
    heatmap(engine, mesh, values)

    engine.reset_view()
    engine.set_axis(False)