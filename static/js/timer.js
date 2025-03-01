<script>
  let timerInterval; // Store the interval ID
  let totalTime = 25 * 60; // 25 minutes in seconds
  let remainingTime = totalTime; // Remaining time in seconds
  const timerElement = document.getElementById("timer");

  // Function to format time as MM:SS
  function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }

  // Function to update the timer display
  function updateTimerDisplay() {
    timerElement.textContent = formatTime(remainingTime);
  }

  // Start button functionality
  document.getElementById("startButton").addEventListener("click", function () {
    if (!timerInterval) { // Prevent multiple intervals
      timerInterval = setInterval(() => {
        if (remainingTime > 0) {
          remainingTime--;
          updateTimerDisplay();
        } else {
          clearInterval(timerInterval);
          alert("Time's up!");
        }
      }, 1000);
    }
  });

  // Stop button functionality
  document.getElementById("stopButton").addEventListener("click", function () {
    clearInterval(timerInterval);
    timerInterval = null; // Reset the interval
  });

  // Restart button functionality
  document.getElementById("restartButton").addEventListener("click", function () {
    clearInterval(timerInterval);
    timerInterval = null;
    remainingTime = totalTime; // Reset to 25 minutes
    updateTimerDisplay();
  });

  // Initialize the timer display
  updateTimerDisplay();
</script>
