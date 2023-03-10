import os
import face_recognition as fr
import cv2
import numpy as np
import os
from flask import  request, jsonify, Blueprint
import cv2
import numpy as np
from MachineLearning.test import readb64


FaceRecognation = Blueprint('Face', __name__)

@FaceRecognation.route('/Save' , methods=['POST'])
def SaveIamage():
     
      if 'file' not in request.files:
            resp = jsonify({'message':'No file part in the request'})
            resp.status_code=400
            return resp
      pic =request.files['file']
      img_path =  "MachineLearning/Face_Recognation/train/" + pic.filename
          
      pic.save(img_path)


       
         
      return jsonify("Image Saved Successfully")

@FaceRecognation.route('/Rec', methods=['GET' , 'POST'])
def Recognation():
    def TestFaces(test_image):
        path = "MachineLearning/Face_Recognation/train/"

        known_names = []
        known_name_encodings = []
        images = os.listdir(path)
        for _ in images:
                image = fr.load_image_file(path + _)
                image_path = path + _
                encoding = fr.face_encodings(image)[0]
                known_name_encodings.append(encoding)
                known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())

                
       
        image = cv2.imread(test_image)
        

        face_locations = fr.face_locations(image)
        face_encodings = fr.face_encodings(image, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_name_encodings, face_encoding)
            name = "Unknown"

            face_distances = fr.face_distance(known_name_encodings, face_encoding)
            best_match = np.argmin(face_distances)

            if matches[best_match]:
                name = known_names[best_match]
            


            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

     
        # cv2.imwrite("MachineLearning/Face_Recognation/output.jpg", image)
       

        return {"The Person is": name}
    
    if  request.method == 'POST':
         
         if 'ph' not in request.files:
            resp = jsonify({'message':'No file part in the request'})
            resp.status_code=400
            return resp
         pic =request.files['ph']
         img_path =  "Faces/Tests/" + pic.filename
          
         pic.save(img_path)

         predict_result = TestFaces(img_path)

       
         
         return predict_result
    


@FaceRecognation.route('/RecBase64', methods=['POST'])
def RecognationBase64():
    def TestFaces(test_image):
        path = "MachineLearning/Face_Recognation/train/"

        known_names = []
        known_name_encodings = []
        images = os.listdir(path)
        for _ in images:
                image = fr.load_image_file(path + _)
                image_path = path + _
                encoding = fr.face_encodings(image)[0]
                known_name_encodings.append(encoding)
                known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())

                
       
        image = cv2.imread(test_image)
        

        face_locations = fr.face_locations(image)
        face_encodings = fr.face_encodings(image, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_name_encodings, face_encoding)
            name = "Unknown"

            face_distances = fr.face_distance(known_name_encodings, face_encoding)
            best_match = np.argmin(face_distances)

            if matches[best_match]:
                name = known_names[best_match]
            


            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

     
        # cv2.imwrite("MachineLearning/Face_Recognation/output.jpg", image)
       

        return {"The Person is": name}
    
    if  request.method == 'POST':
         
         if 'ph' not in request.json:
            resp = jsonify({'message':'No file part in the request'})
            resp.status_code=400
            return resp
         pic =request.json['ph']
        #  img_path =  "Faces/Tests/" + pic.filename
          
        #  pic.save(img_path)
        
         img = readb64(pic)

         predict_result = TestFaces(img)

       
         
         return predict_result