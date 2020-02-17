
const SERIAL_PORT_LIST_API_PATH = '/api/list-serial-ports';
const SERIAL_PORT_SELECT_API_PATH = '/api/confirm-serial-port';
const LIST_CONTAINER_ID = 'list';

// Get a list of serial ports from the API
function fetchSerialPortList() {
  fetch(SERIAL_PORT_LIST_API_PATH, {"method": "GET"})
    .then(function(response) {
      if(response.ok) {
        return response.json();
      } else {
        console.error("Returned non 200 status code");
      }
    })
    .then(function(serialPortList) {
      displaySerialPortList(serialPortList);
    })
    .catch(function(error) {
      console.error(error);
    });
}

/*
 * Take a list of serial ports from the API
 * and produce the buttons that allow selection
 */
function displaySerialPortList(serialPortList) {
  let listContainer = document.querySelector("#" + LIST_CONTAINER_ID);
  for (i=0; i<serialPortList.length; i++) {
    let port = serialPortList[i];
    let portText = port["description"] + "   " + port["path"];
    // Create button, set attributes
    let nextLine = document.createElement("input");
    nextLine.setAttribute("type", "button");
    nextLine.setAttribute("path", port["path"]);
    nextLine.setAttribute("value", portText);
    nextLine.setAttribute("onclick", "sendSelection(event)");
    listContainer.appendChild(nextLine);
  }
}

function sendSelection(event) {
  let selectedPath = event.target.getAttribute("path");
  let postData = {
    "path": selectedPath
  };
  fetch(
    SERIAL_PORT_SELECT_API_PATH,
    {
      "method": "POST",
      "body": JSON.stringify(postData)
    }
  ).then(function(response) {
      if(response.ok) {
        return response.json();
      } else {
        console.error("Returned non 200 status code");
      }
    })
    .then(function(portStatus) {
      // Does the port appear to be working?
      if (portStatus["success"]) {
        window.location.href = '/check-circuit';
      } else {
        document.location.reload(true);
      }
    })
    .catch(function(error) {
      console.error(error);
    });
}

fetchSerialPortList();
