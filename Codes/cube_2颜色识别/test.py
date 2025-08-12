
from methods.CNN import train_cnn_main as train_1
train_1()

#from methods.CNN_2 import train_cnn_main as train_2
#train_2()

'''
from methods.CNN_2 import train_cnn_main as train_2

train_2()
'''
'''
import cv2 as cv
bgr = []

red_1 = cv.imread('red_1.jpg')
red_1_bgr = cv.resize(red_1,(50,50))
bgr.append(red_1_bgr)
red_2 = cv.imread('red_3.jpg')
red_2_bgr = cv.resize(red_2,(50,50))
bgr.append(red_2_bgr)

orange_1 = cv.imread('orange_1.jpg')
orange_1_bgr = cv.resize(orange_1,(50,50))
bgr.append(orange_1_bgr)
orange_2 = cv.imread('orange_3.jpg')
orange_2_bgr = cv.resize(orange_2,(50,50))
bgr.append(orange_2_bgr)

print("BGR:")
k = 0
print('red:')
for pic_bgr in bgr:
	if k == 2:
		print('orange:')
	B,G,R = (0,0,0)
	for i in range(50):
		for n in range(50):
			B = B + pic_bgr[i][n][0]
			G = G + pic_bgr[i][n][1]
			R = R + pic_bgr[i][n][2]
	B_mean = B/2500
	G_mean = G/2500
	R_mean = R/2500
	k = k+1

	print((B_mean, G_mean, R_mean))

hsv = []

red_1_hsv = cv.cvtColor(red_1_bgr, cv.COLOR_BGR2HSV)
hsv.append(red_1_hsv)
red_2_hsv = cv.cvtColor(red_2_bgr, cv.COLOR_BGR2HSV)
hsv.append(red_2_hsv)
orange_1_hsv = cv.cvtColor(orange_1_bgr, cv.COLOR_BGR2HSV)
hsv.append(orange_1_hsv)
orange_2_hsv = cv.cvtColor(orange_2_bgr, cv.COLOR_BGR2HSV)
hsv.append(orange_2_hsv)

print("HSV:")
print('red:')
k = 0
for pic_hsv in hsv:
	if k == 2:
		print('orange:')
	H,S,V = (0,0,0)
	for i in range(50):
		for n in range(50):
			H = H + pic_hsv[i][n][0]
			S = S + pic_hsv[i][n][1]
			V = V + pic_hsv[i][n][2]
	H_mean = H/2500
	S_mean = S/2500
	V_mean = V/2500
	k = k+1
	print((H_mean, S_mean, V_mean))
	'''
