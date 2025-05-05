# Aplikasi Ekstraksi Text dari Citra

Aplikasi ini dibuat untuk mengekstrak teks dari gambar menggunakan OCR (Optical Character Recognition) dengan antarmuka grafis modern berbasis PySide6.

## Fitur

- Interfase modern dengan Material Design menggunakan PySide6
- Ekstraksi teks otomatis dari gambar menggunakan pytesseract
- Database SQLite untuk penyimpanan data
- Operasi CRUD (Create, Read, Update, Delete) lengkap
- Pencarian data berdasarkan nomor atau nama file
- Preprocessing gambar untuk meningkatkan akurasi ekstraksi

## Persyaratan

- Python 3.6+
- PySide6
- Pillow
- pytesseract
- OpenCV (cv2)
- Tesseract OCR (harus diinstal secara terpisah)

## Instalasi

1. Instal dependensi Python:
   ```
   pip install -r requirements.txt
   ```

2. Instal [Tesseract OCR](https://github.com/tesseract-ocr/tesseract#installing-tesseract) sesuai dengan sistem operasi Anda.

3. Sesuaikan path Tesseract OCR di file `ekstraksi.py` jika perlu.

## Fitur UI Modern

- Material design dengan warna yang konsisten
- Kartu dengan sudut melengkung dan bayangan
- Tata letak responsif dan terorganisir
- Dialog dan notifikasi yang informatif
- Penggunaan komponen yang seragam

## Penggunaan

1. Jalankan aplikasi:
   ```
   python main.py
   ```

2. Gunakan tombol "TAMBAH" untuk menambahkan data baru
3. Pilih data di tabel dan gunakan tombol "UBAH" atau "HAPUS" untuk memodifikasi atau menghapus data
4. Gunakan fitur pencarian untuk menemukan data berdasarkan nomor atau nama file

## Struktur Kode

- `main.py`: File utama untuk menjalankan aplikasi
- `ui_main.py`: Implementasi halaman utama
- `ui_tambah.py`: Form untuk menambahkan data baru
- `ui_ubah.py`: Form untuk mengubah data yang ada
- `ui_hapus.py`: Form untuk konfirmasi penghapusan data
- `database.py`: Pengelola koneksi dan operasi database
- `ekstraksi.py`: Implementasi ekstraksi teks dari gambar

## Kontribusi

Silakan berkontribusi dengan membuat pull request atau melaporkan masalah melalui issue.

---

© 2025 Raditya Indra Putranto - PBO D 