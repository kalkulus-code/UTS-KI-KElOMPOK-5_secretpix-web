import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os


def generate_histogram_comparison(
    cover_image_path: str,
    stego_image_path: str,
    output_path: str
):
    """
    Membuat visualisasi perbandingan:
    1. Histogram Cover
    2. Histogram Stego
    3. Pixel Difference

    Pixel Difference dihitung dengan rumus:
        Stego Pixel - Cover Pixel

    Untuk LSB, perubahan umumnya berada pada:
        -1 = pixel berkurang 1
         0 = pixel tidak berubah
        +1 = pixel bertambah 1
    """

    try:
        cover_img = Image.open(
            cover_image_path
        ).convert("RGB")

        stego_img = Image.open(
            stego_image_path
        ).convert("RGB")

    except Exception as e:
        raise ValueError(
            f"Gagal memuat gambar: {str(e)}"
        )

    # Pastikan ukuran gambar sama
    if cover_img.size != stego_img.size:
        raise ValueError(
            "Ukuran cover dan stego image harus sama."
        )

    cover_arr = np.array(cover_img)
    stego_arr = np.array(stego_img)

    colors = ("red", "green", "blue")
    channels = ("Merah", "Hijau", "Biru")

    # ========================================================
    # FIGURE
    # ========================================================

    fig, axes = plt.subplots(
        3,
        3,
        figsize=(18, 12)
    )

    fig.suptitle(
        "Perbandingan Histogram dan Pixel Difference",
        fontsize=16,
        fontweight="bold"
    )

    for i, color in enumerate(colors):

        # ====================================================
        # HISTOGRAM COVER
        # ====================================================

        cover_hist, _ = np.histogram(
            cover_arr[:, :, i],
            bins=256,
            range=(0, 256)
        )

        axes[i, 0].plot(
            range(256),
            cover_hist,
            color=color,
            linewidth=1
        )

        axes[i, 0].set_title(
            f"Cover Image - Channel {channels[i]}"
        )

        axes[i, 0].set_xlabel(
            "Nilai Intensitas"
        )

        axes[i, 0].set_ylabel(
            "Jumlah Pixel"
        )

        axes[i, 0].set_xlim(
            0,
            255
        )

        axes[i, 0].grid(
            alpha=0.2
        )

        # ====================================================
        # HISTOGRAM STEGO
        # ====================================================

        stego_hist, _ = np.histogram(
            stego_arr[:, :, i],
            bins=256,
            range=(0, 256)
        )

        axes[i, 1].plot(
            range(256),
            stego_hist,
            color=color,
            linewidth=1
        )

        axes[i, 1].set_title(
            f"Stego Image - Channel {channels[i]}"
        )

        axes[i, 1].set_xlabel(
            "Nilai Intensitas"
        )

        axes[i, 1].set_ylabel(
            "Jumlah Pixel"
        )

        axes[i, 1].set_xlim(
            0,
            255
        )

        axes[i, 1].grid(
            alpha=0.2
        )

        # ====================================================
        # PIXEL DIFFERENCE
        # ====================================================

        difference = (
            stego_arr[:, :, i].astype(np.int16)
            -
            cover_arr[:, :, i].astype(np.int16)
        )

        # Hitung jumlah untuk setiap perubahan
        diff_values, diff_counts = np.unique(
            difference,
            return_counts=True
        )

        # ====================================================
        # Tampilkan hanya rentang perubahan kecil
        # supaya LSB terlihat jelas
        # ====================================================

        mask = (
            (diff_values >= -2)
            &
            (diff_values <= 2)
        )

        diff_values_display = diff_values[mask]
        diff_counts_display = diff_counts[mask]

        axes[i, 2].bar(
            diff_values_display,
            diff_counts_display,
            width=0.6,
            color=color,
            alpha=0.75
        )

        axes[i, 2].set_title(
            f"Pixel Difference - Channel {channels[i]}",
            fontweight="bold"
        )

        axes[i, 2].set_xlabel(
            "Perubahan Pixel (Stego - Cover)"
        )

        axes[i, 2].set_ylabel(
            "Jumlah Pixel"
        )

        axes[i, 2].set_xticks(
            [-2, -1, 0, 1, 2]
        )

        axes[i, 2].grid(
            axis="y",
            alpha=0.2
        )

        # ====================================================
        # PERSENTASE PIXEL BERUBAH
        # ====================================================

        total_pixels = difference.size

        changed_pixels = np.count_nonzero(
            difference
        )

        percentage_changed = (
            changed_pixels /
            total_pixels
        ) * 100

        axes[i, 2].text(
            0.02,
            0.95,
            f"Pixel berubah: {changed_pixels:,}\n"
            f"Persentase: {percentage_changed:.4f}%",
            transform=axes[i, 2].transAxes,
            verticalalignment="top",
            fontsize=9,
            bbox=dict(
                boxstyle="round,pad=0.4",
                facecolor="white",
                alpha=0.8
            )
        )

    # ========================================================
    # JUDUL KOLOM
    # ========================================================

    axes[0, 0].set_title(
        "COVER IMAGE\nChannel Merah",
        fontweight="bold"
    )

    axes[0, 1].set_title(
        "STEGO IMAGE\nChannel Merah",
        fontweight="bold"
    )

    axes[0, 2].set_title(
        "PIXEL DIFFERENCE\nChannel Merah",
        fontweight="bold"
    )

    plt.tight_layout(
        rect=[0, 0, 1, 0.95]
    )

    # ========================================================
    # OUTPUT
    # ========================================================

    output_dir = os.path.dirname(
        output_path
    )

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True
        )

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    return output_path