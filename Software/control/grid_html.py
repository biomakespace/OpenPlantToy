
# Takes a grid object
# representing a circuit
# as a grid and turns
# this into a json object
# that specifies how
# to build this grid in html

# Format:
# Array of elements
# Each element is a dictionary, keys:
# element_type: String
# attributes: dictionary of attribute names/values
# children: array of child elements
# content: text content (innerHTML)

class GridHtml():

    def __init__(self, grid):
        self.grid = grid
        self.html = {}