# net/client.py
import socket
import json


class SocketClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = None  # 👈 no hay destino hasta conectar

    def set_address(self, ip, port=5000):
        self.addr = (ip, port)

    def send(self, data):
        if not self.addr:
            return
        try:
            self.sock.sendto(json.dumps(data).encode(), self.addr)
        except:
            pass
