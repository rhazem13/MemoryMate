
from MachineLearning.Alzahemer_Detection.AlzahiemerDetection import predict
from flask import request, jsonify, Blueprint 
import base64
from PIL import Image
from io import BytesIO

ALZhemer = Blueprint('Alzahemer', __name__)



@ALZhemer.route('/Predict', methods=['POST'])
def Predicit():
    if  request.method == 'POST':
         if 'pic' not in request.files:
            resp = jsonify({'message':'No file part in the request'})
            resp.status_code=400
            return resp
         pic =request.files['pic']
         img_path =   pic.filename
         #  "Alzhiemer/Tests/" +
         pic.save(img_path)

         predict_result = predict(img_path)

         data = {
            "result": predict_result
            
            
        }
         
         return predict_result


@ALZhemer.route('/sendBase64', methods=['POST'])
def PredicitBase64():
         pic =request.json['pic']

         starter = pic.find(',')
         image_data = pic[starter+1:]
         image_data = bytes(image_data, encoding="ascii")
         image = BytesIO(base64.b64decode(image_data))
         im = Image.open(BytesIO(base64.b64decode(image_data)))
         
         #im.save('image.jpg')
       

         

         predict_result = predict(image)

         
         return predict_result
               

            

             
        

                