"""Example showing the widget :mod:`~darfix.gui.backgroundSubstractionWidget.BackgroundSubstractionWidget`."""

__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "11/05/2020"


import sys

import numpy
from silx.gui import qt

from darfix import dtypes
from darfix.tests.utils import createDataset
from orangecontrib.darfix.widgets.datapartition import DataPartitionWidgetOW


def exec_(argv=None):

    qapp = qt.QApplication([])

    w = DataPartitionWidgetOW()

    # test data
    data = numpy.zeros((10, 50, 50))
    data[3:7, 10:30, 10:20] = 2000

    dataset = createDataset(data=data)
    w.setDataset(dataset=dtypes.Dataset(dataset))
    w.show()

    qapp.exec()


if __name__ == "__main__":
    exec_(sys.argv)
