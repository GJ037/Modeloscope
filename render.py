from core.loader import ModelLoader
from core.renderer import ModelRenderer
from renderer.standard_renderer import StandardRenderer
from renderer.wireframe_renderer import WireframeRenderer
from renderer.pointcloud_renderer import PointCloudRenderer


class RenderRunner:
    """
    Orchestrates rendering pipeline.

    Responsibilities:
        - Own the viewport (ModelRenderer)
        - Load model
        - Execute selected renderers
    """

    def __init__(self, parent):
        self.engine = ModelRenderer()

        if not self.engine.initialize(parent):
            raise RuntimeError("[RenderRunner ERROR] Engine initialization failed.")

    def render(self, file_path, mode):
        try:
            loader = ModelLoader()
            loaded = loader.load(file_path)

            if loaded is None:
                print("[RenderRunner ERROR] Model loading failed.")
                return None

            model, meta = loaded
            
            self.engine.clear()

            if mode == "standard":
                StandardRenderer().render(self.engine, model)

            elif mode == "wireframe":
                WireframeRenderer().render(self.engine, model)

            elif mode == "pointcloud":
                PointCloudRenderer().render(self.engine, model)

            else:
                print(f"[RenderRunner ERROR] Unknown render mode: {mode}")
                return None

            self.engine.fit_camera()
            
            return True

        except Exception as e:
            print(f"[RenderRunner ERROR] {e}")
            return None