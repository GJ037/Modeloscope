from core.loader import ModelLoader
from core.renderer import ModelRenderer
from renderer.standard_renderer import StandardRenderer
from renderer.wireframe_renderer import WireframeRenderer


class RenderRunner:
    """
    Orchestrates rendering pipeline.

    Responsibilities:
        - Load model
        - Initialize viewport
        - Execute selected renderers

    Returns:
        True on success
        None on failure
    """

    def __init__(
        self,
        file_path,
        render_standard=False,
        render_wireframe=False
    ):
        self.file_path = file_path
        self.render_standard = render_standard
        self.render_wireframe = render_wireframe

    def run(self, engine):

        try:
            loader = ModelLoader()
            loaded = loader.load(self.file_path)

            if loaded is None:
                print("[RenderRunner ERROR] Model loading failed.")
                return None

            model, meta = loaded

            for child in list(engine.view.scene.children):
                if child is not engine.view.camera:
                    child.parent = None
                
            if self.render_standard:
                StandardRenderer().render(engine, model)

            if self.render_wireframe:
                WireframeRenderer().render(engine, model)

            engine.fit_camera()

            return True

        except Exception as e:
            print(f"[RenderRunner ERROR] {e}")
            return None