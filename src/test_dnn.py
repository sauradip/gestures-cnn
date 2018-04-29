import cv2                 
import numpy as np         
import os        

from random import shuffle 
from tqdm import tqdm   

import matplotlib.pyplot as plt


TRAIN_DIR = 'C:/Users/SAURADIP/Desktop/cnn/resized'
TEST_DIR = 'C:/Users/SAURADIP/Desktop/cnn/resized'

IMG_SIZE = 100 # Resizing and reshaping 

def process_test_data():
    testing_data = []
    for img in tqdm(os.listdir(TEST_DIR)):
        path = os.path.join(TEST_DIR,img)
        img_num = img[0]
        img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
        testing_data.append([np.array(img), img_num])
        
    shuffle(testing_data)
    np.save('test_data.npy', testing_data)
    return testing_data


# if i need to create the data:
#test_data = process_test_data()
# if i already have some saved:
try:
    test_data = np.load('test_data.npy')
except (FileNotFoundError):
    test_data = process_test_data()
    
show = 20 # number of images to be shown
col = 4 # no of columns to be displayed
fig = plt.figure()
labelss = []
predics = []

model.load("C:/Users/SAURADIP/Desktop/cnn/model/"+MODEL_NAME)

for num,data in enumerate(test_data[:show]):
    img_num = data[1]
    img_data = data[0]
    if img_num == "i":
        labelss.append(1)
    elif img_num == "v":
        labelss.append(2)
    elif img_num == "f":
        labelss.append(3)
    elif img_num == "t":
        labelss.append(4)
    
    y = fig.add_subplot((show/col),col,num+1)
    orig = img_data
    data = img_data.reshape(IMG_SIZE,IMG_SIZE,1)
    # model_out = model.predict([data])[0]
    model_out = (model.predict([data])[0]).round()
    if np.array_equal((model_out),np.array([1.,0.,0.,0.])):
        str_label = 'index'
        predics.append(1)
    elif np.array_equal((model_out),np.array([0.,1.,0.,0.]) ): 
        str_label = 'vshape'
        predics.append(2)
    elif np.array_equal((model_out) , np.array([0.,0.,1.,0.])): 
        str_label = 'fist'
        predics.append(3)
    elif np.array_equal((model_out) , np.array([0.,0.,0.,1.])): 
        str_label = 'thumb'
        predics.append(4)
    
        
    y.imshow(orig,cmap='gray')
    plt.title(str_label)
    y.axes.get_xaxis().set_visible(False)
    y.axes.get_yaxis().set_visible(False)

plt.tight_layout()
plt.show()

from sklearn.metrics import classification_report
print(classification_report(labelss, predics))