
# Takes a circuit and lays out
# the components out on a grid


class Grid:

    def __init__(self, circuit):
        self.circuit = circuit

    # Start at row 0 column 0
    # and lay out the components
    # in a grid according
    # to connectivity
    def lay_out(self):
        start_column = 1
        start_row = 1
        # Place the first call to advance row
        # with the root component
        # and start at 1 1
        return self.advance_row(self.circuit.root_component(), start_row, start_column)

    # Given a component and a start
    # position in the grid, figure out
    # whether the tree branches at this
    # point, place the component then
    # continue the grid building
    # with the required number of branches
    # Does this recursively
    def advance_row(self, component, row, column):
        connected = self.circuit.components_connected_to(component)
        component_position = [component, row, column]
        # Place the component position in an array
        positions = [component_position]
        # If there is at least one connected component
        # continue the first branch
        if len(connected) > 0:
            # A horizontal connector to next component in same row
            connector = ["-", row, column+1]
            positions = [component_position, connector] + self.advance_row(connected[0], row, column+2)
            # If there are two connected components
            # continue with a second branch
            if len(connected) == 2:
                # The next empty row
                next_row = second_branch_start_row = max([position[1] for position in positions]) + 1
                # A vertical connector
                # placed in a row one past the
                # maximum reached in the first branch
                connector = ["|", next_row, column]
                positions.append(connector)
                positions = positions + self.advance_row(connected[1], second_branch_start_row, column)
        return positions
