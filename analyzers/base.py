from core.base import BaseModule


class BaseAnalyzer(BaseModule):
    """
    BaseAnalyzer defines the standard contract for all analysis modules.

    Responsibilities:
    - Enforces the analyze(model, context) interface
    - Processes models to extract metrics and insights
    - Returns structured analysis results using BaseModule utilities

    Acts as the foundation for all analyzers, ensuring consistent
    behavior, output format, and integration within the analysis pipeline.
    """
    
    def analyze(self, model, context=None):
        raise NotImplementedError("Analyzer must implement analyze()")