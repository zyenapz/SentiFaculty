from pysentimiento import create_analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SFAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self.bert = create_analyzer(task="sentiment", lang="en")

    def use_vader(self, comment):
        cleaned = self._preprocess(comment)
        return self.vader.polarity_scores(cleaned) 

    def use_bert(self, comment):
        cleaned = self._preprocess(comment)
        return self.bert.predict(cleaned) 

    def use_hybrid(self, comment):
        vader = self.use_vader(comment)
        bert = self.use_bert(comment).probas

        hybrid_neg = (vader['neg'] + bert['NEG']) / 2
        hybrid_pos = (vader['pos'] + bert['POS']) / 2

        hybrid_all = hybrid_pos - hybrid_neg

        return hybrid_all

    def _preprocess(self, comment):
        # TODO
        # See https://github.com/pysentimiento/pysentimiento
        # In the pre-processing section
        return comment 