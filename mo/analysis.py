import numpy as np
import connector
from itertools import combinations
import cv2

conn = connector.Connector()
# A type : All data
# B type : latest data
rows_1p = ""

def result_rate(dic):
    result = dic.copy()
    cnt_total = sum(dic.values())
    for char in dic:
        if dic.get(char) > 0:
            result[char+"%"] = round(dic.get(char) / cnt_total * 100)
        else:
            result[char+"%"] = 0
    return result


def rows_to_result(rows):
    result = {}
    for row in rows:
        result[row[0]] = row[1]
    return result


def result_by_seq(seq):  # 해당 sequence
    query = "SELECT result, count(*)  FROM result WHERE  sequence = " + str(seq) + " GROUP BY result"
    return result_rate(rows_to_result(conn.select(query)))


def result_by_number(r_bp):  # A type
    """ :param : result Table 의 ex 값과 현재 p,b 값   """
    b_cnt = str(r_bp[0])
    p_cnt = str(r_bp[1])
    query = "SELECT result, count(*) FROM result WHERE ex_p = '" + p_cnt + "' " \
            + " AND ex_b = '" + b_cnt + "' GROUP BY result ORDER BY result"
    return result_rate(rows_to_result(conn.select(query)))


def result_by_number_v2(r_bp, last=""):  # B type
    b_cnt = int(r_bp[0])
    p_cnt = int(r_bp[1])
    rows = conn.select_latest()
    result = {"B": 0, "P": 0, "T": 0}
    for row in rows:
        for a in range(p_cnt+b_cnt, len(row[0])):
            st = row[0][:a]
            if st.count("P") > p_cnt | st.count("B") > b_cnt:
                break
            elif (st.count("P") == p_cnt) & (st.count("B") == b_cnt):
                if ((last != "") & (st[-1] == last)) | (last == ""):
                    d = row[0][a]
                    result.__setitem__(d, result.get(d) + 1)
                    break
    return result_rate(result)


def drow_table():
    rows, result = conn.select_latest()
    arr = np.full((45, 45, 3), 0)
    for row in rows:
        x, y, cnt = 0, 0, 0
        latest = row[0]
        for char in latest:
            if char == "P":
                x = x + 1
            elif char == "B":
                y = y + 1
            # elif char == "T":
            #     continue
            arr[x][y] = arr[x][y] + 1
    arr = 255 - np.array(arr*2)
    b, g, r = cv2.split(arr)
    img_np = cv2.merge([r, g, b])
    cv2.imwrite("test.jpg", img_np)


def result_by_pattern(pattern):
    """
    사용법 :   result_by_latest("BPBP") 이후 나올 확률 반환
    """
    length = pattern.__len__()
    query = "SELECT result, count(*) FROM result " \
            + " WHERE substr(latest,length(latest)-" + str(length) \
            + ", " + str(length) + ") = '" + pattern + "' " \
            + " group by result "
    rows = conn.select(query)
    return result_rate(rows_to_result(rows))


def result_by_pattern_v2(pattern):
    rows = conn.select_latest()
    result = {"B": 0, "P": 0, "T": 0}
    for char in result:
        for row in rows:
            st = row[0]
            result.__setitem__(char, result.get(char) + st.count(pattern + char))
    return result_rate(result)


def cut_pattern(cnt):
    rows = conn.select_latest()
    arr = []
    result = {}
    for row in rows:
        length = len(row[0])
        latest = str(row[0]).replace("T","")
        # latest = str(row[0])
        for s in range(0, length, cnt):
            pattern = latest[s: s + cnt]
            if len(pattern) == cnt:
                arr.append(pattern)
    for ar in arr:
        if result.__contains__(ar):
            result.__setitem__(ar, result.get(ar)+1)
        else:
            result[ar] = 1
    print(result)
    return result


def find_pattern():
    rows = conn.select_latest()
    dic, result = {}, {}
    for row in combinations(rows, 2):
        # t1, t2 = row[0][0], row[1][0]
        t1, t2 = row[0][0].strip("T"), row[1][0].strip("T")
        for a in range(18, 19):  # 글자수
            for b in range(len(t1) - a):  # A의 위치
                str_a = t1[b:a + b]
                for c in range(len(t2) - a):  # B의 위치
                    str_b = t2[c:a + c]
                    if str_a == str_b:
                        if dic.__contains__(str_a):
                            dic.__setitem__(str_a, dic.get(str_a) + 1)
                        else:
                            dic[str_a] = 1
    for a in dic: #일정 개수 이상인 경우 선별
        if dic.get(a) > 1:
            result[a] = dic.get(a)
    print(result)


def synchro_rate():
    rows = conn.select_latest()
    setss = set()
    for row in combinations(rows, 2):
        score = 0
        # t1, t2 = row[0][0], row[1][0]
        t1, t2 = row[0][0].strip("T"), row[1][0].strip("T")
        lt1, lt2 = len(t1), len(t2)
        if lt1 > lt2:
            cnt = lt2
        else:
            cnt = lt1
        for a in range(cnt):
            if t1[a] == t2[a]:
                score = score + 1
        setss.add((score, t1, t2))
        if score > 32:  # 32개 이상 같은거
            print(score, row)