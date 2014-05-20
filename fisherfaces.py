import glob, os
from PIL import Image
import sys,cv2,atexit
from time import clock
import numpy as np
sys.path.append("..")
import errno,random,platform
from utility import *
from input import *
from eigenfaces import pca
      
def lda(X, y, num_components=0):
    y=np.asarray(y)
    c=np.unique(y)
    [n,d]= X.shape
    
    if (num_components<=0) or (num_components>(len(c)-1)):
        num_components=len(c)-1
    '''STEP 1: find global mean '''
    GlobalMean=X.mean(axis=0)
    Sw=np.zeros((d,d),dtype=np.float32)
    Sb=np.zeros((d,d),dtype=np.float32)
    ''' STEP 2: find mean of indiviual classes'''
    for i in c:
        Xi=X[np.where(y==i)[0],:]
        ClassMean= Xi.mean(axis=0)
        Sb = Sb + ( n* np.dot((ClassMean-GlobalMean).T,(ClassMean-GlobalMean)))
        Sw = Sw + ( np.dot((Xi-ClassMean).T,(Xi-ClassMean)))
    eigenvalues, eigenvectors = np.linalg.eig(np.linalg.inv(Sw)*Sb)
    idx=np.argsort(-eigenvalues.real)
    eigenvalues, eigenvectors = eigenvalues[idx], eigenvectors[:,idx]
    eigenvalues = np.array(eigenvalues[0:num_components].real, dtype = np.float32,copy=True)
    eigenvectors = np.array(eigenvectors[0:,0:num_components].real, dtype = np.float32,copy=True)
    return [eigenvalues,eigenvectors]
        

def fisherfaces(X, y, num_components=0):
    y=np.asarray(y)
    c=len(np.unique(y))
    [n,d]= X.shape
    [eigenvalues_pca, eigenvectors_pca, mu_pca] = pca(X,y,n-c)  #Number of components removed ??
    [eigenvalues_lda, eigenvectors_lda] = lda(project(eigenvectors_pca, X, mu_pca),y,num_components)
    eigenvectors=np.dot(eigenvectors_pca,eigenvectors_lda)
    return [eigenvalues_lda, eigenvectors, mu_pca]


def test_yale(test):
    projections = []
    success = []
    failure = []
    print "TESTING YALE DATABASE --- FISHERFACE"
    training, training_answer, testing, testing_answer = [],[],[],[]
    [training, training_answer, testing, testing_answer] = read_yale_images(test)
    if platform.system()=="Windows":
        look="\\"
    else:
        look="/"

    training_class, testing_class = [], []    
    for i in training_answer:
        training_class.append(int(i[i.find("t")+1:i.find(".")]))

    for j in testing_answer:
        testing_class.append(int(i[i.find("t")+1:i.find(".")]))
    [D, W, mu] = fisherfaces(asRowMatrix(training), training_class) 
   
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

    success_Path="Fisherface_yale_success_"+test
    failure_Path="Fisherface_yale_failure_"+test
    success_copyPath=os.path.join(os.path.join("static","images"),success_Path)
    failure_copyPath=os.path.join(os.path.join("static","images"),failure_Path)
    plot(failure_copyPath, failure[:4*(len(failure)/4)])
    plot(success_copyPath, success[:8])
    return failure_Path,success_Path, accuracy, singleTimeString,totalTimeString, len(training), len(testing), count

def test_orl(test):
    projections = []
    success = []
    failure = []
    print "TESTING ORL DATABASE --- FISHERFACE"
    training, training_answer, testing, testing_answer = [],[],[],[]
    [training, training_answer, testing, testing_answer] = read_orl_images(test)
    training_class, testing_class = [], []
    if platform.system()=="Windows":
        look="\\"
    else:
        look="/"
    for i in training_answer:
        training_class.append(int(i[i.find("s",9)+1:i.find(look,12)]))

    for j in testing_answer:
        testing_class.append(int(i[i.find("s",9)+1:i.find(look,12)]))

    [D, W, mu] = fisherfaces(asRowMatrix(training), training_class)
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

    success_Path="Fisherface_orl_success_"+test+".png"
    failure_Path="Fisherface_orl_failure_"+test+".png"
    success_copyPath=os.path.join(os.path.join("static","images"),success_Path)
    failure_copyPath=os.path.join(os.path.join("static","images"),failure_Path)
    plot(failure_copyPath, failure[:4*(len(failure)/4)])
    plot(success_copyPath, success[:16])
    return failure_Path,success_Path, accuracy, singleTimeString,totalTimeString, len(training), len(testing), count


