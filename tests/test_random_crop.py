import unittest
import torch
from torch_audiomentations.augmentations.random_crop import RandomCrop
torch_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class TestRandomCrop(unittest.TestCase):
    
    def testcrop(self):
        samples =  torch.rand(size=(8, 2, 32000), dtype=torch.float32, device=torch_device) - 0.5
        sampling_rate = 16000
        crop_to = 1.5
        desired_samples_len = sampling_rate*crop_to 
        Crop = RandomCrop(seconds=crop_to,sampling_rate=sampling_rate)
        cropped_samples = Crop(samples)
        
        self.assertEqual(desired_samples_len, cropped_samples.size(-1))

        





