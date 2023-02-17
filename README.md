
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


