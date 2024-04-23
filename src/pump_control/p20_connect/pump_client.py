import socket
import struct

__all__ = [
    "PumpClient"
]

MSG_CONNECT = 0
MSG_STATE = 1
MSG_SPEED = 2

class PumpClient():
    def __init__(self, ip="localhost", port=8888):
        self.ip = ip
        self.port = port
        self.address = (ip, port)

        self.connected = False

    def __enter__(cls):
        cls.connect()
        return cls

    def __exit__(cls, typ, val, tb):
        cls.close()

    def connect(self):
        if not hasattr(self, "client"):
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.address)
            print("Connected to controller at {}".format(self.address))
            self.connected = True
    
    def close(self):
        if hasattr(self, "client"):
            self.client.close()
            self.connected = False
            del self.client
    
    def start_pump(self):
        self._send(MSG_STATE, 1)
    
    def stop_pump(self):
        self._send(MSG_STATE, 0)
    
    def set_pump_speed(self, speed):
        self._send(MSG_SPEED, speed)

    def connect_pump(self, com_port=6):
        self._send(MSG_CONNECT, com_port)

    def _get_msg(self, msg_type, value):
        return struct.pack("ii", msg_type, value)

    def _send(self, msg_type, value):
        if hasattr(self, "client"):
            self.client.send(self._get_msg(msg_type, value))
        else:
            print("Client not connected to Pump Controller")

