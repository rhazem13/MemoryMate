
from MachineLearning.Alzahemer_Detection.Alzhemer import prediction
from flask import request, jsonify, Blueprint 
from MachineLearning.test import readb64

ALZhemer = Blueprint('Alzahemer', __name__)



@ALZhemer.route('/Predict', methods=['POST'])
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


@ALZhemer.route('/PredictBase64', methods=['POST'])
def Predicit():
         pic =request.json['pic']
         # img_path =  "Alzhiemer/Tests/" + pic
          
         # pic.save(img_path)

         img = readb64(pic)

         predict_result = prediction(img)

         
         return predict_result
               

            

             
        

                