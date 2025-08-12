from cube_solve import CubeSolver
from tool import window_capture
from methods.CNN import train_cnn_main
#from methods.stacking import train_stacking_main
import cv2 as cv
from methods.use_model import use_cnn, model_cnn, model_cnn_2
import threading
import numpy as np
from time import time, sleep
import json

color_dict = {
	"U": '6',
	"B": '2',
	"L": '5',
	"F": '3',
	"D": '4',
	"R": '1'
}

out_win = 'test'
cv.namedWindow(out_win, cv.WINDOW_NORMAL)
cv.resizeWindow(out_win,900,500)
area = (5,5)
coordinate = {
		'U': [[1291, 591, 0], [1291, 761, 0], [1291, 917, 0],
				[1200, 625, 0], [1200, 761, 0], [1200, 900, 0],
				[1147, 641, 0], [1135, 753, 0], [1135, 869, 0]],#

		'B': [[1400, 920, 0], [1400, 760, 0], [1400, 600, 0],
				[1483, 885, 0], [1483, 765, 0], [1483, 637, 0],
				[1523, 865, 0], [1523, 775, 0], [1525, 670, 0]],#

		'L': [[1557, 139, 0], [1577, 275, 0], [1577, 425, 0],
				[1379, 139, 0], [1379, 275, 0], [1377, 425, 0],
				[1277, 139, 0], [1277, 275, 0], [1277, 425, 0]],#

		'F': [[415, 355, 1], [415, 273, 1], [415, 200, 1],
				[445, 367, 1], [445, 273, 1], [445, 183, 1],
				[505, 397, 1], [505, 283, 1], [505, 153, 1]],#

		'D': [[600, 400, 0], [593, 279, 0], [591, 145, 0],
				[673, 395, 0], [673, 281, 0], [675, 175, 0],
				[729, 367, 0], [729, 277, 0], [725, 183, 0]],#

		'R': [[387, 583, 0], [517, 583, 0], [675, 583, 0],
				[387, 750, 0], [517, 750, 0], [675, 750, 0],
				[387, 890, 0], [517, 890, 0], [675, 890, 0]]#
}

class Cube:
	def __init__(self, train, test, serialPort="COM9", baudRate=115200, timegap=1, msp=100, mtp=70):
		self.solver = CubeSolver(serialPort=serialPort, baudRate=baudRate, timegap=timegap, msp=msp, mtp=mtp)
		self.train_order = train
		self.test_order = test
		self.kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))


	def run(self):
		self.solver.SerialWrite('c')
		#sleep(2)
		if self.train_order:
			self.train_cube()
		elif self.test_order:		
			self.test()
		else:
			self.solve()

	def test_color(self):
		res_dict = dict()
		full_img = window_capture()
		full_img = full_img.copy()

		names = coordinate.keys()
		for name in names:
			res_str = ''
			for point in coordinate[name]:
				y1 = point[1]-area[1]
				y2 = point[1]+area[1]
				x1 = point[0]-area[0]
				x2 = point[0]+area[0]

				img = full_img[point[1]-area[1]:point[1]+area[1], point[0]-area[0]:point[0]+area[0], :]
				img = cv.resize(img, (50, 50))
				img = cv.resize(img, (28, 28))
				img = np.expand_dims(img, axis=0)
				if point[2]:
					color_index = use_cnn(img, model_cnn_2)
				else:
					color_index = use_cnn(img, model_cnn)
				res = str(color_index)
				points = [[x1,y1],[x1,y2],[x2,y2],[x2,y1]]
				points = np.array(points, dtype=np.int32)

				if res == '1':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(0, 0, 255), thickness=3)
				
				elif res == '2':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(0, 255, 0), thickness=3)
				
				elif res == '3':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(255, 0, 0), thickness=3)
					
				elif res == '4':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(255, 255, 255), thickness=3)
					
				elif res == '5':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(0, 0, 0), thickness=3)
				
				elif res == '6':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(100, 214, 255), thickness=3)

				res_str = res_str + res 
			res_dict[name] = res_str

		return res_dict, full_img	

	def solve(self):
		color_ex, img = self.test_color()
		cv.imshow(out_win, img)
		cv.waitKey(10)
		run = self.solver.run(color_ex)
		while not run:
			color_ex, img = self.test_color()
			cv.imshow(out_win, img)
			cv.waitKey(10)
			run = self.solver.run(color_ex)
		self.solver.close()
	'''
	def get_color(self):
		full_img = window_capture()
		result = dict()
		names = coordinate.keys()

		for name in names:
			res = ''
			for point in coordinate[name]:
				img = full_img[point[1]-area[1]:point[1]+area[1], point[0]-area[0]:point[0]+area[0], :]
				img = cv.resize(img, (50, 50))
				#img = cv.erode(img, kernel=self.kernel, iterations=2)
				img = cv.resize(img, (28,28))
				# img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
				img = np.expand_dims(img, axis=0)
				if point[2]:
					color_index = use_cnn(img, model_cnn_2)	
				else:
					color_index = use_cnn(img, model_cnn)
				res = res + str(color_index)
			result[name] = res
		return result,full_img.copy()
	'''

	def train_cube(self):
		self.solver.SerialWrite('c')
		sleep(3)

		def lz(color_dict=color_dict):
			self.solver.SerialWrite('lz')
			D = color_dict.get('D')
			color_dict['D'] = color_dict['L']
			color_dict['L'] = color_dict['U']
			color_dict['U'] = color_dict['R']
			color_dict['R'] = D

		def rz(color_dict=color_dict):
			self.solver.SerialWrite('rz')
			R = color_dict['R']
			color_dict['R'] = color_dict['B']
			color_dict['B'] = color_dict['L']
			color_dict['L'] = color_dict['F']
			color_dict['F'] = R 

		print('收集图像中')

		kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
		def collection(kernel,i):
			full_img = window_capture()
			names = coordinate.keys()
			for name in names:
				for n in range(9):
					point = coordinate[name][n]
					img = full_img[point[1]-area[1]:point[1]+area[1], point[0]-area[0]:point[0]+area[0], :]
					img = cv.resize(img, (50, 50))
					#img = cv.erode(img, kernel=kernel, iterations=1)
					if point[2]:
						path = './datasets3/'+color_dict[name]+'/'+'__{l}___{m}__'.format(l=i, m=n)+str(time())[:-8]+'.jpg'
						cv.imwrite(path, img)
					else:
						path = './datasets2/'+color_dict[name]+'/'+'__{l}___{m}__'.format(l=i, m=n)+str(time())[:-8]+'.jpg'
						cv.imwrite(path, img)						

		for i in range(3):
			lz()
			rz()
			collection(kernel,i)

		rz()
		lz()
		lz()


		for i in range(3,6):
			lz()
			rz()
			collection(kernel,i)		

		self.solver.SerialWrite('o')
		self.solver.close()
		'''
		print('图象收集完成\n开始训练神经网络')

		train_cnn_main()
		
		print('神经网络训练完成\n开始训练集成模型')

		train_stacking_main()

		print('训练完成')
		'''

	def test(self):
		self.solver.SerialWrite('c')
		sleep(5)
		full_img_ = window_capture()
		cv.imwrite('testt.jpg',full_img_)
		self.solver.SerialWrite('o')
		names = coordinate.keys()
		full_img = cv.imread('testt.jpg')
		for name in names:
			for point in coordinate[name]:
				y1 = point[1]-area[1]
				y2 = point[1]+area[1]
				x1 = point[0]-area[0]
				x2 = point[0]+area[0]

				img = full_img_[point[1]-area[1]:point[1]+area[1], point[0]-area[0]:point[0]+area[0], :]
				img = cv.resize(img, (28, 28))
				img = img / 255.0
				img = np.expand_dims(img, axis=0)
				color_index = use_cnn(img, model_cnn)
				res = str(color_index)
				print(res)
				points = [[x1,y1],[x1,y2],[x2,y1],[x2,y2]]
				points = np.array(points, dtype=np.int32)

				if res == '1':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(22, 1, 120), thickness=3)
				
				elif res == '2':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(109, 34, 2), thickness=3)
				
				elif res == '3':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(117, 230, 9), thickness=3)
					
				elif res == '4':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(255, 255, 255), thickness=3)
					
				elif res == '5':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(58, 5, 255), thickness=3)
				
				elif res == '6':
					cv.polylines(full_img, [points.reshape((-1, 1, 2))], True, color=(215, 90, 196), thickness=3)
					


		cv.imwrite('test_res.jpg', full_img)