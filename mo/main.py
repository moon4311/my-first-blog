import collect_short as co
import analysis as an


cnt = -7

rst = co.result_get()
patt = co.one_set_get()[-1].get("latest")[cnt:]
print(rst, patt)
a = an.result_by_number(rst)
print(a)
a = an.result_by_number_v2(rst)
print(a)
a = an.result_by_number_v2(rst, patt[-1])
print(a)
b = an.result_by_pattern(patt)
print(b)