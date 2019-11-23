from feature_extract.bm25 import Bm25
from embedding.sktkobert import SktKobert
from utils import cosine_similarity
from embedding.bert_bm25 import BertBm25
from detect_review import DetectReview
from embedding.w2v_tfidf import W2vTfidf
from recomment_product import RecommentProduct
import json
from konlpy.tag import Kkma

if __name__ == '__main__':
    # f = open("review_test.txt", 'r')
    # reviews = f.readlines()
    # print(reviews)

    '''with open("C:\dev\django\djangoproject\webcrawler\items.json") as json_file:
        items = json.load(json_file)

    raw_reviews = items["오가니언스 에멀젼"]["reviews"]
    reviews = []
    for review in raw_reviews:
        reviews.append(review[1])
    reviews.append("이거 쓰고 부터 여드름이 더 나는것 같네요...향이 너무 진해요.")
    reviews.append("사용후부터 여드름이 더 생긴 것 같아요")

    bertbm25 = BertBm25()
    dr = DetectReview(bertbm25)
    result = dr.get_similar_review("트러블.", reviews, 1000)
    print(result)
    for elem in result:
        print(reviews[elem[0]], elem[1])'''

    # bertbm25 = BertBm25()
    # kkma = Kkma()
    # test = "아홉살23ㄹsfd233이다. 못된 녀석이다. 이 놈아ㅋfsfAㅋㄹㅇFㄴㄹ ㄹㅇ마"
    # result = bertbm25._preprocess(test)
    # result = kkma.sentences(result)
    # print(result)

    with open("C:\dev\django\djangoproject\webcrawler\items.json") as json_file:
        items = json.load(json_file)
    w2vtfidf = W2vTfidf()
    recom = RecommentProduct(w2vtfidf)
    result = recom.recommend_product("allergy")
    print(result)