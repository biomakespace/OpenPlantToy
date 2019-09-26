
SERIAL_PORT_LIST_API_PATH = '/api/list-serial-ports';
LIST_CONTAINER_ID = 'list';

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
    listContainer.appendChild(nextLine);
  }
}

fetchSerialPortList();
