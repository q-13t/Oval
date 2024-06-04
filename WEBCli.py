import base64
import json
import socket
from websockets.sync.client import connect
import configparser as cp
import logging as log
config = cp.ConfigParser()
config.read("config.ini")

IP = socket.gethostbyname(socket.getfqdn()) if config.get("SERVER", "IP") == "-1" else config.get("SERVER", "IP")
PORT = 8765 if config.getint("SERVER", "PORT") == -1 else config.getint("SERVER", "PORT")
LOG_LEVEL = 10 if config.getint("SERVER", "LOG_LEVEL") == -1 else config.getint("SERVER", "LOG_LEVEL")

log.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")

def send(data):
    with connect(f"ws://{IP}:{PORT}") as websocket:
        websocket.send(base64.b64encode(data))
        message = websocket.recv()
        js  =  json.loads(message)
        for i in js:
            log.info(f"Received: {i}")
        # log.info(f"Received: {js[0].get('Class')} with probability {js[0].get('Probability')}")

with open("./test_imgs/Bus.jpg", "rb" ) as f:
    log.info("START::")
    data = f.read()
    f.close()
    send(data)
