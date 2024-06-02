
import asyncio
import base64
import json
import socket
from websockets.sync.client import connect

def send(data):
    ip = socket.gethostbyname(socket.getfqdn())
    port = 8765
    with connect(f"ws://{ip}:{port}") as websocket:
        websocket.send(base64.b64encode(data))
        message = websocket.recv()
        print(f"Received: {json.loads(message)}")

with open("test_imgs/Bus.jpg", "rb" ) as f:
    print("START::")
    data = f.read()
    f.close()
    send(data)
