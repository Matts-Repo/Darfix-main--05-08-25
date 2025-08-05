from silx.gui import qt

from orangecontrib.darfix.widgets.hdf5dataselection import HDF5DataSelectionWidgetOW

if __name__ == "__main__":
    qapp = qt.QApplication([])

    w = HDF5DataSelectionWidgetOW()

    w.show()

    qapp.exec()
