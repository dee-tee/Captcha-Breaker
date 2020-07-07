from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.optimizers import SGD
from helper import preprocess
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2
import os
from nnetwork import LeNet

#Parsing the arguments
ap=argparse.ArgumentParser()
ap.add_argument("-d","--dataset",required=True,help="path to input dataset")
ap.add_argument("-m","--model",required=True,help="path to output model")
args=vars(ap.parse_args())

#Initializing the data and labels
data=[]
labels=[]
#loop over the input images
for imagePath in paths.list_images(args["dataset"]):
    
    #load the image, preprocess it and store it in the data list
    image=cv2.imread(imagePath)
    image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image=preprocess(image,28,28)
    image=img_to_array(image)
    data.append(image)

    #extract the label from image path and update the labels list
    label=imagePath.split(os.path.sep)[-2]
    labels.append(label)
    
#Scaling raw pixel intensities to range[0,1]

data=np.array(data,dtype=float)/255.0
labels=np.array(labels)
    
 #Partitioning the data into training and testing splits using 80% of data
 #for training and the remaining 20% for testing
(trainX,testX,trainY,testY)=train_test_split(data,labels,test_size=0.20,random_state=27)
    
#convert labels from integers to vectors
lb=LabelBinarizer().fit(trainY)
trainY=lb.transform(trainY)
testY=lb.transform(testY)
    
#initializing the LeNet Model
print('[INFO] compiling model....')
model=LeNet.build(width=28, height=28, depth=1, classes=10)
opt=SGD(lr=0.01)
model.compile(loss="categorical_crossentropy",optimizer=opt,metrics=["accuracy"])
    
#train the network
print("[INFO]training network....")
H=model.fit(trainX,trainY,validation_data=(testX,testY),batch_size=32,epochs=20,verbose=1)
    
#evaluate the network
print("[INFO] evaluating network...")
predictions=model.predict(testX,batch_size=32)
print(classification_report(testY.argmax(axis=1),predictions.argmax(axis=1),target_names=lb.classes_))
    
#Saving the model to disk
print("[INFO] serializing model....")
model.save(args["model"])
    
#Plot the training + testing loss and accuracy
#I am a big fan of R and ggplot when it comes to visualizations
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0,20),H.history["loss"],label="train_loss")
plt.plot(np.arange(0,20),H.history["val_loss"],label="val_loss")
plt.plot(np.arange(0,20),H.history["accuracy"],label="acc")
plt.plot(np.arange(0,20),H.history["val_accuracy"],label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch No.")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.show()
    
    
    
