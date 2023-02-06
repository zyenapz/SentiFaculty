import plotly.express as px
import pandas as pd
from feedback.models import Feedback
from wordcloud import STOPWORDS, WordCloud
from feedback.models import Feedback

class SF_SentipieHTML:
    def __new__(self, request):
        user_id = request.user.id

        data = Feedback.objects.filter(evaluatee__teacher__user__id=user_id)
        section = request.GET.get('subject')

        if section:
            data = Feedback.objects.filter(evaluatee__subject__id=section)

        fig = px.pie(
            values=[
                len(data.filter(comment__sentiment_score__hybrid_pos__gt=0.00)),
                len(data.filter(comment__sentiment_score__hybrid_neg__gt=0.00)),
            ],
            names=['positive', 'negative'],
            title='Sentiment Rating',
            color=['positive', 'negative'],
            color_discrete_map={
                'positive': 'green',
                'negative': 'red',
            },
        )

        chart = fig.to_html()

        return chart

class SF_WordcloudHTML:
    def __new__(self, request):
        user_id = request.user.id
        
        data = Feedback.objects.filter(evaluatee__teacher__user__id=user_id)
        words=''.join([str(entry.comment) for entry in data])

        cloud=WordCloud(
            stopwords=STOPWORDS, 
            background_color=None,
            width=200,
            height=200,
        ).generate(words).to_svg()

        return cloud

