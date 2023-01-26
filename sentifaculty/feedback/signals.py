from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import Feedback, Comment

@receiver(post_delete, sender=Feedback)
def post_delete_feedback(sender, instance, *args, **kwargs):
    if instance.comment and instance.evaluator:
        instance.comment.delete()
        instance.evaluator.delete()

@receiver(post_delete, sender=Comment)
def post_delete_comment(sender, instance, *args, **kwargs):
    if instance.sentiment_score:
        instance.sentiment_score.delete()