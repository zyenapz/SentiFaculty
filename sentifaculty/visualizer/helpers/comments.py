from feedback.models import Feedback
from datetime import date
from datetime import datetime, timedelta


class Comment:
    def __init__(self, text, year_level, strand, section):
        self.text = text
        self.year_level = year_level
        self.strand = strand
        self.section = section

class SF_BestComment:
    def __new__(self, request):
        user_id = request.user.id

        query = Feedback.objects.filter(evaluatee__teacher__user__id=user_id)

        feedbacks = list(query)
        highest_fb = None

        for feedback in feedbacks:
            score = feedback.comment.sentiment_score
            hyb_pos = score.hybrid_pos
            hyb_neg = score.hybrid_neg
            hyb_total = hyb_pos - hyb_neg

            if highest_fb == None:
                highest_fb = feedback 
            else:
                # Calculate current highest feedback's score
                hfb_score = highest_fb.comment.sentiment_score
                hfb_hyb_pos = hfb_score.hybrid_pos
                hfb_hyb_neg = hfb_score.hybrid_neg 
                hfb_hyb_total = hfb_hyb_pos - hfb_hyb_neg

                if hyb_total > hfb_hyb_total:
                    highest_fb = feedback

        
        text = highest_fb.comment.text
        year_level = highest_fb.evaluator.year_level
        strand = highest_fb.evaluator.strand
        section = highest_fb.evaluator.section

        best_com = Comment(text, year_level, strand, section)

        return best_com
    
class SF_WorstComment:
    def __new__(self, request):
        user_id = request.user.id

        query = Feedback.objects.filter(evaluatee__teacher__user__id=user_id)

        feedbacks = list(query)
        lowest_fb = None

        for feedback in feedbacks:
            score = feedback.comment.sentiment_score
            hyb_pos = score.hybrid_pos
            hyb_neg = score.hybrid_neg
            hyb_total = hyb_pos - hyb_neg

            if lowest_fb == None:
                lowest_fb = feedback 
            else:
                # Calculate current highest feedback's score
                hfb_score = lowest_fb.comment.sentiment_score
                hfb_hyb_pos = hfb_score.hybrid_pos
                hfb_hyb_neg = hfb_score.hybrid_neg 
                hfb_hyb_total = hfb_hyb_pos - hfb_hyb_neg

                if hyb_total < hfb_hyb_total:
                    lowest_fb = feedback

        
        text = lowest_fb.comment.text
        year_level = lowest_fb.evaluator.year_level
        strand = lowest_fb.evaluator.strand
        section = lowest_fb.evaluator.section

        worst_com = Comment(text, year_level, strand, section)

        return worst_com
    
class SF_CommentReport:
    def __init__(self, request):
        user_id = request.user.id

        query = Feedback.objects.filter(evaluatee__teacher__user__id=user_id)
        feedbacks = list(query)

        self.comments_total = len(query)
        
        # Count comments today and this week
        self.comments_today = 0
        self.comments_thisweek = 0

        last_week = [datetime.today().date() - timedelta(days=i) for i in range(7)]

        for feedback in feedbacks:
            submit_date = feedback.submit_date.date()
            if submit_date == datetime.today().date():
                self.comments_today += 1

                if submit_date in last_week:
                    self.comments_thisweek += 1

        print("done")



