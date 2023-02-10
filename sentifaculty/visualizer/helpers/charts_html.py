import plotly.express as px
import pandas as pd
from feedback.models import Feedback
from wordcloud import STOPWORDS, WordCloud
from feedback.models import Feedback
from sentifaculty.corpus.corpus_reader import get_corpus_polarities

class SF_SentipieHTML:
    def __new__(self, request, user_id, faculty_eval):
        data = Feedback.objects.filter(evaluatee__teacher__user__id=user_id, evaluatee__fe=faculty_eval)
        section = request.GET.get('subject')

        # if section:
        #     data = Feedback.objects.filter(evaluatee__subject__id=section)

        # Count number of positive and negative sentiments
        positives = [fb for fb in data if fb.comment.sentiment_score.get_sentiment_as_str() == "positive"]
        negatives = [fb for fb in data if fb.comment.sentiment_score.get_sentiment_as_str() == "negative"]
        
        fig = px.pie(
            values=[
                len(positives),
                len(negatives),
            ],
            names=['positive', 'negative'],
            title='Sentiment Rating',
            color=['positive', 'negative'],
            color_discrete_map={
                'positive': '#1b2c53',
                'negative': '#ec1f28',
            },
        )

        chart = fig.to_html()

        return chart

class SF_WordcloudHTML:
    
    def __new__(self, user_id, faculty_eval):
        
        data = Feedback.objects.filter(evaluatee__teacher__user__id=user_id, evaluatee__fe=faculty_eval)
        words=' '.join([str(entry.comment) for entry in data])
        corpus = get_corpus_polarities()

        positive_words = set([word for word in corpus.keys() if float(corpus[word]) > 0.0]) & set(words.split(' '))
        negative_words = set([word for word in corpus.keys() if float(corpus[word]) < 0.0]) & set(words.split(' '))

        positive_words = ' '.join(word for word in list(positive_words))
        negative_words = ' '.join(word for word in list(negative_words))

        clouds = dict()
        try:
            positive_cloud=WordCloud(
                stopwords=None, 
                background_color="black",
                width=200,
                height=200,
                # color_func=lambda *args, **kwargs: (0,0,255),
                colormap="Greens",
            ).generate(positive_words).to_svg()

            negative_cloud=WordCloud(
                stopwords=None, 
                background_color="black",
                width=200,
                height=200,
                # color_func=lambda *args, **kwargs: (255,0,0),
                colormap="Reds",
            ).generate(negative_words).to_svg()

            clouds["positive"] = positive_cloud
            clouds["negative"] = negative_cloud
        except:
            return None
        
        return clouds

