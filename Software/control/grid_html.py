
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
    MAXIMUM_ROWS = 3
    MAXIMUM_COLUMNS = 8

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

    HORIZONTAL_CONNECTOR_SVG = (
        '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"'
        + ' xmlns:xlink="http://www.w3.org/1999/xlink"'
        + ' viewBox="0 0 100 100" xml:space="preserve">'
        + '<path d="M 0,50 H 100" class="connector"/></svg>'
    )

    VERTICAL_CONNECTOR_SVG = (
        '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg"'
        + ' xmlns:xlink="http://www.w3.org/1999/xlink"'
        + ' viewBox="0 0 100 100" xml:space="preserve">'
        + '<path d="M 50,0 V 100" class="connector"/></svg>'
    )

    def __init__(self, grid):
        self.grid = grid.lay_out()
        self.html = {}

    def get_json(self):
        container = self.container_element()
        components = ''
        for component in self.grid:
            if component[0] == "-":
                components += self.horizontal_connector(component)
            elif component[0] == "|":
                components += self.vertical_connector(component)
            else:
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

    # A html element
    # that will draw a
    # horizontal connector
    # between two components
    # in the same row
    def horizontal_connector(self, component):
        # Remember: [id/type, row, column]
        return '<div style="{}">{}</div>'.format(
            GridHtml.ITEM_STYLE_TEMPLATE.format(
                component[1],
                component[2]
            ),
            GridHtml.HORIZONTAL_CONNECTOR_SVG
        )

    # A html element
    # that will draw a
    # vertical connector
    # between two components
    # in the same column
    def vertical_connector(self, component):
        # Remember: [id/type, row, column]
        return '<div style="{}">{}</div>'.format(
            GridHtml.ITEM_STYLE_TEMPLATE.format(
                component[1],
                component[2]
            ),
            GridHtml.VERTICAL_CONNECTOR_SVG
        )