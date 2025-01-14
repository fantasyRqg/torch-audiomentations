import unittest
import numpy as np
import torch
import pytest

from torch_audiomentations.augmentations.spliceout import SpliceOut
from torch_audiomentations import Compose


class TestSpliceout(unittest.TestCase):
    def test_spliceout(self):

        audio_samples = torch.rand(size=(8, 1, 32000), dtype=torch.float32)
        augment = Compose(
            [
                SpliceOut(num_time_intervals=10, max_width=400, output_type="dict"),
            ],
            output_type="dict",
        )
        spliceout_samples = augment(
            samples=audio_samples, sample_rate=16000
        ).samples.numpy()

        assert spliceout_samples.dtype == np.float32

    def test_spliceout_odd_hann(self):

        audio_samples = torch.rand(size=(8, 1, 32000), dtype=torch.float32)
        augment = Compose(
            [
                SpliceOut(num_time_intervals=10, max_width=400, output_type="dict"),
            ],
            output_type="dict",
        )
        spliceout_samples = augment(
            samples=audio_samples, sample_rate=16100
        ).samples.numpy()

        assert spliceout_samples.dtype == np.float32

    def test_spliceout_perbatch(self):

        audio_samples = torch.rand(size=(8, 1, 32000), dtype=torch.float32)
        augment = Compose(
            [
                SpliceOut(
                    num_time_intervals=10,
                    max_width=400,
                    mode="per_batch",
                    p=1.0,
                    output_type="dict",
                ),
            ],
            output_type="dict",
        )
        spliceout_samples = augment(
            samples=audio_samples, sample_rate=16000
        ).samples.numpy()

        assert spliceout_samples.dtype == np.float32
        self.assertLess(spliceout_samples.sum(), audio_samples.numpy().sum())
        self.assertEqual(spliceout_samples.shape, audio_samples.shape)

    def test_spliceout_multichannel(self):

        audio_samples = torch.rand(size=(8, 2, 32000), dtype=torch.float32)
        augment = Compose(
            [
                SpliceOut(num_time_intervals=10, max_width=400, output_type="dict"),
            ],
            output_type="dict",
        )
        spliceout_samples = augment(
            samples=audio_samples, sample_rate=16000
        ).samples.numpy()

        assert spliceout_samples.dtype == np.float32
        self.assertLess(spliceout_samples.sum(), audio_samples.numpy().sum())
        self.assertEqual(spliceout_samples.shape, audio_samples.shape)

    @pytest.mark.skipif(not torch.cuda.is_available(), reason="Requires CUDA")
    def test_spliceout_cuda(self):

        audio_samples = (
            torch.rand(
                size=(8, 1, 32000), dtype=torch.float32, device=torch.device("cuda")
            )
            - 0.5
        )
        augment = Compose(
            [
                SpliceOut(num_time_intervals=10, max_width=400, output_type="dict"),
            ],
            output_type="dict",
        )
        spliceout_samples = (
            augment(samples=audio_samples, sample_rate=16000).samples.cpu().numpy()
        )

        assert spliceout_samples.dtype == np.float32
        self.assertLess(spliceout_samples.sum(), audio_samples.cpu().numpy().sum())
