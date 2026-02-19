from core.loader import ModelLoader
from analyzers.topology_analyzer import TopologyAnalyzer
from analyzers.geometry_analyzer import GeometryAnalyzer
from analyzers.quality_analyzer import QualityAnalyzer
from analyzers.performance_analyzer import PerformanceAnalyzer


class AnalyzerRunner:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def run(self):

        loader = ModelLoader()
        model, load_time = loader.load(self.file_path)

        report = {}

        report["Topology"] = TopologyAnalyzer().analyze(model)
        report["Geometry"] = GeometryAnalyzer().analyze(model)
        report["Quality"] = QualityAnalyzer().analyze(model)
        report["Performance"] = PerformanceAnalyzer().analyze(model, load_time)

        return report
