import numpy as np
import cv2
from matplotlib import pyplot as plt

#->라이브러리 생성
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

#얼굴과 눈 검출을 위한 haarcascade 파일 읽기, CascadeClassifier 객체 생성
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#haarcascade 파일은 다운받아야 한다. (원하는 목록, eye, nose, face, body...)
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

img = cv2.imread('test1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#test1.jpg의 이미지를 불러들이고, 이미지를 흑백으로 바꿔준다
#이미지를 처리하는데에는 색깔이 필요없기 때문.
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

#얼굴의 스케일을 조정한다.
#괄호안의 숫자를 바꾸면서 얼굴의 크기에따라 얼굴과 눈을 검출한다.
#괄호안의 숫자가 커질수록 작은 얼굴 감지할수있음
faces = face_cascade.detectMultiScale(gray, 1.9, 2)

"""
    cv2.CascadeClassifier.detectMultiScale(image[, scaleFactor[, minNeighbors[,
                                           flags[, minSize[, maxSize]]]]]) → objects
    image 실제 이미지
    objects [반환값] 얼굴 검출 위치와 영역 변수
    scaleFactor 이미지 스케일
    minNeighbors 얼굴 검출 후보들의 갯수
    flags 이전 cascade와 동일하다 cvHaarDetectObjects 함수 에서
          새로운 cascade에서는 사용하지 않는다.
    minSize 가능한 최소 객체 사이즈
    maxSize 가능한 최대 객체 사이즈
"""
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

for (x,y,w,h) in faces:
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) # (R,G,B)의 명도
	roi_gray = gray[y:y+h, x:x+w]
	roi_color = img[y:y+h, x:x+w]
"""	
	roi = region of interest
    cv2.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]]) → None
    img 적용할 이미지
    pt1 그릴 상자의 꼭지점
    pt2 pt1의 반대편 꼭지점
    color 상자의 색상
    thickness 상자의 라인들의 두께 음수 또는 CV_FILLED를 주면 상자를 채운다.
    lineType 라인의 모양 line()함수 확인하기
    shift ?? Number of fractional bits in the point coordinates.
    포인트 좌표의 분수 비트의 수??
"""
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#imshow를 통해 이미지를 출력한다., waitKey()에서 k는 꼭 대문자로 써야함.
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ