import cv2 as cv

import numpy as np

raw = np.zeros((100,100,3))

path = './datasets/'
colorset = list()


red = np.zeros((100,100,3))
for i in range(100):
	for n in range(100):
		red[i][n][2] = 255
colorset.append(red)

yellow = np.zeros((100,100,3))
for i in range(100):
	for n in range(100):
		yellow[i][n][1] = 255
colorset.append(yellow)

blue = np.zeros((100,100,3))
for i in range(100):
	for n in range(100):
		blue[i][n][0] = 255
	for n in range(100):
		blue[i][n][1] = 180
	for n in range(100):
		blue[i][n][2] = 15
colorset.append(blue)

write = np.zeros((100,100,3))
for i in range(100):
	for n in range(100):
		write[i][n][0] = 100
for i in range(100):
	for n in range(100):
		write[i][n][1] = 100
for i in range(100):
	for n in range(100):
		write[i][n][2] = 84
colorset.append(write)

c1 = np.zeros((100,100,3))
for i in range(100):
	for n in range(100):
		c1[i][n][0] = 96
for i in range(100):
	for n in range(100):
		c1[i][n][1] = 132
for i in range(100):
	for n in range(100):
		c1[i][n][2] = 255
colorset.append(c1)

c2 = np.zeros((100,100,3))
for i in range(100):
	for n in range(100):
		c2[i][n][0] = 100
for i in range(100):
	for n in range(100):
		c2[i][n][1] = 214
for i in range(100):
	for n in range(100):
		c2[i][n][2] = 255
colorset.append(c2)

i = 1
for color in colorset:
	for n in range(108):
		path = './datasets/{l}/{m}.jpg'.format(l=str(i),m=str(n))
		cv.imwrite(path, color)
	i = i+1



