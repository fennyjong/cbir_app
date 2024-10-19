// Event listener yang dijalankan ketika DOM sudah sepenuhnya dimuat
document.addEventListener('DOMContentLoaded', () => {
    // Mendapatkan referensi ke elemen HTML
    const imageInput = document.getElementById('image-input'); // Elemen input untuk mengupload gambar
    const imagePreview = document.getElementById('image-preview'); // Elemen untuk menampilkan preview gambar
    const regionSelect = document.getElementById('region'); // Elemen select untuk memilih daerah
    const notification = document.getElementById('notification'); // Elemen untuk menampilkan notifikasi

    // Event listener untuk perubahan pada dropdown label kain
    document.getElementById('label_name').addEventListener('change', function () {
        const selectedFabric = this.value; // Mengambil nilai kain yang dipilih
        regionSelect.innerHTML = '<option value="">Pilih Daerah Asal</option>'; // Mengatur ulang opsi daerah

        if (selectedFabric) {
            // Mengambil daerah asal yang terkait dengan kain yang dipilih dari server
            fetch(`/get_region/${selectedFabric}`)
                .then(response => {
                    if (!response.ok) throw new Error('Region not found'); // Menangani kesalahan
                    return response.text(); // Mengembalikan teks daerah
                })
                .then(region => {
                    // Menambahkan daerah yang diambil ke dalam opsi select daerah
                    regionSelect.innerHTML += `<option value="${region}">${region}</option>`;
                    regionSelect.value = region; // Mengatur nilai yang dipilih
                })
                .catch(console.error); // Mencetak kesalahan ke konsol
        }
    });

    // Event listener untuk perubahan pada input gambar
    imageInput.addEventListener('change', event => {
        const file = event.target.files[0]; // Mengambil file yang diupload
        if (file) {
            const reader = new FileReader(); // Membuat objek FileReader
            reader.onload = e => {
                imagePreview.src = e.target.result; // Menampilkan gambar yang diupload
                initCropper(); // Memanggil fungsi untuk menginisialisasi cropper
            };
            reader.readAsDataURL(file); // Membaca gambar sebagai URL
        }
    });

    let cropper; // Variabel untuk menyimpan instance Cropper
    function initCropper() {
        if (cropper) cropper.destroy(); // Menghancurkan cropper lama jika ada

        // Menginisialisasi cropper baru dengan opsi yang ditentukan
        cropper = new Cropper(imagePreview, {
            aspectRatio: 1, // Mengatur rasio aspek menjadi 1:1
            viewMode: 1, // Mengatur mode tampilan
            minCropBoxWidth: 225, // Lebar minimum kotak crop
            minCropBoxHeight: 225, // Tinggi minimum kotak crop
        });

        // Menyembunyikan notifikasi setelah 5 detik jika ada
        if (notification) {
            setTimeout(() => {
                notification.style.display = "none";
            }, 5000);
        }
    }
});
