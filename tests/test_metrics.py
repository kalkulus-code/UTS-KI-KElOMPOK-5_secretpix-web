import unittest
import os
import numpy as np
from PIL import Image
from backend.metrics.mse import calculate_mse
from backend.metrics.psnr import calculate_psnr, check_psnr_threshold
from backend.metrics.histogram import generate_histogram_comparison
from backend.metrics.enhanced_lsb import visualize_enhanced_lsb

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

class TestMetricsPSNR(unittest.TestCase):
    def setUp(self):
        self.img1_path = "dummy_psnr_img1.png"
        self.img2_path = "dummy_psnr_img2.png"

        # Image 1 (Cover)
        img1_arr = np.zeros((10, 10, 3), dtype=np.uint8)
        Image.fromarray(img1_arr).save(self.img1_path)

        # Image 2 (Stego): Modifikasi kecil sehingga MSE tidak 0
        img2_arr = np.zeros((10, 10, 3), dtype=np.uint8)
        img2_arr[:, :, 0] = 1 
        Image.fromarray(img2_arr).save(self.img2_path)

    def tearDown(self):
        if os.path.exists(self.img1_path):
            os.remove(self.img1_path)
        if os.path.exists(self.img2_path):
            os.remove(self.img2_path)

    def test_calculate_psnr_identical(self):
        psnr = calculate_psnr(self.img1_path, self.img1_path)
        self.assertEqual(psnr, float('inf'))
        self.assertTrue(check_psnr_threshold(psnr))

    def test_calculate_psnr_difference(self):
        psnr = calculate_psnr(self.img1_path, self.img2_path)
        # MSE = 1/3, PSNR = 10 * log10(255^2 / (1/3)) = 10 * log10(65025 * 3) ~ 52.9 dB
        self.assertTrue(psnr > 50.0)
        self.assertTrue(check_psnr_threshold(psnr))

    def test_psnr_threshold_fails_when_too_much_noise(self):
        # Buat gambar dengan noise tinggi (MSE besar) sehingga PSNR < 30
        noisy_path = "noisy_img.png"
        noisy_arr = np.full((10, 10, 3), 100, dtype=np.uint8) # beda 100 per piksel
        Image.fromarray(noisy_arr).save(noisy_path)
        
        psnr = calculate_psnr(self.img1_path, noisy_path)
        self.assertFalse(check_psnr_threshold(psnr)) # harusnya return False krn kurang dari 30 dB
        
        if os.path.exists(noisy_path):
            os.remove(noisy_path)

class TestMetricsVisual(unittest.TestCase):
    def setUp(self):
        self.img1_path = "dummy_visual_cover.png"
        self.img2_path = "dummy_visual_stego.png"
        self.hist_out = "dummy_hist_out.png"
        self.lsb_out = "dummy_lsb_out.png"

        # Image Cover
        img1_arr = np.zeros((10, 10, 3), dtype=np.uint8)
        img1_arr[:, :, :] = 128
        Image.fromarray(img1_arr).save(self.img1_path)

        # Image Stego (LSB dirubah)
        img2_arr = np.copy(img1_arr)
        img2_arr[0:5, 0:5, 0] = 129 # Modif bit
        Image.fromarray(img2_arr).save(self.img2_path)

    def tearDown(self):
        for path in [self.img1_path, self.img2_path, self.hist_out, self.lsb_out]:
            if os.path.exists(path):
                os.remove(path)

    def test_generate_histogram(self):
        out_path = generate_histogram_comparison(self.img1_path, self.img2_path, self.hist_out)
        self.assertTrue(os.path.exists(out_path))

    def test_visualize_enhanced_lsb(self):
        out_path = visualize_enhanced_lsb(self.img2_path, self.lsb_out, bit_plane=0)
        self.assertTrue(os.path.exists(out_path))
        
        # Validasi bahwa ada piksel putih (255) yang dihasilkan dari LSB = 1
        img_out = Image.open(out_path)
        arr_out = np.array(img_out)
        self.assertTrue(np.any(arr_out == 255))
        self.assertTrue(np.any(arr_out == 0))

if __name__ == "__main__":
    unittest.main()
