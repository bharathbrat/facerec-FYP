import glob, os
from PIL import Image
import sys,cv2
import numpy as np
import errno,random
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

    training_class, testing_class = [], []    
    for i in training_answer:
        training_class.append(int(i[7:i.find(".")]))

    for j in testing_answer:
        testing_class.append(int(j[7:j.find(".")]))
    [D, W, mu] = fisherfaces(asRowMatrix(training), training_class) 
   
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
    plot("Fisherface_yale_failure_"+test, failure[:4*(len(failure)/4)])
    plot("Fisherface_yale_success_"+test, success[:16])
    accuracy = (float(count)/len(testing))*100
    print accuracy
    os.system("convert Fisherface_yale_failure_"+test+".png  Fisherface_yale_failure_"+test+".pgm")
    os.system("convert Fisherface_yale_success_"+test+".png  Fisherface_yale_success_"+test+".pgm")
    return "Fisherface_yale_failure_"+test+".pgm", "Fisherface_yale_success_"+test+".pgm", accuracy


def test_orl(test):
    projections = []
    success = []
    failure = []
    print "TESTING ORL DATABASE --- FISHERFACE"
    training, training_answer, testing, testing_answer = [],[],[],[]
    [training, training_answer, testing, testing_answer] = read_orl_images(test)
    training_class, testing_class = [], []    
    for i in training_answer:
        training_class.append(int(i[1:i.find("/")]))

    for j in testing_answer:
        testing_class.append(int(j[1:j.find("/")]))

    [D, W, mu] = fisherfaces(asRowMatrix(training), training_class)
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
    plot("Fisherface_orl_failure_"+test, failure[:4*(len(failure)/4)])
    plot("Fisherface_orl_success_"+test, success[:16])
    os.system("convert Fisherface_orl_failure_"+test+".png  Fisherface_orl_failure_"+test+".pgm")
    os.system("convert Fisherface_orl_success_"+test+".png  Fisherface_orl_success_"+test+".pgm")
    return "Fisherface_orl_failure_"+test+".pgm", "Fisherface_orl_success_"+test+".pgm", accuracy

