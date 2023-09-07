import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
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
            self.words = ' '.join([str(entry.comment) for entry in data])
            self.cloud = WordCloud(stopwords=STOPWORDS).generate(
                self.words).to_svg()
        else:
            # just return an empty list, janky but works
            self.cloud = []


class SF_OverallLinegraphHTML:
    def __init__(self):
        teachers = Teacher.objects.all()
        # get total feedbacks to determine length of list
        totalFeedbacks = Feedback.objects.all()
        self.feedbackDates = [
            feedback.submit_date for feedback in totalFeedbacks]
        self.ratings = {}
        for teacher in teachers:
            sentimentScores = []
            feedbacks = Feedback.objects.filter(
                evaluatee__teacher__user__mcl_id=teacher.user.mcl_id)
            for tf in totalFeedbacks:
                checked = False
                for entry in feedbacks:
                    if tf.id == entry.id:
                        sentimentScores.append(
                            entry.comment.sentiment_score.hybrid_pos - entry.comment.sentiment_score.hybrid_neg)
                        checked = True
                        break
                if checked:
                    continue
                else:
                    sentimentScores.append(None)
            self.ratings[str(teacher)] = sentimentScores
        self.fig = go.Figure()
        for entry in self.ratings:
            self.fig.add_trace(go.Scatter(
                x=self.feedbackDates, y=self.ratings[entry], name=entry, mode='markers'))
        self.fig.update_layout(title=go.layout.Title(text='Faculty feedback and scores <br><sup>Values closer to 1 skew positive while values closer to -1 skew negative</sup>'),
                               yaxis_dtick=1, yaxis_tickvals=[-1, 0, 1],
                               yaxis_ticktext=['Negative', 'Neutral', 'Positive'], yaxis_range=[-1, 1],
                               margin=dict(pad=20),
                               )
        self.fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")
        self.chart = self.fig.to_html()
