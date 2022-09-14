from email.mime import image
from pickle import BINFLOAT
from turtle import back
from PIL import Image
import PIL.ImageOps
import urllib.request
import numpy as np
import cv2


def Reformat_Image(lst):
    for i in range(0, len(lst)):
        try:
            url_response = urllib.request.urlopen(lst[i]["url"])
            img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, -1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            width = img.shape[1]
            height = img.shape[0]


        except:
            break

        background = None


        if(width != height):
            bigside = width if width > height else height

            # resize the image 
            background = np.zeros((bigside, bigside,3), np.uint8)
            background[np.where((background==[0,0,0]).all(axis=2))] = [255,255,255]
            background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
            midpoint = bigside//2

            # width dominant
            if width == bigside:
                coordinates = 0 , midpoint - (height//2)


            else:
                coordinates = midpoint - (width//2) , 0


            # put image into smaller designated square background
            background[coordinates[1]:coordinates[1]+height, coordinates[0]:coordinates[0]+width] = img

        else:
            print("Image " + str(lst[i]["imgID"]) + " is not resized due to some error!")



        # scale smaller image
        background = img if background is None else background
        background = cv2.resize(background,(1000,1000), cv2.INTER_AREA)
        img = background



        # add white background
        back_img = cv2.imread("src/background.jpg")
        bg_w, bg_h = back_img.shape[1], back_img.shape[0]
        back_img = cv2.cvtColor(back_img, cv2.COLOR_BGR2RGB)
        width, height = img.shape[1], img.shape[0]

        midpoint = bg_w//2, bg_h//2
        coordinates = midpoint[0] - (width//2) , midpoint[1] - (height//2)


        back_img[coordinates[1]:coordinates[1]+height, coordinates[0]:coordinates[0]+width] = img

        # resize and save image
        cv2.resize(back_img, (1920, 1080), cv2.INTER_AREA)
        
        imgID = lst[i]["imgID"]
        cv2.imwrite("processed/" + imgID, cv2.cvtColor(back_img, cv2.COLOR_BGR2RGB))
        print("Image " + imgID + " has been edited and saved!")


