
# Handles requests made
# to the server

from http.server import BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pass

    def page_check_circuit(self):
        pass

    def api_circuit_information(self):
        pass
