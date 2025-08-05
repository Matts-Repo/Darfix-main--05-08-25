"""Example showing the widget :mod:`~darfix.gui.shiftCorrectionWidget.ShiftCorrectionWidget`."""

__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "09/11/2020"


import argparse
import signal
import sys

from silx.gui import qt
from silx.gui.colors import Colormap
from silx.gui.plot.StackView import StackViewMainWindow

import darfix
from darfix import dtypes
from darfix.gui.chooseDimensions import ChooseDimensionDock
from darfix.tests.utils import createRandomEDFDataset
from darfix.tests.utils import createRandomHDF5Dataset


class ChooseDimensionExampleW(qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self._sv = StackViewMainWindow()
        self._sv.setColormap(
            Colormap(name=darfix.config.DEFAULT_COLORMAP_NAME, normalization="linear")
        )
        self.setCentralWidget(self._sv)
        self._chooseDimensionDock = ChooseDimensionDock(self)
        self._chooseDimensionDock.hide()
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._chooseDimensionDock)
        self._chooseDimensionDock.widget.filterChanged.connect(self._filterStack)
        self._chooseDimensionDock.widget.stateDisabled.connect(self._wholeStack)

    def setDataset(self, dataset: dtypes.Dataset):
        """Saves the dataset and updates the stack with the dataset data."""
        self.dataset = dataset.dataset
        self._update_dataset = dataset.dataset
        self.indices = dataset.indices
        self.bg_indices = dataset.bg_indices
        self.bg_dataset = dataset.bg_dataset
        if len(self.dataset.data.shape) > 3:
            self._chooseDimensionDock.show()
            self._chooseDimensionDock.widget.setDimensions(self._update_dataset.dims)
        if not self._chooseDimensionDock.widget._checkbox.isChecked():
            self._wholeStack()

    def setStack(self, dataset=None):
        """
        Sets new data to the stack.
        Mantains the current frame showed in the view.

        :param Dataset dataset: if not None, data set to the stack will be from the given dataset.
        """
        if dataset is None:
            dataset = self.dataset
        nframe = self._sv.getFrameNumber()
        if self.indices is None:
            self._sv.setStack(dataset.get_data() if dataset is not None else None)
        else:
            self._sv.setStack(
                dataset.get_data(self.indices) if dataset is not None else None
            )
        self._sv.setFrameNumber(nframe)

    def _filterStack(self, dim=0, val=0):
        self.dimension = [dim, val]
        data = self._update_dataset.get_data(self.indices, self.dimension)
        if data.shape[0]:
            self._sv.setStack(data)
        else:
            self._sv.setStack(None)

    def _wholeStack(self):
        self.dimension = None
        self.setStack(self._update_dataset)


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

    w = ChooseDimensionExampleW()

    if options.edf_dataset:
        dataset = createRandomEDFDataset(dims=(100, 100), header=True)
    else:
        dataset = createRandomHDF5Dataset(dims=(100, 100), metadata=True)

    dataset.find_dimensions()
    dataset = dtypes.Dataset(dataset=dataset.reshape_data())
    w.setDataset(dataset)
    w.show()

    qapp.exec()


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    exec_(sys.argv)
