import argparse
import signal
import sys

from silx.gui import qt

from darfix import dtypes
from darfix.tests.utils import createRandomEDFDataset
from darfix.tests.utils import createRandomHDF5Dataset
from orangecontrib.darfix.widgets.projection import ProjectionWidgetOW


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
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler
    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    w = ProjectionWidgetOW()

    if options.edf_dataset:
        dataset = createRandomEDFDataset(dims=(100, 100), nb_data_files=10, header=True)
    else:
        dataset = createRandomHDF5Dataset(
            dims=(100, 100), nb_data_frames=10, metadata=True
        )

    dataset.find_dimensions()
    reshaped_dataset = dataset.reshape_data()
    w._widget.setDataset(reshaped_dataset)
    w.set_dynamic_input("dataset", dtypes.Dataset(reshaped_dataset))

    w.show()

    qapp.exec()


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    exec_(sys.argv)
