import numpy as np
import cv2
from PIL import ImageGrab

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
vid = cv2.VideoWriter('record1.avi',fourcc, 8,(590,490))  #  아래 x,y, w,h  보고 계산
while(True):
    img = ImageGrab.grab(bbox=(10, 10, 600, 500))
    img_np = np.array(img)
    #frame = cv2.cvtColor(imp_np, cv2.COLOR_BGR2GRAY)
    vid.write(img_np)
    cv2.imshow("frame", img_np)
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
