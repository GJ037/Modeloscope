from core.base import BaseModule


class BaseInspector(BaseModule):
    """
    BaseInspector defines the standard contract for all inspection modules.

    Responsibilities:
    - Enforces the inspect(model, context) interface
    - Detects structural or geometric issues in models
    - Produces structured inspection outputs (type + payload)

    Acts as the foundation for all inspectors, ensuring consistent
    inspection behavior and seamless integration with visualization layers.
    """
    
    def inspect(self, model, context=None):
        raise NotImplementedError("Inspector method must be implemented")