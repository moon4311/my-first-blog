import numpy as np
import cv2
import pyautogui as gui
from PIL import ImageGrab
from matplotlib import pyplot as plt



# 1. 스크린 인식
def read_screen() :
    # fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    # vid = cv2.VideoWriter('record1.avi',fourcc, 8,(590,490))  #  아래 x,y, w,h  보고 계산
    while(True):

        img = ImageGrab.grab(bbox=(10, 10, 600, 500))

        # 2. 데이터 추출  Labeling >  Contour Tracing > Get Contour Information
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        #vid.write(img_np)
        cv2.imshow("frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break
        print(np.array)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

read_screen()

