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
    const datasetInfoBtn = document.getElementById('datasetInfoBtn');
    const labelInfoBtn = document.getElementById('labelInfoBtn');
    const datasetInfoPopup = document.getElementById('datasetInfoPopup');
    const labelInfoPopup = document.getElementById('labelInfoPopup');

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
                window.location.href = '/login';  // Redirect to login page
            } else {
                alert('Logout failed. Please try again.');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
    
     // Fungsi untuk menampilkan gambar dalam modal
     function showFullImage(imageSrc) {
        const modal = document.getElementById('imageModal');
        const fullImage = document.getElementById('fullImage');
        fullImage.src = imageSrc;
        modal.style.display = 'block';
    }

    // Dapatkan elemen modal
    const modal = document.getElementById("imageModal");

    // Dapatkan elemen <span> yang menutup modal
    const span = document.getElementsByClassName("close")[0];

    // Ketika pengguna mengklik <span> (x), tutup modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // Tutup modal ketika mengklik di luar gambar
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    function loadDatasets() {
        fetch('/get_datasets')
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('datasetTableBody');
                tableBody.innerHTML = '';
                data.forEach((dataset, index) => {
                    const row = `
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap">${index + 1}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <img class="songket-image cursor-pointer" src="/uploads/${dataset.image_filename}" alt="Songket Fabric" onclick="showFullImage('/uploads/${dataset.image_filename}')">
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap" id="class-${dataset.id}">${dataset.fabric_name}</td>
                            <td class="px-6 py-4 whitespace-nowrap">${dataset.region}</td>
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
            });
    }

    addDatasetBtn.addEventListener('click', () => {
        window.location.href = '/new_dataset';
    });

    newLabelBtn.addEventListener('click', () => {
        addLabelModal.style.display = 'block';
    });

    closeLabelModal.addEventListener('click', () => {
        addLabelModal.style.display = 'none';
    });

    addLabelForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const labelName = document.getElementById('labelName').value;
        const labelRegion = document.getElementById('labelRegion').value;
        const labelDescription = document.getElementById('labelDescription').value;

        // Add new label to the labels array
        const newLabel = {
            id: labels.length + 1,
            name: labelName,
            region: labelRegion,
            description: labelDescription,
            count: 0
        };
        labels.push(newLabel);
        updateLabelInfo();
        alert(`Label "${labelName}" added successfully!`);
        addLabelModal.style.display = 'none';
        addLabelForm.reset();
    });

    datasetInfoBtn.addEventListener('click', (e) => {
        let infoContent = '<h3 class="font-bold">Fabric Name Totals:</h3><ul>';
        for (let [fabric, count] of Object.entries(fabricData)) {
            infoContent += `<li>${fabric}: ${count}</li>`;
        }
        infoContent += '</ul>';
        
        datasetInfoPopup.innerHTML = infoContent;
        datasetInfoPopup.style.display = 'block';
        datasetInfoPopup.style.left = `${e.pageX}px`;
        datasetInfoPopup.style.top = `${e.pageY}px`;
    });

    function updateLabelInfo() {
        let infoContent = '<h3 class="font-bold">Labels:</h3><ul>';
        labels.forEach(label => {
            infoContent += `<li>${label.name} (${label.region}): ${label.count}</li>`;
        });
        infoContent += '</ul>';
        labelInfoPopup.innerHTML = infoContent;
    }

    labelInfoBtn.addEventListener('click', (e) => {
        updateLabelInfo();
        labelInfoPopup.style.display = 'block';
        labelInfoPopup.style.left = `${e.pageX}px`;
        labelInfoPopup.style.top = `${e.pageY}px`;
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('#datasetInfoBtn') && !e.target.closest('#datasetInfoPopup')) {
            datasetInfoPopup.style.display = 'none';
        }
        if (!e.target.closest('#labelInfoBtn') && !e.target.closest('#labelInfoPopup')) {
            labelInfoPopup.style.display = 'none';
        }
    });

    toggleSidebar.addEventListener('click', () => {
        sidebar.classList.toggle('w-64');
        sidebar.classList.toggle('w-20');
        document.querySelectorAll('.sidebar-text').forEach(el => el.classList.toggle('hidden'));
    });

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

    logoutBtn.addEventListener('click', () => {
                        window.location.href = '/login';
               
    });

    function loadDatasets() {
        fetch('/get_datasets')
            .then(response => response.json())
            .then(data => {
                const tableBody = document.getElementById('datasetTableBody');
                tableBody.innerHTML = '';
                data.forEach((dataset, index) => {
                    const row = `
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap">${index + 1}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <img class="songket-image" src="/uploads/${dataset.image_filename}" alt="Songket Fabric" onclick="showFullImage('/uploads/${dataset.image_filename}')">
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap" id="class-${dataset.id}">${dataset.fabric_name}</td>
                            <td class="px-6 py-4 whitespace-nowrap">${dataset.region}</td>
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
            });
    }

    function showFullImage(imageSrc) {
        const modal = document.getElementById('imageModal');
        const fullImage = document.getElementById('fullImage');
        fullImage.src = imageSrc;
        modal.style.display = 'block';
    }

    function editDataset(id) {
        const currentName = document.getElementById(`class-${id}`).textContent;
        const newName = prompt("Enter new class name:", currentName);
        if (newName && newName !== currentName) {
            fetch('/edit_dataset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: id, fabric_name: newName }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`class-${id}`).textContent = newName;
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
                    loadDatasets();
                    alert('Dataset deleted successfully');
                } else {
                    alert('Failed to delete dataset');
                }
            });
        }
    }

    // Make functions global
    window.editDataset = editDataset;
    window.deleteDataset = deleteDataset;
    window.showFullImage = showFullImage;
    window.showFullImage = showFullImage;
    window.editDataset = editDataset;
    window.deleteDataset = deleteDataset;

    // Load datasets when the page loads
    loadDatasets();
});
