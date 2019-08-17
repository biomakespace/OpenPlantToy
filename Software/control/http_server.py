
# Handles requests made
# to the server

import json
from http.server import BaseHTTPRequestHandler

from control.check_circuit import get_instance


class RequestHandler(BaseHTTPRequestHandler):

    CHECK_CIRCUIT_PATH = 'check-circuit'

    def do_GET(self):
        if self.path == RequestHandler.CHECK_CIRCUIT_PATH:
            self.page_check_circuit()
        if self.path == 'api/circuit-information':
            self.api_circuit_information()
        if self.path == '/':
            self.root()
        else:
            self.page_not_found()

    def page_check_circuit(self):
        asset_path = 'assets/check-circuit.html'
        body = self.read_file_bytes(asset_path)
        if len(body) > 0:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(500, 'Internal Server Error')
            self.end_headers()

    def api_circuit_information(self):
        # Get an instance of the checker
        circuit_checker = get_instance()
        # 200 status code
        self.send_response(200)
        self.end_headers()
        # Write out the circuit information in the body
        # Information is json, so serialise & encode
        self.wfile.write(
            json.dumps(
                circuit_checker.get_circuit_information()
            ).encode('utf-8')
        )

    # If page not found
    # Redirect to root
    def page_not_found(self):
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    # From root redirect
    # to check circuit path
    def root(self):
        self.send_response(302)
        self.send_header("Location", RequestHandler.CHECK_CIRCUIT_PATH)
        self.end_headers()

    #
    # Helper methods
    #

    # Helper method to read
    # in a whole file as bytes
    # Returns empty bytes if
    # file cannot be found
    def read_file_bytes(self, path):
        try:
            with open(path, 'rb') as asset:
                return asset.read()
        except IOError:
            return b''
