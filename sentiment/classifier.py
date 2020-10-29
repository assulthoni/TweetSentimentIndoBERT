import os
from django.conf import settings

import torch
import torch.nn.functional as F
import pandas as pd

from transformers import BertForSequenceClassification, BertConfig
from transformers import BertTokenizer

class Classifier():
    
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('indobenchmark/indobert-base-p1')
        config = BertConfig.from_pretrained("indobenchmark/indobert-base-p1", num_labels=3)
        self.model = BertForSequenceClassification.from_pretrained("indobenchmark/indobert-base-p1", config=config)
        self.model.load_state_dict(torch.load(os.path.join(settings.BASE_DIR,"sentiment/model.bin")))
        self.results = list()

    def predict(self,tweet):
        i2w = {0: 'positive', 1: 'neutral', 2: 'negative'}
        subwords = self.tokenizer.encode(tweet)
        subwords = torch.LongTensor(subwords).view(1,-1).to(self.model.device)

        logits = self.model(subwords)[0]
        label = torch.topk(logits, k=1, dim=-1)[1].squeeze().item()

        return i2w[label] , str(f'{F.softmax(logits, dim=-1).squeeze()[label] * 100:.2f}')
    
    def process_tweets(self,tweets):
        for tweet in tweets:
            result = dict()
            label , conf = self.predict(tweet=tweet)
            print(f"Success Predict {label}, {conf}")
            result['tweet'] = tweet
            result['label'] = label
            result['conf'] = conf
            self.results.append(result)
        # print(self.results)
    
    def export(self):
        return self.results
    def reset(self):
        self.results = list()