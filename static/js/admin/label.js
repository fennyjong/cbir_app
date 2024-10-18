// Get the modal and form elements
const addLabelModal = document.getElementById('addLabelModal');
const addLabelForm = document.getElementById('addLabelForm');
const newLabelBtn = document.getElementById('newLabelBtn');
const closeLabelModal = document.getElementById('closeLabelModal');
const submitButton = addLabelForm.querySelector('button[type="submit"]');

// Global variable to store the current label ID for editing
let currentEditingLabelId = null;

// Show modal when clicking the add button
newLabelBtn.addEventListener('click', () => {
    currentEditingLabelId = null; // Reset current editing ID
    addLabelModal.classList.remove('hidden');
    addLabelModal.style.display = 'flex'; // Ensure modal is centered
});

// Hide modal when clicking the close button
closeLabelModal.addEventListener('click', hideModal);

// Function to hide modal and reset the form
function hideModal() {
    addLabelModal.classList.add('hidden');
    addLabelForm.reset();
    currentEditingLabelId = null; // Reset editing ID on modal close
}

// Prevent multiple submissions by disabling the submit button
addLabelForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    submitButton.disabled = true; // Disable button to prevent multiple submissions

    const formData = {
        fabric_name: document.getElementById('labelName').value.trim(), // Changed to fabric_name
        region: document.getElementById('labelRegion').value.trim(),
        description: document.getElementById('labelDescription').value.trim()
    };

    // Check for duplicate label
    const labelExists = labels.some(label => label.fabric_name.toLowerCase() === formData.fabric_name.toLowerCase());

    if (labelExists && currentEditingLabelId === null) {
        alert('Label name already exists. Please choose a different name.');
        submitButton.disabled = false; // Re-enable the button
        return; // Stop submission
    }

    try {
        const endpoint = currentEditingLabelId ? `/edit_label/${currentEditingLabelId}` : '/add_label';
        const method = currentEditingLabelId ? 'PUT' : 'POST';

        const response = await fetch(endpoint, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.success) {
            alert(`Label ${currentEditingLabelId ? 'updated' : 'added'} successfully!`);
            hideModal();
            loadLabels(); // Refresh the labels table
        } else {
            alert(`Failed to ${currentEditingLabelId ? 'update' : 'add'} label: ${result.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`An error occurred while ${currentEditingLabelId ? 'updating' : 'adding'} the label`);
    } finally {
        submitButton.disabled = false; // Re-enable the button after submission
    }
});

// Global variables for label pagination
let currentLabelPage = 1;
let labelEntriesPerPage = 10;
let labels = [];

// Function to load and display labels
function loadLabels() {
    fetch('/get_labels')
        .then(response => response.json())
        .then(data => {
            labels = data;
            displayLabels();
        })
        .catch(error => {
            console.error('Error loading labels:', error);
            alert('Failed to load labels');
        });
}

// Function to display labels in the table
function displayLabels() {
    const tableBody = document.getElementById('labelTableBody');
    const labelSearchInput = document.getElementById('labelSearchInput');
    const searchQuery = labelSearchInput.value.toLowerCase();

    // Filter labels based on search query
    const filteredLabels = labels.filter(label =>
        label.fabric_name.toLowerCase().includes(searchQuery) ||
        label.region.toLowerCase().includes(searchQuery)
    );

    // Calculate pagination
    const startIndex = (currentLabelPage - 1) * labelEntriesPerPage;
    const endIndex = startIndex + labelEntriesPerPage;
    const paginatedLabels = filteredLabels.slice(startIndex, endIndex);
    const totalLabels = filteredLabels.length;

    // Clear existing table content
    tableBody.innerHTML = '';

    // Generate table rows
    paginatedLabels.forEach((label, index) => {
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-50';
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">
                <input type="checkbox" name="labelCheckbox" data-id="${label.id}" class="rounded border-gray-300">
            </td>
            <td class="px-6 py-4 whitespace-nowrap">${startIndex + index + 1}</td>
            <td class="px-6 py-4 whitespace-nowrap">${escapeHtml(label.fabric_name)}</td>
            <td class="px-6 py-4 whitespace-nowrap">${escapeHtml(label.region)}</td>
            <td class="px-6 py-4 whitespace-nowrap">${escapeHtml(label.description)}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button onclick="editLabel(${label.id}, '${escapeHtml(label.fabric_name)}', '${escapeHtml(label.region)}', '${escapeHtml(label.description)}')" class="text-gray-600 hover:text-gray-900 mr-3">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button onclick="deleteLabel(${label.id})" class="text-red-600 hover:text-red-900">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });

    // Update pagination info
    updatePaginationInfo(startIndex, endIndex, totalLabels);
    updatePaginationButtons(totalLabels);
}

// Edit label function
function editLabel(id, fabric_name, region, description) {
    currentEditingLabelId = id; // Set the current editing label ID
    document.getElementById('labelName').value = fabric_name;
    document.getElementById('labelRegion').value = region;
    document.getElementById('labelDescription').value = description;

    // Show the modal
    addLabelModal.classList.remove('hidden');
    addLabelModal.style.display = 'flex'; // Ensure modal is centered
}

// Helper function to escape HTML to prevent XSS
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Update pagination information
function updatePaginationInfo(startIndex, endIndex, total) {
    const labelEntriesInfo = document.getElementById('labelEntriesInfo');
    labelEntriesInfo.textContent = `Showing ${startIndex + 1} to ${Math.min(endIndex, total)} of ${total} entries`;
}

// Update pagination buttons
function updatePaginationButtons(total) {
    const labelCurrentPage = document.getElementById('labelCurrentPage');
    const labelPrevBtn = document.getElementById('labelPrevBtn');
    const labelNextBtn = document.getElementById('labelNextBtn');

    labelCurrentPage.textContent = currentLabelPage;

    const totalPages = Math.ceil(total / labelEntriesPerPage);
    labelPrevBtn.disabled = currentLabelPage === 1;
    labelNextBtn.disabled = currentLabelPage === totalPages;
}

// Event listeners for pagination controls
document.getElementById('labelEntriesSelect').addEventListener('change', (e) => {
    labelEntriesPerPage = parseInt(e.target.value);
    currentLabelPage = 1;
    displayLabels();
});

document.getElementById('labelSearchInput').addEventListener('input', () => {
    currentLabelPage = 1;
    displayLabels();
});

document.getElementById('labelPrevBtn').addEventListener('click', () => {
    if (currentLabelPage > 1) {
        currentLabelPage--;
        displayLabels();
    }
});

document.getElementById('labelNextBtn').addEventListener('click', () => {
    const totalPages = Math.ceil(labels.length / labelEntriesPerPage);
    if (currentLabelPage < totalPages) {
        currentLabelPage++;
        displayLabels();
    }
});

// Load labels on page load
window.onload = loadLabels;

// Delete label function
function deleteLabel(id) {
    if (confirm('Are you sure you want to delete this label?')) {
        fetch(`/delete_label/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                alert('Label deleted successfully!');
                loadLabels(); // Refresh the labels table
            } else {
                alert('Failed to delete label: ' + result.message);
            }
        })
        .catch(error => {
            console.error('Error deleting label:', error);
            alert('An error occurred while deleting the label');
        });
    }
}

// Delete multiple labels
const deleteMultipleLabelBtn = document.getElementById('deleteMultipleLabelBtn');
deleteMultipleLabelBtn.addEventListener('click', () => {
    const selectedLabels = document.querySelectorAll('input[name="labelCheckbox"]:checked');
    const idsToDelete = Array.from(selectedLabels).map(checkbox => checkbox.getAttribute('data-id'));

    if (idsToDelete.length === 0) {
        alert('Please select at least one label to delete.');
        return;
    }

    if (confirm(`Are you sure you want to delete ${idsToDelete.length} label(s)?`)) {
        fetch('/delete_multiple_labels', {
            method: 'POST', // Change to POST
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ids: idsToDelete })
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                alert(`${idsToDelete.length} label(s) deleted successfully!`);
                loadLabels(); // Refresh the labels table
            } else {
                alert('Failed to delete labels: ' + result.message);
            }
        })
        .catch(error => {
            console.error('Error deleting labels:', error);
            alert('An error occurred while deleting labels');
        });
    }
});

const selectAllCheckbox = document.getElementById('selectAllLabels');
selectAllCheckbox.addEventListener('change', function() {
    const checkboxes = document.querySelectorAll('input[name="labelCheckbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = this.checked;
    });
});