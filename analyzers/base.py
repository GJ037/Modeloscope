class BaseAnalyzer:
    """
    Defines the standard contract for all analyzers in the system.

    Responsibilities:
    - Enforces a consistent analyze(model, context) interface
    - Provides standardized success and error response formats
    - Ensures uniform behavior across all analyzer implementations

    This serves as the foundation for building scalable and maintainable
    analysis modules.
    """

    def analyze(self, model, context=None):
        raise NotImplementedError("Analyzer must implement analyze()")

    def success(self, data: dict):
        return {
            "status": "success",
            "data": data
        }

    def error(self, message: str):
        return {
            "status": "error",
            "message": message,
            "data": {}
        }