import numpy as np
import cv2
import glob
import pytesseract
import connector
from PIL import (Image, ImageGrab)

width, height = 579, 171
w, h = 170, 103
A = (107, 747, 327, 877)
B1 = (790, 228, 790+w, 228+h)
B2 = (B1[0] - width, B1[1] + height, B1[2] - width, B1[3] + height)
B3 = (B1[0], B2[1], B1[2], B2[3])
B4 = (B2[0], B2[1] + height, B2[2], B2[3] + height)
B5 = (B1[0], B4[1], B1[2], B4[3])
B6 = (B2[0], B4[1] + height, B2[2], B4[3] + height)
B7 = (B1[0], B6[1], B1[2], B6[3])


def set_image(bbox):
    img = ImageGrab.grab(bbox=bbox)
    img_np = np.array(img)
    b, g, r = cv2.split(img_np)
    return cv2.merge([r, g, b])


def many_set_get(page):
    if page == "AGIN":
        arr = (B1, B2, B3, B4, B5, B6, B7)
    else:
        arr = (B1, B2, B3, B4, B5, B6)

    g_id = [[x, 1, 1] for x in range(len(arr))] # gid, switch, len
    min = 80  # 최소 저장 개수
    while True:
        cnt = 0
        for g_set in arr:
            data = one_set_get(g_set)
            g_id[cnt][0] = data[0].get("g_id")
            g_id[cnt][2] = len(data)
            print(g_id)
            if len(data) < 6:  # 새로 시작한 시점
                g_id[cnt] = 1

            if g_id[cnt][1]:  # 새로 시작한 후
                g_id[cnt][1] = one_set_insert(data, min)  # 인서트 후 0으로 변경
                cnt = cnt + 1


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
            # c, g, r = img[y2 + 8:y2 + 9, x2 + 3:x2 + 4][0][0]  # 한칸 크기로 줄임
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


def one_set_insert(data, cnt):
    conn = connector.Connector()
    switch = 1
    if len(data) > int(cnt):
        conn.insert("result", data)
        switch = 0
    return switch


many_set_get("AGIN")

# def image_read_set(name, x1, y1, lang="eng"):
#     # 1.전처리 - 화면 크기 선택
#     w = super.w + x1
#     h = super.h + y1
#     w2, h2 = 17, 17
#     kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
#     img_np = set_image((x1, y1, w, h))
#     result = ""
#     for a in range(0, 10):
#         x2 = w2 * a
#         for b in range(0, 6):
#             y2 = h2 * b
#             fname = "train/" + name + str(a) + str(b) + ".jpg"
#
#             #간소화 방식 1
#             crop_img = img_np[y2+3 : y2 + h2 - 4, x2+4 : x2 + w2 - 4] # 한칸 크기로 줄임
#             img_np = cv2.pyrUp(crop_img)  # 이미지 가로x2 세로x2
#             save = cv2.filter2D(img_np, -1, kernel)
#
#             #간소화 방식 2
#             save = cv2.filter2D(cv2.pyrUp(img_np[y2 + 3: y2 + h2 - 4, x2 + 4: x2 + w2 - 4]), -1, kernel)
#             cv2.imwrite(fname, save)
#             char = pytesseract.image_to_string(Image.open(fname), lang="eng", config='--psm 10')
#             result = result + char
#     # cv2.waitKey(0)  # 3초마다 확인
#     # cv2.destroyAllWindows()
#     return result

#
# def image_read_after_insert_detail():  ## ********
#     """
#     :param name:  "B1" ~ "B7"
#     :return:
#     """
#     conn = connector.Connector()
#     g_id = int(conn.select_limit("result", {}, column=["g_id"], order_by="g_id desc")[0][0]) + 1
#     seq, ex_p, ex_b, p, b, t = 1, 0, 0, 0, 0, 0
#     latest = ""
#     data = []
#     img = set_image((107, 747, 327, 877))
#
#     w2, h2 = 22, 22
#     for i in range(0, 10):
#         x2 = w2 * i
#         for j in range(0, 6):
#             y2 = h2 * j
#             result = ""
#             c, g, r = img[y2+10:y2 + 11, x2+3:x2 + 4][0][0]  # 한칸 크기로 줄임
#             if (r > 100) & (g > 100):
#                 break
#             elif (g > r) & (g > c):
#                 result = "T"
#                 t = t + 1
#             elif c > r:
#                 result = "P"
#                 p = p + 1
#             elif r > c:
#                 result = "B"
#                 b = b + 1
#             latest = latest + result
#             row = {"g_id": g_id, "sequence": seq, "result": result, "latest": latest,
#                    "ex_p": ex_p, "ex_b": ex_b, "P": p, "B": b, "T": t}
#             print(row)
#             data.append(row)
#             ex_p, ex_b = p, b
#             seq = seq + 1
#     conn.insert("result", data)
