
# A class to represent a genetic circuit
# Represented as an array of connections
# Can be a 'theoretical' circuit such
# as the one that the users are aiming for
# or a real circuit that has been built


class Circuit:

    def __init__(self):
        self.connections = []
        self.root = ""

    # Returns the number of connections
    # in this circuit
    def number_of_connections(self):
        return len(self.connections)

    # Add a new connection to the circuit
    def add_connection(self, connection):
        self.connections.append(connection)

    # Set the circuit's root component
    def set_root(self, root):
        self.root = root

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
        # Remember upstream away from controller, downstream close to controller
        for check_connection in self.connections:
            if check_connection.downstream in [connection.upstream for connection in self.connections]:
                continue
            else:
                return check_connection.downstream
        # If none can be found from connections
        # Return the one that was set
        return self.root

    # Return an array containing
    # any components which are
    # connected to the one
    # provided as an argument
    def components_connected_to(self, connected_component):
        return [connection.upstream for connection in self.connections if connection.downstream == connected_component]
