# https://habr.com/ru/post/357666/
import numpy as np

# k = d * G
d = np.array([1, 0, 1, 0])
print("Cyclical code for:", d)

G = np.matrix([[1, 0, 1, 1, 0, 0, 0],
               [0, 1, 0, 1, 1, 0, 0],
               [0, 0, 1, 0, 1, 1, 0],
               [0, 0, 0, 1, 0, 1, 1]])

k = d * G
for index, el in enumerate(k):
    k[index] = el % 2

print(k)

H = np.matrix([[1, 0, 1],
               [1, 1, 1],
               [1, 1, 0],
               [0, 1, 1],
               [1, 0, 0],
               [0, 1, 0],
               [0, 0, 1]])

s = k * H

for index, el in enumerate(s):
    s[index] = el % 2

print("Syndrome for correct message  :", s)

k = np.matrix([[1, 0, 0, 1, 1, 1, 1]])

s = k * H

for index, el in enumerate(s):
    s[index] = el % 2

print("Syndrome for incorrect message:", s)

