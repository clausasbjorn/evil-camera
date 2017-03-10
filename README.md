# Evil Camera - we see you

Using haag cascades with OpenCV to detect faces and report them in.


Detect faces and badges.

Evil sensor listens for wlan wireless beacons formats them and sends them to
the evil api.

## Requirements
* Linux OS / Raspberry pi 
* A v4l2 camera, or more

## Dependencies
* [opencv(www.opencv.org)]
* numpy
* scipy

On Raspberry Pi with raspbian:
```sh
$ sudo apt-get install python-opencv python-numpy python-scipy
```

## Do a test run

Start capture.py, it will start to detect faces and send them into the
[evil-image(https://github.com/clausasbjorn/evil-images)] cloud service.

## See what is going on

Uncomment the debug code in the capture.py to get images on your screen and
comment out the call to report_face():


```
python evil-camera.py 1
```

If you have multiple cameras you can use more of them:

```
python evil-camera.py 2
```
