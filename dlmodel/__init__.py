#from dlmodel import dlmodel
from .iRecomProduct import iRecomProduct
from .iDetectReview import iDetectReview
from .avgtfw2v import avgtfw2v
from .sktkobert import sktkobert
import torch
from .KoBERT.kobert.pytorch_kobert import get_pytorch_kobert_model
from gluonnlp.data import SentencepieceTokenizer
from .KoBERT.kobert.utils import get_tokenizer
import numpy as np
import math
from .bm25 import bm25
from .bert_bm25 import bert_bm25

import json

if __name__ == '__main__':
    '''iRecomProduct = avgtfw2v("symptom_w2v.json", "avgw2v_model.json")
    print(iRecomProduct.getResult("allergy", ["크림 스킨", "타임프리즈 에센스 ex", "딥 씨 워터폴 앰플"]))    
    print(iRecomProduct.recommendProduct("allergy")[0][0])'''

    with open("../webcrawler/items.json") as data_file:    
        items = json.load(data_file)

    reviewdata = items["오가니언스 에멀젼"]["reviews"]
    reviews = []
    for review in reviewdata:
        reviews.append(review[1])
    reviews.append("여드름이 났어요.")
    reviews.append("여드름이 더 생긴 것 같아요")
    reviews.append("이거 쓰고 부터 여드름이 더 나는것 같네요...")
    reviews.append("여드름 나요. 쓰지 마세요.")
    reviews.append("이거 때문인지는 모르겠는데, 사용하고 여드름이 더 많아진 것 같네요. 여드름에 민감하시면 거르세요.")
    reviews.append("피지가 많아진 건지, 여드름이 늘은 건지 모르겠네요... 이거 쓰고 부터 인것 같기도?")
    reviews.append("확실하진 않지만 여드름이 늘어났음. 참고하세요.")

    source = "여드름"
    
    test = bert_bm25()
    mostSimList = test.mostSimilar(source, reviews, 20)
    for mostSim in mostSimList:
        idx = mostSim[0]
        print(reviews[idx], mostSim[1])