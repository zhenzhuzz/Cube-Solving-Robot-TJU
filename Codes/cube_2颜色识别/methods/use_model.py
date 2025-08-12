#import joblib
from tensorflow.keras.models import load_model
from numpy import argmax
'''
with open('./models/stacking_model.txt', 'r') as file:
	stacking_path = file.read()
'''
with open('./models/cnn_model.txt', 'r') as file:
	cnn_path = file.read()

model_cnn = load_model(cnn_path)

with open('./models/cnn_model_2.txt', 'r') as file:
	cnn_path_2 = file.read()

model_cnn_2 = load_model(cnn_path_2)
#model_stacking = joblib.load(stacking_path)

def use_cnn(data, model):
	pre_result = model.predict(data)
	return argmax(pre_result)+1
'''
def use_stacking(data, model):
	data.shape = (28,28,3)
	data = data / 255.0
	R,G,B = (0,0,0)
	for i in range(28):
		for j in range(28):
			R = R + data[i][j][0]
			G = G + data[i][j][1]
			B = B + data[i][j][2]
	R_mean = R/(28*28)
	G_mean = G/(28*28)
	B_mean = B/(28*28)
	data = [[R_mean,G_mean,B_mean]]
	pre_result = model.predict(data)
	return pre_result[0]+1
'''