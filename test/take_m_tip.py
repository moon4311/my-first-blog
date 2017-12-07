import numpy as np
import cv2
import pyautogui as gui
from PIL import ImageGrab
from matplotlib import pyplot as plt



# 1. 스크린 인식
def read_screen() :
    # fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    # vid = cv2.VideoWriter('record1.avi',fourcc, 8,(590,490))  #  아래 x,y, w,h  보고 계산
    i=0
    box1 = []
    img_np = ""
    kernel = np.ones((2, 2), np.uint8)
    while(True):

        img = ImageGrab.grab(bbox=(10, 10, 800, 700))

        # 2. 데이터 추출  Labeling >  Contour Tracing > Get Contour Information
        img_np = np.array(img)
        dila = cv2.dilate(img_np,kernel, iterations=1) # 1 . 확장 dilate
        b,g,r = cv2.split(dila)
        invert = cv2.merge([255-r,255-g,255-b])   # 2. 색반전
        erod = cv2.dilate(invert,kernel, iterations=1) # 3 . 축소 erode

        frame = cv2.cvtColor(erod, cv2.COLOR_BGR2GRAY)  # 4 Gray 화
        # erod = cv2.erode(frame,kernel,iterations=1) # 4. 축소
        # blur = cv2.GaussianBlur(frame,(1,1),0)  # http://bskyvision.com/24
        # blia = cv2.bilateralFilter(frame,100,1,1)  # http://bskyvision.com/24

        canny = cv2.Canny(frame,i,i)   # 5.2진화    http://emaru.tistory.com/15
        # cv2.Canny()
        # cv2.imshow("frame", frame)  #  1. gray
        # cv2.imshow("frame", blur)    # 2. 가우시안blur 필터
        cv2.imshow("frame", canny)    # 3. Canny 필터

        cnts,contours,hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        i+=1

        key = cv2.waitKey(1)
        if key == 27:
            print("i : ", i)
            break

    print("while")
    for j in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        rect_area = w * h  # area size
        aspect_ratio = float(w) / h  # ratio = width/height
        if (aspect_ratio >= 0.2) and (aspect_ratio <= 1.0) and (rect_area >= 100) and (rect_area <= 700):
            cv2.rectangle(img_np, (x, y), (x + w, y + h), (0, 255, 0), 1)
            box1.append(cv2.append(cv2.boundingRect(cnt)))
    # cv2.imshow("frame", img_np)


    cv2.waitKey(0)
    cv2.destroyAllWindows()

read_screen()

