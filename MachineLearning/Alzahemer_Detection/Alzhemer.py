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

model = load_model('../../../../Alzahemer_Detection/AlzhemersModel.h5')
## print(model.summary())


class_avaible = ["Mild Dementia" , "Moderate Dementia" , "Non Demetia" , "Very Mild Dementia"]
def prediction(image):
    

    img = load_img(image, target_size = (224,224,3))
    img = img_to_array(img)
    img = img/255
    imshow(img)
    plt.axis('off')
    img = np.expand_dims(img,axis=0)
    answer = model.predict(img)
    probability = round(np.max(model.predict(img)*100),2)
    probability /=100
    if probability > 0.5:
        Brain = str('%.2f' % (probability * 100) + '% Alzhemer')
    else:
        Brain = str('%.2f' % ((1 - probability) * 100) + '% NonAlzhemer')

    print(probability, '% chances are there that the image is' , class_avaible[np.argmax(model.predict(img))])
 
    # return f"{probability} % chances are there that the image is , {class_avaible[np.argmax(model.predict(img))]}"

    return {"probability":Brain  , "Class":class_avaible[np.argmax(model.predict(img))]}
