import numpy as np
import connector




def result_by_number(p_val,b_val):
    """
    :param : result Table 의 ex 값과 현재 p,b 값
    :return:
    ver_1  : 확률 출력
    ver_2  : 확률 및 답
    """
    conn = connector.Connector()
    # rows = conn.select_limit("result", {"ex_p":p_val,"ex_b": b_val})
    rows = "g"*28
    cnt_p = 10
    cnt_b = 15

    # for row in rows:
    #     result = row[2]
    #     if result == "P":
    #         cnt_p = cnt_p + 1
    #     elif result == "B":
    #         cnt_b = cnt_b + 1

    rate = "[P:" + str(cnt_p) + "/" \
           + str(round(cnt_p/len(rows)*100))+"%]" \
           + "[B:" + str(cnt_b)+"/" \
           + str(round(cnt_b/len(rows)*100)) + "%]"
    print(rate)


def result_by_a():
    connector.select_limit()



result_by_number(0,0)