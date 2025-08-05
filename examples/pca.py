"""Example showing the widget :mod:`~darfix.gui.blindSourceSeparation.BlindSourceSeparation`."""

__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "22/12/2020"


import glob
import signal
import sys
from pathlib import Path

import cv2
import numpy
from silx.gui import qt

from darfix import dtypes
from darfix.gui.PCAWidget import PCAWidget
from darfix.tests.utils import createDataset


def exec_(argv=None):

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

    w = PCAWidget()
    images = glob.glob(str(Path(__file__).parent / "figures" / "*"))
    stack = []

    for i, image in enumerate(images):
        im = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        stack.append(im)

    num_images = 100
    n_z = [15, 30, 45, 65, 85]
    # a = range(2,2+len(stack))
    a = [1.0 for img in stack]

    def J(z):
        img = numpy.zeros(stack[0].shape, dtype=numpy.float32)
        for i, image in enumerate(stack):
            G = (a[i] / numpy.sqrt(2 * numpy.pi * 10)) * numpy.exp(
                -0.5 * ((z - n_z[i]) ** 2) / 100
            )
            img += G * numpy.array(image, dtype=numpy.float32)
        # img += abs(numpy.random.normal(0, 10, im.shape).reshape(im.shape))
        return img

    # Construct the input matrix
    data = []
    for i in numpy.arange(num_images):
        data.append(J(i))

    dataset = createDataset(data=data)
    w.setDataset(dtypes.Dataset(dataset=dataset))
    w.show()

    qapp.exec()


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    exec_(sys.argv)
