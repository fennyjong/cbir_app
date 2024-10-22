document.getElementById('runModelBtn').addEventListener('click', async function() {
    try {
        // Show loading state
        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Processing Database...';
        
        // Call processing endpoint
        const response = await fetch('/admin/process_database', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Update timestamp
            document.getElementById('runModelTimestamp').innerText = 
                `Database terakhir diproses pada: ${result.timestamp}`;
                
            // Show success message
            alert('Database processing completed: ' + result.message);
        } else {
            alert('Processing failed: ' + result.message);
        }
        
    } catch (error) {
        console.error('Error during processing:', error);
        alert('An error occurred during database processing');
    } finally {
        // Reset button state
        this.disabled = false;
        this.innerHTML = '<i class="fas fa-play mr-2"></i> Jalankan Model';
    }
});

// Function to search similar images
async function searchSimilarImages(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);

    try {
        const response = await fetch('/admin/search_similar', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            displaySearchResults(result.results);
        } else {
            alert('Search failed: ' + result.message);
        }
    } catch (error) {
        console.error('Error during search:', error);
        alert('An error occurred during image search');
    }
}

// Function to display search results
function displaySearchResults(results) {
    // Implementation depends on your UI requirements
    console.log('Search results:', results);
    // Add code to display results in your UI
}

// Load last processing timestamp on page load
window.addEventListener('load', async function() {
    try {
        const response = await fetch('/admin/get_last_processing');
        const result = await response.json();
        
        if (result.timestamp) {
            document.getElementById('runModelTimestamp').innerText = 
                `Database terakhir diproses pada: ${result.timestamp}`;
        }
    } catch (error) {
        console.error('Error fetching last processing time:', error);
    }
});