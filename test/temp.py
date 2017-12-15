import cv2
from PIL import ImageGrab
import numpy as np

while(True):
    img = cv2.imread("images/num33.png")
    # img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img2 = ImageGrab.grab(bbox=(492, 620, 512, 640))
    img2 = np.array(img2)
    cv2.i86mshow("frame", img2)

    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key != 27 :
        cv2.imwrite('images/num_6.jpg', img2)

