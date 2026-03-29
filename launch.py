from interfaces.base import BaseInterface
from interfaces.home import HomeInterface
from interfaces.analyze import AnalyzeInterface
from interfaces.render import RenderInterface
from interfaces.inspect import InspectInterface



def main():
    """
    Entry point of Modeloscope UI application.
    """

    try:
        app = BaseInterface()

        app.add_frame("HomeInterface", HomeInterface)
        app.add_frame("AnalyzeInterface", AnalyzeInterface)
        app.add_frame("RenderInterface", RenderInterface)
        app.add_frame("InspectInterface", InspectInterface)

        app.show_frame("HomeInterface")
        app.mainloop()

    except Exception as e:
        print(f"[Application ERROR] {e}")


if __name__ == "__main__":
    main()