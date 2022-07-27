from tensorflow import keras
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.applications.resnet_v2 import preprocess_input, decode_predictions
from keras.utils import to_categorical
import tensorflow as tf
import cv2
from time import sleep
import numpy as np
model = ResNet50V2(input_shape= (224,224,3),weights=None,classes = 8 )
model.load_weights(r'D:\Shengting\checkpoint224first6\saved_weights00000500.h5')
# model = keras.models.load_model(r'D:\Shengting\utmb_resnet50v2_224_first6.h5')
camera = cv2.VideoCapture(1)


# matlab.engine.shareEngine
import matlab.engine
eng = matlab.engine.connect_matlab()
print(matlab.engine.find_matlab())
eng.addpath(r"C:\Program Files (x86)\Bertec\Treadmill\Remote")
eng.workspace['remote'] = eng.eval("tcpip('localhost',4000);")
eng.eval('fopen(remote)',nargout=0)
eng.eval('tm_set(remote,0.5,0.1)',nargout=0)
sleep(20)
print('Start')
while True:
    
    if not camera.isOpened():
        print('unable to load camera')
        sleep(5)
    return_value, image = camera.read()
    imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    imageRGB = cv2.resize(imageRGB,(224,224),interpolation=cv2.INTER_CUBIC)
    # print(image.shape,imageRGB.shape)
    X = preprocess_input(imageRGB)
    # print(X.shape)
    X = np.expand_dims(X, axis=0)
    y = model.predict(X,verbose = 0)
    print(np.argmax(y))
    if np.argmax(y) ==0:
        eng.eval('tm_set(remote,1,1)',nargout=0)
    if np.argmax(y) ==1:
        eng.eval('tm_set(remote,1,1)',nargout=0)
    if np.argmax(y) ==2:
        eng.eval('tm_set(remote,1,1)',nargout=0)
    if np.argmax(y) ==3:
        eng.eval('tm_set(remote,0.3,1)',nargout=0)
    if np.argmax(y) == 4:
        eng.eval('tm_set(remote,0.3,1)',nargout=0)
    if np.argmax(y) ==5:
        eng.eval('tm_set(remote,0.3,1)',nargout=0)
    if np.argmax(y) == 6:
        eng.eval('tm_set(remote,0.3,1)',nargout=0)
    if np.argmax(y) == 7:
        eng.eval('tm_set(remote,0.3,1)',nargout=0)
    sleep(0.001)
    cv2.imshow('real time image:',image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
eng.eval('tm_set(remote,0,0.1)',nargout=0)
sleep(10)
eng.eval('fclose(remote)',nargout =0)

camera.release()
cv2.destroyAllWindows()


