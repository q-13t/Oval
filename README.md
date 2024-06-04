    Oval is an AI image classification tool that runs on Python server and Android App.

<img src="./Oval.svg" style="width:100vw; height:15vh">

# About

This is the android side of the project. This part is responsible for capturing images from the real world and displaying the predictions from server.

# Flow

At first client will try to connect to the server. If successful client will be redirected to the main page where they will be able to take a picture, said picture will be displayed and predictions will be displayed underneath. At first only 5 (most certain) predictions are shown, but client can at any time click the `Expand` button to see all 100 predictions.

# Examples

<div class="container" style="  display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; grid-template-rows: 1fr; gap: 0px 0px; grid-template-areas: '. . . .'; margin: 5% 1%">
        <div style="padding: 2% 5%">
            <img src="./readme_images/Connecting.jpg" style="width: 100%; height:100%"></img>
            <p>Connecting to the server</p>
        </div>
        <div style="padding: 2% 5%">
            <img src="./readme_images/Fox.jpg" style="width: 100%; height:100%"></img>
            <p>Certain fox predictions with day mode UI</p>
        </div>
        <div style="padding: 2% 5%">
            <img src="./readme_images/Telephone.jpg" style="width: 100%; height:100%"></img>
            <p>Certain telephone predictions with night mode UI</p>
        </div>
        <div style="padding: 2% 5%">
            <img src="./readme_images/Oranges.jpg" style="width: 100%; height:100%"></img>
            <p>Uncertain oranges predictions</p>
        </div>
    </div>

# Licensing

This project is licensed under the MIT License. See the LICENSE file for details.

Any contributions and/or suggestions are welcomed
