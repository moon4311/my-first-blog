import numpy as np
import cv2
import pyautogui as gui
import pytesseract
from PIL import (Image, ImageGrab)
from matplotlib import pyplot as plt


def image_read(img_file,x1,y1,x2,y2,lang="eng+kor") :

    # 1.전처리 - 화면 크기 선택
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img_np = np.array(img)
    # 2.전처리 - 원본 색깔로 변경
    b,g,r = cv2.split(img_np)
    img_np = cv2.merge([r,g,b])
    # 3.전처리 - 크기 2배로 조정
    img_np = cv2.pyrUp(img_np)
    img_np = 255 - img_np
    # 4.전처리 - 선명하게
    kernel = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
    img_np = cv2.filter2D(img_np, -1, kernel)

    # 5. Gray 화 >  2진화
    img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)   # Gray 화
    # img_np = cv2.Canny(img_np,200,200)                     # 2진화

    cv2.imwrite(img_file, img_np)
    result = pytesseract.image_to_string(Image.open(img_file),lang)
    cv2.waitKey(3)  # 3초마다 확인
    cv2.destroyAllWindows()
    return result
    # if(result.find())
    # return result


# 1. 스크린 인식

#  Finish!  1
def check_status():
    result = "Please"
    while result.find("Stop") != 0 :
        result = image_read("status.jpg",120, 150, 200, 170)
        if result.find("Stop")+1 :   # status Stop
            print("read_result Start")
            get_result()

def get_result():
    result= image_read("7.jpg",60,300,650,400) # PDF TEST
    # result= image_read("7.jpg",720,620,810,750,lang="kor") # 내부 결과
    list = result.split(" ")
    print(len(list))
    print(result)
    # 1 숫자기준    2 패턴기준    # 최근 x개의 패턴
    # set   회차2     R   exOdd   Odd    exEven  Even   Tie          
    # 00001  1~      O|E    0~    0~       0~     0~    0~


def temp22222() :
    box1 = []
    img_np = ""
    kernel = np.ones((2, 2), np.uint8)
    while(True):
        img = ImageGrab.grab(bbox=(100, 600, 820, 900))
        img_np = np.array(img)
        b,g,r = cv2.split(img_np)
        img_np = cv2.merge([r,g,b])
        img_np = cv2.pyrUp(img_np)                          # 이미지 가로x2 세로x2
        # img_np = cv2.pyrUp(img_np)                          # 이미지 가로x2 세로x2
        origin = img_np

        img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)   # Gray 화
        img_np = cv2.Canny(img_np,50,50)                     # 2진화
        img_np = 255 - img_np
        # cv2.imshow("frame",img_np)
        # cv2.imwrite("7.jpg", img_np)


        # img_np = cv2.dilate(img_np,kernel, iterations=1)    # 확장 dilate
        # img_np = cv2.resize(invert,(1000,400),interpolation=cv2.INTER_CUBIC)  ## 크기 확대
        # img_np = cv2.pyrDown(img_np)                      # 이미지 가로x1/2 세로x1/2
        # img_np = 255 - img_np                             # 색반전
        # img_np = cv2.erode(img_np,kernel, iterations=1) # 4 . 축소 erode
        # blur = cv2.GaussianBlur(frame,(1,1),0)  # http://bskyvision.com/24
        # blia = cv2.bilateralFilter(frame,100,1,1)  # http://bskyvision.com/24

        cv2.imshow("frame", img_np)
        cv2.imwrite("7.jpg", img_np)
        im = Image.open("7.jpg")
        result = pytesseract.image_to_string(im)
        result = str(result).replace(" ","")
        if result.find("Stop")+1 :  # stop 일 때
            print("Stop : ",result.find("Stop"))
        else :
            print("PLEASE")
        # cnts,contours,hierarchy = cv2.findContours(img_np, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # img_np = cv2.drawContours(origin, contours, -1, (0, 255, 0), 1)
        # cv2.imshow("origin",img_np)


        key = cv2.waitKey(1)
        if key == 27:
            break

    # for j in range(len(contours)):
    #     cnt = contours[j]
    #     area = cv2.contourArea(cnt)
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     rect_area = w * h  # area size
    #     aspect_ratio = float(w) / h  # ratio = width/height
    #     if (aspect_ratio >= 0.2) and (aspect_ratio <= 1.0) and (rect_area >= 100) and (rect_area <= 700):
    #         cv2.rectangle(img_np, (x, y), (x + w, y + h), (0, 255, 0), 1)
    #         box1.append(cv2.boundingRect(cnt))

    # cv2.imshow("frame", img_np)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # im = Image.open("7.jpg")
    # result = pytesseract.image_to_string(im)
    # print(result)




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

# check_status()

get_result()