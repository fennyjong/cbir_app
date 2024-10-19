document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    const regionSelect = document.getElementById('region');
    const notification = document.getElementById('notification');

    document.getElementById('label_name').addEventListener('change', function () {
        const selectedFabric = this.value;
        regionSelect.innerHTML = '<option value="">Pilih Daerah Asal</option>';

        if (selectedFabric) {
            fetch(`/get_region/${selectedFabric}`)
                .then(response => {
                    if (!response.ok) throw new Error('Region not found');
                    return response.text();
                })
                .then(region => {
                    regionSelect.innerHTML += `<option value="${region}">${region}</option>`;
                    regionSelect.value = region;
                })
                .catch(console.error);
        }
    });

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

    let cropper;
    function initCropper() {
        if (cropper) cropper.destroy();

        cropper = new Cropper(imagePreview, {
            aspectRatio: 1,
            viewMode: 1,
            minCropBoxWidth: 225,
            minCropBoxHeight: 225,
        });

        if (notification) {
            setTimeout(() => {
                notification.style.display = "none";
            }, 5000);
        }
    }
});
