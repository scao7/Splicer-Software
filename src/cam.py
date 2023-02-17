
'''
Author: Shengting Cao 
School: The University of Alabama 
Email: scao7@crimson.ua.edu
This script is used to run the real time control system
'''
# import the opencv library
import cv2

# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import time

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../openpose/build/python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../openpose/build/x64/Release;' +  dir_path + '/../openpose/build/bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", default="../openpose/examples/media/", help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
    parser.add_argument("--no_display", default=False, help="Enable to disable the visual display.")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../openpose/models"

    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Read frames on directory
    imagePaths = op.get_images_on_directory(args[0].image_dir);
    start = time.time()
    print('''
        Copyright: 
        Author: Shengting Cao (Computer Science and Electrical Compuer Engineering)
        Email: scao7@crimson.ua.edu
        Open to software development and AI development jobs.
    ''')
    
    print("Loading model...")
    import joblib
    clf = joblib.load('random_forest.joblib')
    from GaitControl import GaitController
    
    gaitcontroller = GaitController()
    # define a video capture object
    vid = cv2.VideoCapture(1)
    import serial
    ser = serial.Serial(
        port="COM3",  
        baudrate=4800,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=None,
        xonxoff=0,
        rtscts=0,
    )
    ser.isOpen()
    # from 0.0 to 2.0
    ser.write(b'\xa0')
    speed_list = [b"\xa3\x30\x30\x31\x37",
              b"\xa3\x30\x30\x32\x31",
              b"\xa3\x30\x30\x32\x38",
              b"\xa3\x30\x30\x32\x34",
              b"\xa3\x30\x30\x31\x37",
              b"\xa3\x30\x30\x31\x30",
              b"\xa3\x30\x30\x30\x39",
              b"\xa3\x30\x30\x31\x32"]
    while(True):
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        datum = op.Datum()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        datum.cvInputData = frame
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        if datum.poseKeypoints is not None:
            # print("Body keypoints: \n" + str(datum.poseKeypoints))
            angle = gaitcontroller.ang2vertPoint(datum.poseKeypoints[0])
            # print(angle)
            pred = clf.predict([angle])
            y=pred[0]
            print("The phase prediction is " + str(y))

            # if pred == None:
            #     pass
            # if pred ==0:
            #     SPEED = b"\xa3\x30\x30\x30\x38"
            # if pred == 1:
            #     SPEED = b"\xa3\x30\x30\x31\x31"
            # if pred == 2:
            #     SPEED = b"\xa3\x30\x30\x32\x33"
            # if pred == 3:
            #     SPEED = b"\xa3\x30\x30\x32\x33"
            # if pred ==4:
            #     SPEED = b"\xa3\x30\x30\x31\x38"
            # if pred ==5:
            #     SPEED = b"\xa3\x30\x30\x30\x36"
            # if pred ==6:
            #     SPEED = b"\xa3\x30\x30\x30\x36"
            # if pred ==7:
            #     SPEED = b"\xa3\x30\x30\x30\x38"
            if pred == None:
                pass
            if pred ==0:
                SPEED = b"\xa3\x30\x30\x30\x36"
            if pred == 1:
                SPEED = b"\xa3\x30\x30\x31\x31"
            if pred == 2:
                SPEED = b"\xa3\x30\x30\x31\x31"
            if pred == 3:
                SPEED = b"\xa3\x30\x30\x31\x31"
            if pred ==4:
                SPEED = b"\xa3\x30\x30\x31\x31"
            if pred ==5:
                SPEED = b"\xa3\x30\x30\x30\x35"
            if pred ==6:
                SPEED = b"\xa3\x30\x30\x30\x35"
            if pred ==7:
                SPEED = b"\xa3\x30\x30\x30\x36"

            # if pred == None:
            #     pass 
            # if pred == 0:
            #     SPEED = speed_list[0]
            # if pred == 1:
            #     SPEED = speed_list[1]
            # if pred ==2:
            #     SPEED = speed_list[2]
            # if pred ==3:
            #     SPEED = speed_list[3]
            # if pred ==4: 
            #     SPEED = speed_list[4]
            # if pred == 5:
            #     SPEED= speed_list[5]
            # if pred == 6:
            #     SPEED = speed_list[6]
            # if pred == 7:
            #     SPEED = speed_list[7]
            
            ser.write(SPEED)

        time.sleep(0.1)

            

        if not args[0].no_display:
            cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
            key = cv2.waitKey(15)
            if key == 27: 
                ser.write(b'\xaa')
                ser.close()
                break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    end = time.time()
    print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")
except Exception as e:
    print(e)
    sys.exit(-1)



  

  
