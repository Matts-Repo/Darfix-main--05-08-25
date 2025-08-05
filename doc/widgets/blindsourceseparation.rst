blind source separation
=======================

.. image:: icons/bss.png

Blind source separation (BSS) comprises all techniques that try to decouple a set of
source signals from a set of mixed signals with unknown (or very little) information.
darfix includes some BSS techniques to try to find the different grains along the dataset.

But first, the number of components has to be estimated, it can either be done
automatically by clicking the **Detect number of components** button, or using the PCA
widget.

This widget uses the technique of principal components analysis to find the singular
values with more intensity:

.. image:: img/introduction/bss.png

.. note::
    
    in this example we would take 4 or 5 components.

When automatically detecting the number of components, darfix uses the same
technique with PCA, and takes the components that represent the 99% of the dataset.

The **Blind source separation** widget includes different techniques to find the
components: Principal components analysis (PCA), non-negative independent
component analysis (NICA) and non-negative matrix factorization (NMF).

Although the first one is available for use, it is not recommended since PCA doesn’t take into account
the positivity of the images, and doesn’t give good results.

NICA, although returning positive components, can give negative value at the weight values, and is usually also
discarded. NMF on the other hand gives positive values for both components and
weights, but as the decomposition matrices are randomly initialized, the result is
non-unique.

To solve this last problem, we have a fourth method: NICA+NMF that uses
the output of NICA as input for NMF. The final result is unique and is preferable to NMF
alone, although it is a bit slower.

.. image:: img/introduction/bss_nica.png

Once computed, the components can be seen on the left plot, while on the right we have
different plots of the weights values.

At the right of the widget we can choose to either see the weights in terms of rocking curves,
or see them in terms of an RSM map (like in the figure).
Either way, these plots serve useful to see how each component is present in the dataset.

For the RSM, changing the component on the left changes its RSM map on the right.

After the analysis is done, you can save the components into an hdf5 file by clicking at
the **Save components** button.



Signals
-------

- Dataset

**Outputs**:

- Dataset

Description
-----------

TODO