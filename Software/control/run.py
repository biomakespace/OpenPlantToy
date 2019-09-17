
# Run the web server to
# serve the gui
# for the controller

import threading
from http.server import HTTPServer

from target_circuit import TargetCircuit
from connection import Connection
from check_circuit import open_serial
from check_circuit import set_target
from check_circuit import get_instance
from http_server import RequestHandler

SERIAL_PATH = '/dev/ttyUSB0'
BAUD_RATE = 4800
SERVER_PORT = 12221


def run():

    # The representation of the
    # circuit which is "correct"
    correct_circuit = TargetCircuit()

    correct_circuit.add_connection(
        Connection("5UT", "FRT"),
        "What would you expect to find after the leader sequence?"
    )

    correct_circuit.add_connection(
        Connection("FRT", "3UT"),
        "What must follow the translation termination codon?"
    )

    correct_circuit.add_connection(
        Connection("3UT", "TRM"),
        "Which unit signals the end of transcription?"
    )

    # [ "TRM" , "REP" ]
    # [ "TRM" , "3UT" ]
    # [ "3UT" , "FRT" ]
    # [ "FRT" , "5UT" ]
    # [ "5UT" , "PRM" ]
    # [ "PRM" , "REP" ]
    # [ "REP" , "DRP" ]

    # Set up checking class
    # open_serial(SERIAL_PATH, BAUD_RATE)
    # set_target(correct_circuit)
    # circuit_checker = get_instance()

    # Quit if serial can't be opened
    # if not circuit_checker:
    #     exit(1)

    # Run checking class in thread
    # circuit_checking_thread = threading.Thread(target=circuit_checker.run)
    # circuit_checking_thread.start()

    # Start web server
    server = HTTPServer(("", SERVER_PORT), RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    run()
