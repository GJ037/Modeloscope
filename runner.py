from interface.base_interface import BaseInterface
from interface.home_interface import HomeInterface
from interface.analyze_interface import AnalyzeInterface
from interface.render_interface import RenderInterface


def main():
    """
    Entry point of Modeloscope UI application.
    """

    try:
        app = BaseInterface()

        app.add_frame("HomeInterface", HomeInterface)
        app.add_frame("AnalyzeInterface", AnalyzeInterface)
        app.add_frame("RenderInterface", RenderInterface)

        app.show_frame("HomeInterface")
        app.mainloop()

    except Exception as e:
        print(f"[Application ERROR] {e}")


if __name__ == "__main__":
    main()