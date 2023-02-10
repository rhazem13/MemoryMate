import matplotlib.pyplot as plt
import os
from flask import Flask, request, jsonify
from keras.models import load_model
from flask import send_file
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import base64
import cv2
import  numpy as np
import matplotlib
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import skimage.io
import os 
import tqdm
import glob
import tensorflow as tf
from tqdm import tqdm
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from keras.utils import load_img, img_to_array
from skimage.io import imread, imshow
from skimage.transform import resize
from skimage.color import rgb2gray
import keras 
from keras.models import load_model 
import numpy as np  
from keras.applications.densenet import DenseNet169

model = load_model('AlzhemersModel.h5')
# print(type(model))






def prediction(image):
   
    img = load_img(image, target_size = (224,224,3))
    img = img_to_array(img)
    img = img /255
    inputs=tf.Tensor(shape=(img, 224, 224, 3), dtype=tf.float32, name='inputs')
    training=False
    mask=None
    imshow(img)
    plt.axis('off')
    image = np.expand_dims(inputs,axis=0)
    answer = model.predict(image)
    probability = round(np.max(model.predict(image)*100),2)
    print(f'probability : {probability } % of type  {answer}')

prediction("27.jpg")


