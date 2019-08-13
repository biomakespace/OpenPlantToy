
# Handles requests made
# to the server

import json
from http.server import BaseHTTPRequestHandler

from control.check_circuit import get_instance


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pass

    def page_check_circuit(self):
        pass

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
