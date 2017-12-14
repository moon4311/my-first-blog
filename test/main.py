import connector
import time
import cv2
import datetime
from mobile_collect import *
from PIL import (Image, ImageGrab)
import pyautogui as gui
from matplotlib import pyplot as plt


conn = connector.Connector()

# print(check_status())

data = {"g_id": "TEST",
        "sequence":	2,
        "result": "T",
        "ex_p": 0,
        "ex_b": 0,
        "p": 1,
        "b": 0,
        "t": 1}
# conn.insert("result",data)
g_id = conn.select_limit("result", {}, column=["g_id"])[0][0]

while True:
# while False:
        Id = check_status()
        if Id.find("기") > 0:
                g_id = int(g_id) + 1
                time.sleep(20)
                continue

        if Id.find("완료") > 0:
                # if False :
                last = conn.select_limit("result", {"g_id": g_id})
                if len(last) == 0:      # 시작일 경우 데이터가 조회가 안된다
                        ll = [g_id, 0, 0, 0, 0, 0, 0]
                else:
                        ll = list(last[0])
                print("last : ", last)
                data.__setitem__("g_id", g_id)
                data.__setitem__("sequence", ll[1] + 1)
                data.__setitem__("ex_p",ll[5])
                data.__setitem__("ex_b",ll[6])
                time.sleep(3)

                # xywh = ((142, 350, 180, 398), (580, 350, 620, 398))
                xywh = ((150, 560, 180, 595), (570, 560, 600, 595))
                filename = ("images/p_result.jpg", "images/b_result.jpg")
                save_number(xywh, filename)
                arr = read_number(filename)
                if arr[0] > arr[1]:  # P
                        data.__setitem__("result", "P")
                        data.__setitem__("p", ll[5] + 1)
                elif arr[0] < arr[1]: # B
                        data.__setitem__("result", "B")
                        data.__setitem__("b", ll[6] + 1)
                else:
                        data.__setitem__("result", "T")
                        data.__setitem__("t",ll[7] + 1)
                print("data : ", data)
                conn.insert("result",data)
                time.sleep(5)

# ex_data = conn.select_all("result", {"RowId": "max(RowId"})
# print(ex_data)  GC00517C140FU
##### g_id가 같은 가장 최근 데이터 조회 해서 b p 수정 해서 인서트
##### -> 처음일 경우  b,p 넣어서 인서트


# a.insert("result", data)
# a.select_all("tes")
