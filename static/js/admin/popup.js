document.addEventListener('DOMContentLoaded', function() {
    const datasetModal = document.getElementById('datasetInfoModal');
    const labelModal = document.getElementById('labelInfoModal');
    const closeBtns = document.querySelectorAll('.close-button');
    const datasetInfoBtn = document.getElementById('datasetInfoBtn');
    const labelInfoBtn = document.getElementById('labelInfoBtn');
    const datasetInfoTable = document.getElementById('datasetInfoTable');
    const labelInfoTable = document.getElementById('labelInfoTable');
    const totalDatasetElement = document.getElementById('totalDataset');
    const totalLabelsElement = document.getElementById('totalLabels');

    function openModal(modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    function closeModal(modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    datasetInfoBtn.addEventListener('click', function() {
        openModal(datasetModal);
        fetchDatasetInfo();
    });

    labelInfoBtn.addEventListener('click', function() {
        openModal(labelModal);
        fetchLabelInfo();
    });

    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            closeModal(btn.closest('.dataset-modal'));
        });
    });

    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('dataset-modal')) {
            closeModal(e.target);
        }
    });

    function fetchDatasetInfo() {
        fetch('/dashboard_admin', {
            method: 'POST',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log("Fetched Dataset Data:", data);
            datasetInfoTable.innerHTML = '';
            let totalCount = 0;

            data.dataset_info.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${item.fabric_name}</td><td>${item.count}</td>`;
                datasetInfoTable.appendChild(row);
                totalCount += item.count;
            });

            totalDatasetElement.textContent = totalCount;
        })
        .catch(error => console.error('Error fetching dataset info:', error));
    }

 // Fungsi untuk fetch data label
function fetchLabelInfo() {
    fetch('/dashboard_admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log("Fetched Label Data:", data);
        labelInfoTable.innerHTML = '';
        
        // Populate table with label data
        data.label_info.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.fabric_name}</td>
            `;
            labelInfoTable.appendChild(row);
        });
        
        // Update total labels count
        const totalCountElement = document.getElementById('totalCount');
        totalCountElement.textContent = data.label_info.length;
    })
    .catch(error => {
        console.error('Error fetching label info:', error);
        labelInfoTable.innerHTML = '<tr><td colspan="3">Error loading data</td></tr>';
    });
}
});