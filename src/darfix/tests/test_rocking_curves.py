import numpy
import pytest

from darfix.core import rocking_curves
from darfix.core.utils import NoDimensionsError
from darfix.processing.rocking_curves import fit_1d_rocking_curve

from .utils import createHDF5Dataset2D


def test_generator():
    """Tests the correct creation of a generator without moments"""
    data = numpy.random.random(size=(3, 10, 10))
    g = rocking_curves.generator(data)

    img, moment = next(g)
    assert moment is None
    numpy.testing.assert_array_equal(img, data[:, 0, 0])


def test_generator_with_moments():
    """Tests the correct creation of a generator with moments"""
    data = numpy.random.random(size=(3, 10, 10))
    moments = numpy.ones((3, 10, 10))
    g = rocking_curves.generator(data, moments)

    img, moment = next(g)
    numpy.testing.assert_array_equal(moment, moments[:, 0, 0])
    numpy.testing.assert_array_equal(img, data[:, 0, 0])


def test_fit_rocking_curve():
    """Tests the correct fit of a rocking curve"""

    samples = numpy.random.normal(size=10000) + numpy.random.random(10000)

    y, bins = numpy.histogram(samples, bins=100)

    y_pred, pars = fit_1d_rocking_curve((y, None))
    rss = numpy.sum((y - y_pred) ** 2)
    tss = numpy.sum((y - y.mean()) ** 2)
    r2 = 1 - rss / tss

    assert r2 > 0.9
    assert len(pars) == 4


def test_fit_1d_data():
    """Tests the new data has same shape as initial data"""
    data = numpy.random.random(size=(3, 10, 10))
    new_data, maps = rocking_curves.fit_1d_data(data)

    assert new_data.shape == data.shape
    assert len(maps) == 4
    assert maps[0].shape == data[0].shape


def test_apply_fit_on_2d_dataset():
    data = numpy.random.randint(2, 1000, size=1500).reshape((3, 5, 10, 10))
    dataset = createHDF5Dataset2D(data)
    with pytest.raises(NoDimensionsError):
        fit_dataset, maps = dataset.apply_fit()
    dataset.find_dimensions()
    indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    fit_dataset, maps = dataset.apply_fit(indices=indices)

    assert dataset.dims.ndim == 2
    assert len(maps) == 7
    assert fit_dataset.nframes == dataset.nframes
    assert fit_dataset.data.urls[0] != dataset.data.urls[0]
    numpy.testing.assert_equal(fit_dataset.data[10], dataset.data[10])
