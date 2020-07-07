import imutils
import cv2

def preprocess(image,width,height):
    #grab the dimensions of the image, then initialize padding
    (h,w)=image.shape[:2]
    #if the width is greater then the height then resize along the width
    if w>h:
        image=imutils.resize(image,width=width)
        
    #else height is greater than width hence resize along the height
    else:
        image=imutils.resize(image,height=height)
    #determining the padding values for width and height to obtain target dimension    
    padW=int(width-image.shape[1]/2.0)
    padH=int(height-image.shape[0]/2.0)
    
    #padding the image 
    image=cv2.copyMakeBorder(image,padH,padH,padW,padW,cv2.BORDER_REPLICATE)
    #one final resizing to handle any rounding issues
    image=cv2.resize(image,(width,height))
    
    #returning the preprocessed image
    return image
