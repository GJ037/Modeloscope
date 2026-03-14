from core.loader import ModelLoader
from analyzer.topology_analyzer import TopologyAnalyzer
from analyzer.geometry_analyzer import GeometryAnalyzer
from analyzer.quality_analyzer import QualityAnalyzer
from analyzer.performance_analyzer import PerformanceAnalyzer

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

    def __init__(self, file_path, modes):
        self.file_path = file_path
        self.modes = modes

    def run(self):

        try:
            loader = ModelLoader()
            loaded = loader.load(self.file_path)

            if loaded is None:
                print("[AnalyzerRunner ERROR] Model loading failed.")
                return None

            model, meta = loaded

            report = {}
            
            if "meta" in self.modes:
                report["Meta"] = meta

            if "topology" in self.modes:
                report["Topology"] = TopologyAnalyzer().analyze(model)

            if "geometry" in self.modes:
                report["Geometry"] = GeometryAnalyzer().analyze(model)

            if "quality" in self.modes:
                report["Quality"] = QualityAnalyzer().analyze(model)

            if "performance" in self.modes:
                report["Performance"] = PerformanceAnalyzer().analyze(model, meta["load_time"])

            return report

        except Exception as e:
            print(f"[AnalyzerRunner ERROR] {e}")
            return None
