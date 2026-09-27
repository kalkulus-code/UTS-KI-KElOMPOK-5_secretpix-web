import unittest
from backend.crypto.encryption import encrypt_message, decrypt_message

class TestCryptoEncryption(unittest.TestCase):
    def test_aes_encrypt_decrypt_success(self):
        pesan = "Ini pesan super rahasia untuk UTS Kriptografi!"
        kunci = "KunciSangatKuat123!#"
        
        encrypted = encrypt_message(pesan, kunci, algorithm="aes")
        self.assertIsInstance(encrypted, bytes)
        self.assertTrue(encrypted.startswith(b"AES:"))
        
        decrypted = decrypt_message(encrypted, kunci)
        self.assertEqual(decrypted, pesan)

    def test_xor_encrypt_decrypt_success(self):
        pesan = "Pesan rahasia dengan XOR cipher"
        kunci = "kuncixor123"
        
        encrypted = encrypt_message(pesan, kunci, algorithm="xor")
        self.assertIsInstance(encrypted, bytes)
        self.assertTrue(encrypted.startswith(b"XOR:"))
        
        decrypted = decrypt_message(encrypted, kunci)
        self.assertEqual(decrypted, pesan)

    def test_aes_wrong_key_fails(self):
        pesan = "Data rahasia bank"
        kunci_benar = "password123"
        kunci_salah = "passwordSalah"
        
        encrypted = encrypt_message(pesan, kunci_benar, algorithm="aes")
        with self.assertRaises(ValueError) as ctx:
            decrypt_message(encrypted, kunci_salah)
        self.assertIn("Dekripsi gagal", str(ctx.exception))

    def test_xor_wrong_key_different_output_or_error(self):
        pesan = "Pesan uji kunci XOR"
        kunci_benar = "keyBenar"
        kunci_salah = "keySalah"
        
        encrypted = encrypt_message(pesan, kunci_benar, algorithm="xor")
        try:
            decrypted = decrypt_message(encrypted, kunci_salah)
            self.assertNotEqual(decrypted, pesan)
        except ValueError:
            pass

    def test_empty_key_rejected(self):
        with self.assertRaises(ValueError):
            encrypt_message("Halo", "")
        with self.assertRaises(ValueError):
            decrypt_message(b"AES:dummy", "")

    def test_unicode_and_emojis(self):
        pesan = "Halo dunia! 🔒 SecretPix 🚀 12345 !@#$%^&*()_+ selamat siang"
        kunci = "kunciUnicode🔑"
        
        encrypted = encrypt_message(pesan, kunci, algorithm="aes")
        self.assertEqual(decrypt_message(encrypted, kunci), pesan)

if __name__ == "__main__":
    unittest.main()
