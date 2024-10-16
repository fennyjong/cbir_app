// Sample data for demonstration
let datasetData = []; // Replace with your actual dataset
let labelData = []; // Replace with your actual labels

let currentDatasetPage = 1;
let currentLabelPage = 1;
const datasetEntriesPerPage = 10;
const labelEntriesPerPage = 10;

document.addEventListener('DOMContentLoaded', () => {
    // Initial render
    renderDatasetTable();
    renderLabelTable();

    // Event listeners
    document.getElementById('datasetEntriesSelect').addEventListener('change', updateDatasetEntries);
    document.getElementById('labelEntriesSelect').addEventListener('change', updateLabelEntries);
    document.getElementById('datasetSearchInput').addEventListener('input', renderDatasetTable);
    document.getElementById('labelSearchInput').addEventListener('input', renderLabelTable);
    document.getElementById('datasetPrevBtn').addEventListener('click', () => changeDatasetPage(-1));
    document.getElementById('datasetNextBtn').addEventListener('click', () => changeDatasetPage(1));
    document.getElementById('labelPrevBtn').addEventListener('click', () => changeLabelPage(-1));
    document.getElementById('labelNextBtn').addEventListener('click', () => changeLabelPage(1));
    document.getElementById('deleteMultipleBtn').addEventListener('click', deleteSelectedDatasets);
});

// Function to update entries per page
function updateDatasetEntries() {
    datasetEntriesPerPage = parseInt(document.getElementById('datasetEntriesSelect').value);
    currentDatasetPage = 1; // Reset to the first page
    renderDatasetTable();
}

function updateLabelEntries() {
    labelEntriesPerPage = parseInt(document.getElementById('labelEntriesSelect').value);
    currentLabelPage = 1; // Reset to the first page
    renderLabelTable();
}

// Function to render dataset table
function renderDatasetTable() {
    const searchTerm = document.getElementById('datasetSearchInput').value.toLowerCase();
    const filteredData = datasetData.filter(dataset => dataset.name.toLowerCase().includes(searchTerm));
    const totalEntries = filteredData.length;

    const startIndex = (currentDatasetPage - 1) * datasetEntriesPerPage;
    const paginatedData = filteredData.slice(startIndex, startIndex + datasetEntriesPerPage);

    const tbody = document.getElementById('datasetTableBody');
    tbody.innerHTML = paginatedData.map((dataset, index) => `
        <tr>
            <td class="px-6 py-4 whitespace-nowrap">${startIndex + index + 1}</td>
            <td class="px-6 py-4 whitespace-nowrap"><img src="${dataset.image}" alt="${dataset.name}" class="w-16 h-16 object-cover"/></td>
            <td class="px-6 py-4 whitespace-nowrap">${dataset.name}</td>
            <td class="px-6 py-4 whitespace-nowrap">${dataset.region}</td>
            <td class="px-6 py-4 whitespace-nowrap"><button class="bg-blue-600 text-white px-2 py-1 rounded">Edit</button></td>
        </tr>
    `).join('');

    document.getElementById('datasetEntriesInfo').textContent = `Showing ${startIndex + 1} to ${Math.min(startIndex + datasetEntriesPerPage, totalEntries)} of ${totalEntries} entries`;
    document.getElementById('datasetCurrentPage').textContent = currentDatasetPage;
}

// Function to render label table
function renderLabelTable() {
    const searchTerm = document.getElementById('labelSearchInput').value.toLowerCase();
    const filteredData = labelData.filter(label => label.name.toLowerCase().includes(searchTerm));
    const totalEntries = filteredData.length;

    const startIndex = (currentLabelPage - 1) * labelEntriesPerPage;
    const paginatedData = filteredData.slice(startIndex, startIndex + labelEntriesPerPage);

    const tbody = document.getElementById('labelTable').getElementsByTagName('tbody')[0];
    tbody.innerHTML = paginatedData.map((label, index) => `
        <tr>
            <td class="px-6 py-4 whitespace-nowrap">${startIndex + index + 1}</td>
            <td class="px-6 py-4 whitespace-nowrap">${label.name}</td>
            <td class="px-6 py-4 whitespace-nowrap">${label.description}</td>
            <td class="px-6 py-4 whitespace-nowrap"><button class="bg-blue-600 text-white px-2 py-1 rounded">Edit</button></td>
        </tr>
    `).join('');

    document.getElementById('labelEntriesInfo').textContent = `Showing ${startIndex + 1} to ${Math.min(startIndex + labelEntriesPerPage, totalEntries)} of ${totalEntries} entries`;
    document.getElementById('labelCurrentPage').textContent = currentLabelPage;
}

// Pagination for datasets
function changeDatasetPage(delta) {
    const totalEntries = datasetData.length;
    const totalPages = Math.ceil(totalEntries / datasetEntriesPerPage);

    currentDatasetPage += delta;
    if (currentDatasetPage < 1) currentDatasetPage = 1;
    if (currentDatasetPage > totalPages) currentDatasetPage = totalPages;

    renderDatasetTable();
}

// Pagination for labels
function changeLabelPage(delta) {
    const totalEntries = labelData.length;
    const totalPages = Math.ceil(totalEntries / labelEntriesPerPage);

    currentLabelPage += delta;
    if (currentLabelPage < 1) currentLabelPage = 1;
    if (currentLabelPage > totalPages) currentLabelPage = totalPages;

    renderLabelTable();
}

// Delete selected datasets
function deleteSelectedDatasets() {
    const selectedRows = Array.from(document.querySelectorAll('#datasetTableBody input[type="checkbox"]:checked')).map(input => input.closest('tr'));
    selectedRows.forEach(row => {
        const index = row.rowIndex - 1; // Adjust for header row
        datasetData.splice(index, 1); // Remove from dataset
    });

    renderDatasetTable();
}
