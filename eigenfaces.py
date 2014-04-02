import cv2
import numpy as np
import os
import sys
from PIL import Image
import random

from input import *
from utility import *

def pca(X, y):
    n,d = X.shape
    mu = X.mean(axis = 0)
    X = X - mu
    num_components = n
    if(n>d):
        C = np.dot(X.T,X)
        [eigenvalues,eigenvectors] = np.linalg.eigh(C)
    else:
        C = np.dot(X,X.T)
        [eigenvalues,eigenvectors] = np.linalg.eigh(C)
        eigenvectors = np.dot(X.T,eigenvectors)
        for i in xrange(n):
            eigenvectors[:,i] = eigenvectors[:,i]/np.linalg.norm(eigenvectors[:,i])
    idx = np.argsort(-eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:,idx]
    eigenvalues = eigenvalues[0:num_components].copy()
    eigenvectors = eigenvectors[:,0:num_components].copy()
    return [eigenvalues, eigenvectors, mu]


def test_yale():
    projections = []
    print "TESTING YALE DATABASE"
    training, training_answer, testing, testing_answer = [],[],[],[]
    [training, training_answer, testing, testing_answer] = read_yale_images("illumination")
    [D, W, mu] = pca(asRowMatrix(training), training_answer)    
    for xi in training:
        projections.append(project(W,xi.reshape(1,-1),mu))
    count = 0
    for i in range(len(testing)):
        result = predict(testing[i], training_answer, W, mu, projections)
        print result, testing_answer[i]
        if(result[6:9] == testing_answer[i][6:9]):
            print "HIT!"
            count+= 1
    print (float(count)/len(testing))*100

def test_orl():
    projections = []
    print "TESTING ORL DATABASE"
    training, training_answer, testing, testing_answer = [],[],[],[]
    [training, training_answer, testing, testing_answer] = read_orl_images('pose')
    [D, W, mu] = pca(asRowMatrix(training), training_answer)
    for xi in training:
        projections.append(project(W,xi.reshape(1,-1),mu))
    count = 0
    for i in range(len(testing)):
        result = predict(testing[i], training_answer, W, mu, projections)
        print result, testing_answer[i]
        if(result[:result.find("/")] == testing_answer[i][:testing_answer[i].find("/")]):
            print "HIT!"
            count+= 1
    print (float(count)/len(testing))*100
test_yale()
#test_orl()

