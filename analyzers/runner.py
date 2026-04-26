from cores.loader import ModelLoader
from analyzers.geometry import GeometryAnalyzer
from analyzers.topology import TopologyAnalyzer
from analyzers.quality import QualityAnalyzer
from analyzers.performance import PerformanceAnalyzer

ANALYZERS = {
    "geometry": GeometryAnalyzer,
    "topology": TopologyAnalyzer,
    "quality": QualityAnalyzer,
    "performance": PerformanceAnalyzer
}


class AnalyzerRunner:

    def analyze(self, file_path, modes):
        if not file_path:
            raise ValueError("Invalid file path")

        loader = ModelLoader()
        model, meta = loader.load(file_path)

        report = {}
        context = {
            "load_time": meta["load_time"]
        }

        if "meta" in modes:
            report["meta"] = meta

        for mode in modes:
            if mode in ANALYZERS:
                analyzer = ANALYZERS[mode]()
                report[mode] = analyzer.analyze(model, context)

        return report