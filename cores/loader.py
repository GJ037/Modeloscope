import os, time, trimesh


class ModelLoader:

    def load(self, file_path: str):
        if not file_path:
            raise ValueError("File path is empty")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)

            start = time.perf_counter()
            loaded = trimesh.load(file_path, force="scene")
            load_time = time.perf_counter() - start

            if isinstance(loaded, trimesh.Trimesh):

                if len(loaded.vertices) == 0:
                    raise RuntimeError("Empty model")

                model = loaded
                geometry_count = 1

            elif isinstance(loaded, trimesh.Scene):

                meshes = [
                    g for g in loaded.geometry.values()
                    if isinstance(g, trimesh.Trimesh)
                ]

                if not meshes:
                    raise RuntimeError("No valid mesh found in scene")

                model = trimesh.util.concatenate(meshes)
                geometry_count = len(meshes)

            else:
                raise RuntimeError("Unsupported file format")

            meta = {
                "file_name": file_name,
                "file_size_mb": round(file_size / (1024 * 1024), 3),
                "geometry_count": geometry_count,
                "load_time": round(load_time, 5),
            }

            return model, meta

        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")