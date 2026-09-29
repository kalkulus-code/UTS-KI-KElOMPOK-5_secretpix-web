import numpy as np
from PIL import Image

def calculate_mse(cover_image_path: str, stego_image_path: str) -> float:
    """
    Menghitung Mean Squared Error (MSE) antara dua gambar.
    Mengembalikan nilai MSE (float). Jika citra identik, MSE = 0.0.
    Kedua gambar harus memiliki dimensi yang sama.
    """
    try:
        cover_img = Image.open(cover_image_path).convert("RGB")
        stego_img = Image.open(stego_image_path).convert("RGB")
    except Exception as e:
        raise ValueError(f"Gagal memuat gambar: {str(e)}")

    if cover_img.size != stego_img.size:
        raise ValueError("Dimensi gambar cover dan stego tidak sama, tidak dapat menghitung MSE.")

    cover_arr = np.array(cover_img, dtype=np.float64)
    stego_arr = np.array(stego_img, dtype=np.float64)

    # Hitung error kuadrat (cover - stego)^2
    diff = cover_arr - stego_arr
    squared_error = np.square(diff)
    
    # Hitung rata-rata
    mse = np.mean(squared_error)
    
    return float(mse)
