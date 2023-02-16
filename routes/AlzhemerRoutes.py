import os
from tkinter import Image
from urllib import response
from MachineLearning.Alzahemer_Detection.Alzhemer import prediction
from flask import Flask, request, jsonify,Response, Blueprint
from flask import Flask, render_template, request
import pandas as pd
import cv2
import numpy as np
import base64
from werkzeug.utils import secure_filename


ALZhemer = Blueprint('Alzahemer', __name__)



@ALZhemer.route('/Predict', methods=['GET' , 'POST'])
def Predicit():
    if  request.method == 'POST':
         if 'pic' not in request.files:
            resp = jsonify({'message':'No file part in the request'})
            resp.status_code=400
            return resp
         pic =request.files['pic']
         img_path =  "Alzhiemer/Tests/" + pic.filename
          
         pic.save(img_path)

         predict_result = prediction(img_path)

         data = {
            "result": predict_result
            
            
        }
         
         return predict_result


     
               

            

             
        

                