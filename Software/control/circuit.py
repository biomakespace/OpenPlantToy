
# A class to represent a genetic circuit
# Represented as an array of connections
# Can be a 'theoretical' circuit such
# as the one that the users are aiming for
# or a real circuit that has been built


class Circuit:

    def __init__(self):
        self.connections = []

    # Returns the number of connections
    # in this circuit
    def number_of_connections(self):
        return len(self.connections)

    # Add a new connection to the circuit
    def add_connection(self, connection):
        self.connections.append(connection)

    # Return a hash for the circuit
    # which is the concatenated hashes
    # of the connections is contains
    def hash(self):
        hashes = [connection.hash() for connection in self.connections]
        hashes = sorted(hashes)
        return "".join(hashes)

    # Check if this circuit equals the provided circuit
    def equals(self, circuit):
        return self.hash() == circuit.hash()

    # Generator for connections
    # def elements(self):
    #     for connection in self.connections:
    #         yield connection

    # Finds the 'root component'
    # that is the one closest to the controller
    # The root component will appear as
    # in an upstream position but never
    # in a downstream position
    def root_component(self):
        for check_connection in self.connections:
            if check_connection.upstream in [connection.downstream for connection in self.connections]:
                continue
            else:
                return check_connection
