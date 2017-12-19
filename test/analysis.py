import numpy as np
import connector


conn = connector.Connector()


############## UTIL ##############


def result_rate(dic):
    result = {"P": 0, "B": 0, "T": 0}
    if dic:
        cnt_total = sum(dic.values())
        for char in dic:
            result.__setitem__(char, dic.get(char))
            result[char+"rate"] = round(dic.get(char) / cnt_total * 100)
    return result


############## UTIL ##############


def result_by_number(p_cnt, b_cnt):
    """
    :param : result Table 의 ex 값과 현재 p,b 값
    :return: {'P': 0, 'B': 100, 'T': 0}
    ver_1  : 확률 리턴
    ver_2  : 확률 및 답
    """
    # rows = conn.select_all("result", {"ex_p": p_val, "ex_b": b_val})
    query = "SELECT result, count(*) FROM result " \
            + " WHERE ex_p = '" + str(p_cnt) + "' " \
            + " AND ex_b = '" + str(b_cnt) + "' " \
            + " group by result "
    return result_rate(conn.select(query, {}))


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


def result_by_sequence(seq): # 해당 sequence 에서 뭐가 나오는지
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


ro = result_by_number(0, 1)
print("num : ", ro)
ro = result_by_number_v2(0, 1)
print("num : ", ro)
ro = result_by_pattern("BPBPB")
print("v1 : ", ro)
ro = result_by_pattern_v2("BPBPB")
print("v2 : ", ro)
ro = result_by_sequence(18)
print("seq : ", ro)


def search_Frequency():
    """
    가장 자주 나오는 패턴 검색
    :return:
    """
    pass


# result_by_number(0, 1) # 현재 값 읽어서 하는 방향으로
# result_by_latest("B")  # 현재 값 읽어서 하는 방향으로

