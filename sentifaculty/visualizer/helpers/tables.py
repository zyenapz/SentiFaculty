import django_tables2 as tables
from feedback.models import Feedback

class FeedbackTable(tables.Table):
    class Meta:
        model = Feedback
        # fields = ("name", )