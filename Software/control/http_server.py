
# Handles requests made
# to the server

import json
from http.server import BaseHTTPRequestHandler
import threading

from check_circuit import get_instance
from check_circuit import open_serial
from check_circuit import validate_port
from list_serial_ports import ListSerialPorts


class RequestHandler(BaseHTTPRequestHandler):

    CHECK_CIRCUIT_PATH = '/check-circuit'
    SELECT_SERIAL_PATH = '/select-serial'

    def do_GET(self):
        if self.path == self.CHECK_CIRCUIT_PATH:
            self.page_check_circuit()
        elif self.path == "/application.js":
            self.script_application_js()
        elif self.path == "/check-circuit.css":
            self.style_check_circuit_css()
        elif self.path == "/api/circuit-information":
            self.api_circuit_information()
        elif self.path == "/api/list-serial-ports":
            self.api_list_serial_ports()
        elif self.path == "/api/confirm-serial-port":
            self.api_confirm_serial_port()
        elif self.path == self.SELECT_SERIAL_PATH:
            self.page_select_serial()
        elif self.path == "/select-serial.css":
            self.style_select_serial(),
        elif self.path == "/select-serial.js":
            self.script_select_serial_js(),
        elif self.path == "/":
            self.root()
        else:
            self.page_not_found()

    def do_POST(self):
        if self.path == "/api/confirm-serial-port":
            self.api_confirm_serial_port()
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
        asset_path = 'assets/select-serial.html'
        self.try_load_static_asset(asset_path)

    def style_select_serial(self):
        asset_path = 'assets/select-serial.css'
        self.try_load_static_asset(asset_path)

    def script_select_serial_js(self):
        asset_path = 'assets/select-serial.js'
        self.try_load_static_asset(asset_path)

    def api_circuit_information(self):
        # Get an instance of the checker
        circuit_checker = get_instance()
        circuit_information = self.format_json(
            circuit_checker.get_circuit_information()
        )
        if circuit_information is not None:
            # 200 status code
            self.send_response(200)
            self.end_headers()
            # Write out the circuit information in the body
            # Information is json, so serialise & encode
            self.wfile.write(circuit_information)
        else:
            self.internal_server_error()

    def api_list_serial_ports(self):
        port_list = ListSerialPorts().as_json()
        formatted = self.format_json(port_list)
        if formatted is not None:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                formatted
            )
        else:
            self.internal_server_error()

    def api_confirm_serial_port(self):
        body_length = 0
        post_data = {}
        serial_path = ""
        try:
            body_length = int(self.headers.get("content-length"))
        except (TypeError, ValueError):
            self.invalid_request_error("Content length header required")
            return
        try:
            post_data = json.loads(
                self.rfile.read(body_length).decode('ascii')
            )
        except (json.decoder.JSONDecodeError, UnicodeDecodeError):
            self.invalid_request_error("Could not decode received JSON")
            return
        try:
            serial_path = post_data["path"]
        except KeyError:
            self.invalid_request_error("The 'path' key is required but not provided")
            return
        # Open and validate serial
        could_open = open_serial(serial_path)
        if not could_open:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                self.format_json(
                    {
                        "success": False,
                        "reason": "Could not open serial port"
                    }
                )
            )
            return
        port_valid = validate_port()
        # Try to get the circuit checker, read to spin up thread
        circuit_checker = get_instance()
        if not port_valid or not circuit_checker:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                self.format_json(
                    {
                        "success": False,
                        "reason": "Response from serial port inconsistent with circuit components"
                    }
                )
            )
            return
        # All (as) good (as we can really guarantee)
        # Spin up the checking thread
        circuit_checking_thread = threading.Thread(target=circuit_checker.run, daemon=True)
        circuit_checking_thread.start()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(
            self.format_json(
                {
                    "success": True
                }
            )
        )

    # If page not found
    # Redirect to root
    def page_not_found(self):
        self.send_response(404)
        self.end_headers()

    # Helper methods for common errors
    def internal_server_error(self):
        self.send_response(500, "Internal Server Error")
        self.end_headers()

    def invalid_request_error(self, message):
        self.send_response(400, message)
        self.end_headers()

    # From root redirect
    # to check circuit path
    def root(self):
        self.send_response(302)
        self.send_header("Location", RequestHandler.SELECT_SERIAL_PATH)
        self.end_headers()

    def format_json(self, dictionary):
        try:
            return json.dumps(
                dictionary
            ).encode('utf-8')
        except UnicodeEncodeError:
            return None

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
