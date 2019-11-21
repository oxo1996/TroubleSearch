from dlmodel.iDetectReview import iDetectReview
from dlmodel.embedding.sktkobert import SktKobert
from dlmodel.feature_extract.bm25 import Bm25
from dlmodel.utils import cosine_similarity


class BertBm25(iDetectReview):
    def __init__(self):
        self._model = SktKobert()

    def _calc_weighted_vec(self, tokenized_doc, bm25_doc, encoded_doc):
        vec = [0] * len(encoded_doc[0])
        _token_idx = 0
        for token in tokenized_doc:
            vec += bm25_doc[token] * encoded_doc[_token_idx]
            _token_idx += 1
        vec /= len(tokenized_doc)
        return vec

    def _calc_vec(self, docs):
        _bm25_list = Bm25(docs, self._model.get_tokenizer()).get_result()
        # print(_bm25_list)
        vec_list = []
        _doc_idx = -1

        for doc in docs:
            _doc_idx += 1
            try:
                tokenized_doc, all_encoder_layers, pooled_output = self._model.get_embedding(doc)
            except RuntimeError as e:
                print(e)
                continue
            _encoded_doc = all_encoder_layers[-1][0].detach().numpy()
            _doc_vec = self._calc_weighted_vec(tokenized_doc, _bm25_list[_doc_idx], _encoded_doc)
            vec_list.append([_doc_idx, _doc_vec])
        return vec_list

    def most_similar(self, source: str, targets, num: int, order=True):
        targets.append(source)  # 마지막에 증상을 붙힘
        _vec_list = self._calc_vec(targets)
        similarities = []
        for vec in _vec_list[:-1]:
            sim = cosine_similarity(_vec_list[-1][1], vec[1])  # _vec_list[-1][1]: source
            similarities.append([vec[0], sim])
        similarities.sort(key=lambda x: x[1], reverse=order)
        return similarities[:num]

    def test_most_similar(self, source: str, targets, num: int, order=True):
        return 0