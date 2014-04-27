import cv2
import numpy as np
import scipy
import os
import math
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

def sift(imageFile, db):
    if (db == 'orl'):
        img = cv2.imread('orl_faces/'+imageFile)
        url = 'orl_faces/'+imageFile
    if(db == 'yale'):
        img = cv2.imread('yalefaces/'+imageFile)
        url = 'yalefaces/'+imageFile
#    image = np.asarray(img, dtype=np.uint8)
#    [n,d,s] = image.shape
#    f = open('tmp.pgm','w')
#    f.write('')
#    f.close()

#    f = open('tmp.pgm','a')
#    f.write("P5\n"+str(d)+" "+str(n)+"\n255\n")
#    temp = image.T[0].T.flatten()
#    f.write(temp)
#    f.close()
#    os.system('./sift <tmp.pgm>'+url+'.key')
#    os.system('./sift <orl_faces/s1/'+imageFile+'> tmp.key')
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
    distRatio = 0.5
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
#        else:
#            match.append(0)
    return dist, match
    
def test_orl(test):
    [training,training_answer,testing,testing_answer] = read_orl_images(test)
    success = []
    failure = []
    locs_training, descriptors_training = [], []
    locs_testing, descriptors_testing = [], []
    for i in training_answer:
        [a,b] = sift(i,'orl')
        locs_training.append(a)
        descriptors_training.append(b)
    for i in testing_answer:
        [a,b] = sift(i,'orl')
        locs_testing.append(a)
        descriptors_testing.append(b)
    count = 0
    x = 0
##################################################################
    if(test == "choice"):
        return descriptors_testing, training_answer, descriptors_training
##################################################################
    for i in range(len(testing_answer)):
        result = localPredict(descriptors_testing[i], training_answer, descriptors_training)
        if (result!=999):
            print result, testing_answer[i]
            if(result[:result.find("/")] == testing_answer[i][:testing_answer[i].find("/")]):
                print "HIT!"
                count += 1
                success.append(("orl_faces/"+testing_answer[i],"orl_faces/"+result))
            else:
                failure.append(("orl_faces/"+testing_answer[i],"orl_faces/"+result))
        else:
            print "No match!", testing_answer[i]
            x += 1
    plot("SIFT_orl_failure_"+test+".png", failure[:4*(len(failure)/4)])
    plot("SIFT_orl_success_"+test+".png", success[:16])
    accuracy = 100*float(count)/len(testing_answer)
    print accuracy, x
    return "SIFT_orl_failure_"+test+".png", "SIFT_orl_success_"+test+".png", accuracy

def test_yale(test):
    [training,training_answer,testing,testing_answer] = read_yale_images(test)
    failure = []
    success = []
    locs_training, descriptors_training = [], []
    locs_testing, descriptors_testing = [], []
    for i in training_answer:
        [a,b] = sift(i,'yale')
        locs_training.append(a)
        descriptors_training.append(b)
    for i in testing_answer:
        [a,b] = sift(i,'yale')
        locs_testing.append(a)
        descriptors_testing.append(b)
    count = 0
    x = 0
##################################################################
    if(test == "choice"):
        return descriptors_testing, training_answer, descriptors_training
##################################################################
    for i in range(len(testing_answer)):
        result = localPredict(descriptors_testing[i], training_answer, descriptors_training)
        if (result!=999):
            print i, result, testing_answer[i]
            if(result[0:9] == testing_answer[i][0:9]):
                print "HIT!"
                count += 1
                success.append(("yalefaces/"+testing_answer[i],"yalefaces/"+result))
            else:
                failure.append(("yalefaces/"+testing_answer[i],"yalefaces/"+result))
        else:
            print "No match!", testing_answer[i]
            x += 1
    plot("SIFT_yale_failure_"+test+".png", failure[:4*(len(failure)/4)])
    plot("SIFT_yale_success_"+test+".png", success[:16])
    accuracy = 100*float(count)/len(testing_answer)
    print accuracy, x
    return "SIFT_yale_failure_"+test+".png", "SIFT_yale_success_"+test+".png", accuracy
