from functions.loader import load_mesh
from renderers.flat import render_flat
from renderers.shaded import render_shaded
from renderers.wireframe import render_wireframe
from renderers.pointcloud import render_pointcloud


def load(file_path, mode):
    if not file_path:
        raise ValueError("Invalid file path")

    mesh = load_mesh(file_path)

    match mode:
        case "flat":
            renderer = render_flat
        case "shaded":
            renderer = render_shaded
        case "wireframe":
            renderer = render_wireframe
        case "pointcloud":
            renderer = render_pointcloud
        case _:
            raise ValueError(f"Unknown mode: {mode}")
        
    return mesh, renderer
    
def render(engine, mesh, renderer):
    engine.clear_all()

    renderer(engine, mesh)

    engine.reset_view()
    engine.set_axis(False)