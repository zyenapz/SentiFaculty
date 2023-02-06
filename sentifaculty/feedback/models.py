from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _

class SentimentChoice(models.TextChoices):
    POSITIVE = "POSITIVE", _('Positive')
    NEUTRAL = "NEUTRAL", _('Neutral')
    NEGATIVE = "NEGATIVE", _('Negative')

class Feedback(models.Model):
    # Fields
    submit_date = models.DateTimeField(auto_now_add=True)

    # Foreign Keys
    evaluatee = models.ForeignKey('Evaluatee', on_delete=models.CASCADE)
    evaluator = models.OneToOneField('Evaluator', on_delete=models.CASCADE)
    comment = models.OneToOneField('Comment', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.comment.text

    def clean(self) -> str:
        # TODO add validation to ensure that a 'Student' can only submit one entry for every 'Evaluatee'
        pass

class Comment(models.Model):
    # Validators
    validators = [validators.MinLengthValidator(10)]

    # Fields
    text = models.TextField(max_length=100, validators=validators)
    actual_sentiment = models.CharField(
        max_length=10, 
        choices=SentimentChoice.choices, 
        default=SentimentChoice.NEUTRAL,
    ) 

    # Foreign Keys
    sentiment_score = models.OneToOneField('SentimentScore', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.text

class SentimentScore(models.Model):
    # Vars for rounding decimals
    MAX_DIGITS = 4
    MAX_DECIMAL = 2

    # Fields
    vader_pos = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    vader_neg = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    bert_pos = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    bert_neg = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    hybrid_pos = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)
    hybrid_neg = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=MAX_DECIMAL)

    def get_sentiment_as_str(self) -> str:
        hybrid_total = self.hybrid_pos - self.hybrid_neg

        if hybrid_total > 0:
            return "positive"
        if hybrid_total < 0:
            return "negative"
        if hybrid_total == 0:
            return "neutral"

class Evaluatee(models.Model):
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey('visualizer.Subject', on_delete=models.CASCADE)
    fe = models.ForeignKey('visualizer.FacultyEvaluation', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'subject', 'fe'], name="unique_evaluatee")
        ]

    def __str__(self) -> str:
        return f"({self.subject.subject_code}) {self.teacher}"

class Evaluator(models.Model):
    section = models.ForeignKey('visualizer.Section', on_delete=models.CASCADE)
    strand = models.ForeignKey('visualizer.Strand', on_delete=models.CASCADE)
    year_level = models.ForeignKey('visualizer.YearLevel', on_delete=models.CASCADE)
    fe = models.ForeignKey('visualizer.FacultyEvaluation', on_delete=models.CASCADE)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.year_level}-{self.section}-{self.strand}"

    


