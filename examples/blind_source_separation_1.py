"""Example showing the widget :mod:`~darfix.gui.blindSourceSeparation.BlindSourceSeparation`."""

__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "28/04/2020"


import logging
import signal
import sys

from silx.gui import qt

from darfix import dtypes
from darfix.tests.decomposition.utils import sampler
from darfix.tests.utils import createDataset
from orangecontrib.darfix.widgets.blindsourceseparation import (
    BlindSourceSeparationWidgetOW,
)

logging.basicConfig(filename="example.log", level=logging.INFO)


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

    w = BlindSourceSeparationWidgetOW()
    resources = ["circle", "star", "pentagon", "square"]
    num_images = 100
    means = [15, 30, 45, 60]
    sample = sampler(resources, means)

    X = [sample(i) for i in range(num_images)]

    dataset = dtypes.Dataset(createDataset(data=X))
    w.set_dynamic_input("dataset", dataset)
    w.setDataset(dataset)
    w.show()

    qapp.exec()


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    exec_(sys.argv)
