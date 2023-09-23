document.addEventListener('DOMContentLoaded', function() {
    const fetchDataBtn = document.getElementById('fetchDataBtn');
    const filteredDataElement = document.getElementById('filtered-data');

    fetchDataBtn.addEventListener('click', function() {
        // Fetch the filtered data from the Flask route
        fetch('/filtered-data')
            .then(response => response.text())
            .then(data => {
                filteredDataElement.textContent = data;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });
});
