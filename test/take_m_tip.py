import numpy as np
import cv2
import pyautogui as gui
import pytesseract
from PIL import (Image, ImageGrab)
from matplotlib import pyplot as plt



# 1. 스크린 인식
def read_screen() :
    # fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
    # vid = cv2.VideoWriter('record1.avi',fourcc, 8,(590,490))  #  아래 x,y, w,h  보고 계산
    box1 = []
    img_np = ""
    kernel = np.ones((2, 2), np.uint8)
    # 2. 데이터 추출  Labeling >  Contour Tracing > Get Contour Information
    while(True):

        img = ImageGrab.grab(bbox=(30, 150, 600, 350))
        img_np = np.array(img)
        b,g,r = cv2.split(img_np)
        img_np = cv2.merge([r,g,b])
        img_np = cv2.pyrUp(img_np)                          # 이미지 가로x2 세로x2
        origin = img_np

        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)   # Gray 화
        img_np = cv2.Canny(img_np,50,50)                     # 2진화


        # img_np = cv2.dilate(img_np,kernel, iterations=1)    # 확장 dilate
        # img_np = cv2.resize(invert,(1000,400),interpolation=cv2.INTER_CUBIC)  ## 크기 확대
        # img_np = cv2.pyrDown(img_np)                      # 이미지 가로x1/2 세로x1/2
        # img_np = 255 - img_np                             # 색반전
        # img_np = cv2.erode(img_np,kernel, iterations=1) # 4 . 축소 erode
        # blur = cv2.GaussianBlur(frame,(1,1),0)  # http://bskyvision.com/24
        # blia = cv2.bilateralFilter(frame,100,1,1)  # http://bskyvision.com/24

        cnts,contours,hierarchy = cv2.findContours(img_np, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img_np = cv2.drawContours(origin, contours, -1, (0, 255, 0), 1)

        cv2.imshow("origin",img_np)
        key = cv2.waitKey(1)
        if key == 27:
            break

    for j in range(len(contours)):
        cnt = contours[j]
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        rect_area = w * h  # area size
        aspect_ratio = float(w) / h  # ratio = width/height
        if (aspect_ratio >= 0.2) and (aspect_ratio <= 1.0) and (rect_area >= 100) and (rect_area <= 700):
            cv2.rectangle(img_np, (x, y), (x + w, y + h), (0, 255, 0), 1)
            box1.append(cv2.boundingRect(cnt))

    cv2.imshow("frame", img_np)
    cv2.imwrite("result.jpg",img_np)
    result = pytesseract.image_to_string(Image.open("result.jpg"),lang='eng')
    print(result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def find_circles(img,cimg):
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=25, minRadius=1, maxRadius=10)
    """
        image – 8-bit single-channel image. grayscale image.
        method – 검출 방법. 현재는 HOUGH_GRADIENT가 있음.
        dp – dp=1이면 Input Image와 동일한 해상도.
        minDist – 검출한 원의 중심과의 최소거리. 값이 작으면 원이 아닌 것들도 검출이 되고, 너무 크면 원을 놓칠 수 있음.
        param1 – 내부적으로 사용하는 canny edge 검출기에 전달되는 Paramter
        param2 – 이 값이 작을 수록 오류가 높아짐. 크면 검출률이 낮아짐.
        minRadius – 원의 최소 반지름.
        maxRadius – 원의 최대 반지름.
    """
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.imshow('img', cimg)

read_screen()

