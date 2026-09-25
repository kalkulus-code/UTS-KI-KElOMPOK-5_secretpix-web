import random
import hashlib

def get_shuffled_pixel_indices(stego_key, total_pixels):
    """
    Menghasilkan urutan indeks piksel yang diacak berdasarkan stego-key.
    Menggunakan random.shuffle agar urutannya deterministik untuk kunci yang sama.
    """
    hash_obj = hashlib.sha256(stego_key.encode('utf-8'))
    seed_int = int(hash_obj.hexdigest(), 16)
    rng = random.Random(seed_int)
    
    indices = list(range(total_pixels))
    rng.shuffle(indices)
    return indices
