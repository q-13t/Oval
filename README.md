    Oval is an AI image classification tool that runs on Python server and Android App.

<img src="./Oval.svg" style="width:100vw; height:15vh">

# About

This is the android side of the project. This part is responsible for capturing images from the real world and displaying the predictions from server.

# Flow

At first client will try to connect to the server. If successful client will be redirected to the main page where they will be able to take a picture, said picture will be displayed and predictions will be displayed underneath. At first only 5 (most certain) predictions are shown, but client can at any time click the `Expand` button to see all 100 predictions.

# Examples

| ![](./readme_images/Connecting.jpg) | ![](./readme_images/Fox.jpg)             | ![](./readme_images/Telephone.jpg)               | ![](./readme_images/Oranges.jpg) |
| ----------------------------------- | ---------------------------------------- | ------------------------------------------------ | -------------------------------- |
| Connecting to the server            | Certain fox predictions with day mode UI | Certain telephone predictions with night mode UI | Uncertain oranges predictions    |

# Licensing

This project is licensed under the MIT License. See the LICENSE file for details.

Any contributions and/or suggestions are welcomed
