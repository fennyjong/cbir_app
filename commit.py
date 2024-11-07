import os
from flask import Flask, jsonify
from models import db, SongketDataset

app = Flask(__name__)

# Konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/Songket_Indonesia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi database dengan aplikasi Flask
db.init_app(app)
@app.route('/upload_all_images_rollback', methods=['POST'])
def upload_all_images_rollback():
    rollback_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'New folder')
    print("Checking rollback folder:", rollback_folder)

    if not os.path.exists(rollback_folder):
        return jsonify({'success': False, 'message': 'Rollback folder not found.'}), 404

    uploaded_files = [
        f for f in os.listdir(rollback_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))
    ]
    print("Found uploaded files:", uploaded_files)
    success_count = 0

    try:
        for filename in uploaded_files:
            new_dataset = SongketDataset(image_filename=filename, fabric_name="Songket Awan Larat", region="Riau")
            db.session.add(new_dataset)
            success_count += 1

        db.session.commit()
        print(f"Successfully uploaded {success_count} files.")

    except Exception as e:
        db.session.rollback()
        print("Error during database operation:", str(e))
        return jsonify({'success': False, 'message': str(e)}), 500

    return jsonify({'success': True, 'uploaded_files': success_count}), 200


if __name__ == "__main__":
    app.run(port=5001, debug=True)  # Menjalankan aplikasi Flask di port 5001

    """
    Endpoint ini digunakan untuk mengupload semua gambar dari folder 'uploads' ke database.
    
    1. Menentukan jalur ke folder rollback dan memeriksa keberadaannya.
    2. Mengambil daftar file gambar dari folder tersebut.
    3. Mengupload setiap gambar ke dalam database sebagai entri baru di SongketDataset.
    4. Mengembalikan respons JSON yang mencakup jumlah file yang berhasil diupload atau pesan kesalahan jika terjadi masalah.

    Contoh permintaan POST:
    POST: http://localhost:5001/upload_all_images_rollback 

    Contoh respons sukses:
    {
        "success": true,
        "uploaded_files": 560 (jumlah gambar)
    }

    Jika folder 'uploads' tidak ditemukan, akan mengembalikan:
    {
        "success": false,
        "message": "Rollback folder not found."
    }
    """