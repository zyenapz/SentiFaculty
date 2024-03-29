from pysentimiento import create_analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from feedback.models import SentimentScore

class Sentiment:
    def __init__(self, pos, neg):
        self.pos = pos
        self.neg = neg

class SFAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self.bert = create_analyzer(task="sentiment", lang="en")

    def use_vader(self, comment) -> Sentiment:
        cleaned = self._preprocess(comment)
        results = self.vader.polarity_scores(cleaned) 

        return Sentiment(results['pos'], results['neg'])

    def use_bert(self, comment) -> Sentiment:
        cleaned = self._preprocess(comment)
        results = self.bert.predict(cleaned).probas

        return Sentiment(results['POS'], results['NEG'])

    def use_hybrid(self, comment) -> Sentiment:
        vader = self.use_vader(comment)
        bert = self.use_bert(comment)

        hybrid_neg = (vader.neg + bert.neg) / 2
        hybrid_pos = (vader.pos + bert.pos) / 2

        #hybrid_all = hybrid_pos - hybrid_neg

        return Sentiment(hybrid_pos, hybrid_neg)

    def _preprocess(self, comment):
        # TODO
        # 1. Translate tagalog words into english
        # 2. Remove punctuations
        # 3. Remove urls
        # 4. Remove stop words

        # NOTE: Delegate the preprocessing job to SFTextCleaner class

        # See https://github.com/pysentimiento/pysentimiento
        # In the pre-processing section
        return comment 

