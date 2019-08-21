'''

This script is used to obtain the result of 
'CSP+LDA CSP+QDA FBCSP+LDA FBCSP+QDA'
from 'MI_2', 'MI_4', 'plo' dataset

THREE INPUT ARGS:
'dataset, FLAG_F, FLAG_C = sys.argv[1:]'
where,
'dataset': 'MI_2', 'MI_4' or 'plo'
'FLAG_F' : 'CSP' or 'FBCSP'
'FLAG_C' : 'LDA' or 'QDA'

SAVE FILE:
the BEST_N_COMPONENTS, ACC, CONFUSION_MATRIX will be save into .npz file.

'''

from __future__ import print_function

import sklearn
import sys
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.feature_selection import mutual_info_classif
from sklearn import preprocessing

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import os
import pickle
import numpy as np
import time
from mne.decoding import CSP
from scipy.signal import butter, lfilter, decimate
import scipy.io as sio
from os.path import exists
import csv
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import mutual_info_score

from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import multiprocessing as multi
import itertools
from functools import reduce

np.random.seed(33)


def butter_bandpass(lowcut, highcut, fs=200, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs=200, order=5):
    '''
    The filter is applied to each subarray along one axis, Default is -1
    '''
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = []
    for temp in data:
        y.append(lfilter(b, a, temp))
    return np.array(y)

def select_channel(data):
    '''
    select 32 from the original 68 channels
    '''
    ind = [8, 10, 12, 16, 17, 18, 19, 20, 21, 22, 
                25, 26, 27, 28,29, 30, 31,
                35, 36, 37, 38, 39, 40, 41,
                46, 48, 50,
                55, 56, 57,
                61, 63]
    ind = [e-1 for e in ind]
    data = data[:, ind, :]
    return data


class CSP_classifier():
    def __init__(self):
        return None

    def csp_unit_fit(self, n_components, train_x, train_y):
        '''
        input: n_components, train_x, train_y
        inner_save: csp_model
        output: csp_feature
        '''
        label = set(train_y)
        # the combination between labels
        comb_list = list(itertools.combinations(label, 2))
        self.csp_model = []

        for (class_1, class_2) in comb_list:
            ind_1_train = np.where(train_y == class_1)
            ind_2_train = np.where(train_y == class_2)
            ind_train = np.concatenate((ind_1_train[0], ind_2_train[0]))
            csp = CSP(n_components=n_components, reg=None,
                      log=True, norm_trace=False)
            csp.fit(train_x[ind_train], train_y[ind_train])
            self.csp_model.append(csp)
            del csp

    def csp_unit_transform(self, data):
        temp_data = []
        for csp in self.csp_model:
            temp_data.append(csp.transform(data))

        # concatenate features of different pairs of categories
        data_csp = reduce(lambda x, y: np.concatenate(
            (x, y), axis=1), temp_data)

        return data_csp

    def cross_validation_unit(self, data, label, confuMatrix=False):
        nList = list(range(1, 11))
        cList = [2**(-5), 2**(-4), 2**(-3), 2**(-2), 2**(-1)]
        cList = cList + list(range(1, 21))

        n_splits = 5
        accRecord = np.zeros((n_splits, len(nList), len(cList)))

        sf = StratifiedKFold(n_splits=n_splits, shuffle=True)
        ind_list = [x for x in sf.split(data, label)]

        for fold, (train_ind, test_ind) in enumerate(ind_list):
            train_x, train_y = data[train_ind], label[train_ind]
            test_x, test_y = data[test_ind], label[test_ind]
            for i, n_components in enumerate(nList):
                self.csp_unit_fit(n_components, train_x, train_y)
                train_x_csp = self.csp_unit_transform(train_x)
                test_x_csp = self.csp_unit_transform(test_x)

                for j, c in enumerate(cList):
                    pipe_lr = Pipeline([
                        ('sc', StandardScaler()),
                        # ('pca', PCA(n_components=new_nc)),
                        # ('clf', GridSearchCV(svr, parameters))
                        ('clf', SVC(C=c, gamma='auto'))
                    ])
                    pipe_lr.fit(train_x_csp, train_y.flatten())
                    result = pipe_lr.predict(test_x_csp)
                    curRecord = accuracy_score(test_y.flatten(), result.flatten())
                    accRecord[fold, i, j] = curRecord
        # mean acc over 5 n_splits
        mean_accRecord = np.mean(accRecord, axis=0)
        max_mean_acc = np.max(mean_accRecord)
        maxInd = np.where(mean_accRecord == max_mean_acc)
        max_n = nList[maxInd[0][0]]
        max_c = cList[maxInd[1][0]]

        # given the max_n and max_c, find the max_acc over 5 n_splits
        max_acc = np.max(accRecord[:, maxInd[0][0], maxInd[1][0]])
        max_fold = np.argmax(accRecord[:, maxInd[0][0], maxInd[1][0]])
        

        # re-run the max_fold with max_c and max_n
        train_ind, _ = ind_list[max_fold]
        train_x, train_y = data[train_ind], label[train_ind]

        # # re-fit the model with all the data
        # train_x, train_y = data, label

        self.csp_unit_fit(max_n, train_x, train_y)
        data_csp = self.csp_unit_transform(train_x)

        self.classifier_model = Pipeline([
            ('sc', StandardScaler()),
            # ('pca', PCA(n_components=new_nc)),
            # ('clf', GridSearchCV(svr, parameters))
            ('clf', SVC(C=max_c, gamma='auto'))
        ])
        self.classifier_model.fit(data_csp, train_y.flatten())
        print(max_acc)
        return max_acc

    def fit(self, data, label):
        data = select_channel(data)
        # downsampling the data, the Default axis is -1
        data = decimate(data, q=5)
        fs = 200
        # bandpass filter, the Default axis is -1
        data = butter_bandpass_filter(data, 8, 32, fs, order=6)
        data = data[:, :, 100:700]
        # # split the data into training and test data
        # sf = StratifiedKFold(n_splits=5, shuffle=True)
        
        # train_ind, test_ind = sf.split(data, label).__next__()
        # train_x, train_y = data[train_ind], label[train_ind]
        # test_x, test_y = data[test_ind], label[test_ind]

        acc = self.cross_validation_unit(data, label.flatten())
        return acc

    def predict(self, test_x):
        test_x = select_channel(test_x)
        test_x = decimate(test_x, q=5)
        fs = 200
        
        test_x = butter_bandpass_filter(test_x, 8, 32, fs, order=6)
        test_x = test_x[:, :, 100:700]
        csp_data = self.csp_unit_transform(test_x)
        y_pred = self.classifier_model.predict(csp_data)
        return y_pred


class FBCSP_classifier(CSP_classifier):

    def fbcsp_unit_fit(self, n_components, train_x, train_y):
        lowcut_list = [8, 12, 16, 20, 24, 28]
        highcut_list = [12, 16, 20, 24, 28, 32]
        fs = 200

        label = set(train_y)  # get the label of dataset
        # the combination between labels
        comb_list = list(itertools.combinations(label, 2))
        self.fbcsp_model = []
        for lowcut, highcut in zip(lowcut_list, highcut_list):
            temp_train_x = butter_bandpass_filter(
                train_x, lowcut, highcut, fs, order=6)

            model_per_freq = []
            for (class_1, class_2) in comb_list:
                ind_1_train = np.where(train_y == class_1)
                ind_2_train = np.where(train_y == class_2)
                ind_train = np.concatenate((ind_1_train[0], ind_2_train[0]))
                csp = CSP(n_components=n_components, reg=None,
                          log=True, norm_trace=False)
                csp.fit(temp_train_x[ind_train], train_y[ind_train])
                model_per_freq.append(csp)
                del csp
            self.fbcsp_model.append(model_per_freq)

    def fbcsp_unit_transform(self, data):
        lowcut_list = [8, 12, 16, 20, 24, 28]
        highcut_list = [12, 16, 20, 24, 28, 32]
        fs = 200
        temp_data = []
        for i, (lowcut, highcut) in enumerate(zip(lowcut_list, highcut_list)):
            temp_x = butter_bandpass_filter(data, lowcut, highcut, fs, order=6)
            for csp in self.fbcsp_model[i]:
                temp_data.append(csp.transform(temp_x))
        fbcsp_data = reduce(lambda x, y: np.concatenate(
            (x, y), axis=1), temp_data)
        return fbcsp_data

    def cross_validation_unit(self, data, label, confuMatrix=False):

        nList = list(range(1, 11))
        mList = list(range(2, 7))
        cList = [2**(-5), 2**(-4), 2**(-3), 2**(-2), 2**(-1)]
        cList = cList + list(range(1, 21))

        n_splits = 5
        accRecord = np.zeros((n_splits, len(nList), len(mList), len(cList)))

        sf = StratifiedKFold(n_splits=n_splits, shuffle=True)
        ind_list = [x for x in sf.split(data, label)]

        for fold, (train_ind, test_ind) in enumerate(ind_list):
            train_x, train_y = data[train_ind], label[train_ind]
            test_x, test_y = data[test_ind], label[test_ind]

            for i, n_components in enumerate(nList):

                self.fbcsp_unit_fit(n_components, train_x, train_y)
                train_x_all = self.fbcsp_unit_transform(train_x)
                test_x_all = self.fbcsp_unit_transform(test_x)

                for j, mi_num in enumerate(mList):
                    select_K = sklearn.feature_selection.SelectKBest(
                        mutual_info_classif, k=mi_num).fit(train_x_all, train_y)
                    train_x_mi = select_K.transform(train_x_all)
                    test_x_mi = select_K.transform(test_x_all)

                    for k, c in enumerate(cList):
                        pipe_lr = Pipeline([
                            ('sc', StandardScaler()),
                            # ('pca', PCA(n_components=new_nc)),
                            # ('clf', GridSearchCV(svr, parameters))
                            ('clf', SVC(C=c, gamma='auto'))
                        ])
                        pipe_lr.fit(train_x_mi, train_y.flatten())
                        curRecord = pipe_lr.score(test_x_mi, test_y.flatten())
                        accRecord[fold, i, j, k] = curRecord
        mean_accRecord = np.mean(accRecord, axis=0)
        max_mean_acc = np.max(mean_accRecord)
        maxInd = np.where(mean_accRecord == max_mean_acc)
        max_n = nList[maxInd[0][0]]
        max_m = mList[maxInd[1][0]]
        max_c = cList[maxInd[2][0]]

        # given the max_n and max_c, find the max_acc over 5 n_splits
        max_acc = np.max(accRecord[:, maxInd[0][0], maxInd[1][0], maxInd[2][0]])
        max_fold = np.argmax(accRecord[:, maxInd[0][0], maxInd[1][0], maxInd[2][0]])
        

        # re-run the max_fold with max_c and max_n
        train_ind, _ = ind_list[max_fold]
        train_x, train_y = data[train_ind], label[train_ind]

        # # re-fit the model with all the data
        # train_x, train_y = data, label

        self.fbcsp_unit_fit(max_n, train_x, train_y)
        fbcsp_data = self.fbcsp_unit_transform(train_x)
        self.select_K = sklearn.feature_selection.SelectKBest(mutual_info_classif, k=max_m).fit(fbcsp_data, train_y)
        all_data_mi = self.select_K.transform(fbcsp_data)

        self.classifier_model = Pipeline([
            # ('sc', StandardScaler()),
            # ('pca', PCA(n_components=new_nc)),
            # ('clf', GridSearchCV(svr, parameters))
            ('clf', SVC(C=max_c, gamma='auto'))
        ])
        self.classifier_model.fit(all_data_mi, train_y.flatten())
        print(max_fold, max_n, max_m, max_c)
        print(max_acc)
        return max_acc

    def fit(self, data, label):
        data = select_channel(data)
        # downsampling the data, the Default axis is -1
        data = decimate(data, q=5)
        # bandpass filter, the Default axis is -1
        # data = butter_bandpass_filter(data, 8, 32, 200, order=6)
        
        acc = self.cross_validation_unit(data, label.flatten())
        return acc

    def predict(self, test_x):
        test_x = select_channel(test_x)
        test_x = decimate(test_x, q=5)
        # test_x = butter_bandpass_filter(test_x, 8, 32, 200, order=6)

        fbcsp_data = self.fbcsp_unit_transform(test_x)
        mi_data = self.select_K.transform(fbcsp_data)
        y_pred = self.classifier_model.predict(mi_data)
        return y_pred

'''
if __name__ == '__main__':
    matdata = sio.loadmat('C:/Users/liste/Desktop/temp/subject_26.mat')
    task_data = matdata['task_data'][0:2]
    task_label = matdata['task_label'][0:2]

    data = np.reshape(task_data, (-1, 62, 800))
    label = np.reshape(task_label, (-1, 1))
    a1 = np.where(label==4)[0]
    a5 = np.where(label==5)[0]
    ind = np.concatenate((a1,a5))
    data = data[ind]
    label = label[ind]

    skf = StratifiedKFold(n_splits=5, shuffle=True)
    for train_index, test_index in skf.split(data, label):
        train_x, train_y = data[train_index], label[train_index]
        test_x, test_y = data[test_index], label[test_index]
        
        cla = CSP_classifier()
        cla.fit(train_x, train_y)

        # task_data = matdata['task_data'][3]
        # task_label = matdata['task_label'][3]

        # data = np.reshape(task_data, (-1, 62, 800))
        # label = np.reshape(task_label, (-1, 1))
        # a1 = np.where(label==4)[0]
        # a5 = np.where(label==5)[0]
        # ind = np.concatenate((a1,a5))
        # test_x = data[ind]
        # test_y = label[ind]

        pred_label = cla.predict(train_x)

        print(train_y.flatten())
        print(pred_label)
        break
'''