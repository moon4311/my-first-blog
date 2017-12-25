import numpy as np
import cv2
import glob
import pytesseract
import connector
from PIL import (Image, ImageGrab)

width, height = 579, 171

B1 = [790, 228]
B2 = [B1[0] - width, B1[1] + height]
B3 = [B1[0], B2[1]]
B4 = [B2[0], B2[1] + height]
B5 = [B1[0], B4[1]]
B6 = [B2[0], B4[1] + height]
B7 = [B1[0], B6[1]]
# B1_x, B1_y = 790, 228    # B1
# B2_x, B2_y = B1_x - x_width, B1_y + y_width  # B2
# B3_x, B3_y = B1_x, B2_y   # B3
# B4_x, B4_y = B2_x, B2_y + y_width  # B4
# B5_x, B5_y = B1_x, B4_y   # B5
# B6_x, B6_y = B2_x, B5_y + y_width  # B6
# B7_x, B7_y = B1_x, B6_y  # B7


def set_image(bbox):
    img = ImageGrab.grab(bbox=bbox)
    img_np = np.array(img)
    b, g, r = cv2.split(img_np)
    return cv2.merge([r, g, b])


def image_read_test():
    strr=""
    for fname in glob.glob('train/B4*.jpg'):
        # img_np = cv2.imread(fname)
        # img_np = cv2.pyrUp(img_np)                          # 이미지 가로x2 세로x2
        # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # img_np = cv2.filter2D(img_np, -1, kernel)
        # save = img_np[6:25, 9:26]
        # cv2.imwrite("train/temp6.jpg", save)
        result = pytesseract.image_to_string(Image.open(fname), lang="eng", config='--psm 10')
        print(fname, ":", result)
        strr = strr+result
    # print(strr)


def image_read_set(name, x1, y1, lang="eng"):
    # 1.전처리 - 화면 크기 선택

    w = x1 + 170
    h = y1 + 103
    w2, h2 = 17, 17
    result = ""
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img_np = set_image((x1, y1, w, h))
    result = ""
    for a in range(0, 10):
        x2 = w2 * a
        for b in range(0, 6):
            y2 = h2 * b
            fname = "train/" + name + str(a) + str(b) + ".jpg"

            ## 원래 방식
            # crop_img = img_np[y2:y2 + h2, x2:x2 + w2] # 한칸 크기로 줄임
            # img_np = cv2.pyrUp(crop_img)  # 이미지 가로x2 세로x2
            # img_np = cv2.filter2D(img_np, -1, kernel)
            # save = img_np[6:25, 9:26]

            #간소화 방식 1
            crop_img = img_np[y2+3 : y2 + h2 - 4, x2+4 : x2 + w2 - 4] # 한칸 크기로 줄임
            img_np = cv2.pyrUp(crop_img)  # 이미지 가로x2 세로x2
            save = cv2.filter2D(img_np, -1, kernel)

            #간소화 방식 2
            save = cv2.filter2D(cv2.pyrUp(img_np[y2 + 3: y2 + h2 - 4, x2 + 4: x2 + w2 - 4]), -1, kernel)

            cv2.imwrite(fname, save)
            char = pytesseract.image_to_string(Image.open(fname), lang="eng", config='--psm 10')
            result = result + char
        # key = cv2.waitKey(1)
        # if key == 27:
        #     break
    # cv2.waitKey(0)  # 3초마다 확인
    # cv2.destroyAllWindows()
    return result


def image_read_after_insert(name, xy):  ## ********
    """
    :param name:  "B1" ~ "B7"
    :param xy:   B1 ~ B7
    :return:
    """
    conn = connector.Connector()
    x, y = xy
    w, h = x + 170, y + 103
    g_id = int(conn.select_limit("result", {}, column=["g_id"], order_by="g_id desc")[0][0]) + 1
    seq, ex_p, ex_b, p, b, t = 1, 0, 0, 0, 0, 0
    latest = ""
    img = set_image((x, y, w, h))
    data = []
    w2, h2 = 17, 17
    for i in range(0, 10):
        x2 = w2 * i
        for j in range(0, 6):
            y2 = h2 * j
            result = ""
            # c, g, r = img[y2+10:y2 + 11, x2+3:x2 + 4][0][0]  # 한칸 크기로 줄임
            c, g, r = img[y2 + 8:y2 + 9, x2 + 3:x2 + 4][0][0]  # 한칸 크기로 줄임
            print(r, g, c)
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
            print(row)
            data.append(row)
            ex_p, ex_b = p, b
            seq = seq + 1
    conn.insert_v2("result", data)














def image_read_after_insert_detail():  ## ********
    """
    :param name:  "B1" ~ "B7"
    :return:
    """
    conn = connector.Connector()
    g_id = int(conn.select_limit("result", {}, column=["g_id"], order_by="g_id desc")[0][0]) + 1
    seq, ex_p, ex_b, p, b, t = 1, 0, 0, 0, 0, 0
    latest = ""
    data = []
    img = set_image((107, 747, 327, 877))

    w2, h2 = 22, 22
    for i in range(0, 10):
        x2 = w2 * i
        for j in range(0, 6):
            y2 = h2 * j
            result = ""
            c, g, r = img[y2+10:y2 + 11, x2+3:x2 + 4][0][0]  # 한칸 크기로 줄임
            print(r, g, c)
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
            print(row)
            data.append(row)
            ex_p, ex_b = p, b
            seq = seq + 1
    conn.insert_v2("result", data)
