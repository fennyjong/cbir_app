document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    let currentPage = 1;
    let totalPages = 1;
    let entriesPerPage = 10;
    let searchTerm = '';

    // Get DOM elements
    const historyTableBody = document.getElementById('historyTableBody');
    const historySearchInput = document.getElementById('historySearchInput');
    const historyEntriesSelect = document.getElementById('historyEntriesSelect');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    const exportHistoryBtn = document.getElementById('exportHistoryBtn');
    const historyPrevBtn = document.getElementById('historyPrevBtn');
    const historyNextBtn = document.getElementById('historyNextBtn');
    const historyCurrentPage = document.getElementById('historyCurrentPage');
    const historyEntriesInfo = document.getElementById('historyEntriesInfo');

    // Function to handle view action
    async function handleView(id) {
        try {
            const response = await fetch(`/api/search-history/${id}`);
            const data = await response.json();
            
            // You can implement your view logic here
            // For example, showing a modal with detailed information
            // This is just a placeholder alert
            alert(`Viewing details for entry ${id}`);
        } catch (error) {
            console.error('Error viewing history entry:', error);
        }
    }

    // Function to handle delete action
    async function handleDelete(id) {
        if (confirm('Are you sure you want to delete this entry?')) {
            try {
                const response = await fetch(`/api/search-history/${id}`, {
                    method: 'DELETE'
                });
                if (response.ok) {
                    loadSearchHistory();
                }
            } catch (error) {
                console.error('Error deleting history entry:', error);
            }
        }
    }

    // Function to load search history
    async function loadSearchHistory() {
        try {
            const response = await fetch(`/api/search-history?page=${currentPage}&per_page=${entriesPerPage}&search=${searchTerm}`);
            const data = await response.json();
            
            // Update table
            historyTableBody.innerHTML = '';
            data.data.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.no}</td>
                    <td>${item.username}</td>
                    <td>
                        <img src="/static/uploads/${item.query_image}" 
                             alt="Query Image" 
                             class="history-image"
                             onerror="this.src='/static/placeholder-image.png'">
                    </td>
                    <td>${item.timestamp}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <button onclick="handleView(${item.id}, '${item.query_image}', '${item.username}', '${item.timestamp}')" 
                                class="text-blue-600 hover:text-blue-900 mr-3">
                            <i class="fas fa-eye"></i> Detail
                        </button>
                        <button onclick="handleDelete(${item.id})" 
                                class="text-red-600 hover:text-red-900">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </td>
                `;
                historyTableBody.appendChild(row);
            });

            // Update pagination
            totalPages = data.pages;
            historyCurrentPage.textContent = currentPage;
            historyPrevBtn.disabled = currentPage === 1;
            historyNextBtn.disabled = currentPage === totalPages;

            // Update entries info
            const start = (currentPage - 1) * entriesPerPage + 1;
            const end = Math.min(currentPage * entriesPerPage, data.total);
            historyEntriesInfo.textContent = `Showing ${start} to ${end} of ${data.total} entries`;
        } catch (error) {
            console.error('Error loading search history:', error);
        }
    }

    // Make handleView and handleDelete functions globally available
    window.handleView = handleView;
    window.handleDelete = handleDelete;

    // Event Listeners
    historySearchInput.addEventListener('input', function(e) {
        searchTerm = e.target.value;
        currentPage = 1;
        loadSearchHistory();
    });

    historyEntriesSelect.addEventListener('change', function(e) {
        entriesPerPage = parseInt(e.target.value);
        currentPage = 1;
        loadSearchHistory();
    });

    clearHistoryBtn.addEventListener('click', async function() {
        if (confirm('Are you sure you want to clear all search history?')) {
            try {
                const response = await fetch('/api/search-history/clear', {
                    method: 'POST'
                });
                if (response.ok) {
                    loadSearchHistory();
                }
            } catch (error) {
                console.error('Error clearing history:', error);
            }
        }
    });

    document.getElementById('exportHistoryBtn').addEventListener('click', function() {
        window.open('/admin//api/search_history', '_blank'); // Update to include the /admin prefix
    });
           
    historyPrevBtn.addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            loadSearchHistory();
        }
    });

    historyNextBtn.addEventListener('click', function() {
        if (currentPage < totalPages) {
            currentPage++;
            loadSearchHistory();
        }
    });

    // Initial load
    loadSearchHistory();
});