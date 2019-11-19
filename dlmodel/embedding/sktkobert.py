import torch
from kobert.pytorch_kobert import get_pytorch_kobert_model
from gluonnlp.data import SentencepieceTokenizer
from kobert.utils import get_tokenizer


class SktKobert:
    def __init__(self):
        self._model, self.vocab = get_pytorch_kobert_model()
        self.tokenizer = SentencepieceTokenizer(get_tokenizer())

    def get_tokenizer(self):
        return self.tokenizer

    def get_embedding(self, text: str):
        tokenized_text = self.tokenizer(text)
        _indexed_tokens = self.vocab(tokenized_text)
        _input_ids = torch.LongTensor([_indexed_tokens])
        all_encoder_layers, pooled_output = self._model(_input_ids)
        return tokenized_text, all_encoder_layers, pooled_output
