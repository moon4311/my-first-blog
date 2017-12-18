import numpy as np
import connector


def result_rate(rows):
    cnt_total = 0
    result = {"P": 0, "B": 0, "T": 0}
    result2 = result.copy()
    if rows:
        # 개수 파악
        for row in rows:
            result.__setitem__(row[0], row[1])
            cnt_total = cnt_total + row[1]
        # percent 추가
        result2 = result.copy()
        for key in result:
            result2[key+"rate"] = round(result.get(key) / cnt_total * 100)
    # return result
    return result2


def result_by_number(p_val, b_val):
    """
    :param : result Table 의 ex 값과 현재 p,b 값
    :return: {'P': 0, 'B': 100, 'T': 0}
    ver_1  : 확률 리턴
    ver_2  : 확률 및 답
    """
    # rows = conn.select_all("result", {"ex_p": p_val, "ex_b": b_val})
    conn = connector.Connector()
    query = "SELECT result, count(*) FROM result " \
            + " WHERE ex_p = '" + str(p_val) + "' " \
            + " AND ex_b = '" + str(b_val) + "' " \
            + " group by result "
    return result_rate(conn.select(query, {}))


def result_by_latest(latest):
    """
    사용법 :   result_by_latest("BPBP") 이후 나올 확률 반환
    :param latest:   대문자 원하는 수량 만큼
    :return:
    """
    conn = connector.Connector()
    length = latest.__len__()
    query = "SELECT result, count(*) FROM result "\
            + " WHERE substr(latest,length(latest)-" + str(length) \
            + ", " + str(length) + ") = '" + latest + "' " \
            + " group by result "
    return result_rate(conn.select(query, {}))


def search_Frequency():
    """
    가장 자주 나오는 패턴 검색
    :return:
    """
    pass


# result_by_number(0, 1) # 현재 값 읽어서 하는 방향으로
# result_by_latest("B")  # 현재 값 읽어서 하는 방향으로

