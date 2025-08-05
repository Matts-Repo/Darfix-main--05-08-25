import copy
import os
import tempfile
import unittest
import uuid

import numpy

from darfix.tests import utils


class _BaseDatasetTest:
    """Tests for class Dataset in `dataset.py`"""

    def createRandomDataset(self, dims, nb_frames, metadata=False):
        raise NotImplementedError("Base class")

    def test_data_load(self):
        """Tests the correct load of the data"""
        self.assertEqual(len(self.dataset.get_data()), 3)
        self.assertEqual(self.dataset.nframes, 3)

    def test_nframes(self):
        """Tests the nframes method"""
        self.assertEqual(self.dataset.nframes, 3)

    def test_deepcopy(self):
        """Tests the correct deepcopy of the object"""
        dataset_copy = copy.deepcopy(self.dataset)
        self.assertEqual(self.dataset.nframes, dataset_copy.nframes)
        self.assertEqual(self.dataset.data.shape, dataset_copy.data.shape)

    def test_zsum(self):
        zsum = self.dataset.zsum()
        self.assertEqual(zsum.shape, (100, 100))

        result = numpy.sum(self.dataset.get_data(), axis=0)
        numpy.testing.assert_array_equal(zsum, result)

        indices = [0, 1]
        zsum = self.dataset.zsum(indices)
        result = numpy.sum(self.dataset.get_data(indices), axis=0)
        numpy.testing.assert_array_equal(zsum, result)

    def test_filter_data(self):
        """Tests the correct separation of empty frames and data frames"""
        dims = (10, 100, 100)
        data = numpy.zeros(dims)
        background = numpy.random.random(dims)
        idxs = [0, 2, 4]
        data[idxs] += background[idxs]
        dataset = utils.createDataset(data=data, _dir=self._dir)
        used_idx, not_used_idx = dataset.partition_by_intensity(bottom_bin=1)
        self.assertEqual(used_idx.shape[0], 3)
        self.assertEqual(not_used_idx.shape[0], 7)

    def test_bs(self):
        """Tests the background subtraction function with data in memory"""
        indices = [0, 1]
        bs_dataset = self.dataset.apply_background_subtraction(
            background=[2], indices=indices
        )

        self.assertEqual(bs_dataset.nframes, self.dataset.nframes)
        self.assertNotEqual(bs_dataset.data.urls[0], self.dataset.data.urls[0])
        numpy.testing.assert_equal(self.dataset.data.metadata, bs_dataset.data.metadata)
        numpy.testing.assert_equal(self.dataset.data[2], bs_dataset.data[2])

    def test_hp(self):
        """Tests the hot pixel removal function with data in memory"""
        indices = [0, 1]
        hp_dataset = self.dataset.apply_hot_pixel_removal(indices=indices)

        self.assertEqual(hp_dataset.nframes, self.dataset.nframes)
        self.assertNotEqual(hp_dataset.data.urls[0], self.dataset.data.urls[0])
        numpy.testing.assert_equal(self.dataset.data.metadata, hp_dataset.data.metadata)
        numpy.testing.assert_equal(self.dataset.data[2], hp_dataset.data[2])

    def test_threshold(self):
        """Tests the threshold removal function with data in memory"""
        indices = [0, 1]
        threshold_dataset = self.dataset.apply_threshold_removal(indices=indices)

        self.assertEqual(threshold_dataset.nframes, self.dataset.nframes)
        self.assertNotEqual(threshold_dataset.data.urls[0], self.dataset.data.urls[0])
        numpy.testing.assert_equal(
            self.dataset.data.metadata, threshold_dataset.data.metadata
        )
        numpy.testing.assert_equal(self.dataset.data[2], threshold_dataset.data[2])

    def test_roi(self):
        """Tests the roi function with data in memory"""
        new_dataset = self.dataset.apply_roi(origin=[0, 0], size=[20, 20])
        self.assertEqual(new_dataset.nframes, 3)
        numpy.testing.assert_equal(self.dataset.data[:, :20, :20], new_dataset.data)

    def test_roi_bs(self):
        """Tests the background subtraction function with data on disk"""

        roi_dataset = self.dataset.apply_roi(origin=[0, 0], size=[20, 20])
        indices = [0, 1]
        bs_dataset = roi_dataset.apply_background_subtraction(
            background=[2], indices=indices
        )

        self.assertEqual(bs_dataset.nframes, self.dataset.nframes)
        self.assertNotEqual(self.dataset.data.urls[0], bs_dataset.data.urls[0])
        numpy.testing.assert_equal(bs_dataset.data[2], roi_dataset.data[2])

    def test_roi_hp(self):
        """Tests the background subtraction function with data on disk"""

        roi_dataset = self.dataset.apply_roi(origin=[0, 0], size=[20, 20])
        indices = [0, 1]
        hp_dataset = roi_dataset.apply_hot_pixel_removal(indices=indices)

        self.assertEqual(hp_dataset.nframes, self.dataset.nframes)
        self.assertNotEqual(hp_dataset.data.urls[0], self.dataset.data.urls[0])
        numpy.testing.assert_equal(self.dataset.data.metadata, hp_dataset.data.metadata)
        numpy.testing.assert_equal(roi_dataset.data[2], hp_dataset.data[2])

    def test_roi_threshold(self):
        """Tests the threshold removal function with data in memory"""
        roi_dataset = self.dataset.apply_roi(origin=[0, 0], size=[20, 20])
        indices = [0, 1]
        threshold_dataset = roi_dataset.apply_threshold_removal(indices=indices)

        self.assertEqual(threshold_dataset.nframes, self.dataset.nframes)
        self.assertNotEqual(threshold_dataset.data.urls[0], self.dataset.data.urls[0])
        numpy.testing.assert_equal(
            self.dataset.data.metadata, threshold_dataset.data.metadata
        )
        numpy.testing.assert_equal(roi_dataset.data[2], threshold_dataset.data[2])

    def test_find_shift(self):
        """Tests the shift detection"""
        shift = self.dataset.find_shift()

        self.assertEqual(shift.shape, (2, 3))

        shift = self.dataset.find_shift(indices=[0, 1])

        self.assertEqual(shift.shape, (2, 2))

    def test_apply_shift(self):
        """Tests the shift correction"""

        new_dataset = self.dataset.apply_shift(
            shift=numpy.array([[0, 0.5, 1], [0, 0.5, 1]])
        )

        self.assertEqual(new_dataset.nframes, self.dataset.nframes)
        self.assertNotEqual(new_dataset.data.urls[0], self.dataset.data.urls[0])

    def test_pca(self):
        """Tests PCA with data in memory"""

        H, W = self.dataset.pca()

        self.assertEqual(
            H.shape, (self.dataset.nframes, len(self.dataset.data[0].flatten()))
        )
        self.assertEqual(W.shape, (self.dataset.nframes, self.dataset.nframes))

        n_components = 1
        indices = [1, 2]
        H, W = self.dataset.pca(num_components=n_components, indices=indices)

        self.assertEqual(H.shape, (n_components, len(self.dataset.data[0].flatten())))
        self.assertEqual(W.shape, (2, n_components))

    def test_nmf(self):
        """Tests NMF with data in memory"""

        num_components = 2
        H, W = self.dataset.nmf(num_components)

        self.assertEqual(H.shape, (num_components, len(self.dataset.data[0].flatten())))
        self.assertEqual(W.shape, (self.dataset.nframes, num_components))

        num_components = 1
        indices = [1, 2]
        H, W = self.dataset.nmf(num_components=num_components, indices=indices)

        self.assertEqual(H.shape, (num_components, len(self.dataset.data[0].flatten())))
        self.assertEqual(W.shape, (2, num_components))

    def test_nica(self):
        """Tests NICA with data in memory"""

        num_components = 2
        H, W = self.dataset.nica(num_components)

        self.assertEqual(H.shape, (num_components, len(self.dataset.data[0].flatten())))
        self.assertEqual(W.shape, (self.dataset.nframes, num_components))

        num_components = 1
        indices = [1, 2]
        H, W = self.dataset.nica(num_components=num_components, indices=indices)

        self.assertEqual(H.shape, (num_components, len(self.dataset.data[0].flatten())))
        self.assertEqual(W.shape, (2, num_components))

    def test_recover_weak_beam(self):
        """Tests the recover weak beam function with data in memory
        Consider that threshold removal is already well tested"""
        indices = [0, 1]
        weak_beam_dataset = self.dataset.recover_weak_beam(n=0.5, indices=indices)

        self.assertEqual(weak_beam_dataset.nframes, self.dataset.nframes)
        self.assertNotEqual(weak_beam_dataset.data.urls[0], self.dataset.data.urls[0])
        numpy.testing.assert_equal(
            self.dataset.data.metadata, weak_beam_dataset.data.metadata
        )
        numpy.testing.assert_equal(weak_beam_dataset.data[2], weak_beam_dataset.data[2])


class TestHDF5Dataset(_BaseDatasetTest, unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.mkdtemp()
        output_file = os.path.join(self._dir, str(uuid.uuid1()) + ".hdf5")
        self.dataset = utils.createRandomHDF5Dataset(
            dims=(100, 100), nb_data_frames=3, metadata=True, output_file=output_file
        )

    def createRandomDataset(self, dims, nb_frames, metadata=False):
        return utils.createRandomHDF5Dataset(
            dims=dims, nb_data_frames=nb_frames, metadata=metadata
        )


def test_reshaped_data(dataset):
    """Tests the correct reshaping of the data"""

    dataset.find_dimensions()
    dataset = dataset.reshape_data()
    assert dataset.data.shape == (2, 2, 5, 100, 100)


def test_data_reshaped_data(dataset):
    """Tests that data and reshaped data have same values"""

    dataset.find_dimensions()
    dataset = dataset.reshape_data()
    numpy.testing.assert_array_equal(dataset.get_data(0), dataset.get_data(0))


if __name__ == "__main__":
    unittest.main()
