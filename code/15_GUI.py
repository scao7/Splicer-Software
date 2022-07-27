import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

import sys
import cv2
import os
import json
import numpy as np
from sys import platform
import argparse
from shapely.geometry import Point


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 780

    def __init__(self):
        super().__init__()

        self.title("The Splicer Split Belt Software")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ variable for splicer ============
        # self.textOneScreen = "Gait Splicer:\nThe software is to variate \nspeed based on current gait phase \nchoose a preset to begin"


        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=100,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=1)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(6, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(9, minsize=1)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=1)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Splicer Presets",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Preset 1",
                                                command=self.Preset1)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Preset 2",
                                                command=self.Preset2)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Preset 3",
                                                command=self.Preset3)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Preset 4",
                                                command=self.Preset4)
        self.button_4.grid(row=5, column=0, pady=10, padx=20)


        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3,4,5,6,7,8,9), weight=1)
        self.frame_right.rowconfigure(9, weight=10)
        self.frame_right.columnconfigure((0, 1,3), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        # self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        # self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=10, padx=10, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        # self.frame_info.rowconfigure(0, weight=1)
        # self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_right,
                                                   text="Speed",
                                                   height=20,
                                                   width = 10,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.CENTER)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)
        self.label_info_2 = customtkinter.CTkLabel(master=self.frame_right,
                                                   text="acceleration",
                                                   height=20,
                                                   width = 10,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.CENTER)
        self.label_info_2.grid(column=1, row=0, sticky="nwe", padx=15, pady=15)

        # self.progressbar = customtkinter.CTkProgressBar(master=self.frame_right)
        # self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)


        self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
                                                from_=0,
                                                to=2,
                                                command=self.slider_event)
        self.slider_1.grid(row=1, column=0, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_2.grid(row=2, column=0, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_3 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_3.grid(row=3, column=0, columnspan=1, pady=10, padx=20, sticky="we")

    
        self.slider_4 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_4.grid(row=4, column=0, columnspan=1, pady=10, padx=20, sticky="we")


        self.slider_5 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_5.grid(row=5, column=0, columnspan=1, pady=10, padx=20, sticky="we")


        self.slider_6 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_6.grid(row=6, column=0, columnspan=1, pady=10, padx=20, sticky="we")


        self.slider_7 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_7.grid(row=7, column=0, columnspan=1, pady=10, padx=20, sticky="we")


        self.slider_8 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_8.grid(row=8, column=0, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_9 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_9.grid(row=1, column=1, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_10 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_10.grid(row=2, column=1, columnspan=1, pady=10, padx=20, sticky="we")


        self.slider_11 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_11.grid(row=3, column=1, columnspan=1, pady=10, padx=20, sticky="we")


        self.slider_12 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_12.grid(row=4, column=1, columnspan=1, pady=10, padx=20, sticky="we")
        self.slider_13 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_13.grid(row=5, column=1, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_14 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_14.grid(row=6, column=1, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_15 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_15.grid(row=7, column=1, columnspan=1, pady=10, padx=20, sticky="we")
        self.slider_16 = customtkinter.CTkSlider(master=self.frame_right,from_=0,to=2,
                                                command=self.slider_event)
        self.slider_16.grid(row=8, column=1, columnspan=1, pady=10, padx=20, sticky="we")



        
        self.slider_17 = customtkinter.CTkSlider(master=self.frame_left,from_=0,to=60,
                                                command=self.slider_event)
        self.slider_17.grid(row=6, column=0, columnspan=1, pady=10, padx=20, sticky="we")
        self.slider_18 = customtkinter.CTkSlider(master=self.frame_left,from_=0,to=60,
                                                command=self.slider_event)
        self.slider_18.grid(row=7, column=0, columnspan=1, pady=10, padx=20, sticky="we")

        self.slider_19 = customtkinter.CTkSlider(master=self.frame_left,from_=0,to=60,
                                                command=self.slider_event)
        self.slider_19.grid(row=8, column=0, columnspan=1, pady=10, padx=20, sticky="we")


        self.label_info_3 = customtkinter.CTkLabel(master=self.frame_right,
                                                   text="Current setting:",
                                                   height=600,
                                                   width = 10,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.CENTER)
        self.label_info_3.grid(column=2, row=0, columnspan=1,rowspan=8,sticky="new", padx=15, pady=15)


        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Run setting",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.runAI)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.optionmenu_1.set("Dark")


    def Preset1(self):
        #speed
        self.slider_1.set(0.8)
        self.slider_2.set(1.2)
        self.slider_3.set(1.1)
        self.slider_4.set(0.6)
        self.slider_5.set(0.5)
        self.slider_6.set(0.5)
        self.slider_7.set(0.7)
        self.slider_8.set(0.8)
        # acceleration 
        self.slider_9.set(0.8)
        self.slider_10.set(1.2)
        self.slider_11.set(1)
        self.slider_12.set(1)
        self.slider_13.set(1.2)
        self.slider_14.set(1.2)
        self.slider_15.set(0.8)
        self.slider_16.set(0.8)

        # time for the start and end 
        self.slider_17.set(20)
        self.slider_18.set(30)
        self.slider_19.set(20)


        text = f"""
        Curent Config is: 
        Phase 0: {self.slider_1.get():.02f} {self.slider_9.get():.02f}
        Phase 1: {self.slider_2.get():.02f} {self.slider_10.get():.02f}
        Phase 2: {self.slider_3.get():.02f} {self.slider_11.get():.02f}
        Phase 3: {self.slider_4.get():.02f} {self.slider_12.get():.02f}
        Phase 4: {self.slider_5.get():.02f} {self.slider_13.get():.02f}
        Phase 5: {self.slider_6.get():.02f} {self.slider_14.get():.02f}
        Phase 6: {self.slider_7.get():.02f} {self.slider_15.get():.02f}
        Phase 7: {self.slider_8.get():.02f} {self.slider_16.get():.02f}
        start constant time: {self.slider_17.get():.02f}s
        split time: {self.slider_18.get():.02f}s
        end constant time: {self.slider_19.get():.02f}s"""
        self.label_info_3.configure(text= text)

    def Preset2(self):
        #speed
        self.slider_1.set(0.5)
        self.slider_2.set(0.5)
        self.slider_3.set(0.5)
        self.slider_4.set(0.8)
        self.slider_5.set(1.2)
        self.slider_6.set(1.1)
        self.slider_7.set(0.6)
        self.slider_8.set(0.4)
        # acceleration 
        self.slider_9.set(0.8)
        self.slider_10.set(1.2)
        self.slider_11.set(1)
        self.slider_12.set(1)
        self.slider_13.set(1.2)
        self.slider_14.set(1.2)
        self.slider_15.set(0.8)
        self.slider_16.set(0.8)   

        # time for the start and end 
        self.slider_17.set(20)
        self.slider_18.set(30)
        self.slider_19.set(20)


        text = f"""
        Curent Config is: 
        Phase 0: {self.slider_1.get():.02f} {self.slider_9.get():.02f}
        Phase 1: {self.slider_2.get():.02f} {self.slider_10.get():.02f}
        Phase 2: {self.slider_3.get():.02f} {self.slider_11.get():.02f}
        Phase 3: {self.slider_4.get():.02f} {self.slider_12.get():.02f}
        Phase 4: {self.slider_5.get():.02f} {self.slider_13.get():.02f}
        Phase 5: {self.slider_6.get():.02f} {self.slider_14.get():.02f}
        Phase 6: {self.slider_7.get():.02f} {self.slider_15.get():.02f}
        Phase 7: {self.slider_8.get():.02f} {self.slider_16.get():.02f}
        start constant time: {self.slider_17.get():.02f}s
        split time: {self.slider_18.get():.02f}s
        end constant time: {self.slider_19.get():.02f}s"""
        self.label_info_3.configure(text= text)


    def Preset3(self):
        #speed
        self.slider_1.set(0.8)
        self.slider_2.set(1.2)
        self.slider_3.set(1.1)
        self.slider_4.set(0.6)
        self.slider_5.set(0.0)
        self.slider_6.set(0.0)
        self.slider_7.set(0.0)
        self.slider_8.set(0.5)
        # acceleration 
        self.slider_9.set(0.8)
        self.slider_10.set(1.2)
        self.slider_11.set(1)
        self.slider_12.set(1)
        self.slider_13.set(1.2)
        self.slider_14.set(1.2)
        self.slider_15.set(0.8)
        self.slider_16.set(0.8)

        # time for the start and end 
        self.slider_17.set(20)
        self.slider_18.set(30)
        self.slider_19.set(20)


        text = f"""
        Curent Config is: 
        Phase 0: {self.slider_1.get():.02f} {self.slider_9.get():.02f}
        Phase 1: {self.slider_2.get():.02f} {self.slider_10.get():.02f}
        Phase 2: {self.slider_3.get():.02f} {self.slider_11.get():.02f}
        Phase 3: {self.slider_4.get():.02f} {self.slider_12.get():.02f}
        Phase 4: {self.slider_5.get():.02f} {self.slider_13.get():.02f}
        Phase 5: {self.slider_6.get():.02f} {self.slider_14.get():.02f}
        Phase 6: {self.slider_7.get():.02f} {self.slider_15.get():.02f}
        Phase 7: {self.slider_8.get():.02f} {self.slider_16.get():.02f}
        start constant time: {self.slider_17.get():.02f}s
        split time: {self.slider_18.get():.02f}s
        end constant time: {self.slider_19.get():.02f}s"""
        self.label_info_3.configure(text= text)

    def Preset4(self):
        #speed
        self.slider_1.set(0.0)
        self.slider_2.set(0.0)
        self.slider_3.set(0.0)
        self.slider_4.set(0.8)
        self.slider_5.set(1.2)
        self.slider_6.set(1.1)
        self.slider_7.set(1.0)
        self.slider_8.set(0.4)
        # acceleration 
        self.slider_9.set(0.8)
        self.slider_10.set(1.2)
        self.slider_11.set(1)
        self.slider_12.set(1)
        self.slider_13.set(1.2)
        self.slider_14.set(1.2)
        self.slider_15.set(0.8)
        self.slider_16.set(0.8)   

       # time for the start and end 
        self.slider_17.set(20)
        self.slider_18.set(30)
        self.slider_19.set(20)


        text = f"""
        Curent Config is: 
        Phase 0: {self.slider_1.get():.02f} {self.slider_9.get():.02f}
        Phase 1: {self.slider_2.get():.02f} {self.slider_10.get():.02f}
        Phase 2: {self.slider_3.get():.02f} {self.slider_11.get():.02f}
        Phase 3: {self.slider_4.get():.02f} {self.slider_12.get():.02f}
        Phase 4: {self.slider_5.get():.02f} {self.slider_13.get():.02f}
        Phase 5: {self.slider_6.get():.02f} {self.slider_14.get():.02f}
        Phase 6: {self.slider_7.get():.02f} {self.slider_15.get():.02f}
        Phase 7: {self.slider_8.get():.02f} {self.slider_16.get():.02f}
        start constant time: {self.slider_17.get():.02f}s
        split time: {self.slider_18.get():.02f}s
        end constant time: {self.slider_19.get():.02f}s"""
        self.label_info_3.configure(text= text)

    
    def slider_event(self,b):
        
        text = f"""
        Curent Config is: 
        Phase 0: {self.slider_1.get():.02f} {self.slider_9.get():.02f}
        Phase 1: {self.slider_2.get():.02f} {self.slider_10.get():.02f}
        Phase 2: {self.slider_3.get():.02f} {self.slider_11.get():.02f}
        Phase 3: {self.slider_4.get():.02f} {self.slider_12.get():.02f}
        Phase 4: {self.slider_5.get():.02f} {self.slider_13.get():.02f}
        Phase 5: {self.slider_6.get():.02f} {self.slider_14.get():.02f}
        Phase 6: {self.slider_7.get():.02f} {self.slider_15.get():.02f}
        Phase 7: {self.slider_8.get():.02f} {self.slider_16.get():.02f}
        start constant time: {self.slider_17.get():.02f}s
        split time: {self.slider_18.get():.02f}s
        end constant time: {self.slider_19.get():.02f}s"""
        self.label_info_3.configure(text= text)

    def button_event(self):
        print("Button pressed")

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


    # customized function for the gait estimation and control 
    def azimuth(self,point1, point2):
        '''azimuth between 2 shapely points (interval 0 - 360)'''
        angle = np.arctan2(point2.x - point1.x, point2.y - point1.y)
        return np.degrees(angle) if angle >= 0 else np.degrees(angle) + 360

    def ob2ac(self,angles):
        output = []
        for angle in angles: 
            if angle > 180:
                angle = 360 - angle
            output.append(angle)
        return output  

    def ang2vert(self,path):
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

        azimuth = self.azimuth
        return self.ob2ac([azimuth(point1,point2),azimuth(point2,point3),\
            azimuth(point3,point4),azimuth(point5,point6),azimuth(point6,point7),azimuth(point7,point8),azimuth(point7,point3)])

    def ang2vertPoint(self,pose_keypoints):
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

        azimuth = self.azimuth
        return self.ob2ac([azimuth(point1,point2),azimuth(point2,point3),\
            azimuth(point3,point4),azimuth(point5,point6),azimuth(point6,point7),azimuth(point7,point8),azimuth(point7,point3)])


    def runAI(self):
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

            # Starting OpenPose
            opWrapper = op.WrapperPython()
            opWrapper.configure(params)
            opWrapper.start()

            # Process Image 
            datum = op.Datum()

            # matlab sesssion
            import matlab.engine
            from time import sleep
            from time import time
            

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
            sleep(self.slider_17.get())
            for i in range(5,-1,-1):
                print("Split-belt mode: count down: ",i)
                sleep(1)

            timeout = time() + self.slider_18.get()
            while True:
                # image = cv2.imread(os.path.join(folder,name))
                
                ret, image = vid.read()
                # print(ret)
                imageToProcess = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                datum.cvInputData = imageToProcess
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))
                
                # Display Image
                
                # print("Length of keypoints: " + str(len(datum.poseKeypoints[0])))
                # print("Body keypoints: \n" + str(datum.poseKeypoints))
                # if datum.poseKeypoints== None:
                if datum.poseKeypoints is not None:
                    
                    angle = self.ang2vertPoint(datum.poseKeypoints[0])
                    
                    pred = clf.predict([angle])
                    y=pred[0]
                    print("The phase prediciton is : " + str(y))
                    if pred == None:
                        pass
                    if y ==0:
                        eng.eval(f'tm_set(remote,{self.slider_1.get()},{self.slider_9.get()})',nargout=0)
                    if y ==1:
                        eng.eval(f'tm_set(remote,{self.slider_2.get()},{self.slider_10.get()})',nargout=0)
                    if y ==2:
                        eng.eval(f'tm_set(remote,{self.slider_3.get()},{self.slider_11.get()})',nargout=0)
                    if y ==3:
                        eng.eval(f'tm_set(remote,{self.slider_4.get()},{self.slider_12.get()})',nargout=0)
                    if y == 4:
                        eng.eval(f'tm_set(remote,{self.slider_5.get()},{self.slider_13.get()})',nargout=0)
                    if y ==5:
                        eng.eval(f'tm_set(remote,{self.slider_6.get()},{self.slider_14.get()})',nargout=0)
                    if y == 6:
                        eng.eval(f'tm_set(remote,{self.slider_7.get()},{self.slider_15.get()})',nargout=0)
                    if y == 7:
                        eng.eval(f'tm_set(remote,{self.slider_8.get()},{self.slider_16.get()})',nargout=0)

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
            sleep(self.slider_19.get())
            print("Slow down")
            eng.eval('tm_set(remote,0,0.1)',nargout=0)
            sleep(2)
            # end session
            eng.eval('fclose(remote)',nargout =0)
        except Exception as e:
            print(e)
            sys.exit(-1)


if __name__ == "__main__":
    app = App()
    app.mainloop()