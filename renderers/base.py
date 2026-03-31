from core.base import BaseModule


class BaseRenderer(BaseModule):
    """
    BaseRenderer defines the standard interface for all rendering modules.

    Responsibilities:
    - Enforces the render(engine, model, context) interface
    - Handles visualization of models using the rendering engine
    - Provides a consistent structure for rendering operations

    Acts as the base for all renderers, ensuring uniform interaction
    with the rendering engine and consistent execution flow.
    """
    
    def render(self, engine, model, context=None):
        raise NotImplementedError("Render method must be implemented")