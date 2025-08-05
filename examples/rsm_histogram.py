from silx.gui import qt

from darfix import dtypes
from darfix.pixel_sizes import PixelSize
from darfix.tests.utils import create_dataset_for_RSM
from orangecontrib.darfix.widgets.rsmhistogram import RSMHistogramWidgetOW


def main():
    qapp = qt.QApplication([])

    w = RSMHistogramWidgetOW()

    dataset = create_dataset_for_RSM(dir=None, backend="hdf5")
    dataset.find_dimensions()
    dataset.compute_transformation(PixelSize["Basler"].value, kind="rsm")

    w.setDataset(dtypes.Dataset(dataset))
    w.show()

    qapp.exec()


if __name__ == "__main__":
    main()
