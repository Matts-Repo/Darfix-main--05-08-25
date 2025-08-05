"""Example showing the widget :mod:`~darfix.gui.roiSelectionWidget.ROISelectionWidget`."""

__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "06/12/2019"

import signal
import sys

import numpy
from silx.gui import qt

from darfix import dtypes
from darfix.tests.utils import createDataset
from orangecontrib.darfix.widgets.roiselection import RoiSelectionWidgetOW


def exec_(argv=None):

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

    w = RoiSelectionWidgetOW()

    # test data
    data = numpy.arange(2500).reshape((1, 50, 50))
    data[:, 10:30, 10:20] = 0

    data = numpy.repeat(data, 10, axis=0)

    dataset = createDataset(data=data)

    w.set_dynamic_input("dataset", dtypes.Dataset(dataset=dataset))
    w.handleNewSignals()

    w.show()

    qapp.exec()


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    exec_(sys.argv)
