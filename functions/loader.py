import os, trimesh


def load_mesh(file_path: str) -> trimesh.Trimesh:
    if not file_path:
        raise ValueError("File path is empty")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        loaded = trimesh.load(file_path, force="scene")

        if isinstance(loaded, trimesh.Trimesh):
            if len(loaded.vertices) == 0:
                raise RuntimeError("Empty mesh")

            mesh = loaded

        elif isinstance(loaded, trimesh.Scene):
            scene = [geometry for geometry in loaded.geometry.values() 
                     if isinstance(geometry, trimesh.Trimesh)]

            if not scene:
                raise RuntimeError("No valid mesh found in scene")

            mesh = trimesh.util.concatenate(scene)

        else:
            raise RuntimeError("Unsupported file format")

        return mesh

    except Exception as error:
        raise RuntimeError(f"Failed to load mesh: {error}")