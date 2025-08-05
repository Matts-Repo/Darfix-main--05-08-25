"""Example creating a dataset using the test random dataset class."""

import argparse
import sys

from darfix.tests.utils import createRandomEDFDataset
from darfix.tests.utils import createRandomHDF5Dataset


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
        createRandomEDFDataset(dims=(100, 100), nb_data_files=50)
    else:
        createRandomHDF5Dataset(dims=(100, 100), nb_data_frames=50)


if __name__ == "__main__":
    exec_(sys.argv)
