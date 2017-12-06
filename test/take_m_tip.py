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

        blur = cv2.GaussianBlur(frame,(1,1),0)
        canny = cv2.Canny(blur,0,0)   # http://emaru.tistory.com/15
        # cv2.Canny()
        # cv2.imshow("frame", frame)  #  1. gray
        # cv2.imshow("frame", blur)    # 2. 가우시안blur 필터
        cv2.imshow("frame", canny)    # 3. Canny 필터


        key = cv2.waitKey(1)
        if key == 27:
            break


    cv2.waitKey(0)
    cv2.destroyAllWindows()

read_screen()

