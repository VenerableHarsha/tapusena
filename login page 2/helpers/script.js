document.addEventListener('DOMContentLoaded', function() {
    const dataRowsContainer = document.getElementById('data-rows');
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const body = document.body;

    // Function to toggle the theme
    function toggleTheme() {
        if (body.classList.contains('dark-theme')) {
            body.classList.remove('dark-theme');
            body.classList.add('light-theme');
        } else {
            body.classList.remove('light-theme');
            body.classList.add('dark-theme');
        }
    }

    // Event listener for the theme toggle button
    themeToggleBtn.addEventListener('click', toggleTheme);

    // Function to load data and apply theme
    function loadDataAndTheme() {
        // Send a POST request to the Flask route when the page loads
        fetch('/filtered-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'experience=', // You can keep it empty if no input is needed
        })
        .then(response => response.json())
        .then(data => {
            // Clear existing data rows
            dataRowsContainer.innerHTML = '';

            // Create and append rows for each dictionary
            data.forEach(rowData => {
                const row = document.createElement('tr');
                for (const key in rowData) {
                    const cell = document.createElement('td');
                    cell.textContent = rowData[key];
                    row.appendChild(cell);
                }
                dataRowsContainer.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });

        // Apply the initial theme (you can set it to dark or light by default)
        toggleTheme();
    }

    // Load data and apply theme when the page loads
    loadDataAndTheme();
});
