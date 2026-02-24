import trimesh, time, os

class ModelLoader:
    """
    Loads 3D model files and prepares them for analysis.

    Handles:
        - File existence validation
        - Scene vs single mesh handling
        - Mesh concatenation (for multi-geometry scenes)
        - Metadata extraction (file size, geometry count, load time)

    Returns:
        model, meta dictionary on success
        None on failure
    """

    def load(self, file_path: str):

        if not file_path:
            print("[ModelLoader ERROR] file_path is empty")
            return None

        try:
            if not os.path.exists(file_path):
                print(f"[ModelLoader ERROR] File not found: {file_path}")
                return None

            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)

            start = time.perf_counter()
            loaded = trimesh.load(file_path, force='scene')
            load_time = time.perf_counter() - start

            # Single mesh
            if isinstance(loaded, trimesh.Trimesh):

                if len(loaded.vertices) == 0:
                    print("[ModelLoader ERROR] Model contains no vertices.")
                    return None

                geometry_count = 1
                model = loaded

            # Scene
            elif isinstance(loaded, trimesh.Scene):

                geometry_count = len(loaded.geometry)

                if geometry_count == 0:
                    print("[ModelLoader ERROR] Scene contains no model geometry.")
                    return None

                meshes = [
                    g for g in loaded.geometry.values()
                    if isinstance(g, trimesh.Trimesh)
                ]

                if len(meshes) == 0:
                    print("[ModelLoader ERROR] No valid mesh geometry found in scene.")
                    return None

                model = trimesh.util.concatenate(meshes)

            else:
                print("[ModelLoader ERROR] Unsupported file format or corrupted file.")
                return None

            meta = {
                "file_name": file_name,
                "file_size_mb": round(file_size / (1024 * 1024), 3),
                "geometry_count": geometry_count,
                "load_time": round(load_time, 5)
            }

            return model, meta

        except Exception as e:
            print(f"[ModelLoader ERROR] {e}")
            return None