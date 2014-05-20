import cv2
import numpy as np
import scipy
import os
import math, platform,atexit
from time import clock
from input import *
from utility import *

def parse(fileName):
    f = open(fileName,'r')
    data = f.read()
    data = data.split()
    locs = []
    descriptors = []
    [n, d] = data[0],data[1]
    for i in range(len(data)):
        data[i] = float(data[i])
    i = 2
    while(i<len(data)):
        tempLocs = []
        tempDescriptors = []
        squareDescriptors = []
        tempLocs = data[i:i+4]
        tempDescriptors = data[i+4:i+132]
        squareDescriptors = [x*x for x in tempDescriptors]
        tempDescriptors = [x/math.sqrt(sum(squareDescriptors)) for x in tempDescriptors]
        locs.append(tempLocs)
        descriptors.append(tempDescriptors)
        i += 132
    return [locs, descriptors]

def sift(url):
    locs, descriptors = parse(url+'.key')
    return [locs, descriptors]

def CosineDistance(p,q):
    p = np.asarray(p).flatten()
    q = np.asarray(q).flatten()
    return -np.dot(p.T,q) / (np.sqrt(np.dot(p,p.T)*np.dot(q,q.T)))

def localPredict(test, answerSet, training):
    match = []
    dist = []
    minimum = 0
    index = 999
    for i in xrange(len(training)):
        trainDesc = np.asarray(training[i]).T
        [t1, t2] = matchImage(test, trainDesc)
        if(len(t1)>len(dist)):
            dist = t1
            match = t2
            index = i
    if(index!=999):
        return answerSet[index]
    else:
        return 999

def matchImage(test, trainDesc):
    distRatio = 0.6
    count = 0
    match = []
    dist = []
    testDesc = np.asarray(test)
    dotprods = np.dot(testDesc,trainDesc)
    for i in xrange(len(dotprods)):
        dotprod = dotprods[i]
        for j in xrange(len(dotprod)):
            try:
                dotprod[j] = math.acos(dotprod[j])
            except ValueError:
                continue
        idx = np.argsort(dotprod)
        newdotprods = dotprod[idx]
        if(newdotprods[0] < distRatio * newdotprods[1]):
            match.append(list(dotprod).index(newdotprods[0]))
            dist.append(newdotprods[0])
    return dist, match
    
def test_orl(test):
    [training,training_answer,testing,testing_answer] = read_orl_images(test)
    success = []
    failure = []
    locs_training, descriptors_training = [], []
    locs_testing, descriptors_testing = [], []
    if platform.system()=="Windows":
        look="\\"
    else:
        look="/"
    for i in training_answer:
        [a,b] = sift(i)
        locs_training.append(a)
        descriptors_training.append(b)
    for i in testing_answer:
        [a,b] = sift(i)
        locs_testing.append(a)
        descriptors_testing.append(b)
    count = 0
    x = 0
##################################################################
    if(test == "choice"):
        return descriptors_testing, training_answer, descriptors_training, testing_answer
##################################################################
    #start clock
    startTime=clock()
    for i in range(len(testing_answer)):
        result = localPredict(descriptors_testing[i], training_answer, descriptors_training)
        if (result!=999):
            testAns=testing_answer[i]
            print result," MATCHED WITH ", testAns
            if(result[:result.find(look,12)] == testAns[:testAns.find(look,12)]):
                print "HIT!"
                count += 1
                success.append((testAns,result))
            else:
                failure.append((testAns,result))
        else:
            print "No match!", testAns
            x += 1
    endTime=clock()
    #end clock
    totalTime=endTime-startTime
    singleTime=float(totalTime)/len(testing)
    singleTimeString=formatTime(secondsToStr(singleTime))
    totalTimeString=formatTime(secondsToStr(totalTime))
    accuracy = (float(count)/len(testing))*100
    print accuracy,"\n", totalTimeString, "\n", singleTimeString

    success_Path="SIFT_orl_success_"+test+".png"
    failure_Path="SIFT_orl_failure_"+test+".png"
    success_copyPath=os.path.join(os.path.join("static","images"),success_Path)
    failure_copyPath=os.path.join(os.path.join("static","images"),failure_Path)
    plot(failure_copyPath, failure[:4*(len(failure)/4)])
    plot(success_copyPath, success[:8])
    return failure_Path,success_Path, accuracy, singleTimeString,totalTimeString, len(training), len(testing), count


def test_yale(test):
    [training,training_answer,testing,testing_answer] = read_yale_images(test)
    failure = []
    success = []
    locs_training, descriptors_training = [], []
    locs_testing, descriptors_testing = [], []
    if platform.system()=="Windows":
        look="\\"
    else:
        look="/"
    for i in training_answer:
        [a,b] = sift(i)
        locs_training.append(a)
        descriptors_training.append(b)
    for i in testing_answer:
        [a,b] = sift(i)
        locs_testing.append(a)
        descriptors_testing.append(b)
    count = 0
    x = 0
##################################################################
    if(test == "choice"):
        return descriptors_testing, training_answer, descriptors_training, testing_answer
##################################################################
    #start clock
    startTime=clock()
    for i in range(len(testing_answer)):
        result = localPredict(descriptors_testing[i], training_answer, descriptors_training)
        if (result!=999):
            testAns=testing_answer[i]
            print result," MATCHED WITH ", testAns
            if(result[:result.find('.')] == testAns[:testAns.find('.')]):
                print "HIT!"
                count+= 1
                success.append((testAns,result))
            else:
                failure.append((testAns,result))
        else:
            print "No match!", testAns
            x += 1
    endTime=clock()
    #end clock
    totalTime=endTime-startTime
    singleTime=float(totalTime)/len(testing)
    singleTimeString=formatTime(secondsToStr(singleTime))
    totalTimeString=formatTime(secondsToStr(totalTime))
    accuracy = (float(count)/len(testing))*100
    print accuracy,"\n", totalTimeString, "\n", singleTimeString

    success_Path="SIFT_yale_success_"+test+".png"
    failure_Path="SIFT_yale_failure_"+test+".png"
    success_copyPath=os.path.join(os.path.join("static","images"),success_Path)
    failure_copyPath=os.path.join(os.path.join("static","images"),failure_Path)
    plot(failure_copyPath, failure[:4*(len(failure)/4)])
    plot(success_copyPath, success[:8])
    return failure_Path,success_Path, accuracy, singleTimeString,totalTimeString, len(training), len(testing), count

  

