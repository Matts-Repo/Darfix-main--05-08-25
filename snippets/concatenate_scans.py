"""
This scripts concatenate datasets from a list of files to an output file.
Concatenate scans are:
    * detector dataset (using a VirtualDataset (VDs)): warning: this dataset will contain relative link to the original files. And moving it will break the VDS
    * positioner dataset

It will go through all files then browse all entries for the detector_dataset_path and the output_file.
The input that you can modify are all in the 'main' function
"""

import logging
import os
import sys
from typing import Iterator
from typing import Optional
from typing import Tuple

import h5py
import numpy
from silx.io.dictdump import dicttoh5

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

VDS_POLICY = "relative"
"""
Virtual dataset policy. Values can be:
* 'absolute': in this case the links will be done with the absolute path. Safer for 'single' shot processing.
* 'relative': in this case the links will be done with relative path. Safer if we want to move files. Links will be preserved as long as relative path are preserved.
"""


def _concatenate_dict(dict_1: dict, dict_2: dict) -> None:
    """
    concatenate two dicts into dict_1. Keys are str and values are numpy.ndarray
    """
    assert isinstance(dict_1, dict)
    assert isinstance(dict_2, dict)
    for key in dict_2.keys():
        if key in dict_1.keys():
            dict_1[key] = numpy.concatenate((dict_1[key], dict_2[key]))
        else:
            dict_1[key] = dict_2[key]


def _check_positioners_consistency(my_dict: dict) -> None:
    """
    make sure all the values of 'my_dict' have the same number of elements
    """
    n_elmts = numpy.median([len(value) for value in my_dict.values()])
    for key, value in my_dict.items():
        if len(value) != n_elmts:
            _logger.warning(
                f"Found inconsistent positioner dataset '{key}'. Get {len(value)} elements when {n_elmts} expected"
            )


def _filter_static_positioners(my_dict: dict) -> None:
    """
    replace all positioners which have a unique value by a scalar
    """
    keys = tuple(my_dict.keys())
    for key in keys:
        uniques = numpy.unique(my_dict[key])
        if len(uniques) == 1:
            my_dict[key] = uniques[0]


def _iter_positioner_datasets(
    positioners: h5py.Group,
) -> Iterator[Tuple[str, numpy.ndarray]]:
    # Some positioners are detectors and therefore scalars in `positioners`.
    # To detect those we need to check whether the positioner has a group
    # in the instrument group.
    instrument = positioners.parent
    instrument_names = list(instrument)

    for key in positioners:
        dataset = None

        if key in instrument_names:
            group = instrument[key]
            NX_class = group.attrs.get("NX_class", None)
            try:
                if NX_class == "NXpositioner":
                    dataset = group["value"]
                elif NX_class == "NXdetector":
                    dataset = group["data"]
            except KeyError:
                pass

        if dataset is None:
            dataset = positioners[key]

        if not isinstance(dataset, h5py.Dataset):
            _logger.warning(f"Found a none h5py.Dataset in entry {positioners}: {key}")
        else:
            yield key, dataset[()]


def create_virtual_source(
    input_dataset: h5py.Dataset, output_file: str
) -> h5py.VirtualSource:
    """
    create the VirtualSource according to the defined policy
    """
    if VDS_POLICY == "absolute":
        return h5py.VirtualSource(input_dataset)
    elif VDS_POLICY == "relative":
        relpath = os.path.relpath(
            os.path.abspath(input_dataset.file.filename),
            os.path.dirname(os.path.abspath(output_file)),
        )
        if not relpath.startswith("./"):
            relpath = "./" + relpath
        return h5py.VirtualSource(
            path_or_dataset=relpath,
            name=input_dataset.name,
            shape=input_dataset.shape,
            dtype=input_dataset.dtype,
        )
    else:
        raise ValueError(
            f"VDS_POLICY should be 'absolute' or 'relative'. Get '{VDS_POLICY}'"
        )


def concatenate_scans(
    input_file: str,
    entries_to_concatenate: Optional[tuple],
    output_file: str,
    detector_dataset_path: str,
    positioners_dataset_path: str,
    output_entry_name: str = "entry_0000",
    overwrite: bool = False,
) -> None:
    """
    :param input_file: proposal file containing link to all the detector frame...
    :param entries_to_concatenate: tuple of all entries to concatenate. Order will be preserved. If None provided then all entries will be concatenated
    :param output_file: location of the output file
    :param detector_dataset_path: path to the detector dataset, output dataset will have the same location
    :param positioners_dataset_path: path to the positioners datasets (containing motor positions), output dataset will have the same location
    :param overwrite: if False and output file exist then will not overwrite it
    """
    _logger.info("start concatenation")
    # check inputs
    if os.path.exists(output_file) and not overwrite:
        raise OSError(
            f"output file exists ({output_file}). Please remove it before processing or set 'overwrite to True'"
        )
    if not isinstance(detector_dataset_path, str):
        raise TypeError("detector_dataset_path should be a str")
    if not isinstance(output_entry_name, str):
        raise TypeError("output_entry_name should be a str")
    if not isinstance(positioners_dataset_path, str):
        raise TypeError("positioners_dataset_path should be a str")

    def get_sorted_entries(entries: tuple):
        def get_entry_scan_num(entry_name):
            # entries are expected to be given as x.y
            return int(entry_name.split(".")[0])

        return sorted(entries, key=get_entry_scan_num)

    # concatenate
    with h5py.File(input_file, mode="r") as h5f_input:
        if entries_to_concatenate is None:
            # sort entries to concatenate
            entries_to_concatenate = get_sorted_entries(h5f_input.keys())

        _logger.info(f"(sorted) entries to concatenate {entries_to_concatenate}")
        entries_n_frame = []
        # store the number of frames along all entries
        frame_shape = None
        detector_data_type = None
        positioners = {}
        virtual_sources = []
        # number of frame concatenateed
        for entry in entries_to_concatenate:
            # 1.0 handle detector dataset
            # note: detector frame won;t be duplicated but link to the original file using a Virtual Dataset (VDS)
            entry_detector_path = "/".join([entry, detector_dataset_path])
            if entry_detector_path not in h5f_input:
                _logger.error(
                    f"Unable to find detector path {entry_detector_path}@{input_file}"
                )
                continue
            if h5f_input[entry_detector_path].ndim != 3:
                raise ValueError(
                    f"detector dataset are expected to be 3D. Get {h5f_input[entry_detector_path].ndim}"
                )
            # 1.1: get metadata from the dataset and make sure it is coherent along all the detector datasets
            entry_n_frame = h5f_input[entry_detector_path].shape[0]
            entry_frame_shape = h5f_input[entry_detector_path].shape[1:]
            entries_n_frame.append(entry_n_frame)
            if frame_shape is None:
                frame_shape = entry_frame_shape
            elif entry_frame_shape != frame_shape:
                raise ValueError(
                    f"Incoherent frame shape. {entry} get {entry_frame_shape} when {frame_shape} expected"
                )
            if detector_data_type is None:
                detector_data_type = h5f_input[entry_detector_path].dtype
            elif detector_data_type is not h5f_input[entry_detector_path].dtype:
                raise TypeError(
                    f"Inconsistent data type between the scan. {entry} get {h5f_input[entry_detector_path].dtype} when {detector_data_type} expected"
                )
            # 1.2: create VirtualSource to be used once entries browse

            virtual_sources.append(
                create_virtual_source(
                    input_dataset=h5f_input[entry_detector_path],
                    output_file=output_file,
                )
            )
            # 2.0 handle positioners.
            # note: positioners dataset will be copied
            # number of frame in the current entry / scan
            entry_positioner_path = "/".join([entry, positioners_dataset_path])
            if entry_positioner_path not in h5f_input:
                _logger.error(
                    f"Unable to find positioners path {entry_positioner_path}@{input_file}"
                )
                continue
            entry_positioners_grp = h5f_input[entry_positioner_path]
            # HDF5 group containing the positioners
            entry_positioners = {}
            # dict used to concatenate all the positioners as numpy array
            for key, value in _iter_positioner_datasets(entry_positioners_grp):
                if numpy.isscalar(value) or len(value.shape) == 0:
                    # convert scalars to arrays. As a value can be static in a scan context but
                    # dynamic / array in the scope of the full acquisition
                    value = numpy.array([value] * entry_n_frame)
                entry_positioners[key] = value

            _concatenate_dict(positioners, entry_positioners)
        # write the detector virtual dataset (VDS) to output file
        with h5py.File(output_file, mode="w") as h5f_output:
            output_detector_dataset_path = "/".join(
                (output_entry_name, detector_dataset_path)
            )
            n_frames = numpy.sum(entries_n_frame)
            virtual_layout = h5py.VirtualLayout(
                shape=(n_frames, frame_shape[0], frame_shape[1]),
                dtype=detector_data_type,
            )
            assert len(virtual_sources) == len(
                entries_n_frame
            ), "we expect one virtual source per entry"
            virtual_layout_index = 0
            for entry_n_frame, virtual_source in zip(entries_n_frame, virtual_sources):
                virtual_layout[
                    virtual_layout_index : virtual_layout_index + entry_n_frame
                ] = virtual_source
                virtual_layout_index += entry_n_frame

            h5f_output.create_virtual_dataset(
                output_detector_dataset_path, virtual_layout
            )
    # check number of elements is coherent else warm the user
    _check_positioners_consistency(positioners)
    _filter_static_positioners(positioners)

    dicttoh5(
        positioners,
        h5file=output_file,
        h5path="/".join((output_entry_name, positioners_dataset_path)),
        mode="a",
    )

    _logger.info(
        f"concatenation finished. You can run 'silx view {output_file}' to check the result"
    )


def main(argv):

    # as only the detector images are saved in 'scan_XXXX' we are forced to have the proposal file as input

    input_file = "/tmp_14_days/payno/test_id03/110_pre_strained_3pct_anneale_2x_mosa_test/110_pre_strained_3pct_anneale_2x_mosa_test.h5"

    entries_to_concatenate = None  # either provite a tuple of dataset group like ("1.1", "1.2") or None. If None

    output_file = "/tmp_14_days/payno/test_id03/110_pre_strained_3pct_anneale_2x_mosa_test/concatenated_scans_darfix.hdf5"

    detector_dataset_path = "measurement/pco_ff"  # warning: do not provide the first entry. The script will automatically go through all existing

    positioners_dataset_path = "instrument/positioners"

    concatenate_scans(
        input_file=input_file,
        entries_to_concatenate=entries_to_concatenate,
        output_file=output_file,
        detector_dataset_path=detector_dataset_path,
        positioners_dataset_path=positioners_dataset_path,
    )


if __name__ == "__main__":
    main(sys.argv)
