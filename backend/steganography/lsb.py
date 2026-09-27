from PIL import Image
from backend.steganography.prng import get_shuffled_pixel_indices
from backend.steganography.capacity import cek_kapasitas

def teks_ke_biner(teks):
    return "".join(format(b, "08b") for b in teks.encode("utf-8"))

def biner_ke_teks(biner):
    byte_list = bytes(int(biner[i:i+8], 2) for i in range(0, len(biner), 8))
    return byte_list.decode("utf-8", errors="ignore")

def sisipkan_lsb(lokasi_gambar, lokasi_output, pesan, stego_key):
    img = Image.open(lokasi_gambar).convert("RGB")
    
    # 1. Siapkan header 32-bit + payload pesan
    pesan_biner = teks_ke_biner(pesan)
    data_total = format(len(pesan_biner), "032b") + pesan_biner
    jumlah_bit = len(data_total)

    # 2. Flatten nilai RGB piksel menjadi 1 deretan list linier
    channels = [val for px in img.getdata() for val in px]
    total_pixels = len(channels) // 3

    # Cek kapasitas
    cek_kapasitas(len(pesan_biner), total_pixels)

    # 3. Dapatkan urutan piksel yang diacak berdasarkan stego-key
    pixel_sequence = get_shuffled_pixel_indices(stego_key, total_pixels)

    # 4. Sisipkan bit pesan ke LSB channel pada piksel yang diacak
    for i in range(jumlah_bit):
        px_idx = pixel_sequence[i // 3]  # Ambil piksel ke-berapa dari urutan acak
        ch_idx = px_idx * 3 + (i % 3)    # Tentukan channel (R=0, G=1, B=2)
        channels[ch_idx] = (channels[ch_idx] & ~1) | int(data_total[i])

    # 5. Reconstruct tuple RGB dan simpan gambar
    new_pixels = [tuple(channels[i:i+3]) for i in range(0, len(channels), 3)]
    img.putdata(new_pixels)
    img.save(lokasi_output, format="PNG")
    print(f"Pesan berhasil disisipkan ke: {lokasi_output}")

def ekstrak_lsb(lokasi_gambar, stego_key):
    img = Image.open(lokasi_gambar).convert("RGB")
    
    # Flatten seluruh channel warna
    channels = [val for px in img.getdata() for val in px]
    total_pixels = len(channels) // 3

    # Dapatkan urutan piksel yang diacak (harus sama persis jika key sama)
    pixel_sequence = get_shuffled_pixel_indices(stego_key, total_pixels)

    # Fungsi bantuan untuk membaca bit ke-i dari urutan acak
    def get_bit(i):
        px_idx = pixel_sequence[i // 3]
        ch_idx = px_idx * 3 + (i % 3)
        return str(channels[ch_idx] & 1)

    # 1. Ambil 32 bit pertama untuk membaca header (panjang pesan)
    header_biner = "".join(get_bit(i) for i in range(32))
    panjang_pesan = int(header_biner, 2)

    # Validasi header
    if panjang_pesan == 0 or panjang_pesan > (len(channels) - 32):
        return "Error: Tidak ada pesan rahasia yang valid atau password salah / gambar rusak."

    # 2. Ambil bit pesan sebanyak panjang_pesan langsung dari indeks bit ke 32
    pesan_biner = "".join(get_bit(i) for i in range(32, 32 + panjang_pesan))
    return biner_ke_teks(pesan_biner)

if __name__ == "__main__":
    kunci = "rahasia123"
    sisipkan_lsb("gambar_asli.png", "gambar_stego.png", "Halo, ini pesan rahasia!", kunci)
    print("Pesan ekstraksi:", ekstrak_lsb("gambar_stego.png", kunci))