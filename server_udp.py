import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5000))

print("Servidor UDP escuchando en puerto 5000")

while True:
    data, addr = sock.recvfrom(2048)
    try:
        state = json.loads(data.decode())
        print(state)
    except Exception as e:
        print("Error:", e)