import trimesh
import time, os


class ModelLoader:

    def load(self, file_path: str):
        """Handles loading and validation of 3D files."""

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        start = time.perf_counter()

        try:
            loaded = trimesh.load(file_path, force='scene')
        except Exception as e:
            raise RuntimeError(f"Failed to load file: {str(e)}")

        load_time = time.perf_counter() - start

        if isinstance(loaded, trimesh.Trimesh):
            if len(loaded.vertices) == 0:
                raise RuntimeError("model contains no vertices.")
            return loaded, load_time

        if isinstance(loaded, trimesh.Scene):

            mesh_count = len(loaded.geometry)

            if mesh_count == 0:
                raise RuntimeError("Scene contains no model geometry.")

            if mesh_count > 1:
                raise RuntimeError(
                    f"File contains multiple meshes ({mesh_count}). "
                    "3D Metrics currently supports single-model files only."
                )

            model = next(iter(loaded.geometry.values()))

            if not isinstance(model, trimesh.Trimesh):
                raise RuntimeError("Invalid geometry type in scene.")

            return model, load_time

        raise RuntimeError("Unsupported file format or corrupted file.")
