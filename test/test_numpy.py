import numpy as np

a = np.zeros((100, 100))
print(a)
# 출력:
# [[ 0.  0.]
#  [ 0.  0.]]

a = np.ones((2, 3))
print(a)
# 출력:
# [[ 1.  1.  1.]
#  [ 1.  1.  1.]]

a = np.full((2, 3), 5)
print(a)
# 출력:
# [[5 5 5]
#  [5 5 5]]

a = np.eye(3)
print(a)
# 출력:
# [[ 1.  0.  0.]
#  [ 0.  1.  0.]
#  [ 0.  0.  1.]]

a = np.array(range(20)).reshape((4, 5))
print(a)
# 출력:
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]]


lst = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
arr = np.array(lst)

# 슬라이스
a = arr[0:2, 0:2]
print(a)
# 출력:
# [[1 2]
#  [4 5]]

a = arr[1:, 1:]
print(a)
# 출력:
# [[5 6]
#  [8 9]]


lst = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]
a = np.array(lst)

# 정수 인덱싱
s = a[[0, 2], [1, 3]]

print(s)
# 출력
# [2 12]

lst1 = [ [ [1, 2, 3], [4, 5, 6] ],  [ [7, 8, 9], [10,11,12] ],
         [ [13,14,15],[16,17,18] ], [ [19,20,21],[22,23,24] ] ]

a1 = np.array(lst1)

s1 = a1[[0,0],[1,1]]
print("-------------------------------------")
print(s1)
a2 = np.array(s1)
print(a2)
s2 = a2[[0,1],[0,1]]
print(s2)


lst1 = [
    [1, 1],
    [1, 1]
]

lst2 = [
    [1, 2],
    [3, 4]
]
a = np.array(lst1)
b = np.array(lst2)

c = np.dot(a, b)
print("출력 _ ")
print(c)
# 출력:
# [[19 22]
#  [43 50]]