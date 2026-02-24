from core.loader import ModelLoader
from analyzers.topology_analyzer import TopologyAnalyzer
from analyzers.geometry_analyzer import GeometryAnalyzer
from analyzers.quality_analyzer import QualityAnalyzer
from analyzers.performance_analyzer import PerformanceAnalyzer


class AnalyzerRunner:
    """
    Orchestrates the full analysis pipeline.

    Responsibilities:
        - Load model using ModelLoader
        - Execute all analyzers
        - Collect results into a structured report

    Returns:
        Dictionary report on success
        None on failure
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def run(self):

        try:
            loader = ModelLoader()
            loaded = loader.load(self.file_path)

            if loaded is None:
                print("[AnalyzerRunner ERROR] Model loading failed.")
                return None

            model, meta = loaded

            report = {}
            report["meta"] = meta
            report["Topology"] = TopologyAnalyzer().analyze(model)
            report["Geometry"] = GeometryAnalyzer().analyze(model)
            report["Quality"] = QualityAnalyzer().analyze(model)
            report["Performance"] = PerformanceAnalyzer().analyze(model, meta["load_time"])

            return report

        except Exception as e:
            print(f"[AnalyzerRunner ERROR] {e}")
            return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python analyze.py <model_file>")
        sys.exit(1)

    path = sys.argv[1]

    try:
        runner = AnalyzerRunner(path)
        report = runner.run()

        for section, data in report.items():
            print(f"\n--- {section} ---")
            for key, value in data.items():
                print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")
