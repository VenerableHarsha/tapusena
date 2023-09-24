document.querySelector("form").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent the default form submission behavior
  
    // Get the user's input from the <textarea> with ID "id2"
    var userExperience = document.getElementById("id2").value;
  
    // Send the user's input to the Flask route using AJAX
    fetch("/filtered-data", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded", // Set the content type
      },
      body: "experience=" + encodeURIComponent(userExperience), // Encode the input data
    })
      .then(function (response) {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Server response was not ok.");
        }
      })
      .then(function (data) {
        // Handle the response from the server (data) as needed
        displayFilteredData(data); // Call a function to display the filtered data
      })
      .catch(function (error) {
        console.error("Error:", error);
      });
  });
  
  // Function to display the filtered data received from the server
  function displayFilteredData(data) {
    var ul = document.getElementById("filteredData");
    ul.innerHTML = ""; // Clear any previous data
  
    data.forEach(function (item) {
      var li = document.createElement("li");
      li.textContent = "Psychologist Type: " + item["Psychologist Type"] + ", Name: " + item["Name"];
      ul.appendChild(li);
    });
  }
  