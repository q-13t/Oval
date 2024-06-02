# Server
import base64
import socket
import websockets
from websockets.server import serve
import asyncio
from PIL import Image
import io
import numpy as np
import logging as log
import keras as ks
import json
import configparser as cp

config = cp.ConfigParser()
config.read("config.ini")

LOG_LEVEL = 10 if config.getint("SERVER", "LOG_LEVEL") == -1 else config.getint("SERVER", "LOG_LEVEL")
IP = socket.gethostbyname(socket.getfqdn()) if config.getint("SERVER", "IP") == -1 else config.get("SERVER", "IP")
PORT = 8765 if config.getint("SERVER", "PORT") == -1 else config.getint("SERVER", "PORT")
MODEL_DIR = config.get("MODELS", "MODEL_DIR")
MODEL = config.get("SERVER", "MODEL")
log.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")

class_names = ["apple","aquarium_fish","baby","bear","beaver","bed","bee","beetle","bicycle","bottle","bowl","boy","bridge","bus","butterfly","camel","can","castle","caterpillar","cattle","chair","chimpanzee","clock","cloud","cockroach","couch","cra","crocodile","cup","dinosaur","dolphin","elephant","flatfish","forest","fox","girl","hamster","house","kangaroo","keyboard","lamp","lawn_mower","leopard","lion","lizard","lobster","man","maple_tree","motorcycle","mountain","mouse","mushroom","oak_tree","orange","orchid","otter","palm_tree","pear","pickup_truck","pine_tree","plain","plate","poppy","porcupine","possum","rabbit","raccoon","ray","road","rocket","rose","sea","seal","shark","shrew","skunk","skyscraper","snail","snake","spider","squirrel","streetcar","sunflower","sweet_pepper","table","tank","telephone","television","tiger","tractor","train","trout","tulip","turtle","wardrobe","whale","willow_tree","wolf","woman","worm"]

model = ks.models.load_model(f'./{MODEL_DIR}/{MODEL}') # The best model
model = ks.Sequential([model, ks.layers.Softmax()])

log.info("Loaded Model: ")
model.summary()

def compact_predictions(predictions)->list:
    return [{"Class":class_names[i],"Probability": str("{:.10f}".format(p))} for i, p in enumerate(predictions)]

async def mainHandler(websocket):
    try:
        log.info(f"Client connected: {websocket.remote_address}")
        async for message in websocket:
            try:
                img = Image.open(io.BytesIO(base64.b64decode(message))).resize(size=(32, 32), resample=Image.Resampling.LANCZOS)
                pixels = np.asarray(img).reshape(1, 32, 32, 3)
                pixels = pixels  / 255.0
                predictions = model.predict(pixels)[0]
                if(LOG_LEVEL == log.DEBUG):
                    img.show()
                    for pred in predictions:
                        print("{:.10f}".format(pred))
                await websocket.send(json.dumps(compact_predictions(predictions)))
            except Exception as e :
                log.error("Error: " + str(e))
                await websocket.send(str(e))
    except websockets.exceptions.ConnectionClosedError as e:
        log.info(f"Client disconnected With Error: {websocket.remote_address} : {e}")
    except websockets.exceptions.ConnectionClosedOK as e:
        log.info(f"Client disconnected Gracefully: {websocket.remote_address}")



async def main():
    async with serve(ws_handler=mainHandler,   host=IP, port=PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())