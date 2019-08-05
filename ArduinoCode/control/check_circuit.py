
# Needed for serial communication
# with the base unit
import sys
import serial
import datetime

# Import this package's classes
from connection import Connection
from circuit import Circuit
from target_circuit import TargetCircuit


def milliseconds_elapsed_since(initial_time):
    time_difference = datetime.datetime.now() - initial_time
    return (time_difference.seconds/1000.0) + (time_difference.microseconds*1000)


# inertia + 1 = number of incorrect responses before turning off the light
inertia = 2

# Open the serial port on which the circuit component is connected
try:
    serial1 = serial.Serial("/dev/ttyUSB1", 4800, timeout=1)
except serial.SerialException:
    print("Could not open serial port for communication. Exiting.")
    sys.exit(1)
# serial2 = serial.Serial( "/dev/ttyUSB1" , 4800 , timeout=3 )
# Print the name of the serial port, debug information
print("Opened communication with ", serial1.name)

# The internal circuit representation of the
# circuit which is "correct"
correct_circuit = TargetCircuit()
correct_circuit.add_connection(Connection("TRM", "REP"), "TRM must be followed by REP")
# [ "TRM" , "REP" ]
# [ "TRM" , "3UT" ]
# [ "3UT" , "FRT" ]
# [ "FRT" , "5UT" ]
# [ "5UT" , "PRM" ]
# [ "PRM" , "REP" ]
# [ "REP" , "DRP" ]

# Initial message to circuit, assuming incorrect circuit
response = "TRM,OFF;"

# Count how many incorrect responses we've had since last correct one
incorrect = 0

# How long to wait for responses in milliseconds
RESPONSE_WAIT_TIMEOUT = 1000

# Forever (until broken)
while True:
    
    # New logic
    
    # Send something out
    try:
        serial1.write(response.encode('ascii'))
    except serial.SerialException:
        # Break & quit if connection lost
        print("Serial connection seems to be lost. Stopping.")
        break
    
    # Store parsed connections here
    assembled_circuit = Circuit()

    # Wait a while to get a bunch of responses
    start_time = datetime.datetime.now()
    while milliseconds_elapsed_since(start_time) < RESPONSE_WAIT_TIMEOUT:
        pass

    # Get any received response, and decode from bytes to string
    received = serial1.read(50).decode("ascii")
    # Split by ,
    messages = received.split(",")
    # Split by any ;, append results to array
    for message in messages:
        messages = messages + message.split(";")
    # Throw out anything with ; in it
    messages = [m for m in messages if ";" not in m]
    # Throw out anything without a dash
    messages = [m for m in messages if "-" in m]
    # --- Add those responses into a circuit representation as received
    # Split the messages by the dash ID1-ID2
    # yielding connections in format [ID1,ID2]
    for message in messages:
        assembled_circuit.add_connection(
            Connection(
                message.split("-")[0],
                message.split("-")[1]
            )
        )
    
    # Check against correct representation
    # Update response based on this
        
    # Print response, debug information
    print("From circuit:", assembled_circuit.hash())

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
        if correct_circuit.equals(assembled_circuit):
            # If so reset number of incorrect circuits reported
            incorrect = 0
            # Confirm match, debug information
            print("MATCH")
            # Set response for correct circuit
            response = "TRM,ON;"
        # If reported circuit does not match the correct circuit
        else:
            # Increment number of incorrect responses seen
            incorrect += 1
            # Report lack of match, debug information
            print("NO MATCH")
            # If there have been too many incorrect responses,
            # set the response for an incorrect circuit
            if incorrect > inertia:
                response = "TRM,OFF;"

    # Catch all exceptions and do nothing with them, for now
    # To be improved in the future
    # Note that this means that the response sent to the circuit on
    # the next iteration of the loop, will be the same as the one
    # send earlier in this iteration
    except Exception as e :
        pass

    # Separator between loops, for better legibility of debug information
    print("###############")
