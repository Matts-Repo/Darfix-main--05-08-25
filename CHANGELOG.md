# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [3.0.0] - 2025-07-30

### Added

- _Dimension Definition_ : new parameter to handle zigzag mode. ([Issue 216](https://gitlab.esrf.fr/XRD/darfix/-/issues/216))

- _Dimension Definition_ : Inputs are filled automatically in case of a `fscan` or a `fscan2d` acquisition ([Issue 188](https://gitlab.esrf.fr/XRD/darfix/-/issues/188))

- _ROI_ : ROI is clamped to the dataset shape when user click to apply. ([PR 484](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/484)). 

- _Noise Removal_ : Previously saved operations can now be replayed in one click. ([PR 468](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/468)).

- _Rocking Curve_ : Add axis names to rocking curve plot ([PR 517](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/517)).

### Changed

- Documentation : Reorganize documentation ([PR 508](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/508)).
- Documentation : Enrich Ewoks tasks reference ([PR 503](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/503)).

- _HDF5 Selection_ : Widget reworked in one single tab. Positioner and detector paths can be autofilled by selecting a scan number ([Issue 175](https://gitlab.esrf.fr/XRD/darfix/-/issues/175))

- _Dimension Definition_ : Inputs are validated automatically when changed ([PR 491](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/491)) ([PR 510](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/510)).
- _Dimension Definition_ : Dimension validation is improved ([PR 509](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/509)) .
- _Dimension Definition_ : In dimension table, 'Range' is replaced by two columns 'Start' and 'Stop' ([PR 463](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/463)).

### Fixed

- _Shift Detection_ : Shift is loaded if previously saved (Not fixed for now if 'filter by dimension' is unchecked) ([Issue 212](https://gitlab.esrf.fr/XRD/darfix/-/issues/212))

- _Noise Removal_ : Settings are loaded if previously saved ([Issue 205](https://gitlab.esrf.fr/XRD/darfix/-/issues/205))

- _ROI_ : Users cannot applied two time a ROI within the same widget and the dataset is not recomputed when validated ([Issue 176](https://gitlab.esrf.fr/XRD/darfix/-/issues/176)).

- _Dimension Definition_ : User inputs are disable when dataset is not set ([Issue 105](https://gitlab.esrf.fr/XRD/darfix/-/issues/105))
- _Dimension Definition_ : Dimension can now have a negative step ([Issue 220](https://gitlab.esrf.fr/XRD/darfix/-/issues/220))

- _Rocking Curve_ : Raise explicitly an error when dimension count is greater than 2 ([PR 465](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/465)).

- Plots are plotted with equal aspect ratio ([Issue 160](https://gitlab.esrf.fr/XRD/darfix/-/issues/160))    
- Removed unneeded inputs so that links between tasks automatically map `dataset` to `dataset` by default ([Issue 208](https://gitlab.esrf.fr/XRD/darfix/-/issues/208))

- Documentation : Fix empty Ewoks tasks section ([Issue 145](https://gitlab.esrf.fr/XRD/darfix/-/issues/145))

- _Concatenate scans_ : Fix metadata reading when `positioners` group contains 2D / 3D datasets ([Issue 150](https://gitlab.esrf.fr/XRD/darfix/-/issues/150))


### Removed

- _HDF5 Selection_ : Remove configuration level('Required' / 'Advanced' options) ([PR 474](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/474)).

- _Dimension Definition_ : Remove buttons 'Add', 'Clear' and 'Fit' ([PR 491](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/491)).
- _Dimension Definition_ : In dimension table, remove columns 'Kind' and 'Tolerance' ([PR 463](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/463)).
- _Dimension Definition_ : Remove'Metadata type' combo box ([PR 463](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/463)).

- Remove `colormap` input in ewoks tasks ([Issue 208](https://gitlab.esrf.fr/XRD/darfix/-/issues/208))

## [2.5.1] - 2025-06-26

### Fixed

- Issue #204 : output directory of batch processing.
  Fix breaking change by renaming root_dir in treated_data_dir in HDF5DataSelection.

## [2.5.0] - 2025-04-15

### Added

- _Rocking curves_: Headless computation now saves the fitted data in `rocking_curves.h5`.

### Changed

- Requirements were updated: Darfix now uses Silx v2 and Ewoks v1.

### Fixed

- _HDF5 data selection_: The "Treated data" folder input is now properly saved and restored between runs.
- _HDF5 scans concatenation_: Fixed an issue where the data could not be saved if the directory was not already existing.

## [2.4.0] - 2025-03-13

### Added

- _HDF5 data selection_: Add the possibility to manually select detector and metadata path by browsing the HDF5 file.
- _Rocking curves_: Add motor names in the combobox entries so that they are more easily identifiable.

## Changed

- _Shift correction_: Applied shift is no longer cumulative: the shift correction will always be applied to the input, uncorrected dataset.

### Fixed

- _Noise removal_: Fix error when converting workflows as JSON with saved inputs in this widget.
- _Shift correction_: Fix inversion of vertical and horizontal shift.
- _Shift correction_: Disable "Ok" button when no output would be generated (i.e. no shift applied).
- _ZSum_: Fix multiple triggers of the computation when getting a new dataset.
- _ZSum_: Fix inconsistent results when the data could be filtered by dimensions.
- _ZSum_: Restore saved dimension filtering when possible.

## [2.3.1] - 2025-02-26

### Fixed

- _Grain plot_: Fix inversion of X and Y in hue computation of Mosaicity and Orientation distribution.

## [2.3.0] - 2025-02-24

### Added

- _Grain plot_ (task): New input `orientation_img_origin` to choose the origin of the orientation distribution map.
- _Noise removal_: Display a progress bar in the terminal when removing hot pixels.
- _Noise removal_: Show history of operations by default.

### Changed

- _Rocking curves_: `lm` is now the default fit method.

### Fixed

- _Grain plot_: Fix inversion of X and Y in Orientation distribution contours.
- _Grain plot_: Fix plot not showing after computation of moments for 1D datasets.
- _Noise removal_: Disable "Ok" button when no output would be generated (i.e. no operation in the history).

## [2.2.0] - 2025-02-19

### Added

- _HDF5 data selection_: Operations on files in `RAW_DATA` will save the processed data in `PROCESSED_DATA` if no processing folder is given.
- _EDF data selection_, _HDF5 data selection_ Display a progress bar in the terminal when loading data in memory.
- _Grain plot_: Display a progress bar in the terminal when computing moments.
- _Grain plot_: Display a different message when there is no input and when the computation is ongoing.
- _Grain plot_: Raise an error when trying to compute maps on datasets with no dimensions.

### Fixed

- _Grain plot_, _RSM histogram_: Fix data being saved in the workflows that led to enormous workflow sizes.

## [2.1.1] - 2025-01-21

### Fixed

- _HDF5 data selection_: Restore compatibility with PyQt5.

## [2.1.0] - 2025-01-17

### Added

- _HDF5 data selection_: Speed up loading of the data.
- _Grain plot_: Saved RGB maps can be visualized in h5web.
- _Grain plot_: Display a message while computation is ongoing.
- _Noise removal_: History of operation can now displayed on the bottom of the widget.

## Changed

- _Grain plot_: Changed the _Axis type_ selection controls.
- Requirements were updated: Darfix now uses PyQt6 by default.

### Fixed

- _Grain plot_: Fix mosaicity formula.
- _Grain plot_: Use center of mass rather than motor postions for axes of the mosacity color key plot.


## [2.0.0] - 2024-12-16

### Added

- Add widget for HDF5 scan concatenation ([PR 335](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/335)).
- Add support for Numpy 2 ([PR 375](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/375)).
- _Dimension definition_: Add support for `f2scan` motors ([Issue 135](https://gitlab.esrf.fr/XRD/darfix/-/issues/135)).
- _Grain plot_: Add contour numerical values to the exported maps ([Issue 134](https://gitlab.esrf.fr/XRD/darfix/-/issues/134)).
- _Rocking curves_: Allow to select the fit method ([PR 360](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/360)).

### Changed

- Add support for Python 3.12 and drop support of Python 3.6 and 3.7.
- The `darfix` command line is now only used to start the Orange canvas `darfix <workflow_name>` or display the Darfix version `darfix --version`. To execute a workflow without GUI, use `ewoks execute <workflow_name>`. See the [Ewoks tutorial page](https://darfix.readthedocs.io/en/latest/tutorials/ewoks_tutorial.html) for more information.
- The _Data selection_ widget was split in two widgets: one for EDF and another for HDF5 ([PR 352](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/352)). Information about the different widgets can be found on the [Widgets page](https://darfix.readthedocs.io/en/latest/widgets/index.html).

- Darfix now relies on [Ewoks](https://ewoks.esrf.fr/en/latest/) for data processing. A new specific tutorial can be found in the [documentation](https://darfix.readthedocs.io/en/latest/user_guide/introduction.html).

### Fixed

- _Data selection_: Fix `IndexError: invalid index to scalar variable` ([PR 348](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/348)).
- _Dimension definition_: Fix wrong range for unordered motor datasets ([PR 340](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/340)).
- _Dimension definition_: Fix error on missing dataset values `TypeError: '>' not supported between instances of 'int' and 'NoneType'` ([Issue 144](https://gitlab.esrf.fr/XRD/darfix/-/issues/144)).
- _Transformation_: Fix `TypeError: bad operand type for unary -: NoneType` ([Issue 136](https://gitlab.esrf.fr/XRD/darfix/-/issues/136)).
- _ZSum_: Add missing method `setColormap` ([PR 363](https://gitlab.esrf.fr/XRD/darfix/-/merge_requests/363)).
- Improve error messages for data selection widgets.
- Improve error messages for widgets that require previous operations (e.g. RSM histogram).

### Removed

- _Flash_ widget was removed.

## [1.0.2] - 2024-05-14

### Fixed

- Handle processing from CLI for HDF5.
- Fix dimension fitting.
- Remember previous selected filename for HDF5 dataset.

## [1.0.1] - 2024-04-18

### Fixed

- Fix scikit-image dependency versions.
- Handle API changes of `skimage.registration.phase_correlation`.
- Fix `load_process_data` for a string URL.
- Fix `darfix.core.dimension.Dimension.set_unique_values` when dimension values and step size are small.

## [1.0.0] - 2024-02-20

### Added

- Support HDF5 (including positioners).
- Widget to recover weak beam to obtain dislocations.
- Add top-threshold to the noise removal widget.

### Changed

- Use named tuples when passing data between tasks.
- Provide meaningful message when no dataset provided.
- Upper bound on silx and orange3 packages.

### Fixed

- ROISelectionWidget: reset ROI for new datasets.
- TransformationWidgetOW: reset dimensions for new datasets.
- Fix dtype bug in dataset NMF (blind source separation).
- Support latest PyQt5 API changes.

## [0.10.0] - 2023-07-13

### Added

- Allow ROI selection with integer numbers (by manually typing them).

## Fixed

- Fix data appearing outside of defined dimensions range.
- Reduce memory usage.

## [0.9.8] - 2023-05-10

### Fixed

- Fix Mapping import bug.

## [0.9.7] - 2023-03-01

## Changed

- Reduce memory usage in the rebinning task.
- Partition data widget: range of histogram X-axis based on the number of bins and not intensity.
- Rename "in disk" to "on disk".
- Make all directory creation recursive.
- Clear the mask in the noise removal widget when the ROI changes.

## Fixed

- Fix rocking curve map names when exporting.
- Ignore flash widget in batch processing.

## [0.9.6] - 2023-01-16

### Changed

- Opencv-python<4.7 for python 3.6.
- Fix RSM histogram axes.

## [0.9.5] - 2022-12-20

### Fixed

- Support numpy >= 1.24.

## [0.9.4] - 2022-12-16

### Fixed

- Fix mask error in noiseRemovalWidget.

## [0.9.3] - 2022-12-02

### Fixed

- Fix plot axes in grainPlotWidget, zSumWidget and rockingCurvesWidget.
  when an axes transformation is involved
- Handle NaNs in datasets.

## [0.9.2] - 2022-10-18

### Fixed

- Opencv-python==4.3.0.36 is not on pypi so make it opencv-python>=4.3.0.36.

## [0.9.1] - 2022-10-18

### Changed

- Proper project structure.
- Ewoks lower version bounds.

### Fixed

- Fix orangecontrib namespace package.

## [0.9.0] - 2022-06-10

### Changed

- Core:
  - `mapping.py`:
    - Add binning function (MR !174).
    - Add RSM Histogram function based on Mads Carlsen scripts (MR !176).
    - Improve calculation of RSM to take into account angle tilt (use eta insatead of chi) (MR !176).
  - `dataset.py`:
    - Add `apply_binning` method (MR !174).
    - Add `apply_mask_removal` method and MASK operation (MR !179).
    - Add `compute_rsm` method (MR !176).
    - Append "fake" values to metadata when data is HDF5 (MR !182).
    - Mosaicity: Add third motor parameter and option to choose dimensions to use(MR !177).
    - Project: Allow 2D projection (MR !177).
    - Metadata: Allow for empty rows by setting them to 0 (MR !180).
    - Find dimensions: Return False if dataset is H5 (no dimensions in this case) (MR !182).
  - `dimensions.py`: Sort items of dictionary (MR !181) and return empty dict if no dims when converting to dictionary (MR !182).
  - `imageOperations.py`: Add `mask_removal` function (MR !179).
  - `process.py`: Add mask parameter in `NoiseRemoval` (MR !179) and add `RSMHistogram` function (MR !176).
- GUI:
  - Create widget for binning (MR !174).
  - Add RSMHistogramWidget (MR !176).
  - `noiseRemovalWidget.py`: Add mask property (MR !179).
  - `utils.pt`: Add `values` and `_filter` attributes in `ChooseDimensionWidget` (MR !177).
  - `grainPlotWidget.py`:
    - Add option to choose motors in ori dist and mosaicity maps for 3D datasets(MR !177).
    - Save origine attribute when exporting ori dist and remove minimum size for window (MR !181).
    - Show error message if there are no dimensions defined (MR !182).
  - `projectionWidget.py`: Use `ChooseDimensionWidget` to choose dimensions to project (MR !177).
  - `dimensionsWidget.py`: Show error message when trying to find dimensions in H5 dataset (MR !182).
- Examples: Add binning example (MR !174) and rsmHistogram example (MR !176). Fix typo with keys in `plot_ori_dist` (MR !181).
- Orangecontrib: Add binning widget and its icon (MR !174) and rsmHistogram widget (MR !176).

## [0.8.0] - 2022-04-27

### Changed

- Change needed opencv-python version to fix bug (4.3.0.36) (MR !155).
- Core:
  - `process.py`: Add optional_input_names missing as input parameters (MR !162) and add Projection class (MR !155).
  - `dataset.py`:
    - Dataset:
      - Remove temporary directories (MR !166).
      - Fit: Remove loop along dimensions and return fitted parameters (MR !170).
      - Add title attribute (MR !154).
      - Add `project_data` method to return a new Dataset with the projected data (MR !155).
      - Partition: Add option to filter by top bin (MR !173).
      - Projection: Only add projected image if exists and fix typo with metadata values (MR !169).
      - Shift: Use h5py copy function to avoid loading dataset on memory (MR !169).
      - Orientation distribution: Compute for more than 1 dimensions dataset using first two dimensions (MR !169).
      - PCA: Temporarily set a fixed number of chunks to avoid memory errors on big datasets (MR !169).
    - Data:
      - Save: Use indices to not copy all data if not needed (MR !175) and filter by indices after flattening (MR !171).
  - `dimension.py` (MR 169):
    - Add `unique_values` in `Dimension` `__init__`.
    - Convert axis to `int` before converting dictionary to `Dimension`.
  - `mapping.py`:
    - Return fitted parameters with rocking curves (MR !170).
    - Add multi_gaussian method (MR !155).
    - Add 2D rocking curve fit and 2D data fit (MR !155).
    - Return FWHM value instead of std both in moments and rocking methods (MR !172).
    - Add indices in generator and use them for 2D fit (MR !169).
    - Make sure bounds are feasible when fiting rocking curves and set lower bound of std to 0 (MR !171).
  - `utils.py`:
    - Create function to create NXdata in dict form (MR !172).
  - `test`:
    - `partition.py`: Computer partition using range (MR !173).
    - `dimension.py`: Add 2D fit test method (MR !169).
- Decomposition (MR !169):
  - `base.py`: Use indices when computing error.
- GUI:
  - Add optional title into plots (MR !154).
  - `dataSelectionWidget.py`: Add option to enter workflow title (MR !154).
  - `magnificationWidget.py`: Add Orientation Enum class to define orientations (MR !160).
  - `shiftCorrectionWidget.py`: Fix error when filtering data after data partition (MR !167).
  - `rockingCurvesWidget.py`:
    - Add `Background` map replace `Integrated intensity` for `Amplitude` (MR !170).
    - Use fitted parameters to show the maps (MR !170).
    - Remove "filter by dimension" option (MR !170).
    - Change `Method` class to `Maps` and add `Maps_2D` class to enumerate the maps when having 2D data (MR !155).
    - Show label with parameters for each rocking curve (MR !155).
    - Apply transformation if any (MR !155).
    - Show image with fitted contours instead of rocking curve with 2D datasets (MR !155).
    - Export 2D maps (MR !155) and use NXdata for each (MR !172).
    - Add residuals property (MR! 172).
    - Use plotRockingCurves method when changing stackview frame and put zeros in unused indices (MR !169).
  - `grainPlotWidget.py`:
    - Add option to center the axes or use motor values in orientation distribution (MR !155).
    - Create property for mosaicity (MR !172).
    - Export maps: create NXdata for each map, and add transformation axes if necessary.
  - `dataPartitionWidget.py`: Compute partition using range (MR !173).
  - `noiseRemovalWidget.py`: Add DATA_TYPES Enum (MR !173).
  - `utils.py`: Add `vertical` parameter in `ChooseDimensionWidget` to set orientation of widget (MR !169).
  - `displayComponentsWidget.py`:
    - Use `ChooseDimensionWidget` to filter by dimension and add corresponding methods to filter and unfilter (MR !169).
    - Use `indices` when applying threshold (MR !175).
  - `linkComponentsWidget.py`: Convert dimensions to `AcquisitionDims` (MR !169).
  - Create new widget "ProjectionWidget" to reduce the number of data in a 2D dataset by projecting one of the dimensions (MR !155).
- IO:
  `utils.py`: Modify read and write compontents functions to save/read to/from dimensions dictionary and to save dimensions values(MR !169)
- Examples: Add projection example (MR !155).
- Orangecontrib: Add `projection.py` widget (MR !155).
- Gitlab-ci: Add continous deployment and tests for win32 (MR !163).

## [0.7.3] - 2022-02-04

### Changed

- Core:
  - `mapping.py`: Convert list to numpy array to allow calculate ptp() (MR !152).
  - `dataset.py`:
    - Dataset:
      - Append url to urls list to avoid error when not fitting (MR !152).
      - Bs/hp/tr: Create temporary hdf5 file to save the new data in case of data partition(MR !159).
    - Data: Modify save() method to reshape modified urls to previous shape (MR !159).
  - `test`:
    - Dataset: Add tests that use hdf5 as input (MR !159).
- GUI:
  - `rockingCurvesWidget.py`: Add export maps option (MR !152).
  - `roiSelectionWidget.py`: Fix bug when ROI is None (MR !157).
  - `dimensionsWidget.py`: Fix typo when computing unique values with more than two dimensions (MR !158).
  - `displayComponentsWidget.py`: Create MixingPlotsWidget (MR !158).
  - `linkComponentsWidget.py`: Only show scatter if number of dimensions is 2 (MR !158).
- Io:
  - `utils.py`: Write components with shape parameter (MR !158).

## [0.7.2] - 2021-12-16

### Changed

- Core (!MR 156):
  - `dataset.py`: Remove unused `treated` property.
  - `data_selection.py`: Fix typo when creatintg treated directory. Dark treated files are now saved under `treated/dark`.

## [0.7.0] - 2021-12-14

### Changed

- Add ewoks support instead of pypushflow and allow for batch processing (MR !143, !149).
- `requirements.txt`: Add ewoksorange and remove Orange3 version (MR !143, !144).
- Core:
  - `dataset.py`:
    - Accept new parameter `isH5` which reads an hdf5 file (MR !140).
  - `dimensions.py`:
    - `Dimension`: Add `_range` attribute (MR !141).
    - Create new method `_values_with_step` that finds the range between a set of values (MR !141).
    - Modify method `_set_unique_values` to use `range` (start/stop/step) as first option for the values, and to use `size` if `step` is 0 or None. (MR !141, !142, !144).
  - `mapping.py`:
    - `fit`: Fix typo: use `int_thresh` parameter instead of fixed value (MR !140).
    - `magnification`: Add parameter to uncenter axes (MR !151).
    - Add function to compute peak position map and add tests (MR !150).
    - Add tests for moments, magnification and rsm (MR !148).
  - `process.py`: Use ewoks instead of pypushflow and update classes as necessary (MR !143, !142).
  - `data_selection.py`: Create new function to load data and create Dataset (MR !143).
  - Tests: Use seed for random numbers to avoid failing of tests in image registration(MR !153).
- Decomposition (MR !146):
  - Use chunks to compute norms.
  - Add squared frobenius norm.
  - NMF: Fix update of H and W matrices by chunks. Use `error_step` to check for convergence.
  - Tests: Use seed for random numbers to avoid failing of tests in NMF and NICA (MR !153).
- GUI:
  - Pass parent by parameter when setting datasets (to all GUI widgets) and add `_updateDataset` methods to free memory of datasets (MR !140).
  - `datasetSelectionWidget.py`: Add checkbox for hdf5 files, dimension definition is still not controlled for this files (MR !140).
  - `dimensionsWidget.py`:
    - Add `Range` vertical header (MR !141).
    - `_DimensionItem`: Create `_RangeWidget` to accept `start/stop/step` values before using unique values(MR !141).
    - `DimensionWidget`: Improve `fit` method to use `range` and `step` values (MR !141, !144).
  - `grainPlotWidget.py`: Fix typo when showing kurtosis maps (MR !145).
  - `rockingCurvesWidget.py`: Fix bug when computing peak position map and add residuals map (MR !145, !150).
  - `magnificationWidget.py`: Add center axes checkbox (MR !151).
- Orangecontrib (MR !147):
  - Add `flash.py` file that contains `FlashWidget`: widget to update previous datasets and free memory.
  - Update orange widgets to emit `self` together with the dataset to be able to update previous datasets.

## [0.6.1] - 2021-09-29

### Changed

- Downgrade pypushflow to 0.1.0 for compatibility issues (MR !137).
- Core (MR !137):
  - `dataset.py`:
    - Nica_nmf: Set 'init' as 'custom' when initializing NMF to use H and W absoulte values from NICA.
    - Change `cascade` to `waterfall`.
    - Mosaicity only computable in two dimensions.
    - `compute_transformation`: Flip axes if rotate is checked (MR !138).
    - Add `Transformation` class (MR !138).
  - `mapping.py` (MR !138):
    - Rsm: Convert to degrees and fix computation typo.
    - Magnification: Convert to radians before computing sin and cos and add topography option.
- Decomposition (MR !137):
  - `nica.py`: Add epsilon to avoid division by 0.
- GUI:
  - `blindSourceSeparationWidget.py`: Change NNICA to NICA (MR !137).
  - `shiftCorrectionWidget.py`: Convert 'shift' attribute to numpy array after setter (MR !137).
  - `magnificationWidget.py`: Add topography checkbox and orientation axis combobox (MR !138).
  - `grainPlotWidget.py` & `zSumWidget.py`: Rotate image 90 degrees in case of active rotation (rsm), and set label corresponding to the transformation type (if so) (MR !138).
- Orangecontrib (MR !137):
  - `shiftcorrection.py`: Fix bug when clearing stack and loading and saving shift.

## [0.6.0] - 2021-09-15

### Changed

- Core:
  - Dataset:
    - Save data into hdf5 instead of numpy files, all images are saved into a single hdf5 file (MR !128):
      - `Data` class methods `apply_funcs` and `save` are modified to work with h5py and to only replace the necessary rows of the file.
      - `DataUrls` used in `Dataset` are linked to the corresponding image (using data slicing of h5py).
      - Temporary datasets are used to not lose information in case of crash or abortion.
    - Raise error if directory for treated data is read-only (MR !114).
    - Use treated data directory for dark files (MR !114).
    - Add `roi_dir` parameter in `apply_roi` as directory path for the new dataset (MR !122).
    - New treated files in disk automatically replace previous ones except said by parameter (MR !123).
    - Add `get_metadata_value` method to obtain metadata info from a key (MR !124).
    - Add attribute `transformation` with the transformation values and method `compute_transformation` to compute it (MR !125).
    - Modify `find_shift` and `apply_shift` methods parameters to use `steps` instead of `h_step` and `h_max` and use linear shift when applying shifts greater than 1 (MR !127).
    - Add methods `find_shift_along_dimension` and `apply_shift_along_dimension` that find and apply shift, respectively, in a loop along a dimensions values (MR !134).
  - Mapping:
    - Apply median filter to COM and std to remove Nans (MR !117).
    - Add functions `compute_rsm` and `compute_magnification` (MR !125).
  - Image registration:
    - Modify shift detection to work with higher values of shift than 0.5 (MR !127).
  - Process (MR !130):
    - Add new process `_GrainPlot`.
    - Add new process `_Transformation`.
    - Add step and chunk properties in `_NoiseRemoval` process.
  - ROI:
    - Fix typo when computing 2D ROI (MR !130).
- GUI:
  - `grainPlotWidget.py`:
    - Orientation distribution: Increase resolution of hsv key, set coordinate labels as the angles of the motors, add checkbox to center angle values to 0 and fix bugs (MR !116).
    - Add export button that saves maps into Nexus file (MR !132).
    - Stop using opticolor (MR !117).
    - Modify axes if transformation is present and set global attributes origin and scale (MR !125).
  - `rockingCurvesWidget.py`:
    - Add two scatter points at the frame number position in the rocking curves (MR !119).
  - `noiseRemovalWidget.py`:
    - Fix bug when resetting data and applying new operations (MR !115).
    - Only show abort button if abortion is possible (MR !128).
    - Add step and chunks properties (MR !130).
  - `roiWidget.py`:
    - Return bg_dataset in `get_dataset` (MR !122).
    - Use same directory for consecutive roi applies (MR !122).
    - Only show abort button if abortion is possible (MR !128).
  - `displayComponentsWidget.py`: Set X values as motor positions when filtering by dimensions (MR !121).
  - `linkComponentsWidget.py`: Add colormap (orientation distribution maps) from the components (MR !126).
  - Add `rsmWidget.py` for Reciprocal Space Map 1D datasets (MR !124).
  - Add `magnificationWidget.py` for dataset with magnification values (MR !125).
  - `shiftCorrectionWidget.py`:
    - Add `ShiftCorrectionDialog` which includes `ShiftCorrectionWidget` as main widget (MR !127).
    - Add `_filtered_shift` attribute that contains the shift values, if any, along a dimension (MR !134).
    - Use methods for finding and applying shift along a dimension in `Dataset` (MR !134).
    - Modify checkbox to be used when shift should be applied to only selected value (MR !134).
    - Update values of vertical and horizontal shifts to show currently selected dimension value shift (MR !134).
  - Create `zSumWidget` to show plot of zsum (MR !131).
- Pffaddon: Add alias for `GrainPlotWidgetOW`, for `TransformationWidgetOW` (MR !130) and for `zSumWidgetOW` (MR !131).
- App: Modify `ows_to_script.py` executable script arguments for Dataset (MR !130).
- Orangecontrib:
  - Add `transformation.py` that shows either `magnificationWidget` or `RSMWidget` (MR !125, MR!133).
  - Add step and chunks Settings in `NoiseRemovalWidgetOW` (MR !130).
  - Add local in `shiftCorrectionWidgetOW` to avoid bugs depending on the local computers locale (MR !130).
  - Use `zSumWidget` in `ZSumWidgetOW` (MR !131).

## [0.5.0] - 2020-12-23

### Changed

- Add tqdm package to requirements.txt and setup.py.
- Core:
  - Dataset:
    - Update constructor to admit `first_filename` parameter. (MR !106).
    - Fix reshaping: Correct the methodology used for reshaping to be consistent with the way data is obtained in id06 (MR !101).
    - Modify methods that work with dimensions (get_data, apply_shift) so that they work if more than one dimension is fixed (MR !102).
    - Add `running_data` property which contains the data currently being used by any of the operations (if any). This data is stopped in case of `Abort` option called (MR !95).
    - Apply_background_subtraction:
      - Use multiprocessing to chunk images (MR !87).
      - Add step option to compute median using only every step image (MR !87).
      - Add tests with step and chunks and add docstring (MR !92).
    - Add `apply_moments` method for computing orientation distribution and colorkey based on the dimensions (for now only works with two dimensions) (MR !96).
    - Add `apply_fit` method for fitting the rocking curves of the data (a curve corresponds to a pixel around the stack), multiprocessing is used to chunk the images (MR !98).
    - Add `apply_threshold` method for thresholding the data (MR !108).
  - Create new file `dimension.py` that contains the classes AcquisitionDims and Dimensions moved from `dataset.py` (MR !105).
  - Create new file `mapping.py` with several functions: fit a rocking curve and computation of moments (MR !98).
  - `process.py`: Add new process `_RockingCurves` (MR !104).
  - Add `test_dimension.py` file that contains the tests that use the Dimension and AcquisitionDim classes (MR !105).
- GUI:
  - Add setters and getters for colormaps in widgets that use them (MR !110).
  - Disable buttons when computing operations (MR !109).
  - `datasetSelectionWidget.py` (MR !106).
    - Add new tab for treated data.
    - Create class `DirSelectionWidget`.
  - `noiseRemovalWidget.py`:
    - Add `setDataset` method in `NoiseRemovalDialog` to enable buttons after the dataset is set (MR !100).
    - Add widgets only visible when data in disk, which give option to use step or chunks when computing the median (MR !87, MR!90).
    - Fix bug when showing or not the in disk widget (MR !97).
    - Make methods `toggleChunks` and `toggleInDiskWidget` private (MR !100).
    - Correctly set and get properties (background, method, etc) (MR !104).
    - Add threshold removal option (MR !108).
    - Add signal that emits when method starts or ends computing (MR !109).
    - Fix some typos (MR !111).
  - `shiftCorrectionWidget.py`:
    - Use `skimage.registration.phase_correlation` instead of `register_translation` when finding shift (MR !91).
    - Fix bug when shifting only using first dimension (MR !99).
    - Round shift to 5 decimals (MR !105).
  - `roiSelectionWidget.py`:
    - Run ROI operation in thread and add abort button(MR !95).
  - `blindSourceSeparationWidget.py`:
    - Modify `Method` class so that its values are a description of the method. The keys are used in the `BlindSourceSeparationWidget` as text in the combobox, and the values are its tooltips (MR !100).
    - Remove widgets to set a maximum number of components (MR !105).
  - `pca.py` (MR !105):
    - Add title and labels to plot.
    - Automatically compute PCA when creating widget and remove widgets to set a maximum number of components.
  - `displayComponentsWidget.py`:
    - Add parameter in `setDimensions` to know the shape of the data, and use it to correctly take values from W (MR !107).
  - `ChooseDimensionWidget`: Add as many dimension widgets as dimensions are (minus 1), so all the dimensions are fixed except for one (MR !102).
  - Create `GrainPlotWidget`:
    - Show different COM, FWHM, Skewness, Kurtosis of the dataset around a certain dimension (MR !96).
    - Add a contours map to show the contours of the orientation distribution on top of the colorkey (MR !96).
    - Add a plot for the mosaicity map (only works with two dimensions) (MR !96).
  - Create `RockingCurvesWidget` (MR !98, MR !111, MR !112):
    - Show the stack of images where the user can click any pixel.
    - Show a 1D plot with the rocking curve of the pixel selected in the stack.
    - A ChooseDimensionWidget allows the data to be filtered by the chosen dimension.
    - A button to fit the data shows a plot with 3 maps computed from the fitted data: Integrated intensity, FWHM and peak position.
    - If data is filtered by dimensions then the data is fitted in chunks, where every chunk is a certain value of the chosen dimension.
  - Create `LineProfileWidget` (MR !103):
    - Upload a `*.npy` image from disk and show intensity curve from a chosen y value of the image.
  - Create `ShowStackWidget` to show stack of data (MR !106).
- Pffaddon: Add alias for rockingCurveWidget (MR !104).
- Orangecontrib:
  - Zsum: Use `ChooseDimensionDock` instead of `ChooseDimensionWidget` and fix bug when computing sum in disk (MR !92).
  - Add `GrainPlotWidgetOW` to show a `GrainPlotWidget` (MR !96).
  - Add `RockingCurvesWidgetOW` to show a `RockingCurvesWidget` (MR !98).
  - Add `LineProfileWidgetOW` for `LineProfileWidget` (MR !103).
  - Add properties in `NoiseRemovalWidgetOW` for threshold removal (MR !108).
  - Add colormap as input and output on widgets that use it (MR !110).

## [0.4.2] - 2020-09-15

### Fixed

- Use version 4.1.2.30 of opencv to avoid uncompatibility with PyQt5 latest release.

## [0.4.1] - 2020-09-14

### Changed

- Modify `setup.py` (MR !82):
  - Add `opencv-python`, `scikit-image` and `silx` in `install_requires`.
  - Add package `full` in `extras` with `matplotlib`, `PyQt5` and `orange`.
  - Add package `test` in `extras` with `pillow`.
- Core:
  - `dataset.py`:
    - Add parameter bins when partitioning data in `Dataset` (MR !67).
    - Create `in_memory` setter in `Dataset` (MR !68).
    - Improve methods `flatten`, `reshape` and `take` in `Data` (MR !67).
    - Add try-except when fitting data in blind source separation methods to close file in case of crash (MR !71).
    - Add methods to convert dimensions to dictionary and viceversa in `AcquisitionDims` (MR !74).
    - Add `to_memory` method in `Dataset` to load only part of the data into memory (MR !77).
    - Add property `ndim` in `Data` (MR !80).
- Decomposition:
  - Fix bug in IPCA with cases where in the last iteration the chunk was smaller than the number of components (omit last iteration) (MR !73).
- GUI:
  - Temporarily register resources directory in when used in `DisplayComponentsWidget` (MR !84).
  - Change colormap default normalization to `log` for better visualization of the data (MR !85).
  - Add widget for bins in `DataPartitionWidget` (MR !67).
  - Add parameter for chunks in `NoiseRemovalWidget` (MR !68).
  - Add abort options in `dataPartitionWidget`, `NoiseRemovalWidget` and `ShiftCorrectionWidget` (MR !68).
  - Get next free axis when removing dimensions in `DimensionsWidget` (MR !86).
  - Fix bug when clearing stack in `RoiSelectionWidget` (MR !67).
  - Fix bug when getting filtered indices in `DataPartitionWidget` (MR !68).
- IO:
  - New file `dataset_io.py` with functions to save and load data into/from json files (MR !74).
- Orangecontrib:
  - Remove progressBar due to bugs in the workflows (MR !84).
  - Fix bug with qthreads when creating and deleting the thread using orange widgets (MR !70).

## [0.4.0] - 2020-05-19

### Changed

- Refactors the project (MR !48).
  - Changes default colormap to cividis.
  - Core:
    - Dataset class stops inheriting from `silx.qt.QObject`.
    - The dataset class takes control of all the operations done to the data.
    - Metadata is obtained from the frames using `fabioh5` from silx and then each frame is closed to spare space in memory.
    - Creates new class `Data` that inherits from numpy.ndarray and contains the corresponding urls and metadata of the data.
    - Adds new methods to `Dataset` for image operations, image registration, region of interest, and partition by intensity (filter data), that are applied differently depending on if the data is loaded into memory or is taken from disk in chunks.
    - Data can be saved into an Hdf5 file with images in the rows.
    - Implement in `Data` methods `shape`, `reshape`, `flatten`, `take`, `__getitem__` that work similarly to a numpy.ndarray.
    - Adds and modifies functions in `imageOperations.py` and `imageRegistration.py` to be used when data is not loaded into memory.
    - Adds class `IPCA` in `blindSourceSeparation.py` that uses IncrementalPCA from scikit-learn to apply PCA in chunks.
    - Implements methods in `Dataset` to apply blind source separation algorithms to the data.
    - PCA and NMF algorithms used from scikit-learn when data is loaded into memory.
  - Decomposition:
    - A new package `decomposition` is created.
    - A base class `Base` is created for decomposition methods.
    - Adds class `NMF` that updates the matrices `H` and `W` using NMF method without having the data in memory.
    - Adds class `NICA` with the already implemented algorithm in `core`.
    - Adds class `PCA` currently not used (substitued for PCA in scikit-learn).
  - GUI:
    - Modifies all widgets to only have `Dataset` objects and call its corresponding methods.
- Core:
  - Adds method `in_memory` to Dataset to upload data from disk or remove data from memory (MR !51).
  - Adds method that returns intensity per frame (MR !58).
  - Number of bins can be passed as parameter when partitioning the data by intensity (MR !52).
  - Fix bugs when not closing Hdf5 files (MR !56).
  - Adds methos `zsum` in `Dataset` to sum images when not in memory (MR !57).
  - Fix bugs with `__getitem__` in `Data` (MR !57).
- Decomposition:
  - Adds IPCA to decomposition package (MR !50).
  - NICA implements IPCA for whitening when data is not in memory. Fix bugs when computing IPCA with data in the rows or in the columns (MR !53).
  - Allow matrices H and W in IPCA to be stored in disk using Hdf5 (MR !54).
- GUI:
  - Adds ComboBox in `DatasetSelectionWidget` to use data from disk or load it into memory (MR !57).
  - Adds widget to partition the data by intensity (MR !58).
  - Removes ComboBox in `DatasetSelectionWidget` to filter the data (MR !59).
- Orangecontrib:
  - Add corresponding data partition widget (MR !58).
  - Update example tutorial (MR !64).

## [0.3.0] - 2020-03-04

### Changed

- Adds resources package (MR !29).
- Adds configuration file for default parameters (MR !30).
- Minor fixes (MR !12 !14 !15 !32 !37 !41 !46).
- Use silx backend when available (MR !44).
- Core:
  - Adds tolerance to dimensions that defines the uniqueness of its values (MR !17).
  - Modifies ROI performance (MR !23).
  - Implements blind source separation algorithms (MR !18 !20 !22 !28).
  - Implements algorithms for linking components between datasets: ORB, SIFT, Euclidean distance (MR !36 !44 !45).
- GUI:
  - Creates a unified noise removal widget (MR !21 !24 !25).
  - Adds checkbox to filter the data in `DataSelectionWidget` (MR !19).
  - Improves `DimensionWidget` (MR !16 !17 !33).
  - Improves `roiSelectionWidget` (MR !23 !31 !43).
  - Implements widgets `blindSourceSeparationWidget` and `displayComponentsWidget` to display the components (MR !18 !22 !26 !29 !35).
  - Creates `PCAWidget` to show the eigenvalues of the PCA computation (MR !22).
  - Creates widget `LinkComponentsWidget` that implements the component matching algorithms from two sets of components (MR !36 !38).
- IO:
  - Creates functions for reading and writing the components of the BSS into Nexus files (MR !42).

## [0.2.0] - 2019-10-15

### Changed

- Renames project linkdick06 to darfix.
- Refactors project into core, gui, io and test packages.
- Adds unittests.
- Adds orangecontrib package.
- Adds examples package.
- Adds continous integration with gitlab-ci.
- Adds requirements.txt file with dependencies on numpy, silx, PyQt5, opencv-python, scikit-image.
  and orange3 with version 3.22.0
- Core:
  - Dataset class inherits from `silx.qt.QObject`.
  - Adds threshold to split data into high intensity images and low intensity images.
  - Adds `Dimension` class to save information about how the frames are taken through the dataset.
  - Adds roi file that implements region of interest functions.
  - Image registration operations moved to new file `imageRegistration.py`.
  - Adds shift detection using OpenCV.
  - Adds `autofocus.py` to use at the shift detection.
  - Adds `geneticShiftDetection` file to improve shift detection using a genetic algorithm.
- GUI:
  - Adds `RoiSelectionWidget`.
  - Adds `ShiftCorrectionWidget` to apply shift detection and shift correction.
  - Adds widgets `BackgroundSubstractionWidget` and `HotPixelRemovalWidget` for noise removal.
  - Adds widgets for data selection, metadata, and choosing dimensions.
  - Adds a `QThread`, `operationThread`, to run widgets operations in a thread.
  - Adds utils to create datasets from scratch.
  - Removes `frameInterpretationWidget` and adds `DimensionWidget`.
- IO:
  - Adds utils.

## [0.1.0] - 2019-07-15 [NO PYPI RELEASE]

### Added

- Adds project build, documentation and test structure.
- Adds continuous integration set-up for Gitlab.
- Adds EDF reader from Fabio.
- Adds operations for correction of images in imageOperations.
- Adds notebook tutorial.

[3.0.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v2.5.1...v3.0.0
[2.5.1]: https://gitlab.esrf.fr/XRD/darfix/compare/v2.5.0...v2.5.1
[2.5.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v2.4.0...v2.5.0
[2.4.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v2.3.1...v2.4.0
[2.3.1]: https://gitlab.esrf.fr/XRD/darfix/compare/v2.3.0...v2.3.1
[2.3.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v2.2.0...v2.3.0
[2.2.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v2.1.1...v2.2.0
[2.1.1]: https://gitlab.esrf.fr/XRD/darfix/compare/v2.1.0...v2.1.1
[2.1.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v2.0.0...v2.1.0
[2.0.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v1.0.2...v2.0.0
[1.0.2]: https://gitlab.esrf.fr/XRD/darfix/compare/v1.0.1...v1.0.2
[1.0.1]: https://gitlab.esrf.fr/XRD/darfix/compare/v1.0.0...v1.0.1
[1.0.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.10.0...v1.0.0
[0.10.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.9.8...v0.10.0
[0.9.8]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.9.7...v0.9.8
[0.9.7]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.9.6...v0.9.7
[0.9.6]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.9.5...v0.9.6
[0.9.5]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.9.4...v0.9.5
[0.9.4]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.9.3...v0.9.4
[0.9.3]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.9.2...v0.9.3
[0.9.2]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.9.1...v0.9.2
[0.9.1]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.9.0...v0.9.1
[0.9.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.8.0...v0.9.0
[0.8.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.7.3...v0.8.0
[0.7.3]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.7.2...v0.7.3
[0.7.2]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.7.0...v0.7.2
[0.7.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.6.1...v0.7.0
[0.6.1]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.6.0...v0.6.1
[0.6.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.5.0...v0.6.0
[0.5.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.4.2...v0.5.0
[0.4.2]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.4.1...v0.4.2
[0.4.1]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.4.0...v0.4.1
[0.4.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.3.0...v0.4.0
[0.3.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.2.0...v0.3.0
[0.2.0]: https://gitlab.esrf.fr/XRD/darfix/compare/v0.1...v0.2.0
[0.1.0]: https://gitlab.esrf.fr/XRD/darfix/-/tags/v0.1
