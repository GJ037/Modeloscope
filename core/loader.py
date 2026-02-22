import trimesh
import time
import os


class ModelLoader:

    def load(self, file_path: str):

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)

        start = time.perf_counter()

        try:
            loaded = trimesh.load(file_path, force='scene')
        except Exception as e:
            raise RuntimeError(f"Failed to load file: {str(e)}")

        load_time = time.perf_counter() - start

        # Single mesh
        if isinstance(loaded, trimesh.Trimesh):

            if len(loaded.vertices) == 0:
                raise RuntimeError("Model contains no vertices.")

            geometry_count = 1
            model = loaded

        # Scene
        elif isinstance(loaded, trimesh.Scene):

            geometry_count = len(loaded.geometry)

            if geometry_count == 0:
                raise RuntimeError("Scene contains no model geometry.")

            meshes = [
                g for g in loaded.geometry.values()
                if isinstance(g, trimesh.Trimesh)
            ]

            if len(meshes) == 0:
                raise RuntimeError("No valid mesh geometry found in scene.")

            model = trimesh.util.concatenate(meshes)

        else:
            raise RuntimeError("Unsupported file format or corrupted file.")

        meta = {
            "file_name": file_name,
            "file_size_mb": round(file_size / (1024 * 1024), 3),
            "geometry_count": geometry_count,
            "load_time": round(load_time, 5)
        }

        return model, meta
