class BaseInspector:
    """
    Abstract base class for all inspection modules.

    Responsibilities:
    - Defines the contract for all inspectors
    - Ensures consistent input/output structure across implementations

    Provides a standardized interface for implementing inspection logic
    while keeping individual inspectors modular and interchangeable.
    """

    def inspect(self, model):
        raise NotImplementedError("Inspector method must be implemented")