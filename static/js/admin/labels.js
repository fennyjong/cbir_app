// Label management state and functionality
let currentLabelPage = 1;
let labelEntriesPerPage = 10;
let labels = [];
let isEditMode = false;
let editLabelId = null;

// Load labels with pagination and search
function loadLabels() {
    fetch('/get_labels')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                labels = data.labels;
                displayLabels();
            }
        })
        .catch(error => console.error('Error loading labels:', error));
}

function displayLabels() {
    const tableBody = document.getElementById('labelTableBody');
    tableBody.innerHTML = '';

    const searchQuery = document.getElementById('labelSearchInput').value.toLowerCase();
    const filteredLabels = labels.filter(label =>
        label.name.toLowerCase().includes(searchQuery) ||
        label.region.toLowerCase().includes(searchQuery)
    );

    const totalEntries = filteredLabels.length;
    const totalPages = Math.ceil(totalEntries / labelEntriesPerPage);
    const startIndex = (currentLabelPage - 1) * labelEntriesPerPage;
    const endIndex = startIndex + labelEntriesPerPage;
    const paginatedLabels = filteredLabels.slice(startIndex, endIndex);

    paginatedLabels.forEach((label, index) => {
        const row = `
            <tr>
                <td class="px-6 py-4">
                    <input type="checkbox" class="label-checkbox" data-id="${label.id}">
                </td>
                <td class="px-6 py-4 whitespace-nowrap">${startIndex + index + 1}</td>
                <td class="px-6 py-4 whitespace-nowrap">${label.name}</td>
                <td class="px-6 py-4 whitespace-nowrap">${label.region}</td>
                <td class="px-6 py-4 whitespace-nowrap">${label.description}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button onclick="editLabel(${label.id})" class="text-gray-600 hover:text-gray-900 mr-3">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button onclick="deleteLabel(${label.id})" class="text-red-600 hover:text-red-900">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });

    // Update entries info and pagination
    document.getElementById('labelEntriesInfo').textContent = 
        `Showing ${startIndex + 1} to ${Math.min(endIndex, totalEntries)} of ${totalEntries} entries`;
    document.getElementById('labelCurrentPage').textContent = currentLabelPage;
}

// Handle form submission for both add and edit
function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = {
        name: form.labelName.value,
        region: form.labelRegion.value,
        description: form.labelDescription.value
    };

    const url = isEditMode ? '/edit_label' : '/add_label';
    if (isEditMode) {
        formData.id = editLabelId;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (isEditMode) {
                const index = labels.findIndex(l => l.id === editLabelId);
                labels[index] = data.label;
            } else {
                labels.push(data.label);
            }
            displayLabels();
            closeModal();
            alert(isEditMode ? 'Label updated successfully!' : 'Label added successfully!');
        } else {
            alert(data.message || 'An error occurred');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your request');
    });
}

// Edit label functionality
function editLabel(id) {
    const label = labels.find(l => l.id === id);
    if (!label) return;

    isEditMode = true;
    editLabelId = id;

    const form = document.getElementById('addLabelForm');
    form.labelName.value = label.name;
    form.labelRegion.value = label.region;
    form.labelDescription.value = label.description;
    
    // Update modal title to reflect edit mode
    const modalTitle = document.querySelector('#addLabelModal h2');
    if (modalTitle) {
        modalTitle.textContent = 'Edit Label';
    }

    // Show modal
    document.getElementById('addLabelModal').style.display = 'block';
}

// Function to close modal and reset form
function closeModal() {
    const modal = document.getElementById('addLabelModal');
    const form = document.getElementById('addLabelForm');
    
    modal.style.display = 'none';
    form.reset();
    isEditMode = false;
    editLabelId = null;

    // Reset modal title
    const modalTitle = document.querySelector('#addLabelModal h2');
    if (modalTitle) {
        modalTitle.textContent = 'Add New Label';
    }
}

// Delete label functionality
function deleteLabel(id) {
    if (!confirm('Are you sure you want to delete this label?')) return;

    fetch('/delete_label', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: id })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            labels = labels.filter(label => label.id !== id);
            displayLabels();
            alert('Label deleted successfully');
        } else {
            alert('Failed to delete label: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the label');
    });
}

// Delete multiple labels
function deleteMultipleLabels() {
    const selectedLabels = Array.from(document.querySelectorAll('.label-checkbox:checked'))
        .map(checkbox => parseInt(checkbox.dataset.id));

    if (selectedLabels.length === 0) {
        alert('Please select labels to delete');
        return;
    }

    if (!confirm(`Are you sure you want to delete ${selectedLabels.length} labels?`)) return;

    Promise.all(selectedLabels.map(id =>
        fetch('/delete_label', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: id })
        }).then(response => response.json())
    ))
    .then(() => {
        labels = labels.filter(label => !selectedLabels.includes(label.id));
        displayLabels();
        alert('Selected labels deleted successfully');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the labels');
    });
}

// Initialize label management
document.addEventListener('DOMContentLoaded', () => {
    loadLabels();

    // Set up form submission handler
    const form = document.getElementById('addLabelForm');
    form.addEventListener('submit', handleFormSubmit);

    // Set up modal close handler
    document.getElementById('closeLabelModal').addEventListener('click', closeModal);

    // Set up new label button handler
    document.getElementById('newLabelBtn').addEventListener('click', () => {
        isEditMode = false;
        editLabelId = null;
        const form = document.getElementById('addLabelForm');
        form.reset();
        document.getElementById('addLabelModal').style.display = 'block';
    });

    // Pagination controls
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

    // Select all labels checkbox
    document.getElementById('selectAllLabels').addEventListener('change', (e) => {
        const checkboxes = document.querySelectorAll('.label-checkbox');
        checkboxes.forEach(checkbox => checkbox.checked = e.target.checked);
    });

    // Delete multiple labels button
    document.getElementById('deleteMultipleLabelBtn').addEventListener('click', deleteMultipleLabels);

    // Make functions global
    window.editLabel = editLabel;
    window.deleteLabel = deleteLabel;
    window.deleteMultipleLabels = deleteMultipleLabels;
    window.closeModal = closeModal;
});