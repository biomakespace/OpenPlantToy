
let HINT_DISPLAY = document.getElementById("hint");
let MATCH_DISPLAY = document.getElementById("status");
let CIRCUIT_INFORMATION_API_PATH = "/api/circuit-information";

function updateDisplayAll() {
  fetch(CIRCUIT_INFORMATION_API_PATH)
    .then(function(response) {
      if(response.ok) {
        return response.json();
      } else {
        console.error("Returned non 200 status code");
      }
    })
    .then(function(circuitInformation) {
      console.log(circuitInformation);
      console.log(circuitInformation["match"]);
      console.log(circuitInformation["hint"]);
      updateMatch(circuitInformation["match"]);
      updateHint(circuitInformation["hint"]);
    })
    .catch(function(error) {
      console.error(error);
    })
}

/*
 * Updates the part of the display
 * that indicates whether the circuit
 * matches the target circuit or not
 * circuitCorrect is a boolean
 * which specifies this
 */
function updateMatch(circuitCorrect) {
  if (circuitCorrect) {
    MATCH_DISPLAY.innerHTML = "Circuit is correct!";
  } else {
    MATCH_DISPLAY.innerHTML = "Circuit is not correct...";
  }
}

/*
 * Displays a hint that tells
 * the user how to improve
 * the circuit is one is
 * provided from the api
 * Hint should be either
 * a string (of the hint)
 * or null if no hint
 */
function updateHint(hint) {
  HINT_DISPLAY.innerHTML = hint;
}

setInterval(updateDisplayAll, 500);
