class BaseRenderer:
    """
    Defines the standard interface for all renderers.

    Responsibilities:
    - Enforces a consistent render(engine, model) method
    - Serves as the base class for all rendering implementations

    Ensures uniform structure and behavior across all renderers,
    enabling scalability and maintainability.
    """

    def render(self, engine, model):
        raise NotImplementedError("Render method must be implemented")