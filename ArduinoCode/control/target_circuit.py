
# Represents the circuit
# that the users are
# try to build
# In addition to the Circuit
# class, adds 'hints' to
# help the users
# towards the answer

from circuit import Circuit


class TargetCircuit(Circuit):

    def __init__(self):
        self.connections = []
        self.hints = []

    def add_connection(self, connection, hint):
        self.connections.append(connection)
        self.hints.append(hint)

    # For the given 'actual' circuit
    # identify the hint to be provided
    # to the users for the next connection
    def get_next_hint(self, circuit):
        # Find the first element in
        # the target circuit that
        # is not in the actual circuit
        for i in range(len(self.connections)):
            if self.connections[i].hash() not in circuit.hash():
                return self.hints[i]
