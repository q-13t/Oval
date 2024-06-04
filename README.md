    Oval is an AI image classification tool that runs on Python server and Android App.

<img src="./Oval.svg" style="width:100vw; height:15vh">

# About

This is the server side of the project. It's a python app that contains:

# Training

This part was only used for training the model. You can see in `models` folder 3 models to choose from:

1. best_model.h5

   This model is expected to be the best model according to the tensorflow training calls. It was created during longes training session.

2. Cifar100.h5

   This is the model that simply run for the longest time util it achieved ~90% accuracy. By no mean this is the best model, due to overfilling concerns.

3. Cifar100_5.h5

   This model was created during training of another model. It's main goal is not to be the best, but to see the results of predictions excluding any possibility for overfilling.

# Server

This is the main part of the project as this part communicates directly with the client side.

The server will use the model and data specified in `config.ini`.

You can set up `your own IP address and your own port`, if no port or ip are specified the server will use default port and choose the first fitting ip address. See [WEBSock.py](./WEBSock.py) and [config.ini](./config.ini)

The server expects a `Base64` encoded image. That will be scaled down to the 32 x 32 resolution for classification.

The server will respond with `JSON Array` that contains 100 classes with predictions (in range of 0 - 1) in descending order. As an example:

```JSON
[
    {"Class": "pickup_truck", "Probability": "0.4843437970"},
    {"Class": "telephone", "Probability": "0.1512999386"},
    ...
]
```

# Client

This is an example websocket client that may be used for testing the models and predictions without running android client. The client will automatically use the same ip and port as the server. The example images are located in `test_imgs` folder.

# Licensing

This project is licensed under the MIT License. See the LICENSE file for details.

Any contributions and/or suggestions are welcomed
