import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

def generate_histogram_comparison(cover_image_path: str, stego_image_path: str, output_path: str):
    """
    Menghasilkan dan menyimpan perbandingan histogram antara cover image dan stego image.
    Mengekstrak nilai warna (Red, Green, Blue) dan membuat plot berdampingan.
    """
    try:
        cover_img = Image.open(cover_image_path).convert("RGB")
        stego_img = Image.open(stego_image_path).convert("RGB")
    except Exception as e:
        raise ValueError(f"Gagal memuat gambar: {str(e)}")

    cover_arr = np.array(cover_img)
    stego_arr = np.array(stego_img)

    colors = ('r', 'g', 'b')
    channels = ('Merah', 'Hijau', 'Biru')

    fig, axes = plt.subplots(3, 2, figsize=(12, 12))
    fig.suptitle('Perbandingan Histogram: Cover vs Stego Image')

    for i, color in enumerate(colors):
        # Histogram Cover
        axes[i, 0].hist(cover_arr[:, :, i].ravel(), bins=256, color=color, alpha=0.7)
        axes[i, 0].set_title(f'Cover Image - Channel {channels[i]}')
        axes[i, 0].set_xlim([0, 256])

        # Histogram Stego
        axes[i, 1].hist(stego_arr[:, :, i].ravel(), bins=256, color=color, alpha=0.7)
        axes[i, 1].set_title(f'Stego Image - Channel {channels[i]}')
        axes[i, 1].set_xlim([0, 256])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Buat direktori output jika belum ada
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    
    return output_path
