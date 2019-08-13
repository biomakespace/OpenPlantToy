
# Run the web server to
# serve the gui
# for the controller

from control.target_circuit import TargetCircuit
from control.connection import Connection


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

    # Set up target circuit

    # Set up checking class

    # Run checking class in thread

    # Set up web server

    # Run web server
