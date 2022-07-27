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
import os.path as osp

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
    # dataFolder = r"D:\Shengting\UTMBLabel"
   
    # dataFolder = r"D:\Shengting\UTMBLabel"
    # print(os.listdir(dataFolder))
    # imageSize = 224
    # labels = []
    # training_data = []
    # for subject in os.listdir(dataFolder):
    #     print(subject)
    #     for speed in os.listdir(osp.join(dataFolder,subject)):
    #         print(speed)
    #         for phase in os.listdir(osp.join(dataFolder,subject,speed)):
    #             print(phase)
    #             for imName in os.listdir(osp.join(dataFolder,subject,speed,phase))[:5]:
    #                 labels.append(int(phase[-1]))
    #                 # Process Image
    #                 datum = op.Datum()
    #                 image = cv2.imread(osp.join(dataFolder,subject,speed,phase,imName))
    #                 imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    #                 # imageRGB = cv2.resize(imageRGB,(imageSize,imageSize),interpolation=cv2.INTER_CUBIC)
    #                 datum.cvInputData = imageRGB
    #                 opWrapper.emplaceAndPop(op.VectorDatum([datum]))
    #                 angle = ang2vertPoint(datum.poseKeypoints[0])
    #                 training_data.append(angle)
    #                 # cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
    #                 # cv2.waitKey(1)
    # labels = np.asarray(labels)
    # training_data = np.asarray(training_data)
    # print(training_data.shape,labels.shape)
    # print(labels)
    # np.save("training_data_angle.npy",training_data)
    # np.save("labels_angle.npy",labels)

    X = np.load("training_data_angle.npy")
    y = np.load("labels_angle.npy")
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(max_depth=30, random_state=0)
    clf.fit(X,y)
    import joblib
    joblib.dump(clf, "random_forest.joblib")
    
except Exception as e:
    print(e)
    sys.exit(-1)
