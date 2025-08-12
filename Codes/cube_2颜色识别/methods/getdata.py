# using coding:utf-8 
import os
from tensorflow.keras.preprocessing import image
from numpy import argmax
import numpy as np
import cv2 as cv
import random

def data_split(full_list, ratio, shuffle=True):
    n_total = len(full_list)
    offset = int(n_total * ratio)
    if n_total == 0 or offset < 1:
        return [], full_list
    if shuffle:
        random.shuffle(full_list)
    list_train = full_list[:offset]
    list_test = full_list[offset:]
    return list_train, list_test


def get_data_for_cnn():
    res = dict()
    i = 0
    for color_set in os.listdir('./datasets2'):
        try:
            pic_names = os.listdir('./datasets2/'+color_set)
            Y = [0]*6
            Y[i] = 1
            X = []
            for pic in pic_names:
                path = './datasets2/'+color_set+'/'+pic
                # print(path)
                img = cv.imread(path)
                img = cv.resize(img, (28, 28))
                #img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
                # img = img / 255.0
                X.append(list(img))
            res[tuple(Y)] = X
            i = i + 1
        except NotADirectoryError:
            pass
    return res 


data_for_cnn = get_data_for_cnn()

def get_data_for_cnn_2():
    res = dict()
    i = 0
    for color_set in os.listdir('./datasets3'):
        try:
            pic_names = os.listdir('./datasets3/'+color_set)
            Y = [0]*6
            Y[i] = 1
            X = []
            for pic in pic_names:
                path = './datasets3/'+color_set+'/'+pic
                # print(path)
                img = cv.imread(path)
                img = cv.resize(img, (28, 28))
                #img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
                # img = img / 255.0
                X.append(list(img))
            res[tuple(Y)] = X
            i = i + 1
        except NotADirectoryError:
            pass
    return res 


data_for_cnn_2 = get_data_for_cnn_2()

'''
def get_data_for_stacking():
    res = list()
    for color_set in os.listdir('./datasets'):
        try:
            pic_names = os.listdir('./datasets/'+color_set)
            label = [int(color_set)]
            for pic in pic_names:
                path = './datasets/'+color_set+'/'+pic
                img = cv.imread(path)
                img = cv.resize(img, (28, 28))
                img = img / 255.0
                R,G,B = (0,0,0)
                for i in range(28):
                    for j in range(28):
                        R = R + img[i][j][0]
                        G = G + img[i][j][1]
                        B = B + img[i][j][2]
                R_mean = R/(28*28)
                G_mean = G/(28*28)
                B_mean = B/(28*28)

                res_pic = ([R_mean,G_mean,B_mean],label)
                res.append(res_pic)
        except NotADirectoryError:
            pass
    return res 

data_for_stacking = get_data_for_stacking()

'''