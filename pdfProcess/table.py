import cv2
import os
import numpy as np
import pytesseract
from PIL import Image,ImageEnhance

def box_extraction(img,component_name):
    (thresh, img_bin) = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY,cv2.THRESH_OTSU)
    img_bin=255-img_bin

    kernel_length=np.array(img).shape[1]//40
    vertical_kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(1,kernel_length))
    hori_kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_length,1))
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

    img_temp1=cv2.erode(img_bin,vertical_kernel,iterations=1)
    vertical_lines_img=cv2.dilate(img_temp1,vertical_kernel,iterations=1)
    # cv2.imwrite('vertical.jpg',vertical_lines_img)

    img_temp2=cv2.erode(img_bin,hori_kernel,iterations=1)
    horizontal_lines_img=cv2.dilate(img_temp2,hori_kernel,iterations=1)
    # cv2.imwrite('horizontal.jpg',horizontal_lines_img)

    alpha=0.5
    beta=1-alpha
    img_final_bin=cv2.addWeighted(vertical_lines_img,alpha,horizontal_lines_img,beta,0)
    # img_final_bin=cv2.erode(img_final_bin,kernel,iterations=1)
    # img_final_bin=cv2.dilate(img_final_bin,kernel,iterations=1)
    # (thresh,img_final_bin)=cv2.threshold(img_final_bin,128,255,cv2.THRESH_BINARY,cv2.THRESH_OTSU)
    # cv2.imwrite('temp.jpg',img_final_bin)
    img_final_bin=cv2.cvtColor(img_final_bin,cv2.COLOR_BGR2GRAY)
    contours,hierachy=cv2.findContours(img_final_bin,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # (contours,boundingBoxes)=cv2.sort_contours(contours,method="top-to-bottom")
    textlist=[]
    for i in range(len(contours)):
        x,y,w,h=cv2.boundingRect(contours[i])

        if(w>10 and h>10) and w>h:
            # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            new_img=img[y:y+h,x:x+w]
            cv2.imwrite(os.path.join("pdfProcess","tests",component_name,"tableSeg",str(i+1)+".jpg"),new_img)
            text=totext(os.path.join("pdfProcess","tests",component_name,"tableSeg",str(i+1)+".jpg"))
            textlist.append([(x,y),text])
    textlist=textlist[2:]
    out=open(os.path.join("pdfProcess","tests",component_name,"pinName.txt"),'w')
    for item in textlist:
        out.write("(%s,%s) %s\n"%(item[0][0],item[0][1],item[1]))
    #print(textlist)
    #cv2.imshow('contour',img)
    #cv2.waitKey(0)


def totext(filename):
    im=Image.open(filename)
    im=im.resize((im.width*1,im.height*1))
    imgray=im.convert('L')
    sharpness=ImageEnhance.Contrast(imgray)
    sharp_img=sharpness.enhance(1)
    text=pytesseract.image_to_string(sharp_img,config="-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXY(1)(2)(3)(4)(5)(6)(7)(8)(9)(0)/#*")
    return text
if __name__=='__main__':
    img = cv2.imread('./problem/ds093/ds093.png')
    box_extraction(img)

