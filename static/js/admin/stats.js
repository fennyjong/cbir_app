// Initialize charts
let userActivityChart;
let datasetChart;

// Chart configuration
const chartConfig = {
    type: 'line',
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Activity Over Time'
            }
        }
    }
};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    // Create initial charts
    userActivityChart = new Chart(
        document.getElementById('userActivityCanvas'),
        {
            ...chartConfig,
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Logins',
                        borderColor: 'rgb(75, 192, 192)',
                        data: [],
                        tension: 0.1
                    },
                    {
                        label: 'Registrations',
                        borderColor: 'rgb(255, 99, 132)',
                        data: [],
                        tension: 0.1
                    }
                ]
            },
            options: {
                ...chartConfig.options,
                plugins: {
                    ...chartConfig.options.plugins,
                    title: {
                        ...chartConfig.options.plugins.title,
                        text: 'User Activity'
                    }
                }
            }
        }
    );

    datasetChart = new Chart(
        document.getElementById('datasetCanvas'),
        {
            ...chartConfig,
            data: {
                labels: [],
                datasets: [{
                    label: 'Datasets',
                    borderColor: 'rgb(153, 102, 255)',
                    data: [],
                    tension: 0.1
                }]
            },
            options: {
                ...chartConfig.options,
                plugins: {
                    ...chartConfig.options.plugins,
                    title: {
                        ...chartConfig.options.plugins.title,
                        text: 'Dataset Growth'
                    }
                }
            }
        }
    );

    // Load initial data (daily by default)
    setTimeframe('daily');
});

function setTimeframe(timeframe) {
    // Update active button state
    document.querySelectorAll('.timeframe-buttons button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`button[onclick="setTimeframe('${timeframe}')"]`).classList.add('active');

    // Fetch and update data
    fetch(`/api/stats/${timeframe}`)
        .then(response => response.json())
        .then(data => {
            updateCharts(data, timeframe);
            updateTotals(data.totals);
        })
        .catch(error => console.error('Error fetching stats:', error));
}

function updateCharts(data, timeframe) {
    // Get all unique dates across all datasets
    const dates = [...new Set([
        ...Object.keys(data.logins),
        ...Object.keys(data.registrations),
        ...Object.keys(data.datasets)
    ])].sort();

    // Update user activity chart
    userActivityChart.data.labels = dates;
    userActivityChart.data.datasets[0].data = dates.map(date => data.logins[date] || 0);
    userActivityChart.data.datasets[1].data = dates.map(date => data.registrations[date] || 0);
    userActivityChart.update();

    // Update dataset chart
    datasetChart.data.labels = dates;
    datasetChart.data.datasets[0].data = dates.map(date => data.datasets[date] || 0);
    datasetChart.update();
}

function updateTotals(totals) {
    // Update the summary cards with real-time totals from the database
    document.getElementById('total-logins').textContent = totals.total_logins.toLocaleString();
    document.getElementById('total-registrations').textContent = totals.total_registrations.toLocaleString();
    document.getElementById('total-datasets').textContent = totals.total_datasets.toLocaleString();
}