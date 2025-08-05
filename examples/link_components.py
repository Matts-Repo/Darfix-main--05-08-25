"""Example showing the widget :mod:`~darfix.gui.linkComponentsWidget.LinkComponentsWidget`."""

__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "13/01/2020"


from silx.gui import qt

from darfix.gui.linkComponentsWidget import LinkComponentsWidget


def exec_():
    qapp = qt.QApplication([])

    w = LinkComponentsWidget()
    w.show()

    qapp.exec()


if __name__ == "__main__":
    exec_()
