
from MachineLearning.Alzahemer_Detection.Alzhemer import prediction
from flask import request, jsonify, Blueprint


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


     
               

            

             
        

                