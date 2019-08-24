
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


class GridHtml:

    # These should be set per circuit
    # To ensure the display looks good
    MAXIMUM_ROWS = 2
    MAXIMUM_COLUMNS = 5

    CONTAINER_STYLE_TEMPLATE = (
        "display:grid;"                                     # Grid display
        + "grid-template-rows:repeat({},1fr);"              # Number of rows
        + "grid-template-columns:repeat({},1fr);"            # Number of columns
        + "align-items:center;justify-items:stretch;"        # Centre items horizontally & vertically
    )

    ITEM_STYLE_TEMPLATE = "grid-row-start:{0};grid-row-end:{0};" \
                          + "grid-column-start:{1};grid-column-end:{1};"

    DIAGRAM_ELEMENT_ID = "diagram"

    COMPONENT_STYLE_CLASS = "component"

    def __init__(self, grid):
        self.grid = grid.lay_out()
        self.html = {}

    def get_json(self):
        container = self.container_element()
        components = ''
        for component in self.grid:
            components += self.component_element(component)
        return container.format(components)

    # Create the div container
    # for the diagram
    def container_element(self):
        total_rows = GridHtml.MAXIMUM_ROWS
        total_columns = GridHtml.MAXIMUM_COLUMNS
        return '<div style="{}" id="{}">{}</div>'.format(
            GridHtml.CONTAINER_STYLE_TEMPLATE.format(
                total_rows,
                total_columns
            ),
            GridHtml.DIAGRAM_ELEMENT_ID,
            '{}'
        )

    # Create a html element
    # for a provided component
    def component_element(self, component):
        # Remember: [id, row, column]
        return '<div style="{}" class="{}"><p>{}</p></div>'.format(
            GridHtml.ITEM_STYLE_TEMPLATE.format(
                component[1],
                component[2]
            ),
            GridHtml.COMPONENT_STYLE_CLASS,
            component[0]
        )
