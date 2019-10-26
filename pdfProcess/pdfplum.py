import pdfplumber as plum
import pandas as pd
import re
import pytesseract as pyt
from PIL import Image
import os
from pdf2image import convert_from_path, convert_from_bytes


def textExtract(fname,textList):
    with plum.open(fname) as pdf:
        page_count = len(pdf.pages)
        print(page_count)
        for page in pdf.pages:
            print('--------------pg[%d]----------------' % page.page_number)
            textList.append(test)
            print(page.extract_text())
        return pdf.pages
def tableExtract(fname):
    with plum.open(fname) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            for pdf_table in page.extract_tables(table_settings={
                                                "vertical_strategy": "lines",
                                                "horizontal_strategy": "lines",
                                                "intersection_tolerance": 20}):
                for row in pdf_table:
                    print([re.sub('\s+','',cell)if cell is not None else None for cell in row])

def pdf2jpg(fname):
    path = fname[:fname.find('.')]
    exist = False
    image = list()
    if(not os.path.isdir(path)):
        os.mkdir(path)
        image = convert_from_path(fname, 900, fmt="PNG")
    else:
        dirs = os.listdir(path)
        for fname in dirs:
            image.append(Image.open(path+"/"+fname))
        exist = True

    for i,pg in enumerate(image):
        if(not exist):
            outfile = path + "/"+fname[:fname.find('.')] + "-" + str(i+1) + ".png"
            pg.save(outfile, "PNG")
        text = pyt.image_to_string(pg)
        print(text)

def findUsefulPg(textList, pages, pinName):
    frequency = [0]*len(pages)
    usefulPg = list()
    for pg in pages:
        pgText = textList[pg.page_number]
        for name in pinName:
            if(name in pgText):
                frequency[pg.page_number]+=1
        if frequency[pg.page_number]>(len(textList)*0.8):
            usefulPg.append(pg)
            print(pg.page_number)
    return usefulPg

def readPinNameFile(fname):
    fin = open(fname, "r")
    pinNameList = list()
    for line in fname:
        list.append(line)
    return pinNameList
if __name__=="__main__":
    textList = list()
    pages = list()
    usefulPg = list()
    pinName = list()
    readPinNameFile("pinName")
    pages = textExtract("ads1298.pdf",testList)
    usefulPg = findUsefulPg(textList, pages, pinName)
