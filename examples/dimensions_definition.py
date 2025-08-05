import argparse

from silx.gui import qt
from silx.io.url import DataUrl

from darfix.core.data_selection import load_process_data
from darfix.dtypes import Dataset
from darfix.tests.utils import create_3motors_dataset
from orangecontrib.darfix.widgets.dimensions import DimensionWidgetOW


def main(dataset: Dataset):
    qapp = qt.QApplication([])

    w = DimensionWidgetOW()

    w.setDataset(dataset)
    w.show()

    qapp.exec()


if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--hdf5_path",
        type=str,
        help="Path to an hdf5 file containing the dataset",
        default=None,
    )
    argparser.add_argument(
        "--detector",
        default="pco_ff",
        type=str,
        help="Detector name",
    )
    argparser.add_argument(
        "--scan_number",
        default="1.1",
        type=str,
        help="Scan number group (eg: '1.1')",
    )

    args = argparser.parse_args()

    if args.hdf5_path is None:
        print("Use example dataset.")
        dataset = create_3motors_dataset(dir=None, backend="hdf5")
        dataset = Dataset(dataset)
    else:
        data_url = DataUrl(
            file_path=args.hdf5_path,
            data_path=f"/{args.scan_number}/measurement/{args.detector}",
            scheme="silx",
        )
        metadata_url = DataUrl(
            file_path=args.hdf5_path,
            data_path=f"/{args.scan_number}/instrument/positioners",
            scheme="silx",
        )

        dataset = Dataset(
            *load_process_data(
                data_url,
                ".",
                isH5=True,
                metadata_url=metadata_url,
            )
        )

    main(dataset)
