import db_connector
import mobile_collect

import numpy as np
import cv2
from PIL import (Image, ImageGrab)
import pyautogui as gui
from matplotlib import pyplot as plt


######   KNNN 으로 숫자 학습 했으니   KNN import  해서  숫자 판독 하면 된다.!!

a = db_connector.Connector()
me = mobile_collect

print(me)


row = a.select_all("result", {"RowId": 2})
print(row)
data = {"g_id": "TEST",
        "sequence":	2,
        "result": "T",
        "ex_p": 0,
        "ex_b": 0,
        "p": 1,
        "b": 0,
        "t": 1}

# a.insert("result", data)
# a.select_all("tes")
