Darfix
======

``darfix`` is a project to create and execute workflows to process dark-field X-ray microscopy data acquired at the ID03 beamline at ESRF. 

It provides a graphical user interface based on `Orange <https://orangedatamining.com/>`_ to load the data, pretreat it and derive grain plots or rocking curves (see `Garriga Ferrer J. et al. 2023 <https://doi.org/10.1107/S1600577523001674>`_ for more details).

These operations (or tasks) can be arranged as computational data pipelines, also called workflows, and can be run headless with `Ewoks <https://ewoks.esrf.fr/en/latest/>`_.

Installation
------------

You can install darfix as any usual Python package 

.. code-block:: bash
   :caption: With `pip`

   pip install darfix[full]

.. tip::

   It is recommended to create a `virtual environment <https://docs.python.org/3/library/venv.html>`_ to
   avoid conflicts between dependencies. Click below for instructions on how to do so.

   .. dropdown:: Create a virtual environment

      On Linux or Mac

      .. code-block:: bash

         python3 -m venv /path/to/new/virtual/environment

         source /path/to/new/virtual/environment/bin/activate

      On Windows

      .. code-block:: batch

         python3 -m venv C:\path\to\new\virtual\environment

         C:\path\to\new\virtual\environment\Scripts\activate.bat

      *Note: To deactivate the environment, call:* :code:`deactivate`

.. admonition:: At ESRF

   On a computer inside ESRF network, you can load ``darfix`` by running

   .. code-block:: bash
      
      module load darfix

.. dropdown:: Troubleshooting

   On Windows you may get this installation error

   .. code-block:: bash

      Building wheels for collected packages: ewoksorange
      Building wheel for ewoksorange (pyproject.toml) ... error
      error: subprocess-exited-with-error

      × Building wheel for ewoksorange (pyproject.toml) did not run successfully.
      │ exit code: 1
      ╰─> [154 lines of output]
         ...
         error: could not create 'build\lib\ewoksorange\tests\examples\ewoks_example_1_addon\orangecontrib\ewoks_example_supercategory\ewoks_example_subcategory\tutorials\sumtask_tutorial3.ows': No such file or directory
         [end of output]

      note: This error originates from a subprocess, and is likely not a problem with pip.
      ERROR: Failed building wheel for ewoksorange
      Failed to build ewoksorange
      ERROR: Could not build wheels for ewoksorange, which is required to install pyproject.toml-based projects

   If you do, you need to enable long paths. Instructions to do this in Windows 10 or later can be found `here <https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry>`_.


Usage
-----

Launch the Orange canvas

.. code-block:: bash

    darfix

Then, you can have a look at the example workflows in `Help > Example workflows`.

The :doc:`../tutorials/index` and the :doc:`../widgets/index` documentation give detailed explanations on the different tasks in the example workflows.

If you already have a workflow, you can open it directly in the Orange canvas using

.. code-block:: bash

    darfix my_workflow.ows


.. toctree::
   :hidden:

   tutorials/index.rst
   widgets/index.rst
   ewoks_tasks.rst
   changelog.rst
   license.rst
   development/index.rst
   archives/index.rst
