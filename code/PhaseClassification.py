# Author: Shengting Cao

import os
import os.path as osp
import cv2
import numpy as np

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
#             for imName in os.listdir(osp.join(dataFolder,subject,speed,phase))[:6]:
#                 labels.append(int(phase[-1]))
#                 image = cv2.imread(osp.join(dataFolder,subject,speed,phase,imName))
#                 imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
#                 imageRGB = cv2.resize(imageRGB,(imageSize,imageSize),interpolation=cv2.INTER_CUBIC)
#                 training_data.append(imageRGB)
#                 # cv2.imshow("images: ", imageRGB)
#                 # cv2.waitKey(0)
# labels = np.asarray(labels)
# training_data = np.asarray(training_data)
# print(training_data.shape,labels.shape)
# print(labels)
# np.save("training_data_224_first6.npy",training_data)
# np.save("labels_224_first6.npy",labels)

training_data = np.load('training_data_224_first6.npy')
labels = np.load('labels_224_first6.npy')

from tensorflow import keras
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.applications.resnet_v2 import preprocess_input, decode_predictions
from keras.utils import to_categorical
import tensorflow as tf

cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath='checkpoint224first6/saved_weights{epoch:08d}.h5', 
    verbose=1, 
    save_weights_only=True,
    period= 10)

physical_devices = tf.config.list_physical_devices('GPU')
for gpu_instance in physical_devices:
  tf.config.experimental.set_memory_growth(gpu_instance, True)

model = ResNet50V2(input_shape=(224,224,3),weights=None,classes = 8 )
model.compile(loss="categorical_crossentropy",optimizer='adam',metrics  = ['accuracy'])
X = preprocess_input(training_data)
y = to_categorical(labels,num_classes = 8)
model.fit(X,y,epochs=1000,batch_size =32,callbacks=[cp_callback])
model.save('utmb_resnet50v2_224_first6.h5')
