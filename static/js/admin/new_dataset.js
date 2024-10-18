document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('image-input');
    const imagePreview = document.getElementById('image-preview');
    const regionSelect = document.getElementById('region');
    
         // Handle change event for fabric name select
         document.getElementById('label_name').addEventListener('change', function() {
            const selectedFabric = this.value;
            const regionSelect = document.getElementById('region');

            // Clear current options
            regionSelect.innerHTML = '<option value="">Pilih Daerah Asal</option>';

            if (selectedFabric) {
                // Call the Flask endpoint to get the region
                fetch(`/get_region/${selectedFabric}`)
                    .then(response => {
                        if (response.ok) {
                            return response.text();
                        }
                        throw new Error('Region not found');
                    })
                    .then(region => {
                        const option = document.createElement('option');
                        option.value = region;
                        option.textContent = region;
                        regionSelect.appendChild(option);
                        regionSelect.value = region; // Set the selected region
                    })
                    .catch(error => {
                        console.error(error);
                    });
            }
        });
    
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
   
        window.onload = function() {
            var notification = document.getElementById("notification");
            if (notification) {
                setTimeout(function() {
                    notification.style.display = "none";
                }, 5000); // Change duration (in milliseconds) as needed
            }
        } }
});