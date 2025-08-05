"""Example showing the widget :mod:`~darfix.gui.blindSourceSeparation.BlindSourceSeparation`."""

__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "08/04/2020"

import argparse
import signal
import sys

from silx.gui import qt

from darfix.dtypes import Dataset
from darfix.gui.dimensionsWidget import DimensionWidget
from darfix.tests.utils import createRandomEDFDataset
from darfix.tests.utils import createRandomHDF5Dataset
from orangecontrib.darfix.widgets.blindsourceseparation import (
    BlindSourceSeparationWidgetOW,
)


def get_dimensions(dataset_type):
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

    w = DimensionWidget()

    if dataset_type == "edf":
        dataset = createRandomEDFDataset(dims=(100, 100), header=True)
    elif dataset_type == "hdf5":
        dataset = createRandomHDF5Dataset(dims=(100, 100), metadata=True)
    else:
        raise ValueError(f"Unrecognized dataset_type: '{dataset_type}'")

    w.setDataset(Dataset(dataset))
    w.show()

    qapp.exec()

    return Dataset(w._dataset)


def run_bss(dataset):
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
    w.setDataset(dataset)
    w.set_dynamic_input("dataset", dataset)
    w.show()

    qapp.exec()


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


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
    if options.edf_dataset:
        dataset_type = "edf"
    else:
        dataset_type = "hdf5"
    dataset = get_dimensions(dataset_type=dataset_type)
    run_bss(dataset)


if __name__ == "__main__":
    exec_(sys.argv)
