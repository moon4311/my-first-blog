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
    str=""
    for fname in glob.glob('train/B2*.jpg'):
        img_np = cv2.imread(fname)
        img_np = cv2.pyrUp(img_np)                          # 이미지 가로x2 세로x2
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        img_np = cv2.filter2D(img_np, -1, kernel)
        save = img_np[6:25, 9:26]
        cv2.imwrite("train/temp6.jpg", save)
        result = pytesseract.image_to_string(Image.open("train/temp6.jpg"), lang="eng", config='--psm 10')
        str = str+result
    print(str)


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
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = set_image((x, y, w, h))

    w2, h2 = 17, 17
    for i in range(0, 10):
        x2 = w2 * i
        for j in range(0, 6):
            y2 = h2 * j
            fname = "train/" + name + "_" + str(g_id)+"_" + str(seq) + ".jpg"

            ## 원래 방식
            crop_img = img[y2:y2 + w2, x2:x2 + h2]  # 한칸 크기로 줄임
            img_np = cv2.cvtColor(cv2.filter2D(cv2.pyrUp(crop_img), -1, kernel), cv2.COLOR_BGR2GRAY)  # Gray 화
            save = 255 - img_np[6: 25, 9:26]
            # cv2.imshow("fF", save)
            # k = cv2.waitKey(0)
            # if k == 27:
            #     break
            # result = ""
            cv2.imwrite(fname, save)
            # cv2.imwrite(fname, cv2.filter2D(cv2.pyrUp(img[y2+3: y2 + h2 - 4, x2+4: x2 + w2 - 4]), -1, kernel))
            result = pytesseract.image_to_string(Image.open(fname), lang="eng", config='--psm 10')
            if (result == "7") | (result == "1") | (result ==""):
                result = "T"
            result = str(result.upper())
            if (result != "P") & (result != "B") & (result != "T"):
                print(name + " " + str(seq) + "번" + result)
                return
            else:
                latest = latest + result
                if result == "P":
                    p = p+1
                elif result =="B":
                    b = b+1
                elif result == "T":
                    t = t+1
                row = {"g_id": g_id, "sequence": seq, "result": result, "latest": latest,
                       "ex_p": ex_p, "ex_b": ex_b, "P": p, "B": b, "T": t}
                conn.insert("result", row)
                ex_p, ex_b = p, b
                seq = seq + 1