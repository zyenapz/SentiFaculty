from django.test import TestCase
from django import setup

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sentifaculty.settings")
setup()

# Create your tests here.
from feedback.models import SentimentScore

class SentimentScoreTestCase(TestCase):
    def test_score_exists(self):
        scores = SentimentScore.objects.all()
        self.assertTrue(scores.exists())
