import os
from PIL import Image
import pytesseract as pyt
import pdf2image
def pdf2jpg(fname):
    path = fname[:fname.find('.')]
    exist = False
    image = list()
    if(not os.path.isdir(path)):
        os.mkdir(path)
        image = pdf2image.convert_from_path(fname, 900, fmt="JPEG")
    else:
        dirs = os.listdir(path)
        for fname in dirs:
            image.append(Image.open(path+"/"+fname))
        exist = True

    for i,pg in enumerate(image):
        if not exist:
            outfile = os.path.join(path,str(i+1)+".jpg")
            pg.save(outfile, "JPEG")
    return len(image)

