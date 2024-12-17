# Perancangan Sistem Temu Kembali Kain Songket Indonesia
## Menggunakan Convolutional Neural Network dan Cosine Similarity

## Deskripsi Proyek

Proyek ini bertujuan untuk mengembangkan sistem temu kembali (retrieval) kain Songket Indonesia menggunakan teknologi Convolutional Neural Network (CNN) dan Cosine Similarity. Sistem ini dirancang untuk membantu pengguna mengenali dan mencari kembali berbagai jenis kain Songket berdasarkan ciri visual, serta mendukung pelestarian budaya Indonesia dengan teknologi modern.

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
- **Preservasi Budaya**: Mendukung upaya pelestarian kain Songket Indonesia.
- **Efisiensi Pencarian**: Mempermudah identifikasi kain Songket melalui teknologi AI.
- **Peningkatan Akurasi**: Memanfaatkan CNN untuk ekstraksi fitur visual yang lebih detail.

## Prasyarat
- Python 3.8+
- GPU (disarankan untuk pelatihan model)

## Instalasi Program

### 1. Clone Repository
```bash
git clone https://github.com/fennyjong/cbir_app.git
cd cbir_app
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)
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
Untuk melihat pengaturan file gambar, proses evaluasi kinerja sistem, termasuk perhitungan metrik presisi, recall, dan mAP, silakan akses tautan berikut: [Link Jupyter Notebook Evaluasi]

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
