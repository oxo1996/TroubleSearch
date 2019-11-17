import torch
from .KoBERT.kobert.pytorch_kobert import get_pytorch_kobert_model
from gluonnlp.data import SentencepieceTokenizer
from .KoBERT.kobert.utils import get_tokenizer

class sktkobert:
    def __init__(self):
        self.model, self.vocab  = get_pytorch_kobert_model()
        self.tokenizer = SentencepieceTokenizer(get_tokenizer())

    def getTokenizer(self):
        return self.tokenizer

    def getEmbedding(self, text : str):
        tokenizedText = self.tokenizer(text)
        indexedTokens = self.vocab(tokenizedText)
        input_ids = torch.LongTensor([indexedTokens])
        all_encoder_layers, pooled_output = self.model(input_ids)
        return tokenizedText, all_encoder_layers, pooled_output