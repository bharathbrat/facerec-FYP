import numpy as np
import cv2, platform
import sys,os,glob
import errno,random
from PIL import Image
from input import *
from utility import *
import operator,math,atexit
from time import clock

minDist=100000

def CannyThreshold(img,lowThreshold,ratio,kernel_size):
#    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    detected_edges = cv2.GaussianBlur(img,(3,3),0)
    detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)
    dst = cv2.bitwise_and(img,img,mask = detected_edges)  # just add some colours to edges from original image.
    return dst

def extract_corners(gray):
    corners=cv2.goodFeaturesToTrack(gray,100,0.01,6)
    return corners

def extract_contours(gray):
    ret,thresh1 = cv2.threshold(gray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours= np.vstack(contours).squeeze()
    return contours

def calc_distance(a,b):
    maxDist=0
    for i in a:
        minB=1000000
        for j in b:
            (x1,y1)=i.ravel()
            (x2,y2)=j.ravel()
            dx=x1-x2
            dy=y1-y2
            tempDist= dx*dx + dy*dy

            if(tempDist<minB):
                minB=tempDist
            elif(tempDist == 0):
                break
        maxDist +=minB
        if(maxDist>minDist):
            return 10000000
    return maxDist

def hausdroff_distance(a,b):
    a= np.int0(a)
    b= np.int0(b)
    maxDistAB = calc_distance(a,b)
    if(maxDistAB==10000000):
        return maxDistAB
    maxDistBA = calc_distance(b,a)
    if(maxDistBA==10000000):
        return maxDistAB
    maxDist = max(maxDistAB, maxDistBA)
    return math.sqrt(maxDist)

def predict_hausdroff(testing_corners,training_corners,training_answer):
    countJ=0
    distances=[]
    for j in training_corners:
            dist=hausdroff_distance(testing_corners,j)
            distances.append(dist)
            minDist=min(distances)
            #print "---",distances
            #print "***",minDist
            #print training_answer[countJ]," dist is= ",dist
            countJ+=1
    min_index, min_value = min(enumerate(distances), key=operator.itemgetter(1))
    result=training_answer[min_index]
    return result



def test_yale(test):
    projections = []
    success = []
    failure = []
    print "TESTING YALE DATABASE---- LINE EDGE MAP"
    training, training_answer, testing, testing_answer = [],[],[],[]
    [training, training_answer, testing, testing_answer] = read_yale_images(test)    
    print "read images"
    training_canny,testing_canny,testing_corners,training_corners=[],[],[],[]
    if platform.system()=="Windows":
        look="\\"
    else:
        look="/"
        
    for i in training:
        modified = CannyThreshold(i,50,3,3)
        training_canny.append(modified)
#        gray = cv2.cvtColor(modified,cv2.COLOR_BGR2GRAY)
        training_corners.append(extract_corners(modified))
    
    for i in testing:
        modified = CannyThreshold(i,50,3,3)
        testing_canny.append(modified)
#        gray = cv2.cvtColor(modified,cv2.COLOR_BGR2GRAY)
        testing_corners.append(extract_corners(modified))
    print "extracted corners"
    
    #predict_LEM(testing_corners[0],training_corners[0])
##################################    
    if(test == "choice"):
        return testing_corners, training_corners, training_answer, testing_answer
###################################
    countI=0
    count=0
    #start clock
    startTime=clock()
    for i in testing_corners:
        result=predict_hausdroff(i,training_corners,training_answer)
        testAns=testing_answer[countI]
        print result," MATCHED WITH ",  testAns
        if(result[:result.find('.')] == testAns[:testAns.find('.')]):
            print "HIT!"
            count+=1
            success.append((testAns,result))
        else:
            failure.append((testAns,result))
        countI+=1
    endTime=clock()
    #end clock
    totalTime=endTime-startTime
    print "total time = ", totalTime
    singleTime=float(totalTime)/len(testing)
    print "single time = ", singleTime
    singleTimeString=formatTime(secondsToStr(singleTime))
    totalTimeString=formatTime(secondsToStr(totalTime))
    accuracy = (float(count)/len(testing))*100
    print accuracy,"\n", totalTimeString, "\n", singleTimeString
    print len(success),len(failure)
    failure_Path="LEM_yale_failure_"+test+".png"
    success_Path="LEM_yale_success_"+test+".png"
    success_copyPath=os.path.join(os.path.join("static","images"),success_Path)
    failure_copyPath=os.path.join(os.path.join("static","images"),failure_Path)
    plot(failure_copyPath, failure[:4*(len(failure)/4)])
    plot(success_copyPath, success[:4])
    return failure_Path,success_Path, accuracy, singleTimeString,totalTimeString, len(training), len(testing), count


def test_orl(test):
    projections = []
    success = []
    failure = []
    print "TESTING ORL DATABASE ---- LINE EDGE MAP"
    training, training_answer, testing, testing_answer = [],[],[],[]
    [training, training_answer, testing, testing_answer] = read_orl_images(test)
    print "read images"
    training_canny,testing_canny,testing_corners,training_corners=[],[],[],[]
    if platform.system()=="Windows":
        look="\\"
    else:
        look="/"
        
    for i in training:
        modified = CannyThreshold(i,50,3,3)
        training_canny.append(modified)
#        gray = cv2.cvtColor(modified,cv2.COLOR_BGR2GRAY)
        training_corners.append(extract_corners(modified))
    
    for i in testing:
        modified = CannyThreshold(i,50,3,3)
        testing_canny.append(modified)
#        gray = cv2.cvtColor(modified,cv2.COLOR_BGR2GRAY)
        testing_corners.append(extract_corners(modified))
    print "extracted corners"
    
    #predict_LEM(testing_corners[0],training_corners[0])
##################################    
    if(test == "choice"):
        return testing_corners, training_corners, training_answer, testing_answer
###################################
    countI=0
    count=0
    #start clock
    startTime=clock()
    for i in testing_corners:
        result=predict_hausdroff(i,training_corners,training_answer)
        testAns=testing_answer[countI]
        print result," MATCHED WITH ",testAns
        if(result[:result.find(look,12)] == testAns[:testAns.find(look,12)]):
            print "HIT!"
            count+= 1
            success.append((testAns,result))
        
        else:
            failure.append((testAns,result))
        countI+=1
    endTime=clock()
    #end clock
    totalTime=endTime-startTime
    print "total time = ", totalTime
    singleTime=float(totalTime)/len(testing)
    print "single time = ", singleTime
    print "seconds to string " , secondsToStr(singleTime)
    print "seconds to string total" , secondsToStr(totalTime)
    singleTimeString=formatTime(secondsToStr(singleTime))
    totalTimeString=formatTime(secondsToStr(totalTime))
    accuracy = (float(count)/len(testing))*100
    print accuracy,"\n", totalTimeString, "\n", singleTimeString
    failure_Path="LEM_orl_failure_"+test+".png"
    success_Path="LEM_orl_success_"+test+".png"
    success_copyPath=os.path.join(os.path.join("static","images"),success_Path)
    failure_copyPath=os.path.join(os.path.join("static","images"),failure_Path)
    plot(failure_copyPath, failure[:4*(len(failure)/4)])
    plot(success_copyPath, success[:16])
    return failure_Path,success_Path, accuracy, singleTimeString,totalTimeString, len(training), len(testing), count



