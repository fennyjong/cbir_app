document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    const regionSelect = document.getElementById('region');
    const customRegion = document.getElementById('custom-region');
    const fabricNameSelect = document.getElementById('fabric_name');
    const customNama = document.getElementById('custom-nama');
    let cropper;

    imageInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                initCropper();
            };
            reader.readAsDataURL(file);
        }
    });

    function initCropper() {
        if (cropper) {
            cropper.destroy();
        }
        cropper = new Cropper(imagePreview, {
            aspectRatio: 1,
            viewMode: 1,
            minCropBoxWidth: 225,
            minCropBoxHeight: 225,
            crop: function(event) {
                if (event.detail.width < 225 || event.detail.height < 225) {
                    cropper.setCropBoxData({
                        width: Math.max(500, event.detail.width),
                        height: Math.max(500, event.detail.height)
                    });
                }
            }
        });
    }
});