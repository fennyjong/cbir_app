$(document).ready(function() {
    const imageInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    const croppedPreview = document.getElementById('cropped-preview');
    const regionInput = document.getElementById('region');
    const notification = document.getElementById('notification');
    let cropper;

    // Inisialisasi Select2 untuk nama kain
    $('#label_name').select2({
        placeholder: 'Pilih atau ketik nama kain',
        allowClear: true,
        tags: true // Memungkinkan pengguna menambahkan opsi baru jika tidak ditemukan
    });

    // Event listener untuk perubahan pada select nama kain
    $('#label_name').on('change', function() {
        updateRegion($(this).val());
    });

    // Fungsi untuk memperbarui daerah asal berdasarkan nama kain yang dipilih
    function updateRegion(selectedFabric) {
        if (selectedFabric) {
            fetch(`/get_region/${selectedFabric}`)
                .then(response => {
                    if (!response.ok) throw new Error('Region not found');
                    return response.text();
                })
                .then(region => {
                    regionInput.value = region;
                })
                .catch(error => {
                    console.error('Error:', error);
                    regionInput.value = '';
                });
        } else {
            regionInput.value = '';
        }
    }

    imageInput.addEventListener('change', event => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = e => {
                imagePreview.src = e.target.result;
                initCropper();
            };
            reader.readAsDataURL(file);
        }
    });

    function initCropper() {
        if (cropper) cropper.destroy();

        cropper = new Cropper(imagePreview, {
            aspectRatio: 1,
            viewMode: 1,
            minCropBoxWidth: 100,
            minCropBoxHeight: 100,
            crop: function(event) {
                updateCroppedPreview();
            }
        });
    }

    function updateCroppedPreview() {
        if (cropper) {
            const croppedCanvas = cropper.getCroppedCanvas();
            if (croppedCanvas) {
                croppedPreview.src = croppedCanvas.toDataURL();
            }
        }
    }

    $('#upload-form').on('submit', function(e) {
        e.preventDefault();
        if (cropper) {
            const croppedCanvas = cropper.getCroppedCanvas();
            if (croppedCanvas) {
                $('#cropped-data').val(croppedCanvas.toDataURL());
            }
        }
        this.submit();
    });

    if (notification) {
        setTimeout(() => {
            notification.style.display = "none";
        }, 5000);
    }
});