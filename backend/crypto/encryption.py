import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def _derive_key_aes(key: str, salt: bytes) -> bytes:
    """
    Menurunkan kunci 256-bit (32 bytes) dari passphrase teks menggunakan PBKDF2-HMAC-SHA256.
    """
    return hashlib.pbkdf2_hmac("sha256", key.encode("utf-8"), salt, 100_000, dklen=32)


def encrypt_message(plaintext: str, key: str, algorithm: str = "aes") -> bytes:
    """
    Enkripsi plaintext menggunakan key.
    
    Format output bytes untuk AES:
      b"AES:" + salt (16 bytes) + iv (16 bytes) + ciphertext

    Format output bytes untuk XOR:
      b"XOR:" + ciphertext
    """
    if not isinstance(plaintext, str):
        raise TypeError("Plaintext harus bertipe string.")
    if not key:
        raise ValueError("Kunci enkripsi tidak boleh kosong.")

    plain_bytes = plaintext.encode("utf-8")

    if algorithm.lower() == "aes":
        salt = get_random_bytes(16)
        iv = get_random_bytes(16)
        aes_key = _derive_key_aes(key, salt)
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        padded_data = pad(plain_bytes, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        return b"AES:" + salt + iv + ciphertext

    elif algorithm.lower() == "xor":
        # XOR cipher dengan key-stream SHA-256 berulang
        key_bytes = key.encode("utf-8")
        stream = hashlib.sha256(key_bytes).digest()
        cipher_bytes = bytearray()
        for idx, byte_val in enumerate(plain_bytes):
            key_byte = stream[idx % len(stream)]
            cipher_bytes.append(byte_val ^ key_byte)
        return b"XOR:" + bytes(cipher_bytes)

    else:
        raise ValueError(f"Algoritma tidak dikenal: {algorithm}. Pilih 'aes' atau 'xor'.")


def decrypt_message(encrypted_data: bytes, key: str) -> str:
    """
    Mendekripsi data bytes hasil enkripsi kembali ke string plaintext.
    Mendeteksi otomatis format (AES atau XOR) berdasarkan prefix.
    """
    if not isinstance(encrypted_data, (bytes, bytearray)):
        raise TypeError("Encrypted data harus berupa bytes/bytearray.")
    if not key:
        raise ValueError("Kunci dekripsi tidak boleh kosong.")

    if encrypted_data.startswith(b"AES:"):
        payload = encrypted_data[4:]
        if len(payload) < 32:  # minimal 16 bytes salt + 16 bytes IV
            raise ValueError("Data terenkripsi rusak atau format AES tidak lengkap.")
        salt = payload[:16]
        iv = payload[16:32]
        ciphertext = payload[32:]
        if len(ciphertext) == 0 or len(ciphertext) % 16 != 0:
            raise ValueError("Panjang ciphertext AES tidak valid.")

        aes_key = _derive_key_aes(key, salt)
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        try:
            decrypted_padded = cipher.decrypt(ciphertext)
            plaintext_bytes = unpad(decrypted_padded, AES.block_size)
            return plaintext_bytes.decode("utf-8")
        except Exception as exc:
            raise ValueError("Dekripsi gagal: Kunci salah atau data korup.") from exc

    elif encrypted_data.startswith(b"XOR:"):
        ciphertext = encrypted_data[4:]
        key_bytes = key.encode("utf-8")
        stream = hashlib.sha256(key_bytes).digest()
        plain_bytes = bytearray()
        for idx, byte_val in enumerate(ciphertext):
            key_byte = stream[idx % len(stream)]
            plain_bytes.append(byte_val ^ key_byte)
        try:
            return plain_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Dekripsi gagal: Kunci salah atau data bukan UTF-8 valid.") from exc

    else:
        # Fallback kompatibilitas: bila input berupa plain string atau data tanpa prefix
        raise ValueError("Format data terenkripsi tidak dikenali (harus diawali AES: atau XOR:).")
