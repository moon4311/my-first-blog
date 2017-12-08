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
    print(im.split())
    pytesseract.image_to_string(im)

    # print(text)

OCR('ocr_test.jpg')