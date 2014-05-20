from PIL import Image
import random
import numpy as np
import cv2,os,atexit
from time import clock

def read_yale_images(test):
    if(test == "general"):
        training_dataset = ['centerlight','glasses','happy','leftlight','noglasses','normal']
        testing_dataset = ['rightlight','sad','sleepy','surprised','wink']
    elif(test == "illumination"):
        training_dataset = ['glasses','noglasses','normal']
        testing_dataset = ['centerlight','leftlight','rightlight']
    elif(test == "expression"):
        training_dataset = ['noglasses','normal']
        testing_dataset = ['happy','sleepy','sad','wink','surprised']
    elif(test == "glasses"):
        training_dataset = ['noglasses','normal']
        testing_dataset = ['glasses']
    elif(test == "choice"):
        training_dataset = ['centerlight','glasses','happy','leftlight','noglasses']
        testing_dataset = ['normal','rightlight','sad','sleepy','surprised','wink']
    training,testing,testing_answer,training_answer = [],[],[],[]
    for i in range(1,16):
        if(i < 10):
            filename = "subject0"+str(i)+"."
        else:
            filename = "subject"+str(i)+"."
        for item in testing_dataset:
            absName=os.path.join("yalefaces",filename+item+".pgm")
            img = Image.open(absName)
            img = img.convert("L")
            testing.append(np.asarray(img, dtype=np.uint8))
            testing_answer.append(absName)
        for item in training_dataset:
            absName=os.path.join("yalefaces",filename+item+".pgm")
            img = Image.open(absName)
            img = img.convert("L")
            training.append(np.asarray(img, dtype=np.uint8))
            training_answer.append(absName)
    print "training: ",len(training),", testing:",len(testing)
    return [training,training_answer,testing,testing_answer]

def read_orl_images(test):
    if(test == 'general'):
        training_dataset = ['1','2','3','4','5']
        testing_dataset = ['6','7','8','9','10']
    elif(test == 'pose'):
        training_dataset = ['1','3','7','8']
        testing_dataset = ['2','4','5','6','9','10']
    elif(test == "choice"):
        training_dataset = ['1','3','5','7','9']
        testing_dataset = ['2','4','6','8','10']
    count = 0
    training,testing,testing_answer,training_answer = [],[],[],[]
    for i in range(1,41):
        for j in testing_dataset:
            storeName=os.path.join("s"+str(i),j+".pgm")
            absName=os.path.join("orl_faces",storeName)
            img = cv2.imread(absName,0)
            testing.append(np.asarray(img, dtype=np.uint8))
            storeName
            testing_answer.append(absName)
        for j in training_dataset:
            storeName=os.path.join("s"+str(i),j+".pgm")
            absName=os.path.join("orl_faces",storeName)
            img = cv2.imread(absName,0)
            training.append(np.asarray(img, dtype=np.uint8))
            training_answer.append(absName)
    print "training : ",len(training),"  ,  testing :",len(testing)
    return [training,training_answer,testing,testing_answer]


