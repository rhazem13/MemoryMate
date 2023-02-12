import os
from urllib import response
from MachineLearning.Alzahemer_Detection.Alzhemer import prediction
from flask import Flask, request, jsonify,Response
from flask import Flask, render_template, request
import pandas as pd
import cv2
import numpy as np
import base64
from werkzeug.utils import secure_filename

ALZhemer = Flask(__name__)

UPLOAD_FOLDER = 'static\image'


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ALZhemer.route('/AD', methods=['GET', 'POST'])

def Predicit():
      file = request.files['file']
      filename = secure_filename(file.filename)
      Photo =  file.save(os.path.join(UPLOAD_FOLDER, filename))

      return prediction(Photo)
        
            

    
                    

    
if __name__ == '__main__':
    ALZhemer.run()