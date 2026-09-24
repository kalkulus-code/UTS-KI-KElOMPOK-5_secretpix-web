from PIL import Image


def teks_ke_biner(teks):
    """
    Mengubah teks menjadi deretan bit biner.
    Contoh:
    'A' -> 01000001
    """
    data = teks.encode("utf-8")
    return ''.join(format(byte, '08b') for byte in data)


def sisipkan_lsb(lokasi_gambar, lokasi_output, pesan):
    """
    Menyisipkan pesan teks ke dalam gambar menggunakan metode LSB.

    Setiap channel RGB digunakan untuk menyimpan 1 bit pesan.
    """

    # ==========================================
    # 1. Membuka gambar
    # ==========================================

    gambar = Image.open(lokasi_gambar)

    # Pastikan gambar menggunakan RGB
    if gambar.mode != "RGB":
        gambar = gambar.convert("RGB")

    pixel = gambar.load()

    lebar, tinggi = gambar.size

    # ==========================================
    # 2. Mengubah pesan menjadi biner
    # ==========================================

    data_biner = teks_ke_biner(pesan)

    jumlah_bit = len(data_biner)

    # ==========================================
    # 3. Mengecek kapasitas gambar
    # ==========================================

    kapasitas = lebar * tinggi * 3

    if jumlah_bit > kapasitas:
        raise ValueError(
            "Pesan terlalu besar untuk gambar."
        )

    # ==========================================
    # 4. Menyisipkan bit ke LSB pixel
    # ==========================================

    indeks_bit = 0

    for y in range(tinggi):
        for x in range(lebar):

            # Ambil nilai RGB
            merah, hijau, biru = pixel[x, y]

            # ----------------------------------
            # Channel Merah
            # ----------------------------------

            if indeks_bit < jumlah_bit:

                bit = int(data_biner[indeks_bit])

                # Ganti LSB merah
                merah = (merah & ~1) | bit

                indeks_bit += 1

            # ----------------------------------
            # Channel Hijau
            # ----------------------------------

            if indeks_bit < jumlah_bit:

                bit = int(data_biner[indeks_bit])

                # Ganti LSB hijau
                hijau = (hijau & ~1) | bit

                indeks_bit += 1

            # ----------------------------------
            # Channel Biru
            # ----------------------------------

            if indeks_bit < jumlah_bit:

                bit = int(data_biner[indeks_bit])

                # Ganti LSB biru
                biru = (biru & ~1) | bit

                indeks_bit += 1

            # Simpan pixel yang sudah diubah
            pixel[x, y] = (merah, hijau, biru)

            # Jika semua bit pesan sudah dimasukkan
            if indeks_bit >= jumlah_bit:
                break

        if indeks_bit >= jumlah_bit:
            break

    # ==========================================
    # 5. Menyimpan gambar hasil steganografi
    # ==========================================

    gambar.save(lokasi_output, format="PNG")

    print("Pesan berhasil disisipkan.")
    print("Gambar hasil:", lokasi_output)


# ==============================================
# PROGRAM UTAMA
# ==============================================

if __name__ == "__main__":

    # Nama file gambar asli
    gambar_asli = "gambar_asli.png"

    # Nama file hasil steganografi
    gambar_stego = "gambar_stego.png"

    # Pesan yang ingin disembunyikan
    pesan = "Halo, ini pesan rahasia!"

    # Menjalankan proses embedding
    sisipkan_lsb(
        gambar_asli,
        gambar_stego,
        pesan
    )