shift correction
================

.. image:: icons/shift_correction.png

The consecutive images might show a displacement of the object of study that does not correspond to reality. This
displacement is here identified as shift and can be detected.

This can be done either simultaneously along all the dataset, or individually for each motor.

This last case is activated when clicking the **Filter by dimension** option. With this option active,
the **Find shift** button loops through the values of the selected dimension and finds, for
each value, the linear shift of the images for that motor value (which are the ones displayed). It not only finds the shift for the selected
value but for **all** values of that dimension.

After the shift is found, you can move through the values and see the different found shifts. After that clicking **Apply shift** will apply all
the shifts found to the corresponding images (although clicking Apply only to selected
values, which only applies the shift to the images you see on the plot).

Signals
-------

- Dataset

**Outputs**:

- Dataset

Description
-----------

TODO