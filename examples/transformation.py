from silx.gui import qt

from darfix.dtypes import Dataset
from darfix.tests.utils import createRandomHDF5Dataset
from orangecontrib.darfix.widgets.transformation import TransformationWidgetOW


def main():
    app = qt.QApplication([])

    w = TransformationWidgetOW()
    dataset = createRandomHDF5Dataset(
        (100, 100), nb_data_frames=5, metadata=True, num_dims=1
    )
    dataset.find_dimensions()
    dataset.reshape_data()
    w.setDataset(Dataset(dataset))

    w.show()
    app.exec()


if __name__ == "__main__":
    main()
