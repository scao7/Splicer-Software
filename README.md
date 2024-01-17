
# Splicer software
### Simulating the split-belt treadmill using single-belt treadmill (4front treadmill of woodway)
### This is the treadmill control system based on gait phases detected with webcams.

Author: Shengting Cao 
School: University of Alabama
Email: scao7@crimson.ua.edu

This code is tested in windows with CUDA 11.6 and python 3.9.

1. install the openpose python (build from source using cmake-gui )

```python
project layout:
-- connectKineAssistTutorial
    -- ethernetStatus.png
    -- ipv4.png
    -- openNetworkandShareCenter.png
    -- setip.png 
-- openpose
-- rs232
    -- connectExample.py # rs232 connection example
--src
    -- keypoints_example.py # example to use the pyopenpose to extract the joints
    -- GaitControl.py # The scripts for training model and testing
```


# Connect to the KineAssist using the computer 
### demo images are int he connectKineAssistTutorial
-set the local machine ip to 10.0.203.55
-set the sub net mask to 255.0.0.0
-set the default gateway to 10.0.203.1 
-use "telnet 10.0.203.234" to build the communication channel (root and root)

# Woodway Protocols
The baud is 4800.
Use the A1 or A0 command to start the treadmill. With the A1 command you do not need to communicate every second with the treadmill (great for testing). Or use the A0 command, but make sure you send a command every second or the treadmill will time out and come to a stop. A0 is recommended for safety once you have a program written.
You can then send A3 and A4 commands to set the speed and incline of the treadmill.
You can send an AA command to stop the treadmill. You would have to send an A1 or A0 to start the treadmill again.
 
Example of an elevation command: A4 30 3**1** 3**4** 3**5**  this will set the incline to 14.5%
Example of a speed command: A3 30 3 3**5** 3**8** this will set the speed to 5.8 mph.
Keep your packet size to 5 bytes and only one command every 100ms. 


