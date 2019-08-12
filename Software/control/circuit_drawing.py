
# This class takes a Grid object
# and produces a HTML representation
# of the circuit laid out on that
# grid which can be inserted
# into the web page


class CircuitDrawing:

    CONTAINER_STYLE_TEMPLATE = "display:grid;" \
                               + "grid-template-rows:repeat({},1fr);" \
                               + "grid-template-column:repeat({},1fr);"

    ITEM_STYLE_TEMPLATE = "grid-row-start:{0};grid-row-end:{0};" \
                          + "grid-column-start:{1};grid-column-end:{1};"

    def __init__(self, circuit_grid):
        self.grid = circuit_grid.lay_out()

    def html(self):
        total_rows = max([position[1] for position in self.grid])
        total_columns = max([position[2] for position in self.grid])
        html = '<div style="{}">'.format(
            CircuitDrawing.CONTAINER_STYLE_TEMPLATE.format(
                total_rows,
                total_columns
            )
        )
        for position in self.grid:
            html += '<div style="{}"><p>{}</p></div>"'.format(
                CircuitDrawing.ITEM_STYLE_TEMPLATE.format(
                    position[1],
                    position[2]
                ),
                position[0]
            )
        html += '</div>'
        return html
