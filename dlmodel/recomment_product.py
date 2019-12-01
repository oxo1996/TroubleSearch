from dlmodel.embedding.iembedding import iEmbedding
import numpy as np
import json


class RecommentProduct:
    def __init__(self, input_embedding: iEmbedding):
        self._embedding = input_embedding
        self._items = self._read_file("webcrawler/items.json")
        self._ingr_ko2eng = self._read_file("webcrawler/ingrKo2Eng.json")

    @staticmethod
    def _read_file(path):
        with open(path) as data_file:
            items = json.load(data_file)
        return items

    @staticmethod
    def _norm_sim(similarity, var):
        return np.exp(-(similarity ** 2) / (2 * var))

    def _weights(self, real_sims):
        w = []
        # print(real_sims)
        _variance = np.var(real_sims)
        # print(_variance)
        for sim in real_sims:
            w.append(self._norm_sim(sim, _variance))
        # print(w)
        return w

    @staticmethod
    def _get_real_sims(similarities):
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
        for pname in self._items.keys():
            if len(self._items[pname]["ingredients"]) < 2:
                print("not exist ingredients data")
                continue
            eng_name_list = []
            for ko_name in self._items[pname]["ingredients"]:
                try:
                    eng_name = self._ingr_ko2eng[ko_name]
                    eng_name_list.append(eng_name)
                except KeyError as e:
                    continue

            similarities = self._embedding.most_similar(symptom, eng_name_list, len(eng_name_list))
            tot_sim = self._product_tot_sim(similarities)
            # print(pname, tot_sim)
            vec_list.append((pname, tot_sim))

        vec_list = sorted(vec_list, key=(lambda x: x[1]), reverse=False)
        return vec_list

    def get_result(self, symptom, products):
        print("get_result 실행: ", symptom, products)
        # products는 str의 list
        _topn = 3
        vec_dict = {}
        _symtom_vec = self._embedding.calc_vec([symptom], 300, 0)

        for pname in products:
            if len(self._items[pname]["ingredients"]) < 2:
                print("not exist ingredients data")
                continue
            vec_dict[pname] = {}

            eng_name_list = []
            eng2ko = {}
            for ko_name in self._items[pname]["ingredients"]:
                try:
                    print(ko_name)
                    eng_name = self._ingr_ko2eng[ko_name]
                    print(eng_name)
                    eng_name_list.append(eng_name)
                    eng2ko[eng_name] = ko_name
                except KeyError as e:
                    continue

            similarities = self._embedding.most_similar(symptom, eng_name_list, _topn)
            result_vec = {}
            for sim in similarities:
                eng_name = eng_name_list[sim[0]]
                ko_name = eng2ko[eng_name]
                result_vec[ko_name] = sim[1]

            vec_dict[pname]["ingr"] = result_vec
            vec_dict[pname]["sim"] = self._product_tot_sim(similarities)

        vec_dict = sorted(vec_dict.items(), key=(lambda x: x[1]["sim"]), reverse=True)
        print("result: ", vec_dict)

        return vec_dict
