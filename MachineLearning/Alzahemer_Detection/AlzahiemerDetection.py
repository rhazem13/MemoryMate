
import os
from keras.models import load_model
import  numpy as np
from PIL import Image
import numpy as np
import os 
from keras.utils import load_img, img_to_array
from keras.models import load_model 
import numpy as np  

cwd = os.getcwd()


relative_path = os.path.join(cwd,  'alzheimer_cnn_model.h5')

model = load_model(relative_path, compile=False)

verbose_name = {
    0: "Non Demented",
    1: "Very Mild Demented",
    2: "Mild Demented",
    3: "Moderate Demented",
}
def predict(image):
    
    test_image = Image.open(image).convert("L")
    test_image = test_image.resize((128, 128))
    test_image = img_to_array(test_image) / 255.0
    test_image = test_image.reshape(-1, 128, 128, 1)

    predict_x = model.predict(test_image)
    classes_x = np.argmax(predict_x, axis=1)
    probability = round(np.max(model.predict(test_image)*100),2)
    probability /=100
  
    if probability != 1.0:
        Brain = str('%.2f' % (probability * 100) + '% Alzhemer')
    else:
        Brain = str('%.2f' % ((1 - probability) * 100) + '% NonAlzhemer')

    # print(f'probability:{Brain}  , Class:{verbose_name[classes_x[0]]}')
 
    

    return {"probability":Brain  , "Class":verbose_name[classes_x[0]]}
