import numpy as np
import cv2
import glob
import pytesseract
import connector
from PIL import (Image, ImageGrab)

width, height = 579, 171
w, h = 170, 103
A = (107, 747, 327, 877)
B1 = (790, 228, 790+w, 228+h)  # PC
# B1 = (790, 83, 790+w, 83+h) # NOTE
B2 = (B1[0] - width, B1[1] + height, B1[2] - width, B1[3] + height)
B3 = (B1[0], B2[1], B1[2], B2[3])
B4 = (B2[0], B2[1] + height, B2[2], B2[3] + height)
B5 = (B1[0], B4[1], B1[2], B4[3])
B6 = (B2[0], B4[1] + height, B2[2], B4[3] + height)
B7 = (B1[0], B6[1], B1[2], B6[3])



def many_set_get(page):
    if page == "AGQ":
        arr = (B1, B2, B3, B4, B5, B6, B7)
        # arr = (B1, B2, B5, B6, B7)
    else:
        arr = (B1, B2, B3, B4, B5)

    g_id = [[x, 1, 1] for x in range(len(arr))]  # gid, switch, len
    min = 3  # 최소 저장 개수
    while True:
        cnt = 0
        print(g_id)
        for g_set in arr:
            data = one_set_get(g_set)
            if len(data) < min:  # 새로 시작한 시점
                g_id[cnt][1] = 1
            elif g_id[cnt][1]:  # 새로 시작한 후
                g_id[cnt][0] = data[0].get("g_id")
                g_id[cnt][1] = one_set_insert(data, min)  # 인서트 후 0으로 변경
                g_id[cnt][2] = len(data)
            elif (g_id[cnt][1] == 0) & (len(data) > g_id[cnt][2]):
                data[-1].__setitem__("g_id", g_id[cnt][0])
                one_circle_insert(data[-1])
                g_id[cnt][2] = len(data)
            # elif (g_id[cnt][1] == 0 ) & (g_id[cnt][2] >= 54):
            #     data[-1].__setitem__("g_id", g_id[cnt][0])
            #     data[-1].__setitem__("sequence", g_id[cnt][2])
            #     latest 값 , p값 ,b값
            cnt = cnt + 1


def image_get(xywh=A):  ## ********
    """
    :param xywh:  A ,  B1 ~ B7
    :return:
    """
    while True:
        img = set_image(xywh)
        cv2.imshow("gramce",img)
        k = cv2.waitKey(10)
    data = []


def result_get(cnt=6):
    bp = [(770,745,800,762), (770,762,800,779)]
    r_bp = []
    for bbox in bp:
        img = cv2.pyrUp(cv2.cvtColor(set_image(bbox), cv2.COLOR_BGR2GRAY))
        img = cv2.GaussianBlur(img, (3, 3), 0)  # http://bskyvision.com/24
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        img = cv2.filter2D(img, -1, kernel)
        cv2.imwrite("result.jpg",img)
        r_bp.append(pytesseract.image_to_string(Image.open("result.jpg"), config="--psm 10"))
    return r_bp


def set_image(bbox):
    b, g, r = cv2.split(np.array(ImageGrab.grab(bbox=bbox)))
    return cv2.merge([r, g, b])

def one_set_get(xywh=A):  ## ********
    """
    :param xywh:  A ,  B1 ~ B7
    :return:
    """
    conn = connector.Connector()
    g_id = int(conn.select_limit("result", {}, column=["g_id"], order_by="g_id desc")[0][0]) + 1
    seq, ex_p, ex_b, p, b, t = 1, 0, 0, 0, 0, 0
    latest = ""
    img = set_image(xywh)
    data = []
    if xywh == A:
        w2, h2 = 22, 22
    else:
        w2, h2 = 17, 17

    for i in range(0, 10):
        x2 = w2 * i
        for j in range(0, 6):
            y2 = h2 * j
            result = ""
            c, g, r = img[y2 + 9:y2 + 10, x2 + 3:x2 + 4][0][0]  # 한칸 크기로 줄임
            if (r > 100) & (g > 100):
                break
            elif (g > r) & (g > c):
                result = "T"
                t = t + 1
            elif c > r:
                result = "P"
                p = p + 1
            elif r > c:
                result = "B"
                b = b + 1
            latest = latest + result
            row = {"g_id": g_id, "sequence": seq, "result": result, "latest": latest,
                   "ex_p": ex_p, "ex_b": ex_b, "P": p, "B": b, "T": t}
            # print(row)
            data.append(row)
            ex_p, ex_b = p, b
            seq = seq + 1
    return data


def one_set_insert(data, cnt): # 여러개 값
    conn = connector.Connector()
    switch = 1
    if len(data) > int(cnt):
        conn.insert("result", data)
        switch = 0
    return switch


def one_circle_insert(data):  # 한개 값
    conn = connector.Connector()
    conn.insert("result", data)

