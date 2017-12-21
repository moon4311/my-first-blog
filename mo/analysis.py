import numpy as np
import connector
from itertools import combinations

conn = connector.Connector()


# A type : All data
# B type : latest data

def result_rate(dic):
    result = dic.copy()
    cnt_total = sum(dic.values())
    for char in dic:
        if dic.get(char) > 0:
            result[char+"%"] = round(dic.get(char) / cnt_total * 100)
        else:
            result[char+"%"] = 0
    return result


def result_by_number(p_cnt, b_cnt):  # A type
    """
    :param : result Table 의 ex 값과 현재 p,b 값
    """
    # rows = conn.select_all("result", {"ex_p": p_val, "ex_b": b_val})
    query = "SELECT result, count(*) FROM result " \
            + " WHERE ex_p = '" + str(p_cnt) + "' " \
            + " AND ex_b = '" + str(b_cnt) + "' " \
            + " group by result "
    result = {"P": 0, "B": 0, "T": 0}
    rows = conn.select(query, {})
    for row in rows:
        result.__setitem__(row[0], row[1])
    return result_rate(result)


def result_by_number_v2(p_cnt, b_cnt): # B type
    rows, result = conn.select_latest()
    for row in rows:
        for a in range(p_cnt+b_cnt, len(row[0])):
            st = row[0][:a]
            if st.count("P") > p_cnt | st.count("B") > b_cnt:
                break
            elif (st.count("P") == p_cnt) & (st.count("B") == b_cnt):
                d = row[0][a:a + 1]
                result.__setitem__(d, result.get(d)+1)
                break
    return result_rate(result)


def result_by_number_v3(p_cnt, b_cnt, last):  # B type
    rows, result = conn.select_latest()
    for row in rows:
        for a in range(p_cnt+b_cnt, len(row[0])):
            st = row[0][:a]
            if st.count("P") > p_cnt | st.count("B") > b_cnt:
                break
            elif (st.count("P") == p_cnt) & (st.count("B") == b_cnt) & (st[-1] == last):
                d = row[0][a:a + 1]
                result.__setitem__(d, result.get(d)+1)
                break
    return result_rate(result)


# def result_by_sequence(seq):  # 해당 sequence 에서 뭐가 나오는지
#     rows, result = conn.select_latest()
#     for row in rows:
#         char = row[0][seq]
#         result.__setitem__(char, result.get(char)+1)
#     return result_rate(result)


def result_by_pattern(pattern):
    """
    사용법 :   result_by_latest("BPBP") 이후 나올 확률 반환
    :param pattern:   대문자 원하는 수량 만큼
    :return:
    """
    length = pattern.__len__()
    query = "SELECT result, count(*) FROM result " \
            + " WHERE substr(latest,length(latest)-" + str(length) \
            + ", " + str(length) + ") = '" + pattern + "' " \
            + " group by result "
    result = {"P": 0, "B": 0, "T": 0}
    rows = conn.select(query, {})
    for row in rows:
        result.__setitem__(row[0], row[1])
    return result_rate(result)


def result_by_pattern_v2(pattern):
    """
    :param pattern:
    :return:
    """
    rows, result = conn.select_latest()
    for char in result:
        for row in rows:
            st = row[0]
            result.__setitem__(char, result.get(char) + st.count(pattern + char))
    return result_rate(result)


def cut_pattern(cnt):
    rows, result = conn.select_latest()
    arr = []
    tu = {}
    for row in rows:
        # arr2 = []
        length = len(row[0])
        latest = str(row[0])
        for s in range(0, length, cnt):
            pattern = latest[s: s + cnt]
            if len(pattern) == cnt:
                # arr2.append(pattern)
                arr.append(pattern)
    for ar in arr:
        if tu.__contains__(ar):     tu.__setitem__(ar, tu.get(ar)+1)
        else:        tu[ar] = 1
    return tu


def find_pattern():
    rows, result = conn.select_latest()
    dic, result = {}, {}
    for row in combinations(rows, 2):
        t1, t2 = row[0][0], row[1][0]
        for a in range(5, 6):  # 글자수
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
        if dic.get(a) > 100:
            result[a] = dic.get(a)
    print(result)


def synchro_rate():
    rows, result = conn.select_latest()
    setss = set()
    for row in combinations(rows, 2):
        score = 0
        t1, t2 = row[0][0], row[1][0]
        lt1, lt2 = len(t1), len(t2)
        if lt1 > lt2:
            cnt = lt2
        else:
            cnt = lt1
        for a in range(cnt):
            if t1[a] == t2[a]:
                score = score + 1
        setss.add((score, t1, t2))
        print(score, t1, t2)

    for a in setss:
        pass

b_val, p_val = 7, 9
patt = "B"
ro = result_by_number(p_val, b_val)
print("num : ", ro)
ro = result_by_number_v2(p_val, b_val)
print("num2 : ", ro)
ro = result_by_number_v3(p_val, b_val, patt[-1])
print("num3 : ", ro)
ro = result_by_pattern(patt)
print("pat1 : ", ro)
ro = result_by_pattern_v2(patt)
print("pat2 : ", ro)
find_pattern()
# synchro_rate()