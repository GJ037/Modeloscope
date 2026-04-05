import os, psutil


class PerformanceAnalyzer:

    def analyze(self, model, context=None):
        if model is None:
            raise ValueError("Model is None")

        load_time = context.get("load_time", 0.0) if context else 0.0

        num_faces = int(len(model.faces))
        num_vertices = int(len(model.vertices))

        process = psutil.Process(os.getpid())
        memory_use = round(process.memory_info().rss / (1024 * 1024), 2)

        complexity_index = round((num_vertices + num_faces) / 2.0, 2)

        triangle_rate = (
            num_faces / load_time if load_time > 0 else 0.0
        )

        return {
            "memory_usage_mb": memory_use,
            "complexity_index": complexity_index,
            "triangles_per_second": round(triangle_rate, 5),
        }