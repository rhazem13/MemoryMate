import matplotlib.pyplot as plt
import os
from keras.models import load_model
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import  numpy as np
import numpy as np
import matplotlib.pyplot as plt
import os 
from keras.utils import load_img, img_to_array
from skimage.io import imshow
from keras.models import load_model 
import numpy as np  

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
