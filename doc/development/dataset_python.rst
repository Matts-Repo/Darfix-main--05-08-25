Create a ``ImageDataset`` object in Python
==========================================

A lot of low-level functions in Darfix takes a ``ImageDataset`` or a ``Dataset`` object as input. When testing/debugging these, it can be useful to create such an object in Python to run the functions.

To do this, we use the ``load_process_data`` function:

.. autofunction:: darfix.core.data_selection.load_process_data

Here is an example on how to use it to load a HDF5 dataset (here the **Silicon_111_reflection_0003** dataset)

.. code-block:: python

    from darfix.core.data_selection import load_process_data

    filepath = '/data/scisoft/darfix/datasets/darfix/bliss_hdf5/Silicon_111_reflection_0003/Silicon_111_reflection_0003.h5'
    scan_index = 1
    detector_name = 'pco_ff'

    img_dataset, indices, bg_indices, bg_dataset = load_process_data(
        filenames=f"silx://{filepath}?/{scan_index}.1/measurement/{detector_name}",
        metadata_url=f"silx://{filepath}?{scan_index}.1/instrument/positioners",
        copy_files=False,
        isH5=True,
    )


Then, we use the ``find_dimensions`` method to register the appropriate dimensions in the ``ImageDataset``. This is mandatory to run most operations on a ``Dataset``

.. code-block:: python
    
    from darfix.core.dimension import POSITIONER_METADATA

    img_dataset.find_dimensions(kind=POSITIONER_METADATA, tolerance=1e-5)

The `tolerance` need to be changed depending on the dataset used. We use here the value appropriate for **Silicon_111_reflection_0003**, the default value being `1e-9`.

The ``ImageDataset`` is now ready for computations. For example, we can compute the moments (Center of Mass, Skewness, Kurtosis, ...) by using ``apply_moments``:

.. code-block:: python

    img_dataset.apply_moments()
    moments = img_dataset.moments_dims

.. tip:: 

    For some operations (e.g. noise removal), you will need a ``Dataset`` object. You can generate it from the ``ImageDataset`` object:

    .. code-block:: python

        from darfix.dtypes import Dataset
        from darfix.core.noiseremoval import apply_background_subtraction

        dataset = Dataset(img_dataset)

        new_img_dataset = apply_background_subtraction(dataset)
