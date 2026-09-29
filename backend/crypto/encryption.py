import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes


def _derive_key_aes(key: str, salt: bytes) -> bytes:
    """
    Menurunkan kunci 256-bit (32 bytes) dari passphrase teks menggunakan PBKDF2-HMAC-SHA256.
    """
    return hashlib.pbkdf2_hmac("sha256", key.encode("utf-8"), salt, 100_000, dklen=32)


def encrypt_message(plaintext: str, key: str, algorithm: str = "aes") -> bytes:
    """
    Enkripsi plaintext menggunakan key.
    
    Format output bytes untuk AES-GCM:
      b"AES:GCM:" + salt (16 bytes) + nonce (12 bytes) + tag (16 bytes) + ciphertext

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
        nonce = get_random_bytes(12)
        aes_key = _derive_key_aes(key, salt)
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(plain_bytes)
        return b"AES:GCM:" + salt + nonce + tag + ciphertext

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

    if encrypted_data.startswith(b"AES:GCM:"):
        payload = encrypted_data[len(b"AES:GCM:"):]
        # 16 bytes salt + 12 bytes nonce + 16 bytes tag
        if len(payload) < 44:
            raise ValueError("Data terenkripsi rusak atau format AES-GCM tidak lengkap.")

        salt = payload[:16]
        nonce = payload[16:28]
        tag = payload[28:44]
        ciphertext = payload[44:]

        aes_key = _derive_key_aes(key, salt)
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        try:
            plaintext_bytes = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext_bytes.decode("utf-8")
        except Exception as exc:
            raise ValueError("Dekripsi gagal: Kunci salah atau data korup.") from exc

    elif encrypted_data.startswith(b"AES:"):
        # Format AES-CBC lama tetap didukung agar stego image yang sudah dibuat
        # sebelum migrasi ini masih dapat diekstraksi.
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
