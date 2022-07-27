# this file is used for UTMB project to detect the gait phase using joints
# Author: Shengting Cao

# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
import json
import numpy as np
from sys import platform
import argparse
from shapely.geometry import Point


def azimuth(point1, point2):
    '''azimuth between 2 shapely points (interval 0 - 360)'''
    angle = np.arctan2(point2.x - point1.x, point2.y - point1.y)
    return np.degrees(angle) if angle >= 0 else np.degrees(angle) + 360
def ob2ac(angles):
    output = []
    for angle in angles: 
        if angle > 180:
            angle = 360 - angle
        output.append(angle)
    return output  

def ang2vert(path):
    f = open(path)
    data = json.load(f)
    # pose_keypoints = data['people'][0]["pose_keypoints_2d"]
    if (len(data['people']))> 1:
            pose_keypoints1 = data['people'][0]["pose_keypoints_2d"]
            pose_keypoints2 = data['people'][1]["pose_keypoints_2d"]

            pose_keypoints = []
            for j in range(2,75,3):
                if pose_keypoints1[j] > pose_keypoints2[j]:
                    pose_keypoints.append(pose_keypoints1[j-2])
                    pose_keypoints.append(pose_keypoints1[j-1])
                    pose_keypoints.append(pose_keypoints1[j])
                else:
                    pose_keypoints.append(pose_keypoints2[j-2])
                    pose_keypoints.append(pose_keypoints2[j-1])
                    pose_keypoints.append( pose_keypoints2[j])
    else:
        pose_keypoints = data['people'][0]["pose_keypoints_2d"]
    # right leg
    point1 = Point(pose_keypoints[9*3],pose_keypoints[9*3+1])
    point2 = Point(pose_keypoints[10*3],pose_keypoints[10*3+1])
    point3 = Point(pose_keypoints[11*3],pose_keypoints[11*3+1])
    point4 = Point(pose_keypoints[22*3],pose_keypoints[22*3+1])

    # left leg
    point5 = Point(pose_keypoints[12*3],pose_keypoints[12*3+1])
    point6 = Point(pose_keypoints[13*3],pose_keypoints[13*3+1])
    point7 = Point(pose_keypoints[14*3],pose_keypoints[14*3+1])
    point8 = Point(pose_keypoints[19*3],pose_keypoints[19*3+1])

    return ob2ac([azimuth(point1,point2),azimuth(point2,point3),\
        azimuth(point3,point4),azimuth(point5,point6),azimuth(point6,point7),azimuth(point7,point8),azimuth(point7,point3)])

def ang2vertPoint(pose_keypoints):
    # right leg
    point1 = Point(pose_keypoints[9][0],pose_keypoints[9][1])
    point2 = Point(pose_keypoints[10][0],pose_keypoints[10][1])
    point3 = Point(pose_keypoints[11][0],pose_keypoints[11][1])
    point4 = Point(pose_keypoints[22][0],pose_keypoints[22][1])

    # left leg
    point5 = Point(pose_keypoints[12][0],pose_keypoints[12][1])
    point6 = Point(pose_keypoints[13][0],pose_keypoints[13][1])
    point7 = Point(pose_keypoints[14][0],pose_keypoints[14][1])
    point8 = Point(pose_keypoints[19][0],pose_keypoints[19][1])

    return ob2ac([azimuth(point1,point2),azimuth(point2,point3),\
        azimuth(point3,point4),azimuth(point5,point6),azimuth(point6,point7),azimuth(point7,point8),azimuth(point7,point3)])

# # train a model based on previous label, use random forest
def trainRFModel():
    basePath = 'D:\Shengting\groundTruth'
    # datasetPath = '/data/Shengting/splitBeltProject/groundTruth'
    X = []
    y = []
    for subject in os.listdir(basePath):
        datasetPath = os.path.join(basePath,subject)
        print(datasetPath)
        for phase in sorted(os.listdir(datasetPath)):
            print(phase)
            for file in sorted(os.listdir(os.path.join(datasetPath,phase))):
                # print(file)
                if 'json' in file:
                    # print(ang2vert(os.path.join(datasetPath,phase,file)))
                    X.append(ang2vert(os.path.join(datasetPath,phase,file)))
                    y.append(int(phase[-1]))

    X = np.asarray(X)
    y = np.asarray(y)
    print(X.shape,y.shape)
    # print(y)

    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(max_depth=30, random_state=0)
    clf.fit(X,y)
    return clf
# clf = trainRFModel()

    

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../bin/python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../x64/Release;' +  dir_path + '/../bin;'
        import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="../examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../models/"

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

    # Process Image 
    datum = op.Datum()
    # imageToProcess = cv2.imread(args[0].image_path)
    # datum.cvInputData = imageToProcess
    # opWrapper.emplaceAndPop(op.VectorDatum([datum]))

    # matlab sesssion
    import matlab.engine
    from time import sleep
    from time import time

    # from oct2py import Oct2Py
    
    try:
        eng = matlab.engine.connect_matlab()
        print("Connecting to the matlab sesssion: ",matlab.engine.find_matlab())
        eng.addpath(r"C:\Program Files (x86)\Bertec\Treadmill\Remote")
        eng.workspace['remote'] = eng.eval("tcpip('localhost',4000);")
        # start session
        eng.eval('fopen(remote)',nargout=0)
    except:
        print("Please open matlab and type matlab.engine.shareEngine")
        exit()

    # folder = r"C:\Users\mako\Desktop\Splicer software\Subject 63\Speed0.5vs0.5\Phase 3"
    
    vid = cv2.VideoCapture(1)
    # X = np.load("training_data_angle.npy")
    # y = np.load("labels_angle.npy")
    # from sklearn.ensemble import RandomForestClassifier
    # clf = RandomForestClassifier(max_depth=30, random_state=0)
    # clf.fit(X,y)

    print("Loading model...")
    import joblib
    clf = joblib.load('random_forest.joblib')

    print('Start session, increase to 0.8 m/s ') 
    eng.eval('tm_set(remote,0.8,0.1)',nargout=0)
    sleep(10)
    for i in range(5,-1,-1):
        print("Split-belt mode: count down: ",i)
        sleep(1)

    timeout = time() + 20
    while True:
        # image = cv2.imread(os.path.join(folder,name))
        
        ret, image = vid.read()
        # print(ret)
        imageToProcess = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        
        print('No Person')

        # Display Image
        
        # print("Length of keypoints: " + str(len(datum.poseKeypoints[0])))
        # print("Body keypoints: \n" + str(datum.poseKeypoints))
        # if datum.poseKeypoints== None:
        if datum.poseKeypoints is not None:
            
            angle = ang2vertPoint(datum.poseKeypoints[0])
            
            pred = clf.predict([angle])
            y=pred[0]
            print("The phase prediciton is : " + str(y))
            if pred == None:
                pass
            if y ==0:
                eng.eval('tm_set(remote,0.8,0.8)',nargout=0)
            if y ==1:
                eng.eval('tm_set(remote,1.2,1.2)',nargout=0)
            if y ==2:
                eng.eval('tm_set(remote,1.1,1)',nargout=0)
            if y ==3:
                eng.eval('tm_set(remote,0.6,1)',nargout=0)
            if y == 4:
                eng.eval('tm_set(remote,0.5,1.2)',nargout=0)
            if y ==5:
                eng.eval('tm_set(remote,0.5,1.2)',nargout=0)
            if y == 6:
                eng.eval('tm_set(remote,0.7,0.8)',nargout=0)
            if y == 7:
                eng.eval('tm_set(remote,0.8,0.8)',nargout=0)

            cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
            # cv2.waitKey(0)
        sleep(0.01)
        if time()> timeout:
            print("Exit split belt mode.. ")
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    print('Set to constant speed 0.8 m/s')
    eng.eval('tm_set(remote,0.8,0.1)',nargout=0)
    sleep(10)
    print("Slow down")
    eng.eval('tm_set(remote,0,0.1)',nargout=0)
    sleep(2)
    # end session
    eng.eval('fclose(remote)',nargout =0)
except Exception as e:
    print(e)
    sys.exit(-1)
