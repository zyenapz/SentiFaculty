from feedback.models import Evaluatee, Evaluator, Feedback
from feedback.helpers.analyzer import SFAnalyzer
from feedback.models import SentimentScore
from visualizer.models import FacultyEvaluation

from django.db import IntegrityError, transaction

class FeedbackProcessor:
    def __init__(self, request, form, evaluatee):
        # Save evaluatee
        self.evaluatee = evaluatee

        # Process comment
        self.comment = form.save(commit=False)
        self.score = self._get_score(self.comment.text)
        self.comment.sentiment_score = self.score

        # Process evaluator
        self.student = request.user.student
        self.evaluator = Evaluator(
            section=self.student.section,
            strand=self.student.strand,
            year_level=self.student.year_level,
            fe=FacultyEvaluation.objects.first(), # TODO dummy data
            student=self.student,
        )
        
        # Process feedback
        self.feedback = Feedback(
            evaluatee=self.evaluatee,
            evaluator=self.evaluator,
            comment=self.comment,
        )

    def _get_score(self, text):
        # Calculate Vader, BERT and hybrid scores
        analyzer = SFAnalyzer()
        vader = analyzer.use_vader(text)
        bert = analyzer.use_bert(text)
        hybrid = analyzer.use_hybrid(text)

        score = SentimentScore(
            vader_pos = vader.pos,
            vader_neg = vader.neg,
            bert_pos = bert.pos,
            bert_neg = bert.neg,
            hybrid_pos = hybrid.pos,
            hybrid_neg = hybrid.neg,
        )

        return score
    
    def save(self):
        # Save transaction
        try:
            with transaction.atomic():
                self.score.save()
                self.comment.save()
                self.evaluator.save()
                self.feedback.save()
        except IntegrityError as e:
            raise IntegrityError(e)