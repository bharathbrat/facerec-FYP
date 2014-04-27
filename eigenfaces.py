import cv2
import numpy as np
import os
import sys
from PIL import Image
import random

from input import *
from utility import *

def pca(X, y, num_components=0):
    n,d = X.shape
    if (num_components<=0) or (num_components>n):
        num_components=n
    mu = X.mean(axis = 0)
    X = X - mu
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


def test_yale(test):
    projections = []
    success = []
    failure = []
    print "TESTING YALE DATABASE --- EIGENFACE"
    training, training_answer, testing, testing_answer = [],[],[],[]
    [training, training_answer, testing, testing_answer] = read_yale_images(test)
    [D, W, mu] = pca(asRowMatrix(training), training_answer)    
    for xi in training:
        projections.append(project(W,xi.reshape(1,-1),mu))
    count = 0
##################################################################
    if(test == "choice"):
        return testing, training_answer, W, mu, projections, testing_answer
##################################################################
    for i in range(len(testing)):
        result = predict(testing[i], training_answer, W, mu, projections)
        print result, testing_answer[i]
        if(result[6:9] == testing_answer[i][6:9]):
            print "HIT!"
            count+= 1
            success.append(("yalefaces/"+testing_answer[i],"yalefaces/"+result))
        else:
            failure.append(("yalefaces/"+testing_answer[i],"yalefaces/"+result))
    plot("Eigenface_yale_failure_"+test, failure[:4*(len(failure)/4)])
    plot("Eigenface_yale_success_"+test, success[:16])
    accuracy = (float(count)/len(testing))*100
    print accuracy
    os.system("convert Eigenface_yale_failure_"+test+".png  Eigenface_yale_failure_"+test+".pgm")
    os.system("convert Eigenface_yale_success_"+test+".png  Eigenface_yale_success_"+test+".pgm")
    return "Eigenface_yale_failure_"+test+".pgm", "Eigenface_yale_success_"+test+".pgm", accuracy

def test_orl(test):
    projections = []
    success = []
    failure = []
    print "TESTING ORL DATABASE --- EIGENFACE"
    training, training_answer, testing, testing_answer = [],[],[],[]
    [training, training_answer, testing, testing_answer] = read_orl_images(test)
    [D, W, mu] = pca(asRowMatrix(training), training_answer)
    for xi in training:
        projections.append(project(W,xi.reshape(1,-1),mu))
    count = 0
##################################################################
    if(test == "choice"):
        return testing, training_answer, W, mu, projections, testing_answer
##################################################################
    for i in range(len(testing)):
        result = predict(testing[i], training_answer, W, mu, projections)
        print result, testing_answer[i]
        if(result[:result.find("/")] == testing_answer[i][:testing_answer[i].find("/")]):
            print "HIT!"
            count+= 1
            success.append(("orl_faces/"+testing_answer[i],"orl_faces/"+result))
        else:
            failure.append(("orl_faces/"+testing_answer[i],"orl_faces/"+result))
    accuracy = (float(count)/len(testing))*100
    print accuracy
    plot("Eigenface_orl_failure_"+test, failure[:4*(len(failure)/4)])
    plot("Eigenface_orl_success_"+test, success[:16])
    os.system("convert Eigenface_orl_failure_"+test+".png  Eigenface_orl_failure_"+test+".pgm")
    os.system("convert Eigenface_orl_success_"+test+".png  Eigenface_orl_success_"+test+".pgm")
    return "Eigenface_orl_failure_"+test+".pgm", "Eigenface_orl_success_"+test+".pgm", accuracy
