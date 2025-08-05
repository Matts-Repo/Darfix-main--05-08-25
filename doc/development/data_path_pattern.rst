Data path pattern
"""""""""""""""""

Users can define HDF5 data path from patterns.
Patterns can contains one or several keyword that will be resolved automatically.

Existing keywords are:

* `{detector}`: if provided then a detector dataset (or group) will be search from the upstream path.
    * constraint: must be at the end of the pattern
    * use cases: scan concatenation and HDF5 scan selection
* `{scan}`: 'wildcard' for first entry of a HDF5 file.
    * constraint: must be at the beginning of the pattern
* `{first_scan}`: pick the first entry of a HDF5 file
    * constraint: must be at the beginning of the pattern
    * note: was not sure if this is a good idea / helping the user. Anyway this is cost-less to have. If unused we will remove it.
* `{last_scan}`: pick the last entry of a HDF5 file
    * constraint: must be at the beginning of the pattern
    * note: was not sure if this is a good idea / helping the user. Anyway this is cost-less to have. If unused we will remove it.
