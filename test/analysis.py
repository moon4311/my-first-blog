import numpy as np
import connector
from itertools import combinations

conn = connector.Connector()


def result_rate(dic):
    result = {"P": 0, "B": 0, "T": 0}
    if dic:
        cnt_total = sum(dic.values())
        for char in dic:
            result.__setitem__(char, dic.get(char))
            if dic.get(char) > 0:
                result[char+"%"] = round(dic.get(char) / cnt_total * 100)
            else:
                result[char+"%"] = 0
    return result


def result_by_number(p_cnt, b_cnt):
    """
    :param : result Table 의 ex 값과 현재 p,b 값
    :return: {'P': 0, 'B': 100, 'T': 0}
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


def result_by_number_v2(p_cnt, b_cnt):
    result = {"P": 0, "B": 0, "T": 0}
    rows = conn.select_latest()
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


def result_by_number_v3(p_cnt, b_cnt, last):
    result = {"P": 0, "B": 0, "T": 0}
    rows = conn.select_latest()
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


def result_by_sequence(seq):  # 해당 sequence 에서 뭐가 나오는지
    result = {"P": 0, "B": 0, "T": 0}
    rows = conn.select_latest()
    for row in rows:
        char = row[0][seq]
        result.__setitem__(char, result.get(char)+1)
    return result_rate(result)


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
    result = {"P": 0, "B": 0, "T": 0}
    rows = conn.select_latest()
    for char in result:
        for row in rows:
            st = row[0]
            result.__setitem__(char, result.get(char) + st.count(pattern + char))
    return result_rate(result)


def cut_pattern(cnt):
    rows = conn.select_latest()
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
    rows = conn.select_latest()
    dic, result = {}, {}
    for row in combinations(rows, 2):
        t1, t2 = row[0][0], row[1][0]
        for a in range(6, 7):  # 글자수
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


b_val, p_val = 6, 7
patt = "PPPPP"
ro = 0
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
# ro = result_by_sequence(28+27+2)
# print("seq : ", ro)
# find_pattern()