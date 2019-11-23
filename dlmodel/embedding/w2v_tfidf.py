from embedding.iembedding import iEmbedding
import json
import math
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import cosine_similarity


class W2vTfidf(iEmbedding):
    def __init__(self):
        # 현재 특정 증상에 관한 벡터만 받아옴. 보완해야 함.
        self._w2v = self._read_file("embedding/temp_w2v.json")
        # self._ingr_w2v = self._load_model()
        # self._ingr_ko2eng = self._load_ingr_ko2eng()
        # self._items = self._load_items()

    @staticmethod
    def _read_file(path):
        with open(path) as data_file:
            w2v = json.load(data_file)
        return w2v

    @staticmethod
    def _preprocess(input_str):
        text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》;0-9\—\–\{\}â®€“¶ï¬ã¼™]', '', input_str)
        short_word = re.compile(r'\W*\b\w{1,2}\b')  # 1,2 글자 수 삭제
        text = short_word.sub('', text)
        text = text.lower()

        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)

        clean_word_set = []
        for w in word_tokens:
            if w not in stop_words:
                clean_word_set.append(w)

        result = ''
        for word in clean_word_set:
            result = result + word + ' '

        return result.rstrip()

    def _tfidf(self, input_desc):
        input_data = []
        return_data = {}
        for name in input_desc.keys():
            desc = input_desc[name]
            desc = self.preprocess(desc)
            input_data.append(desc)
            return_data[name] = desc
        tfidfv = TfidfVectorizer().fit(input_data)
        return return_data, tfidfv.transform(input_data).toarray(), tfidfv.vocabulary_

    def _calc_vec(self, ingr_desc, dim):
        """
        범용적으로 벡터를 계산함.
        """
        result = {}
        docs, vec, vocab = self._tfidf(ingr_desc)
        doc_i = 0
        for name in docs.keys():
            doc = docs[name]
            word_tokens = word_tokenize(doc)
            num_word = 0
            avgw2v = [0] * dim
            for word in word_tokens:
                num_word += 1
                try:
                    v = self._w2v[word]
                except KeyError as e:
                    v = np.asarray([0] * dim)
                # w 예외 처리 다시 볼 것
                try:
                    w = vec[doc_i][vocab[word]]
                except KeyError as e:
                    print(e)
                    w = np.asarray([0] * dim)
                avgw2v += v * w
            avgw2v = avgw2v / num_word
            result[name] = avgw2v
            doc_i += 1
        return result

    def _calc_vec_temp(self, keys):
        """
        word2vec을 못 불러와서 임시용으로 만듬
        """
        vec_list = []
        idx = -1
        for key in keys:
            idx += 1
            try:
                vec_list.append([idx, self._w2v[key]])
            except KeyError as e:
                print("not found ingr vec in temp_w2v")
        return vec_list

    def calc_vec(self, docs, dim, type):
        """
        현재는 키값으로 받아옴.
        나중에 string으로 받아서 할 예정
        0일 때, 임시용이고
        1일 때, string을 입력받음
        """
        if type is 0:
            result = self._calc_vec_temp(docs)
        elif type is 1:
            result = self._calc_vec(docs, dim)
        else:
            raise Exception("non type calc_vec")
        return result

    def most_similar(self, source: str, targets, num: int, splitter="sent", order=True):
        """
        범용적인 most_similar 함수를 일단 만들었음.
        현재 targets가 키값이지만 후에 string으로 바꿀 예정
        doc를 기준으로 벡터화함
        """
        source_vec = self.calc_vec([source], 300, 0)
        similarities = []

        target_vec_list = self.calc_vec(targets, 300, 0)
        for target_vec in target_vec_list:
            sim = cosine_similarity(source_vec[0][1], target_vec[1])
            similarities.append([target_vec[0], sim])
        similarities.sort(key=lambda x: x[1], reverse=order)
        return similarities[:num]
