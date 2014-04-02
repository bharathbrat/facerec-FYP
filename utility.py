import numpy as np

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

