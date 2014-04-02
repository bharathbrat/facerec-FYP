from PIL import Image
import random
import numpy as np
import cv2

"""
def read_yale_images(path, sz=None):
    c = 0
    count = 0
    flag = 1
    training,testing,testing_answer,training_answer = [],[],[],[]
    for dirname,dirnames,filenames in os.walk(path):
        for filename in filenames:
            c = c+1
            x =random.random()
            try:
                if(x<0.5):
                    img = Image.open(os.path.join(dirname, filename))
                    img = img.convert("L")
                    testing.append(np.asarray(img, dtype=np.uint8))
                    testing_answer.append(filename)
                else:
                    im = Image.open(os.path.join(dirname,filename))
                    im = im.convert("L")    
                    if(sz is not None):
                        im = im.resize(sz, Image.ANTIALIAS)
                    training.append(np.asarray(im,dtype=np.uint8))
                    training_answer.append(filename)
            except IOError:
                print "I/O Error({0}) : {1}".format(errno,strerror)
            except:
                print "Unexpected Error: ",sys.exc_info()[0]
                raise
    print len(training), len(testing)
    return [training,training_answer,testing,testing_answer]
"""

def read_yale_images(test):
    if(test == "general"):
        dataset = ['centerlight','glasses','happy','leftlight','noglasses','normal','rightlight','sad','sleepy','surprised','wink']
    elif(test == "illumination"):
        dataset = ['centerlight','leftlight','noglasses','normal','rightlight']
    elif(test == "expression"):
        dataset = ['centerlight','happy','noglasses','normal','sad','sleepy','surprised','wink']
    elif(test == "glasses"):
        dataset = ['centerlight','glasses','noglasses','normal']
    count = 0
    training,testing,testing_answer,training_answer = [],[],[],[]
    for i in range(1,16):
        if(i < 10):
            filename = "subject0"+str(i)+"."
        else:
            filename = "subject"+str(i)+"."
        for item in dataset:
            if(count%2 == 0):
                    img = Image.open("yalefaces/"+filename+item)
                    img = img.convert("L")
                    testing.append(np.asarray(img, dtype=np.uint8))
                    testing_answer.append(filename+item)
            elif(count%2 == 1):
                    img = Image.open("yalefaces/"+filename+item)
                    img = img.convert("L")
                    training.append(np.asarray(img, dtype=np.uint8))
                    training_answer.append(filename+item)
            count += 1
    print len(training), len(testing)
    return [training,training_answer,testing,testing_answer]

def read_orl_images(test):
    if(test == 'general'):
        dataset = ['1','2','3','4','5','6','7','8','9','10']
    elif(test == 'pose'):
        dataset = ['1','2','3','4','5','6','10']
    count = 0
    training,testing,testing_answer,training_answer = [],[],[],[]
    for i in range(1,41):
        for j in range(len(dataset)):
            if(count%2   == 1):
                img = cv2.imread("orl_faces/s"+str(i)+"/"+str(dataset[j])+".pgm",0)
                testing.append(np.asarray(img, dtype=np.uint8))
                testing_answer.append('s'+str(i)+'/'+str(dataset[j])+'.pgm')
            else:
                img = cv2.imread("orl_faces/s"+str(i)+"/"+str(dataset[j])+".pgm",0)
                training.append(np.asarray(img, dtype=np.uint8))
                training_answer.append('s'+str(i)+"/"+str(dataset[j])+'.pgm')
            count += 1
    print len(training), len(testing)
    return [training,training_answer,testing,testing_answer]
                            

