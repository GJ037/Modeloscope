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

    def __init__(
        self,
        file_path,
        run_meta=True,
        run_geometry=True,
        run_topology=True,
        run_quality=True,
        run_performance=True
    ):
        self.file_path = file_path
        self.run_meta = run_meta
        self.run_geometry = run_geometry
        self.run_topology = run_topology
        self.run_quality = run_quality
        self.run_performance = run_performance

    def run(self):

        try:
            loader = ModelLoader()
            loaded = loader.load(self.file_path)

            if loaded is None:
                print("[AnalyzerRunner ERROR] Model loading failed.")
                return None

            model, meta = loaded

            report = {}
            
            if self.run_meta:
                report["meta"] = meta

            if self.run_topology:
                report["Topology"] = TopologyAnalyzer().analyze(model)

            if self.run_geometry:
                report["Geometry"] = GeometryAnalyzer().analyze(model)

            if self.run_quality:
                report["Quality"] = QualityAnalyzer().analyze(model)

            if self.run_performance:
                report["Performance"] = PerformanceAnalyzer().analyze(model, meta["load_time"])

            return report

        except Exception as e:
            print(f"[AnalyzerRunner ERROR] {e}")
            return None
