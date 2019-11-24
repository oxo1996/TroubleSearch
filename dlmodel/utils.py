import numpy as np
import math


def l2_norm(a):
    return math.sqrt(np.dot(a, a))


def cosine_similarity(a, b):
    # print(np.dot(a,b) / (self._l2_norm(a) * self._l2_norm(b)))
    return np.dot(a, b) / (l2_norm(a) * l2_norm(b))
