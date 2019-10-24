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
