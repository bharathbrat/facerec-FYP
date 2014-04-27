import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
import os
def asRowMatrix(X):
    if len(X) == 0:
        return np.array([])
    mat = np.empty((0,X[0].size),dtype=X[0].dtype)
    for row in X:
        mat = np.vstack((mat,np.asarray(row).reshape(1,-1)))
    return mat

def project(W,X,mu=None):
    if mu is None:
        return np.dot(X,W)
    return np.dot(X-mu,W)

def EuclideanDistance(p, q):
    p = np.asarray(p).flatten()
    q = np.asarray(q).flatten()
    return np.sqrt(np.sum(np.power((p-q),2)))

def predict(X, y, W, mu, projections):
    minDist = np.finfo('float').max
    minClass = -1
    Q = project(W, X.reshape(1,-1), mu)
    i = 0
    for i in xrange(len(projections)):
        dist = EuclideanDistance(projections[i], Q)
        #print i
        if(dist<minDist):
            minDist = dist
            minClass  = y[i]
    return minClass

def create_font(fontname='Tahoma',fontsize=10):
    return {'fontname':fontname, 'fontsize':fontsize}

def choicePlot(image1,image2,title):
    os.system("convert "+image1+" "+image2+" +append "+"plots/"+title)

def plot(title, images):
    fig = plt.figure()#figsize=(4,3),dpi=50)
    for i in xrange(len(images)):
        os.system("convert "+images[i][0]+" "+images[i][1]+" +append temp")
        ax0 = plt.subplot(len(images)/4, 4, i)
        plt.setp(ax0.get_xticklabels(),visible=False)
        plt.setp(ax0.get_yticklabels(),visible=False)
        img = Image.open("temp")
        plt.imshow(img, cmap = cm.gray, origin = 'lower')
    print "Plotted "+title
    fig.savefig("plots/"+title)

def subplot(title, images, rows, cols, sptitle="subplot", sptitles = [], colormap=cm.gray, ticks_visible=True, filename=None):
    fig = plt.figure()
    fig.text(.5, .95, title, horizontalalignment='center')
    for i in xrange(len(images)):
        ax0 = fig.add_subplot(rows,cols,(i+1))
        plt.setp(ax0.get_xticklabels(),visible=False)
        plt.setp(ax0.get_yticklabels(),visible=False)
        if(len(sptitles) == len(images)):
            plt.title("%s #%s"%(sptitle,str(sptitles[i])), create_font('Tahoma',10))
        else:
            plt.title("%s #%d"%(sptitle,(i+1)), create_font('Tahoma',10))
        img = plt.imread(images[i])
        plt.imshow(img, cmap = colormap, origin = 'upper')

    if (filename is None):
        plt.show()
    else:
        fig.savefig(filename)

