import db_connector
# import mobile_collect
from mobile_collect import *

import numpy as np
import cv2
from PIL import (Image, ImageGrab)
import pyautogui as gui
from matplotlib import pyplot as plt


######   KNNN 으로 숫자 학습 했으니   KNN import  해서  숫자 판독 하면 된다.!!

conn = db_connector.Connector()
# me = mobile_collect
# me = mobile_collect

print(check_status())
# while me.check_status() :
#         xywh = ((142, 350, 180, 398), (580, 350, 620, 398))
#         filename = ("images/p_result.jpg", "images/b_result.jpg")
        # me.save_number(xywh, filename)
        # arr = me.read_number(filename)

ex_data = conn.select_all("result", {"RowId": "max(RowId"})
print(ex_data)
##### g_id가 같은 가장 최근 데이터 조회 해서 b p 수정 해서 인서트
##### -> 처음일 경우  b,p 넣어서 인서트

data = {"g_id": "TEST",
        "sequence":	2,
        "result": "T",
        "ex_p": 0,
        "ex_b": 0,
        "p": 1,
        "b": 0,
        "t": 1}

# a.insert("result", data)
# a.select_all("tes")ㅏ
