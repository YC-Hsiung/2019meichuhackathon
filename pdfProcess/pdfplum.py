import pdfplumber as plum
import numpy as np
import pytesseract as pyt
import os
import cv2
from skimage.measure import compare_ssim 
from pdf2image import convert_from_path, convert_from_bytes

def isChart(img,component):
    ##constants
    convert_width=img.shape[1]
    convert_height=img.shape[0]
    if convert_width<10 or convert_height < 10:
        return False
    threshold_chart_similarity=0.5
    threshold_component_similarity=0.7
    ##constants
    chart_img=cv2.imread("chart.png")
    #conver images to gray for compare
    clone_gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clone_gray_chart_img=cv2.cvtColor(cv2.resize(chart_img.copy(),(convert_width,convert_height)),cv2.COLOR_BGR2GRAY)
    clone_gray_component_img=cv2.cvtColor(cv2.resize(component.copy(),(convert_width,convert_height)),cv2.COLOR_BGR2GRAY)
    score1 = compare_ssim(clone_gray_chart_img,clone_gray_img,full=True)[0]
    score2 = compare_ssim(clone_gray_component_img,clone_gray_img,full=True)[0]
    print(score1,score2)
    if score1>threshold_chart_similarity and score2<threshold_component_similarity:
        return True
    return False

    """
     #try to eliminate original pin_img
    score=compare_ssim(clone_gray_pin_img,clone_gray_candidates[i],full=True)[0]
        print(score)
        if score<threshold_pin_similarity:
            new_candidates.append(clone_gray_candidates[i])
    print("completed")   
    #try to choose chart
    print("choosing image similar to chart")
    charts=[]
    for i,gray_candidate in enumerate(new_candidates):#calculate similarity score
        score=compare_ssim(clone_gray_chart_img,gray_candidate,full=True)[0]
        print(score)
        if score>threshold_chart_similarity:
            charts.append(new_candidates[i])
    return charts
""" 

def isContainTable(img):
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
    contours,hierachy=cv2.findContours(img_final_bin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    imageList = list();
    if contours:
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            imageList.append(img[y:y+h,x:x+w])
        return (True,imageList)
    else:
        return (False,[])

def textExtract(fname,textList):
    with plum.open(fname) as pdf:
        page_count = len(pdf.pages)
        print(page_count)
        for page in pdf.pages:
            print('--------------pg[%d]----------------' % page.page_number)
            textList.append(page.extract_text())
            #print(page.extract_text())
        return pdf.pages
    with plum.open(fname) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            for pdf_table in page.extract_tables(table_settings={
                                                "vertical_strategy": "lines",
                                                "horizontal_strategy": "lines",
                                                "intersection_tolerance": 20}):
                for row in pdf_table:
                    print([re.sub('\s+','',cell)if cell is not None else None for cell in row])


def findUsefulPg(textList, pages, pinNameList,component_name):
    component = cv2.imread(os.path.join("pdfProcess","tests",component_name,component_name+".png")
    frequency = [0]*len(pages)
    usefulPg = list()
    for i,pg in enumerate(pages):
        isTable = False
        table_img_list = list()
        pgText = textList[i]
        pgImg = cv2.imread(os.path.join("pdfProcess","tests",component_name,component_name,str(i+1)+".jpg")
        isTable, table_img_list = isContainTable(pgImg)
        for name in pinNameList:
            if name in pgText:
                frequency[i]+=1
        if frequency[i]>0.3*len(pinNameList) and isTable :
            usefulPg.append(pg)
            for j,tb in enumerate(table_img_list):
                if isChart(tb, component):
                    cv2.imwrite(os.path.join("pdfProcess","tests",component_name,"PinChart","p"+str(i+1)+"_"+str(j)+".jpg"),tb)
    return usefulPg

def readPinNameFile(fname):
    fin = open(fname, "r")
    pinNameList = list()
    for line in fname:
        pinNameList.append(line)
    return pinNameList
if __name__=="__main__":
    textList = list()
    pages = list()
    usefulPg = list()
    pinNameList = list()
    pinNameList = readPinNameFile("./tests/ds093/pinName")
    pages = textExtract("./tests/ds093/ds093.pdf",textList)
    usefulPg = findUsefulPg(textList, pages, pinNameList)
