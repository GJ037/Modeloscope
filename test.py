import tkinter as tk

from renderers.runner import RenderRunner
from inspectors.runner import InspectRunner
from renderers.highlight import HighlightRenderer


def main():
    root = tk.Tk()
    root.title("Inspect Test")
    root.geometry("800x600")

    # container frame
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    # initialize render system
    runner = RenderRunner(frame)

    # test file
    file_path = "vase.ply"   # change if needed

    try:
        # 🔹 Step 1: Render normally (this loads model internally)
        runner.render(file_path, "standard")

        # 🔹 Step 2: Get model from runner
        model = runner.model   # 🔥 IMPORTANT: your runner must store this

        if model is None:
            print("[TEST] Model not available from RenderRunner")
            return

        # 🔹 Step 3: Run inspector
        inspect_runner = InspectRunner()
        inspect_data = inspect_runner.run(model, "flipped_normals")

        print("[DEBUG] Inspect Type:", inspect_data.get("type"))

        if inspect_data["type"] in ["boundary_edges", "non_manifold_edges"]:
            print("[DEBUG] Edge Count:", len(inspect_data.get("edges", [])))

        elif inspect_data["type"] == "face_normals":
            print("[DEBUG] Normals Count:", len(inspect_data.get("normals", [])))

        # 🔹 Step 4: Render overlay
        highlight_renderer = HighlightRenderer()

        runner.engine.clear_overlay()
        highlight_renderer.render(runner.engine, model, inspect_data)

        print("[DEBUG FULL DATA]:", inspect_data.keys())

    except Exception as e:
        print("[TEST ERROR]", e)

    root.mainloop()


if __name__ == "__main__":
    main()