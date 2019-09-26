
import serial.tools.list_ports


class ListSerialPorts:

    def __init__(self):
        self.port_list = []
        self.port_dictionaries = []

    def as_json(self):
        self.port_list = serial.tools.list_ports.comports()
        for port in self.port_list:
            self.port_dictionaries.append(
                {
                    "path": port.device,
                    "description": port.description
                }
            )
        return self.port_dictionaries
