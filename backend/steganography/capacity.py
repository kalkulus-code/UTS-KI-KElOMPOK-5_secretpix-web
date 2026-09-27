def cek_kapasitas(jumlah_bit_pesan, total_pixels):
    """
    Mengecek apakah pesan + header 32-bit muat di dalam gambar.
    1 piksel = 3 bit (karena ada channel RGB).
    """
    kapasitas_maksimal = total_pixels * 3
    total_bit_dibutuhkan = jumlah_bit_pesan + 32
    
    if total_bit_dibutuhkan > kapasitas_maksimal:
        raise ValueError(
            f"Kapasitas tidak cukup! Butuh {total_bit_dibutuhkan} bit, "
            f"tersedia hanya {kapasitas_maksimal} bit."
        )
    return True
