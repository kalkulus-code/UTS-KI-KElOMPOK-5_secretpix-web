import unittest
import os
import numpy as np
from PIL import Image
from backend.metrics.mse import calculate_mse

class TestMetricsMSE(unittest.TestCase):
    def setUp(self):
        # Buat gambar dummy untuk test
        self.img1_path = "dummy_img1.png"
        self.img2_path = "dummy_img2.png"
        self.img3_diff_size_path = "dummy_img3.png"

        # Image 1 (Cover): 10x10, all black (0,0,0)
        img1_arr = np.zeros((10, 10, 3), dtype=np.uint8)
        Image.fromarray(img1_arr).save(self.img1_path)

        # Image 2 (Stego): 10x10, with LSB modified (e.g. all pixels has R=1 instead of 0)
        # diff = 1 per pixel in R channel. Squared diff = 1
        # Mean diff per pixel = (1^2 + 0^2 + 0^2) / 3 = 1/3 ~ 0.333333
        img2_arr = np.zeros((10, 10, 3), dtype=np.uint8)
        img2_arr[:, :, 0] = 1 
        Image.fromarray(img2_arr).save(self.img2_path)

        # Image 3: 5x5 (Different size)
        img3_arr = np.zeros((5, 5, 3), dtype=np.uint8)
        Image.fromarray(img3_arr).save(self.img3_diff_size_path)

    def tearDown(self):
        if os.path.exists(self.img1_path):
            os.remove(self.img1_path)
        if os.path.exists(self.img2_path):
            os.remove(self.img2_path)
        if os.path.exists(self.img3_diff_size_path):
            os.remove(self.img3_diff_size_path)

    def test_calculate_mse_identical(self):
        mse = calculate_mse(self.img1_path, self.img1_path)
        self.assertEqual(mse, 0.0)

    def test_calculate_mse_difference(self):
        mse = calculate_mse(self.img1_path, self.img2_path)
        # Expect MSE = 1/3 (0.33333333...)
        self.assertAlmostEqual(mse, 1/3, places=5)

    def test_calculate_mse_different_size(self):
        with self.assertRaises(ValueError) as context:
            calculate_mse(self.img1_path, self.img3_diff_size_path)
        self.assertIn("Dimensi gambar cover dan stego tidak sama", str(context.exception))

    def test_calculate_mse_file_not_found(self):
        with self.assertRaises(ValueError):
            calculate_mse("not_exist.png", self.img1_path)

if __name__ == "__main__":
    unittest.main()
