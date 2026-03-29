class BaseInspector:
    """
    Base class for all inspectors.
    """

    def inspect(self, model):
        """
        Takes model → returns structured inspection data.

        Must be implemented by subclasses.
        """
        raise NotImplementedError("Inspector must implement inspect()")