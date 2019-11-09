from iDetectReview import iDetectReview
from sktkobert import sktkobert
from bm25 import bm25
from utils import cosineSimilarity

class bert_bm25(iDetectReview):
    def __init__(self):
        self.model = sktkobert()

    def _calcWeightedVec(self, tokenizedDoc, bm25Doc, encodedDoc):
        vec = [0] * len(encodedDoc[0])
        tokenIdx = 0
        for token in tokenizedDoc:
            vec += bm25Doc[token] * encodedDoc[tokenIdx]
            tokenIdx += 1
        return vec
    
    def calcVec(self, docs):
        bm25List = bm25(docs, self.model.getTokenizer()).getResult()
        #print(bm25List)
        vecList = []
        docIdx = -1

        for doc in docs:
            docIdx += 1
            try:
                tokenizedDoc, all_encoder_layers, pooled_output = self.model.getEmbedding(doc)
            except RuntimeError as e:
                print(e)
                continue
            encodedDoc = all_encoder_layers[-1][0].detach().numpy()
            docVec = self._calcWeightedVec(tokenizedDoc, bm25List[docIdx], encodedDoc)
            vecList.append([docIdx, docVec])
        return vecList

    def mostSimilar(self, source : str, targets, num : int, order = True):
        targets.append(source)  # 마지막에 증상을 붙힘
        vecList = self.calcVec(targets)      
        similarities = []
        for vec in vecList[:-1]:
            sim = cosineSimilarity(vecList[-1][1], vec[1])    # vecList[-1][1]: source
            similarities.append([vec[0], sim])
        similarities.sort(key=lambda x: x[1], reverse = order)
        return similarities[:num]