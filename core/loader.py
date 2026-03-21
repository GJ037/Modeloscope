import trimesh, time, os


class ModelLoader:
    """
    Handles loading and preprocessing of 3D models.

    Responsibilities:
    - Validates file existence and input path
    - Supports both single mesh and multi-geometry scenes
    - Merges scene geometries into a single mesh when required
    - Extracts metadata (file name, size, geometry count, load time)

    Acts as the entry point for bringing model data into the system
    in a consistent and usable format.
    """

    def load(self, file_path: str):

        if not file_path:
            return {
                "status": "error",
                "message": "File path is empty"
            }

        try:
            if not os.path.exists(file_path):
                return {
                    "status": "error",
                    "message": f"File not found: {file_path}"
                }

            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)

            start = time.perf_counter()
            loaded = trimesh.load(file_path, force='scene')
            load_time = time.perf_counter() - start

            if isinstance(loaded, trimesh.Trimesh):

                if len(loaded.vertices) == 0:
                    return {"status": "error", "message": "Empty model"}

                geometry_count = 1
                model = loaded

            elif isinstance(loaded, trimesh.Scene):

                meshes = [
                    g for g in loaded.geometry.values()
                    if isinstance(g, trimesh.Trimesh)
                ]

                if not meshes:
                    return {"status": "error", "message": "No valid mesh"}

                model = trimesh.util.concatenate(meshes)
                geometry_count = len(meshes)

            else:
                return {"status": "error", "message": "Unsupported format"}

            meta = {
                "file_name": file_name,
                "file_size_mb": round(file_size / (1024 * 1024), 3),
                "geometry_count": geometry_count,
                "load_time": round(load_time, 5),
            }

            return {
                "status": "success",
                "model": model,
                "meta": meta
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }