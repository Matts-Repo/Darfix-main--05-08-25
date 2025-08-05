from silx.gui import qt

from darfix.dtypes import Dataset
from darfix.tests.utils import create_3motors_dataset
from orangecontrib.darfix.widgets.grainplot import GrainPlotWidgetOW


def main():
    qapp = qt.QApplication([])

    w = GrainPlotWidgetOW()

    dataset = create_3motors_dataset(dir=None, in_memory=True, backend="hdf5")
    dataset.find_dimensions()
    dataset = Dataset(dataset.reshape_data())
    w.setDataset(dataset)
    w.show()

    qapp.exec()


if __name__ == "__main__":
    main()
