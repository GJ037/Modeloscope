import psutil, os
from analyzers.base import BaseAnalyzer


class PerformanceAnalyzer(BaseAnalyzer):
    """
    Evaluates computational and complexity-related aspects of the mesh.

    Responsibilities:
    - Measures current process memory usage
    - Computes a mesh complexity index (vertices + faces)
    - Calculates triangle processing rate based on load time

    Provides insight into computational cost and scalability of
    processing the mesh.
    """

    def analyze(self, model, context=None):

        if model is None:
            return self.error("Model is None")

        try:
            load_time = context.get("load_time", 0.0) if context else 0.0

            num_faces = int(len(model.faces))
            num_vertices = int(len(model.vertices))

            process = psutil.Process(os.getpid())
            memory_use = round(process.memory_info().rss / (1024 * 1024), 2)

            complexity_index = round((num_vertices + num_faces) / 2.0, 2)

            triangle_rate = (
                num_faces / load_time if load_time > 0 else 0.0
            )

            data = {
                "memory_usage_mb": memory_use,
                "complexity_index": complexity_index,
                "triangles_per_second": round(triangle_rate, 5),
            }

            return self.success(data)

        except Exception as e:
            return self.error(str(e))