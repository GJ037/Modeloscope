class BaseModule:
    """
    BaseModule provides a unified response structure for all pipeline modules.

    Responsibilities:
    - Defines standard success() and error() response formats
    - Ensures consistency across analyzers, renderers, and inspectors
    - Acts as the foundational abstraction for all pipeline components

    This class enables uniform communication between modules, runners,
    and UI layers by enforcing a predictable output schema.
    """

    def success(self, data=None, meta=None):
        return {
            "status": "success",
            "data": data or {},
            "meta": meta or {}
        }

    def error(self, message):
        return {
            "status": "error",
            "message": message,
            "data": {}
        }