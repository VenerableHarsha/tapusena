// Fetch the filtered data from the server and update the webpage
fetch('filtered-data.txt')
    .then(response => response.text())
    .then(data => {
        const filteredDataElement = document.getElementById('filtered-data');
        filteredDataElement.textContent = data;
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
