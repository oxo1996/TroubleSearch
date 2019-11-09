import numpy as np
import math

def l2Norm(a):
    return math.sqrt(np.dot(a, a))

def cosineSimilarity(a, b):
    #print(np.dot(a,b) / (self._l2Norm(a) * self._l2Norm(b)))
    return np.dot(a, b) / (l2Norm(a) * l2Norm(b))