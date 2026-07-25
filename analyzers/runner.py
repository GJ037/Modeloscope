from cores.loader import load
from analyzers.topology import analyze_topology
from analyzers.geometry import analyze_geometry
from analyzers.quality import analyze_quality
from analyzers.performance import analyze_performance

ANALYZERS = {
    "topology": analyze_topology,
    "geometry": analyze_geometry,
    "quality": analyze_quality,
    "performance": analyze_performance
}


def analyze(file_path, modes):
    if not file_path:
        raise ValueError("Invalid file path")

    model, meta = load(file_path)
    report, context = {}, {"load_time": meta["load_time_sec"]}

    if "meta" in modes:
        report["meta"] = meta

    for mode in modes:
        if mode in ANALYZERS:
             report[mode] = ANALYZERS[mode](model, context)

    return report