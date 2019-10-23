import pytesseract as pyt
from PIL import Image

if __name__ == "__main__":
    image = Image.open("circuit.jpeg")  
    image2 = Image.open("circuit.png")
    text1 = pyt.image_to_string(image)
    text2 = pyt.image_to_string(image2)
    print(text1)
    print(text2)
