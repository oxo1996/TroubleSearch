from embedding.iembedding import iEmbedding


class DetectReview:
    def __init__(self, input_embedding: iEmbedding):
        self._embedding = input_embedding

    def get_similar_review(self, source: str, targets, num: int, order=True):
        result = self._embedding.most_similar(source, targets, num, order=True)
        return result
