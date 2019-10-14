
# Needed for serial communication
# with the base unit
import datetime
import json
import serial
import time

# Import this package's classes
from circuit import Circuit
from connection import Connection
from grid import Grid
from grid_html import GridHtml


TIME_BETWEEN_CHECKS = 1000
LATEST_CONNECTIONS_REQUEST = "LATEST;".encode("ASCII")
IDENTIFY_REQUEST = "WHOGOESTHERE;".encode("ASCII")
IDENTIFY_RESPONSE = "OPENPLANTTOY"


# Need to be static methods

def set_baud_rate(baud_rate):
    CircuitChecker.baud_rate = baud_rate


# Try to open the serial port
# Must be successfully
# completed before the class
# can be used
def open_serial(serial_path):
    CircuitChecker.serial_path = serial_path
    try:
        connection = serial.Serial(
            CircuitChecker.serial_path,
            CircuitChecker.baud_rate,
            timeout=0
        )
        CircuitChecker.connection = connection
        CircuitChecker.instance = CircuitChecker()
        print("Opened communication with ", CircuitChecker.connection.name)
        return True
    except serial.SerialException:
        print("Could not open serial port for communication.")
        return False


# Helper method to calculate
# time elapsed in ms
def milliseconds_elapsed_since(initial_time):
    time_difference = datetime.datetime.now() - initial_time
    return (time_difference.seconds * 1000.0) + (time_difference.microseconds / 1000)


# Helper method to await response
def await_response():
    time.sleep(TIME_BETWEEN_CHECKS/1000.0)


# Check for a valid(ish) response
# to see if the serial port set
# is the correct one
def validate_port():
    # Send twice (seems to work...)
    for i in [0, 1]:
        await_response()
        try:
            # Clear previous response first
            CircuitChecker.connection.reset_input_buffer()
            # Then get the connection information from the circuit
            CircuitChecker.connection.write(IDENTIFY_REQUEST)
        except (serial.SerialException, AttributeError):
            return False
        # Wait for a response
        await_response()
        response_bytes = CircuitChecker.connection.read(50)
        print(response_bytes)
    # Should return json, only ascii, has msg key, specific value for that key
    try:
        response_raw = response_bytes.decode("ascii")
        response_raw = response_raw.replace(";", "")
        response_parsed = json.loads(response_raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False
    if "msg" not in response_parsed:
        return False
    else:
        return response_parsed["msg"] == IDENTIFY_RESPONSE


# Set the target circuit
# Must be done before the
# class can be used
def set_target(circuit):
    CircuitChecker.target_circuit = circuit


# Return an instance if one
# has already been set
# Otherwise, check if both
# the connection and the
# target have been set, and if
# so create the instance and
# return it
def get_instance():
    if CircuitChecker.instance is not None:
        return CircuitChecker.instance
    elif CircuitChecker.connection is not None and CircuitChecker.target_circuit is not None:
        CircuitChecker.instance = CircuitChecker()
        return CircuitChecker.instance
    return None


class CircuitChecker:

    # Serial parameters
    serial_path = ""
    baud_rate = 0
    # Class intended to be singleton
    instance = None
    connection = None
    # Correct circuit
    target_circuit = None
    # Count the number of
    # subsequent incorrect responses
    incorrect = 0
    # inertia + 1 =
    # number of incorrect responses
    # before turning off the light
    inertia = 2
    # Response sent to circuit
    response = "A,B;"
    # Last received information about circuit
    circuit_information = {}

    def __init__(self):
        pass   # Nothing to do

    # Get the current circuit status
    # and send an update to turn
    # on/off LEDs, etc
    def check(self):

        try:
            # Clear previous response first
            CircuitChecker.connection.reset_input_buffer()
            # Then get the connection information from the circuit
            CircuitChecker.connection.write(CircuitChecker.response.encode('ascii'))
            # Then place a request for the latest circuit information
            CircuitChecker.connection.write(LATEST_CONNECTIONS_REQUEST)
        except serial.SerialException:
            # TODO REMOVE (DEBUG)
            print("Serial connection seems to be lost.")

        # Wait a while to get a bunch of responses
        start_time = datetime.datetime.now()
        while milliseconds_elapsed_since(start_time) < TIME_BETWEEN_CHECKS:
            pass

        # Get any received response, and decode from bytes to string
        assembled_circuit = self.parse_responses(CircuitChecker.connection.read(50).decode("ascii"))

        # TODO REMOVE (DEBUG)
        print("From circuit: ", assembled_circuit.hash())

        CircuitChecker.circuit_information["html"] = GridHtml(Grid(assembled_circuit)).get_json()

        # I think the main point of failure would be
        # the first line, the call to parse_tree, if
        # the string reported by the circuit is not well formed
        # Potentially the tree_match call could produce an error
        # if one of the arrays of connections is ill-formed
        # but this should either be very unlikely to happen
        # or happen every time if the "correct" circuit
        # is not set up correctly at the start
        try:
            # Check if reported circuit matches correct circuit
            if CircuitChecker.target_circuit.equals(assembled_circuit):
                # If so reset number of incorrect circuits reported
                CircuitChecker.incorrect = 0
                CircuitChecker.circuit_information['match'] = True
                CircuitChecker.circuit_information['hint'] = None
                # TODO REMOVE (DEBUG)
                print("MATCH")
                # Set response for correct circuit
                CircuitChecker.response = "TRM,ON;"
            # If reported circuit does not match the correct circuit
            else:
                # Increment number of incorrect responses seen
                CircuitChecker.incorrect += 1
                CircuitChecker.circuit_information['match'] = False
                # Report lack of match, debug information
                print("NO MATCH")
                print(CircuitChecker.target_circuit.get_next_hint(assembled_circuit))
                CircuitChecker.circuit_information['hint'] = CircuitChecker.target_circuit.get_next_hint(
                    assembled_circuit
                )
                # If there have been too many incorrect responses,
                # set the response for an incorrect circuit
                if CircuitChecker.incorrect > CircuitChecker.inertia:
                    CircuitChecker.response = "TRM,OFF;"

        # Catch all exceptions and do nothing with them, for now
        # To be improved in the future
        # Note that this means that the response sent to the circuit on
        # the next iteration of the loop, will be the same as the one
        # send earlier in this iteration
        except Exception as e :
            pass

        # try:
        #     CircuitChecker.connection.write(CircuitChecker.response.encode('ascii'))
        # except serial.SerialException:
        #     # TODO REMOVE (DEBUG)
        #     print("Serial connection seems to be lost.")

        # TODO REMOVE (DEBUG)
        print(CircuitChecker.circuit_information)

    # Helper method to parse
    # the received responses
    # and turn them into
    # a Circuit representation
    def parse_responses(self, received):
        # Should get json back
        try:
            response = json.loads(received)
        except json.JSONDecodeError:
            # If it fails, return 'null' circuit
            return Circuit()
        # Start building the circuit
        circuit = Circuit()
        # Check for root_component
        if "root" in response:
            root_component = response["root"]
        else:
            root_component = ""
        circuit.set_root(root_component)
        # Get the connections
        if "connections" in response:
            for connection in response["connections"]:
                # Double check the format is correct
                if "-" in connection:
                    circuit.add_connection(
                        Connection(
                            connection.split("-")[0],
                            connection.split("-")[1]
                        )
                    )
        return circuit

    def run(self):
        while True:
            self.check()

    def get_circuit_information(self):
        return CircuitChecker.circuit_information

