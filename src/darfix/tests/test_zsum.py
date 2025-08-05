import numpy


def test_zsum(dataset):
    indices = [1, 2, 3, 6]

    dataset.find_dimensions()
    dataset = dataset.reshape_data()
    result = numpy.sum(dataset.get_data(dimension=[0, 1], indices=indices), axis=0)
    zsum = dataset.zsum(dimension=[0, 1], indices=indices)
    numpy.testing.assert_array_equal(zsum, result)
