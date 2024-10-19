document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('image-input');  // Ambil elemen input gambar
    const imagePreview = document.getElementById('image-preview');  // Ambil elemen preview gambar

    let cropper;

    imageInput.addEventListener('change', function(event) {
        const file = event.target.files[0];  // Ambil file gambar yang diupload
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;  // Tampilkan gambar yang diupload
                initCropper();  // Inisialisasi cropper setelah gambar dimuat
            };
            reader.readAsDataURL(file);  // Baca gambar sebagai URL
        }
    });

    function initCropper() {
        if (cropper) {
            cropper.destroy();  // Hancurkan cropper lama jika ada
        }
        cropper = new Cropper(imagePreview, {
            aspectRatio: 1,  // Set rasio aspek menjadi 1:1
            viewMode: 1,
            minCropBoxWidth: 225,  // Minimal lebar crop box
            minCropBoxHeight: 225,  // Minimal tinggi crop box
            crop: function(event) {
            }
        });

        document.getElementById('label_name').addEventListener('change', function() {
            const selectedFabric = this.value;  // Ambil kain yang dipilih
            const regionSelect = document.getElementById('region');
            regionSelect.innerHTML = '<option value="">Pilih Daerah Asal</option>';  // Reset opsi daerah
            if (selectedFabric) {
                fetch(`/get_region/${selectedFabric}`)  // Ambil daerah asal kain dari server
                    .then(response => response.ok ? response.text() : Promise.reject('Region not found'))
                    .then(region => {
                        regionSelect.innerHTML += `<option value="${region}">${region}</option>`;  // Tambah opsi daerah
                        regionSelect.value = region;
                    })
                    .catch(console.error);  // Tampilkan error jika gagal
            }
        });
   
        const notification = document.getElementById("notification");  // Ambil elemen notifikasi
        if (notification) {
            setTimeout(() => { notification.style.display = "none"; }, 5000);  // Sembunyikan notifikasi setelah 5 detik
        }
    }
});
