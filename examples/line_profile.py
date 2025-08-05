"""Example showing the widget :mod:`~darfix.gui.backgroundSubstractionWidget.BackgroundSubstractionWidget`."""

__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "19/11/2020"


import signal
import sys

from silx.gui import qt

from darfix.gui.lineProfileWidget import LineProfileWidget


def exec_():
    qapp = qt.QApplication([])

    # add connection with ctrl + c signal
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler
    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    w = LineProfileWidget()
    w.show()

    qapp.exec()


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    exec_()
