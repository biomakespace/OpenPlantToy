
SERIAL_PORT_LIST_API_PATH = '/api/list-serial-ports'

function getSerialPortList() {
  fetch(SERIAL_PORT_LIST_API_PATH, {method=GET})
    .then(function(response) {
      if(response.ok) {
        return response.json();
      } else {
        console.error("Returned non 200 status code");
      }
    })
    .then(function(serialPortList) {
      console.log(serialPortList);
    })
    .catch(function(error) {
      console.error(error);
    })
}

setTimeout(1000, getSerialPortList);
