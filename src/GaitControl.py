# This file is used for UTMB project to detect the gait phase using joints
# Author: Shengting Cao
# The University of Alabama
'''
Author: Shengting Cao 
School: The University of Alabama 
Email: scao7@crimson.ua.edu
This file is used for UTMB project to detect the gait phase using joints
'''

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

class GaitController():
    def __init__(self):
        self.data_folder = '../data/'
        self.data_type = 'json' # json + images or npy + tiffile

    def azimuth(self,point1, point2):
        '''azimuth between 2 shapely points (interval 0 - 360)'''
        angle = np.arctan2(point2.x - point1.x, point2.y - point1.y)
        return np.degrees(angle) if angle >= 0 else np.degrees(angle) + 360

    def ob2ac(self,angles):
        ''' Obtuse to acute angle '''
        output = []
        for angle in angles: 
            if angle > 180:
                angle = 360 - angle
            output.append(angle)
        return output  

    def ang2vertPoint(self,pose_keypoints):
        ''' alculate 8 angles'''
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

        return self.ob2ac([self.azimuth(point1,point2),self.azimuth(point2,point3),\
            self.azimuth(point3,point4),self.azimuth(point5,point6),self.azimuth(point6,point7),self.azimuth(point7,point8),self.azimuth(point7,point3)])
    

    def dataPreprocessing(self):
        '''conver each image to angles and save in npy'''


    # # train a model based on previous label, use random forest
    def trainRFModel(self):
        '''Tran a random forest model based on the datasets '''
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
                        X.append(self.ang2vert(os.path.join(datasetPath,phase,file)))
                        y.append(int(phase[-1]))

        X = np.asarray(X)
        y = np.asarray(y)
        print(X.shape,y.shape)