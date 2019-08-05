
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
