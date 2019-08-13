
# Run the web server to
# serve the gui
# for the controller

import threading

from control.target_circuit import TargetCircuit
from control.connection import Connection
from control.check_circuit import open_serial
from control.check_circuit import set_target
from control.check_circuit import get_instance

SERIAL_PATH = '/dev/ttyUSB0'
BAUD_RATE = 4800


def run():
    # The representation of the
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

    # Set up checking class
    open_serial(SERIAL_PATH, BAUD_RATE)
    set_target(correct_circuit)
    circuit_checker = get_instance()

    # Run checking class in thread
    circuit_checking_thread = threading.Thread(target=circuit_checker.run)
    circuit_checking_thread.start()

    # Set up web server

    # Run web server
