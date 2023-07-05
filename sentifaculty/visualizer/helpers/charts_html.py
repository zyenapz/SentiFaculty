import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from feedback.models import Feedback
from wordcloud import STOPWORDS, WordCloud
from feedback.models import Feedback
from sentifaculty.corpus.corpus_reader import get_corpus_polarities
from visualizer.models import AcademicYear, FacultyEvaluation
from users.models import Teacher


class SF_SentipieHTML:
    def __new__(self, request, user_id, faculty_eval):
        data = Feedback.objects.filter(
            evaluatee__teacher__user__id=user_id, evaluatee__fe=faculty_eval)
        section = request.GET.get('subject')

        # if section:
        #     data = Feedback.objects.filter(evaluatee__subject__id=section)

        # Count number of positive and negative sentiments
        positives = [
            fb for fb in data if fb.comment.sentiment_score.get_sentiment_as_str() == "positive"]
        negatives = [
            fb for fb in data if fb.comment.sentiment_score.get_sentiment_as_str() == "negative"]

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

        data = Feedback.objects.filter(
            evaluatee__teacher__user__id=user_id, evaluatee__fe=faculty_eval)
        words = ' '.join([str(entry.comment) for entry in data])
        corpus = get_corpus_polarities()

        positive_words = set([word for word in corpus.keys() if float(
            corpus[word]) > 0.0]) & set(words.split(' '))
        negative_words = set([word for word in corpus.keys() if float(
            corpus[word]) < 0.0]) & set(words.split(' '))

        positive_words = ' '.join(word for word in list(positive_words))
        negative_words = ' '.join(word for word in list(negative_words))

        clouds = dict()
        try:
            positive_cloud = WordCloud(
                stopwords=None,
                background_color="black",
                width=200,
                height=200,
                # color_func=lambda *args, **kwargs: (0,0,255),
                colormap="Greens",
            ).generate(positive_words).to_svg()

            negative_cloud = WordCloud(
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


class SF_OverallWordcloudHTML:
    def __init__(self, faculty_eval=FacultyEvaluation.objects.filter(is_ongoing=True).first()):
        data = Feedback.objects.filter(evaluatee__fe=faculty_eval)
        if data:
            self.words = ''.join([str(entry.comment) for entry in data])
            self.cloud = WordCloud(stopwords=STOPWORDS).generate(
                self.words).to_svg()
        else:
            #just return an empty list, janky but works
            self.cloud = []


class SF_OverallLinegraphHTML:
    def __init__(self):
        teachers = Teacher.objects.all()
        queryYears = AcademicYear.objects.all().order_by('start_year')
        self.yearsList = [str(year) for year in queryYears]
        self.ratings = {}
        for teacher in teachers:
            sentimentRating = []
            for year in queryYears:
                positives = len(Feedback.objects.filter(evaluatee__fe__academic_year=year.start_year).filter(
                    comment__sentiment_score__hybrid_pos__gt=0.00).filter(evaluatee__teacher__user__mcl_id=teacher.user.mcl_id))
                negatives = len(Feedback.objects.filter(evaluatee__fe__academic_year=year.start_year).filter(
                    comment__sentiment_score__hybrid_neg__gt=0.00).filter(evaluatee__teacher__user__mcl_id=teacher.user.mcl_id))
                if positives > negatives:
                    sentimentRating.append(2)
                elif positives < negatives:
                    sentimentRating.append(0)
                elif positives > 0 and negatives > 0 and positives == negatives:
                    sentimentRating.append(1)
                else:
                    sentimentRating.append(None)
            self.ratings[str(teacher)] = sentimentRating
        self.fig = go.Figure()
        for entry in self.ratings:
            self.fig.add_trace(go.Scatter(
                x=self.yearsList, y=self.ratings[entry], name=entry))
        self.fig.update_layout(title=go.layout.Title(text='Faculty sentiment per school year<br><sup>Comment majority determines sentiment rating</sup>'),
                               yaxis_dtick=1, yaxis_tickvals=[0, 1, 2],
                               yaxis_ticktext=['Negative', 'Neutral', 'Positive'], yaxis_range=[0, 2])
        self.chart = self.fig.to_html()
