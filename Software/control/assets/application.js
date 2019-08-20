
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
      if (circuitInformation["match"]) {
        MATCH_DISPLAY.innerHTML = "Circuit is correct!";
      } else {
        MATCH_DISPLAY.innerHTML = "Circuit is not correct...";
      }
      HINT_DISPLAY.innerHTML = circuitInformation["hint"];
    })
    .catch(function(error) {
      console.error(error);
    })
}



setInterval(updateDisplayAll, 500);
