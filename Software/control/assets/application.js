
let HINT_DISPLAY = document.getElementById("hint");
let MATCH_DISPLAY = document.getElementById("status");
let DIAGRAM_DISPLAY_ID = "diagram";
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
      // TODO DEBUG REMOVE
      console.log(circuitInformation);
      console.log(circuitInformation["match"]);
      console.log(circuitInformation["hint"]);
      console.log(circuitInformation["html"]);
      updateMatch(circuitInformation["match"]);
      updateHint(circuitInformation["hint"]);
      updateDrawing(circuitInformation["html"]);
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

/*
 * Takes a json version of
 * the html representation
 * of the current circuit
 * and converts this into
 * a DOM element to insert
 *
 * Structure of json
 * html = [
 *   {
 *     children: [child element information],
 *     attributes: {
 *       attribute-name: attribute-value
 *     },
 *     element_type: div/a/p/etc...,
 *     content: text content/innerHTML
 *   }
 * ]
 */
function updateDrawing(diagramHtml) {
  // Delete old drawing, need to get each time since element deleted/recreated
  let oldDrawingElement = document.getElementById(DIAGRAM_DISPLAY_ID);
  if (oldDrawingElement != null) {
    oldDrawingElement.parentNode.removeChild(oldDrawingElement);
  }
  // Insert new drawing into document
  MATCH_DISPLAY.insertAdjacentHTML("afterend", diagramHtml);
}

// function domElementsFromJson(rootElementJson) {
//   // Steps
//   // Create new element
//   // Set innerHTML to content
//   // Set each attribute value pair
//   // Call draw function on all children
//   // Insert children as children of this element
//   // Return element
// }

setInterval(updateDisplayAll, 2000);
