from math import log


class Bm25:
    def __init__(self, docs, tokenizer):
        self._doc_list = docs
        self._tokenizer = tokenizer
        self._vocab = {}

    def _calc_bow(self, token_list):
        # 하나의 문서 안에서 단어의 등장 횟수와 문서의 길이 계산
        doc_dict = {}
        doc_dict["fl"] = len(token_list)  # field length
        doc_dict["nwid"] = {}  # number of word in doc

        for token in token_list:
            if token in doc_dict["nwid"]:
                doc_dict["nwid"][token] += 1
            else:
                doc_dict["nwid"][token] = 1

        return doc_dict

    def _get_materials(self):
        # idf와 tf를 구하기 위한 변수 계산
        materials = {}
        materials["docCount"] = len(self._doc_list)
        materials["avgFieldLength"] = 0
        materials["docsFreq"] = {}
        materials["docs"] = []

        for doc in self._doc_list:
            tokenized_doc = self._tokenizer(doc)
            doc_dict = self._calc_bow(tokenized_doc)
            materials["avgFieldLength"] += doc_dict["fl"]
            materials["docs"].append(doc_dict)
            for token in doc_dict["nwid"].keys():
                if token in materials["docsFreq"].keys():
                    materials["docsFreq"][token] += 1
                else:
                    materials["docsFreq"][token] = 1
                    self._vocab[token] = len(self._vocab.keys())
        materials["avgFieldLength"] /= materials["docCount"]
        return materials

    def _idf(self, doc_freq, doc_count):
        return log(1 + (doc_count - doc_freq + 0.5) / (doc_freq + 0.5))

    def _tfnorm(self, term_freq, avg_field_len, field_len, k1, b):
        return (term_freq * (k1 + 1)) / (term_freq + k1 * (1 - b + b * field_len / avg_field_len))

    def _calc_bm25(self, doc_freq, doc_count, term_freq, avg_field_len, field_len, k1, b):
        return self._idf(doc_freq, doc_count) * self._tfnorm(term_freq, avg_field_len, field_len, k1=k1, b=b)

    def transform(self, k1=1.2, b=0.75):
        bm25_vec_list = []
        _doc_idx = 0
        _materials = self._get_materials()
        for elem in _materials["docs"]:
            preprocessed_doc = elem["nwid"]
            bm25_vec = [0] * len(self._vocab.keys())
            for token in preprocessed_doc:
                doc_freq = _materials["docsFreq"][token]
                doc_count = _materials["docCount"]
                term_freq = _materials["docs"][_doc_idx]["nwid"][token]
                avg_field_len = _materials["avgFieldLength"]
                field_len = _materials["docs"][_doc_idx]["fl"]
                result = self._calc_bm25(doc_freq, doc_count, term_freq, avg_field_len, field_len, k1, b)
                bm25_vec[self._vocab[token]] = result
            bm25_vec_list.append(bm25_vec)
            _doc_idx += 1
        return bm25_vec_list

    def get_result(self, k1=1.2, b=0.75):
        calc_bm25_list = []
        _doc_idx = 0
        _materials = self._get_materials()
        for elem in _materials["docs"]:
            bm25_dict = {}
            preprocessed_doc = elem["nwid"]
            for token in preprocessed_doc:
                doc_freq = _materials["docsFreq"][token]
                doc_count = _materials["docCount"]
                term_freq = _materials["docs"][_doc_idx]["nwid"][token]
                avg_field_len = _materials["avgFieldLength"]
                field_len = _materials["docs"][_doc_idx]["fl"]
                result = self._calc_bm25(doc_freq, doc_count, term_freq, avg_field_len, field_len, k1, b)
                bm25_dict[token] = result
            calc_bm25_list.append(bm25_dict)
            _doc_idx += 1
        return calc_bm25_list
