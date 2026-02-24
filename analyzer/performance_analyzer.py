import psutil, os

class PerformanceAnalyzer:
    """
    Evaluates computational and complexity-related metrics of the 3D mesh model.

    Calculates:
        - Load time (provided externally)
        - Current process memory usage
        - Model complexity index (faces + vertices)
        - Triangle processing rate
    """

    def analyze(self, model, load_time=0.0):

        if model is None:
            print("[PerformanceAnalyzer ERROR] model is None")
            return None

        try:
            num_faces = int(len(model.faces))
            num_vertices = int(len(model.vertices))

            process = psutil.Process(os.getpid())
            memory_use = round(process.memory_info().rss / (1024 * 1024), 2)

            complexity_index = round((num_vertices + num_faces) / 2.0, 2)
            triangle_rate = round(num_faces / (load_time * 1000.0), 5) if load_time > 0 else 0.0

            return {
                "memory_usage_mb": memory_use,
                "complexity_index": complexity_index,
                "triangle_rate": triangle_rate
            }

        except Exception as e:
            print(f"[PerformanceAnalyzer ERROR] {e}")
            return None
        