from PIL import Image


def teks_ke_biner(teks):
    """
    Mengubah teks menjadi deretan bit biner.
    Contoh:
    'A' -> 01000001
    """
    data = teks.encode("utf-8")
    return ''.join(format(byte, '08b') for byte in data)


def biner_ke_teks(biner):
    """
    Mengubah deretan bit biner kembali menjadi teks (UTF-8).
    """
    bytes_list = []
    for i in range(0, len(biner), 8):
        byte = biner[i: i+8]
        if len(byte) == 8:
            bytes_list.append(int(byte, 2))
    return bytes(bytes_list).decode("utf-8", errors="ignore")


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
    # 2. Mengubah pesan menjadi biner dan menambah Header
    # ==========================================

    pesan_biner = teks_ke_biner(pesan)
    panjang_pesan = len(pesan_biner)
    
    # Header: 32-bit yang menyimpan angka panjang pesan
    header_biner = format(panjang_pesan, '032b')
    
    # Gabungkan header + pesan
    data_total = header_biner + pesan_biner

    jumlah_bit = len(data_total)

    # ==========================================
    # 3. Mengecek kapasitas gambar (Sederhana)
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
                bit = int(data_total[indeks_bit])
                merah = (merah & ~1) | bit
                indeks_bit += 1

            # ----------------------------------
            # Channel Hijau
            # ----------------------------------

            if indeks_bit < jumlah_bit:
                bit = int(data_total[indeks_bit])
                hijau = (hijau & ~1) | bit
                indeks_bit += 1

            # ----------------------------------
            # Channel Biru
            # ----------------------------------

            if indeks_bit < jumlah_bit:
                bit = int(data_total[indeks_bit])
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


def ekstrak_lsb(lokasi_gambar):
    """
    Mengekstrak pesan tersembunyi dari gambar menggunakan Header 32-bit.
    """
    gambar = Image.open(lokasi_gambar)
    if gambar.mode != "RGB":
        gambar = gambar.convert("RGB")

    pixel = gambar.load()
    lebar, tinggi = gambar.size

    bit_terkumpul = ""
    panjang_pesan = None
    
    # Proses pembacaan bit berurutan (sama seperti saat menyisipkan)
    for y in range(tinggi):
        for x in range(lebar):
            merah, hijau, biru = pixel[x, y]

            bit_terkumpul += str(merah & 1)
            bit_terkumpul += str(hijau & 1)
            bit_terkumpul += str(biru & 1)

            # Cek apakah kita baru saja selesai membaca header 32 bit pertama
            if panjang_pesan is None and len(bit_terkumpul) >= 32:
                header_biner = bit_terkumpul[:32]
                panjang_pesan = int(header_biner, 2)
                
                # Validasi untuk memastikan gambar benar-benar gambar stego
                if panjang_pesan == 0 or panjang_pesan > (lebar * tinggi * 3 - 32):
                    return "Error: Tidak ada pesan rahasia yang valid atau gambar rusak."

            # Jika header sudah tahu, berhenti kalau payload bit pesannya komplit
            if panjang_pesan is not None:
                total_bit_yang_dibutuhkan = 32 + panjang_pesan
                if len(bit_terkumpul) >= total_bit_yang_dibutuhkan:
                    break
                    
        # Break out loop y
        if panjang_pesan is not None and len(bit_terkumpul) >= 32 + panjang_pesan:
            break

    # Potong khusus bagian payload (setelah 32-bit header)
    pesan_biner = bit_terkumpul[32:32+panjang_pesan]
    return biner_ke_teks(pesan_biner)


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
    
    # Menguji hasil (Ekstraksi berdasarkan header)
    print("\nMencoba mengekstrak pesan...")
    hasil_pesan = ekstrak_lsb(gambar_stego)
    print("Pesan yang didapat:", hasil_pesan)