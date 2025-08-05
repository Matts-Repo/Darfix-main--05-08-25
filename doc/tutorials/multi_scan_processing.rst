Process multiple scans from the same HDF5 file
==============================================

.. admonition:: In short

    1. Process one scan with darfix (Orange GUI)
    2. Save the Orange workflow
    3. Use the provided Python script to run this workflow on multiple scans

To process multiple **similar** scans contained in a single HDF5 file (also known as a `master file`), you will need to combine processing from darfix (GUI) and Python (batch).

The first step is to process one scan from the GUI to find the parameters that will be reused for all scans.


Process one scan with darfix
----------------------------

Process a scan as usual with `darfix`. If you are new to `darfix`, have a look at the `main documentation page <../index>`_ first.

Once you did run the processing till the end and are happy with the result, **save the workflow as an OWS file**. By doing so, you will save the processing pipeline (order of tasks **and** parameters).


Process multiple scans with Python
----------------------------------

Now that you have a OWS file describing the processing pipeline, you can use it to process all the desired scans using Python.

For the sake of example, consider that this file is located in ``/data/id00/inhouse/blc0000/RAW_DATA/Sample/Sample_0000/Sample_0000.h5`` and that you saved the workflow in ``/data/id00/inhouse/blc0000/SCRIPTS/darfix_workflow.ows``.

Then, you can process multiple scans by using the following script:

.. code-block:: python

    import os.path

    from ewoks import execute_graph
    
    hdf5_file = '/data/id00/inhouse/blc0000/RAW_DATA/Sample/Sample_0000/Sample_0000.h5'
    scan_list = ['1.1', '2.1', '4.1']
    output_folder = '/data/id00/inhouse/blc0000/PROCESSED_DATA/Sample/Sample_0000/'
    graph = "/data/id00/inhouse/blc0000/SCRIPTS/darfix_workflow.ows"

    for scan in scan_list:
        execute_graph(
            graph,
            inputs=[
                {
                    "name": "raw_input_file",
                    "value": hdf5_file,
                },
                {
                    "name": "raw_detector_data_path",
                    "value": f"/{scan}/instrument/my_detector/data",
                },
                {
                    "name": "raw_metadata_path", 
                    "value": f"/{scan}/instrument/positioners"
                },
                {
                    "name": "treated_data_dir",
                    "value": os.path.join(output_folder, f"Sample_0000_{scan}")
                }
            ],
        )

Adapt and save this script in a Python file (e.g. ``multi_scan_darfix.py``) and you can then run the processing with ``python``

.. code-block:: bash

    python multi_scan_darfix.py

.. tip::

    Variables in the top of the script can be changed and adapted to the usecase. 
    
    For example, ``scan_list`` defines the scan to process that are (`1.1`, `2.1` and `4.1` in the given example).

    ``output_folder`` is the folder where the processing data folders will be created (one per scan). The name of those folders is given by the ``treated_data_dir`` input. 

    **It is absolutely mandatory to have a different** ``treated_data_dir`` **for each scan**. Otherwise, the workflow will save processing files for all scans in the same folder, overwriting them when looping through scans.
