
# Represents the circuit
# that the users are
# try to build
# In addition to the Circuit
# class, adds 'hints' to
# help the users
# towards the answer

from circuit import Circuit


class TargetCircuit(Circuit):

    EMPTY_CIRCUIT_HINT = "There must be at least one component in the circuit"
    ROOT_COMPONENT_HINT = "Which genetic unit opens translation?"

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
        # If the circuit is empty
        # (no components connected)
        # default empty circuit hint
        if circuit.root_component() == "":
            return TargetCircuit.EMPTY_CIRCUIT_HINT
        # If there is a single component
        # (i.e. root exists, but no connections)
        if circuit.number_of_connections() == 0:
            # If the root component is incorrect
            if circuit.root_component() != self.connections[0].downstream:
                # Hint what it should be
                return TargetCircuit.ROOT_COMPONENT_HINT
            else:
                # Otherwise provide root connection hint
                return self.hints[0]
        # Find the first element in
        # the target circuit that
        # is not in the actual circuit
        for i in range(len(self.connections)):
            if self.connections[i].hash() not in circuit.hash():
                return self.hints[i]

    # When only one element is connected
    # to the circuit