from interface.base_interface import BaseInterface
from interface.home_interface import HomeInterface
from interface.analyze_interface import AnalyzeInterface


def main():
    app = BaseInterface()

    app.add_frame("HomeInterface", HomeInterface)
    app.add_frame("AnalyzeInterface", AnalyzeInterface)

    app.show_frame("HomeInterface")

    app.mainloop()


if __name__ == "__main__":
    main()