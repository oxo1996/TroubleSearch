from .feature_extract.bm25 import Bm25
from .embedding.sktkobert import SktKobert
from .utils import cosine_similarity
from .embedding.bert_bm25 import BertBm25
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

if __name__ == '__main__':
    f = open("review_test.txt", 'r')
    reviews = f.readlines()
    print(reviews)
    
    bertbm25 = BertBm25()
    result = bertbm25.most_similar("이거 쓰고 여드름이 났어요.", reviews, 1000)
    for elem in result:
        print(reviews[elem[0]], elem[1])