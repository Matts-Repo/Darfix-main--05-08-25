import argparse
import sys

import numpy
from silx.gui import qt

from darfix import dtypes
from darfix.math import bivariate_gaussian
from darfix.tests.utils import create_3motors_dataset
from darfix.tests.utils import createHDF5Dataset1D
from darfix.tests.utils import createHDF5Dataset2D
from orangecontrib.darfix.widgets.rockingcurves import RockingCurvesWidgetOW


def main(argv=None):
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser()
    parser.add_argument("--dims", default=2, type=int)

    options = parser.parse_args(argv[1:])

    qapp = qt.QApplication([])

    w = RockingCurvesWidgetOW()

    data = numpy.empty((20, 200, 200))
    x = numpy.arange(200)

    sigmas = [*range(1, 11), *range(10, 0, -1)]

    for i in range(0, 20):
        sigma = sigmas[i] * 5
        data[i] = bivariate_gaussian(
            numpy.meshgrid(x, x), 100, 100, sigma, sigma, amplitude=100
        )

    if options.dims == 3:
        dataset = create_3motors_dataset("", backend="hdf5")
    elif options.dims == 2:
        dataset = createHDF5Dataset2D(data=data.reshape((5, 4, 200, 200)))
    elif options.dims == 1:
        dataset = createHDF5Dataset1D(data=data)
    else:
        raise ValueError("--dims must be 1, 2 or 3")

    dataset.find_dimensions()
    reshaped_dataset = dtypes.Dataset(dataset=dataset.reshape_data())
    w.set_dynamic_input("dataset", reshaped_dataset)
    w.setDataset(reshaped_dataset)
    w.show()

    qapp.exec()


if __name__ == "__main__":
    main(sys.argv)
