import argparse
import sys

import numpy
from silx.gui import qt

from darfix.dtypes import Dataset
from darfix.tests.utils import create_3motors_dataset
from darfix.tests.utils import createHDF5Dataset1D
from darfix.tests.utils import createHDF5Dataset2D
from orangecontrib.darfix.widgets.shiftcorrection import ShiftCorrectionWidgetOW

USE_3D_DATASET = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dims", default=2, type=int)
    options = parser.parse_args(sys.argv[1:])

    qapp = qt.QApplication([])

    w = ShiftCorrectionWidgetOW()

    if options.dims == 3:
        dataset = create_3motors_dataset("", backend="hdf5")
    elif options.dims == 2:
        data = numpy.zeros(150000).reshape((10, 5, 50, 60))
        for i in range(10):
            data[i, :, 3 * i + 10 : 3 * i + 20, 2 * i + 10 : 2 * i + 20] = 1
        dataset = createHDF5Dataset2D(data)
    elif options.dims == 1:
        data = numpy.zeros(30000).reshape((10, 50, 60))
        for i in range(10):
            data[i, 3 * i + 10 : 3 * i + 20, 2 * i + 10 : 2 * i + 20] = 1
        dataset = createHDF5Dataset1D(data=data)
    else:
        raise ValueError("--dims must be 1, 2 or 3")

    dataset.find_dimensions()
    w.setDataset(Dataset(dataset))
    w.show()

    qapp.exec()
