// Wait for the DOM content to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
  
  // Add event listener to the submitResponses button
  document.getElementById("submitResponses").addEventListener("click", () => {
    // Submit the form when the button is clicked
    document.querySelector("form").submit();
  });

  // Get all range sliders
  const rangeSliders = document.querySelectorAll(".range-slider");

  // Mapping for range slider values
  const hashMap = {
    1: "Totally Disagree",
    2: "Slightly Disagree",
    3: "Neutral",
    4: "Slightly Agree",
    5: "Totally Agree",
  };

  // Function to update range slider labels
  function updateRangeLabel(element) {
    const rangeLabel = element.querySelector(".range-form-label");
    const rangeValue = element.querySelector(".form-range").value;
    rangeLabel.innerText = hashMap[rangeValue];
  }

  // Add event listeners to range sliders
  rangeSliders.forEach((element) => {
    element.addEventListener("input", () => {
      // Update range label when slider value changes
      updateRangeLabel(element);
    });

    // Initial update of range label
    updateRangeLabel(element);
  });

  // Add event listener to the saveResponses button
  document.getElementById("saveResponses").addEventListener("click", () => {
    // Set formCompleted value to False before submitting the form
    document.getElementById("formCompleted").value = "False";
    // Submit the form
    document.querySelector("form").submit();
  });
});

// Redirect to the jobs page
function redirectToJobs() {
  window.location.href = "/jobs";
}

// Logout function to redirect to the logout page
function logout() {
  window.location.href = "/logout";
}
