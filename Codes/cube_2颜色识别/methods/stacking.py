from methods.getdata import data_for_stacking,data_split
from msvcrt import getch
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier,StackingClassifier
from sklearn.metrics import accuracy_score
import joblib
from time import time

import numpy as np 


def stacking_model():
	lr = LogisticRegression(dual=False,random_state=0,n_jobs=-1)
	svc = SVC(kernel='rbf',random_state=0,gamma=0.20)
	dectree = DecisionTreeClassifier(criterion='gini',max_depth=4,random_state=0)
	knc = KNeighborsClassifier(n_jobs=-1)
	gpc = GaussianProcessClassifier(n_jobs=-1)
	abc = AdaBoostClassifier(learning_rate=.5,random_state=0)

	estimators = [
		('lr', lr),
		('svc',svc),
		('dectree',dectree),
		('knc',knc),
		('gpc',gpc),
		('abc',abc)]
	sc = StackingClassifier(estimators=estimators,final_estimator=RandomForestClassifier(),n_jobs=-1)
	return sc

def train_stacking():

	train, test = data_split(full_list=data_for_stacking, ratio=0.8)
	X_train = []
	Y_train = []
	X_test = []
	Y_test = []

	for i in range(len(train)):
		X_train.append(train[i][0])
		Y_train.append(train[i][1])

	for i in range(len(test)):
		X_test.append(test[i][0])
		Y_test.append(test[i][1])

	sc = stacking_model()

	sc.fit(X_train, list(np.array(Y_train).ravel()))

	joblib.dump(sc,'./models/StackingClassifier.pkl')

	Y_pre = joblib.load('./models/StackingClassifier.pkl').predict(X_test)
	score = accuracy_score(Y_test, Y_pre)
	print('预测和实际相比：')
	print(score)


def train_stacking_full():

	X_train = []
	Y_train = []

	for i in range(len(data_for_stacking)):
		X_train.append(data_for_stacking[i][0])
		Y_train.append(data_for_stacking[i][1])

	sc = stacking_model()
	
	sc.fit(X_train, list(np.array(Y_train).ravel()))

	path = './models/StackingClassifier_fin_{time}.pkl'.format(time=str(time())[:-8])
	joblib.dump(sc, path)

	return path

def train_stacking_main():

	train_stacking()

	print('训练完成，表现良好时按下回车使用完整数据集训练')

	Input = getch()
	if Input == b'\r':
		model_path = train_stacking_full()
		with open('./models/stacking_model.txt', 'w') as file:
			file.write(model_path)