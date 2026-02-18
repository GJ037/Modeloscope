import psutil, os

class PerformanceAnalyzer:

    def analyze(self, mesh, load_time=0.0):

        num_faces = int(len(mesh.faces))
        num_vertices = int(len(mesh.vertices))

        try:
            process = psutil.Process(os.getpid())
            memory_use = round(process.memory_info().rss / (1024 * 1024), 2)
        except Exception:
            memory_use = 0.0

        complexity_index = round((num_vertices + num_faces) / 2.0, 2)

        triangle_rate = round(
            num_faces / (load_time * 1000.0), 5
        ) if load_time > 0 else 0.0

        return {
            "load_time": round(float(load_time), 5),
            "memory_usage_mb": memory_use,
            "complexity_index": complexity_index,
            "triangle_rate": triangle_rate
        }
