import math
from backend.metrics.mse import calculate_mse

def calculate_psnr(cover_image_path: str, stego_image_path: str) -> float:
    """
    Menghitung nilai Peak Signal-to-Noise Ratio (PSNR) antara cover image dan stego image.
    Semakin tinggi nilai PSNR, semakin baik kualitas stego image (semakin mirip dengan cover).
    Nilai kembalian dalam satuan dB (float).
    """
    mse_value = calculate_mse(cover_image_path, stego_image_path)
    
    # Jika tidak ada perbedaan (MSE = 0), PSNR bernilai tak hingga
    if mse_value == 0:
        return float('inf')
    
    max_pixel = 255.0
    psnr_value = 10 * math.log10((max_pixel ** 2) / mse_value)
    
    return float(psnr_value)

def check_psnr_threshold(psnr_value: float, threshold: float = 30.0) -> bool:
    """
    Memeriksa apakah nilai PSNR mencapai atau melebihi ambang batas yang ditentukan.
    Berdasarkan standar tugas, ambang batas minimal adalah 30 dB.
    Mengembalikan True jika memenuhi, False jika tidak.
    """
    return psnr_value >= threshold
