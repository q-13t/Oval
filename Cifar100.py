import os.path
from random import randint
import PIL.Image
import numpy as np 
import keras as ks
import TrainCall as tc
import logging as log
import configparser as cp

config = cp.ConfigParser()
config.read("config.ini")
LOG_LEVEL = 10 if config.getint("TRAINING", "LOG_LEVEL") == -1 else config.getint("TRAINING", "LOG_LEVEL")

log.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")

EPOCHS = config.getint("TRAINING", "EPOCHS")
EXPECTED_ACC = config.getfloat("TRAINING", "EXPECTED_ACC")
DO_TRAIN = config.getboolean("TRAINING", "DO_TRAIN")
MODEL_DIR = config.get("MODELS", "MODEL_DIR")

class_names = ["apple","aquarium_fish","baby","bear","beaver","bed","bee","beetle","bicycle","bottle","bowl","boy","bridge","bus","butterfly","camel","can","castle","caterpillar","cattle","chair","chimpanzee","clock","cloud","cockroach","couch","cra","crocodile","cup","dinosaur","dolphin","elephant","flatfish","forest","fox","girl","hamster","house","kangaroo","keyboard","lamp","lawn_mower","leopard","lion","lizard","lobster","man","maple_tree","motorcycle","mountain","mouse","mushroom","oak_tree","orange","orchid","otter","palm_tree","pear","pickup_truck","pine_tree","plain","plate","poppy","porcupine","possum","rabbit","raccoon","ray","road","rocket","rose","sea","seal","shark","shrew","skunk","skyscraper","snail","snake","spider","squirrel","streetcar","sunflower","sweet_pepper","table","tank","telephone","television","tiger","tractor","train","trout","tulip","turtle","wardrobe","whale","willow_tree","wolf","woman","worm"]
(train_imgs, train_labels), (test_imgs, test_labels) = ks.datasets.cifar100.load_data()
log.info("Train:" + str(train_imgs.shape) + "\tTest:" + str(test_imgs.shape))
train_imgs, test_imgs = train_imgs / 255.0, test_imgs / 255.0

if os.path.exists(f'./{MODEL_DIR}/best_model.h5') and not DO_TRAIN:
    model = ks.models.load_model(f'./{MODEL_DIR}/best_model.h5')
else:
    model = ks.Sequential([
        ks.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        ks.layers.MaxPooling2D((2, 2)),
        ks.layers.Conv2D(128, (3, 3), activation='relu'),
        ks.layers.MaxPooling2D((2, 2)),
        ks.layers.Conv2D(256, (3, 3), activation='relu'),
        ks.layers.Flatten(),
        ks.layers.Dense(128, activation='relu'),
        ks.layers.Dense(100)
    ])
    model.compile(optimizer='adam', loss=ks.losses.SparseCategoricalCrossentropy(from_logits=True),  metrics=['accuracy'])

    callbacks = [
        # ks.callbacks.ModelCheckpoint(f'./{MODEL_DIR}/best_model.h5', save_best_only=True),
        tc.TrainingCall(EXPECTED_ACC, EPOCHS)
    ]
    model.fit(train_imgs, train_labels, epochs=EPOCHS, shuffle=True, callbacks=callbacks, validation_data=(test_imgs, test_labels))
    model.save(f'./{MODEL_DIR}/cifar100_5.h5')

model = ks.Sequential([model, ks.layers.Softmax()]) # flatten all values to sum up to 1, so that they may be interpreted as probabilities
model.compile(optimizer='adam', loss=ks.losses.SparseCategoricalCrossentropy(from_logits=False),  metrics=['accuracy'])
model.summary()
test = np.array(test_imgs[0]).reshape(1, 32, 32, 3)
for pred in model.predict(test)[0]:
    log.info("{:.12f}".format(pred))

test_loss, test_acc = model.evaluate(test_imgs, test_labels, verbose=2)
log.info(f'Test accuracy: {test_acc}')


