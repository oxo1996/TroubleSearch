from dlmodel.embedding.iembedding import iEmbedding
from dlmodel.embedding.sktkobert import SktKobert
from dlmodel.feature_extract.bm25 import Bm25
from dlmodel.utils import cosine_similarity
from konlpy.tag import Kkma
import json
import re
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer


class BertBm25(iEmbedding):
    def __init__(self):
        self._model = SktKobert()
        self._sent_splitter = Kkma()

    def _read_stopwords(self):
        with open("dlmodel/embedding/ko_stopwords.json") as json_file:
            json_data = json.load(json_file)
        return json_data

    def _preprocess(self, input_str: str):
        read_hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        input_str = read_hangul.sub('', input_str)
        input_str = re.sub("[ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉㅏㅑㅓㅕㅜㅠㅡㅣㅢㅟㅘㅄㄶ]", '', input_str)
        stop_words = self._read_stopwords()
        word_tokens = word_tokenize(input_str)
        preprocess_str = []
        for w in word_tokens:
            if w not in stop_words:
                preprocess_str.append(w)
        result = TreebankWordDetokenizer().detokenize(preprocess_str)
        return result

    def _calc_weighted_vec(self, tokenized_doc, bm25_doc, encoded_doc):
        vec = [0] * len(encoded_doc[0])
        _token_idx = 0
        for token in tokenized_doc:
            vec += bm25_doc[token] * encoded_doc[_token_idx]
            _token_idx += 1
        vec /= len(tokenized_doc)
        return vec

    def calc_vec(self, docs):
        _bm25_list = Bm25(docs, self._model.get_tokenizer()).get_result()
        # print(_bm25_list)
        vec_list = []
        _doc_idx = -1

        for doc in docs:
            _doc_idx += 1
            # doc = self._preprocess(doc)
            print(doc)
            try:
                tokenized_doc, all_encoder_layers, pooled_output = self._model.get_embedding(doc)
            except RuntimeError as e:
                print(e)
                continue
            _encoded_doc = all_encoder_layers[-1][0].detach().numpy()
            _doc_vec = self._calc_weighted_vec(tokenized_doc, _bm25_list[_doc_idx], _encoded_doc)
            vec_list.append([_doc_idx, _doc_vec])
        return vec_list

    def _most_similar_doc(self, source: str, targets, num: int, order=True):
        targets.append(source)  # 마지막에 증상을 붙힘
        _vec_list = self._calc_vec(targets)
        similarities = []
        for vec in _vec_list[:-1]:
            sim = cosine_similarity(_vec_list[-1][1], vec[1])  # _vec_list[-1][1]: source
            similarities.append([vec[0], sim])
        similarities.sort(key=lambda x: x[1], reverse=order)
        return similarities[:num]

    def _most_similar_sent(self, source: str, targets, num: int, order=True):
        source_vec = self.calc_vec([source])
        similarities = []
        idx = 0
        for target in targets:
            target = self._preprocess(target)
            max_sim = -1
            lines = self._sent_splitter.sentences(target)
            for line in lines:
                if len(line) is 0:
                    continue
                line_vec = self.calc_vec([line])
                # print("lv: ", line_vec[-1][1])
                # print("sv: ", source_vec[-1][1])
                sim = cosine_similarity(source_vec[0][1], line_vec[0][1])
                max_sim = max(max_sim, sim)
            # print(max_sim)
            similarities.append([idx, max_sim])
            idx += 1
        similarities.sort(key=lambda x: x[1], reverse=order)
        return similarities[:num]

    def most_similar(self, source: str, targets, num: int, splitter="sent", order=True):
        if splitter == "sent":
            result = self._most_similar_sent(source, targets, num, order)
        elif splitter == "doc":
            result = self._most_similar_doc(source, targets, num, order)
        else:
            raise Exception("not exist similar type")
        return result
