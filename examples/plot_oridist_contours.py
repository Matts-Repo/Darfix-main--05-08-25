"""Sample code illustrating how to custom silx view into another application."""

__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "10/08/2021"


import argparse
import signal
import sys

from silx.gui import qt
from silx.gui.plot import Plot2D
from silx.io.dictdump import nxtodict

from darfix.gui.grainplot.grainPlotWidget import MapType


class PlotOriDistContours(qt.QMainWindow):
    def __init__(self, filename, parent=None):
        qt.QMainWindow.__init__(self, parent)
        plot = Plot2D(parent=self)
        try:
            h5file = nxtodict(filename)
            key = h5file["entry"][MapType.ORIENTATION_DIST.value]["key"]
            curves = h5file["entry"][MapType.ORIENTATION_DIST.value]["curves"]
            plot.addImage(
                key["image"],
                xlabel=key["xlabel"],
                ylabel=key["ylabel"],
                origin=tuple(key["origin"]),
                scale=tuple(key["scale"]),
            )
            for legend in curves:
                if legend != "@NX_class":
                    curve = curves[legend]
                    plot.addCurve(
                        x=curve["points"][0],
                        y=curve["points"][1],
                        linestyle="-",
                        linewidth=2.0,
                        legend=legend,
                        resetzoom=False,
                        color=curve["color"],
                    )
        except KeyError:
            raise KeyError("Make sure orientation distribution keys have been saved")
        self.setCentralWidget(plot)


def createParser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file",
        type=str,
        nargs=argparse.ZERO_OR_MORE,
        help="Data file to show (h5 file)",
    )
    return parser


def exec_(argv=None):
    if argv is None:
        argv = sys.argv
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

    parser = createParser()
    options = parser.parse_args(argv[1:])

    w = PlotOriDistContours(options.file[0])
    w.show()

    qapp.exec()


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    exec_(sys.argv)
