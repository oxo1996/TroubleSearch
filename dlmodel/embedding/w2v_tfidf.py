from dlmodel.iRecomProduct import iRecomProduct
import json
import math
import numpy as np
from dlmodel.utils import cosine_similarity


class W2vTfidf(iRecomProduct):
    def __init__(self, word2vecPath: str, modelPath: str):
        self._w2v_path = word2vecPath  # 현재 특정 증상에 관한 벡터만 받아옴. 보완해야 함.
        self._mpath = modelPath
        self._w2v = self._load_w2v()
        self._ingr_w2v = self._load_model()
        self._ingr_ko2eng = self._load_ingr_ko2eng()
        self._items = self._load_items()

    def _load_w2v(self):
        with open(self._w2v_path) as data_file:
            w2v = json.load(data_file)
        return w2v

    def _load_model(self):
        with open(self._mpath) as data_file:
            ingrW2v = json.load(data_file)
        return ingrW2v

    def _load_ingr_ko2eng(self):
        with open("webcrawler/ingrKo2Eng.json") as data_file:
            ingrKo2Eng = json.load(data_file)
        return ingrKo2Eng

    def _load_items(self):
        with open("webcrawler/items.json") as data_file:
            items = json.load(data_file)
        return items

    def most_similar(self, symptom, product, topn: int, order=True):
        _calc_cs = {}
        _koIngrList = self._items[product]["ingredients"]
        _symptomVec = self._w2v[symptom]

        for koName in _koIngrList:
            try:
                engName = self._ingr_ko2eng[koName]
                iwv = self._ingr_w2v[engName]
                _calc_cs[koName] = cosine_similarity(iwv, _symptomVec)
                # _calc_cs[engName] = self._cosine_similarity(iwv, _symptomVec)
            except KeyError as e:
                # print(e)
                continue

        res = sorted(_calc_cs.items(), key=(lambda x: x[1]), reverse=order)
        return res[:topn]

    def _norm_sim(self, similarity, var):
        return np.exp(-(similarity ** 2) / (2 * var))

    def _weights(self, real_sims):
        w = []
        _varience = np.var(real_sims)
        for sim in real_sims:
            w.append(self._norm_sim(sim, _varience))
        return w

    def _get_real_sims(self, similarities):
        real_sims = []
        for sim in similarities:
            real_sims.append(sim[1])
        return real_sims

    def _product_tot_sim(self, similarities):
        _real_sims = self._get_real_sims(similarities)
        _w = self._weights(_real_sims)
        return np.dot(_w, _real_sims)

    def recommend_product(self, symptom):
        vec_list = []
        _symtom_vec = self._w2v[symptom]

        for pname in self._items.keys():
            if len(self._items[pname]["ingredients"]) < 2:
                # print("not exist ingredients data")
                continue
            similarities = self.most_similar(symptom, pname, len(self._items[pname]["ingredients"]))
            tot_sim = self._product_tot_sim(similarities)
            # print(pname, tot_sim)
            vec_list.append((pname, tot_sim))

        vec_list = sorted(vec_list, key=(lambda x: x[1]), reverse=False)
        return vec_list

    def get_result(self, symptom, products):
        # products는 str의 list
        _topn = 3
        vec_dict = {}
        _symtom_vec = self._w2v[symptom]

        for pname in products:
            if len(self._items[pname]["ingredients"]) < 2:
                # print("not exist ingredients data")
                continue
            vec_dict[pname] = {}
            similarity = self.most_similar(symptom, pname, _topn)
            vec_dict[pname]["ingr"] = similarity
            vec_dict[pname]["sim"] = self._product_tot_sim(similarity)

        vec_dict = sorted(vec_dict.items(), key=(lambda x: x[1]["sim"]), reverse=True)
        # print(vec_dict)

        return vec_dict
