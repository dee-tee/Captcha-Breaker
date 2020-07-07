from imutils import paths
import argparse
import imutils
import cv2
import os
import sys

#Parse the arguments
ap=argparse.ArgumentParser()
ap.add_argument("-i","--input",required=True,help="path to input directory of images")
ap.add_argument("-a","--annot",required=True,help="path to output directory of annotations")
args=vars(ap.parse_args())

#grab the image paths and initialize the dictionary of character
#counts
imagePaths=list(paths.list_images(args["input"]))
counts={}

#loop over image paths 
for (i,imagePath) in enumerate(imagePaths):
    #display an update
    print(f"[PROCESSING IMAGES]Currently processing {i+1}/{len(imagePaths)}")
    try:
         #loading the images and converting them to grayscale
         #add a border to ensure the digits on the border of the image are retained
         image=cv2.imread(imagePath)
         gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
         gray=cv2.copyMakeBorder(gray,8,8,8,8,cv2.BORDER_REPLICATE)
         #threshold image to reveal digits
         thresh=cv2.threshold(gray,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
         #find contours in the image,keeping only the four largest ones
         cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
         cnts=cnts[0]
         cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:4]
         #Loop over the contours
         for c in cnts:
             x,y,w,h=cv2.boundingRect(c)
             roi=gray[y-5:y+h+5,x-5:x+w+5]
             #display the character and then wait for keypress
             cv2.imshow("ROI",imutils.resize(roi,width=100))
             key=cv2.waitKey(0)
             if key==ord("`"):
                 print("[INFO]ignoring character")
                 continue
             #grab the key that was pressed and construct the path to output directory
             key=chr(key).upper()
             dirPath=os.path.sep.join([args["annot"],key])
             if not os.path.exists(dirPath):
                 os.makedirs(dirPath)
                 
             count=counts.get(key,1)
             p=os.path.sep.join([dirPath,f"{str(count).zfill(6)}.png"])
             cv2.imwrite(p,roi)
             counts[key]=count+1
    #Handles the keyboard interrupt when we want to stop annotation         
    except KeyboardInterrupt:
        print("[INFO]Ugh I dont want to do this anymore....that's what she said")
        break
    #catch the unexpected exception and print its type and line number
    except Exception as e:
        exception_type,exception_object,exception_traceback=sys.exc_info()
        line_number=exception_traceback.tb_lineno
        print("Exception type:",exception_type)
        print("Line Number",line_number)
        print("[INFO] skipping image......")
    
cv2.destroyAllWindows()      
        
                    
        