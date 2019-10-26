import pdfProcess
import UI1
import os
import cv2
if __name__=="__main__":
    component_name = input("Please Enter the component:")
    # read component , convert to jpg
    pin_img = pdfProcess.find_chart.Convert2Jpg(component_name) 
    pdfProcess.table.box_extraction(cv2.imread(os.path.join("pdfProcess","tests",component_name,component_name+".jpg")),component_name)
    pinNameList=pdfProcess.pdfplum.readPinNameFile(os.path.join("pdfProcess","tests",component_name,"pinName.txt"))
    textList=[]
    pages=pdfProcess.pdfplum.textExtract(os.path.join("pdfProcess","tests",component_name,component_name+".pdf"),textList)
    usefulPg=pdfProcess.pdfplum.findUsefulPg(textList,pages,pinNameList,component_name)
    
