import numpy as np
from PIL import Image
import os

def visualize_enhanced_lsb(image_path: str, output_path: str, bit_plane: int = 0):
    """
    Menghasilkan visualisasi (enhanced) dari bidang bit (bit plane) tertentu.
    Secara default menampilkan LSB (bit ke-0). 
    Nilai 0 akan menjadi hitam (0), nilai 1 akan menjadi putih (255),
    sehingga pola LSB dapat terlihat jelas.
    """
    if not (0 <= bit_plane <= 7):
        raise ValueError("Bit plane harus berada di antara 0 dan 7")
        
    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as e:
        raise ValueError(f"Gagal memuat gambar: {str(e)}")

    img_arr = np.array(img, dtype=np.uint8)

    # Ekstrak bit ke-n dengan melakukan shift dan masking
    # Misalnya untuk bit_plane=0, maka (img_arr >> 0) & 1
    bit_extracted = (img_arr >> bit_plane) & 1

    # Skalakan 0 -> 0, dan 1 -> 255
    enhanced_arr = (bit_extracted * 255).astype(np.uint8)

    enhanced_img = Image.fromarray(enhanced_arr, mode="RGB")
    
    # Buat direktori output jika belum ada
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    enhanced_img.save(output_path)
    
    return output_path
