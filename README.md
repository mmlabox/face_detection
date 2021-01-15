# Face Detection & Distances
AlwaysAI app for computing distances between detected faces from real-time video on Raspberry PI.

## Setup
Setup your development computer by installing the [AlwaysAI CLI](https://alwaysai.co/docs/get_started/development_computer_setup.html).
Setup your Raspberry PI to run AlwaysAI by following [these](https://alwaysai.co/docs/reference/raspberry_pi_setup.html) instructions.
Note that you might need to enable camera support on your Raspberry PI, which is easily done via [SSH](https://www.raspberrypi.org/documentation/configuration/camera.md).

## Deploy & run
With the AlwaysAI CLI installed, open a terminal on your development computer and navigate to the project folder.

### To configure the application for your Raspberry PI, run the following command:
```
aai app configure
```
This will allow you to initialize a project connected to your AlwaysAI account and choose a target device (your Raspberry PI).

### To deploy the application to your device, run:

```
aai app deploy
```
This will push your application to your device, create docker files & take care of any dependencies specified in the requirements.txt file. 
Repeat this step every time you've made changes to the code.

### To start the app, run:
```
aai app start
```
Output will be printed to the terminal and written to influxDB (make sure to provide a .env file with the necessary information). A live video-stream is also available by navigating to localhost:5000 in your browser.

