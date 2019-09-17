
# Handles requests made
# to the server

import json
from http.server import BaseHTTPRequestHandler

from check_circuit import get_instance


class RequestHandler(BaseHTTPRequestHandler):

    CHECK_CIRCUIT_PATH = '/check-circuit'
    SELECT_SERIAL_PATH = '/select-serial'

    PATH_HANDLER_MAP = {}

    def initialise_path_mapping(self):
        RequestHandler.PATH_HANDLER_MAP = {
            self.CHECK_CIRCUIT_PATH: self.page_check_circuit,
            "/application.js": self.script_application_js,
            "/check-circuit.css": self.style_check_circuit_css,
            "/api/circuit-information": self.api_circuit_information(),
            self.SELECT_SERIAL_PATH: self.page_select_serial(),
            "select-serial.css": self.style_select_serial(),
            "/": self.root
        }

    def do_GET(self):
        # A bit inefficient
        # Check each time if the map has
        # been initialised, initialise if not
        if RequestHandler.PATH_HANDLER_MAP == {}:
            self.initialise_path_mapping()
        # Find the handler method
        # and call it
        if self.path in RequestHandler.PATH_HANDLER_MAP.keys():
            RequestHandler.PATH_HANDLER_MAP[self.path]()
        else:
            self.page_not_found()

    # Helper method to try
    # to read in a static asset
    # Return 200 if good
    # Return 500 if no good
    # Takes path as argument
    def try_load_static_asset(self, asset_path):
        body = self.read_file_bytes(asset_path)
        if len(body) > 0:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(500, 'Internal Server Error')
            self.end_headers()

    def page_check_circuit(self):
        asset_path = 'assets/check-circuit.html'
        self.try_load_static_asset(asset_path)

    def script_application_js(self):
        asset_path = 'assets/application.js'
        self.try_load_static_asset(asset_path)

    def style_check_circuit_css(self):
        asset_path = 'assets/check-circuit.css'
        self.try_load_static_asset(asset_path)

    def page_select_serial(self):
        pass   # TODO implement

    def style_select_serial(self):
        asset_path = 'assets/select-serial.css'
        self.try_load_static_asset(asset_path)

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
