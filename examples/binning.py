import signal
import sys

import numpy
from silx.gui import qt

from darfix.dtypes import Dataset
from darfix.tests.utils import createDataset
from orangecontrib.darfix.widgets.binning import BinningWidgetOW


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

    w = BinningWidgetOW()

    # test data
    data = numpy.arange(2500).reshape((1, 50, 50))
    data[:, 10:30, 10:20] = 0

    data = numpy.repeat(data, 10, axis=0)

    dataset = Dataset(createDataset(data=data))
    w.setDataset(dataset)
    w.set_dynamic_input("dataset", dataset)

    w.show()
    qapp.exec()


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    exec_(sys.argv)
