// Add this to your JavaScript file (search_history.js)
document.addEventListener('DOMContentLoaded', function() {
    // Initialize search history functionality
    initSearchHistory();
});

function initSearchHistory() {
    const historyTable = document.getElementById('historyTableBody');
    const historySearchInput = document.getElementById('historySearchInput');
    const historyEntriesSelect = document.getElementById('historyEntriesSelect');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    const exportHistoryBtn = document.getElementById('exportHistoryBtn');
    const historyEntriesInfo = document.getElementById('historyEntriesInfo');

    // Pagination controls
    const historyPrevBtn = document.getElementById('historyPrevBtn');
    const historyNextBtn = document.getElementById('historyNextBtn');
    const historyCurrentPage = document.getElementById('historyCurrentPage');
    
    let currentPage = 1;
    let entriesPerPage = 10;

    // Function to load search history data
    function loadSearchHistory() {
        fetch('/api/search-history')
            .then(response => response.json())
            .then(data => {
                updateHistoryTable(data);
            })
            .catch(error => console.error('Error loading search history:', error));
    }

    // Function to update the history table
    function updateHistoryTable(data) {
        historyTable.innerHTML = '';
        
        data.forEach((entry, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap">${index + 1}</td>
                <td class="px-6 py-4 whitespace-nowrap">${entry.username}</td>
                <td class="px-6 py-4">${entry.keyword}</td>
                <td class="px-6 py-4">
                    ${entry.query_image ? `<img src="${entry.query_image}" class="h-16 w-16 object-cover rounded">` : 'No image'}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">${formatDateTime(entry.timestamp)}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <button class="text-red-600 hover:text-red-900" onclick="deleteHistoryEntry(${entry.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            historyTable.appendChild(row);
        });
    }

    // Function to format date and time
    function formatDateTime(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleDateString('id-ID') + ' ' + date.toLocaleTimeString('id-ID');
    }

    // Event listener for search input
    historySearchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const rows = historyTable.getElementsByTagName('tr');
        
        Array.from(rows).forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });

    // Event listener for entries select
    historyEntriesSelect.addEventListener('change', function(e) {
        entriesPerPage = parseInt(e.target.value);
        currentPage = 1;
        loadSearchHistory();
    });

    // Clear all history
    clearHistoryBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear all search history?')) {
            fetch('/api/clear-search-history', {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(() => {
                loadSearchHistory();
            })
            .catch(error => console.error('Error clearing history:', error));
        }
    });

    // Export history
    exportHistoryBtn.addEventListener('click', function() {
        fetch('/api/export-search-history')
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'search_history.csv';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            })
            .catch(error => console.error('Error exporting history:', error));
    });

    // Initialize the table
    loadSearchHistory();

    // Set up real-time updates using WebSocket
    const socket = new WebSocket('ws://' + window.location.host + '/ws/search-history');
    
    socket.onmessage = function(event) {
        const newSearch = JSON.parse(event.data);
        // Prepend new search entry to the table
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">1</td>
            <td class="px-6 py-4 whitespace-nowrap">${newSearch.username}</td>
            <td class="px-6 py-4">${newSearch.keyword}</td>
            <td class="px-6 py-4">
                ${newSearch.query_image ? `<img src="${newSearch.query_image}" class="h-16 w-16 object-cover rounded">` : 'No image'}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">${formatDateTime(newSearch.timestamp)}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <button class="text-red-600 hover:text-red-900" onclick="deleteHistoryEntry(${newSearch.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        historyTable.insertBefore(row, historyTable.firstChild);
        
        // Update row numbers
        updateRowNumbers();
    };

    function updateRowNumbers() {
        const rows = historyTable.getElementsByTagName('tr');
        Array.from(rows).forEach((row, index) => {
            const numberCell = row.cells[0];
            if (numberCell) {
                numberCell.textContent = index + 1;
            }
        });
    }

    // Function to delete individual history entry
    window.deleteHistoryEntry = function(id) {
        if (confirm('Are you sure you want to delete this entry?')) {
            fetch(`/api/search-history/${id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(() => {
                loadSearchHistory();
            })
            .catch(error => console.error('Error deleting entry:', error));
        }
    };
}
