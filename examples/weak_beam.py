import argparse
import signal
import sys

import numpy
from silx.gui import qt

from darfix import dtypes
from darfix.tests.utils import createRandomEDFDataset
from darfix.tests.utils import createRandomHDF5Dataset
from orangecontrib.darfix.widgets.weakbeam import WeakBeamWidgetOW


def exec_(argv=None):
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--edf-dataset",
        help="Create the example from an EDF random dataset. Else from an HDF5 one",
        default=False,
        action="store_true",
    )

    options = parser.parse_args(argv[1:])

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

    w = WeakBeamWidgetOW()

    # test data
    data = numpy.arange(2500).reshape((1, 50, 50))
    data[:, 10:30, 10:20] = 0

    data = numpy.repeat(data, 10, axis=0)

    if options.edf_dataset:
        dataset = createRandomEDFDataset(
            dims=(100, 100), nb_data_files=5, header=True, num_dims=1
        )
    else:
        dataset = createRandomHDF5Dataset(
            dims=(100, 100),
            nb_data_frames=5,
            metadata=True,
            num_dims=1,
        )
    dataset.find_dimensions()
    reshaped_dataset = dataset.reshape_data()
    ow_dataset = dtypes.Dataset(dataset=reshaped_dataset)

    w.setDataset(ow_dataset)
    w.set_dynamic_input("dataset", ow_dataset)
    w.show()

    qapp.exec()


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    exec_(sys.argv)
