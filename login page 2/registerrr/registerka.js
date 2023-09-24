// Your original code for handling form submission
document.querySelector("input").addEventListener("click", function () {
  var hobbies = document.getElementById("id1").value;
  var harass = document.getElementById("id2").value;
  if (checkfam(hobbies) == true && checkharas(harass) == true) {
      alert("Your message has been received");
      // Add the code to send user input to the Flask route here
      sendUserInputToFlask(harass); // Pass the 'harass' variable to the function
  } else {
      alert("Please fill both the boxes");
  }
});

function checkfam(context) {
  if (context.length != 0) {
      return true;
  } else {
      return false;
  }
}

function checkharas(context) {
  if (context.length != 0) {
      return true;
  } else {
      return false;
  }
}

// New function to send user input to Flask using AJAX
function sendUserInputToFlask(userInput) {
  fetch("/filtered-data", {
      method: "POST",
      headers: {
          "Content-Type": "application/x-www-form-urlencoded",
      },
      body: "experience=" + encodeURIComponent(userInput),
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
}

function redirectToIndex12WithData(data) {

  var index12Url = "tapusena/login%20page%202/helpers/index12.html?data=" + encodeURIComponent(JSON.stringify(data));
  
  window.location.href = index12Url;
}