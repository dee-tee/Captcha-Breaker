from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from helper import preprocess
from imutils import contours
from imutils import paths
import argparse
import cv2
import imutils
import numpy as np

#Parse the arguments
ap=argparse.ArgumentParser()
ap.add_argument("-c", "--captcha",required=True,help="path to input directory of captcha images")
ap.add_argument("-m","--model",required=True,help="path to input model")
args=vars(ap.parse_args())

#load the pre-trained network
print("[INFO] loading pre trained network.....")
model=load_model(args["model"])

#store captcha image paths
imagePaths=list(paths.list_images(args["captcha"]))
for imagePath in imagePaths:
    image=cv2.imread(imagePath)
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray=cv2.copyMakeBorder(gray,20,20,20,20,cv2.BORDER_REPLICATE)
    
    #thresholding the image
    thresh=cv2.threshold(gray,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
    
    #find contours in the image keeping only the four with the largest areas
    cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=cnts[0]
    cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:4]
    #Sorting the contours from left to right 
    #(in the order in which they appear in the captchaimage)
    cnts=contours.sort_contours(cnts)[0]
    
    #initialize the output image along with output predictions
    output=cv2.merge([gray]*3)
    predictions=[]
    
    #loop over the contours
    for c in cnts:
        #computing the bounding box and then extracting the digit
        (x,y,w,h)=cv2.boundingRect(c)
        roi=gray[y-5:y+h+5,x-5:x+w+5]
        #preprocess the roi and then classify it
        roi=preprocess(roi,28,28)
        roi=np.expand_dims(img_to_array(roi), axis=0)/255.0
        pred=model.predict(roi).argmax(axis=1)[0]
        predictions.append(str(pred))
        
        #draw the prediction on the output image
        cv2.rectangle(output,(x-2,y-2),(x+w+4,y+h+4),(0,0,255),1)
        cv2.putText(output,str(pred),(x-5,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.60,(255,0,0),2)
    predictions="".join(predictions)    
    #show the output image
    print(f"Shhh Not a Robot : {predictions}")
    cv2.imshow("Output",output)
    cv2.waitKey()
    
cv2.destroyAllWindows()