#import the required packages
import argparse
import requests
import time
import os
#Parse the arguments
ap=argparse.ArgumentParser()
ap.add_argument("-o","--output",required=True,help="path to ouput directory of images")
ap.add_argument("-n","--num_images",type=int,default=500,help="Number of images to download")
args=vars(ap.parse_args())
url="Enter URL here"
total=0
#Loop over the number of images
for i in range(0,args["num_images"]):
    try:
        #try to grab a captcha image
        r=requests.get(url,timeout=60)
        p=os.path.sep.join([args["output"],f"{str(total).zfill(5)}.jpg"])
        f=open(p,"wb")
        f.write(r.content)
        f.close()
        #update the counter
        print(f"[INFO] downloaded image{p}")
        total+=1
    except:
        print("[INFO] Error downloading image....ohh give me my captcha image amour, quoth the server 404")
     #being courteous to the server  
    time.sleep(1)
    