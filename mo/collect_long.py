import time
import connector
from collect_mobile import *

conn = connector.Connector()

data = {"g_id": "TEST", "sequence":	1,    "result": "T",
        "ex_p": 0,    "ex_b": 0,
        "p": 1,       "b": 0,
        "t": 1, "latest": ""}
# conn.insert("result",data)
g_id = conn.select_limit("result", {}, column=["g_id"])[0][0]
g_id = int(g_id) + 1

xywh = ((150, 555, 190, 600), (570, 555, 610, 600))   # 40 x 40  STR
filename = ("images/p_result.jpg", "images/b_result.jpg")
xywh2 = ((154, 655, 174, 680), (203, 655, 223, 680),(252, 655, 272, 680))   # result Int
filename2 = ("images/b_cnt.jpg", "images/p_cnt.jpg", "images/t_cnt.jpg")

# g_id = 2
while True :
        # while False :
        Id = check_status()
        if Id.find("기") > 0:
                g_id = int(g_id) + 1
                time.sleep(10)
                continue

        if Id.find("완료") > 0:
                time.sleep(3)
                # 조회
                pb = save_number(xywh, filename)
                rst_str = "P" if (pb[0] > pb[1]) else "B" if (pb[0] < pb[1]) else "T"
                time.sleep(2)
                rst_int = read_result(xywh2, filename2)
                last = conn.select_limit("result", {"g_id": g_id})

                # 가공
                if last:
                        ll = list(last[0])
                else:   # 시작일 경우 데이터가 조회가 안된다
                        ll = [g_id, 0, 0, 0, 0, 0, 0, 0, 0, " "]

                try:
                        seq = int(rst_int[0]) + int(rst_int[1]) + int(rst_int[2])
                except Exception as e:
                        seq = ll[1]+1

                # 대입
                data.__setitem__("g_id", g_id)
                data.__setitem__("sequence", seq)  ## 원 개수 파악해서 넣는 방향으로
                data.__setitem__("result", rst_str)
                data.__setitem__("ex_p", ll[5])
                data.__setitem__("ex_b", ll[6])
                data.__setitem__("b", rst_int[0]) # B
                data.__setitem__("p", rst_int[1]) # P
                data.__setitem__("t", rst_int[2]) # T
                data.__setitem__("latest", ll[9]+rst_str)
                if rst_str == "P":
                        data.__setitem__("p", ll[5] + 1)
                elif rst_str == "B":
                        data.__setitem__("b", ll[6] + 1)
                if rst_str == "T":
                        data.__setitem__("t", ll[7] + 1)

                # if pb[0] > pb[1]:  # P
                #         data.__setitem__("result", "P")
                # elif pb[0] < pb[1]:  # B
                #         data.__setitem__("result", "B")
                # else:
                #         data.__setitem__("result", "T")

                print("data : ", data)
                conn.insert("result", data)
                time.sleep(15)

# ex_data = conn.select_all("result", {"RowId": "max(RowId"})
# print(ex_data)  GC00517C140FU
##### g_id가 같은 가장 최근 데이터 조회 해서 b p 수정 해서 인서트
##### -> 처음일 경우  b,p 넣어서 인서트


# a.insert("result", data)
# a.select_all("tes")
