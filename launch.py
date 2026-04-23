from interfaces.controller import Controller
from interfaces.home import HomeInterface
from interfaces.analyze import AnalyzeInterface
from interfaces.render import RenderInterface
from interfaces.inspect import InspectInterface


def main():
    app = Controller()

    app.add_frame("HomeInterface", HomeInterface)
    app.add_frame("AnalyzeInterface", AnalyzeInterface)
    app.add_frame("RenderInterface", RenderInterface)
    app.add_frame("InspectInterface", InspectInterface)

    app.show_frame("HomeInterface")
    app.mainloop()


if __name__ == "__main__":
    main()