Test datasets
=============

A set of datasets is available at `/data/scisoft/darfix/datasets`

The folder contains:

* HDF5 / bliss datasets (*bliss_hdf5* folder)
    * *Silicon_111_reflection_0003*: *chi*, *mu* evolving.
        .. note:: for this dataset you must modify the tolerance to `1e-5` to have a correct fitting of the dimensions

* SPEC / EDF datasets (*spec_edf* folder)
    * *2017_run3_es_binary*
    * *3Dstrainlayer_full*
    * *55min*

* "HDF5-like" datasets (*converted_from_spec_edf_to_hdf5* folder)

    Those datasets were converted from the SPEC / EDF datasets to HDF5 using the `convert_to_hdf5.py` script.
    They were originally created to get HDF5-like datasets before the beamline fully moved to bliss and HDF5
