# Perancangan Sistem Temu Kembali Kain Songket Indonesia
## Menggunakan Convolutional Neural Network dan Cosine Similarity

## Deskripsi Proyek

Proyek ini bertujuan untuk mengembangkan sistem temu kembali (retrieval) kain Songket Indonesia menggunakan teknologi Convolutional Neural Network (CNN) dan Cosine Similarity. Sistem ini dirancang untuk membantu pengguna mengenali dan mencari gambar serupa dari berbagai jenis kain Songket berdasarkan ciri visual serta mendukung pelestarian budaya Indonesia dengan teknologi modern.

## 🌟 Fitur Utama

### 👤 Pengguna
- 🔍 **Pencarian Serupa**: Cari kain Songket berdasarkan kemiripan visual menggunakan **Cosine Similarity**.
- 📤 **Unggah Gambar**: Temukan kain hanya dengan mengunggah foto.
- 🖥️ **Antarmuka Ramah Pengguna**: Tampilan sederhana dan intuitif untuk mempermudah penggunaan.

### 🔑 Admin
- 🗂️ **Kelola Dataset**: Tambah, hapus, atau perbarui koleksi dataset gambar kain Songket.
- 🧠 **Latih Ulang Model**: Pelatihan model **CNN** dengan dataset baru untuk meningkatkan akurasi.
- 🕑 **Riwayat Pencarian**: Pantau aktivitas pencarian pengguna untuk analisis dan pengelolaan data.

## 🚀 Manfaat Utama
Untuk mempermudah akses informasi dan memperkenalkan kain songket sebagai warisan budaya Indonesia, sekaligus mendukung pemberdayaan industri kerajinan songket. Dengan meningkatkan pemasaran dan memperluas pasar, sistem ini dapat memperkenalkan kain songket kepada generasi muda dan wisatawan, memperkuat ekonomi kreatif, meningkatkan pengetahuan budaya dan mendukung pengembangan pariwisata di Indonesia.

## Tech Stack
- PostgreSQL
- Flask
- Python 3.8+
- GPU (disarankan untuk pelatihan model)

## Konfigurasi Database
1. **Restore Database**:
   ```bash
   # Import dataset SQL
   psql -U your_username -d your_database_name < dataset_songket.sql
   ```
   Atau menggunakan pgAdmin4:
   - Buka pgAdmin4
   - Buat database baru
   - Klik kanan pada database
   - Pilih "Restore"
   - Pilih file dataset_songket.sql
   - Klik "Restore"

2. **Konfigurasi config.py**:
   ```python
   # config.py
  
   # Ubah SQLAlchemy Database URL
   SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

## Instalasi Program

### 1. Clone Repository
```bash
git clone https://github.com/fennyjong/cbir_app.git
cd cbir_app
```

### 2. Buat Virtual Environment (Opsional)
```bash
python -m venv venv
source venv/bin/activate  # Untuk Linux/Mac
# atau
venv\Scripts\activate  # Untuk Windows
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```

## Cara Penggunaan
1. Jalankan aplikasi:
```bash
python app.py
```

2. Akses antarmuka pengguna melalui browser di `http://localhost:5000`

3. Unggah gambar kain Songket untuk memulai pencarian

## Referensi Dataset
Dataset yang digunakan dalam proyek ini dapat diakses melalui tautan berikut: [[Link Download Dataset Kain Songket](https://kirimin.link/QfehrNC0)]

## Rujukan Notebook Evaluasi
Untuk melihat pengaturan file gambar seperti (Scrapping gambar, Resize seluruh gambar dalam folder tertentu , Proses Augmentasi Gambar dalam folder tertentu dan Pembuatan Label Ground Truth bedasarkan folder gambar uji) proses evaluasi kinerja sistem termasuk perhitungan metrik presisi, recall, dan mAP, silakan akses tautan berikut: [[Link Jupyter Notebook Evaluasi]](https://drive.google.com/file/d/1H2QF3WV7GhEZDC_w1UGNUijnLkD-cK2O/view?usp=sharing)

## Metode yang Digunakan
- **Convolutional Neural Network (CNN)**: Untuk ekstraksi fitur visual dari gambar
- **Cosine Similarity**: Untuk menghitung tingkat kemiripan antara gambar yang diunggah dengan dataset

## Rujukan Penggunaan
Untuk mempelajari lebih lanjut cara kerja sistem, silakan merujuk pada dokumentasi di [[tautan dokumentasi](https://drive.google.com/file/d/16j-wzHSc_HFhpeagpHrDPMwJrpEaVhkj/view?usp=drive_link)].

## Batasan dan Catatan
- Akurasi sistem bergantung pada kualitas dan variasi dataset
- Disarankan menggunakan gambar dengan resolusi tinggi untuk hasil terbaik
- Pastikan pencahayaan dan sudut gambar yang baik saat mengambil foto kain

## Kontributor
- **Fenny Jong (535210001)** - Universitas Tarumanagara

## Kontak
- 📧 Email: fennyjong7@gmail.com
- 🐱 GitHub: https://github.com/fennyjong/cbir_app

---
