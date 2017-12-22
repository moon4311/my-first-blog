from PIL import Image
import pytesseract
import cv2
import numpy as np
def OCR(imgfile, lang='eng'):

    # img1 = cv2.imread(imgfile)
    # img_np = np.array(img1)
    # cv2.imshow("f", img_np)
    # cv2.waitKey(0)
    im = Image.open(imgfile)
    text= pytesseract.image_to_string(im,lang=lang)
    print(text)

    # print(text)

# OCR('ocr_test.jpg')
OCR('korean_ocr.png','kor')