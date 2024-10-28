document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    const sidebar = document.getElementById('sidebar');
    const toggleSidebar = document.getElementById('toggleSidebar');
    const navItems = document.querySelectorAll('nav a');
    const contentSections = document.querySelectorAll('.content-section');
    const logoutBtn = document.getElementById('logoutBtn');
    const addDatasetBtn = document.getElementById('addDatasetBtn');
    const newLabelBtn = document.getElementById('newLabelBtn');
    const addLabelModal = document.getElementById('addLabelModal');
    const closeLabelModal = document.getElementById('closeLabelModal');
    const addLabelForm = document.getElementById('addLabelForm');
    
    // Logout functionality
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            fetch('/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/login'; 
                } else {
                    alert('Logout failed. Please try again.');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        });
    }

    // Show image in modal
    function showFullImage(imageSrc) {
        const modal = document.getElementById('imageModal');
        const fullImage = document.getElementById('fullImage');
        fullImage.src = imageSrc;
        modal.style.display = 'block';
    }

    // Modal close functionality
    const modal = document.getElementById("imageModal");
    const span = document.getElementsByClassName("close")[0];

    if (span) {
        span.onclick = function() {
            modal.style.display = "none";
        };
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

    // Navigation and sidebar toggle
    if (addDatasetBtn) {
        addDatasetBtn.addEventListener('click', () => {
            window.location.href = '/admin/new_dataset'
        });
    }

    if (closeLabelModal) {
        closeLabelModal.addEventListener('click', () => {
            addLabelModal.style.display = 'none';
        });
    }

    if (toggleSidebar) {
        toggleSidebar.addEventListener('click', () => {
            sidebar.classList.toggle('w-64');
            sidebar.classList.toggle('w-20');
            document.querySelectorAll('.sidebar-text').forEach(el => el.classList.toggle('hidden'));
        });
    }

    // Navigation item click functionality
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const sectionId = item.getAttribute('data-section');
            navItems.forEach(navItem => navItem.classList.remove('bg-gray-700'));
            contentSections.forEach(section => section.classList.remove('active'));
            item.classList.add('bg-gray-700');
            document.getElementById(sectionId).classList.add('active');
        });
    });

    // Delete multiple datasets
    const deleteMultipleBtn = document.getElementById('deleteMultipleBtn');
    if (deleteMultipleBtn) {
        deleteMultipleBtn.addEventListener('click', () => {
            const selectedIds = [];
            const checkboxes = document.querySelectorAll('input[name="datasetCheckbox"]:checked');
            
            checkboxes.forEach(checkbox => {
                selectedIds.push(checkbox.dataset.id);
            });

            if (selectedIds.length === 0) {
                alert('Please select at least one dataset to delete.');
                return;
            }

            if (confirm(`Are you sure you want to delete the selected datasets? (${selectedIds.length})`)) {
                fetch('/delete_multiple_datasets', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ ids: selectedIds }),
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        loadDatasets(); // Refresh the dataset table
                        alert('Selected datasets deleted successfully.');
                    } else {
                        alert('Failed to delete selected datasets.');
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting datasets.');
                });
            }
        });
    }

    // Select/Deselect all checkboxes
    const selectAllCheckbox = document.getElementById('selectAll');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('input[name="datasetCheckbox"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }

    // Load datasets and handle pagination
    let currentPage = 1;
    let entriesPerPage = 10;
    let datasets = [];

    function loadDatasets() {
        fetch('/get_datasets')
            .then(response => response.json())
            .then(data => {
                datasets = data;
                displayDatasets();
            });
    }

    function displayDatasets() {
        const tableBody = document.getElementById('datasetTableBody');
        tableBody.innerHTML = '';

        const searchQuery = datasetSearchInput.value.toLowerCase();
        const filteredDatasets = datasets.filter(dataset =>
            dataset.fabric_name.toLowerCase().includes(searchQuery)
        );

        const totalEntries = filteredDatasets.length;
        const totalPages = Math.ceil(totalEntries / entriesPerPage);
        const startIndex = (currentPage - 1) * entriesPerPage;
        const endIndex = startIndex + entriesPerPage;
        const paginatedDatasets = filteredDatasets.slice(startIndex, endIndex);

        paginatedDatasets.forEach((dataset, index) => {
            const row = `
                <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <input type="checkbox" name="datasetCheckbox" data-id="${dataset.id}" />
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">${startIndex + index + 1}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <img class="songket-image" src="/uploads/${dataset.image_filename}" alt="Songket Fabric" onclick="showFullImage('/uploads/${dataset.image_filename}')">
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap" id="class-${dataset.id}">${dataset.fabric_name}</td>
                    <td class="px-6 py-4 whitespace-nowrap" id="region-${dataset.id}">${dataset.region}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button onclick="editDataset(${dataset.id})" class="text-gray-600 hover:text-gray-900 mr-3">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button onclick="deleteDataset(${dataset.id})" class="text-red-600 hover:text-red-900">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });

        datasetEntriesInfo.textContent = `Showing ${startIndex + 1} to ${Math.min(startIndex + entriesPerPage, totalEntries)} of ${totalEntries} entries`;
        datasetCurrentPage.textContent = currentPage;
    }

    // Edit and delete dataset functionality
    function editDataset(id) {
        const currentName = document.getElementById(`class-${id}`).textContent;
        const currentRegion = document.querySelector(`#region-${id}`).textContent;

        const newName = prompt("Masukkan nama kain:", currentName);
        const newRegion = prompt("Masukkan asal daerah kain:", currentRegion);

        if ((newName && newName !== currentName) || (newRegion && newRegion !== currentRegion)) {
            fetch('/edit_dataset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    id: id, 
                    fabric_name: newName, 
                    region: newRegion 
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`class-${id}`).textContent = newName;
                    document.querySelector(`#region-${id}`).textContent = newRegion;
                    alert('Dataset updated successfully');
                } else {
                    alert('Failed to update dataset');
                }
            });
        }
    }    

    function deleteDataset(id) {
        if (confirm('Are you sure you want to delete this dataset?')) {
            fetch('/delete_dataset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: id }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadDatasets(); // Refresh the dataset table
                    alert('Dataset deleted successfully');
                } else {
                    alert('Failed to delete dataset');
                }
            });
        }
    }

    // Search functionality
    const datasetSearchInput = document.getElementById('datasetSearchInput');
    datasetSearchInput.addEventListener('input', function() {
        currentPage = 1; // Reset to first page
        displayDatasets(); // Redisplay datasets with the current filter
    });

    loadDatasets(); // Initial load
});
