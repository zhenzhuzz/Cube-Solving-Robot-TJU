from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
from methods.getdata import data_for_cnn, data_split
import numpy as np
import tensorflow
from time import time 
from msvcrt import getch
import os

gpus = tensorflow.config.experimental.list_physical_devices('GPU')
if gpus:
	try:
		for gpu in gpus:
			tensorflow.config.experimental.set_memory_growth(gpu, True)

	except RuntimeError as e:
		print(e)

def cnn():
	model = Sequential()
	model.add(Conv2D(32, kernel_size=(5, 5), strides=(1, 1),
				 activation='relu',
				 input_shape=(28,28,3)))
	model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
	model.add(Dropout(0.25))
	model.add(Conv2D(64, (5, 5), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	model.add(Flatten())
	model.add(Dense(1000, activation='relu'))
	model.add(Dense(6, activation='softmax'))

	model.compile(loss=tensorflow.keras.losses.categorical_crossentropy,
			  optimizer=tensorflow.keras.optimizers.Adam(),
			  metrics=['accuracy'])
	return model


def train_cnn():

	data = []
	X_train = []
	X_test = []
	Y_train = []
	Y_test = []

	for key in list(data_for_cnn.keys()):
		key_ = np.array(key)
		for i in range(len(data_for_cnn[key])):
			data.append((data_for_cnn[key][i], key_))


	train, test = data_split(full_list=data, ratio=0.8)


	for i in range(len(train)):
		X_train.append(train[i][0])
		Y_train.append(train[i][1])
	  
	for i in range(len(test)):
		X_test.append(test[i][0])
		Y_test.append(test[i][1])


	X_train = tensorflow.stack(X_train)
	Y_train = tensorflow.stack(Y_train)
	X_test = tensorflow.stack(X_test)
	Y_test = tensorflow.stack(Y_test)

	model = cnn()

	model.fit(X_train,Y_train,
		  batch_size=128,
		  epochs=100,
		  verbose=1,
		  validation_data=(X_test, Y_test))

	model.save('./models/cnn.h5')

	score = model.evaluate(X_test, Y_test, verbose=0)
	print('Test loss:', score[0])
	print('Test accuracy:', score[1])

def train_cnn_full():

	data = []
	X_train = []
	Y_train = []

	for key in list(data_for_cnn.keys()):
		key_ = np.array(key)
		for i in range(len(data_for_cnn[key])):
			data.append((data_for_cnn[key][i], key_))

	for i in range(len(data)):
		X_train.append(data[i][0])
		Y_train.append(data[i][1])

	X_train = tensorflow.stack(X_train)
	Y_train = tensorflow.stack(Y_train)

	model = cnn()
	callback = EarlyStopping(monitor='accuracy', patience=100, restore_best_weights=True, mode='auto')
	osdir = os.path.join('logs7')
	tbCallBack = TensorBoard(log_dir=osdir,  # log 目录
                 histogram_freq=0,  # 按照何等频率（epoch）来计算直方图，0为不计算
#                  batch_size=32,     # 用多大量的数据计算直方图
                 write_graph=True,  # 是否存储网络结构图
                 write_grads=True, # 是否可视化梯度直方图
                 write_images=True,# 是否可视化参数
                 embeddings_freq=0, 
                 embeddings_layer_names=None, 
                 embeddings_metadata=None)

	model.fit(X_train,Y_train,
		  batch_size=128,
		  epochs=500,
		  verbose=1,
		  callbacks=[tbCallBack,callback])
	path = './models/cnn_fin_{time}.h5'.format(time=str(time())[:-8])
	model.save(path)
	return path



def train_cnn_main():

	train_cnn()

	print('训练完成，表现良好时按下回车使用完整数据集训练')

	Input = getch()
	if Input == b'\r':
		model_path = train_cnn_full()
		with open('./models/cnn_model.txt', 'w') as file:
			file.write(model_path)

if __name__ == '__main__':
	train_cnn_main()