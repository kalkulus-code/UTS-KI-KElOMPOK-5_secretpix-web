# SecretPix

**SecretPix** adalah aplikasi web yang menerapkan teknik steganografi
untuk menyembunyikan pesan rahasia ke dalam citra digital menggunakan
metode Least Significant Bit (LSB).

## Deskripsi

SecretPix dikembangkan sebagai proyek mata kuliah Keamanan Informasi
dengan topik Steganografi.

Aplikasi ini memungkinkan pengguna untuk menyisipkan pesan rahasia
ke dalam gambar (embed) dan mengambil kembali pesan tersebut dari
gambar stego (extract).

Pada proses embedding, pesan akan diproses sebelum disisipkan ke dalam
pixel gambar. Sistem menggunakan stego-key untuk membantu menentukan
posisi penyisipan data secara pseudo-random.

SecretPix dirancang untuk mendukung citra PNG dan BMP serta menyediakan
analisis terhadap hasil steganografi, seperti MSE, PSNR, perbandingan
histogram, dan visualisasi bidang LSB.

## Fitur Utama

### Embed
- Upload cover image
- Input pesan rahasia
- Input stego-key
- Penyisipan pesan menggunakan metode LSB
- Pemeriksaan kapasitas citra
- Menghasilkan stego image

### Extract
- Upload stego image
- Input stego-key
- Ekstraksi pesan tersembunyi
- Menampilkan pesan yang berhasil diekstraksi

### Analisis
- MSE
- PSNR
- Perbandingan histogram cover dan stego
- Enhanced LSB

## Teknologi

Frontend:
- HTML
- Tailwind CSS
- JavaScript

Backend:
- Python
- Flask

Library:
- Pillow
- NumPy
- PyCryptodome

## Struktur Project

```text
UTS-KI-KELOMPOK-5_secretpix-web/
│
├── backend/
├── docs/
├── frontend/
├── tests/
│
├── PROJECT_WORKSHEET.md
├── TEAM_WORK.md
├── README.md
└── .gitignore

Persyaratan
- Python 3
- Web browser
- Git
Instalasi
Clone repository:
git clone https://github.com/kalkulus-code/UTS-KI-KElOMPOK-5_secretpix-web.git

Masuk ke folder project:
cd UTS-KI-KELOMPOK-5_secretpix-web

Instal dependency dari folder utama project:
```bash
python -m pip install -r backend/requirements.txt
```

Menjalankan aplikasi:
```bash
python backend/app.py
```

Buka `http://127.0.0.1:5000/` di browser. Buka halaman melalui alamat
Flask tersebut agar request frontend ke `/api/embed` dan `/api/extract`
terhubung ke backend. Jangan membuka `frontend/index.html` langsung atau
menjalankannya lewat Live Server tanpa mengatur proxy API.

Cara Penggunaan
Embed Message
1. Buka halaman Embed.
2. Pilih cover image berformat PNG atau BMP.
3. Masukkan pesan yang ingin disembunyikan.
4. Masukkan stego-key.
5. Jalankan proses embed.
6. Sistem menghasilkan stego image.
Extract Message
1. Buka halaman Extract.
2. Pilih stego image.
3. Masukkan stego-key.
4. Jalankan proses extract.
5. Sistem menampilkan pesan yang berhasil diambil.
Anggota Kelompok
No	Nama	NPM
1	Fajar Rizky Mulyana	TODO
2	Safid Nasih Ulwan	TODO
3	Muhamad Abyan Furqan	TODO


Repository
GitHub:
https://github.com/kalkulus-code/UTS-KI-KELOMPOK-5_secretpix-web
Status Project
Project masih dalam tahap pengembangan.
- [x] Repository dibuat
- [x] Struktur project awal
- [x] UI Embed dan Extract
- [ ] Image upload dan preview
- [ ] LSB embedding
- [ ] LSB extraction
- [ ] Stego-key dan PRNG
- [ ] Enkripsi pesan
- [ ] Capacity validation
- [ ] MSE dan PSNR
- [ ] Histogram
- [ ] Enhanced LSB
- [ ] Unit testing
- [ ] Pengujian akhir
- [ ] Dokumentasi final
