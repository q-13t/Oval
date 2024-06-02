import base64
import json
import socket
from websockets.sync.client import connect
import configparser as cp
import logging as log
config = cp.ConfigParser()
config.read("config.ini")

IP = socket.gethostbyname(socket.getfqdn()) if config.getint("SERVER", "IP") == -1 else config.get("SERVER", "IP")
PORT = 8765 if config.getint("SERVER", "PORT") == -1 else config.getint("SERVER", "PORT")
LOG_LEVEL = 10 if config.getint("SERVER", "LOG_LEVEL") == -1 else config.getint("SERVER", "LOG_LEVEL")

log.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")

def send(data):
    with connect(f"ws://{IP}:{PORT}") as websocket:
        websocket.send(base64.b64encode(data))
        message = websocket.recv()
        log.info(f"Received: {json.loads(message)}")

with open("./test_imgs/Bus.jpg", "rb" ) as f:
    log.info("START::")
    data = f.read()
    f.close()
    send(data)
