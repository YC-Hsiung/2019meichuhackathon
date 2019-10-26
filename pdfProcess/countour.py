import cv2
import pdf2image
import os
class Component:
    def __init__(name,pdfPath):
        self.name = name
        self.pdfPath = pdfPath
        self.pngPath = name+"/"+name+".png"
        if(not os.isdir(name)):
            os.mkdir(name)
    def pdf2Png():
        image = convert_from_path(self.pdfPath,900,fmt="PNG")
        image[0].save(self.pngPath,"PNG")
    def segmentation():
        image = cv2.imread(self.pngPath)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (11, 11), 0)
        binaryIMG = cv2.Canny(blurred, 20, 160) 
        (cnts, _) = cv2.findContours(binaryIMG.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        clone = image.copy()
        for i,c in enumerate(cnts):
            (x,y,w,h) = cv2.boundingRect(c)
            if(w>25 and h>25 and w<70):
                cv2.rectangle(clone,(x,y),(x+w,y+h),(0,255,0),2)
                cv3.imwrite(self.name+"/"+self.name+"_seg"+str(i)+".png",clone[y:y+h,x:x+w])

  
import cv2

image = cv2.imread("sample.jpg")
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)
binaryIMG = cv2.Canny(blurred, 20, 160) 
(cnts, _) = cv2.findContours(binaryIMG.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
clone = image.copy()
for c in cnts:
    (x,y,w,h) = cv2.boundingRect(c)
    if(w>25 and h>25 and w<70):
        cv2.rectangle(clone,(x,y),(x+w,y+h),(0,255,0),2)
cv2.imshow("countour",clone)
cv2.imwrite("countour.png",clone)
cv2.waitKey(0)
cv2.destroyAllWindows()

