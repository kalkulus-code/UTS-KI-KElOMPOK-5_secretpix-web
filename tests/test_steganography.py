import unittest
import os
import shutil
import tempfile
from PIL import Image
from backend.steganography.lsb import sisipkan_lsb, ekstrak_lsb

class TestSteganographyIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.cover_path = os.path.join(self.test_dir, "cover.png")
        self.stego_path = os.path.join(self.test_dir, "stego.png")
        
        # Buat dummy image 100x100 RGB
        img = Image.new("RGB", (100, 100), color=(128, 128, 128))
        img.save(self.cover_path, format="PNG")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_embed_and_extract_with_aes(self):
        secret_text = "Secret message test with AES-256 encryption!"
        key = "SuperStegoKey2026"
        
        sisipkan_lsb(self.cover_path, self.stego_path, secret_text, key, encrypt=True, crypto_algo="aes")
        extracted = ekstrak_lsb(self.stego_path, key, decrypt=True)
        self.assertEqual(extracted, secret_text)

    def test_embed_and_extract_with_xor(self):
        secret_text = "Secret message test with XOR encryption!"
        key = "StegoXorKey123"
        
        sisipkan_lsb(self.cover_path, self.stego_path, secret_text, key, encrypt=True, crypto_algo="xor")
        extracted = ekstrak_lsb(self.stego_path, key, decrypt=True)
        self.assertEqual(extracted, secret_text)

    def test_extract_with_wrong_key_fails(self):
        secret_text = "Sensitive cryptographic data"
        correct_key = "correctKey99"
        wrong_key = "wrongKey00"
        
        sisipkan_lsb(self.cover_path, self.stego_path, secret_text, correct_key, encrypt=True)
        extracted = ekstrak_lsb(self.stego_path, wrong_key, decrypt=True)
        self.assertTrue(extracted.startswith("Error"))

if __name__ == "__main__":
    unittest.main()
