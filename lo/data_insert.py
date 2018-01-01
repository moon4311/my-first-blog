import connector
from itertools import combinations

conn = connector.Connector()

aa = range(1,46)
for num in combinations(aa, 6):

    conn.insert("origin",str(list(num)))

print("finish")