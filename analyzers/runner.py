from core.loader import ModelLoader
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
    """
    Orchestrates the complete analysis pipeline.

    Responsibilities:
    - Loads model using ModelLoader
    - Executes selected analyzers based on requested modes
    - Passes shared context (e.g., load time) to analyzers
    - Aggregates results into a structured report

    Acts as the central controller coordinating all analysis operations.
    """

    def analyze(self, file_path, modes):
        if not file_path:
            return {"status": "error", "message": "Invalid file path"}
        
        loader = ModelLoader()
        result = loader.load(file_path)

        if result["status"] != "success":
            return result

        model = result["model"]
        meta = result["meta"]

        report = {}

        if "meta" in modes:
            report["meta"] = meta

        context = {
            "load_time": meta["load_time"]
        }

        for mode in modes:
            if mode in ANALYZERS:
                analyzer = ANALYZERS[mode]()
                report[mode] = analyzer.analyze(model, context)

        return {
            "status": "success",
            "report": report
        }