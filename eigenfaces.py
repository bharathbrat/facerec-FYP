import cv2
import numpy as np
import os,sys, platform
from PIL import Image
import random,atexit
from time import clock
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
    if platform.system()=="Windows":
        look="\\"
    else:
        look="/"
        
    for xi in training:
        projections.append(project(W,xi.reshape(1,-1),mu))
    count = 0
##################################################################
    if(test == "choice"):
        return testing, training_answer, W, mu, projections, testing_answer
##################################################################
    #start clock
    startTime=clock()
    for i in range(len(testing)):
        result = predict(testing[i], training_answer, W, mu, projections)
        testAns=testing_answer[i]
        print result," MATCHED WITH ", testAns
        if(result[:result.find('.')] == testAns[:testAns.find('.')]):
            print "HIT!"
            count += 1
            success.append((testAns,result))
        else:
            failure.append((testAns,result))
    endTime=clock()
    #end clock
    totalTime=endTime-startTime
    singleTime=float(totalTime)/len(testing)
    singleTimeString=formatTime(secondsToStr(singleTime))
    totalTimeString=formatTime(secondsToStr(totalTime))
    accuracy = (float(count)/len(testing))*100
    print accuracy,"\n", totalTimeString, "\n", singleTimeString
    print len(success), len(failure)
    success_Path="Eigenface_yale_success_"+test+".png"
    failure_Path="Eigenface_yale_failure_"+test+".png"
    success_copyPath=os.path.join(os.path.join("static","images"),success_Path)
    failure_copyPath=os.path.join(os.path.join("static","images"),failure_Path)
    plot(failure_copyPath, failure[:4*(len(failure)/4)])
    plot(success_copyPath, success[:16])
    return failure_Path,success_Path, accuracy, singleTimeString,totalTimeString, len(training), len(testing), count

def test_orl(test):
    projections = []
    success = []
    failure = []
    print "TESTING ORL DATABASE --- EIGENFACE"
    training, training_answer, testing, testing_answer = [],[],[],[]
    [training, training_answer, testing, testing_answer] = read_orl_images(test)
    [D, W, mu] = pca(asRowMatrix(training), training_answer)
    if platform.system()=="Windows":
        look="\\"
    else:
        look="/"
        
    for xi in training:
        projections.append(project(W,xi.reshape(1,-1),mu))
    count = 0
##################################################################
    if(test == "choice"):
        return testing, training_answer, W, mu, projections, testing_answer
##################################################################
    #start clock
    startTime=clock()
    for i in range(len(testing)):
        result = predict(testing[i], training_answer, W, mu, projections)
        testAns=testing_answer[i]
        print result," MATCHED WITH ", testAns
        if(result[:result.find(look,12)] == testAns[:testAns.find(look,12)]):
            print "HIT!"
            count+= 1
            success.append((testAns,result))
        else:
            failure.append((testAns,result))
    endTime=clock()
    #end clock
    totalTime=endTime-startTime
    singleTime=float(totalTime)/len(testing)
    singleTimeString=formatTime(secondsToStr(singleTime))
    totalTimeString=formatTime(secondsToStr(totalTime))
    accuracy = (float(count)/len(testing))*100
    print accuracy,"\n", totalTimeString, "\n", singleTimeString

    success_Path="Eigenface_orl_success_"+test+".png"
    failure_Path="Eigenface_orl_failure_"+test+".png"
    success_copyPath=os.path.join(os.path.join("static","images"),success_Path)
    failure_copyPath=os.path.join(os.path.join("static","images"),failure_Path)
    plot(failure_copyPath, failure[:4*(len(failure)/4)])
    plot(success_copyPath, success[:16])
    return failure_Path,success_Path, accuracy, singleTimeString,totalTimeString, len(training), len(testing), count



