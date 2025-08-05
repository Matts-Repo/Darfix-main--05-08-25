import sys

import numpy
from silx.gui import qt

from darfix import dtypes
from darfix.tests.utils import createDataset
from orangecontrib.darfix.widgets.noiseremoval import NoiseRemovalWidgetOW


def main(argv=None):

    qapp = qt.QApplication([])

    w = NoiseRemovalWidgetOW()

    # test data
    data = numpy.arange(2500).reshape((1, 50, 50))
    dark_frames = data.copy()
    data[:, 10:30, 10:20] = 2000

    data = numpy.repeat(data, 10, axis=0)

    dataset = createDataset(data=data)
    bg_dataset = createDataset(data=dark_frames)
    w.setDataset(dtypes.Dataset(dataset=dataset, bg_dataset=bg_dataset))
    w.show()

    qapp.exec()


if __name__ == "__main__":
    main(sys.argv)
